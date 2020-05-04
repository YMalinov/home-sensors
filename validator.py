from hardware import Sensor

# Generic "is number" check
def __try_parse_float(input_num):
    try:
        return float(input_num)
    except ValueError:
        return False

def __temperature(value):
    # The DS18B20 sensor supports a temperature reading range of [-55, 125] °C.
    # BME280's temperature sensor has a narrower range, so we're fine.
    if -55 <= value <= 125:
        return True

    return False

def __pressure(value):
    # The BME280 sensor (which I'm using for pressure) supports a pressure
    # measurement range of [300, 1100] hPa.
    if 300 <= value <= 1100:
        return True

    return False

def __humidity(value):
    # Percentage of the humidity in the air. As such, it can only be between
    # 0 and 100%.
    if 0 <= value <= 100:
        return True

    return False

def __pm(value):
    # The SDS011 supports a PM (Particulate Matter) reading range of
    # [0.0, 999.9] μg/m3.
    if 0 <= value <= 1000:
        return True

    return False

def __carb_mono(value):
    # The MQ-7 supports a ppm (parts per million) reading range of
    # [20, 2000] ppm
    if 20 <= value <= 2000:
        return True

    return False

def is_sane(sensor, value):
    if not isinstance(sensor, Sensor):
        raise TypeError('sensor isn\'t a common.Sensor')

    reading = __try_parse_float(value)
    if not reading:
        return False

    mapper = {
        Sensor.ds18_long_temp: __temperature,
        Sensor.ds18_short_temp: __temperature,
        Sensor.bme_temp: __temperature,
        Sensor.bme_pressure: __pressure,
        Sensor.bme_humidity: __humidity,
        # Sensor.sds_pm25: __pm,
        # Sensor.sds_pm10: __pm,
        Sensor.mq7_carb_mono: __carb_mono,
    }

    return mapper[sensor](reading)
