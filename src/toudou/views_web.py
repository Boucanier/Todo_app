from flask import Flask, render_template, request, send_file
from datetime import datetime
import uuid
from toudou import services

import toudou.models as models


app = Flask(__name__)


@app.route("/toudou/", methods=["GET"])
def controller():
    if request.args.get('id', ''):
        if request.args.get('action') == "add":
            models.create_todo(request.args.get('task', ''), due=((datetime.strptime(request.args.get('due', ''), "%Y-%m-%d")).date() if request.args.get('due') else None)) # type: ignore

        elif request.args.get('action') == "update":
            new_comp = False
            if request.args.get('complete') :
                new_comp = True
            models.update_todo(uuid.UUID(request.args.get('id', '')), request.args.get('task', ''), new_comp, due=((datetime.strptime(request.args.get('due', ''), "%Y-%m-%d")).date() if request.args.get('due') else None)) # type: ignore
        
        elif request.args.get('action') == "delete":
            models.delete_todo(uuid.UUID(request.args.get('id', '')))
            
    return render_template("index.html", todos=models.get_all_todos())

@app.route("/toudou/")
def index():
    return render_template("index.html", todos=models.get_all_todos())

@app.route("/toudou/download/")
def download():
    path = "../../" + services.export_to_csv()
    return send_file(path, as_attachment=True)