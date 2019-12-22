#!/usr/bin/python3

import os
def get_abs_path(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

# so we have access to shared libs
import sys
sys.path.insert(1, get_abs_path('..'))

import common
import requests
import ds18
import bme
import sds

sensor_data = { **ds18.get(), **bme.get(), **sds.get() }
units = common.get_units()

for k, v in sensor_data.items():
    print(k + ':', v, units[k])

backend_url = common.read_line_from('backend_url.txt') + '/update'
secret = common.read_line_from('secret.txt')

data = { **sensor_data, 'secret': secret }

print(requests.post(backend_url, json=data))
