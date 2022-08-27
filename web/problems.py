import flask
from .templates import getTemplateFolder
from . import login
from problem import Problem

defaultProblems = [
    Problem(0, 'aoeu', 10, 'htns', 'desc'),
    Problem(1, 'htns', 20, 'aoeu', 'desc2')
]

blueprint = flask.Blueprint('problems', __name__, template_folder=getTemplateFolder())


@blueprint.route('/problems')
def problems():
    uid = login.getUid(flask.request)
    if not uid:
        return login.requireLogin()

    return flask.render_template('problems.html', problems=defaultProblems)

@blueprint.route('/problems/<int:pid>')
def problem(pid):
    try:
        return flask.render_template('problem.html', problem=defaultProblems[pid])
    except IndexError:
        flask.abort(404)

@blueprint.route('/problems/<int:pid>/submit', methods=['POST'])
def submit(pid):
    uid = login.getUid(flask.request)
    if not uid:
        return login.requireLogin()

    return 'TODO: receive the file'