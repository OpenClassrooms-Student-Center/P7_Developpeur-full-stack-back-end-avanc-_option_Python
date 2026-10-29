# Santélog — Suivi des transports

API interne de l'équipe Suivi Transports de Santélog. Elle trace chaque transport de produits de santé (médicaments, dispositifs médicaux, échantillons biologiques), les relevés de température effectués en route et les établissements destinataires.

L'interface web de suivi (écran de suivi des transports, tableau de bord) est maintenue par une autre équipe et consomme cette API.

## Prérequis

- Python 3.14.10 (`python --version`)
- `pip` et le module `venv`
- Git

## Installation

```bash
git clone <url-du-depot> santelog-suivi-transports
cd santelog-suivi-transports
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Renseigner `DJANGO_SECRET_KEY` dans `.env` avant tout usage hors poste de développement.

## Lancement

```bash
python manage.py migrate
python manage.py loaddata donnees_demo
python manage.py runserver
```

L'API répond sur `http://127.0.0.1:8000/api/`. L'interface d'administration Django est disponible sur `/admin/` après création d'un compte avec `python manage.py createsuperuser`.

En production, l'application est servie par gunicorn. Les fichiers statiques (CSS et JavaScript de l'interface d'administration) sont d'abord rassemblés dans `staticfiles/`, puis servis par WhiteNoise :

```bash
python manage.py collectstatic --noinput
python -m gunicorn santelog.wsgi:application --bind 0.0.0.0:8000
```

## Stack technique

| Composant | Version |
|---|---|
| Python | 3.14.10 |
| Django | 6.1.2 |
| Django REST Framework | 3.18.3 |
| Base de données | SQLite (fichier `db.sqlite3`) |
| Serveur applicatif | gunicorn |
| Fichiers statiques | WhiteNoise |
| Tests | pytest, pytest-django, coverage |

## Structure du projet

```
.
├── manage.py
├── requirements.txt
├── pytest.ini
├── .coveragerc          # configuration de la mesure de couverture
├── santelog/            # configuration du projet Django (settings, urls, wsgi)
├── comptes/             # opérateurs de l'équipe et connexion à l'API
│   ├── models.py        # Operateur
│   ├── auth.py          # résolution de l'opérateur depuis l'en-tête X-Jeton
│   └── views.py         # connexion
├── transports/          # cœur métier
│   ├── models.py        # Destinataire, Transport, ReleveTemperature
│   ├── serializers.py
│   ├── services.py      # règles métier (excursion, relevés, clôture)
│   ├── views.py         # vues de l'API
│   ├── tests.py
│   └── fixtures/donnees_demo.json
├── starter-kit/         # documents partagés avec le dépôt
└── .github/workflows/   # intégration continue
```

## Points d'entrée de l'API

### Comptes

| Méthode | Route | Description |
|---|---|---|
| POST | `/api/comptes/connexion/` | Connexion d'un opérateur (`login`, `mot_de_passe`), renvoie un jeton |

Le jeton obtenu se transmet ensuite dans l'en-tête HTTP `X-Jeton`.

### Transports

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/transports/` | Résumé de tous les transports (statut, destinataire, nombre de relevés) |
| POST | `/api/transports/` | Création d'un transport |
| GET | `/api/transports/<id>/` | Détail d'un transport |
| GET | `/api/transports/<id>/retard/` | Retard d'un transport (en minutes) |
| GET | `/api/transports/recherche/?ville=` | Recherche des transports par ville de destination |
| GET | `/api/transports/<id>/releves/` | Relevés de température d'un transport |
| POST | `/api/transports/<id>/releves/` | Ajout d'un relevé (`valeur`, `horodatage` optionnel) |
| POST | `/api/transports/<id>/cloturer/` | Clôture d'un transport livré (en-tête `X-Jeton` requis) |
| GET | `/api/destinataires/` | Liste des établissements destinataires |

Exemple d'ajout de relevé :

```bash
curl -X POST http://127.0.0.1:8000/api/transports/2/releves/ \
  -H "Content-Type: application/json" \
  -d '{"valeur": "-19.0"}'
```

Les données de démonstration contiennent les comptes `evasseur`, `kmartin` et `svc-export`, dont les identifiants sont dans la fixture `transports/fixtures/donnees_demo.json`.

## Scripts

| Commande | Rôle |
|---|---|
| `python manage.py runserver` | Serveur de développement |
| `python manage.py migrate` | Application des migrations |
| `python manage.py loaddata donnees_demo` | Chargement des données de démonstration |
| `pytest -v` | Exécution de la suite de tests |
| `python manage.py test` | Idem, via le lanceur Django |
| `coverage run -m pytest && coverage report` | Couverture de la suite de tests |
| `python manage.py check` | Vérification de la configuration |

## Intégration continue

Le workflow GitHub Actions `.github/workflows/ci.yml` s'exécute sur la branche `main`.

## Licence

Logiciel interne Santélog. Tous droits réservés. Usage restreint aux équipes de l'entreprise.
