import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from collections import deque

class SimpleWebCrawler:
    def __init__(self, start_url, max_depth=2):
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited = set()
        self.queue = deque([(start_url, 0)])  # (URL, depth)
    
    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_page(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            absolute_link = urljoin(base_url, link)
            links.add(absolute_link)
        return links

    def crawl(self):
        while self.queue:
            url, depth = self.queue.popleft()
            
            if depth > self.max_depth:
                continue
            
            if url in self.visited:
                continue
            
            self.visited.add(url)
            print(f"Crawling {url} at depth {depth}")
            
            html = self.fetch_page(url)
            if html:
                links = self.parse_page(html, url)
                for link in links:
                    if link not in self.visited:
                        self.queue.append((link, depth + 1))
            
            # Respectful crawling by sleeping between requests
            time.sleep(1)

if __name__ == "__main__":
    crawler = SimpleWebCrawler(start_url="http://example.com")
    crawler.crawl()
