import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.getenv("api_key")
LATITUDE = float(os.getenv("lat"))
LONGITUDE = float(os.getenv("lon"))

account_sid = os.getenv("acc_sid")
auth_token = os.getenv("token")
PHONE_NUMBER = os.getenv("phone_number")

weather_params = {
    "appid": API_KEY,
    "exclude": "current,minutely,daily",
    "lat": LATITUDE,
    "lon": LONGITUDE
}

response = requests.get(url=OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

forecast_12_hours = weather_data["hourly"][:12]

will_rain = False

for hour in forecast_12_hours:
    condition_code = hour["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It is going to rain today. Don't forget to bring an ☂️.",
        from_="+12018905717",
        to=PHONE_NUMBER
    )
    print(message.status)
