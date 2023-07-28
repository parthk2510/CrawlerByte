import os
import re
import requests
from urllib.parse import urlparse
from collections import deque

# Global variables
internal = set()
processed = set()
headers = {}
crawl_level = 2  # The number of levels to crawl

# Function to extract URLs from a given URL's response
def extractor(url):
    global internal, processed

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            processed.add(url)
            print("Crawling:", url)

            # Extracting URLs from the response body
            matches = re.findall(r'href=["\'](.*?)["\']', response.text)
            for link in matches:
                if link.startswith("http"):
                    if link.startswith(main_url):
                        internal.add(link)
                else:
                    internal.add(main_url + link)

    except Exception as e:
        print("Error crawling:", url, e)

# Main crawler function
def web_crawler(root_url):
    global main_url

    # Set the main URL and extract headers if not already done
    main_url = root_url
    try:
        headers.update(extract_headers())
    except FileNotFoundError as e:
        print('Could not load headers prompt:', e)
        quit()

    internal.add(main_url)

    # Start crawling
    for level in range(crawl_level):
        links = internal - processed
        if not links:
            break

        print('Level {}: {} URLs'.format(level + 1, len(links)))

        for link in links.copy():
            extractor(link)

# Function to extract headers from a prompt
def extract_headers():
    # Your code here to extract headers from a prompt
    # For example, you can use input() to get user input for headers
    headers = {
        "User-Agent": "Your User-Agent Here",
    }
    return headers

# Main function to start crawling
if __name__ == "__main__":
    root_url = input("Enter the root URL to crawl: ").strip()
    web_crawler(root_url)
