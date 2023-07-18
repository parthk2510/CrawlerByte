import requests
url = "https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en"

def fetchandsave(url, path):
    r = requests.get(url)
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)
   
fetchandsave(url, "DATA/Link.txt")
r = requests.get(url)
print = r.text
