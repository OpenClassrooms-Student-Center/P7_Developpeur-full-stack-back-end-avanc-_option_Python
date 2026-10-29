from django.db import models

ROLES = [
    ("LIVREUR", "Livreur"),
    ("RESPONSABLE", "Responsable"),
    ("ADMIN", "Administrateur"),
]


class Operateur(models.Model):
    """Compte d'un membre de l'équipe Suivi Transports autorisé à utiliser l'API."""

    login = models.CharField(max_length=50, unique=True)
    mot_de_passe = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLES, default="LIVREUR")
    jeton = models.CharField(max_length=64, blank=True, default="")
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "opérateur"
        verbose_name_plural = "opérateurs"

    def __str__(self) -> str:
        return self.login
