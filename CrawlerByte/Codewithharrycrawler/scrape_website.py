def scrape_website(url):
    # Send a request to the website to get the HTML content
    response = requests.get(url,proxies,headers = None, timeout = 40)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove unwanted elements from the HTML content
        for unwanted_element in soup(["script", "style", "meta", "link"]):
            unwanted_element.extract()

        # Extract the text from the remaining elements
        text_content = soup.get_text()

        # Remove extra white spaces and newlines
        text_content = " ".join(text_content.split())
        parse(url)

        return text_content
    else:
        print(
            f"Failed to retrieve content from '{url}'. Status code: {response.status_code}"
        )

        return None