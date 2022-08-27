import flask
from .templates import getTemplateFolder
from . import login
from problem import Problem
import judge
from werkzeug.exceptions import RequestEntityTooLarge
import config.problem as config

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
    # TODO: add problem visibility
    try:
        return flask.render_template('problem.html', problem=defaultProblems[pid])
    except IndexError:
        flask.abort(404)

@blueprint.route('/problems/<int:pid>/submit', methods=['POST'])
def submit(pid):
    uid = login.getUid(flask.request)
    if not uid:
        return login.requireLogin()

    if pid >= len(defaultProblems):
        flask.abort(404)

    if 'file' not in flask.request.files:
        flask.flash('no file')
        return flask.redirect(f'/problems/{pid}')

    file = flask.request.files['file']
    if file.filename == '':
        flask.flash('file is empty')
        return flask.redirect(f'/problems/{pid}')

    dirname = judge.mkdir()
    try:
        file.save(f'{dirname}/submission.zip')
    except RequestEntityTooLarge:
        flask.flash('File too large')
        judge.cleanup(dirname)
        return flask.redirect(f'problems/{pid}')

    jid = judge.run(defaultProblems[pid], dirname)

    return flask.redirect(f'/result/{jid}')