from enum import Enum
from common import Sensor

class aqi:
    class label(Enum):
        Good = 0
        Moderate = 1
        Unhealthy_for_Sensitive_Groups = 2
        Unhealthy = 3
        Very_Unhealthy = 4
        Hazardous = 5

    class bp:
        def __init__(self, low, high):
            self.low = low
            self.high = high

        def is_in_bounds(self, value):
            if self.low <= value <= self.high:
                return True

            return False


    concentration_bps = {
        Sensor.sds_pm25: [
            bp(0.0, 12.0),
            bp(12.1, 35.4),
            bp(35.5, 55.4),
            bp(55.5, 150.4),
            bp(150.5, 250.4),
            bp(250.5, 350.4),
            bp(350.5, 500.4),
        ],
        Sensor.sds_pm10: [
            bp(0, 54),
            bp(55, 154),
            bp(155, 254),
            bp(255, 354),
            bp(355, 424),
            bp(425, 504),
            bp(505, 604),
        ]}

    index_bps = [
        bp(0, 50),
        bp(51, 100),
        bp(101, 150),
        bp(151, 200),
        bp(201, 300),
        bp(301, 400),
        bp(401, 500),
    ]

    def __init__(self, arr, sensor):
        self.arr = arr

        if not isinstance(sensor, Sensor):
            raise TypeError('sensor isn\'t a common.Sensor')

        if sensor not in self.concentration_bps.keys():
            raise TypeError('%s isn\'t currently supported' % sensor.name)

        self.sensor = sensor

    def get_breakpoint(value, bp_list):
        for i, bp in enumerate(bp_list):
            if bp.is_in_bounds(value):
                return bp, i

        # hmm, maybe the value is even higher than that (you know, if an atom bomb blows up closeby,
        # though I doubt the likeliness of the Raspberry being powered in such an event - especially
        # considering the tendency of my electrical company in failing to deliver the goods even on
        # pretty summer days)
        last = bp_list[-1]
        if value > last.high:
            return last, len(bp_list) - 1

        raise RuntimeError('%d is invalid for get_breakpoint()' % value)

    # Tips:
    #  1. 75%, or 18-24 hours of data are needed to get a proper AQI reading for the day.
    #  2. Formula is a piecewise linear function, as follows:
    #        I(high) - I(low)
    #    I = ---------------- * (C - C(low)) + I(low)
    #        C(high) - C(low)
    #  Where:
    #    I = the Air Quality index,
    #    C = the pollutant concentration,
    #    C(low) = the concentration breakpoint that is <= C,
    #    C(high) = the concentration breakpoint that is >= C,
    #    I(low) = the index breakpoint corresponding to C(low),
    #    I(high) = the index breakpoint corresponding to C(high)
    def get(self):
        avg = sum(self.arr) / len(self.arr)
        C, index = aqi.get_breakpoint(avg, aqi.concentration_bps[self.sensor])
        I = aqi.index_bps[index]
        result = ((I.high - I.low) / (C.high - C.low)) * (avg - C.low) + I.low

        return result, aqi.label(index) if index < len(list(aqi.label)) else aqi.label.Hazardous
