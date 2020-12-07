from flask import Flask, abort, request, make_response, render_template, url_for, redirect, session
from lti_module.check_request import check_request
from lti_module import utils
from db import get_secret, add_session
from auth_checkers import check_auth, check_admin, check_task_access


app = Flask(__name__)
app.secret_key = 'super_secret_key'


@app.route('/<task_id>', methods=['GET'])
def index(task_id):
    user = check_auth()
    if check_task_access(task_id):  # == user['tasks'].get(task_id)
        return make_response(render_template('index.html', task_id=task_id))
    else:
        abort(401, "You don't have access to task_id={}. Allowed tasks: {}".format(task_id, list(user['tasks'].keys())))


@app.route('/lti', methods=['POST'])
def lti_route():
    params = request.form
    consumer_secret = get_secret(params.get('oauth_consumer_key', ''))
    request_info = dict( 
        headers=dict(request.headers),
        data=params,
        url=request.url,
        secret=consumer_secret
    )
    
    if check_request(request_info):
        # request is ok, let's start working!
        username = utils.get_username(params)
        custom_params = utils.get_custom_params(params)
        task_id = custom_params.get('task_id', 'default_task_id')
        role = utils.get_role(params)
        params_for_passback = utils.extract_passback_params(params) 

        add_session(username, task_id, params_for_passback, role)
        session['session_id'] = username

        return redirect(url_for('index', task_id=task_id))
    else:
        abort(403)


if __name__ == "__main__":
    app.debug = True
    app.run()
