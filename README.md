# Toudou

The best todo application!

## How to use

A todo is an object that contains a unique id, a task to do, a deadline (optional = can be *None*) and a status (*True* or *False*).

### Command line

To use the application from a terminal, you can use the following commands:

- `toudou init-db` : initialize the database
- `toudou create [-t Task to do] [-d Deadline]` : create a todo
- `toudou get [--id id of the todo]` : get a todo
- `toudou get-all [--as-csv]` : get all todos
- `toudou delete [--id id of the todo]` : delete a todo
- `toudou update [--id id of the todo] [-c | --complete] [-t New task] [-d New deadline]` : update a todo
- `toudou import-csv [file.csv]` : import todos from a CSV file

### Web interface

The home page of the application displays the list of todos and two forms. It is possible to create, modify or delete a todo from these forms.

The header of the application allows to access the home page and the import page of todos from a CSV file and to download the list of todos in CSV format.

The import page contains a form to select a CSV file and import the todos it contains.

The file [routes.py](src/toudou/web_views/routes.py) links the html templates and the functions  of the models and services.

#### Connection and roles

The connection to the site is a basic http connection. The two existing roles are *admin* and *user*. *Admin* users can import, create, modify or delete todos. *User* users can only view and export the list of todos.

Two users exist by default: *admin* and *user*. Their passwords are respectively *admin* and *user*.

### RESTful API

The functions of the **RESTful API** allow to manipulate the todos from an external client. The routes of the API are as follows:

- `/api/todos` (GET) : get all todos
- `/api/todos/<int:id>` (GET) : get a todo
- `/api/todos` (POST) : create a todo
- `/api/todos/<int:id>` (PUT) : update a todo
- `/api/todos/<int:id>` (PATCH) : update a todo (partially)
- `/api/todos/<int:id>` (DELETE) : delete a todo

The existing **tokens** are: ***tk1*** and ***tk2***.

## Content of [src/toudou](src/toudou) (source code of the application)

- [static](src/toudou/static) : static files used by the application (css, js, ico)
- [wsgi.py](src/toudou/wsgi.py) : allows to launch the web application with a WSGI server
- [models.py](src/toudou/models.py) : Todo class and functions to manipulate them
- [services.py](src/toudou/services.py) : functions to export or import todos in CSV format
- [views_cli.py](src/toudou/views_cli.py) : functions to manage the commands of the application from a terminal
- [templates](src/toudou/templates) : html templates used by the application
  - [header.html](src/toudou/templates/header.html) : html header
  - [index.html](src/toudou/templates/index.html) : home page (display of todos, creation, deletion, modification)
  - [import.html](src/toudou/templates/import.html) : page to import a csv file
  - [error.html](src/toudou/templates/error.html) : error page
- [web_views](src/toudou/web_views) : files for the web interface
  - [routes.py](src/toudou/web_views/routes.py) : routes of the web interface
  - [forms.py](src/toudou/web_views/forms.py) : forms used by the web application
  - [auth.py](src/toudou/web_views/auth.py) : functions to manage the connection and roles of users
- [api](src/toudou/api) : files for the API
  - [routes.py](src/toudou/api/routes.py) : routes of the API
  - [auth.py](src/toudou/api/auth.py) : functions to manage the connection of users
  - [models.py](src/toudou/api/models.py) : class representing the JSON file formats to send

## Commands to run the application

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
