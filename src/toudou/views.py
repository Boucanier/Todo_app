from flask import Flask, redirect, render_template, request, send_file, Blueprint, url_for
from datetime import datetime
import uuid, os
from toudou import services

import toudou.models as models


web_ui = Blueprint('web_ui', __name__, url_prefix="/toudou")

# The folder where the uploaded files are stored
UPLOAD_FOLDER = "uploads/"


@web_ui.route("/", defaults={"page": "index"})
@web_ui.route("/<page>")
def show(page):
        return render_template(f"{page}.html", todos=models.get_all_todos())


@web_ui.route("/controller", methods=["GET", "POST"])
def controller():
    """
        The controller for the Toudou app that handles GET and POST requests

        - Args :
            - None

        - Returns :
            - (str) : the HTML for the index page
    """
    if request.method == "GET":
        if request.args.get('id', ''):
            if request.args.get('action') == "update":
                new_comp = False
                if request.args.get('complete') :
                    new_comp = True
                models.update_todo(uuid.UUID(request.args.get('id', '')), request.args.get('task', ''), new_comp, due=((datetime.strptime(request.args.get('due', ''), "%Y-%m-%d")).date() if request.args.get('due') else None)) # type: ignore
            
            elif request.args.get('action') == "delete":
                models.delete_todo(uuid.UUID(request.args.get('id', '')))
            
        if request.args.get('action') == "add":
            models.create_todo(request.args.get('task', ''), due=((datetime.strptime(request.args.get('due', ''), "%Y-%m-%d")).date() if request.args.get('due') else None)) # type: ignore
    
    elif request.method == "POST":
        if request.files:
            file = request.files["file"]
            
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            file = open(filename)
            services.import_from_csv(file)
            
    return redirect(url_for('web_ui.show'))


@web_ui.route("export/")
def export():
    """
        Download the CSV file of all the Todos

        - Args :
            - None

        - Returns :
            - (file) : the CSV file of all the Todos
    """
    path = "../../" + services.export_to_csv()
    return send_file(path, as_attachment=True)


def create_app():
    app = Flask(__name__)
    from toudou.views import web_ui
    app.register_blueprint(web_ui)
    return app