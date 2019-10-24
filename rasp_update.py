#!/usr/bin/python3

import requests
import common, rasp_ds18, rasp_bme

sensor_data = { **rasp_ds18.get(), **rasp_bme.get() }
units = common.get_units()

for k, v in sensor_data.items():
    print(k + ':', v, units[k])

backend_url = common.read_line_from('backend_url.txt') + '/update'
secret = common.read_line_from('secret.txt')

data = { **sensor_data, 'secret': secret }

print(requests.post(backend_url, json=data))
