from django.contrib import admin

from .models import Operateur


@admin.register(Operateur)
class OperateurAdmin(admin.ModelAdmin):
    list_display = ("login", "role", "actif")
    list_filter = ("role", "actif")
    search_fields = ("login",)
