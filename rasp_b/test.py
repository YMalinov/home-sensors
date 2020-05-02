#!/usr/bin/python3

# from enum import Enum, unique

# @unique
# class Sensor(Enum):
#     # Short/long are the differentiating terms between both ds18 sensors, due to
#     # the difference in the length of their cables (they're enclosed in
#     # waterproof probes). The order is important here - should correspond to
#     # order of elements in sheet as well.
#     ds18_long_temp = 1
#     ds18_short_temp = 2
#     bme_temp = 3
#     bme_pressure = 4
#     bme_humidity = 5
#     sds_pm25 = 6 # PM2.5
#     sds_pm10 = 7 # PM10

# @unique
# class Client(Enum):
#     ModelA = 1
#     ModelB = 2

# sensors_by_client = {
#     Client.ModelA: [
#         Sensor.ds18_short_temp,
#         Sensor.bme_temp,
#         Sensor.bme_pressure,
#         Sensor.bme_humidity,
#         Sensor.sds_pm25,
#         Sensor.sds_pm10,
#     ],
#     Client.ModelB: [
#         Sensor.ds18_long_temp,
#     ],
# }

# print(sensors_by_client)

dict1 = {
    "key1": "key1a",
    "key2": "key2a"
}

dict2 = {
    "key3": "key3a",
    "key4": "key4a"
}

dicts = [ dict1, dict2 ]

dict3 = { **dictionary for dictionary in dicts }

print(dict3)