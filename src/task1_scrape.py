import requests
import responses
from bs4 import BeautifulSoup
import json


class HTTPError(Exception):
    pass

def fetch_wikipedia_page(url):
    """
    Fetch the HTML content of the given Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The HTML content of the page as a string.

    Raises:
        HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text



def extract_title(soup):
    """
    Extract the title of the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The title of the page.
    """
    
    return soup.find('h1', {'id': 'firstHeading'}).text


def extract_first_sentence(soup):
    """
    Extract the first sentence of the first paragraph on the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The first sentence of the first paragraph.
    """
    paragraphs = soup.find_all('p')
    # Print the first few paragraphs of the page
    for i, para in enumerate(paragraphs[:1], start=1):
        result = para.text

    result = result.split('.')[0] + '.'
    return result


def save_to_json(data, filename):
    """
    Save the extracted data to a JSON file.

    Args:
        data (dict): The data to be saved to the JSON file.
        filename (str): The name of the JSON file to save the data in.
    """
    with open(filename, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    page_content = fetch_wikipedia_page(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    # Extract the title of the page
    title = extract_title(soup)

    # Extract the first sentence of the first paragraph
    first_sentence = extract_first_sentence(soup)

    # Combine the extracted data
    extracted_data = {
        "title": title,
        "first_sentence": first_sentence
    }

    # Print the extracted data
    print("Extracted Data:", extracted_data)

    # Save the data to a JSON file
    save_to_json(extracted_data, 'extracted_wikipedia_data.json')

    print("Data successfully saved to extracted_wikipedia_data.json")
