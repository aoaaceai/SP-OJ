import flask
from web.templates import getTemplateFolder
from web import login
import db


blueprint = flask.Blueprint('problems', __name__, template_folder=getTemplateFolder())


@blueprint.route('/problems')
def problems():
    uid = login.getUid(flask.request)
    if not uid:
        return login.requireLogin()

    return 'This is the problems page'