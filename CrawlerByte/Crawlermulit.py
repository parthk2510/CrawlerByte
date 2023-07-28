import threading
import queue
import requests
import json

# Function to request the link and process the data
def process_link(link):
    try:
        response = requests.get(link)
        # Process the response data here
        data = response.text  # Replace this with your actual data processing logic

        # Store the data in a JSON file
        filename = link.replace("/", "_").replace(":", "") + ".json"
        with open(filename, "w") as file:
            json.dump(data, file)

        print(f"Data saved to {filename}")
    except requests.RequestException as e:
        print(f"Failed to get data for link: {link}, Error: {e}")

# Function to be run by each thread
def thread_worker():
    while True:
        link = link_queue.get()
        if link is None:
            break
        process_link(link)
        link_queue.task_done()

# Seed link and depth
seed_link = "https://www.geeksforgeeks.org/category/language/python/page/"
depth = 5

# Initialize the link queue and add the seed link
link_queue = queue.Queue()
link_queue.put(seed_link)

# Create and start 25 threads
num_threads = 25
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=thread_worker)
    thread.start()
    threads.append(thread)

# Wait for all links to be processed
link_queue.join()

# Stop all threads
for _ in range(num_threads):
    link_queue.put(None)

for thread in threads:
    thread.join()

print("All links processed.")
