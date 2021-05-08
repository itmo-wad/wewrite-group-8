from flask import Blueprint, render_template,session
from module.favorite import Favorite
from module.article import Article
from module.users import Users
from flask import request
ucenter = Blueprint("ucenter", __name__)

@ucenter.route('/ucenter')
def user_center():
    result = Favorite().find_my_favorite()
    return render_template('user-center.html', result=result)

@ucenter.route('/user/favorite/<int:favoriteid>')
def user_favorite(favoriteid):
    canceled = Favorite().switch_favorite(favoriteid)
    return str(canceled)

@ucenter.route('/user/post')
def user_post():
    id=request.args.get("id")
    if id is not None:
        article=Article().find_by_id2(id)
    else:
        article=None

    return render_template('user-post.html',article=article)


@ucenter.route('/user/article')
def user_post_list():
    result = Article().find_with_users()
    return render_template('user-post-list.html',result=result)

@ucenter.route('/user/person')
def user_person():
    result = Users().find_by_userid(session["userid"])
    return render_template('user-person.html',user=result)