from common import Sensor

# generic "is number" check
def try_parse_float(input_num):
    try:
        float(input_num)
        return True
    except ValueError:
        return False

def __temperature__(value):
    # The DS18B20 sensor supports a temperature reading range of [-55, 125] °C.
    # BME280's temperature sensor has a narrower range, so we're fine.
    if -55 <= value <= 125:
        return True

    return False

def __pressure__(value):
    # The BME280 sensor (which I'm using for pressure) supports a pressure
    # measurement range of [300, 1100] hPa.
    if 300 <= value <= 1100:
        return True

    return False

def __humidity__(value):
    # Percentage of the humidity in the air. As such, it can only be between
    # 0 and 100%.
    if 0 <= value <= 100:
        return True

    return False

def __pm__(value):
    # The SDS011 supports a PM (Particulate Matter) reading range of
    # [0.0, 999.9] μg/m3.
    if 0 <= value <= 1000:
        return True

    return False

def is_sane(sensor, value):
    if not isinstance(sensor, Sensor):
        raise TypeError('sensor isn\'t a common.Sensor')

    if not try_parse_float(value):
        return False

    reading = float(value)

    mapper = {
        Sensor.ds18_long_temp: __temperature__,
        Sensor.ds18_short_temp: __temperature__,
        Sensor.bme_temp: __temperature__,
        Sensor.bme_pressure: __pressure__,
        Sensor.bme_humidity: __humidity__,
        Sensor.sds_pm25: __pm__,
        Sensor.sds_pm10: __pm__,
    }

    return mapper[sensor](reading)
