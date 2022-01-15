import os

import requests


class Weather:

    def get_city_weather(self, city: str) -> str:
        try:
            open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")
            data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=fr&units=metric&APPID={open_weather_api_key}"
            ).json()
            temperature_in_degree = data.get('main')['temp']
            weather_description = data.get('weather')[0].get('description')
            return f"A {city}, il fait {temperature_in_degree}°C avec un temps {weather_description}"
        except:
            return "Désolé, mais je ne connais pas cette ville sur la planète Terre 🤖"
