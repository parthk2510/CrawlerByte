

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
        response = crawl_link(link)
        parse(response)

        # Mark the task as done in the queue
        link_queue.task_done()

        # Release the semaphore to allow another thread to start
        thread_semaphore.release()