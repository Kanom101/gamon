import requests
import sqlite3
import time
import atexit
from requests.auth import HTTPBasicAuth

URL = "http://141.212.161.136:8080/gamon"
API_BASE = "/report/"

USER = "admin"
PASSWORD = "admin"

auth = HTTPBasicAuth(USER, PASSWORD)
connection = sqlite3.connect('gamon.db')
cursor = connection.cursor()

atexit.register(connection.close)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamon_data (
        id INTEGER PRIMARY KEY,
        type TEXT,
        creationDateTime TEXT,
        startDateTime TEXT,
        endDateTime TEXT,
        status TEXT,
        softwareVersion TEXT,
        deviceModel TEXT,
        deviceSerialNumber TEXT,
        manufacturer TEXT,
        minimumDoseRate REAL,
        minimumDoseRateDateTime TEXT,
        maximumDoseRate REAL,
        maximumDoseRateDateTime TEXT,
        averageDoseRate REAL,
        warningThreshold REAL,
        alarmThreshold REAL,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        raining BOOL
    )
""")
connection.commit()

COLUMNS = [
    "id",
    "type",
    "creationDateTime",
    "startDateTime",
    "endDateTime",
    "status",
    "softwareVersion",
    "deviceModel",
    "deviceSerialNumber",
    "manufacturer",
    "minimumDoseRate",
    "minimumDoseRateDateTime",
    "maximumDoseRate",
    "maximumDoseRateDateTime",
    "averageDoseRate",
    "warningThreshold",
    "alarmThreshold",
    "latitude",
    "longitude",
    "altitude",
    "raining"
]

current = 301813

while True:
    try:
        response = requests.get(URL + API_BASE + str(current), auth=auth)

        if response.status_code == 200:
            data = response.json()
            values = [data.get(column) for column in COLUMNS]
            cursor.execute(
                f"INSERT INTO gamon_data ({', '.join(COLUMNS)}) VALUES ({', '.join(['?'] * len(COLUMNS))})",
                values
            )
            connection.commit()
            print(f"[OK] Inserted record {current}: {data}")
            current += 1
        else:
            print(f"[Error] Status {response.status_code} for record {current}")

    except requests.exceptions.ConnectionError:
        print(f"[Error] Could not connect to server. Retrying in 10s...")
    except requests.exceptions.Timeout:
        print(f"[Error] Request timed out for record {current}. Retrying in 10s...")
    except Exception as e:
        print(f"[Error] Unexpected error: {e}")

    time.sleep(3)