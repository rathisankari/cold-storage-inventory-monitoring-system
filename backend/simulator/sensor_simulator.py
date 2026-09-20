import time
import requests
import sys
import os

API_URL = "http://127.0.0.1:8001/temperature-logs/"
LOGIN_URL = "http://127.0.0.1:8001/auth/login"

EMAIL = os.getenv("COLDGUARD_EMAIL")
PASSWORD = os.getenv("COLDGUARD_PASSWORD")

STORAGE_UNIT_ID = 3
HUMIDITY = 60
INTERVAL = 10

scenarios = {
    "normal": 5.5,
    "high": 10.5,
    "low": 1.5
}

scenario = sys.argv[1] if len(sys.argv) > 1 else "normal"

if scenario not in scenarios:
    print("Invalid scenario. Use: normal, high, or low")
    sys.exit(1)

if not EMAIL or not PASSWORD:
    print("COLDGUARD_EMAIL and COLDGUARD_PASSWORD environment variables are required")
    sys.exit(1)

temperature = scenarios[scenario]

login_response = requests.post(
    LOGIN_URL,
    json={
        "email": EMAIL,
        "password": PASSWORD
    }
)

login_response.raise_for_status()

token = login_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

while True:
    data = {
        "storage_unit_id": STORAGE_UNIT_ID,
        "temperature": temperature,
        "humidity": HUMIDITY,
        "source": "IoT_Sensor"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=data
    )

    print(
        f"Temperature: {temperature}°C | "
        f"Status: {response.status_code}"
    )

    if response.status_code != 200:
        print(response.text)

    time.sleep(INTERVAL)