import flask
from web.templates import getTemplateFolder
app = flask.Flask('main', template_folder=getTemplateFolder())

from web import login
from web import problems
app.register_blueprint(login.blueprint)
app.register_blueprint(problems.blueprint)

@app.route('/')
def root():
    if not login.getUid(flask.request):
        return login.requireLogin()

    return flask.redirect('/problems')

