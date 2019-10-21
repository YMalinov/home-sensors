#!/usr/bin/python3

import os

class sensor:
    # short/long are the differentiating terms between both ds18 sensors, due
    # to the difference in the length of their cables (they're in waterproof
    # probes)
    ds18_long_temp = 'ds18_long_temp'
    ds18_short_temp = 'ds18_short_temp'
    bme_temp = 'bme_temp'
    bme_pressure = 'bme_pressure'
    bme_humidity = 'bme_humidity'

def get_sensors():
    return [ # subject to changes
        sensor.ds18_long_temp,
        sensor.ds18_short_temp,
        sensor.bme_temp,
        sensor.bme_pressure,
        sensor.bme_humidity
    ]

def get_abs_path(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

def read_line_from(path):
    file = open(get_abs_path(path), 'r')
    line = file.readline()
    file.close()

    return line.strip() # just in case

def try_parse_float(input_num):
    try:
        float(input_num)
        return True
    except ValueError:
        return False

def round_num_dict(input_dict):
    return { k:round(v, 2) for (k, v) in input_dict.items() }
