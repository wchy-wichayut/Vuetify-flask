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
@app.route('/getDemo')
def indexDemo():
    return render_template('getDemo.html')

@app.route('/getContact')
def getContact():
   return render_template('getContact.html')

 
# @app.route('/json_chatbot')
# def chatbot():
#     fb = FirebaseAPI(db, "chatbot_transactions")
#     lst = fb.transaction_index()
#     data = {
#         "ref": lst[::-1]
#     }
#     return jsonify(data)

# @app.route('/update_chatbot/<id>',methods=["POST"])
# def update_index(id):
#     post_data = request.get_json()
#     print(id)
#     print(post_data)
#     db.child('chatbot_transactions').child(id).update(post_data)
#     return make_response(post_data)

# @app.route('/delete_chatbot/<id>',methods=["POST"])
# def delete_index(id):
#     post_data = request.get_json()
#     print(id)
#     print(post_data)
#     db.child("chatbot_transactions").child(id).remove()
#     return make_response(post_data)

# ----------------GetDemo-------------------- #

@app.route('/json_getdemo')
def getdemo():
    fb = FirebaseAPI(db, "requestDemo")
    lst = fb.tabledemo()
    data = {
        'ref': lst[::-1]
    }
    return jsonify(data)

@app.route('/update_getdemo/<id>',methods=["POST"])
def update_getdemo(id):
    post_data = request.get_json()
    print(id)
    print(post_data)
    # date = post_data['Date']
    # time = post_data['Time']
    # company = post_data['company']
    # email = post_data['email']
    # fname = post_data['fname']
    # message = post_data['massage']
    # product = post_data['product']
    # tel = post_data['tel']
    # tag = post_data['tag']
    group = {'Date': post_data['Date'],'Time':post_data['Time'], 'event':{'company':post_data['company'], 'email':post_data['email'], 'fname':post_data['fname'], 'message':post_data['message'],
     'product':post_data['product'], 'tel':post_data['tel']},'tag':post_data['tag']}
    # db.child('requestDemo').child(id).update(group)
    return make_response(group)

@app.route('/delete_getdemo/<id>',methods=["POST"])

def delete_getdomo(id):
    post_data = request.get_json()
    print(id)
    print(post_data)
    db.child("requestDemo").child(id).remove()
    return make_response(post_data)

# ----------------Contract-------------------- #

@app.route('/json_contact')
def contract():
    fb = FirebaseAPI(db, "requestContract")
    lst = fb.tablecontact()
    data = {
        'ref': lst[::-1]
    }
    return jsonify(data)

@app.route('/update_contact/<id>',methods=["POST"])
def update_contact(id):
    post_data = request.get_json()
    print(id)
    print(post_data)
    group = {'Date': post_data['Date'],'Time':post_data['Time'], 
        'event':{'contact_email':post_data['contact_email'], 'contact_email_div':post_data['contact_email_div'], 'contact_message':post_data['contact_message'], 'contact_name':post_data['contact_name'],
        'contact_name_company':post_data['contact_name_company'],'contact_subject':post_data['contact_subject'], 'contact_tel':post_data['contact_tel']},'tag':post_data['tag']}
    db.child('requestContract').child(id).update(group)
    return make_response(group)

@app.route('/delete_contact/<id>',methods=["POST"])
def delete_contact(id):
    post_data = request.get_json()
    print(id)
    print(post_data)
    db.child("requestDemo").child(id).remove()
    return make_response(post_data)

# -----------------Chat Bot----------------- #
@app.route('/webhook')
def webhook():
   return 'ok'





if __name__ == '__main__':
    app.run(debug=True, port=8080)
 