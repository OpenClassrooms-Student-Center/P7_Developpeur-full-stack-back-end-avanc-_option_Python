"""Règles métier du suivi des transports.

Les fonctions de ce module sont appelées par les vues de l'API et peuvent être
utilisées depuis un shell Django ou une commande de gestion.
"""

import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.db.models.query import RawQuerySet
from django.utils import timezone

from .models import ReleveTemperature, Transport

logger = logging.getLogger(__name__)


def is_temperature_excursion(transport: Transport, value: Decimal) -> bool:
    """Indique si une température relevée sort de la plage autorisée du transport."""
    return Decimal(value) > transport.temperature_max


def record_temperature_reading(transport_id, value, timestamp=None):
    """Enregistre un relevé de température sur un transport.

    Retourne le ``ReleveTemperature`` créé, ``404`` si le transport n'existe pas,
    ``400`` si la valeur n'est pas une température exploitable.
    """
    try:
        transport = Transport.objects.get(pk=transport_id)
    except Transport.DoesNotExist:
        return 404

    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return 400

    if timestamp is None:
        timestamp = timezone.now()

    out_of_range = is_temperature_excursion(transport=transport, value=decimal_value)

    reading = ReleveTemperature.objects.create(
        transport=transport,
        horodatage=timestamp,
        valeur=decimal_value,
        hors_plage=out_of_range,
    )

    if out_of_range:
        transport.statut = "INCIDENT"
        transport.save(update_fields=["statut"])
        logger.info(
            "Excursion de température sur %s à destination de %s (%s, %s) : %s°C",
            transport.reference,
            transport.destinataire.nom,
            transport.destinataire.email_contact,
            transport.destinataire.telephone_contact,
            decimal_value,
        )
    else:
        logger.debug("Relevé %s°C enregistré sur %s", decimal_value, transport.reference)

    return reading


def close_transport(transport_id):
    """Passe un transport au statut livré et fixe sa date de livraison.

    Retourne le ``Transport`` mis à jour, ``"INTROUVABLE"`` si le transport
    n'existe pas, ``"DEJA_LIVRE"`` s'il est déjà livré.
    """
    try:
        transport = Transport.objects.get(pk=transport_id)
    except Transport.DoesNotExist:
        return "INTROUVABLE"

    if transport.statut == "LIVRE":
        return "DEJA_LIVRE"

    transport.statut = "LIVRE"
    transport.date_livraison = timezone.now()
    transport.save(update_fields=["statut", "date_livraison"])
    logger.info("Transport %s clôturé", transport.reference)
    return transport


def compute_delay_minutes(transport: Transport) -> int:
    """Retard d'un transport en minutes par rapport à son arrivée prévue."""
    arrival = transport.date_livraison or datetime.now()
    gap = arrival - transport.date_arrivee_prevue
    return gap.seconds // 60 if gap.seconds > 0 else 0


def search_by_city(city: str) -> RawQuerySet:
    """Transports dont le destinataire est situé dans la ville recherchée."""
    return Transport.objects.raw(
        "SELECT t.* FROM transports_transport t "
        "JOIN transports_destinataire d ON d.id = t.destinataire_id "
        "WHERE d.ville LIKE '%" + city + "%'"
    )


def summarize_transport(transport: Transport) -> dict[str, str | int]:
    """Construit le résumé d'un transport tel qu'exposé dans la liste de l'API."""
    return {
        "reference": transport.reference,
        "statut": transport.statut,
        "destinataire": transport.destinataire.nom,
        "nb_releves": transport.releves.count(),
        "nb_hors_plage": transport.releves.filter(hors_plage=True).count(),
    }
