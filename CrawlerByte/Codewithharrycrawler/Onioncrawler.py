import asyncio
import aiohttp
import aiofiles
import os

# Function to save the data to a file
async def save_data(url, data):
    filename = f"{url.replace('/', '_').replace('.', '_')}.html"
    async with aiofiles.open(filename, "wb") as f:
        await f.write(data.encode("utf-8"))
        print(f"Saved {filename}")

# Function to fetch a single page
async def fetch_page(url, session):
    try:
        async with session.get(url) as response:
            data = await response.text()
            await save_data(url, data)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Main crawler function
async def crawl_onion_links(links):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(link, session) for link in links]
        await asyncio.gather(*tasks)

# Read .onion links from the file
def read_onion_links(file_path):
    with open(file_path, "r") as file:
        links = [line.strip() for line in file]
    return links

# File path with .onion links
file_path = "C:\\Users\\kpart\\Desktop\\Codewithharrycrawler\\New Text Document (2).txt"

# Create a directory to save the files
if not os.path.exists("onion_data"):
    os.makedirs("onion_data")

# Run the crawler
if __name__ == "__main__":
    onion_links = read_onion_links(file_path)
    asyncio.run(crawl_onion_links(onion_links))
