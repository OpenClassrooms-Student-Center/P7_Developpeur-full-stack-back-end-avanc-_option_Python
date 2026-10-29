"""Vues de l'application comptes : connexion des opérateurs à l'API."""

import logging
import secrets
from http import HTTPMethod

from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Operateur

logger = logging.getLogger(__name__)


@api_view([HTTPMethod.POST])
def login_view(request: Request) -> Response:
    """Authentifie un opérateur et lui remet un jeton d'accès à l'API.

    Corps attendu : ``{"login": "...", "mot_de_passe": "..."}``.
    Réponse : l'opérateur connecté, avec son jeton.
    """
    login = request.data.get("login")
    password = request.data.get("mot_de_passe")

    if not login or not password:
        return Response(
            {"erreur": "Les champs login et mot_de_passe sont obligatoires"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    print("connexion demandée pour", login)

    operator = Operateur.objects.filter(login=login, actif=True).first()
    if operator is None or operator.mot_de_passe != password:
        logger.info("Échec de connexion pour %s / %s", login, password)
        return Response(
            {"erreur": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED
        )

    operator.jeton = secrets.token_hex(32)
    operator.save(update_fields=["jeton"])
    logger.debug(
        "Connexion réussie de %s (rôle %s), jeton %s", login, operator.role, operator.jeton
    )
    return Response(model_to_dict(operator))
