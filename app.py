from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask.helpers import make_response
import pyrebase
import json
from oop import FirebaseAPI

with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')

@app.route("/home")
def home():
    lst = []
    count = 1
    ref = db.child('chatbot_transactions').get()
    for i in ref.each()[62:]:
        r = i.val()
        day = i.val()['day']
        hour = i.val()['hour']
        img = i.val()['img']
        message = i.val()['message']
        mins = i.val()['min']
        month = i.val()['month']
        profile = i.val()['profile']
        reply = i.val()['reply']
        sec = i.val()['sec']
        userid = i.val()['userid']
        year = i.val()['year']
        key = i.key()
        box = {'date/time': f'{year}/{month}/{day} {hour}:{mins}:{sec}', 'img':img, 'message':message,
        'profile':profile, 'reply':reply,'userid':userid, "key":key, "index":count}
        lst.append(box)
        count += 1
    show = {
        'ref':lst      
        }
    return jsonify(show)
 
@app.route('/json_index')
def update():
    fb = FirebaseAPI(db, "chatbot_transactions")
    lst = fb.transaction_index()
    data = {
        "ref": lst[::-1]
    }
    return jsonify(data)



@app.route('/update_index/<id>',methods=["POST"])
def update_index(id):
    post_data = request.get_json()
    print(id)
    print(post_data)
    db.child('chatbot_transactions').child(id).update(post_data)
    return make_response(post_data)

@app.route('/delete_index/<id>',methods=["POST"])
def delete_index(id):
    post_data = request.get_json()
    print(id)
    print(post_data)
    db.child("chatbot_transactions").child(id).remove()
    return make_response(post_data)

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
 