import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_endPoint = "https://api.openweathermap.org/data/2.5/onecall"

api_key = os.environ.get("OWM_API_KEY")

account_sid = "AC6734c81f980f3cb8c3df9e2e94379921"

auth_token = os.environ.get("OWM_AUTH_TOKEN")

weather_params = {
    "lat": 18.383199,
    "lon": 75.20743,
    "appid": api_key,
    "exclude": "current,minutely,daily",

}

response = requests.get(OWM_endPoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☂☔",
        from_="+12532313063",
        to='+919850009828'

    )
    print(message.status)
