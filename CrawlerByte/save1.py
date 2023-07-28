# Importing the required libraries
import os

# For saving the json data
import json

# For saving the csv data
import csv
from bs4 import BeautifulSoup
import requests

'''
def save_json(crawled_data):
    with open(
        os.path.join(os.path.dirname(__file__), "..", "results", "results.json"),
        "w",
        encoding="utf-8",
    ) as results:
        json.dump(crawled_data, results)


def check_word_in_tokenized_data(word_to_check):
    json_file_path = "results/results.json"
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        tokenized_data = json.load(json_file)

    if not isinstance(tokenized_data, dict):
        raise ValueError("The JSON file does not contain valid tokenized data.")

    words = tokenized_data.get("Words", [])

    word_to_check_lower = word_to_check.lower()
    words_lower = [word.lower() for word in words]

    if word_to_check_lower in words_lower:
        print(f"The word '{word_to_check}' is present in the tokenized set of words.")
    else:
        print(
            f"The word '{word_to_check}' is NOT present in the tokenized set of words."
        )
'''

"""
def save_json(crawled_data, word_to_check):
    def check_word_in_tokenized_data(tokenized_data, word_to_check):
        if not isinstance(tokenized_data, dict):
            raise ValueError("The JSON file does not contain valid tokenized data.")

        words = tokenized_data.get("Words", [])

        word_to_check_lower = word_to_check.lower()
        words_lower = [word.lower() for word in words]

        if word_to_check_lower in words_lower:
            print(f"The word '{word_to_check}' is present in the tokenized set of words.")
        else:
            print(f"The word '{word_to_check}' is NOT present in the tokenized set of words.")

    with open(os.path.join(os.path.dirname(__file__), '..', 'results', 'results.json'), 'w', encoding="utf-8") as results:
        json.dump(crawled_data, results)

    # Assuming you already have the path to the JSON file containing the tokenized data
    json_file_path =os.path.join(os.path.dirname(__file__), json_file_path)
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        tokenized_data = json.load(json_file)

    check_word_in_tokenized_data(tokenized_data, word_to_check)
"""


# Saving crawled data in results/results.json

def save_json(crawled_data):
    with open(os.path.join(os.path.dirname( __file__ ), '..', 'results', 'results.json'), 'w', encoding="utf-8") as results:
        json.dump(crawled_data, results)



# Saving crawled data in results/results.csv
def save_csv(crawled_data):
    crawled_links = crawled_data["crawled_links"]
    fields = list(crawled_links[0].keys())

    with open(
        os.path.join(os.path.dirname(__file__), "..", "results", "results.csv"),
        "w",
        encoding="utf-8",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(crawled_links)

def save_website_data_to_json(url):

    path=os.path.dirname( __file__ ), '..', 'results', 'results.json'
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
# Backup the data
def backup(crawled_data):
    print("Backing up the data...")
    save_json(crawled_data)
