# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup
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
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('DATA'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


python_articles = "https://www.geeksforgeeks.org/category/language/python/page/"

def get_links(name,pages):
    links = []
    for i in range(1,pages+1):
        py_page = requests.get(name+'/'+str(i))
        py_soup = BeautifulSoup(py_page.content, 'lxml')
        jobs = py_soup.find_all("div",class_='content')
        links.extend(jobs)
        print(i)
    return links


links = get_links(python_articles,10)


print(links[0])


def get_urls(links):
    urls = []
    for link in links:
        a = link.find("a")
        if a!=None:
            urls.append(a['href'])
        else:
            urls.append(None)
    return urls


urls = get_urls(links)
#how many non-na articles there are
print('Links found',len([el for el in urls if el!=None]))
print('Overall length',len(urls))
print(urls)

def tag_visible(element):
    if element.parent.name in [
            'style', 'script', 'head', 'title', 'meta', '[document]'
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    body = urllib.request.urlopen(body).read()
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)



texts = []
for (i,url) in enumerate(urls):
    if url!=None:
        text = text_from_html(url)
        #print("TEXT\n\n\n",url)
        #print(text)
        texts.append(text)
    else:
        texts.append(None)
    if i%10==0:
        print(i)
    
df = pd.DataFrame()
df['text_unprocessed'] = texts
df['url'] = urls
df['class'] = 'python'