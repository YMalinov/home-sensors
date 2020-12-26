import os, glob, time

from common import round_num_dict

class Ds18Short:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        short_id = '28-000006747eff'
        base_dir = '/sys/bus/w1/devices/'

        self.file = glob.glob(base_dir + short_id)[0] + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
