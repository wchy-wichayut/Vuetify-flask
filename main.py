from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pyrebase

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

@app.route('/table')
def table():
    lst = []
    ref = db .child('event').get()
    for i in ref.each():
        commpant = i.val()['compant']
        email = i.val()['email']
        fname = i.val()['fname']
        message = i.val()['message']
        product = i.val()['product']
        tel = i.val()['tel']
        key = i.key()
        box = {'conpant':commpant, 'email':email, 'fname':fname, 'message': message,
                'product':product, 'tel':tel, 'key':key}
        lst.append(box)
    data = {
        'ref':lst
        }
    return render_template('index.html', data=data)

    


if __name__=='__main__':
    app.run(debug=True, port=5010)