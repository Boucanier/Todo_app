from flask import Flask, render_template, request
from datetime import date, datetime

import toudou.models as models

app = Flask(__name__)

# TODO: Update tasks
@app.route("/toudou/", methods=["GET"])
def controller():
    if request.args.get('action') == "add":
        models.create_todo(request.args.get('task', ''), due=((datetime.strptime(request.args.get('due', ''), "%Y-%m-%d")).date() if request.args.get('due') else None)) # type: ignore
    return render_template("index.html", todos=models.get_all_todos())

@app.route("/toudou/")
def index():
    return render_template("index.html", todos=models.get_all_todos())