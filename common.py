import os
from enum import Enum, unique, auto

@unique
class Sensor(Enum):
    # Short/long are the differentiating terms between both ds18 sensors, due to
    # the difference in the length of their cables (they're enclosed in
    # waterproof probes). The order is important here - should correspond to
    # order of elements in sheets as well.
    ds18_long_temp = auto()
    ds18_short_temp = auto()
    bme_temp = auto()
    bme_pressure = auto()
    bme_humidity = auto()
    # sds_pm25 = auto() # PM2.5
    # sds_pm10 = auto() # PM10
    mq7_carb_mono = auto()

@unique
class Client(Enum):
    rasp_a = 1
    rasp_b = 2
    rasp_c = 3

    def from_str(label):
        mapping = {
            'rasp_a': Client.rasp_a,
            'rasp_b': Client.rasp_b,
            'rasp_c': Client.rasp_c,
        }

        return mapping[label] if label else Client.rasp_b

sensors = {
    Client.rasp_a: [
        Sensor.mq7_carb_mono,
    ],
    Client.rasp_b: [
        Sensor.ds18_short_temp,
        Sensor.bme_temp,
        Sensor.bme_pressure,
        Sensor.bme_humidity,
        # Sensor.sds_pm25,
        # Sensor.sds_pm10,
    ],
    Client.rasp_c: [
        Sensor.ds18_long_temp,
    ],
}

def get_units():
    units = [
        '°C',
        '°C',
        '°C',
        'hPa',
        '%',
        # 'µg/m³',
        # 'µg/m³',
        'ppm',
    ]

    return dict(zip([val.name for val in list(Sensor)], units))

def get_abs_path(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

def read_line_from(path):
    with open(get_abs_path(path), 'r') as file:
        return file.readline().strip()

def print_to_file(data, path):
    print(data)
    with open(get_abs_path(path), 'w') as file:
        print(data, file=file)

def round_num_dict(input_dict):
    return {
        k:v if isinstance(v, str) else round(v, 2) \
            for (k, v) in input_dict.items()
    }

def avg(arr):
    return sum(arr) / len(arr)
