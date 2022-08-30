import flask
from .templates import getTemplateFolder
from . import login
from problem import Problem
import judge
from werkzeug.exceptions import RequestEntityTooLarge

defaultProblems = [
    Problem(0, 'aoeu', 10, 'judger', 'aoeu\nhnts'),
    Problem(1, 'htns', 20, 'judger', 'desc2')
]

blueprint = flask.Blueprint('problems', __name__, template_folder=getTemplateFolder())

@blueprint.route('/problems')
def problems():
    login.checkLogin(flask.request)

    return flask.render_template('problems.html', problems=defaultProblems)

@blueprint.route('/problems/<int:pid>')
def problem(pid):
    login.checkLogin(flask.request)

    try:
        return flask.render_template('problem.html', problem=defaultProblems[pid])
    except IndexError:
        flask.abort(404)

@blueprint.route('/problems/<int:pid>/submit', methods=['POST'])
def submit(pid):
    login.checkLogin(flask.request)

    if pid >= len(defaultProblems):
        flask.abort(404)

    if 'file' not in flask.request.files:
        flask.flash('no file')
        return flask.redirect(f'/problems/{pid}')

    file = flask.request.files['file']
    if file.filename == '':
        flask.flash('file is empty', 'danger')
        return flask.redirect(f'/problems/{pid}')

    dirname = judge.mkdir()
    try:
        file.save(f'{dirname}/submission.zip')
    except RequestEntityTooLarge:
        flask.flash('File too large')
        judge.rmdir(dirname)
        return flask.redirect(f'problems/{pid}')

    jid = judge.run(defaultProblems[pid], dirname)

    return flask.redirect(f'/result/{jid}')