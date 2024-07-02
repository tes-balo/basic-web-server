import os
from typing import Any
from fastapi import FastAPI, Request
import httpx
from dotenv import load_dotenv
import uvicorn

load_dotenv()

keys = {
    "WEATHER_API_KEY": os.environ.get("WEATHER_API_KEY"),
    "GEOLOCATION_API_KEY": os.environ.get("GEOLOCATION_API_KEY"),
}

if not keys["WEATHER_API_KEY"]:
    raise ValueError("WEATHER_API_KEY is not set")

if not keys["GEOLOCATION_API_KEY"]:
    raise ValueError("GEO Key is not set")


WEATHER_API_KEY = keys["WEATHER_API_KEY"]
GEOLOCATION_API_KEY = keys["GEOLOCATION_API_KEY"]

app = FastAPI()


def get_geolocation_response(ip_addr: str):
    res = httpx.get(
        f"https://api.ip2location.io/?key={GEOLOCATION_API_KEY}&ip={ip_addr}"
    )

    print(res.json())

    # Check if the request was successful
    geolocation_data = res.json()

    return geolocation_data


# geolocation_response = get_geolocation_response()
# # client_ip = geolocation_response["ip"]
# location_name = geolocation_response["city_name"]


def get_weather_response(ip_addr: str):
    res = httpx.get(
        f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={ip_addr}"
    )

    print(res.json())

    # Check if the request was successful
    weather_data = res.json()

    return weather_data


@app.get("/")
def get_index():
    return {
        "message": "Index is active, navigate to /api/hello/visitor_name=any-name-off-your-choice to get started"
    }


@app.get("/api/hello")
def get_user_locale_info(visitor_name: str, request: Request):
    if request.client is None:
        raise ValueError("Could not get client host")
    client_host = request.client.host

    geolocation_response = get_geolocation_response(client_host)
    weather_response: dict[str, dict[str, Any]] = get_weather_response(client_host)
    location_tempt: float = weather_response["current"]["temp_c"]
    location_name = geolocation_response["city_name"]

    print(location_tempt, location_name, client_host)
    location_name = geolocation_response["city_name"]

    return {
        "client_ip": client_host,
        "location": location_name,
        "greeting": f"Hello, {visitor_name}!, the temperature is {location_tempt} degrees Celcius in {location_name}",
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
