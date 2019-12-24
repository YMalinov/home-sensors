from apiclient import discovery
from google.oauth2 import service_account
from datetime import datetime, timedelta
from itertools import zip_longest
from enum import Enum, unique
import os
import pytz

import common
from common import avg, Sensor, Client, sensors

from aqi import aqi

DEFAULT_CLIENT = Client.rasp_b
SHEETS = {
    Client.rasp_a: {
        'id': '1Ok_khmMncDeS4YGq05haVBrh-yI1mKfbSnPejxRALKw',
        'range': 'data!A2:C',
    },
    Client.rasp_b: {
        'id': '18SQJSHL2Lg8kgPxiiHce8Yrquyf8Y9i5USvYQyvWWZs',
        'range': 'data!A2:H',
    },
}
CREDS_FILE = common.get_abs_path('credentials.json')
SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
]
TIMEZONE = 'Europe/Sofia'
TS_FMT = "%Y%m%d_%H%M%S"
TS_FMT_PRETTY = "%Y-%m-%d %H:%M:%S" # parsable by Sheets

@unique
class Mode(Enum):
    avg = 1
    min = 2
    max = 3

def sheets():
    credentials = service_account.Credentials \
            .from_service_account_file(CREDS_FILE, scopes=SCOPES)

    # Let's try a couple of times, just to be sure
    for i in range(3):
        try:
            return discovery.build(
                'sheets', 'v4', credentials=credentials).spreadsheets()
        except:
            print('Problems building spreadsheet service, attempt: %d' % i + 1)

def put(LOCAL_ENV, client, readouts):
    localized = datetime.now()
    if not LOCAL_ENV:
        timezone = pytz.timezone(TIMEZONE)
        utc = pytz.utc
        localized = utc.localize(localized).astimezone(timezone)

    timestamp = localized.strftime(TS_FMT)
    timestamp_pretty = localized.strftime(TS_FMT_PRETTY)

    data = {
        'values': [ [timestamp, timestamp_pretty] + readouts ]
    }

    if LOCAL_ENV: data['values'][0].append("test")

    sheets().values().append(
            spreadsheetId=SHEETS[client]['id'],
            body=data,
            range=SHEETS[client]['range'],
            valueInputOption='USER_ENTERED').execute()

def add_aqi(entry):
    pm25 = Sensor.sds_pm25
    if pm25.name in entry:
        pm25_aqi, pm25_label = aqi(entry[pm25.name], pm25).get()
        entry['pm25_aqi'] = pm25_aqi
        entry['pm25_aqi_label'] = pm25_label.name

    pm10 = Sensor.sds_pm10
    if pm10.name in entry:
        pm10_aqi, pm10_label = aqi(entry[pm10.name], pm10).get()
        entry['pm10_aqi'] = pm10_aqi
        entry['pm10_aqi_label'] = pm10_label.name

    return entry

def filter_per_delta(matrix, delta):
    # We're going to count our timedelta from the last entry in the matrix
    # array onwards.
    last = datetime.strptime(matrix[0][0], TS_FMT)
    start_date = last - delta;

    for i, row in enumerate(matrix):
        if datetime.strptime(row[0], TS_FMT) < start_date:
            return matrix[:i - 1], start_date
    else:
        # OK, so the period specified goes outside of the bonds of the matrix.
        # No biggie, just return the entire matrix and say the start date is the
        # earliest time specified there.
        return matrix, datetime.strptime(matrix[-1][0], TS_FMT)

def squash_by_mode(input, mode):
    operations = {
        Mode.avg: avg,
        Mode.min: min,
        Mode.max: max
    }

    return [operations[mode](col) for col in input]

def get_last_record(entries):
    last_entry = entries[-1]

    # Parse out numbers, so it's easier to calculate AQI on them later.
    last_entry[2:] = [float(x) for x in last_entry[2:]]

    keys = ['timestamp', 'timestamp_pretty'] + \
        [id.name for id in sensors[Client.rasp_b]]

    output = dict(zip(keys, last_entry))

    return output

def get_last_period(entries, delta, mode=Mode.avg):
    # Let's prep the array for processing by sorting it in reverse chronological
    # order.
    entries = sorted(
        entries,
        key = lambda x: x[0], reverse=True
    )

    # Filter out needless data per the timedelta needed.
    entries, start_date = filter_per_delta(entries, delta)

    # Swap columns for rows, so that we get all values for averaging in
    # separate arrays.
    entries = list([x for x in y] for y in zip_longest(*entries))

    # Remove redundant timestamps.
    entries = entries[2:]

    # Parse all numbers.
    entries = [[float(y) for y in x] for x in entries]

    # Squash data as per required mode.
    squashed = squash_by_mode(entries, mode)

    # Prep the readouts + their labels.
    readouts = dict(zip(\
        [sensor.name for sensor in sensors[Client.rasp_b]], \
        squashed))

    # Add mode of operation, start date & readouts.
    squashed_dict = { 'mode': mode.name }
    squashed_dict.update({ 'period_start': start_date.strftime(TS_FMT) })
    squashed_dict.update(**readouts)

    # And finally return processed dict.
    return squashed_dict

def get(LOCAL_ENV, delta, mode, client):
    entries = sheets().values().get(
            spreadsheetId=SHEETS[client]['id'],
            range=SHEETS[client]['range']).execute()['values']

    if delta == timedelta(): # as in, no user inputted data
        return add_aqi(get_last_record(entries))

    return add_aqi(get_last_period(entries, delta, mode))
