import decouple
import pip
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()

configure()

LAT = os.getenv("LAT")
LONG = os.getenv("LONG")
forecast_day_1 = "3"
precipitation = "precipitation_probability" + "," + "weather_code"
timezone = "auto"

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
client = Client(account_sid, auth_token)

parameters = {
    "latitude": LAT,
    "longitude": LONG,
    "hourly": precipitation,
    "forecast_days": forecast_day_1,
    "time_zone": timezone
}
response = requests.get("https://api.open-meteo.com/v1/forecast", params=parameters)
response.raise_for_status()

data = response.json()


hour = data["hourly"]["time"][:20]
weather_code = data["hourly"]["weather_code"][:20]

will_rain = False
for i in range(len(weather_code)):
    code = weather_code[i]
    time = hour[i]
    if code > 59:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Bring an umbrella!",
        from_=os.getenv("twilio_num"),
        to=os.getenv("my_number")
    )
    print(message.status)

