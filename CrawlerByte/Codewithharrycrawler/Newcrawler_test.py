import requests
from bs4 import BeautifulSoup
import re
import socks
import socket
from stem import Signal
from stem.control import Controller

from dotenv import *
proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}


config = dotenv_values(".env")
TORCC_HASH_PASSWORD = config['TORCC_HASH_PASSWORD']
TOR_BROWSER_PATH = config['TOR_BROWSER_PATH']


# Function to change the IP address of Tor
def change_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="TORCC_HASH_PASSWORD")
        controller.signal(Signal.NEWNYM)

# Function to crawl a website and extract email addresses


def crawl_website(url, depth=1, allowed_extensions=None):
    if depth == 0:
        return

    # Change Tor's IP to avoid IP blocking
    change_tor_ip()

    # Set up SOCKS proxy for requests
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket

    try:
        response = requests.get(url,proxies)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Save crawl results in a file
            with open("crawl_results.txt", "a", encoding="utf-8") as file:
                file.write(url + "\n")

            # Obtain email addresses from the crawled page
            email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            emails = re.findall(email_regex, soup.get_text())
            if emails:
                with open("email_addresses.txt", "a", encoding="utf-8") as email_file:
                    email_file.write("\n".join(emails) + "\n")

            # Crawl links recursively up to the specified depth
            if depth > 1:
                for link in soup.find_all("a"):
                    next_url = link.get("href")
                    if next_url and (allowed_extensions is None or any(next_url.endswith(ext) for ext in allowed_extensions)):
                        crawl_website(next_url, depth - 1, allowed_extensions)

    except requests.exceptions.RequestException as e:
        print("Error: ", e)


# Usage example
if __name__ == "__main__":
    starting_url = "https://hiddenwikitor.com/"  # Replace with your desired starting URL
    max_depth = 2  # Specify the maximum depth for crawling
    # Specify the allowed extensions (None for all)
    extensions = [".html", ".php"]

    crawl_website(starting_url, depth=max_depth, allowed_extensions=extensions)
