from apiclient import discovery
from google.oauth2 import service_account

from datetime import datetime
import os, pytz
import util

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '18SQJSHL2Lg8kgPxiiHce8Yrquyf8Y9i5USvYQyvWWZs'
RANGE_NAME = 'data!A2:D'
CREDS_FILE = util.get_abs_path('credentials.json')
SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
]
TIMEZONE = 'Europe/Sofia'

def get_sheets():
    credentials = service_account.Credentials \
            .from_service_account_file(CREDS_FILE, scopes=SCOPES)

    return discovery.build(
            'sheets', 'v4', credentials=credentials).spreadsheets()

def put(LOCAL_ENV, in_value, out_value):
    localized = datetime.now()
    if not LOCAL_ENV:
        timezone = pytz.timezone(TIMEZONE)
        utc = pytz.utc
        localized = utc.localize(localized).astimezone(timezone)

    timestamp = localized.strftime("%Y%m%d_%H%M%S")
    timestamp_pretty = localized.strftime("%d/%m/%Y %H:%M:%S")

    data = {
        'values': [ [ timestamp, timestamp_pretty, in_value, out_value ] ]
    }

    if LOCAL_ENV: data['values'][0].append("test")

    get_sheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            body=data,
            range=RANGE_NAME,
            valueInputOption='USER_ENTERED').execute()

def get(LOCAL_ENV):
    entries = get_sheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME).execute()['values']

    last_entry = entries[-1] # latest reading

    return {
        'in': last_entry[2],
        'out': last_entry[3],
        'timestamp': last_entry[0],
        'timestamp_pretty': last_entry[1]
    }

# TODO: have /get/avg, /get/max, /get/min, etc