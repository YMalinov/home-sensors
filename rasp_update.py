#!/usr/bin/python

import requests
import common, rasp_ds18, rasp_bme
from common import readout_ids

def round_number(num):
    return round(num, 2)

ds18_info = rasp_ds18.get()
bme_info = rasp_bme.get()

print('DS18 in temp:', ds18_info['in'], 'C')
print('DS18 out temp:', ds18_info['out'], 'C')

print('BME temperature:', bme_info['temperature'], 'C')
print('BME pressure:', bme_info['pressure'], 'hPa')
print('BME humidity:', bme_info['humidity'], '%')

backend_url = common.read_line_from('backend_url.txt') + '/update'
secret = common.read_line_from('secret.txt')

data = {
	readout_ids[0]: round_number(ds18_info['in']),
	readout_ids[1]: round_number(ds18_info['out']),
    readout_ids[2]: round_number(bme_info['temperature']),
    readout_ids[3]: round_number(bme_info['pressure']),
    readout_ids[4]: round_number(bme_info['humidity']),
	'secret': secret
}

requests.post(backend_url, json=data)
