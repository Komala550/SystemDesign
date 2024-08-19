import requests
from bs4 import BeautifulSoup

class WebCrawler:
    def __init__(self, seed_urls):
        self.url_frontier = seed_urls
        self.visited_urls = set()
        self.documents = {}  # To store content of visited URLs

    def crawl(self):
        print("Starting crawl...")
        while self.url_frontier:
            url = self.url_frontier.pop(0)
            if url not in self.visited_urls:
                print(f"Fetching URL: {url}")
                content, links = self.fetch(url)
                self.process(url, content)
                self.url_frontier.extend(links)
                self.visited_urls.add(url)
        print("Crawl complete. Visited URLs:", self.visited_urls)

    def fetch(self, url):
        try:
            response = requests.get(url)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return content, links
        except requests.RequestException as e:
            print(f"Request failed for URL {url}: {e}")
            return "", []

    def process(self, url, content):
        self.documents[url] = content  # Save document content
        print(f"Processed URL: {url} with {len(content)} characters")

class Indexer:
    def __init__(self):
        self.inverted_index = {}
    
    def index_document(self, doc_id, content):
        print(f"Indexing document ID: {doc_id}")
        for word in content.split():
            word = word.lower()  # Normalize to lowercase
            if word not in self.inverted_index:
                self.inverted_index[word] = set()
            self.inverted_index[word].add(doc_id)
    
    def save_index(self):
        # Save the index to disk or a distributed store
        print("Index saved. Number of unique words:", len(self.inverted_index))

class QueryProcessor:
    def __init__(self, indexer):
        self.indexer = indexer
    
    def process_query(self, query):
        print(f"Processing query: '{query}'")
        words = query.split()
        doc_ids = set()
        for word in words:
            word = word.lower()  # Normalize to lowercase
            if word in self.indexer.inverted_index:
                doc_ids.update(self.indexer.inverted_index[word])
        print(f"Found document IDs for query: {doc_ids}")
        return doc_ids

class Ranker:
    def rank_results(self, doc_ids, query):
        # Rank documents based on relevance to the query
        print(f"Ranking document IDs: {doc_ids}")
        return sorted(doc_ids)  # Placeholder for actual ranking logic

class DistributedSystem:
    def __init__(self):
        self.servers = []
    
    def add_server(self, server):
        self.servers.append(server)
        print(f"Server added: {server}")
    
    def distribute_tasks(self, tasks):
        print(f"Distributing tasks: {tasks} to servers: {self.servers}")

def main():
    # Create a WebCrawler instance
    seed_urls = ["http://example.com"]
    crawler = WebCrawler(seed_urls)
    crawler.crawl()
    
    # Create an Indexer instance
    indexer = Indexer()
    for doc_id, (url, content) in enumerate(crawler.documents.items()):
        indexer.index_document(doc_id, content)
    
    # Save the index
    indexer.save_index()
    
    # Create a QueryProcessor instance
    query_processor = QueryProcessor(indexer)
    query = "example"
    doc_ids = query_processor.process_query(query)
    
    # Create a Ranker instance
    ranker = Ranker()
    ranked_docs = ranker.rank_results(doc_ids, query)
    
    # Create a DistributedSystem instance
    distributed_system = DistributedSystem()
    # Example of adding servers
    distributed_system.add_server("server1")
    distributed_system.add_server("server2")
    # Example of distributing tasks
    distributed_system.distribute_tasks(["task1", "task2"])
    
    print(f"Ranked documents for query '{query}': {ranked_docs}")

if __name__ == "__main__":
    main()
