import urllib.request
from stem.control import *
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse
import re
import argparse
import pandas as pd
import lxml
from bs4 import Comment
import string
from sklearn.metrics import r2_score
from sklearn.naive_bayes import MultinomialNB
import re
import urllib
import seaborn as sns
import matplotlib.pyplot as plt
from tokenization import tokenize_text
import json
from checkword import check_word_in_tokenized_data
from preprocessing import preprocess_text
from pathlib import Path
from queue import Queue
import threading
from dotenv import *
import argparse
import math
import time
from datetime import datetime
from functools import reduce
from random import choice
from multiprocessing import Pool, cpu_count, current_process, freeze_support
from tqdm import tqdm
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.parse import quote
from urllib.parse import unquote
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib3.exceptions import ProtocolError
from concurrent.futures import ThreadPoolExecutor
from parse import parse
import socks
import socket
from Crawl_link import *
from Save import *
from save1 import *
from Multi_Try import MultiThreadedDarkWebCrawler
from function import *
from anytree import Node, RenderTree
import httplib2

config = dotenv_values(".env")
TORCC_HASH_PASSWORD = config['TORCC_HASH_PASSWORD']
TOR_BROWSER_PATH = config['TOR_BROWSER_PATH']


proxies = {'http': 'socks5h://127.0.0.1:9150',
           'https': 'socks5h://127.0.0.1:9150', 'http': 'http://proxy.server:3128'}
proxy_handler = urllib.request.ProxyHandler(proxies)
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)

link = input("enter the url ")
link_queue = Queue()
url = link
word_to_check = "pidilite"


def connect_tor():
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socket
    pass


'''class scarper():
    def proxies(self):
      self.proxies = {
            'http' : 'socks5h://127.0.0.1:9150', 
            'https' : 'socks5h://127.0.0.1:9150'
        }
      
    def fetchandsave(url, path):
        r = requests.get(url)
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            folder_name = parsed_url.netloc.replace(".", "_")
            os.makedirs(folder_name, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
 '''


def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=TORCC_HASH_PASSWORD)
        controller.signal(Signal.NEWNYM)

# Get the current IP address to check whether the IP address of tor changed or not.


def get_current_ip(self):
    try:
        response = requests.get("http://httpbin.org/ip", proxies=self.proxies)
        return response.text.split(",")[-1].split('"')[3]
    except Exception as e:
        return str(e)


def tokenization2(url, path):
    with open("DATA\Link.txt", "r", encoding="utf-8", errors="ignore") as file:
        input_text = file.read()

    sentences, words, word_punct_tokens = tokenize_text(input_text)

    tokenized_data = {
        "Sentences": sentences,
        "Words": words,
        "WordPunct Tokens": word_punct_tokens,
    }

    # Save tokenized data to a JSON file
    with open(path, "w", encoding="utf-8", errors="ignore") as json_file:
        json.dump(tokenized_data, json_file, indent=4, ensure_ascii=False)

    print(f"Tokenized data saved to '{path}'")


def fetch_url_with_tor(url):
    try:
        response = requests.get(url, proxies, verify=False)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url}")
        print(e)
        return None


def Main_Function():

    fetchandsave(url, r"DATA/Link.txt")
    fetchandsavehtml(url, r"DATA/Link.html")
    fetchandsaveemailid(url, r"DATA/ExtractedEmailID.csv")
    fetchandsavecsv(url, r"DATA/Link.csv")
    fetchandsavecsv1(url, r"DATA/Phonenum.csv")
    fetchandsavephonenum(url, r"DATA/Phonenum2.csv")
    fetchandsaveurl(url, r"DATA/url.csv")
    # preprocess_text(input_text2)
    save_website_data_to_json(url, r"DATA/Json_output.json")
    tokenization2(url, r"DATA/tokenized_output.json")
    check_word_in_tokenized_data(
        word_to_check, r"DATA/tokenized_output.json")


Main_Function()
