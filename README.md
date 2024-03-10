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

Le fichier [views.py](src/toudou/views.py) fait le lien entre les templates html et les fonctions de manipulation des todos.

## Contenu de [src/toudou](src/toudou) (code source de l'application)

- [static](src/toudou/static) : fichiers statiques utilisés par l'application (css, js)
- [templates](src/toudou/templates) : templates html utilisés par l'application
  - [header.html](src/toudou/templates/header.html) : header html
  - [index.html](src/toudou/templates/index.html) : page d'accueil (affichage des todos, création, suppression, modification)
  - [import.html](src/toudou/templates/import.html) : page pour importer un fichier csv
- [models.py](src/toudou/models.py) : classe Todo et fonctions pour les manipuler
- [services.py](src/toudou/services.py) : fonctions pour exporter ou importer des todos au format CSV
- [views_cli.py](src/toudou/views_cli.py) : fonctions pour gérer les commandes de l'application depuis un terminal
- [views.py](src/toudou/views.py) : fonctions pour gérer l'application Flask

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
