import flask
from .templates import getTemplateFolder
import config

app = flask.Flask('main', template_folder=getTemplateFolder())
app.secret_key = config.secret
app.config['MAX_CONTENT_LENGTH'] = config.maxContentLength


from . import login, problems, result
for page in (login, problems, result):
    app.register_blueprint(page.blueprint)

@app.route('/')
def root():
    return flask.redirect('/problems')

