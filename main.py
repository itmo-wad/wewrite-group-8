from flask import Flask, abort, render_template
import os
from flask_mongoengine import MongoEngine

app = Flask(__name__, template_folder='template', static_url_path='/', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MONGODB_SETTINGS'] = {
    'db':   'blog2',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')

@app.errorhandler(500)
def server_error(e):
    return render_template('error-500.html')

@app.before_request
def before():
    url = request.path

    pass_list = ['/user', '/login', '/logout','/admin']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg'):
        pass

    elif session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username != None and password != None:
            user = Users()
            result = user.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role

def mytruncate(s, length, end='...'):
    count = 0
    new = ''
    for c in s:
        new += c
        if ord(c) <= 128:
            count += 0.5
        else:
            count += 1
        if count > length:
            break
    return new + end
app.jinja_env.filters.update(truncate=mytruncate)

@app.context_processor
def gettype():
    type = {
        '1': 'PHP development',
        '2': 'Java development',
        '3': 'Python development',

    }
    return dict(article_type=type)


@app.route('/upload', methods=['POST'])
def do_upload():
    headline = request.form.get('headline')
    content = request.form.get('content')
    file = request.files.get('upfile')
    suffix = file.filename.split('.')[-1]

    if suffix.lower() not in ['jpg', 'jpeg', 'png', 'rar', 'zip', 'doc', 'docx']:
        return 'Invalid'

    file.save('D:/test001.' + suffix)
    return 'Done'

if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)

    from controller.user import *
    app.register_blueprint(user)

    #
    from controller.admin import *
    app.register_blueprint(admin)
    #
    from controller.ucenter import *
    app.register_blueprint(ucenter)
    from controller.article import *
    app.register_blueprint(article)
    from controller.favorite import *
    app.register_blueprint(favorite)

    app.run(host='localhost', port=5002, debug=True)