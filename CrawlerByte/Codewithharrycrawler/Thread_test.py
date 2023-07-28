import concurrent.futures
import urllib.request
import time

start = time.time()
urls = [
    "http://www.google.com",
    "http://www.apple.com",
    "http://www.microsoft.com",
    "http://www.amazon.com",
    "http://www.facebook.com",
]

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read().decode("utf-8")

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('"%s" generated an exception: %s' % (url, exc))
        else:
            print('"%s" fetched in %ss' % (url, (time.time() - start)))

print("Elapsed Time: %ss" % (time.time() - start))
