# weather.py

import requests
from datetime import datetime

def get_weather_info(location: str, date: str = None) -> str:
    api_key = "a7c421db06954d99a4c132931251605"
    if date:
        try:
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.today().date()
            if query_date < today:
                endpoint = "history.json"
            elif query_date == today:
                endpoint = "current.json"
            else:
                endpoint = "forecast.json"
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."
    else:
        endpoint = "current.json"

    url = f"http://api.weatherapi.com/v1/{endpoint}?key={api_key}&q={location}"

    if endpoint == "forecast.json":
        url += "&days=1"

    try:
        response = requests.get(url)
        data = response.json()

        if endpoint == "current.json":
            condition = data['current']['condition']['text']
            temp_c = data['current']['temp_c']
            return f"The current weather in {location} is {condition} with a temperature of {temp_c}°C."
        elif endpoint == "history.json":
            condition = data['forecast']['forecastday'][0]['day']['condition']['text']
            temp_c = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            return f"The weather in {location} on {date} was {condition} with an average temperature of {temp_c}°C."
        elif endpoint == "forecast.json":
            condition = data['forecast']['forecastday'][0]['day']['condition']['text']
            temp_c = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            return f"The forecasted weather in {location} on {date} is {condition} with an average temperature of {temp_c}°C."
        else:
            return "Unable to determine the weather information."
    except Exception as e:
        return f"Unable to fetch weather data: {e}"
