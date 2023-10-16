import requests
import datetime

# Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'imperial',  # Change to 'metric' for Celsius
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data

def main():
    print("Welcome to the Weather Assistant!")
    while True:
        user_input = input("Ask a question or type 'exit' to quit: ").lower()

        if user_input == 'exit':
            print("Goodbye!")
            break
        elif "weather" in user_input:
            city = input("Please enter the city name: ")
            weather_data = get_weather_data(city)

            if weather_data.get('cod') == 200:
                weather_description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                print(f"The weather in {city} is {weather_description} with a temperature of {temperature}°C.")
            else:
                print(f"Sorry, I couldn't retrieve weather data for {city}.")
        elif "location" in user_input:
            print("I am a virtual assistant and do not have a physical location.")
        elif "time" in user_input:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"The current time is {current_time}.")
        elif "day" in user_input:
            current_day = datetime.datetime.now().strftime('%A')
            print(f"Today is {current_day}.")
        else:
            print("I'm sorry, I can't answer that question.")

if __name__ == "__main__":
    main()
