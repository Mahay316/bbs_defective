from flask import Flask, session, request, render_template, redirect, send_from_directory

from common import save_session, get_summary, type_to_str, startsWithList
from controller import auth, ueditor, message, comment, profile, search
from model import User, init_db
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.before_request
def auto_login():
    """automated login using cookie"""
    if session.get('isLogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username is not None and password is not None:
            result = User.find_by_username(username)
            if len(result) == 1 and password == result[0].password:
                save_session(result[0])


@app.before_request
def verify_login():
    """verify requests that need login"""
    # ignore pages don't need login
    if not startsWithList(request.path, ['/profile']):
        return
    if session.get('isLogin') is None:  # redirect to login page
        return redirect('/login?from=' + request.path)


@app.errorhandler(404)
def page_not_found(err):
    """customized 404 page"""
    return render_template('error-404.html')


@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/download/<file_path>')
# def download_avatar(file_path):
#     print(file_path)
#     dir_name = os.path.dirname(file_path)
#     file_name = file_path[len(dir_name):]
#     print(dir_name, file_name)
#     return send_from_directory(os.path.join('static', dir_name), filename=file_name, as_attachment=True)


@app.route('/download/<path:file_path>')
def download_avatar(file_path):
    print(file_path)
    dir_name = os.path.dirname(file_path)
    file_name = file_path[len(dir_name):].strip('/')
    print(dir_name, file_name)
    return send_from_directory(os.path.join('static', dir_name), filename=file_name, as_attachment=True)


# register function for Jinja
app.jinja_env.globals.update(get_summary=get_summary)
app.jinja_env.globals.update(type_to_str=type_to_str)

if __name__ == '__main__':
    app.app_context().push()
    init_db(app)

    app.register_blueprint(auth)
    app.register_blueprint(ueditor)
    app.register_blueprint(message)
    app.register_blueprint(comment)
    app.register_blueprint(profile)
    app.register_blueprint(search)
    app.run(debug=True)
