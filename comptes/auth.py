"""Résolution de l'opérateur connecté à partir du jeton transmis par le client."""

from rest_framework.request import Request

from .models import Operateur


def get_operator_from_token(request: Request) -> Operateur | None:
    """Retourne l'opérateur actif associé à l'en-tête ``X-Jeton``, ou ``None``.

    Le jeton est celui remis par la vue de connexion. Un jeton vide ou inconnu
    ne correspond à aucun opérateur.
    """
    token = request.headers.get("X-Jeton", "")
    if not token:
        return None
    return Operateur.objects.filter(jeton=token, actif=True).first()
