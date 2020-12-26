# TODO: update this to new sensor class style

import serial
import time

from hardware import Sensor

DEVICE = '/dev/ttyUSB0' # let's hope it stays there
BAUD_RATE = 9600
TIMEOUT = 5 # in secs
CMD = b'r'

def get():
    result = 0
    while not result:
        try:
            with serial.Serial(DEVICE, BAUD_RATE, timeout = TIMEOUT) as ser:
                # The Arduino resets each time the port is opened, so we need to
                # wait a bit for it to boot before sending anything.
                time.sleep(2)

                ser.write(CMD)
                result = ser.readline()
                result = result.decode('utf-8').strip()
                result = int(result)
        except Exception as e:
            pass


    # The MQ7's min viable reading range is 20 ppm, so values below that are
    # suspect.
    if result < 20:
        result = 20

    return {
        Sensor.mq7_carb_mono: result
    }
