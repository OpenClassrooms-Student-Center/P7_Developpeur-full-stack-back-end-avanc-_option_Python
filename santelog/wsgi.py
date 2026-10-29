"""Point d'entrée WSGI du projet Santélog, utilisé par gunicorn.

Lancement : python -m gunicorn santelog.wsgi:application
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "santelog.settings")

application = get_wsgi_application()
