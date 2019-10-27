#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask import render_template
import json, os

import storage, common

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__, template_folder=common.get_abs_path('templates'))

LOCAL_ENV = os.getenv('ENVIRONMENT', '') == 'local'
SECRET = common.read_line_from('secret.txt')

@app.route('/update', methods=['POST'])
def update():
    if 'secret' not in request.json or request.json['secret'] != SECRET:
        return abort(403)

    readouts = []
    for arg in list(common.Sensor):
        name = arg.name

        if name not in request.json:
            return abort(400)

        if not common.try_parse_float(request.json[name]):
            return abort(406)
        else:
            readouts.append(request.json[name])

    storage.put(LOCAL_ENV, readouts)
    return 'success', 202


@app.route('/get/last', methods = ['GET'])
def get_last():
    return render_template('get.html',
        data=storage.get_last(LOCAL_ENV),
        units=common.get_units(),
    )

@app.route('/get/last/json', methods=['GET'])
def get_last_json():
    return jsonify(storage.get_last(LOCAL_ENV))


# @app.route('/get/day', methods = ['GET'])
# def get_day():
#     return render_template('get.html',
#         data=storage.get_day(LOCAL_ENV),
#         units=common.get_units(),
#     )

# @app.route('/get/day/json', methods=['GET'])
# def get_day_json():
#     return jsonify(storage.get_day(LOCAL_ENV))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
