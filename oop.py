

class FirebaseAPI:
    def __init__(self, db, transaction):
        self.db = db
        self.transaction = transaction

    # def transaction_index(self):
    #     lst = []
    #     count = 1
    #     ref = self.db.child(self.transaction).get()
    #     for i in ref.each()[62:]:
    #         userID = i.val()['userid']
    #         image = i.val()['img']
    #         profile = i.val()['profile']
    #         msg = i.val()['message']
    #         rep = i.val()['reply']
    #         day = i.val()['day']
    #         month = i.val()['month']
    #         year = i.val()['year']
    #         hour = i.val()['hour']
    #         minute = i.val()['min']
    #         second = i.val()['sec']
    #         key = i.key()
    #         group = {'userid': userID, 'img': image, 'profile': profile, 'message': msg, 'reply': rep,
    #                  'date_time': f'{year}/{month}/{day} {hour}:{minute}:{second}', 'key': key, "index": count
    #                  }
    #         lst.append(group)
    #         count += 1
    #     return lst

    def tabledemo(self):
        lst = []
        count = 1
        ref = self.db.child(self.transaction).get()
        for i in ref.each()[1:]:
            r = i.val()
            date = r['Date']
            time = r['Time']
            company = r['event']['company']
            email = r['event']['email']
            fname = r['event']['fname']
            message = r['event']['message']
            product = r['event']['product']
            tel = r['event']['tel']
            tag = r['tag']
            key = i.key()
            box = {'date/time': f'{date} {time}', 'company':company, 'email':email,
                'fname':fname, 'message': message,'product':product, 'tel':tel,
                 'tag':tag, 'key':key, 'index':count,'Date':date,"Time":time}
            lst.append(box)
            count += 1 
        return lst

    def tablecontact(self):
        lst = []
        count = 1
        ref = self.db.child(self.transaction).get()
        for i in ref.each()[1:]:
            r = i.val()
            date = r['Date']
            time = r['Time']
            ctemail = r['event']['contact_email']
            ctemaildiv = r['event']['contact_email_div']
            ctmessage = r['event']['contact_message']
            ctname = r['event']['contact_name']
            ctnamecompany = r['event']['contact_name_company']
            ctsubject = r['event']['contact_subject']
            cttel = r['event']['contact_tel']
            tag = r['tag']
            key = i.key()
            box = {'date/time':f'{date} {time}', 'contact_email':ctemail, 'contact_email_div':ctemaildiv, 'contact_message':ctmessage,
                    'contact_name':ctname, 'contact_name_company':ctnamecompany, 'contact_subject':ctsubject,
                    'contact_tel': cttel, 'tag':tag, 'key':key, 'index':count,'Date':date,"Time":time}
            lst.append(box)
            count += 1
        return lst

