import csv
import re


def clean_text(line):
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    
    return ''.join([i if ord(i) < 128 else ' ' for i in line])


def extract_weather_data(text_file):
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.
    """
    with open(text_file) as file:
        lines = [line.rstrip() for line in file]
    extracted_data = []


    for line in lines:
        clean = clean_text(line)
        nums = re.findall(r"\d+\.?\d*", clean)
        temp_dict = {}
        temp_dict['date'] = nums[0] + '-' + nums[1] + '-' + nums[2]
        temp_dict['max_temperature'] = float(nums[3])
        temp_dict['min_temperature'] = float(nums[4])
        temp_dict['humidity'] = int(nums[5])
        temp_dict['precipitation'] = float(nums[6])
        extracted_data.append(temp_dict)
    return extracted_data

def save_to_csv(data, filename="extracted_weather_data.csv"):
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Date', 'Max Temperature', 'Min Temperature', 'Humidity', 'Precipitation'])
        for day in data:
            line = [value for value in day.values()]
            w.writerow(line)


if __name__ == "__main__":
    # Extract data from the text file
    weather_data = extract_weather_data("weather_report.txt")

    # Save the extracted data to a CSV file
    save_to_csv(weather_data)
    print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
