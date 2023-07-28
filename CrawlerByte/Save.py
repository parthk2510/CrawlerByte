import urllib.request
from stem.control import *
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse
import re
import pandas as pd
from bs4 import Comment
import string
from sklearn.metrics import r2_score
from sklearn.naive_bayes import MultinomialNB
import re
import urllib
import seaborn as sns
import matplotlib.pyplot as plt
import json 
import requests

def fetchandsave(url, path):
    r = requests.get(url,verify=False)
    response = requests.get(url,headers = None, timeout = 40)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        folder_name = parsed_url.netloc.replace(".", "_")
        os.makedirs(folder_name, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(r.text)

def fetchandsavehtml(url, path):
    get = urllib.request.urlopen(url,verify=False)
    html = get.read()
    soup = BeautifulSoup(html)
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))


def fetchandsavecsv(url, path):
    get = urllib.request.urlopen(url,verify=False)
    html = get.read()
    soup = BeautifulSoup(html, "html.parser")

    # Extract specific data from the HTML
    # Example: Extract all table rows and write them to the CSV
    data = []
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            data_row = [column.get_text(strip=True) for column in columns]
            data.append(data_row)

    # Save data as a CSV
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)


def fetchandsaveemailid(url, path):
    get = urllib.request.urlopen(url,verify=False)
    html = get.read()
    soup = BeautifulSoup(html, "html.parser")
    emailid_data = []
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    email_tags = soup.find_all(text=re.compile(email_regex))
    for tag in email_tags:
        email = re.findall(email_regex, tag)
        if email:
            emailid_data.append([email[0], url])
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Email", "URL"])
        writer.writerows(emailid_data)


def fetchandsavephonenum(url, path):
    get = urllib.request.urlopen(url,verify=False)
    html = get.read()
    soup = BeautifulSoup(html, "html.parser")

    # Extract phone numbers and corresponding URLs with country origin from the HTML
    phone_data = []
    phone_regex = (
        r"(\+\d{1,3}\s?)?(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\d{4}[-]\d{3}[-]\d{4})"
    )
    phone_tags = soup.find_all(text=re.compile(phone_regex))
    for tag in phone_tags:
        phone_numbers = re.findall(phone_regex, tag)
        for phone_number in phone_numbers:
            country_origin = ""
            if phone_number[0] and phone_number[0].startswith("+"):
                country_origin = phone_number[0].strip()
                phone_number = phone_number[1].strip()
            else:
                phone_number = phone_number[0].strip()
            phone_data.append([phone_number, url, country_origin])

    # Save phone number data as a CSV
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Phone Number", "URL", "Country Origin"])
        writer.writerows(phone_data)


def fetchandsavecsv1(url, path):
    get = urllib.request.urlopen(url,verify=False)
    html = get.read()
    soup = BeautifulSoup(html, "html.parser")

    # Extract phone numbers and corresponding URLs with country origin from the HTML
    phone_data = []
    phone_regex = r"(^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$)"
    phone_tags = soup.find_all(text=re.compile(phone_regex))
    for tag in phone_tags:
        phone_numbers = re.findall(phone_regex, tag)
        for phone_number in phone_numbers:
            country_origin = ""
            if phone_number[0] and phone_number[0].startswith("+"):
                country_origin = phone_number[0].strip()
                phone_number = phone_number[1].strip()
            else:
                phone_number = phone_number[0].strip()
            phone_data.append([phone_number, url, country_origin])

    # Save phone number data as a CSV
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Phone Number", "URL", "Country Origin"])
        writer.writerows(phone_data)


def fetchandsaveurl(url, path):
    get = urllib.request.urlopen(url,verify=False)
    html = get.read()
    soup = BeautifulSoup(html, "html.parser")

    # Extract URLs from the HTML
    url_data = []
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    url_tags = soup.find_all(href=re.compile(url_regex))
    for tag in url_tags:
        url = re.findall(url_regex, tag["href"])
        if url:
            url_data.append([url[0]])

    # Save URL data as a CSV
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["URL"])
        writer.writerows(url_data)


def save_website_data_to_json(url, path):
   
    # Send a request to the website and get the HTML content
    response = requests.get(url,verify=False)
    if response.status_code != 200:
        print(
            f"Failed to retrieve the website content. Status code: {response.status_code}"
        )
        return

    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the desired parameters
    data = {
        "title": soup.title.string,
        "title_name": soup.title.name,
        "title_parent_name": soup.title.parent.name,
        "paragraph": soup.p.string if soup.p else None,
        "paragraph_class": soup.p["class"] if "class" in soup.p.attrs else None,
        "first_anchor_tag": soup.a.string if soup.a else None,
        "all_anchor_tags": [tag.string for tag in soup.find_all("a") if tag.string],
    }

    # Save the data in JSON format
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)