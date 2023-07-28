
def crawl_link(link):
    # Function to make a request to the given link and extract data
    try:
        response = requests.get(link)
        # Process the response here and extract data
        parse(response)
    except requests.exceptions.RequestException as e:
        print(f"Error crawling link: {link}, {e}")