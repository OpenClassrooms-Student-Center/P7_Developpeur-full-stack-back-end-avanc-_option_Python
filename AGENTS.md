# Guide pour les assistants IA travaillant sur ce dépôt

Ce fichier s'adresse aux assistants de programmation utilisés dans l'éditeur. Il décrit la posture attendue et le contexte du projet.

## Posture

- Aider à comprendre avant de produire : expliquer le fonctionnement d'un mécanisme (ORM, sérialiseur, vue DRF, middleware) avant d'écrire du code qui l'utilise.
- Procéder par petites étapes vérifiables. Après chaque modification, proposer la commande qui la vérifie (`pytest -v`, `python manage.py check`, un appel `curl`).
- Poser des questions quand l'intention n'est pas claire : quel comportement attendu, quel cas d'erreur, quel utilisateur concerné.
- Ne pas réécrire un module entier quand une modification locale suffit. Le développeur doit rester capable de relire et de justifier chaque ligne.
- Quand plusieurs approches existent, les présenter avec leurs compromis plutôt qu'imposer la première.

## Bonnes pratiques propres à cette stack

- Python 3.14.10, Django 6.1.2, Django REST Framework 3.18.3 : respecter ces versions, ne pas proposer d'API dépréciées ou absentes de ces versions.
- Organisation en applications Django (`models.py`, `views.py`, `serializers.py`, `urls.py`) : ne pas introduire de couches abstraites étrangères au cadre.
- La validation des données entrantes passe par les sérialiseurs DRF, pas par des vérifications dispersées dans les vues.
- La logique métier vit dans `transports/services.py` ou dans les modèles, pas dans les vues.
- Toute modification de modèle s'accompagne d'une migration générée par `makemigrations` et committée.
- PEP 8 ; `black` pour le formatage, `ruff` ou `flake8` pour les signalements.
- Annotations de type bienvenues sur les signatures publiques.
- Tests avec pytest et pytest-django ; doublures avec `unittest.mock` ou `pytest-mock` ; couverture avec `coverage.py`.

## Mises en garde

- Aucun secret (clé, mot de passe, jeton) dans le code ni dans les messages : les valeurs vont dans `.env`, les noms de variables dans `.env.example`.
- Ne jamais faire confiance aveuglément au code généré : le relire, l'exécuter, le tester avant de le committer.
- Les données manipulées concernent des transports de produits de santé et des coordonnées d'établissements : ne pas les copier dans des exemples, des journaux ou des prompts externes.
- Ne pas proposer de désactiver une protection (CSRF, validation, contrôle d'accès) pour « faire passer » un test ou une requête.

## Architecture de ce projet

- `santelog/` : configuration du projet (settings, routage racine, WSGI pour gunicorn).
- `comptes/` : modèle `Operateur`, connexion (`POST /api/comptes/connexion/`) et résolution de l'opérateur depuis l'en-tête `X-Jeton`.
- `transports/` : modèles `Destinataire`, `Transport`, `ReleveTemperature` ; services métier (vérification d'excursion de température, enregistrement de relevé, clôture, résumé, retard, recherche) ; vues fonction DRF ; sérialiseurs ; fixture `donnees_demo.json`.
- `.github/workflows/ci.yml` : intégration continue GitHub Actions.
- Base SQLite locale (`db.sqlite3`, hors dépôt).
- Fichiers statiques (interface d'administration) servis par WhiteNoise, après `python manage.py collectstatic` dans `staticfiles/` (hors dépôt).

## Commandes utiles

```bash
python manage.py migrate
python manage.py loaddata donnees_demo
python manage.py runserver
pytest -v
coverage run -m pytest && coverage report
```
