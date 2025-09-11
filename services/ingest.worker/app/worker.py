import time
import requests
import os

def fetch_weather_stub():
    # In real world call Open-Meteo or local provider
    print("Fetching weather... (stub)")

def fetch_satellite_stub():
    print("Fetching satellite tiles... (stub)")

def fetch_market_stub():
    print("Fetching market prices... (stub)")

if __name__ == "__main__":
    # run once and exit (docker-compose service)
    fetch_weather_stub()
    fetch_satellite_stub()
    fetch_market_stub()
    print("Ingest worker finished.")
