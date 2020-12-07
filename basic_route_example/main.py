from flask import Flask, abort, request, make_response, render_template, url_for, redirect
from lti_module.check_request import check_request
from db import get_secret


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return make_response(render_template('index.html'))


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
        return 'Hi'
        #return redirect(url_for('index'))
    else:
        return 'Not hi!'
        #abort(403)


if __name__ == "__main__":
    app.debug = True
    app.run()
