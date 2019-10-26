#!/usr/bin/python3

import sys, time
from common import Sensor, get_abs_path

sys.path.insert(1, get_abs_path('libs'))
# I'd like to thank Frank Heuer and Teus Hagen for creating and updating this library - it's been
# very helpful in making the SDS011 work correctly on short notice. The webpage for their project is
# as follows:
#    https://gitlab.com/frankrich/sds011_particle_sensor
from sds011 import SDS011


DEVICE_FILE = '/dev/ttyUSB0' # let's hope it stays there
BAUD_RATE = 9600
READ_TIMEOUT = 4 # in secs; as in, how much time we are gonna wait to collect a full response
WARMUP_PERIOD = 120 # in secs

def get():
    sensor = SDS011(
        DEVICE_FILE,
        timeout=READ_TIMEOUT,
        unit_of_measure=SDS011.UnitsOfMeasure.MassConcentrationEuropean
    )

    sensor.reset()

    # Let's wake the sensor up...
    sensor.workstate = SDS011.WorkStates.Measuring

    # ...and leave it some time to get qualified readings.
    time.sleep(WARMUP_PERIOD)

    # Should be enough. Get the values and...
    values = sensor.get_values()

    # ... put it to sleep until next time we need its values. It has a mechanical fan - better not
    # keep it spinning needlessly.
    sensor.workstate = SDS011.WorkStates.Sleeping

    return {
        Sensor.sds_pm25.name: values[1],
        Sensor.sds_pm10.name: values[0]
    }
