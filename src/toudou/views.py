from flask import Flask, render_template, request, send_file
from datetime import datetime
import uuid, os
from toudou import services

import toudou.models as models


app = Flask(__name__)

# The folder where the uploaded files are stored
UPLOAD_FOLDER = "uploads/"


@app.route("/toudou/", methods=["GET", "POST"])
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
            
    return render_template("index.html", todos=models.get_all_todos())


@app.route("/toudou/")
def index():
    return render_template("index.html", todos=models.get_all_todos())


@app.route("/toudou/export/")
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


@app.route("/toudou/import/")
def import_csv():
    return render_template("import.html")
