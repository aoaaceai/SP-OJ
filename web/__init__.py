import flask
from .templates import getTemplateFolder
import config

app = flask.Flask('main', template_folder=getTemplateFolder())
app.secret_key = config.secret

from . import login, problems
for page in (login, problems):
    app.register_blueprint(page.blueprint)

@app.route('/')
def root():
    if not login.getUid(flask.request):
        return login.requireLogin()

    return flask.redirect('/problems')

