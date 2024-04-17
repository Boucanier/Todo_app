# Toudou

The best todo application!

## Fonctionnement

Un todo est un objet qui contient un id unique, une tâche à réaliser, une deadline (optionnelle = peut être *None*) et un statut (*True* ou *False*).

### Ligne de commande

Pour utiliser l'application depuis un terminal, il est possible d'utiliser les commandes suivantes :

- `toudou init-db` : initialise la base de données
- `toudou create [-t Tâche à réaliser] [-d Date de fin]` : crée un todo
- `toudou get [--id id du todo]` : récupère un todo
- `toudou get-all [--as-csv]` : récupère tous les todos
- `toudou delete [--id id du todo]` : supprime un todo
- `toudou update [--id id du todo] [-c | --complete] [-t Nouvelle tâche] [-d Nouvelle date de fin]` : met à jour un todo
- `toudou import-csv [fichier.csv]` : importe des todos depuis un fichier CSV

### Interface web

La page d'accueil de l'application affiche la liste des todos et deux formulaires. Il est possible de créer, modifier ou supprimer un todo depuis ces formulaires.

Le header de l'application permet d'accéder à la page d'accueil, à la page d'import de todos depuis un fichier CSV et de télécharger la liste des todos au format CSV.

La page d'import des todos contient un formulaire pour sélectionner un fichier CSV et importer les todos qu'il contient.

Le fichier [routes.py](src/toudou/web_views/routes.py) fait le lien entre les templates html et les fonctions de manipulation des todos.

#### Connexion et rôles

La connexion au site est une connexion http basique. Les deux rôles existants sont *admin* et *user*. Les utilisateurs *admin* peuvent importer, créer, modifier ou supprimer des todos. Les utilisateurs *user* peuvent seulement consulter et exporter la liste des todos.

Deux utilisateurs existent par défaut : *admin* et *user*. Leurs mots de passe sont respectivement *admin* et *user*.

### API RESTful

Les fonctions de l'**API RESTful** permettent de manipuler les todos depuis un client externe. Les routes de l'API sont les suivantes :

- `/api/todos` (GET) : récupère tous les todos
- `/api/todos/<int:id>` (GET) : récupère un todo
- `/api/todos` (POST) : crée un todo
- `/api/todos/<int:id>` (PUT) : met à jour un todo
- `/api/todos/<int:id>` (PATCH) : met à jour un todo (partiellement)
- `/api/todos/<int:id>` (DELETE) : supprime un todo

Les **tokens** existants sont : ***tk1*** et ***tk2***.

## Contenu de [src/toudou](src/toudou) (code source de l'application)

- [static](src/toudou/static) : fichiers statiques utilisés par l'application (css, js, ico)
- [wsgi.py](src/toudou/wsgi.py) : permet de lancer l'application web avec un serveur WSGI
- [models.py](src/toudou/models.py) : classe Todo et fonctions pour les manipuler
- [services.py](src/toudou/services.py) : fonctions pour exporter ou importer des todos au format CSV
- [views_cli.py](src/toudou/views_cli.py) : fonctions pour gérer les commandes de l'application depuis un terminal
- [views.py](src/toudou/views.py) : routes de l'application web, permet de créer l'application Flask
- [templates](src/toudou/templates) : templates html utilisés par l'application
  - [header.html](src/toudou/templates/header.html) : header html
  - [index.html](src/toudou/templates/index.html) : page d'accueil (affichage des todos, création, suppression, modification)
  - [import.html](src/toudou/templates/import.html) : page pour importer un fichier csv
  - [error.html](src/toudou/templates/error.html) : page d'erreur
- [web_views](src/toudou/web_views) : fichiers pour l'interface web
  - [forms.py](src/toudou/web_views/forms.py) : formulaires utilisés par l'application web
  - [auth.py](src/toudou/web_views/auth.py) : fonctions pour gérer la connexion et les rôles des utilisateurs
- [api](src/toudou/api) : fichiers pour l'API
  - [routes.py](src/toudou/api/routes.py) : routes de l'API
  - [auth.py](src/toudou/api/auth.py) : fonctions pour gérer la connexion des utilisateurs
  - [models.py](src/toudou/api/models.py) : classe représentant les format de fichiers JSON à envoyer

## Remarques

Les docstrings et les commentaires du code sont en anglais.

```bash
$ pdm install
$ pdm run toudou
Usage: toudou [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    create
    delete
    get
    get-all
    import-csv
    init-db
    update
```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)
