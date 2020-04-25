import serial
import time
from common import Sensor

DEVICE_FILE = '/dev/ttyUSB0' # let's hope it stays there
BAUD_RATE = 9600
TIMEOUT = 5 # in secs
CMD = b'r'

def get():
    result = ''
    with serial.Serial(DEVICE_FILE, BAUD_RATE, timeout = TIMEOUT) as ser:
        while not result:
            # the Arduino, for some reason, resets each time the port is opened
            # anew, so we need to wait a bit for it to load before sending
            # anything
            time.sleep(2)

            ser.write(CMD)
            result = ser.readline()

    result = result.decode('utf-8').strip()

    return {
        Sensor.mq7_carb_mono: result
    }
