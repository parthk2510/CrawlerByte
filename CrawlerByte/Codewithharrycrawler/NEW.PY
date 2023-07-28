import os
import requests
from urllib.parse import urlparse


def scrape_and_save(url):
    response = requests.get(url)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        folder_name = parsed_url.netloc.replace(".", "_")
        os.makedirs(folder_name, exist_ok=True)
        with open(os.path.join(folder_name, "data.txt"), "w", encoding="utf-8") as file:
            file.write(response.text)


if __name__ == "__main__":
    url_to_scrape = (
        "https://www.codewithharry.com/"  # Replace this with the URL you want to scrape
    )
    scrape_and_save(url_to_scrape)
