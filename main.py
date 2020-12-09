from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pyrebase
from firebase_admin import credentials, auth

cred = credentials.Certificate('config.json')
firebase_auth = firebase_admin.initialize_app(cred)


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
    userTest = [{'username':'login', 'password': '12345'}]
    error = None
    erText = None
    if request.method == 'POST':
        # Register
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        usname = request.form['usname']
        pword = request.form['pword']
        confirmpw = request.form['confirmpw']
        # Login
        user = request.form['username']
        password = request.form['password']
        for i in userTest:
            if i['username'] != user or i['password'] != password:
                error = "Try Again"
                return render_template('login.html', error=error)
            else:
                return redirect(url_for('index')) 
        if confirmpw != pword:
            return render_template('login.html', error=confirmpw)
        if firstname is None or lastname is None or pword is None or email is None or usname is None:
            return render_template('login.html', errort=erText)
        try:
            username = auth.create_user(email=email, password=password, display_name=usname)
            data = {'firstname':firstname, 'lastname':lastname, 'email':username.email, 'usname':username.display_name,'userToken': user.uid}
            db.child('signup').push(data)
            return 
        except:
            return redirect(url_for('table'))
    return render_template('login.html')


dfg
if __name__=='__main__':
    app.run(debug=True, port=5010)