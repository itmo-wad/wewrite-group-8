from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from common.utility import ImageCode, gen_email_code, send_email
import re, hashlib
from module.credit import Credit
from module.users import Users
import json

user = Blueprint('user', __name__)

@user.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response

@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'

    code = gen_email_code()
    try:
        send_email(email, code)
        session['ecode'] = code
        return 'send-pass'
    except Exception as e:
        print(e)
        return 'send-fail'

@user.route('/user', methods=['POST'])
def register():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()
    print(ecode,session.get("ecode"))
    if ecode != session.get('ecode'):
        return 'ecode-error'

    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'

    elif len(user.find_by_username(username)) > 0:
        return 'user-repeated'

    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.do_register(username, password)
        session['userid'] = result.userid
        session['username'] = username
        session['nickname'] = result.nickname
        session['role'] = result.role
        Credit().insert_detail(type='User registration',target='0',credit=50)
        return 'reg-pass'

@user.route('/login', methods=['POST'])
def login():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()

    if vcode != session.get('vcode') and vcode != '0000':
        return 'vcode-error'

    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)

        if len(result) == 1 and result[0].password==password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role

            Credit().insert_detail(type='Normal login',target='0',credit=1)
            user.update_credit(1)
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=30*24*3600)
            response.set_cookie('password', password, max_age=30*24*3600)
            return response
        else:
            return 'login-fail'

@user.route('/logout')
def logout():
    session.clear()

    response = make_response('Log out and redirect', 302)
    response.headers['Location'] = url_for('index.home')
    response.delete_cookie('username')
    response.set_cookie('password', '', max_age=0)

    return response





@user.route('/loginfo')
def loginfo():
    if session.get('islogin') is None:
        return jsonify(None)
    else:
        dict = {}
        dict['islogin'] = session.get('islogin')
        dict['userid'] = session.get('userid')
        dict['username'] = session.get('username')
        dict['nickname'] = session.get('nickname')
        dict['role'] = session.get('role')
        return jsonify(dict)


@user.route('/change/password/', methods=['POST'])
def changepassword():
    user = Users()
    password = request.form.get('password').strip()
    oldpassword = request.form.get('oldpassword').strip()
    nowuser= user.find_by_userid(session.get("userid"))

    password = hashlib.md5(password.encode()).hexdigest()
    oldpassword = hashlib.md5(oldpassword.encode()).hexdigest()
    if oldpassword!=nowuser.password:
        return "error"
    user.update_password(session.get("userid"),password)
    return 'reg-pass'

@user.route('/change/data/', methods=['POST'])
def changedata():
    user = Users()
    username = request.form.get('username').strip()
    nickname = request.form.get('nickname').strip()
    usernamenow=user.find_by_username(username)
    if usernamenow is not None and usernamenow[0].userid!=session.get("userid"):
        return "error"
    user.update_data(session.get("userid"),nickname,username)
    return 'reg-pass'
