import requests, datetime, os

print("-" * 30)
print("Learning Weather requests with OpenMeteo API")
print("-" * 30)

date = datetime.datetime.now().strftime("%Y-%m-%d")
get_information = ["temperature_2m", "wind_speed_10m", "shortwave_radiation", "diffuse_radiation", "visibility", "weathercode" ]

def chk_geocode(location): 
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": location.lower(),
        "language": "id"
    }

    data = requests.get(url=BASE_URL, params=params, timeout=10).json()
    return data

def chk_forecast(latitude, longitude):
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ",".join(get_information)
    }

    data = requests.get(url=BASE_URL, params=params, timeout=10).json()
    return data

while True:
    print("Enter your location name")
    try:
        location = str(input("> "))
        geocode_data = chk_geocode(location=location)
        geocode_results = geocode_data["results"]
        latitude = geocode_results[0]["latitude"]
        longitude = geocode_results[0]["longitude"]

        print("-" * 20)
        print(f"Fetched latitude: {latitude}")
        print(f"Fetched longitude: {longitude}")
        print("-" * 20)
        forecast_data = chk_forecast(latitude=latitude, longitude=longitude)
        current_forecast = forecast_data["current"]
        temperature = current_forecast["temperature_2m"]
        wind_speed = current_forecast["wind_speed_10m"]
        shortwave_radiation = current_forecast["shortwave_radiation"]
        weathercode = current_forecast["weathercode"]
        print("Forecast Information: ")
        print(f"Temperature: {temperature}")
        print(f"Wind Speed: {wind_speed}")
        print(f"ShortWave Radiation: {shortwave_radiation}")
        print(f"Weather Code: {weathercode}")
        print("-" * 20)

        with open("weather.csv", "a") as file:
            csv_exists = os.path.isfile("weather.csv")
            if not csv_exists:
                file.write("date,location,temp,wind,radiation,weathercode")
            file.write(f"\n{date},{location},{temperature},{wind_speed},{shortwave_radiation},{weathercode}")

    except requests.Timeout:
        print("Connection Timeout")
        break
    except AttributeError:
        print("The structured changed, check the code again.")
    except KeyboardInterrupt:
        print("\nProgram stopped.")
        break
    except EOFError:
        print("\nProgram stopped.")
        break
    except OSError:
        print("Unable to write an output to weather.csv")
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
    except Exception as e:
        print("The program didn't work properly!")
        print(f"Error: {e}")
