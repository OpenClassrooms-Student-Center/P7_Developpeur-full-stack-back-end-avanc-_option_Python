from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Operateur",
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
                ("login", models.CharField(max_length=50, unique=True)),
                ("mot_de_passe", models.CharField(max_length=128)),
                (
                    "role",
                    models.CharField(
                        choices=[("OPERATEUR", "Opérateur"), ("RESPONSABLE", "Responsable")],
                        default="OPERATEUR",
                        max_length=20,
                    ),
                ),
                ("jeton", models.CharField(blank=True, default="", max_length=64)),
                ("actif", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "opérateur",
                "verbose_name_plural": "opérateurs",
            },
        ),
    ]
