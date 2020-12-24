from os import abort
from typing import Text
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask.helpers import make_response
from flask.templating import render_template_string
import pyrebase
import json
from oop import FirebaseAPI
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, StickerSendMessage, TextMessage,ImageSendMessage, LocationSendMessage, AudioSendMessage, VideoSendMessage, FlexSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction, CarouselTemplate, CarouselColumn, URIAction, DatetimePickerAction, ImagemapSendMessage, BaseSize, Video, ImagemapArea, ExternalLink, URIImagemapAction, MessageImagemapAction
from linebot.exceptions import InvalidSignatureError, LineBotApiError

with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()
    line_bot_api = LineBotApi(data["channal"])
    handler = WebhookHandler(data["secret"])

app = Flask(__name__)

# แยกวันเวลา
# del test['key']
# del test['index']
# d = datetime.datetime.strptime(test['date/time'], "%d-%m-%Y  %H:%M:%S")
# day, month, year, hour, minute, sec = d.day, d.month, d.year, d.hour, d.minute, d.second
# test['Date'] = test.pop('date/time')
# test.update({'Date': f'{day}-{month}-{year}'})
# test['Time'] = test
# test.update({'Time': f'{hour}:{minute}:{sec}'})
# print(test)

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
    db.child('requestDemo').child(id).update(group)
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

#--------- Chatbot ---------------------#

@app.route("/chatbot", methods=["POST"])
def chatbot():
    raw_json = request.get_json() # รับเข้ามา
    json_line = json.dumps(raw_json) # ตึงข้อมูลออกมา
    decoder = json.loads(json_line) # เอาไปใช้งาน

   
    # reply = decoder['events'][0]['replyToken'] # replyToken ของ user
    # text = decoder['events'][0]['message']['text'] # user พิมพ์เข้ามา
    # line_bot_api.push_message("U50481b342c27ecfde2a85b738589274e", TextSendMessage(text="Hello World")) # ส่งตนไหนก็ได้ ไม่เปลี่ยน Token
    with open("log_line.json", "w") as data_line: 
        json.dump(raw_json ,data_line)

    signature = request.headers['X-Line-Signature'] # ความปลอดภัย
    body = request.get_data(as_text=True)

    no_event = len(decoder['events'])
    for i in range(no_event):
        event = decoder['events'][i]
        event_type(event)
        

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return make_response(raw_json)



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text= 'สวัสดี 😀'))
    texts = event.message.text
#------------imageMap--------------------------#
    imagemap_message = ImagemapSendMessage(
    base_url='https://sv1.picz.in.th/images/2020/12/23/jpRD0q.jpg',
    alt_text='this is an imagemap',
    base_size=BaseSize(height=1040, width=1040),
    # video=Video(
    #     original_content_url='https://3b846bd26978.ngrok.io/static/cat.mp4',
    #     preview_image_url='https://fairtradejudaica.org/wp-content/uploads/2013/03/Song-Contest-Logo.gif',
    #     area=ImagemapArea(
    #         x=0, y=0, width=1040, height=585
    #     ),
    #     external_link=ExternalLink(
    #         link_uri='https://example.com/see_more.html',
    #         label='See More',
    #     ),
    # ),
    actions=[
        MessageImagemapAction(
            text='นอน',
            area=ImagemapArea(
                x=14, y=11, width=316, height=267
            )
        ),
        URIImagemapAction(
            link_uri='https://www.youtube.com/',
            area=ImagemapArea(
                x=362, y=12, width=320, height=266
            )
        ),
        MessageImagemapAction(
            text='หิวข้าวววว!!!',
            area=ImagemapArea(
                x=720, y=12, width=311, height=255
            )
        ),
        URIImagemapAction(
            link_uri='https://www.youtube.com/',
            area=ImagemapArea(
                x=14, y=302, width=320, height=267
            )
        ),
        URIImagemapAction(
            link_uri='https://www.dota2.com/play/',
            area=ImagemapArea(
                x=357, y=304, width=323, height=269
            )
        ),
        MessageImagemapAction(
            text='hahaha555',
            area=ImagemapArea(
                x=704, y=306, width=320, height=260
            )
        )
    ]
)
#------------imageMap--------------------------#

#------------carousel--------------------------#
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://1.bp.blogspot.com/-77J_hFsHhck/WDVTu_vI59I/AAAAAAAAl7U/UOdknmL9is8hnzGwky94M2iiGvaaJeolwCPcB/s1600/bg-animation-013.gif',
                title='ยินดีต้อนรับ',
                text='สวัสดี',
                actions=[
                    MessageAction(
                        label='คลิ๊ก',
                        text='เย้ เย'
                    )
                ],
        thumbnailImageUrl= "PROVIDE_URL_FROM_YOUR_SERVER",
        imageBackgroundColor= "#CCF912"
            ),
            CarouselColumn(
                thumbnail_image_url='https://2.bp.blogspot.com/-ZDy7jBeGLsY/WDVTuwUydJI/AAAAAAAAl7U/dLXO4cs5AZoMetxU_FozEl66M-b-RMn1wCPcB/s1600/bg-animation-014.gif',
                title='Food',
                text='อาหาร',
                actions=[
                    URIAction(
                        label='Web',
                        uri='https://www.kfc.co.th/'
                    )
                ],
        imageBackgroundColor= "#0C0101"
            ),
            CarouselColumn(
                thumbnail_image_url='https://st3.depositphotos.com/1229718/16838/i/1600/depositphotos_168380432-stock-photo-time-date-background.jpg',
                title='Welcome',
                text='Hello',
                actions=[
                    DatetimePickerAction(
                label='Click',
                data='สวัสดี',
                mode="datetime",
                initial= "2020-12-22T15:19",
                max= "2021-12-22T15:19",
                min= "2019-12-22T15:19"
            )
                ],
                thumbnailImageUrl = "PROVIDE_URL_FROM_YOUR_SERVER",
        imageBackgroundColor= "#F011F2"
            )
        ]
    )
)
#------------carousel--------------------------#

#------------Confirm message--------------------------#
    confirm_template_message = TemplateSendMessage(
    alt_text='this is a confirm template',
    template=ConfirmTemplate(
        text='Are you sure?',
        actions=[
            PostbackAction(
                label='No',
                display_text='ปฎิเสธ',
                data='hello'
            ),
            MessageAction(
                label='Yes',
                text='ยอมรับ'
            )
        ]
    )
)
#------------Confirm message--------------------------#   

#------------flex--------------------------#
    flex_message = FlexSendMessage(
    alt_text='hello',
    contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://1.bp.blogspot.com/-F79__e-W7Ak/VOx9OdxH7FI/AAAAAAAAj3o/5Mjn0XU_-bo/s1600/bg.dookdik.008.gif",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "backgroundColor": "#5CBFCBFF",
    "action": {
      "type": "uri",
      "label": "Line",
      "uri": "https://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Brown Cafe",
        "weight": "bold",
        "size": "xl",
        "contents": []
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
            "size": "sm"
          },
          {
            "type": "icon",
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Heart_font_awesome.svg/1200px-Heart_font_awesome.svg.png",
            "size": "sm"
          },
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
            "size": "sm"
          },
          {
            "type": "icon",
            "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzdikfDI9FSkeTT5QslMs2PQOwrRNV9neesw&usqp=CAU",
            "size": "sm"
          },
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "3.5",
            "size": "sm",
            "color": "#999999",
            "flex": 0,
            "margin": "md",
            "contents": []
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "margin": "lg",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Place",
                "size": "sm",
                "color": "#AAAAAA",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                "size": "sm",
                "color": "#666666FF",
                "flex": 5,
                "wrap": True,
                "contents": []
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Time",
                "size": "sm",
                "color": "#AAAAAA",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": "10:00 - 23:00",
                "size": "sm",
                "color": "#666666",
                "flex": 5,
                "wrap": True,
                "contents": []
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "flex": 0,
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "WEBSITE",
          "uri": "https://www.themall.co.th/th/about-us"
        },
        "height": "sm",
        "style": "link"
      }
    ]
  }
}
)
#------------flex--------------------------#

    
    print(texts)
    if texts == 'ไง':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= 'สวัสดี 😀'))
    elif texts == 'location' or texts == 'โล':
        line_bot_api.reply_message(event.reply_token , LocationSendMessage(title='My Location', address='Unknow',
                                                                 latitude=13.77406313026302, longitude=100.70916621761938))   
    elif texts == 'flex':
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif texts == 'cftem':
        line_bot_api.reply_message(event.reply_token, confirm_template_message)   
    elif texts == "crst":
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif texts == "เย้ เย":
        line_bot_api.reply_message(event.reply_token , VideoSendMessage(original_content_url='https://3b846bd26978.ngrok.io/static/cat.mp4',
                                                                        preview_image_url='https://fairtradejudaica.org/wp-content/uploads/2013/03/Song-Contest-Logo.gif')) 
    elif texts == "im":
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= 'งง???')) 
        
    
    

        
    
    



def event_type(event):
    typeline = event['message']['type']
    userId = event['source']['userId']
    imageid = event['message']['id']
    
    print(userId)
    
    if typeline == 'image':
        message_content = line_bot_api.get_message_content(imageid)
        with open('static/shinchan.jpg', 'wb') as fd:
          for i in message_content.iter_content():
            fd.write(i)
        line_bot_api.push_message(userId, ImageSendMessage(
                                      original_content_url='https://3b846bd26978.ngrok.io/static/shinchan.jpg', 
                                      preview_image_url='https://3b846bd26978.ngrok.io/static/shinchan.jpg'))

    elif typeline == 'sticker':
        line_bot_api.push_message(userId, StickerSendMessage(package_id='11537', sticker_id='52002746'))
        
    elif typeline == 'location':
        line_bot_api.push_message(userId, LocationSendMessage(title='My Location', address='Unknow',
                                                                 latitude=13.77406313026302, longitude=100.70916621761938))
    
    elif typeline == "audio":
        # ms_audio = line_bot_api.get_message_content(imageid)
        # with open('static/tan.mp3', 'wb') as fd:
        #     for i in ms_audio.iter_content():
        #         fd.write(i)
        line_bot_api.push_message(userId, AudioSendMessage(original_content_url='https://3b846bd26978.ngrok.io/static/tan.mp3', duration=235000))
    

    return event

#--------- Chatbot ---------------------#


@app.route("/test", methods=["GET", "POST"])
def test():
  if request.method == "POST":
    test = request.get_json()
    print(test)
    return make_response(test)
  else:
    return render_template('line.html')




if __name__ == '__main__':
    app.run(debug=True, port=8080)
 