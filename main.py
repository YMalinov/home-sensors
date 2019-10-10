from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import json, os

import storage, util

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

LOCAL_ENV = os.getenv('ENVIRONMENT', '') == 'local'
SECRET = open(util.get_abs_path('secret.txt'), 'r').readline()

@app.route('/update', methods = ['POST'])
def update():
    if 'secret' not in request.json or request.json['secret'] != SECRET:
        return abort(403)

    if 'in' not in request.json or 'out' not in request.json:
        return abort(400)

    in_temp = request.json['in']
    out_temp = request.json['out']

    if not util.try_parse_float(in_temp) or not util.try_parse_float(out_temp):
        return abort(406)

    storage.put(LOCAL_ENV, request.json['in'], request.json['out'])
    return 'success', 202

@app.route('/get', methods = ['GET'])
def get():
    return jsonify(storage.get(LOCAL_ENV))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
