import flask
from .templates import getTemplateFolder
from . import login
import problem
import judge
from werkzeug.exceptions import RequestEntityTooLarge
from quota import useQuota, getQuota

blueprint = flask.Blueprint('problems', __name__, template_folder=getTemplateFolder())

@blueprint.route('/problems/')
def problems():
    login.checkLogin()
    u = login.getCurrentUser()
    return flask.render_template('problems.html', problems=problem.getProblems(), user=u, getQuota=getQuota)

@blueprint.route('/problems/reload')
def reloadProblems():
    login.checkLogin()
    if login.getCurrentUser().isAdmin:
        problem.loadProblems()
    return flask.redirect('/problems')

@blueprint.route('/problems/<int:pid>')
def singleProblem(pid):
    login.checkLogin()

    prob = problem.getProblem(pid)
    if prob:
        return flask.render_template('problem.html', problem=prob)
    else:
        flask.abort(404)

@blueprint.route('/problems/<int:pid>/submit', methods=['POST'])
def submit(pid):
    login.checkLogin()

    prob = problem.getProblem(pid)
    user = login.getCurrentUser()

    if not prob:
        flask.abort(404)

    if not prob.available:
        flask.flash('Problem not available.', 'danger')
        return flask.redirect(f'/problems/{pid}')

    if not useQuota(pid, user.uid):
        flask.flash('Quota Exceeded.', 'danger')
        return flask.redirect(f'/problems/{pid}')

    if 'file' not in flask.request.files:
        flask.flash('No file.', 'danger')
        return flask.redirect(f'/problems/{pid}')

    file = flask.request.files['file']
    if file.filename == '':
        flask.flash('File is empty.', 'danger')
        return flask.redirect(f'/problems/{pid}')

    jid = judge.new()
    try:
        judge.saveZip(jid, file)
    except RequestEntityTooLarge:
        flask.flash('File too large', 'danger')
        judge.rmZip(jid)
        return flask.redirect(f'/problems/{pid}')

    judge.run(jid, prob)

    return flask.redirect(f'/result/{jid}')