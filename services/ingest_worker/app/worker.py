import time
import requests
import os

# Env config
BHUWAN_API_ENDPOINT = os.getenv("BHUVAN_API_ENDPOINT", "https://bhuvan.nrsc.gov.in/api/some_endpoint")
BHUWAN_API_KEY = os.getenv("BHUVAN_API_KEY", "")

FARMONAUT_API_ENDPOINT = os.getenv("FARMONAUT_API_ENDPOINT", "https://api.farmonaut.com/ai/agri/health")
FARMONAUT_API_KEY = os.getenv("FARMONAUT_API_KEY", "")

# Example lat/lon or get from config/external source for ingestion
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", "20.5937"))  # India center latitude
DEFAULT_LON = float(os.getenv("DEFAULT_LON", "78.9629"))  # India center longitude

def fetch_weather_stub():
    print("Fetching weather... (stub)")
    # TODO: Replace with real weather API

def fetch_bhuvan_satellite(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    print(f"Fetching Bhuvan satellite/agri data for lat={lat}, lon={lon}")
    params = {"lat": lat, "lon": lon, "apikey": BHUWAN_API_KEY}
    try:
        response = requests.get(BHUWAN_API_ENDPOINT, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Bhuvan data fetched: {data}")
            return data
        else:
            print(f"Bhuvan API error status: {response.status_code}")
    except Exception as e:
        print(f"Bhuvan API call failed: {e}")
    return None

def fetch_farmonaut_data(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    print(f"Fetching Farmonaut crop health data for lat={lat}, lon={lon}")
    headers = {"Authorization": f"Bearer {FARMONAUT_API_KEY}"}
    params = {"lat": lat, "lng": lon}
    try:
        response = requests.get(FARMONAUT_API_ENDPOINT, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Farmonaut data fetched: {data}")
            return data
        else:
            print(f"Farmonaut API error status: {response.status_code}")
    except Exception as e:
        print(f"Farmonaut API call failed: {e}")
    return None

def fetch_market_stub():
    print("Fetching market prices... (stub)")
    # TODO: Replace with real market prices API

if __name__ == "__main__":
    fetch_weather_stub()
    fetch_bhuvan_satellite()
    fetch_farmonaut_data()
    fetch_market_stub()
    print("Ingest worker finished.")
