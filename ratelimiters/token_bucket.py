import time
from threading import Lock

class TokenBucket:
    def __init__(self, max_bucket_size, refill_rate):
        self.max_bucket_size = max_bucket_size
        self.refill_rate = refill_rate  # tokens per second
        self.current_bucket_size = max_bucket_size
        self.last_refill_time = time.time()
        self.lock = Lock()

    def allow_request(self, tokens):
        with self.lock:
            self.refill()
            if self.current_bucket_size >= tokens:
                self.current_bucket_size -= tokens
                return True
            return False

    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill_time
        tokens_to_add = elapsed * self.refill_rate
        self.current_bucket_size = min(self.current_bucket_size + tokens_to_add, self.max_bucket_size)
        self.last_refill_time = now

def main():
    bucket = TokenBucket(max_bucket_size=2, refill_rate=2)  # max 5 tokens, refill 2 tokens per second

    # Simulate requests
    print(f"Initial bucket size: {bucket.current_bucket_size}")

    print(f"Request processed: {bucket.allow_request(2)}")  # True
    print(f"Bucket size after 1st request: {bucket.current_bucket_size}")
    
    time.sleep(1)
    print(f"Request processed: {bucket.allow_request(3)}")  # True or False
    print(f"Bucket size after 2nd request: {bucket.current_bucket_size}")
    
    time.sleep(2)  # Wait for refill
    print(f"Request processed: {bucket.allow_request(5)}")  # True or False
    print(f"Bucket size after refill: {bucket.current_bucket_size}")
    
    # Request should be rejected or processed based on current bucket size
    print(f"Request processed: {bucket.allow_request(1)}")  # True or False
    print(f"Bucket size after final request: {bucket.current_bucket_size}")

if __name__ == "__main__":
    main()

