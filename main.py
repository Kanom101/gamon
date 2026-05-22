import requests
import sqlite3
import time
from requests.auth import HTTPBasicAuth

URL = "http://141.212.161.136:8080/gamon"
API_BASE = "/report/"

USER = "admin"
PASSWORD = "admin"

auth = HTTPBasicAuth(USER, PASSWORD)
connection = sqlite3.connect('gamon.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamon_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        creationDateTme TEXT,
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
    "type",
    "creationDateTme",
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
try:
    response = requests.get(URL + API_BASE + str(current), auth=auth)
    data = response.json()
    values = [data.get(column) for column in COLUMNS]
    cursor.execute("INSERT INTO gamon_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    connection.commit()
    print(data)
    current += 1
    if response.status_code == 200:
        print("OK")
    else:
        print("Error")
    time.sleep(10)
except Exception as e:
    print("Error:", e)