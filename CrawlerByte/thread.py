import threading
import requests
from queue import Queue
from pathlib import Path

# Maximum number of threads running concurrently
MAX_CONCURRENT_THREADS = 25

# Queue to hold links to be crawled
link_queue = Queue()

# Semaphore to control the number of concurrent threads
thread_semaphore = threading.Semaphore(MAX_CONCURRENT_THREADS)

def crawl_link(link):
    # Function to make a request to the given link and extract data
    try:
        response = requests.get(link)
        # Process the response here and extract data
        parse(response)
    except requests.exceptions.RequestException as e:
        print(f"Error crawling link: {link}, {e}")

def thread_worker():
    while True:
        # Acquire the semaphore to limit the number of concurrent threads
        thread_semaphore.acquire()
        
        # Get the link from the queue
        link = link_queue.get()
        if link is None:
            # If the queue is empty (None is used as a sentinel value), release the semaphore and exit the thread
            thread_semaphore.release()
            break

        # Crawl the link
        crawl_link(link)

        # Mark the task as done in the queue
        link_queue.task_done()

        # Release the semaphore to allow another thread to start
        thread_semaphore.release()

def parse(response):
    page = response.url.split("/")[-2]
    filename = f"quotes-{page}.html"
    with open(filename, "wb") as file:
        file.write(response.content)
    print(f"Saved file {filename}")

if __name__ == "__main__":
    # Get the seed link from the user
    seed_link = input("Enter the seed link: ")
    link_queue.put(seed_link)

    # Start the thread workers
    num_threads = min(MAX_CONCURRENT_THREADS, link_queue.qsize())  # Number of threads is the minimum of queue size and MAX_CONCURRENT_THREADS
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=thread_worker)
        threads.append(thread)
        thread.start()

    # Wait for all the links to be processed
    link_queue.join()

    # Add None as a sentinel value to signal the threads to exit
    for _ in range(num_threads):
        link_queue.put(None)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Crawling completed.")
