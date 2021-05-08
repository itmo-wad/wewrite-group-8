from flask import session
from common.database import dbconnect
import time, random

from module.article import Article

db = dbconnect()

class Favorite(db.Document):
    articleid=db.IntField()
    userid=db.IntField()
    canceled=db.BooleanField(default=False)
    createtime=db.DateTimeField()
    updatetime=db.DateTimeField()

    def insert_favorite(self, articleid):
        row = Favorite.objects.filter(articleid=articleid, userid=session.get('userid')).first()
        if row is not None:
            row.canceled = False
            row.save()
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(articleid=articleid, userid=session.get('userid'),canceled=False,createtime=now, updatetime=now)
            favorite.save()
    def cancel_favorite(self, articleid):
        row = Favorite.objects.filter(articleid=articleid, userid=session.get('userid')).first()
        row.canceled = True
        row.save()
    def check_favorite(self, articleid):
        row = Favorite.objects.filter(articleid=articleid, userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == True:
            return False
        else:
            return True

    def find_my_favorite(self):
        favorite=Favorite.objects.filter(userid = session.get('userid')).filter(canceled=False).all()
        print(favorite)
        result=[]
        for i in favorite:
            article=Article.objects.filter(articleid=i.articleid).first()
            dict1={}
            dict1["favorite"]=i
            dict1["article"]=article
            result.append(dict1)
        return result

    def switch_favorite(self, favoriteid):
        row = Favorite.objects.filter(favoriteid=favoriteid).first()
        if row.canceled == True:
            row.canceled = False
        else:
            row.canceled = True
        row.save()
        return row.canceled