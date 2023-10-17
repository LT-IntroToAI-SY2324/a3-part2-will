import datetime as dt
import http.client
import json

API_KEY = open('api_key', 'r').read().strip() # past API key here
BASE_URL = '/data/2.5/weather'

def get_weather_data(city):
    conn = http.client.HTTPSConnection("api.openweathermap.org")
    url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return json.loads(data)

def get_temperature(city):
    weather_data = get_weather_data(city)
    if weather_data.get('cod') == 200:
        temperature_kelvin = weather_data['main']['temp']
        temperature_fahrenheit = (temperature_kelvin - 273.15) * 9/5 + 32
        return int(temperature_fahrenheit)
    return None

def get_weather_description(city):
    weather_data = get_weather_data(city)
    if weather_data.get('cod') == 200:
        return weather_data['weather'][0]['description']
    return None

def get_forecast(city, day_delta):
    current_date = dt.datetime.now()
    target_date = current_date + dt.timedelta(days=day_delta)
    return target_date.strftime('%Y-%m-%d')

def get_weather(city, day_delta=0):
    if day_delta > 0:
        date = get_forecast(city, day_delta)
        weather_data = get_weather_data(city)
        if weather_data.get('cod') == 200:
            weather_description = weather_data['weather'][0]['description']
            temperature_kelvin = weather_data['main']['temp']
            temperature_fahrenheit = (temperature_kelvin - 273.15) * 9/5 + 32
            return f"On {date}, the weather in {city} is {weather_description} with a temperature of {temperature_fahrenheit}°F."
    else:
        return get_weather_description(city)

def is_sunny(city, day_delta=0):
    weather = get_weather_description(city)
    if weather:
        return "sunny" in weather.lower()
    return None

def is_cloudy(city, day_delta=0):
    weather = get_weather_description(city)
    if weather:
        return "cloudy" in weather.lower()
    return None

def is_raining(city, day_delta=0):
    weather = get_weather_description(city)
    if weather:
        return "rain" in weather.lower()
    return None

# in what area? answer: what is the weather in {city}
def main():
    print("Welcome to the Weather Assistant!")
    city = None  # Initialize city to None

    while True:
        user_input = input("Ask a question or type 'exit' to quit: ").lower()

        if user_input == 'exit':
            print("Goodbye!")
            break
        if "what is the weather in" in user_input:
            city = user_input.split("in", 1)[-1].strip()
            response = get_weather(city)
        elif "what is the temperature" in user_input:
            if city:
                temperature = get_temperature(city)
                if temperature:
                    response = f"The temperature in {city} is {temperature}°F."
                else:
                    response = f"Sorry, I couldn't retrieve temperature data for {city}."
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "what will the weather be tomorrow" in user_input:
            if city:
                response = get_weather(city, 1)
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "what was the weather yesterday" in user_input:
            if city:
                response = get_weather(city, -1)
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "what was the temperature yesterday" in user_input:
            if city:
                temperature = get_temperature(city)
                if temperature:
                    response = f"The temperature in {city} was {temperature}°F yesterday."
                else:
                    response = f"Sorry, I couldn't retrieve temperature data for {city}."
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "what will be the temperature tomorrow" in user_input:
            if city:
                temperature = get_temperature(city)
                if temperature:
                    response = f"The temperature in {city} will be {temperature}°F tomorrow."
                else:
                    response = f"Sorry, I couldn't retrieve temperature data for {city}."
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "is it sunny today" in user_input:
            if city:
                sunny = is_sunny(city)
                if sunny is not None:
                    response = "Yes" if sunny else "No"
                else:
                    response = "I'm not sure."
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "is it cloudy today" in user_input:
            if city:
                cloudy = is_cloudy(city)
                if cloudy is not None:
                    response = "Yes" if cloudy else "No"
                else:
                    response = "I'm not sure."
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        elif "is it raining today" in user_input:
            if city:
                raining = is_raining(city)
                if raining is not None:
                    response = "Yes" if raining else "No"
                else:
                    response = "I'm not sure."
            else:
                response = "In what area?"
                area = input("Please enter the area name and ask again: ")
                city = area
        else:
            response = "I'm sorry, I can't answer that question."

        print(response)

if __name__ == "__main__":
    main()
