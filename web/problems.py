import flask
from .templates import getTemplateFolder
from . import login
import problem
import judge
from werkzeug.exceptions import RequestEntityTooLarge

blueprint = flask.Blueprint('problems', __name__, template_folder=getTemplateFolder())

@blueprint.route('/problems')
def problems():
    login.checkLogin(flask.request)

    return flask.render_template('problems.html', problems=problem.getProblems())

@blueprint.route('/problems/<int:pid>')
def singleProblem(pid):
    login.checkLogin(flask.request)

    prob = problem.loadProblem(pid)
    if prob:
        return flask.render_template('problem.html', problem=prob)
    else:
        flask.abort(404)

@blueprint.route('/problems/<int:pid>/submit', methods=['POST'])
def submit(pid):
    login.checkLogin(flask.request)

    prob = problem.loadProblem(pid)

    if not prob:
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

    jid = judge.run(prob, dirname)

    return flask.redirect(f'/result/{jid}')