import httplib2
import csv
import json
from bs4 import BeautifulSoup
import socks
import socket
from stem import Signal
from stem.control import Controller

# Temporary override of socket.getaddrinfo to filter responses for AF_INET
old_getaddrinfo = socket.getaddrinfo


def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]


socket.getaddrinfo = new_getaddrinfo


def connect_tor():
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket


def renew_tor_ip():
    with Controller.from_port(port=9050) as controller:
        controller.authenticate(password='16:F542E95058E4CA74608DB75282043DF32DDE5D30B0B22A038F8C61B5A0')
        controller.signal(Signal.NEWNYM)


renew_tor_ip()


def fetch_data_from_website(url):
    http = httplib2.Http()
    response, content = http.request(url, 'GET')

    if response.status == 200:
        soup = BeautifulSoup(content, 'html.parser')
        items_list = soup.find('ul')

        if items_list:
            items = [item.get_text() for item in items_list.find_all('li')]
            return items
        else:
            print("No items found on the page.")
    else:
        print(f"Request failed with status code: {response.status}")


def save_data_in_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Item"])
        writer.writerows([[item] for item in data])


def save_data_in_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)


def save_data_in_html(data, filename):
    with open(filename, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write("<html><body><ul>\n")
        for item in data:
            htmlfile.write(f"<li>{item}</li>\n")
        htmlfile.write("</ul></body></html>")


if __name__ == "__main__":
    connect_tor()  # Connect to Tor network via SOCKS5 proxy

    # Replace with the URL of the website you want to scrape
    website_url = "http://darkeyepxw7cuu2cppnjlgqaav6j42gyt43clcn4vjjf7llfyly5cxid.onion/hs/kingdom-market.html"

    renew_tor_ip()
    data = fetch_data_from_website(website_url)

    if data:
        # Save data in CSV format
        csv_filename = "data.csv"
        save_data_in_csv(data, csv_filename)

        # Save data in JSON format
        json_filename = "data.json"
        save_data_in_json(data, json_filename)

        # Save data in HTML format
        html_filename = "data.html"
        save_data_in_html(data, html_filename)

        print("Data scraped and saved successfully.")
    else:
        print("No data was scraped.")
