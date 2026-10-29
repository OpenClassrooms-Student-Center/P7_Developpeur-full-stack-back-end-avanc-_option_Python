import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Destinataire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=120)),
                (
                    "type_etablissement",
                    models.CharField(
                        choices=[
                            ("PHARMACIE", "Pharmacie"),
                            ("HOPITAL", "Hôpital"),
                            ("LABORATOIRE", "Laboratoire"),
                            ("CLINIQUE", "Clinique"),
                        ],
                        max_length=30,
                    ),
                ),
                ("adresse", models.CharField(max_length=255)),
                ("code_postal", models.CharField(max_length=10)),
                ("ville", models.CharField(max_length=80)),
                ("email_contact", models.EmailField(max_length=254)),
                ("telephone_contact", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name": "destinataire",
                "verbose_name_plural": "destinataires",
            },
        ),
        migrations.CreateModel(
            name="Transport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reference", models.CharField(max_length=20, unique=True)),
                (
                    "type_produit",
                    models.CharField(
                        choices=[
                            ("MEDICAMENT", "Médicament"),
                            ("DISPOSITIF", "Dispositif médical"),
                            ("ECHANTILLON", "Échantillon biologique"),
                        ],
                        max_length=20,
                    ),
                ),
                ("temperature_min", models.DecimalField(decimal_places=1, max_digits=5)),
                ("temperature_max", models.DecimalField(decimal_places=1, max_digits=5)),
                ("date_depart", models.DateTimeField()),
                ("date_arrivee_prevue", models.DateTimeField()),
                ("date_livraison", models.DateTimeField(blank=True, null=True)),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("PLANIFIE", "Planifié"),
                            ("EN_COURS", "En cours"),
                            ("LIVRE", "Livré"),
                            ("INCIDENT", "Incident"),
                        ],
                        default="PLANIFIE",
                        max_length=15,
                    ),
                ),
                ("commentaire", models.TextField(blank=True, default="")),
                (
                    "destinataire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transports",
                        to="transports.destinataire",
                    ),
                ),
            ],
            options={
                "verbose_name": "transport",
                "verbose_name_plural": "transports",
            },
        ),
        migrations.CreateModel(
            name="ReleveTemperature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("horodatage", models.DateTimeField()),
                ("valeur", models.DecimalField(decimal_places=1, max_digits=5)),
                ("hors_plage", models.BooleanField(default=False)),
                (
                    "transport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="releves",
                        to="transports.transport",
                    ),
                ),
            ],
            options={
                "verbose_name": "relevé de température",
                "verbose_name_plural": "relevés de température",
                "ordering": ["horodatage"],
            },
        ),
    ]
