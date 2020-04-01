import sys, time
from common import Sensor, get_abs_path

sys.path.insert(1, get_abs_path('rasp_b/libs'))
# I'd like to thank Frank Heuer and Teus Hagen for creating and updating this
# library - it's been a huge help in making the SDS011 work correctly on short
# notice. The webpage for their project is as follows:
#    https://gitlab.com/frankrich/sds011_particle_sensor
from sds011 import SDS011


DEVICE_FILE = '/dev/ttyUSB0' # let's hope it stays there
BAUD_RATE = 9600

# Sensor is sometimes slow, hence the generous read timeout:
READ_TIMEOUT = 20 # in secs

# As in, how long are we gonna wait before collecting the sensors' readings:
WARMUP_PERIOD = 120 # in secs

def get():
    print('Initiating connection with SDS011...')
    sensor = SDS011(
        DEVICE_FILE,
        timeout=READ_TIMEOUT,
        unit_of_measure=SDS011.UnitsOfMeasure.MassConcentrationEuropean
    )

    print('Resetting...')
    sensor.reset()

    # Let's wake the sensor up...
    print('Waking up...')
    sensor.workstate = SDS011.WorkStates.Measuring

    # ...and leave it some time to get qualified readings.
    print('Going to sleep for %d secs...' % WARMUP_PERIOD)
    time.sleep(WARMUP_PERIOD)

    # Should be enough. Get the values and...
    print('Done sleeping, next: read SDS011 measurements...')
    values = sensor.get_values()

    # ... put it to sleep until next time we need its values. It has a
    # mechanical fan - better not keep it spinning needlessly.
    print('Done! Putting sensor back to sleep...')
    sensor.workstate = SDS011.WorkStates.Sleeping

    return {
        Sensor.sds_pm25: values[1],
        Sensor.sds_pm10: values[0]
    }
