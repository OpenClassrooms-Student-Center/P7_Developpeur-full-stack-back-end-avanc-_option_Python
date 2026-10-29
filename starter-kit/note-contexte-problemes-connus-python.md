# Note de contexte — Application de suivi des transports

**Rédigée par :** l'équipe Suivi Transports (compilation Élodie Vasseur)
**Destinataire :** développeur en renfort
**Statut :** document interne, non exhaustif

## Pourquoi cette note

Avant votre arrivée, on a essayé de mettre à plat ce qu'on sait, ce qu'on suppose, et ce qui nous inquiète sur l'application. Certains points viennent d'incidents vécus, d'autres sont des impressions jamais vérifiées faute de temps. Ne prenez rien ici pour acquis : vérifiez dans le code, on n'a pas eu le recul pour le faire nous-mêmes.

## Ce qu'on sait des lenteurs

Depuis quelques mois, plusieurs personnes de l'équipe commerciale nous remontent que l'écran de suivi met du temps à afficher l'historique d'un transport quand il y a beaucoup d'étapes (température relevée à chaque point de contrôle). On soupçonne un souci du côté du chargement des données liées (les relevés de température rattachés à un transport), mais personne n'a profilé la requête. Ça pourrait aussi venir du réseau chez certains clients, on ne sait pas trancher.

On a aussi un doute sur le nombre d'appels faits à la base au moment de l'affichage du tableau de bord. Un ancien du projet parlait d'un problème classique de l'ORM de Django où chaque ligne affichée déclenche une requête séparée, mais ça n'a jamais été confirmé formellement.

## Ce qui nous inquiète côté sécurité

On n'a pas d'audit de sécurité formel sur l'application. Ce qu'on peut dire :

- l'authentification existe (on se connecte avec un compte), mais on n'est pas certains que les autorisations soient bien vérifiées partout. Un livreur a par exemple réussi une fois à accéder à un écran qui semblait réservé aux responsables, sans qu'on comprenne pourquoi ;
- certains mots de passe de comptes de service (utilisés par des scripts internes) sont, on le pense, stockés quelque part dans les fichiers de configuration du projet plutôt que dans un coffre-fort de secrets. À vérifier ;
- on ne sait pas dire avec certitude si les échanges entre l'application et la base de données sont chiffrés de bout en bout. Le trafic entre le navigateur et le serveur, si, on pense que oui ;
- les données de température et les informations sur les destinataires nous semblent sensibles (certaines touchent à des patients), mais on n'a jamais formalisé qui a le droit de voir quoi.

On sait qu'il existe des référentiels de vulnérabilités standards pour ce genre d'audit, mais personne dans l'équipe n'a le temps de s'y plonger sérieusement.

## Ce qu'on pense des tests

Il y a des tests dans le projet, mais on a l'impression qu'ils ne couvrent que les cas simples. Plusieurs bugs remontés en production ces derniers mois concernaient des cas qu'on aurait dû détecter avant la mise en ligne (un mauvais calcul de délai, une erreur qui remontait un message technique incompréhensible côté client). On n'a pas de vision claire du pourcentage du code réellement testé : quelqu'un a mentionné un outil de couverture, mais on n'a jamais vu de rapport récent.

On ne sait pas non plus si les tests touchent vraiment la base de données ou s'ils se contentent de simuler les réponses. Ça change beaucoup de choses, mais ce n'est pas notre expertise.

## Ce qu'on sait des déploiements

Aujourd'hui, chaque mise en production se fait un peu à la main : la personne qui déploie construit le projet sur son poste, puis pousse elle-même les fichiers sur le serveur. Il n'y a pas vraiment de procédure écrite, chacun fait un peu à sa façon selon ce qu'il a appris de son prédécesseur. Il y a bien un fichier d'automatisation qui existe dans le dépôt, mais on n'est pas sûrs qu'il fasse grand-chose d'utile : personne ne l'a retouché depuis longtemps et on ne sait plus s'il exécute les tests avant de livrer.

On a eu au moins un incident où une version buggée est passée en production alors que, apparemment, un test aurait dû l'attraper. On n'a jamais compris pourquoi le test n'avait pas bloqué la livraison.

## Ce qu'on pense de la qualité générale du code

Des développeurs qui sont passés sur ce projet avant vous nous ont dit, en partant, que certaines parties du code étaient difficiles à faire évoluer sans tout casser autour. On n'a pas de liste précise des zones concernées. Ce qu'on peut dire, c'est que les modules liés à la gestion des transports et à leur suivi sont ceux qui reviennent le plus souvent dans les demandes de correctifs, ce qui laisse penser qu'ils accumulent plus de dette que les autres, mais ce n'est qu'une impression.

On a aussi remarqué que les journaux d'erreurs de l'application sont difficiles à lire quand un incident survient : parfois trop de détails inutiles, parfois pas assez pour comprendre ce qui s'est passé. Un collègue a mentionné une fois avoir vu une adresse e-mail de client dans un journal, mais on n'a pas creusé.

## Ce qu'on attend pour la V2

La direction veut une V2 plus robuste, capable de tenir la montée en charge annoncée avec deux nouveaux clients grands comptes. On ne sait pas dire aujourd'hui si l'application actuelle tiendrait cette charge, ni si elle est prête à être auditée par un client exigeant sur les questions de sécurité et de protection des données.

Cette note est un point de départ, pas un diagnostic. Elle mélange sûrement des faits, des approximations et au moins une ou deux idées reçues qui ne résisteront pas à un examen du code. C'est précisément ce qu'on vous demande de démêler.
