from os import error
from flask import Flask, render_template, jsonify, request, redirect, url_for, session,g
import json

from flask.globals import session
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth


with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()

cred = credentials.Certificate("keypython.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

    return 'Hello World'




if __name__ == '__main__':
    app.run(debug=True, port=8080)