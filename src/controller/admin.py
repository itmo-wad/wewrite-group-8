from flask import Blueprint, render_template, session, request, jsonify,redirect
from module.article import Article
from module.users import Users
import math

admin = Blueprint("admin", __name__)

# @admin.before_request
# def before_admin():
#     if session.get('islogin') != 'true' or session.get('role') != 'admin':
#         return 'perm-denied'

@admin.route('/admin')
def sys_admin():
    pagesize = 50
    article = Article()
    result = article.find_all_except_draft(0, pagesize)
    total = math.ceil(article.get_count_except_draft() / pagesize)
    return render_template('system-admin.html', page=1, result=result, total=total)

@admin.route('/admin/article/<int:page>')
def admin_article(page):
    pagesize = 50
    start = (page - 1) * pagesize
    article = Article()
    result = article.find_all_except_draft(start, pagesize)
    total = math.ceil(article.get_count_except_draft() / pagesize)
    return render_template('system-admin.html', page=page, result=result, total=total)

@admin.route('/admin/type/<int:type>-<int:page>')
def admin_search_type(type, page):
    pagesize = 50
    start = (page - 1) * pagesize
    result, total = Article().find_by_type_except_draft(start, pagesize, type)
    total = math.ceil(total / pagesize)
    return render_template('system-admin.html', page=page, result=result, total=total)

@admin.route('/admin/search/<keyword>')
def admin_search_headline(keyword):
    result = Article().find_by_headline_except_draft(keyword)
    return render_template('system-admin.html', page=1, result=result, total=1)

@admin.route('/admin/article/hide/<int:articleid>')
def admin_article_hide(articleid):
    hidden = Article().switch_hidden(articleid)
    return str(hidden)


@admin.route("/admin/user/")
def admin_user_list():
    userlist=Users().find_all()
    print(userlist)
    return render_template('system-user.html',userlist=userlist)

@admin.route("/admin/user/del/<int:userid>")
def admin_user_del(userid):
    Users().delete(userid)
    return redirect("/admin/user/")


@admin.route('/admin/article/check/<int:articleid>')
def admin_article_check(articleid):
    checked = Article().switch_checked(articleid)
    return str(checked)

@admin.route('/admin/article/hide2/<int:articleid>')
def admin_article_hide2(articleid):
    hidden = Article().switch_hidden(articleid)
    return redirect("/user/article")

@admin.route('/admin/article/drafted/<int:articleid>')
def admin_article_drafted(articleid):
    drafted = Article().switch_publish(articleid)
    return redirect("/user/article")