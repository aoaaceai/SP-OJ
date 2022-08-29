import flask
from .templates import getTemplateFolder
from . import login
import judge

blueprint = flask.Blueprint('result', __name__, template_folder=getTemplateFolder())

@blueprint.route('/result/<jid>')
def result(jid):
    uid = login.getUid(flask.request)
    if not uid:
        return login.requireLogin()

    try:
        result = judge.jobs[jid]
    except KeyError:
        flask.abort(404)

    print(judge.jobs)
    print(result.ready)
    return flask.render_template('result.html', result=result)
    