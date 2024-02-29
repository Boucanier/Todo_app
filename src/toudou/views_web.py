from flask import Flask, render_template

import toudou.models as models

app = Flask(__name__)

@app.route("/toudou/")
def index(todos=None):
    return render_template("index.html", todos=models.get_all_todos())