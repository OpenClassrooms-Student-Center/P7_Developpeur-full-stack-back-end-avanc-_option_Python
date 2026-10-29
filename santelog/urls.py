"""Routage racine du projet Santélog."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/comptes/", include("comptes.urls")),
    path("api/", include("transports.urls")),
]
