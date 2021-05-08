from flask import session
from common.database import dbconnect
import time

db = dbconnect()

class Credit(db.Document):
    creditid=db.IntField()
    userid=db.IntField()
    category=db.StringField()
    target=db.StringField()
    credit=db.IntField()
    createtime=db.DateTimeField()
    updatetime=db.DateTimeField()
    def insert_detail(self, type, target, credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'), category=type, target=target,
                        credit=credit, createtime=now, updatetime=now)
        credit.save()
    def check_payed_article(self, articleid):

        if session.get("userid") is None:
            return False
        result = Credit.objects.filter(target=str(articleid)).filter(userid=int(session.get("userid"))).all()


        if len(result) > 0:
            return True
        else:
            return False
