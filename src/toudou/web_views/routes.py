"""
    This module contains the routes for the Toudou app web interface
"""
from flask import abort, flash, redirect, render_template, request, send_file, Blueprint, url_for
from datetime import datetime
import uuid, os, logging
from toudou import services, config
from toudou.web_views.forms import AddForm, UpdateForm, DeleteForm
from toudou.web_views.auth import auth

import toudou.models as models


web_ui = Blueprint('web_ui', __name__, url_prefix="/")


# Routes

@web_ui.route("/error/<code>", methods=["GET", "POST"])
def error(code):
    """
        Render the error page

        - Args :
            - code (str) : the error code

        - Returns :
            - (str) : the HTML for the error page
    """
    return render_template(f"error.html", role=auth.get_user_roles(auth.username()), error=code)


@web_ui.route("/", defaults={"page": "index"})
@web_ui.route("/<page>")
@auth.login_required
def show(page):
    """
        Render the requested page

        - Args :
            - page (str) : the page to render

        - Returns :
            - (str) : the HTML for the requested page
    """
    if os.path.exists(os.path.join("src", "toudou", "templates", f"{page}.html")):
        if "user" in auth.get_user_roles(auth.username()) and page not in ("index", "export"):
            abort(403)
        
        else :
            logging.info(f"Rendering {page}.html")
            return render_template(f"{page}.html", todos=models.get_all_todos(), add_form=AddForm(), update_form=UpdateForm(), delete_form=DeleteForm(), role=auth.get_user_roles(auth.username()))
    else:
        abort(404)


@web_ui.route("/controller", methods=["GET", "POST"])
@auth.login_required
def controller():
    """
        The controller for the Toudou app that handles GET and POST requests

        - Args :
            - None

        - Returns :
            - (str) : the HTML for the index page
    """
    if "admin" in auth.get_user_roles(auth.username()):
        if request.method == "POST":
            if request.form.get('action') == "add":
                form = AddForm()
                if form.validate_on_submit():
                    logging.info(f"Adding a new Todo: {request.form.get('task', '')}")
                    models.create_todo(request.form.get('task', ''), due=((datetime.strptime(request.form.get('due', ''), "%Y-%m-%d")).date() if request.form.get('due') else None)) # type: ignore
                else:
                    return redirect(url_for('web_ui.show'))
                
            elif request.form.get('id', ''):
                if request.form.get('action') == "update":
                    form = UpdateForm()
                    new_comp = False
                    if request.form.get('complete'):
                        new_comp = True
                    if form.validate_on_submit():
                        logging.info(f"Updating Todo: {request.form.get('task', '')}")
                        models.update_todo(uuid.UUID(request.form.get('id', '')), request.form.get('task', ''), new_comp, due=((datetime.strptime(request.form.get('due', ''), "%Y-%m-%d")).date() if request.form.get('due') else None)) # type: ignore
                    else:
                        return redirect(url_for('web_ui.show'))
                
                elif request.form.get('action') == "delete":
                    form = DeleteForm()
                    if form.validate_on_submit():
                        logging.info(f"Deleting Todo: {request.form.get('id', '')}")
                        models.delete_todo(uuid.UUID(request.form.get('id', '')))
                    else:
                        return redirect(url_for('web_ui.show'))
        
            elif request.files:
                file = request.files["file"]

                filename = os.path.join(config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                file = open(filename)
                logging.info(f"Importing Todos from CSV: {filename}")
                services.import_from_csv(file)
                file.close()
                
    return redirect(url_for('web_ui.show'))


@web_ui.route("export/")
@auth.login_required
def export():
    """
        Download the CSV file of all the Todos

        - Args :
            - None

        - Returns :
            - (file) : the CSV file of all the Todos
    """
    logging.info(f"Exporting Todos to CSV")
    path = "../../" + services.export_to_csv()
    return send_file(path, as_attachment=True)


@web_ui.route("out/")
def out():
    """
        Log out the user

        - Args :
            - None

        - Returns :
            - (str) : the HTML for the index page
    """
    logging.info(f"Logging out user {auth.username()}")
    return redirect("http://nouser:nouser@localhost:5000/")


# Error Handlers

@web_ui.errorhandler(401)
def handle_401(error):
    """
        Handle 401 errors
        
        - Args :
            - error (str) : the error message

        - Returns :
            - (str) : the HTML for the error page
    """
    flash("401: Unauthorized")
    logging.exception(error)
    return redirect(url_for('web_ui.error', code=401))


@web_ui.errorhandler(403)
def handle_403(error):
    """
        Handle 403 errors

        - Args :
            - error (str) : the error message

        - Returns :
            - (str) : the HTML for the error page
    """
    flash("403: Forbidden")
    logging.exception(error)
    return redirect(url_for('web_ui.error', code=403))


@web_ui.errorhandler(404)
def handle_404(error):
    """
        Handle 404 errors

        - Args :
            - error (str) : the error message

        - Returns :
            - (str) : the HTML for the error page
    """
    flash("404: Page not found")
    logging.exception(error)
    return redirect(url_for('web_ui.error', code=404))


@web_ui.errorhandler(405)
def handle_405(error):
    """
        Handle 405 errors

        - Args :
            - error (str) : the error message

        - Returns :
            - (str) : the HTML for the error page
    """
    flash("405: Method Not Allowed")
    logging.exception(error)
    return redirect(url_for('web_ui.error', code=405))


@web_ui.errorhandler(500)
def handle_500(error):
    """
        Handle 500 errors

        - Args :
            - error (str) : the error message

        - Returns :
            - (str) : the HTML for the error page
    """
    flash("500: Internal Server Error")
    logging.exception(error)
    return redirect(url_for('web_ui.error', code=500))
