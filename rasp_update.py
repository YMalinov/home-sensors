#!/usr/bin/python3

import requests
import common, rasp_ds18, rasp_bme
from common import sensor

def round_number(num):
    return round(num, 2)

ds18_info = rasp_ds18.get()
bme_info = rasp_bme.get()

print('DS18 in temp:', ds18_info[sensor(1).name], 'C')
print('DS18 out temp:', ds18_info[sensor(2).name], 'C')

print('BME temperature:', bme_info[sensor(3).name], 'C')
print('BME pressure:', bme_info[sensor(4).name], 'hPa')
print('BME humidity:', bme_info[sensor(5).name], '%')

backend_url = common.read_line_from('backend_url.txt') + '/update'
secret = common.read_line_from('secret.txt')

data = { **ds18_info, **bme_info, 'secret': secret }

print(requests.post(backend_url, json=data))
