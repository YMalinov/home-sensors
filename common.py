#!/usr/bin/python

import os

class sensor:
    ds18_in = 'ds18_in'
    ds18_out = 'ds18_out'
    bme_temp = 'bme_temp'
    bme_pressure = 'bme_pressure'
    bme_humidity = 'bme_humidity'

def get_sensors():
    return [ # subject to changes
        sensor.ds18_in,
        sensor.ds18_out,
        sensor.bme_temp,
        sensor.bme_pressure,
        sensor.bme_humidity
    ]

def get_abs_path(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

def try_parse_float(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def read_line_from(path):
    file = open(get_abs_path(path), 'r')
    line = file.readline()
    file.close()

    return line.strip() # just in case
