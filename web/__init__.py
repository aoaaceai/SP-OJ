import flask
from web.templates import getTemplateFolder
app = flask.Flask('main', template_folder=getTemplateFolder())

from web import login
app.register_blueprint(login.blueprint)

@app.route('/')
def root():
    if not login.isLoggedIn(flask.request):
        response = flask.redirect('/login')
        response.delete_cookie('login')
        return response

    return "You are logged in, but it's empty here..."

