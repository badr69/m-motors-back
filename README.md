# M-MOTORS BACKEND
Ce projet est le backend de l’application M-Motors.
Il expose une API REST permettant la gestion des utilisateurs, véhicules, dossiers de location et documents.
L’application est développée en Python avec Flask et utilise PostgreSQL comme base de données.
L’authentification est sécurisée via JWT.


# STACK TECHNIQUE
Python 3.14 (environnement local – développement)
Python 3.11 (environnement VPS – production, stabilité)
Ubuntu 26.04 LTS (environnement serveur avec Python intégré côté système)
Flask (API REST)
SQLAlchemy (ORM)
Alembic (migrations)
PostgreSQL
JWT (authentification)
Pytest (tests unitaires)
Coverage (qualité de code)


# ARCHITECTURE DU PROJET
example:
app/
├── core → configuration, DB, sécurité
├── modules → logique métier (users, vehicles, etc.)
├── api → routes REST (blueprints)
├── models → modèles SQLAlchemy
├── services → logique métier (CRUD)
└── controllers → gestion des requêtes HTTP


# CONFIGURATION BASE DE DONNÉES
En local (DEV)
m_motors_dev_db sur alwaysdata

En production (VPS)
m_motors_prod_db sur alwaysdata

La configuration est gérée via les variables d’environnement (.env).


# MIGRATIONS (ALEMBIC)
Initialisation de la base :
alembic upgrade head

Création d’une migration :
alembic revision --autogenerate -m "message"

Important :
Les migrations sont testées en environnement DEV avant PROD
Aucune modification directe de la base de données en production
Utilisation d’Alembic pour garantir la cohérence du schéma
Synchronisation obligatoire entre code et base de données


# AUTHENTIFICATION
L’authentification est basée sur JWT.

Génération d’un token à la connexion
Stockage côté frontend (localStorage)
Vérification du token sur les routes protégées
Gestion des rôles (ADMIN / CLIENT)

# STRUCTURE API
Exemples d’endpoints :

/api/v1/auth/login
/api/v1/users
/api/v1/vehicles
/api/v1/dossiers
/api/v1/documents


# FONCTIONNALITÉS BACKEND
Authentification utilisateur (JWT)
CRUD utilisateurs
CRUD véhicules
Gestion des dossiers de location
Upload et gestion des documents
Gestion des rôles (admin / client)


# TESTS UNITAIRES
Le backend est testé avec postman et Pytest.

Commande :
pytest

Couverture du code :
coverage run -m pytest && coverage report

Objectif : environ 80% de couverture

ou:
coverage run -m pytest
coverage report
coverage json

Les fichiers .coverage et coverage.json sont inclus dans le repository afin de permettre la vérification du taux de couverture.
Couverture obtenue : 82 %


# DÉPLOIEMENT
Le backend est déployé sur un VPS Linux.

Architecture :

Docker (containerisation)
Nginx (reverse proxy)
PostgreSQL (base de données)
Gunicorn (serveur WSGI)


# ENVIRONNEMENTS
DEV : développement local
PROD : serveur VPS

Séparation via .env pour éviter toute confusion entre environnements.


# SÉCURITÉ
Hash des mots de passe (werkzeug / bcrypt)
JWT pour sécuriser les routes
Contrôle des rôles (RBAC)
Validation des données côté backend
Protection des endpoints sensibles


# PROBLÈMES RENCONTRÉS
Désynchronisation des migrations Alembic entre DEV et PROD
Erreur DuplicateTable lors du déploiement
Résolution via reset de l’état Alembic (stamp) et réalignement des bases

Affichage des image et documents apres un refactor


# AUTEUR
Projet réalisé dans le cadre du Bachelor Développeur d’Application Python.

Projet réalisé par Mr Derrouiche Badreddine


