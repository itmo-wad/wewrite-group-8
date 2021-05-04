from flask import session

from common.database import dbconnect
import time, random
#
db = dbconnect()

class Users(db.Document):
    userid=db.SequenceField()
    username=db.StringField()
    password=db.StringField()
    nickname=db.StringField()
    avatar=db.StringField()
    qq=db.StringField()
    role=db.StringField()
    credit=db.IntField()
    createtime=db.DateTimeField()
    updatetime=db.DateTimeField()

    def find_all(self):
        user=Users.objects.filter(role="user").all()

        return user
    def delete(self,id):
        user=Users.objects.filter(userid=id)
        user.delete()
        return True
    def update_password(self,id,password):
        result = Users.objects.filter(userid=id).first()
        result.password=password
        result.save()
    def update_data(self,id,nickname,username):
        result = Users.objects.filter(userid=id).first()
        result.username=username
        result.nickname=nickname
        result.save()



    def find_by_username(self, username):
        result = Users.objects.filter(username=username).all()
        return result

    def do_register(self, username, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]
        avatar = str(random.randint(1, 15))
        user = Users(username=username, password=password, role='user', credit=50,
                     nickname=nickname, avatar=avatar + '.png', createtime=now, updatetime=now)
        user.save()
        return user

    def update_credit(self, credit):
        user=Users.objects.filter(userid=session.get('userid')).first()
        user.credit = int(user.credit) + credit
        user.save()
    def find_by_userid(self, userid):
        user = Users.objects.filter(userid=userid).first()
        return user