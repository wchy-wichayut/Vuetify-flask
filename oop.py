

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
        for i in ref.each()[62:]:
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
                'fname':fname, 'message': message,'product':product, 'tel':tel, 'tag':tag, 'key':key}
            lst.append(box)
            count += 1
        return lst


