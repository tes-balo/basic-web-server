import os
from typing import Any
from fastapi import FastAPI

# import socket

from dotenv import load_dotenv
import httpx
# import uvicorn

load_dotenv()


keys = {
    "WEATHER_API_KEY": os.environ.get("WEATHER_API_KEY"),
    "GEOLOCATION_API_KEY": os.environ.get("GEOLOCATION_API_KEY"),
}

if not keys["WEATHER_API_KEY"]:
    raise ValueError("WEATHER_API_KEY is not set")

if not keys["GEOLOCATION_API_KEY"]:
    raise ValueError("GEO Key is not set")


# def get_client_ip():
#     hostname = socket.gethostname()
#     ip_address = socket.gethostbyname(hostname)
#     print(ip_address)
#     return ip_address


WEATHER_API_KEY = keys["WEATHER_API_KEY"]
GEOLOCATION_API_KEY = keys["GEOLOCATION_API_KEY"]

app = FastAPI()


def get_geolocation_response():
    res = httpx.get(f"https://api.ip2location.io/?key={GEOLOCATION_API_KEY}")

    print(res.json())

    # Check if the request was successful
    geolocation_data = res.json()

    return geolocation_data


geolocation_response = get_geolocation_response()
client_ip = geolocation_response["city_name"]


def get_weather_response():
    res = httpx.get(
        f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={client_ip}"
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
        "client_ip": client_ip,
        "location": location_name,
        "greeting": f"Hello, {visitor_name}!, the temperature is {location_tempt} degrees Celcius in {location_name}",
    }


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
