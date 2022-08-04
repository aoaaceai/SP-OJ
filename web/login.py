import flask
from web.templates import getTemplateFolder
import db
import config

blueprint = flask.Blueprint('login', __name__, template_folder=getTemplateFolder())
blueprint.secret_key = config.loginSecretKey

session_serializer = flask.sessions.SecureCookieSessionInterface().get_signing_serializer(blueprint)

def signCookie(content):
    return session_serializer.dumps(content)

def getCookie(request, key):
    try:
        return session_serializer.loads(request.cookies.get(key))
    except:
        return None

def isLoggedIn(request):
    uid = getCookie(request, 'login')
    return uid

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if isLoggedIn(flask.request):
        return flask.redirect('/')
    elif flask.request.method == 'GET':
        failed = flask.request.args.get('failed') is not None
        return flask.render_template('login.html', failed=failed)
    else:
        uid = flask.request.form.get('uid')
        password = flask.request.form.get('password')

        result = db.checkPassword(uid, password)

        if not result:
            return flask.redirect('/login?failed')

        response = flask.redirect('/')
        response.set_cookie('login', signCookie(uid))
        return response

@blueprint.route('/logout')
def logout():
    response = flask.redirect('/')
    response.delete_cookie('login')
    return response
