class Sensor:
    items = []

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

        self.items.append(self)

    def get_map():
        return { s.name:s.unit for s in Sensor.items }

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash((self.name, self.unit))

    def __eq__(self, other):
        return (self.name, self.unit) == (other.name, other.unit)

class Client:
    items = []

    def __init__(self, name, sensors, sheet):
        self.name = name
        self.sensors = sensors
        self.sheet = sheet

        self.items.append(self)

    def from_str(input):
        for item in Client.items:
            if input == item.name:
                return item

    def get_sheet_range(self):
        end_col = chr(ord('B') + len(self.sensors))
        return f'data!A2:{end_col}'

    def __str__(self):
        sensors_str = ','.join([s.name for s in self.sensors])
        return f'{self.name}: {sensors_str}'

    def __hash__(self):
        return hash((self.name, self.sheet['id']))

    def __eq__(self, other):
        return (self.name, self.sheet['id']) ==\
            (other.name, other.sheet['id'])

# Short/long are the differentiating terms between both ds18 sensors, due to
# the difference in the length of their cables (they're enclosed in waterproof
# probes).
Sensor.ds18_long_temp = Sensor(name='ds18_long_temp', unit='°C')
Sensor.ds18_short_temp = Sensor(name='ds18_short_temp', unit='°C')
Sensor.bme_temp = Sensor(name='bme_temp', unit='°C')
Sensor.bme_pressure = Sensor(name='bme_pressure', unit='hPa')
Sensor.bme_humidity = Sensor(name='bme_humidity', unit='%')
# Sensor.sds_pm25 = Sensor(name=''sds_pm25', unit='µg/m³') # PM2,5
# Sensor.sds_pm10 = Sensor(name=''sds_pm10', unit='µg/m³') # PM10
Sensor.mq7_carb_mono = Sensor(name='mq7_carb_mono', unit='ppm')

# The order of sensors is important here - should correspond to order of
# elements in sheets as well.
Client.rasp_a = Client(
    name='rasp_a',
    sensors=[
        Sensor.ds18_short_temp,
        Sensor.bme_temp,
        Sensor.bme_pressure,
        Sensor.bme_humidity,
        # Sensor.sds_pm25,
        # Sensor.sds_pm10,
    ],
    sheet={
        'id': '18SQJSHL2Lg8kgPxiiHce8Yrquyf8Y9i5USvYQyvWWZs',
    }
)
Client.rasp_b = Client(
    name='rasp_b',
    sensors=[
        Sensor.mq7_carb_mono,
    ],
    sheet={
        'id': '1KDgfft4t-7S7tr57HdGmZvhuKxGu7UW9lySjIud-bA8',
    }
)
Client.rasp_c = Client(
    name='rasp_c',
    sensors=[
        Sensor.ds18_long_temp,
    ],
    sheet={
        'id': '1Ok_khmMncDeS4YGq05haVBrh-yI1mKfbSnPejxRALKw',
    }
)
