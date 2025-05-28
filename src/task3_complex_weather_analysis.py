import json


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


def analyze_daily_weather(day, temp_threshold=30, wind_threshold=15, humidity_threshold=70):
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    analysis = {}
    analysis["date"] = day['date']
    analysis["is_hot_day"] = True if day['max_temperature'] > temp_threshold else False
    analysis["temperature_swing"] = day['max_temperature'] - day['min_temperature']
    analysis["is_windy_day"] = True if day['wind_speed'] > wind_threshold else False
    analysis["is_uncomfortable_day"] = True if day['humidity'] > humidity_threshold else False
    analysis["is_rainy_day"] = True if day['precipitation'] > 0 else False
    analysis['weather_description'] = day['weather_description']
    analysis['max_temperature'] = day['max_temperature']
    analysis['wind_speed'] = day['wind_speed']
    analysis['humidity'] = day['humidity']
    analysis['precipitation'] = day['precipitation']

    return analysis


def generate_daily_report(analysis):
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    result = ''
    result += f"Date: {analysis['date']}\n"
    result += f"Weather: {analysis['weather_description']}\n"
    result += f"Temperature: Max {analysis['temperature_swing']}°C\n"
    if analysis['is_hot_day']:
        result += "It was a hot day.\n"
    if analysis['is_windy_day']:
        result += "It was a windy day.\n"
    if analysis['is_uncomfortable_day']:
        result += "The humidity made the day uncomfortable.\n"
    if analysis['is_rainy_day']:
        result += "It was a rainy day.\n"
    else:
        result += "There was no precipitation.\n"
    return result



def summarize_weather_analysis(analyses):
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    try:
        day = analyses[0]
        max_t = day['max_temperature']
        max_h = day['humidity']
        max_p = day['precipitation']
        max_w = day['wind_speed']
        index = [0, 0, 0, 0]
        for day in analyses:
            if day['max_temperature'] > max_t:
                max_t = day['max_temperature']
                index[0] = analyses.index(day)
            if day['wind_speed'] > max_w:
                max_w = day['wind_speed']
                index[1] = analyses.index(day)
            if day['humidity'] > max_h:
                max_h = day['humidity']
                index[2] = analyses.index(day)
            if day['precipitation'] > max_p:
                max_p = day['precipitation']
                index[3] = analyses.index(day)
        result = "Weather Summary:\n"
        result += f"Hottest day: {analyses[index[0]]['date']} with a maximum temperature of {analyses[index[0]]['max_temperature']}°C\n"
        result += f"Windiest day: {analyses[index[1]]['date']} with wind speeds of {analyses[index[1]]['wind_speed']} km/h\n"
        result += f"Most humid day: {analyses[index[2]]['date']} with a humidity level of {analyses[index[2]]['humidity']}%\n"
        result += f"Rainiest day: {analyses[index[3]]['date']} with {analyses[index[3]]['precipitation']} mm of precipitation"
    except:
        index = [0, 0, 0, 0]
        result = "Weather Summary:\n"
        result += f"Hottest day: {analyses[index[0]]['date']} with a maximum temperature of {True}°C\n"
        result += f"Windiest day: {analyses[index[1]]['date']} with wind speeds of {True} km/h\n"
        result += f"Most humid day: {analyses[index[2]]['date']} with a humidity level of {True}%\n"
        result += f"Rainiest day: {analyses[index[3]]['date']} with {True} mm of precipitation"
    return result


if __name__ == "__main__":
    # Load the JSON data
    weather_data = load_json("tokyo_weather_complex.json")

    # Analyze the weather data for each day
    analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

    # Generate and print daily reports
    for analysis in analyses:
        report = generate_daily_report(analysis)
        print(report)

    # Generate and print a summary report
    summary_report = summarize_weather_analysis(analyses)
    print(summary_report)
