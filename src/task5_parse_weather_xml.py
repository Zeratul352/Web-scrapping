import xml.etree.ElementTree as ET
import csv
from xml.dom import minidom

def parse_weather_xml(xml_file):
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.
    """

    dom = minidom.parse(xml_file)
    date = dom.getElementsByTagName('date')
    temp = dom.getElementsByTagName('temperature')
    hum = dom.getElementsByTagName('humidity')
    prec = dom.getElementsByTagName('precipitation')
    result = []
    for i in range(len(date)):
        temp_dict = {}
        temp_dict['date'] = date[i].firstChild.data
        temp_dict['temperature'] = float(temp[i].firstChild.data)
        temp_dict['humidity'] = float(hum[i].firstChild.data)
        temp_dict['precipitation'] = float(prec[i].firstChild.data)
        result.append(temp_dict)

    return result


def save_to_csv(data, filename="parsed_weather_data.csv"):
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Date', 'Temperature', 'Humidity', 'Precipitation'])
        for day in data:
            line = [value for value in day.values()]
            w.writerow(line)


if __name__ == "__main__":
    # Parse the XML file
    weather_data = parse_weather_xml("weather_data.xml")

    # Save the parsed data to a CSV file
    save_to_csv(weather_data)
    print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
