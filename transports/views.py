"""Vues de l'API de suivi des transports."""

import logging
from http import HTTPMethod

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from comptes.auth import get_operator_from_token

from .models import Destinataire, Transport
from .serializers import (
    DestinataireSerializer,
    ReleveTemperatureSerializer,
    TransportSerializer,
)
from .services import (
    close_transport,
    compute_delay_minutes,
    record_temperature_reading,
    search_by_city,
    summarize_transport,
)

logger = logging.getLogger(__name__)

REQUIRED_TRANSPORT_FIELDS = [
    "reference",
    "type_produit",
    "destinataire",
    "temperature_min",
    "temperature_max",
    "date_depart",
    "date_arrivee_prevue",
]


@api_view([HTTPMethod.GET, HTTPMethod.POST])
def transport_list(request: Request) -> Response:
    """GET : résumé de tous les transports. POST : création d'un transport."""
    if request.method == HTTPMethod.GET:
        results = []
        for transport in Transport.objects.all():
            results.append(summarize_transport(transport=transport))
        return Response(results)

    for field in REQUIRED_TRANSPORT_FIELDS:
        if request.data.get(field) in (None, ""):
            return Response(
                {"erreur": f"Le champ {field} est obligatoire"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    recipient = Destinataire.objects.filter(pk=request.data.get("destinataire")).first()
    if recipient is None:
        return Response(
            {"erreur": "Destinataire inconnu"}, status=status.HTTP_400_BAD_REQUEST
        )

    transport = Transport.objects.create(
        reference=request.data.get("reference"),
        type_produit=request.data.get("type_produit"),
        destinataire=recipient,
        temperature_min=request.data.get("temperature_min"),
        temperature_max=request.data.get("temperature_max"),
        date_depart=request.data.get("date_depart"),
        date_arrivee_prevue=request.data.get("date_arrivee_prevue"),
        statut=request.data.get("statut", "PLANIFIE"),
        commentaire=request.data.get("commentaire", ""),
    )
    logger.info(
        "Transport %s créé pour %s (%s)",
        transport.reference,
        recipient.nom,
        recipient.email_contact,
    )
    return Response(TransportSerializer(transport).data, status=status.HTTP_201_CREATED)


@api_view([HTTPMethod.GET])
def transport_detail(request, pk):
    """Détail complet d'un transport."""
    try:
        transport = Transport.objects.get(pk=pk)
    except Transport.DoesNotExist:
        return JsonResponse({"erreur": "Transport introuvable"}, status=404)
    return JsonResponse(model_to_dict(transport))


@api_view([HTTPMethod.GET])
def transport_delay(request: Request, pk: int) -> Response:
    """Retard d'un transport, en minutes."""
    try:
        transport = Transport.objects.get(pk=pk)
    except Transport.DoesNotExist:
        return Response(
            {"erreur": "Transport introuvable"}, status=status.HTTP_404_NOT_FOUND
        )
    return Response(
        {
            "reference": transport.reference,
            "retard_minutes": compute_delay_minutes(transport=transport),
        }
    )


@api_view([HTTPMethod.GET])
def transport_search(request: Request) -> Response:
    """Recherche des transports par ville de destination."""
    city = request.query_params.get("ville", "")
    return Response(TransportSerializer(search_by_city(city=city), many=True).data)


@api_view([HTTPMethod.GET, HTTPMethod.POST])
def transport_readings(request: Request, pk: int) -> Response:
    """GET : relevés d'un transport. POST : ajout d'un relevé de température."""
    if request.method == HTTPMethod.GET:
        try:
            transport = Transport.objects.get(pk=pk)
        except Transport.DoesNotExist:
            return Response(
                {"erreur": "Transport introuvable"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(ReleveTemperatureSerializer(transport.releves.all(), many=True).data)

    try:
        timestamp = request.data.get("horodatage")
        if timestamp:
            timestamp = parse_datetime(timestamp)
        else:
            timestamp = None
        result = record_temperature_reading(
            transport_id=pk, value=request.data.get("valeur"), timestamp=timestamp
        )
    except Exception as exc:
        return Response({"erreur": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if result == 404:
        return Response(
            {"erreur": "Transport introuvable"}, status=status.HTTP_404_NOT_FOUND
        )
    if result == 400:
        return Response(
            {"erreur": "Valeur de température invalide"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        ReleveTemperatureSerializer(result).data, status=status.HTTP_201_CREATED
    )


@api_view([HTTPMethod.POST])
def transport_close(request: Request, pk: int) -> Response:
    """Clôture un transport (livraison effectuée). Réservé aux opérateurs connectés."""
    operator = get_operator_from_token(request=request)
    if operator is None:
        return Response(
            {"erreur": "Jeton manquant ou invalide"}, status=status.HTTP_401_UNAUTHORIZED
        )

    result = close_transport(transport_id=pk)
    if result == "INTROUVABLE":
        return Response(
            {"erreur": "Transport introuvable"}, status=status.HTTP_404_NOT_FOUND
        )
    if result == "DEJA_LIVRE":
        return Response(
            {"erreur": "Ce transport est déjà livré"}, status=status.HTTP_409_CONFLICT
        )

    logger.info("Transport %s clôturé par %s", result.reference, operator.login)
    return Response(TransportSerializer(result).data)


@api_view([HTTPMethod.GET])
def recipient_list(request: Request) -> Response:
    """Liste des établissements destinataires."""
    return Response(DestinataireSerializer(Destinataire.objects.all(), many=True).data)
