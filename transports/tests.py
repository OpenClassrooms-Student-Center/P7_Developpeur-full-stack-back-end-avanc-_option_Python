from datetime import datetime, timezone as dt_timezone
from decimal import Decimal

from django.test import TestCase

from .models import Destinataire, ReleveTemperature, Transport
from .services import is_temperature_excursion, record_temperature_reading


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.recipient = Destinataire.objects.create(
            nom="Pharmacie des Tests",
            type_etablissement="PHARMACIE",
            adresse="1 rue du Test",
            code_postal="13000",
            ville="Marseille",
            email_contact="test@pharmacie.example",
            telephone_contact="04 00 00 00 00",
        )
        self.transport = Transport.objects.create(
            reference="TR-TEST-0001",
            type_produit="MEDICAMENT",
            destinataire=self.recipient,
            temperature_min=Decimal("2.0"),
            temperature_max=Decimal("8.0"),
            date_depart=datetime(2024, 11, 4, 6, 30, tzinfo=dt_timezone.utc),
            date_arrivee_prevue=datetime(2024, 11, 4, 9, 0, tzinfo=dt_timezone.utc),
        )

    def test_transport_str(self) -> None:
        self.assertEqual(str(self.transport), "TR-TEST-0001")

    def test_recipient_str(self) -> None:
        self.assertEqual(str(self.recipient), "Pharmacie des Tests (Marseille)")

    def test_record_temperature_reading_within_range(self) -> None:
        reading = record_temperature_reading(transport_id=self.transport.pk, value="5.0")
        self.assertIsInstance(reading, ReleveTemperature)
        self.assertFalse(reading.hors_plage)
        self.assertEqual(reading.transport, self.transport)

    def test_temperature_excursion_above_max(self) -> None:
        self.assertTrue(is_temperature_excursion(transport=self.transport, value=Decimal("9.5")))
