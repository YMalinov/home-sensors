import common
import requests

last_file = "../../last_readings.txt"

class client:
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data

    def post_update(self):
        sensor_data = { k.name:v for (k, v) in self.sensor_data.items() }
        units = common.get_units()

        readings = ''
        for k, v in sensor_data.items():
            readings += '%s: %s %s\n' % (k, v, units[k])

        backend_url = common.read_line_from('backend_url.txt') + '/update'
        secret = common.read_line_from('secret.txt')

        data = { **sensor_data, 'secret': secret }

        result = requests.post(backend_url, json=data)
        common.print_to_file(readings + str(result), last_file)
