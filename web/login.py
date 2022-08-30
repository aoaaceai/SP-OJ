import flask
from .templates import getTemplateFolder
import user
import config.login as config

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

def checkLogin():
    if not getCookie(flask.request, 'login'):
        flask.abort(requireLogin())
        
def getUid():
    return getCookie(flask.request, 'login')

def requireLogin():
    response = flask.redirect('/login')
    response.delete_cookie('login')
    return response

def getCurrentUser():
    u = user.getUser(getUid())
    if not u:
        flask.abort(requireLogin())
    return u

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if getUid():
        return flask.redirect('/')
    elif flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        uid = flask.request.form.get('uid')
        password = flask.request.form.get('password')

        result = user.verify(uid, password)

        if not result:
            flask.flash('Login failed.', 'danger')
            return flask.redirect('/login')

        response = flask.redirect('/')
        response.set_cookie('login', signCookie(uid))
        return response

@blueprint.route('/logout')
def logout():
    response = flask.redirect('/')
    response.delete_cookie('login')
    return response
