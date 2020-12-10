from os import error
from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("keypython.json")
firebase_admin.initialize_app(cred)

with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()


# db.child('signup').set({'key' : 'value'})

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
        company = i.val()['event']['company']
        email = i.val()['event']['email']
        fname = i.val()['event']['fname']
        message = i.val()['event']['message']
        product = i.val()['event']['product']
        tel = i.val()['event']['tel']
        tag = i.val()['tag']
        key = i.key()
        box = {'Date':date, 'Time': time, 'company':company, 'email':email, 'fname':fname, 'message': message,
                'product':product, 'tel':tel, 'tag':tag, 'key':key}
        lst.append(box)
    data = {
        'ref':lst
        }
    return jsonify(data)


@app.route('/login', methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        error = "Please fill in correctly."
        ertext = "Please fill in all information"
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        usname = request.form['usname']
        pword = request.form['pword']
        confirmpw = request.form['confirmpw']
        if confirmpw != pword:
            return render_template('login.html', error=error)
        if firstname is None or lastname is None or pword is None or email is None or usname is None:
            return render_template('login.html', ertext=ertext)
        try:
            username = auth.create_user(email=email, password=pword, display_name=usname)
            data = {'firstname':firstname, 'lastname':lastname, 'email':username.email, 
            'usname':username.display_name,'userToken': username.uid}
            db.child('signup').push(data)
            return redirect(url_for('table'))
        except:
            return render_template('login.html', error=erText)
    



@app.route('/key', methods=["POST"])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    usname = request.form['usname']
    pword = request.form['pword']
    
    send = {'firstname':firstname, 'lastname':lastname, 'email':email, 'usname':usname, "pword":pword}

    username = auth.create_user(email=email, password=pword, display_name=usname)
    return jsonify({'user':username})

@app.route('/logkey', methods=['POST'])
def signin():
    email = request.form['email']
    pword = request.form['pword']
    try:
        pb.auth().sign_in_with_email_and_password(email, pword)
        return jsonify({'user':'success'})
    except:
        return jsonify({'user':'error'})
 


if __name__=='__main__':
    app.run(debug=True, port=5010)