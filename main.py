import os
from fastapi import FastAPI, Request
import socket

from dotenv import load_dotenv
import uvicorn

load_dotenv()


def get_token():
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    if not ACCESS_TOKEN:
        raise ValueError("ACCESS_TOKEN is not set")

    return ACCESS_TOKEN


app = FastAPI()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# handler = ipinfo.getHandler(get_token())
# data = handler.getDetails(ip_address)


# def get_location():
#     return data.city


@app.get("/api/hello")
def get_index(visitor_name: str, request: Request):
    visitor_name = visitor_name
    location = "Lagos"

    if request.client is None:
        return {"error": "Client information is not available"}

    client_host = request.client.host
    print(client_host)
    if client_host == "::1" or client_host == "127.0.0.1":
        client_host = "8.8.4.4"

    return {
        "client_ip": client_host,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is 11 degrees Celcius in {location}",
    }


#  if (clientIp === '::1' || clientIp === '127.0.0.1') {
#         clientIp = '8.8.4.4'; // Use a default IP address for testing, such as Google's public DNS server
#     }


# const express = require('express');
# const axios = require('axios');
# const app= express();
# const IP_GEOLOCATION_API_KEY = '3c157014abe54a2fa062bf9ded9f4c5c';
# const WEATHERAPI_KEY = '1f659253b7024c0885602159240107';
# app.set('trust proxy', true);
# app.get('/api/hello', async (req, res) => {
#     const visitorName = req.query.visitor_name;
#     let clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
#     // Handle local IP addresses
#     if (clientIp === '::1' || clientIp === '127.0.0.1') {
#         clientIp = '8.8.4.4'; // Use a default IP address for testing, such as Google's public DNS server
#     }
#     try {
#         // Get location data from IP Geolocation API
#         const geoResponse = await axios.get(`https://api.ipgeolocation.io/ipgeo?apiKey=${IP_GEOLOCATION_API_KEY}&ip=${clientIp}`);
#         const location = geoResponse.data.city || 'Unknown Location';
#         // Get weather data from WeatherAPI
#         const weatherResponse = await axios.get(`https://api.weatherapi.com/v1/current.json?key=${WEATHERAPI_KEY}&q=${location}`);
#         const temperature = weatherResponse.data.current.temp_c;
#         // Construct the response
#         const response = {
#             client_ip: clientIp,
#             location: location,
#             greeting: `Hello, ${visitorName}!, the temperature is ${temperature} degrees Celsius in ${location}`
#         };
#         res.json(response);
#     } catch (error) {
#         console.error('Error fetching data:', error);
#         res.status(500).json({ error: 'Internal Server Error' });
#     }
# });
# const PORT = process.env.PORT || 3000;
# app.listen(PORT, () => {
#     console.log(`Server is running on port ${PORT}`);
# });

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
