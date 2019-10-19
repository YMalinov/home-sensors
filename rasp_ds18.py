#!/usr/bin/python

import os, glob, time
from common import sensor

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

outside_id = '28-000006747eff'
inside_id = '28-00000674764e'
base_dir = '/sys/bus/w1/devices/'

outside_file = glob.glob(base_dir + outside_id)[0] + '/w1_slave'
inside_file = glob.glob(base_dir + inside_id)[0] + '/w1_slave'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def get():
    return {
        sensor.ds18_in: read_temp(inside_file),
        sensor.ds18_out: read_temp(outside_file)
    }
