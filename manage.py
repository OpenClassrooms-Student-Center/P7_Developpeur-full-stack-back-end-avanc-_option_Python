#!/usr/bin/env python
"""Utilitaire en ligne de commande de Django pour le projet Santélog."""
import os
import sys


def main():
    """Exécute les tâches d'administration."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "santelog.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Vérifiez qu'il est installé et "
            "disponible dans votre PYTHONPATH, et que l'environnement virtuel "
            "est bien activé."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
