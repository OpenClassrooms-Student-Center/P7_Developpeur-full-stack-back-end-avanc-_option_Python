from django.db import models

ESTABLISHMENT_TYPES = [
    ("PHARMACIE", "Pharmacie"),
    ("HOPITAL", "Hôpital"),
    ("LABORATOIRE", "Laboratoire"),
    ("CLINIQUE", "Clinique"),
]


class Destinataire(models.Model):
    """Établissement de santé qui reçoit un transport."""

    nom = models.CharField(max_length=120)
    type_etablissement = models.CharField(max_length=30, choices=ESTABLISHMENT_TYPES)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=80)
    email_contact = models.EmailField()
    telephone_contact = models.CharField(max_length=20)

    class Meta:
        verbose_name = "destinataire"
        verbose_name_plural = "destinataires"

    def __str__(self) -> str:
        return f"{self.nom} ({self.ville})"


class Transport(models.Model):
    """Un transport de produits de santé, de son départ à sa livraison."""

    STATUSES = [
        ("PLANIFIE", "Planifié"),
        ("EN_COURS", "En cours"),
        ("LIVRE", "Livré"),
        ("INCIDENT", "Incident"),
    ]

    PRODUCT_TYPES = [
        ("MEDICAMENT", "Médicament"),
        ("DISPOSITIF", "Dispositif médical"),
        ("ECHANTILLON", "Échantillon biologique"),
    ]

    reference = models.CharField(max_length=20, unique=True)
    type_produit = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    destinataire = models.ForeignKey(
        Destinataire, on_delete=models.PROTECT, related_name="transports"
    )
    temperature_min = models.DecimalField(max_digits=5, decimal_places=1)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=1)
    date_depart = models.DateTimeField()
    date_arrivee_prevue = models.DateTimeField()
    date_livraison = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=15, choices=STATUSES, default="PLANIFIE")
    commentaire = models.TextField(blank=True, default="")
    nom_patient = models.CharField(max_length=120, blank=True, default="")
    date_naissance_patient = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "transport"
        verbose_name_plural = "transports"

    def __str__(self) -> str:
        return self.reference


class ReleveTemperature(models.Model):
    """Une mesure de température relevée pendant un transport."""

    transport = models.ForeignKey(
        Transport, on_delete=models.CASCADE, related_name="releves"
    )
    horodatage = models.DateTimeField()
    valeur = models.DecimalField(max_digits=5, decimal_places=1)
    hors_plage = models.BooleanField(default=False)

    class Meta:
        ordering = ["horodatage"]
        verbose_name = "relevé de température"
        verbose_name_plural = "relevés de température"

    def __str__(self) -> str:
        return f"{self.transport.reference} @ {self.horodatage:%d/%m/%Y %H:%M} : {self.valeur}°C"
