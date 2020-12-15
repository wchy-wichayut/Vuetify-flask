

class FirebaseAPI:
    def __init__(self, db, transaction):
        self.db = db
        self.transaction = transaction

    def transaction_index(self):
        lst = []
        count = 1
        ref = self.db.child(self.transaction).get()
        for i in ref.each()[62:]:
            userID = i.val()['userid']
            image = i.val()['img']
            profile = i.val()['profile']
            msg = i.val()['message']
            rep = i.val()['reply']
            day = i.val()['day']
            month = i.val()['month']
            year = i.val()['year']
            hour = i.val()['hour']
            minute = i.val()['min']
            second = i.val()['sec']
            key = i.key()
            group = {'userid': userID, 'img': image, 'profile': profile, 'message': msg, 'reply': rep,
                     'date_time': f'{year}/{month}/{day} {hour}:{minute}:{second}', 'key': key, "index": count
                     }
            lst.append(group)
            count += 1
        return lst

    def getDemo_index(self):
        lst = []
        ref = self.db.child(self.transaction).get()
        count = 1
        for i in ref.each()[1:]:
            tag = i.val()['tag']
            date = i.val()['Date']
            time = i.val()['Time']
            company = i.val()['company']
            email = i.val()['email']
            fname = i.val()['fname']
            message = i.val()['message']
            product = i.val()['product']
            tel = i.val()['tel']
            key = i.key()
            group = {'tag': tag, 'date_time': f'{date} {time}', 'company': company, 'email': email,
                     'firstname': fname, 'msg': message, 'product': product, 'tel': tel, 'key': key}
            lst.append(group)
        count += 1
        return lst
