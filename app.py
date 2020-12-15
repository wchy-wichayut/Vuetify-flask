from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pyrebase
from random import randrange

with open("config.json", encoding="utf 8")as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():

    return render_template('index.html')


# @app.route("/welcome")
# def index():
#     return render_template('main/welcome.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
