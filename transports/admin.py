from django.contrib import admin

from .models import Destinataire, ReleveTemperature, Transport


class ReleveTemperatureInline(admin.TabularInline):
    model = ReleveTemperature
    extra = 0


@admin.register(Destinataire)
class DestinataireAdmin(admin.ModelAdmin):
    list_display = ("nom", "type_etablissement", "ville")
    list_filter = ("type_etablissement",)
    search_fields = ("nom", "ville")


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ("reference", "type_produit", "destinataire", "statut", "date_depart")
    list_filter = ("statut", "type_produit")
    search_fields = ("reference",)
    inlines = [ReleveTemperatureInline]


@admin.register(ReleveTemperature)
class ReleveTemperatureAdmin(admin.ModelAdmin):
    list_display = ("transport", "horodatage", "valeur", "hors_plage")
    list_filter = ("hors_plage",)
