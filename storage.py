#!/usr/bin/python3

from apiclient import discovery
from google.oauth2 import service_account
from datetime import datetime
import os, pytz

import common

SPREADSHEET_ID = '18SQJSHL2Lg8kgPxiiHce8Yrquyf8Y9i5USvYQyvWWZs'
RANGE_NAME = 'data!A2:G'
CREDS_FILE = common.get_abs_path('credentials.json')
SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
]
TIMEZONE = 'Europe/Sofia'
TIMESTAMP_FMT = "%Y%m%d_%H%M%S"
TIMESTAMP_FMT_PRETTY = "%Y-%m-%d %H:%M:%S" # parsable by Sheets

def get_sheets():
    credentials = service_account.Credentials \
            .from_service_account_file(CREDS_FILE, scopes=SCOPES)

    return discovery.build(
            'sheets', 'v4', credentials=credentials).spreadsheets()

def put(LOCAL_ENV, readouts):
    localized = datetime.now()
    if not LOCAL_ENV:
        timezone = pytz.timezone(TIMEZONE)
        utc = pytz.utc
        localized = utc.localize(localized).astimezone(timezone)

    timestamp = localized.strftime(TIMESTAMP_FMT)
    timestamp_pretty = localized.strftime(TIMESTAMP_FMT_PRETTY)

    data = {
        'values': [ [timestamp, timestamp_pretty] + readouts ]
    }

    if LOCAL_ENV: data['values'][0].append("test")

    get_sheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            body=data,
            range=RANGE_NAME,
            valueInputOption='USER_ENTERED').execute()

def get(LOCAL_ENV):
    # Does this actually get *ALL* lines of the 'data' sheet and return them as
    # an array?! That's horribly inefficient, if we'll only be dealing with the
    # last line there.
    entries = get_sheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME).execute()['values']

    last_entry = entries[-1] # latest reading

    keys = ['timestamp', 'timestamp_pretty'] + common.get_sensors()
    output = dict(zip(keys, last_entry))

    return output

# TODO: have /get/avg, /get/max, /get/min, etc
