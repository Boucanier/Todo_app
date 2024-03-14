from flask import Flask, redirect, render_template, request, send_file, Blueprint, url_for
from datetime import datetime
import uuid, os, logging
from toudou import services, config
from toudou.forms import AddForm, UpdateForm, DeleteForm

import toudou.models as models


web_ui = Blueprint('web_ui', __name__, url_prefix="/")


@web_ui.route("/", defaults={"page": "index"})
@web_ui.route("/<page>")
def show(page):
    return render_template(f"{page}.html", todos=models.get_all_todos(), add_form=AddForm(), update_form=UpdateForm(), delete_form=DeleteForm())


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
        if request.args.get('action') == "delete":
            models.delete_todo(uuid.UUID(request.args.get('id', '')))

    if request.method == "POST":            
        if request.form.get('action') == "add":
            form = AddForm()
            if form.validate_on_submit():
                models.create_todo(request.form.get('task', ''), due=((datetime.strptime(request.form.get('due', ''), "%Y-%m-%d")).date() if request.form.get('due') else None)) # type: ignore
            else:
                return redirect(url_for('web_ui.show'))
            
        elif request.form.get('id', ''):
            if request.form.get('action') == "update":
                form = UpdateForm()
                new_comp = False
                if request.form.get('complete') :
                    new_comp = True
                if form.validate_on_submit():
                    models.update_todo(uuid.UUID(request.form.get('id', '')), request.form.get('task', ''), new_comp, due=((datetime.strptime(request.form.get('due', ''), "%Y-%m-%d")).date() if request.form.get('due') else None)) # type: ignore
                else:
                    return redirect(url_for('web_ui.show'))
            
            elif request.form.get('action') == "delete":
                form = DeleteForm()
                if form.validate_on_submit():
                    models.delete_todo(uuid.UUID(request.form.get('id', '')))
                else:
                    return redirect(url_for('web_ui.show'))
    
        elif request.files:
            file = request.files["file"]
            
            if not os.path.exists(config['UPLOAD_FOLDER']):
                os.makedirs(config['UPLOAD_FOLDER'])

            filename = os.path.join(config['UPLOAD_FOLDER'], file.filename)
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
    app.config['SECRET_KEY'] = config['SECRET_KEY']
    from toudou.views import web_ui
    app.register_blueprint(web_ui)
    return app