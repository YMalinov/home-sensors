#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask import render_template
from datetime import timedelta
import json
import os

import storage
import common

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


@app.route('/get', methods = ['GET'])
def get():
    hours = request.args.get('hours', default=0, type=int)
    days = request.args.get('days', default=0, type=int)
    weeks = request.args.get('weeks', default=0, type=int)
    json = 'json' in request.args

    data = storage.get(LOCAL_ENV, timedelta(
        hours=hours,
        days=days,
        weeks=weeks,
    ))

    # Prettify result - most of the time these are not pretty numbers.
    data = common.round_num_dict(data)

    if json:
        return jsonify(data)
    else:
        return render_template('get.html',
            data=data,
            units=common.get_units(),
        )

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
