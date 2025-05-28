import json
import csv
import gzip

def load_json(filename):
    """
    Load JSON data from a file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict: The loaded JSON data.
    """
   
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def summarize_weather_data(data):
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.
        {
    "date": "2024-08-18",
    "max_temperature": 32.5,
    "min_temperature": 22.5,
    "precipitation": 0.0,
    "wind_speed": 15.5,
    "humidity": 65,
    "weather_description": "Clear sky"
}

    Returns:
        dict: A summary of the key metrics across all days.


    """
    avg_max = 0
    avg_min = 0
    total_perc = 0
    avg_wind = 0
    avg_hum = 0
    hot_days = 0
    windy_days = 0
    rainy_days = 0
    for day in data:
        avg_max += day['max_temperature']
        if day['max_temperature'] > 30:
            hot_days += 1
        avg_min += day['min_temperature']
        total_perc += day['precipitation']
        if day['precipitation'] > 0:
            rainy_days += 1
        avg_wind += day['wind_speed']
        if day['wind_speed'] > 15:
            windy_days += 1
        avg_hum += day['humidity']

    avg_max /= len(data)
    avg_min /= len(data)
    avg_hum /= len(data)
    avg_wind /= len(data)
    summary = {}
    summary["average_max_temp"] = avg_max
    summary["average_min_temp"] = avg_min
    summary["total_precipitation"] = total_perc
    summary["average_wind_speed"] = avg_wind
    summary["average_humidity"] = avg_hum
    summary["hot_days"] = hot_days
    summary["windy_days"] = windy_days
    summary["rainy_days"] = rainy_days

    return summary


def export_to_csv(data, file):
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    if isinstance(file, str):
        with open(file, 'w', newline='') as csvfile:
            w = csv.writer(csvfile, delimiter=',',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
            w.writerow(
                "Date,Max Temperature,Min Temperature,Precipitation,Wind Speed,Humidity,Weather Description,Is Hot Day,Is Windy Day,Is Rainy Day".split(
                    ','))
            for day in data:
                line = []
                line.append(day['date'])
                line.append(day['max_temperature'])
                line.append(day['min_temperature'])
                line.append(day['precipitation'])
                line.append(day['wind_speed'])
                line.append(day['humidity'])
                line.append('True' if day['max_temperature'] > 30 else 'False')
                line.append('True' if day['wind_speed'] > 15 else 'False')
                line.append('True' if day['precipitation'] > 0 else 'False')
                w.writerow(line)
    else:
        #gzip_file = gzip.GzipFile(fileobj=file, mode='w')
        w = csv.writer(file, delimiter=',',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(
            "Date,Max Temperature,Min Temperature,Precipitation,Wind Speed,Humidity,Weather Description,Is Hot Day,Is Windy Day,Is Rainy Day".split(
                ','))
        for day in data:
            line = []
            line.append(day['date'])
            line.append(day['max_temperature'])
            line.append(day['min_temperature'])
            line.append(day['precipitation'])
            line.append(day['wind_speed'])
            line.append(day['humidity'])
            line.append(day['weather_description'])
            line.append('True' if day['max_temperature'] > 30 else 'False')
            line.append('True' if day['wind_speed'] > 15 else 'False')
            line.append('True' if day['precipitation'] > 0 else 'False')
            w.writerow(line)



if __name__ == "__main__":
    # Load the JSON data
    weather_data = load_json("tokyo_weather_complex.json")

    # Summarize the weather data
    summary = summarize_weather_data(weather_data['daily'])

    # Print the summary for verification
    print("Weather Data Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Export the summarized data to a CSV file
    export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

    print("Data successfully exported to tokyo_weather_summary.csv")
