import os
from typing import Any
from fastapi import FastAPI, Request
import httpx
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY is not set")

app = FastAPI()


def get_weather_response(ip_address: str):
    res = httpx.get(
        f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={ip_address}"
    )

    # confirm if the request was successful
    print(res.json())

    weather_data = res.json()
    return weather_data


@app.get("/")
def get_index() -> dict[str, str]:
    return {
        "message": "Index is active, navigate to /api/hello/visitor_name=any-name-off-your-choice to get started"
    }


@app.get("/api/hello")
def get_user_locale_info(visitor_name: str, request: Request) -> dict[str, str]:
    if request.client is None:
        raise ValueError("Could not get client host")
    client_host = request.client.host

    weather_response: dict[str, dict[str, Any]] = get_weather_response(client_host)
    location_name: str = weather_response["location"]["name"]
    location_tempt: float = weather_response["current"]["temp_c"]

    print(location_tempt, location_name, client_host)

    return {
        "client_ip": client_host,
        "location": location_name,
        "greeting": f"Hello, {visitor_name}!, the temperature is {location_tempt} degrees Celcius in {location_name}",
    }
