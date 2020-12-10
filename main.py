from os import error
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json

from flask.globals import session
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

app.secret_key = 'patthadonhahah'

@app.route('/')
@app.route('/index')
def index():
    # log = False 
    # if 'hhname' in session and 'ssword' in session:
    #     log = True
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
   
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        user = auth.create_user(email=email, password=password, display_name=username)
        data = {'firstname':firstname, 'lastname':lastname, 'email':user.email, 
        'username':user.display_name,'userToken': user.uid}
        db.child('signup').push(data)
        return redirect(url_for('index'))

# @app.route('/lg', methods=['GET', 'POST'])
# def lg():
#     userTest = [{'hhname':'admin', 'ssword': '123456'}]
#     ertet = None
#     if request.method == 'POST':
#         for i in userTest:
#             if request.form['hhname'] != i['hhname'] or request.form['ssword'] != i['ssword']:
#                 ertet = "Try Again"
#                 return render_template('testlogin.html', error=ertet)
#             else:
#                 return redirect(url_for('index'))
#         session['hhname'] = request.form['hhname']
#         session['ssword'] = request.form['ssword']
#         return redirect(url_for('index'))
#     return render_template('testlogin.html')
        
# @app.route('/logout')
# def logout():
#     session.pop('hhname', None)
#     session.pop('ssword', None)
#     return redirect(url_for('lg'))


# @app.route('/key', methods=["POST"])
# def register():
#     firstname = request.form['firstname']
#     lastname = request.form['lastname']
#     email = request.form['email']
#     usname = request.form['usname']
#     pword = request.form['pword']
    
#     send = {'firstname':firstname, 'lastname':lastname, 'email':email, 'usname':usname, "pword":pword}

#     username = auth.create_user(email=email, password=pword, display_name=usname)
#     return jsonify({'user':username})

# @app.route('/logkey', methods=['POST'])
# def signin():
#     email = request.form['email']
#     pword = request.form['pword']
#     try:
#         pb.auth().sign_in_with_email_and_password(email,pword)
#         return jsonify({'user':'success'})
#     except:
#         return jsonify({'user':'error'})
 


if __name__=='__main__':
    app.run(debug=True, port=5010)