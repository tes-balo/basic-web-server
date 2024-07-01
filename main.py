import os
from typing import Any
from fastapi import FastAPI

import socket

from dotenv import load_dotenv
import httpx
# import uvicorn

load_dotenv()


def get_token():
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    if not WEATHER_API_KEY:
        raise ValueError("WEATHER_API_KEY is not set")

    return WEATHER_API_KEY


def get_client_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
    return ip_address


WEATHER_API_KEY = get_token()
CLIENT_IP = get_client_ip()

app = FastAPI()

# def get_geolocation_response():
#     res = httpx.get(
#         f"https://api.ipgeolocation.io/ipgeo?apiKey={GEOLOCATION_API_KEY}"
#     )

#     print(res.json())

#     # Check if the request was successful
#     geolocation_data = res.json()

#     return geolocation_data


def get_weather_response():
    res = httpx.get(
        f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CLIENT_IP}"
    )

    print(res.json())

    # Check if the request was successful
    weather_data = res.json()

    return weather_data


weather_response: dict[str, dict[str, Any]] = get_weather_response()

location_name: str = weather_response["location"]["name"]
location_tempt: float = weather_response["current"]["temp_c"]


@app.get("/api/hello")
def get_index(visitor_name: str):
    print(location_tempt, location_name)
    # if CLIENT_IP is None:
    #     return {"error": "Client information is not available"

    return {
        "client_ip": CLIENT_IP,
        "location": location_name,
        "greeting": f"Hello, {visitor_name}!, the temperature is {location_tempt} degrees Celcius in {location_name}",
    }


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
