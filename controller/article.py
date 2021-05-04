import os

from flask import Blueprint, abort, render_template, request, session

from common.utility import parse_image_url, generate_thumb
from module.article import Article
from module.credit import Credit
from module.favorite import Favorite
from module.users import Users
import math

article = Blueprint("article", __name__)



@article.route('/article/<int:articleid>')
def read(articleid):
    try:
        result,user = Article().find_by_id(articleid)
        if result is None:
            abort(404)
    except Exception as e:
        abort(500)
    article=Article()
    last = article.find_last_9()
    most = article.find_most_9()


    payed = Credit().check_payed_article(articleid)

    position = 0
    if not payed:
        content = result.content
        temp = content[0:int(len(content)/2)]
        try:
            position = temp.rindex('</p>') + 4
            content = temp[0:position]

        except:
            content=temp
            position=int(len(content)/2)

    else:
        content = result.content


    Article().update_read_count(articleid)

    is_favorited = Favorite().check_favorite(articleid)


    total=0

    return render_template('article-user.html', article=result, position=position, payed=payed,
                           is_favorited=is_favorited,content=content,
                           total=total,user=user,last=last,most=most)


@article.route('/readall', methods=['POST'])
def read_all():
    position = int(request.form.get('position'))
    articleid = request.form.get('articleid')
    article = Article()
    result = article.find_by_id(articleid)
    content = result[0].content[position:]
    user=Users().find_by_userid(session.get("userid"))
    if user.credit<result[0].credit():
        return "not credit"

    payed = Credit().check_payed_article(articleid)
    if not payed:
        Credit().insert_detail(type='阅读文章', target=articleid, credit=-1*result[0].credit)

        Users().update_credit(credit=-1*result[0].credit)

    return content

@article.route('/prepost')
def pre_post():
    id=request.args.get("id")
    article=Article().find_by_id(id)
    return render_template('post-user.html',article=article)

@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    type = int(request.form.get('type'))
    credit = int(request.form.get('credit'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    articleid = int(request.form.get('articleid',0))
    print(drafted)
    if drafted==0:
        drafted=True
    else:
        drafted=False

    print(drafted)


    url_list = parse_image_url(content)
    if len(url_list) > 0:
        thumbname = generate_thumb(url_list)
    else:
        thumbname = '%d.png' % type

    article = Article()
    if articleid == 0:
        try:
            id = article.insert_article(type=type, headline=headline, content=content, credit=credit,
                                        thumbnail=thumbname, drafted=drafted, checked=checked,hidden=False)

            return str(id)
        except Exception as e:
            print(e)
            return 'post-fail'
    else:
        try:
            id = article.update_article(articleid=articleid, type=type,
                                        headline=headline, content=content)
            return str(id)
        except Exception as e:
            print(e)
            return 'post-fail'
