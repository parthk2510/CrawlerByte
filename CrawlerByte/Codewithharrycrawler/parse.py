def parse(response):
    page = response.url.split("/")[-2]
    filename = f"quotes-{page}.html"
    with open(filename, "wb") as file:
        file.write(response.content)
    print(f"Saved file {filename}")