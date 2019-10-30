import os
from enum import Enum, unique

@unique
class Sensor(Enum):
    # Short/long are the differentiating terms between both ds18 sensors, due
    # to the difference in the length of their cables (they're enclosed in
    # waterproof probes). The order is important here - should correspond to
    # order of elements in sheet as well.
    ds18_long_temp = 1
    ds18_short_temp = 2
    bme_temp = 3
    bme_pressure = 4
    bme_humidity = 5
    sds_pm25 = 6 # PM2.5
    sds_pm10 = 7 # PM10

def get_units():
    units = [
        'C',
        'C',
        'C',
        'hPa',
        '%',
        'µg/m³',
        'µg/m³',
    ]

    return dict(zip([val.name for val in list(Sensor)], units))

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

def avg(arr):
    return sum(arr) / len(arr)
