import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    query = f"{city}, {state}"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        picture_url = data['photos'][0]['src']['medium'] if data['photos'] else None
        return {"picture_url": picture_url}
    return {"picture_url": None}



def get_weather_data(city, state):
    # Step 1: Geocoding API to get latitude and longitude
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state}&appid={OPEN_WEATHER_API_KEY}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code == 200 and geo_response.json():
        lat, lon = geo_response.json()[0]['lat'], geo_response.json()[0]['lon']

        # Step 2: Current weather data API
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={OPEN_WEATHER_API_KEY}"
        weather_response = requests.get(weather_url)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            return {
                "temp": weather_data['main']['temp'],
                "description": weather_data['weather'][0]['description']
            }
    return None