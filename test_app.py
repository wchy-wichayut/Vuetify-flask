from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
from flask.helpers import make_response
import pyrebase
from oop import FirebaseAPI
from random import randrange

with open("config.json", encoding="utf 8")as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()

app = Flask(__name__)


@app.route('/')
@app.route('/chatbotTable')
def chatbotTable():
    base = FirebaseAPI(db, 'chatbot_transactions')
    lst = base.transaction_index()
    data = {
        'ref': lst
    }
    return jsonify(data)


@app.route('/index')
def index():
    return render_template('chatbotTable.html')


@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    post_data = request.get_json()
    # print(id)
    # print(post_data)
    return make_response(post_data)


@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    # print('>>>>> ', id)
    db.child('chatbot_transactions').child(id).remove()
    return make_response(id)


@app.route('/getDemo')
def requestDemo():
    setDemo = FirebaseAPI(db, 'requestDemo')
    lst = setDemo.getDemo_index()
    setIndex = {
        'ref': lst
    }
    return jsonify(setIndex)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
