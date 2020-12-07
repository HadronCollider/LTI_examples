from flask import Flask, request, make_response, render_template, url_for, redirect
from lti_module.check_request import check_request
from lti_module import utils
from db import get_secret


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    print(request.args)
    return make_response(render_template('index.html', **request.args))


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
        lti_params = {
            'username': utils.get_username(params),
            'person_name': utils.get_person_name(params),
            'course_title': utils.get_title(params),
            'return_url': utils.get_return_url(params),
            'custom_params': utils.get_custom_params(params),
            'role': utils.get_role(params)
        }
        return redirect(url_for('index', **lti_params))
    else:
        abort(403)


if __name__ == "__main__":
    app.debug = True
    app.run()
