import time

from flask import session
from common.database import dbconnect
from module.users import Users
db = dbconnect()


class Article(db.Document):
    articleid=db.SequenceField()
    userid=db.IntField()
    type=db.IntField()
    headline=db.StringField()
    replycount=db.StringField()
    content=db.StringField()
    thumbnail=db.StringField()
    credit=db.IntField()
    readcount=db.IntField()
    commentcount=db.IntField()
    hidden=db.BooleanField()
    drafted=db.BooleanField()
    checked=db.BooleanField()
    createtime=db.DateTimeField()
    updatetime=db.DateTimeField()
#
    def find_all(self):
        result = Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).all()
        return result
#
    def find_by_id(self, articleid):
        article=Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).filter(articleid=articleid).first()
        user=Users.objects.filter(userid=article.userid).first()

        return article,user

    def find_by_id2(self,articleid):
        article = Article.objects.filter(articleid=articleid).first()

        return article
#
    def find_with_users(self):

        article=Article.objects.filter(userid=session.get("userid")).order_by("articleid").all()

        return article

    def find_with_all(self,start,count):

        article=Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).order_by("articleid").all().limit(count).skip(start)
        result = []
        for i in article:
            user = Users.objects.filter(userid=i.userid).first()
            result.append({"article": i, "user": user})
        return result

#
    def get_total_count(self):
        count=Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).count()

        return count
#
    def find_by_type(self, type, start, count):
        article=Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).filter(type=type).order_by("articleid").limit(count).skip(start).all()

        result = []
        for i in article:
            user = Users.objects.filter(userid=i.userid).first()
            result.append({"article": i, "user": user})
        return result

    def get_count_by_type(self, type):
        count=Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).filter(type=type).count()

        return count


    def find_by_headline(self, headline, start, count):
        article = Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).filter(
            headline__contains=headline).order_by("articleid").limit(count).skip(start).all()

        result = []
        for i in article:
            user = Users.objects.filter(userid=i.userid).first()
            result.append({"article": i, "user": user})
        return result


    def get_count_by_headline(self, headline):
        count =Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True).filter(
            headline__contains=headline).order_by("articleid").count()
        return count
#
    def find_last_9(self):
        result = Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True)\
            .order_by("-articleid").limit(9).all()

        return result
#
    def find_most_9(self):
        result = Article.objects.filter(hidden=False).filter(drafted=False).filter(checked=True) \
            .order_by("-readcount").limit(9).all()

        return result
#

#

#
    def update_read_count(self, articleid):
        article=Article.objects.filter(articleid=articleid).first()
        article.readcount += 1
        article.save()

#
    def find_headline_by_id(self, articleid):
        article=Article.objects.filter(articleid=articleid).first()
        return article.headline
#

    def update_replycount(self, articleid):
        row = Article.objects.filter(articleid=articleid).first()
        row.replycount += 1
        row.save()#
#
    def insert_article(self, type, headline, content, thumbnail, credit, drafted=False, checked=False,hidden=False):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        userid = session.get('userid')

        article = Article(userid=userid, type=type, headline=headline, content=content,
                          thumbnail=thumbnail, credit=credit, drafted=drafted,
                          checked=checked, createtime=now, updatetime=now,hidden=hidden,readcount=0)
        article.save()

        return article.articleid
#
    def update_article(self, articleid, type, headline, content):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        row =Article.objects.filter(articleid=articleid).first()
        row.type = type
        row.headline = headline
        row.content = content

        row.updatetime = now
        row.save()
        return articleid
#
#
#
    def find_all_except_draft(self, start, count):
        result=Article.objects.filter(Article.drafted==False).order_by("-articleid").limit(count).skip(start).all()
        return result
#
    def get_count_except_draft(self):
        count=Article.objects.filter(Article.drafted==False).count()
        return count
#
    def find_by_type_except_draft(self, start, count, type):
        if type == 0:
            result = self.find_all_except_draft(start, count)
            total = self.get_count_except_draft()
        else:
            result = Article.objects.filter(Article.drafted == False).filter(type=type).order_by("-articleid").limit(count).skip(start).all()
            total = Article.objects.filter(Article.drafted == False).filter(type=type).count()

        return result, total
#
    def find_by_headline_except_draft(self, headline):
        result = Article.objects.filter(drafted=False).filter(
            headline__contains=headline).order_by("articleid").all()

        return result
#
    def switch_hidden(self, articleid):
        row=Article.objects.filter(articleid=articleid).first()
        if row.hidden == True:
            row.hidden = False
        else:
            row.hidden = True
        row.save()
        return row.hidden

    def switch_publish(self, articleid):
        row=Article.objects.filter(articleid=articleid).first()
        if row.drafted == True:
            row.drafted = False
        else:
            row.drafted = True
        row.save()
        return row.drafted
#

#
    def switch_checked(self, articleid):
        row=Article.objects.filter(articleid=articleid).first()
        if row.checked == True:
            row.checked = False
        else:
            row.checked = True
        row.save()
        return row.checked
