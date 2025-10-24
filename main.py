from flask import Flask, render_template, request
import datetime as dt 
import requests
from dotenv import load_dotenv
import os

app = Flask (__name__)

load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")

# Now you can use the api_key in your API calls
# Example:
# import requests
# url = "https://api.example.com/data"
# headers = {"Authorization": f"Bearer {api_key}"}
# response = requests.get(url, headers=headers)
# print(response.json())

def kelvin_to_celcius_fahrenheit(kelvin):
    celcius = kelvin - 273.15 # converts kelvin to celcius 
    fahrenheit = celcius * (9/5) + 32 # converts celcius to Fahrenheit 
    return round(fahrenheit)

def return_search_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url) # requests.get(url) sends HTTP GET requests to API then .json() converts that JSON into a python dictionary 
    
    if response.status_code != 200:
        return f"Error fetching weather for {city}"
    json = response.json()

    # response is now a big nested dictionary you can access the the below 
    # keys are "main", "wind", "weather", "sys"
    temp_kelvin = json['main']['temp'] 
    temp_fahrenheit = kelvin_to_celcius_fahrenheit(temp_kelvin)
    feels_like_kelvin = json['main']['feels_like']
    feels_like_fahrenheit = kelvin_to_celcius_fahrenheit(feels_like_kelvin)
    wind_speed = json['wind']['speed']
    humidity = json['main']['humidity']
    description = json['weather'][0]['description'] # 0 means you are accessing the first item in the weather list
    sunrise_time = dt.datetime.utcfromtimestamp(json['sys']['sunrise'] + json['timezone'])
    sunrise_set = dt.datetime.utcfromtimestamp(json['sys']['sunset'] + json['timezone'])

    return render_template('weather.html', city_name = city, temp_fahrenheit = temp_fahrenheit, feels_like_kelvin = feels_like_kelvin, feels_like_fahrenheit = feels_like_fahrenheit, wind_speed = wind_speed, humidity = humidity, description = description, sunrise_time = sunrise_time , sunrise_set = sunrise_set);

@app.route('/weather')
def weather ():
    
    url = 'http://ipinfo.io/json'
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error fetching weather for {city}"
    json = response.json()

    city = json["city"]

    return return_search_weather(city);

@app.route('/weather/<city>')
def meow_weather(city):

    return return_search_weather(city);

@app.route('/')
def get_ip():
    # Get the client's IP address
    ip_address = request.remote_addr
    return f"Your IP address is: {ip_address}"

if __name__ == '__main__':
    app.run(debug=True)

