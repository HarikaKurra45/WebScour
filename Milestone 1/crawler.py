import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import os
def fetch_page(url):
    try:
        response = requests.get(url, timeout=4)
        print("Status Code:", response.status_code)
        response.raise_for_status()
        return response.text
    except:
        print(f"Error fetching {url}:")
        return None
    
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, tag["href"])
        links.add(absolute_url)

    return links
def crawl(seed_url, max_pages=7):
    queue = deque([seed_url])
    visited = set()
    count = 1
    os.makedirs("pages", exist_ok=True)
    while queue and count <= max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        print(f"\nFetching: {url}")
        html = fetch_page(url)

        if html is None:
            continue

        filename = f"pages/page_{count}.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)
        
        links = extract_links(html, url)
        print(f"Saved: page_{count}.html")
        print(f"Extracted {len(links)} links")
        visited.add(url)
        count += 1

        for link in links:
            if link not in visited:
                queue.append(link)
    if html:
        print(f"Total Pages {count-1}")
        print("Page feteched Succesfully")

if __name__ == "__main__":
    seed_url = input("Enter seed URL: ")
    crawl(seed_url, max_pages=7)