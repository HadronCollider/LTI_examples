from flask import Flask, request
from lti_module.check_request import check_request
from db import get_secret


app = Flask(__name__)

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
    else:
        return 'Not hi!'



if __name__ == "__main__":
    app.debug = True
    app.run()
