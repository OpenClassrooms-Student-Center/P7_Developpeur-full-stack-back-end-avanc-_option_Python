:::meta
titre: Sécurisez, déployez et maintenez une application full-stack
parcours: Développeur Full-stack back-end avancé
numero_projet: P7
variation_scenario: standard
nb_missions: 1
guidage: peu_guide
duree_supervisee_h: 45
duree_personnelle_h: 45
competence_1: Mettre en œuvre les configurations critiques, les mécanismes de protection et de défense sur les actifs, les flux et les données
competence_2: Concevoir et mettre en œuvre une stratégie de tests automatisés ou non
competence_3: Concevoir, mettre en œuvre et maintenir les pipelines d'intégration et de déploiement continu (CI/CD)
competence_4: Assurer la maintenance préventive, corrective et évolutive
:::

# Page d'accueil

## Qu'allez-vous apprendre dans ce projet ?

Une équipe vous confie une application en production, avec ses défauts accumulés, et attend que vous la remettiez sur des bases fiables. C'est exactement ce que vous allez faire ici : diagnostiquer une application existante, repérer ses failles de sécurité, ses tests incomplets, sa configuration fragile et sa dette technique, puis décider par quoi commencer et le justifier.

Vous allez ensuite mettre en œuvre les protections qui manquent : contrôle des accès par authentification, validation des entrées, protection des données stockées et échangées, en vous appuyant sur les référentiels de vulnérabilités reconnus. Vous documenterez ce travail dans une **note de sécurisation technique**, avec un tableau des vulnérabilités traitées et une cartographie des flux chiffrés et des privilèges.

Vous construirez aussi un filet de sécurité vérifiable : une stratégie de tests automatisés assumée, avec un **rapport de couverture de code** généré automatiquement, et un pipeline d'intégration et de déploiement continu qui construit, teste et empaquette l'application à chaque modification.

Enfin, vous tiendrez un **journal de maintenance** : les preuves de votre diagnostic, de votre audit et de vos refactorisations, pour que l'équipe puisse reprendre derrière vous. C'est la différence entre corriger un code et maintenir une application.

## En quoi ces compétences sont-elles importantes pour votre carrière ?

La grande majorité des postes de développement portent sur des applications existantes, pas sur des pages blanches. Savoir auditer un code que vous n'avez pas écrit, prioriser les corrections et sécuriser les données est ce qui distingue un développeur confirmé d'un développeur qui exécute des tickets. C'est aussi ce que les recruteurs testent en entretien technique : pas la syntaxe, mais les arbitrages.

Avec la généralisation des assistants d'intelligence artificielle qui produisent du code, la valeur du développeur se déplace vers la garantie de qualité : tester, sécuriser, vérifier, documenter. Ces compétences sont demandées dans tous les secteurs, et particulièrement là où les données sont sensibles : santé, finance, logistique réglementée.

## Comment allez-vous procéder ?

- **Exercice optionnel : Déployez et maintenez une application** : sur une petite base de code fournie, vous suivrez des étapes guidées pour conteneuriser l'application, automatiser sa construction et mettre en place un monitoring basique. Un échauffement avant la mission.
- **Mission 1 : Garantissez la maintenance, la sécurité et la qualité d'une application** : sur une application complète, vous mènerez le diagnostic, la sécurisation, la stratégie de tests, l'automatisation de la livraison et la documentation de maintenance. Cette mission est volontairement peu guidée.

À l'issue de ce projet, vous présenterez les livrables de la mission à un mentor évaluateur lors d'une soutenance. Cela vous permettra de valider les compétences visées par ce projet.

:::encadre type=info
Ce projet mobilise tout ce que vous avez construit dans les projets précédents, en particulier la mise en place de tests automatisés pour valider la qualité du code. Si vous ne maîtrisez pas une ou plusieurs notions techniques (vulnérabilités applicatives, authentification, tests automatisés, pipelines, conteneurisation), prenez le temps de suivre les cours associés et de réaliser l'exercice optionnel si votre planning le permet, puis sollicitez votre mentor, votre tuteur en entreprise, la communauté Circle et Companion.
:::

## Prêt à démarrer votre projet ?

Lancez-vous dans la première section « Exercice optionnel — Déployez et maintenez une application ».

:::encadre type=info
**Votre projet démarre : suivez ces quelques recommandations pour être plus efficace !**

- Coupez dès à présent toutes les sources de distraction : téléphone, messagerie, mails, notifications, etc.
- Évitez les situations de multitâches : n'écoutez pas un podcast ou les informations en travaillant.
- Préparez votre environnement de travail : onglets, documents téléchargés, raccourcis, etc.

Vous avez toutes les cartes en main, c'est parti ! Pour plus de conseils, suivez ce chapitre de cours : Mettez en place votre environnement d'apprentissage.
:::

---

# Exercice optionnel — Déployez et maintenez une application (Python)

Vous recevez une petite application au périmètre volontairement limité : **MiniLien**, un service de raccourcissement d'URL en Django. On lui donne une adresse longue, il renvoie un lien court qui redirige vers l'adresse d'origine et compte les visites. Elle fonctionne sur votre poste en local, et c'est tout : pas de conteneur, pas d'automatisation, pas de monitoring. Vous allez combler ces trois manques, dans cet ordre, en suivant les étapes guidées.

### Étape A — Conteneurisez l'application avec Docker

**Prérequis :**

- avoir cloné le dépôt et vérifié que `pip install -r requirements.txt` puis `python manage.py test` passent sur votre poste ;
- avoir installé Docker et vérifié son fonctionnement avec `docker run hello-world`.

**Résultats attendus :**

- un `Dockerfile` à la racine du dépôt, qui installe les dépendances et sert l'application avec `gunicorn` dans une image basée sur une image Python slim ;
- une **image Docker** qui se construit avec `docker build` et se lance avec `docker run`, l'application répondant sur le port exposé.

**Recommandations :**

- Séparez l'installation des dépendances de la copie du code applicatif dans le `Dockerfile` : cela permet à Docker de mettre en cache la couche des dépendances tant que `requirements.txt` ne change pas.
- Externalisez la configuration (port, identifiants) en variables d'environnement plutôt qu'en dur dans `settings.py`.

**Points de vigilance :**

- Une image qui embarque des identifiants en clair est une mauvaise habitude à corriger dès maintenant : vous la retrouverez en critère bloquant dans la mission.

### Étape B — Automatisez la construction avec GitHub Actions

**Prérequis :**

- avoir poussé le dépôt sur GitHub ;
- avoir un `Dockerfile` fonctionnel (étape A).

**Résultats attendus :**

- un fichier de workflow dans `.github/workflows/` qui, à chaque push, installe les dépendances et lance `pytest`, puis construit l'image Docker ;
- une exécution verte du workflow, visible dans l'onglet Actions du dépôt.

**Recommandations :**

- Commencez par un workflow minimal (checkout, installation de Python, installation des dépendances, `pytest`), vérifiez qu'il passe, puis ajoutez la construction de l'image. Un workflow se construit par itérations courtes.

**Points de vigilance :**

- Un workflow qui construit l'image sans avoir exécuté les tests avant livre du code non vérifié : l'ordre des étapes du pipeline porte du sens.

### Étape C — Mettez en place un monitoring basique

**Prérequis :**

- avoir l'application conteneurisée et lançable (étape A).

**Résultats attendus :**

- l'exposition de métriques de base de l'application (santé, temps de réponse, utilisation mémoire) via l'instrumentation OpenTelemetry ou un endpoint de santé dédié ;
- un tableau de bord Grafana minimal affichant au moins 2 de ces métriques.

**Recommandations :**

- Restez au niveau basique : l'objectif est de savoir dire si l'application est vivante et comment elle se comporte, pas de construire une supervision de production.

**Points de vigilance :**

- Un tableau de bord qui affiche des métriques que vous ne savez pas interpréter n'a pas de valeur : pour chaque courbe, sachez dire ce qu'un pic signifierait.

---

# Mission 1 — Garantissez la maintenance, la sécurité et la qualité d'une application (Python)

**Conseils mentor**

Pendant la mission, demandez à votre étudiant de vous parler de :

1. son avancement ;
2. ses difficultés ;
3. sa compréhension de l'exercice.

Vous pourrez ainsi identifier ses problèmes, ses lacunes, ses processus ou méthodologies erronés.

**Compréhension des attendus**

Assurez-vous que l'étudiant puisse répondre à ces questions : Que doivent contenir les livrables ? À quoi ressembleront-ils ? Quel est le niveau de précision attendu ?

**Lacunes récurrentes**

Cette mission suppose acquises les compétences de test des projets P4 et P6 : si votre étudiant n'est pas à l'aise avec pytest, pytest-mock ou la logique de la pyramide de tests, renvoyez-le vers les cours associés et l'exercice optionnel avant qu'il n'avance sur l'étape 3. Deuxième fragilité fréquente : la distinction entre authentification et autorisation dans Django REST Framework (classes d'authentification et classes de permission), et la lecture d'un flux OAuth2.

**Méthodologie**

L'ordre de travail recommandé est celui des étapes : d'abord l'audit et la priorisation, ensuite la sécurisation, puis les tests, le pipeline, et enfin les refactorisations. Vérifiez que l'étudiant tient son journal de maintenance au fil de l'eau, et non reconstitué la veille de la soutenance : demandez à le voir dès la première séance.

**Points de vigilance**

Cette mission est volontairement peu guidée : ne fournissez pas de plan d'action à l'étudiant, aidez-le à construire le sien. Deux erreurs invalident tout en aval : une priorisation absente (des corrections en vrac sans diagnostic préalable) et une suite de tests qui ne passe pas avec `pytest` au moment de la soutenance.

:::encadre type=autoeval
Les critères d'évaluation sont dans le guide mentor du projet.
Cependant, l'étudiant a accès à une **fiche d'autoévaluation** dans la dernière étape de son travail.
Elle contient des critères moins détaillés que les vôtres.
L'étudiant peut l'utiliser comme base de discussion avec vous mais surtout comme checklist pour vérifier qu'il n'a rien oublié.
:::

## Comment allez-vous procéder ?

Cette mission suit un scénario de projet professionnel. Elle est **volontairement très peu guidée** pour vous inciter à prendre vos propres décisions : les étapes fixent des objectifs et des attendus, pas un pas-à-pas. C'est vous qui construisez le plan d'action, et c'est ce plan qu'on évaluera autant que le code.

Si vous êtes en poste, vous pouvez mener cette mission sur une application réelle de votre entreprise, avec l'accord de votre tuteur, à condition qu'elle permette de produire les mêmes livrables. Sinon, suivez le scénario fictif ci-dessous.

Avant de démarrer, nous vous conseillons de :

- lire toute la mission et ses documents liés ;
- prendre des notes sur ce que vous avez compris ;
- consulter les étapes pour vous guider ;
- préparer une liste de questions pour votre session de mentorat.

:::encadre type=info
**Quelques conseils de méthodologie de travail :**

**Sur la construction du projet :** Soyez prêt à détailler votre processus de décision. Exemples : pourquoi avoir traité cette vulnérabilité avant celle-là ? Pourquoi avoir écrit un test unitaire plutôt qu'un test d'intégration sur ce module ?

**Sur l'usage de l'IA :** Si vous utilisez des outils d'intelligence artificielle, vous devez être capable d'expliquer comment vous avez vérifié et adapté le contenu produit. L'IA doit être un assistant à la compréhension, pas un substitut à votre diagnostic et à vos arbitrages techniques.
:::

## Prêt à mener la mission ?

Vous êtes développeur expérimenté chez Santélog, une entreprise régionale de logistique spécialisée dans le transport de produits de santé : médicaments, dispositifs médicaux, échantillons biologiques. L'équipe Suivi Transports maintient l'application Python qui trace chaque transport, ses températures, ses destinataires. Une V2 est attendue par la direction, mais l'équipe, sous l'eau depuis des mois, a perdu le recul sur l'état réel de son application. Votre manager et Élodie Vasseur, la responsable de l'équipe, viennent de valider votre prêt inter-équipes.

Avant même votre première journée dans l'équipe, ce message vous attend sur Teams.

:::artefact canal=teams de="Élodie Vasseur" fonction="Responsable de l'équipe Suivi Transports" canal_nom="Message direct"
**Élodie Vasseur — 9 h 12**

Salut, c'est officiel depuis ce matin : tu nous rejoins sur l'appli de suivi des transports. Je préfère être franche : on n'a pas le recul qu'il faudrait. La V2 est attendue, et personne ici ne peut te dire aujourd'hui où on en est vraiment côté sécurité, tests ou livraisons.

**Élodie Vasseur — 9 h 14**

Je te pose ce que j'attends, dans l'ordre :

1. Un état des lieux honnête de l'application, et surtout : par quoi commencer. Je ne veux pas une liste de 40 problèmes, je veux savoir ce qui est urgent, ce qui peut attendre, et pourquoi.
2. Les données qu'on transporte sont sensibles, certaines relèvent de la santé. Protège les accès, les échanges et ce qu'on stocke. Et laisse-nous une trace écrite de ce que tu as traité : qui a le droit de faire quoi, ce qui circule chiffré, ce qui ne l'était pas.
3. Aujourd'hui, personne ne sait si une modif casse quelque chose ailleurs. Il nous faut un filet de sécurité vérifiable avant chaque changement, avec de quoi mesurer ce qui est couvert et ce qui ne l'est pas.
4. Nos livraisons sont artisanales : chacun construit et déploie à sa façon. Automatise ça pour que chaque modification soit construite, testée et empaquetée de la même manière, sans intervention manuelle.
5. Et surtout : laisse l'équipe en état de reprendre derrière toi. Corrige ce qui doit l'être dans le code, et documente tout ce que tu fais : ce que tu as trouvé, ce que tu as décidé, ce que tu as changé.

**Élodie Vasseur — 9 h 16**

Je t'envoie dans l'heure les accès au dépôt de l'application et la note de contexte que l'équipe a rédigée sur les problèmes connus. Elle est incomplète, c'est justement le problème. On se cale un point jeudi ?

**Fichiers partagés :** dépôt Git de l'application de suivi des transports, note de contexte de l'équipe (problèmes connus et attentes pour la V2)
:::

Les cinq demandes d'Élodie structurent votre travail. Les étapes ci-dessous en donnent les objectifs et les attendus ; le chemin pour y arriver est le vôtre.

### Étape 1 — Diagnostiquez l'application et priorisez vos actions

**Objectif :** établir un état des lieux factuel de l'application (code, configuration, tests, journalisation, pipeline, dette technique) et en tirer un plan d'action priorisé et justifié.

**Attendus concrets :**

- un **audit initial** consigné dans le journal de maintenance : pour chaque famille de problèmes constatée (validation des entrées, gestion des erreurs, tests, configuration, logs, pipeline, dette), une preuve concrète (extrait de code, sortie de commande, capture) ;
- un **plan d'action priorisé** : ce que vous traitez d'abord, ce que vous reportez, et le critère de priorisation (risque sur les données, impact sur la V2, effort).

**Recommandations :**

- Outillez votre audit : `pytest -v` pour l'état de la suite existante, le rapport `coverage report` pour la couverture réelle, une analyse `ruff` ou `flake8` pour objectiver la dette. Un chiffre constaté vaut mieux qu'une impression.
- Lisez la note de contexte de l'équipe, puis vérifiez chacune de ses affirmations dans le code : c'est l'écart entre les deux qui fait la valeur de votre diagnostic.
- Parcourez l'organisation en applications Django (`models.py`, `views.py`, `serializers.py`) : les défauts de découpage (modèle exposé directement au lieu d'un sérialiseur, code d'erreur renvoyé depuis une fonction métier) sont des marqueurs de dette à noter dès maintenant.

**Points de vigilance :**

- Se lancer dans les corrections sans diagnostic préalable ni priorisation argumentée peut motiver un refus en soutenance : c'est la compétence de maintenance elle-même qui est en jeu, pas seulement le résultat.

### Étape 2 — Sécurisez les actifs, les flux et les données

**Objectif :** traiter les vulnérabilités identifiées à l'audit, mettre en place le contrôle des accès et protéger les données stockées et échangées, puis en rendre compte dans la **note de sécurisation technique**.

**Attendus concrets :**

- les vulnérabilités traitées dans le code, référencées par rapport à l'OWASP Top 10 dans sa version 2025 (le référentiel des 10 catégories de vulnérabilités applicatives les plus critiques) ;
- une authentification OAuth2 avec jetons JWT mise en œuvre via Django REST Framework (ou son système d'authentification natif), et des autorisations différenciées par rôle ;
- la validation des entrées par les sérialiseurs DRF (ou les modèles Pydantic) plutôt que par des vérifications manuelles dispersées ;
- la protection des données stockées : mots de passe hachés avec un algorithme adapté (le hachage PBKDF2 ou Argon2 du système d'authentification Django), secrets sortis du code et de `settings.py`, et secrets déjà exposés dans l'historique Git traités (révocation et remplacement, purge de l'historique si vous la jugez nécessaire) ;
- la **note de sécurisation technique** : le lien vers le dépôt, un tableau récapitulant les vulnérabilités traitées (catégorie OWASP, localisation, correction apportée), et la cartographie des flux chiffrés et des privilèges — c'est elle qui rend compte de la protection des échanges : quels flux circulent chiffrés, où se fait la terminaison TLS (le point où le chiffrement des échanges s'arrête), et qui accède à quoi.

**Recommandations :**

- Pour chaque mécanisme de sécurité que vous posez, sachez dire ce qu'il déclenche : une configuration Django REST Framework copiée sans être comprise se voit immédiatement en soutenance.
- La cartographie des privilèges est un document de communication : Élodie doit pouvoir la lire sans ouvrir le code.
- Les données transportées relèvent en partie de la santé : vos choix de protection doivent se justifier au regard du RGPD (le règlement européen sur la protection des données personnelles), pas seulement de la technique.

**Points de vigilance :**

- Des secrets (mots de passe, clés) laissés en clair dans le dépôt, ou exposés dans l'historique sans avoir été révoqués, ou des mots de passe stockés sans hachage, peuvent motiver un refus en soutenance.

### Étape 3 — Concevez et mettez en œuvre la stratégie de tests

**Objectif :** construire le filet de sécurité demandé : une stratégie de tests explicite, mise en œuvre dans le dépôt, avec une couverture mesurée automatiquement.

**Attendus concrets :**

- une stratégie de tests écrite (dans le dépôt ou le journal de maintenance) : ce que vous testez en unitaire, en intégration, via l'API, et ce que vous choisissez de ne pas automatiser, avec la justification, en cohérence avec la pyramide de tests (beaucoup de tests unitaires rapides, moins de tests d'intégration, encore moins de tests de bout en bout) ;
- des tests unitaires pytest avec `pytest-mock` pour les doublures, ciblant en priorité les règles métier des services ;
- des tests d'intégration et des tests d'API sur les vues via le client de test DRF (`APIClient`), sur une base de données réelle éphémère (Testcontainers, ou une alternative que vous justifiez) ;
- une suite qui passe intégralement avec `pytest` ;
- un **rapport de couverture de code** généré automatiquement par `coverage.py` lors du build.

**Recommandations :**

- Distinguez le mock d'une dépendance isolée et le test qui sollicite la base de test Django : le premier ne charge pas l'application, le second démarre le contexte entier. Un test qui charge toute l'application pour vérifier une règle de calcul est un test lent pour rien.
- L'injection explicite des dépendances dans les fonctions, plutôt que leur résolution implicite dans le corps de la vue, est ce qui rend vos services testables sans base de données : si une fonction résiste au test unitaire, c'est souvent sa construction qu'il faut corriger d'abord.
- Visez la couverture des zones à risque avant le pourcentage global : 100 % sur les sérialiseurs triviaux n'a jamais protégé personne.

**Points de vigilance :**

- Une suite de tests qui ne passe pas avec `pytest` au moment de la soutenance peut motiver un refus : le filet de sécurité qui ne tient pas n'est pas un filet.
- Un rapport de couverture produit à la main ou par capture retouchée, plutôt que généré par le build, peut motiver un refus.

### Étape 4 — Complétez et fiabilisez le pipeline CI/CD

**Objectif :** transformer les livraisons artisanales en un pipeline d'intégration et de déploiement continu : chaque modification est construite, testée et empaquetée automatiquement, de la même manière, à chaque fois.

**Attendus concrets :**

- le fichier de configuration du pipeline GitHub Actions dans `.github/workflows/`, complété à partir du pipeline incomplet existant ;
- un pipeline qui, sur chaque push et pull request : installe les dépendances depuis `requirements.txt`, exécute `pytest`, génère le rapport `coverage.py` et construit l'image Docker de l'application, dans cet ordre, et échoue si les tests échouent ;
- au moins une exécution verte du pipeline, visible dans l'historique du dépôt.

**Recommandations :**

- Auditez d'abord le pipeline existant : ce qui manque, ce qui est mal ordonné, ce qui échoue silencieusement. La complétion argumentée vaut mieux que la réécriture de zéro.
- Le `Dockerfile` suit la même logique qu'à l'exercice optionnel : l'application installée dans un environnement virtuel, servie par `gunicorn`, la configuration en variables d'environnement.

**Points de vigilance :**

- Un pipeline qui construit l'image sans exécuter les tests, ou qui reste vert alors que les tests échouent, contredit tout le travail de l'étape 3 : vérifiez l'ordre et les conditions d'échec de chaque étape.

### Étape 5 — Corrigez, refactorisez et documentez la maintenance

**Objectif :** livrer le code amélioré et débogué, refactoriser les modules les plus endettés, et compléter le **journal de maintenance** pour que l'équipe reprenne l'application en connaissance de cause.

**Attendus concrets :**

- les défauts identifiés à l'audit corrigés dans le code : gestion des erreurs centralisée (exceptions métier en classes dédiées, traduites en réponses HTTP par un gestionnaire d'exceptions DRF), validation des entrées généralisée, logs rendus exploitables (niveaux cohérents, contexte suffisant, aucune donnée sensible journalisée) ;
- au moins une refactorisation significative d'un module endetté, protégée par les tests écrits à l'étape 3, avec preuve avant/après dans le journal ;
- un historique de commits lisible, qui trace les corrections une par une ;
- le **journal de maintenance** complet : preuves de diagnostic, d'audit et de refactorisation, décisions prises, arbitrages, et ce que vous laissez volontairement à l'équipe pour la suite ;
- votre fiche d'autoévaluation complétée, pour identifier d'éventuels oublis avant l'échange avec votre mentor.

**Recommandations :**

- Refactorisez sous protection : les tests d'abord, la refactorisation ensuite, `pytest` au vert après chaque mouvement. Une refactorisation sans tests est un pari, pas de la maintenance.
- Le classique du parcours : les requêtes N+1 de l'ORM Django qui passent inaperçues sur un jeu de données réduit et s'effondrent en production. Si vous la rencontrez, expliquez-la dans le journal ; ne la contournez pas au hasard.
- Le journal s'écrit au fil de l'eau. Reconstitué après coup, il perd les preuves, et ça se voit.

**Points de vigilance :**

- Un journal sans preuves (pas d'extraits, pas de sorties de commandes, pas d'avant/après) ne démontre pas la maintenance : il l'affirme. Le manque de preuves vérifiables peut motiver un refus en soutenance.

Quand vous poussez votre dernier commit, l'équipe Suivi Transports récupère une application qu'elle comprend, qu'elle peut modifier sans peur et livrer sans cérémonie. La V2 peut commencer, et c'est votre passage qui l'a rendue possible.

---

# Renforcez vos connaissances

La reformulation fait partie des techniques de l'apprentissage qui fonctionnent et qui permettent de renforcer vos connaissances et compétences.

Dans ce projet, vous avez appris à diagnostiquer et sécuriser une application existante, à construire une stratégie de tests, à automatiser la livraison et à documenter la maintenance : ce sont des compétences importantes pour votre futur métier.

Nous allons donc vous proposer un outil qui vous permet de travailler cette reformulation et ainsi ancrer votre apprentissage plus profondément.

Pour cela, vous allez pouvoir utiliser l'outil Companion qui a été spécialement entraîné pour vous permettre de reformuler et d'affiner votre pensée. Cet engagement cognitif plus fort vous permettra de renforcer vos connaissances et d'être plus à l'aise en soutenance.

Quand vous serez parvenu à une formulation claire et satisfaisante des notions que vous souhaitez retravailler, faites une capture d'écran de la fin de la conversation et intégrez-la dans vos livrables.

Si des notions du projet vous semblent suffisamment claires pour ne pas nécessiter d'échange d'approfondissement, cela signifie que vous vous sentez suffisamment solide pour votre soutenance avec l'évaluateur.

Cliquez sur le bouton ci-dessous et commencez à échanger avec Companion.

:::encadre type=info
Mettre ici le lien vers le custom Companion
:::

---

# Livrables et Soutenance

## Livrables

1. **Lien vers le repo GitHub** de l'application, contenant au minimum : le code amélioré et débogué, le code source des tests, le fichier de configuration du pipeline d'intégration et de déploiement continu, et un historique de commits traçant les corrections.
2. **Note de sécurisation technique** synthétique, contenant au minimum : le lien vers le repo GitHub, un tableau récapitulant les vulnérabilités traitées, et la cartographie des flux chiffrés et des privilèges.
3. **Rapport de couverture du code**, généré automatiquement par l'outillage de build.
4. **Journal de maintenance** intégrant les preuves de diagnostic, d'audit et de refactorisation, ainsi que les arbitrages réalisés.
5. **Support de présentation** pour la soutenance, reprenant : le diagnostic et la priorisation, les actions de sécurisation, la stratégie de tests et sa couverture, le pipeline, et ce que vous laissez à l'équipe.
6. **Capture(s) d'écran de vos échanges avec Companion** montrant votre compréhension des notions du projet que vous aviez besoin de retravailler.

:::encadre type=info
Déposez sur la plateforme, dans un dossier zip nommé **Titre_du_projet_nom_prénom**, tous les livrables du projet comme suit : **Nom_Prénom_n° du livrable_nom du livrable_date de démarrage du projet**.

Cela donnera :

- Nom_Prénom_1_lien_repo_github_mmaaaa
- Nom_Prénom_2_note_securisation_mmaaaa
- Nom_Prénom_3_rapport_couverture_mmaaaa
- Nom_Prénom_4_journal_maintenance_mmaaaa
- Nom_Prénom_5_support_presentation_mmaaaa
- Nom_Prénom_6_captures_companion_mmaaaa

Par exemple, le premier livrable peut être nommé comme suit : Dupont_Jean_1_lien_repo_github_012026.
:::

## Soutenance

Pendant la soutenance, l'évaluateur jouera le rôle d'Élodie, la responsable de l'équipe Suivi Transports, à qui vous présentez votre travail.

**Présentation (12 minutes)**

- Vous présenterez l'ensemble de votre travail au travers du support de présentation que vous avez préparé : le diagnostic, la priorisation, puis les actions menées.
- Vous présenterez la note de sécurisation : les vulnérabilités traitées et la cartographie des flux et des privilèges.
- Vous ferez la démonstration, en direct, de votre filet de sécurité : la suite de tests qui passe, le rapport de couverture, et une exécution du pipeline. Une démonstration qui ne fonctionne pas faute d'environnement préparé peut motiver un refus.

**Discussion (10 minutes)**

- L'évaluateur, jouant le rôle d'Élodie, vous challengera sur vos choix, par exemple :
  - la priorisation retenue : pourquoi avoir traité ceci d'abord et reporté cela ;
  - les mécanismes de protection choisis au regard de la sensibilité des données transportées ;
  - la répartition de vos tests et ce que vous avez choisi de ne pas automatiser ;
  - le rôle de chaque étape du pipeline et ce qui se passe quand l'une d'elles échoue ;
  - ce que l'équipe doit surveiller ou reprendre après votre départ.

**Débriefing pédagogique et conseil (8 minutes)**

L'évaluateur sort de son rôle pour devenir un pair expérimenté. Ce temps est dédié à la transmission :

- **Retour sur votre méthodologie** : conseils pour optimiser le flux de travail (par exemple l'ordre audit, tests, refactorisation, et la tenue du journal au fil de l'eau).
- **Utilisation de l'IA** : discussion constructive sur la manière dont vous avez utilisé l'IA (accélération de l'écriture vs diagnostic et arbitrages) et conseils pour une utilisation éthique et efficace à l'avenir.
- **Axes d'amélioration** : retour détaillé sur la fluidité, la précision de votre vocabulaire technique et la pertinence de vos arbitrages.
- **Conseil de carrière** : quel conseil donner à un développeur qui reprend une application existante pour la première fois ?

:::encadre type=info
Votre présentation devrait durer 15 minutes (+/- 5 minutes). Puisque le respect des durées des présentations est important en milieu professionnel, les présentations en dessous de 10 minutes ou au-dessus de 20 minutes peuvent être refusées.
:::

---
