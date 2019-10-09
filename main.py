from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

import json, os

from storage import Storage

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

LOCAL_ENV = os.getenv('ENVIRONMENT', '') == 'local'
SECRET = open('secret.txt', 'r').readline()

def try_parse_float(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

@app.route('/update', methods = ['POST'])
def update():
    if 'secret' not in request.json or request.json['secret'] != SECRET:
        return abort(403)

    if 'in' not in request.json or 'out' not in request.json:
        return abort(400)

    inTemp = request.json['in']
    outTemp = request.json['out']

    if not try_parse_float(inTemp) or not try_parse_float(outTemp):
        return abort(406)

    Storage.put(LOCAL_ENV, request.json['in'], request.json['out'])
    return 'success', 202

@app.route('/get', methods = ['GET'])
def get():
    return jsonify(Storage.get(LOCAL_ENV))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
