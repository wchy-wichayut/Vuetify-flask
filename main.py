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
    ref = db .child('requestDemo').get()
    for i in ref.each()[1:]:
        date = i.val()['Date']
        time = i.val()['Time']
        commpany = i.val()['event']['company']
        email = i.val()['event']['email']
        fname = i.val()['event']['fname']
        message = i.val()['event']['message']
        product = i.val()['event']['product']
        tel = i.val()['event']['tel']
        tag = i.val()['tag']['0']
        key = i.key()
        box = {'Date':date, 'Time': time, 'conpany':commpany, 'email':email, 'fname':fname, 'message': message,
                'product':product, 'tel':tel, 'tag':tag, 'key':key}
        lst.append(box)
    data = {
        'ref':lst
        }
    return jsonify('index.html', data=data)

   
   


if __name__=='__main__':
    app.run(debug=True, port=5010)