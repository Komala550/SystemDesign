import time
from collections import deque

class LeakyBucket:
    def __init__(self, bucket_size, leak_rate):
        self.bucket_size = bucket_size  # Maximum number of requests the bucket can hold
        self.leak_rate = leak_rate      # Rate at which requests are processed (requests per second)
        self.queue = deque()            # Queue to store incoming requests
        self.last_leak_time = time.time()  # Last time the bucket was leaked

    def allow_request(self):
        now = time.time()
        elapsed_time = now - self.last_leak_time

        # Calculate the number of requests to leak based on elapsed time and leak rate
        requests_to_leak = int(elapsed_time * self.leak_rate)
        print(f"Elapsed time: {elapsed_time:.2f} seconds, Requests to leak: {requests_to_leak}")

        # Leak requests from the bucket
        for _ in range(requests_to_leak):
            if self.queue:
                leaked_request_time = self.queue.popleft()
                print(f"Leaked request with timestamp: {leaked_request_time:.2f}")

        # Update the last leak time
        self.last_leak_time = now

        # Check if there is space in the bucket for the new request
        if len(self.queue) < self.bucket_size:
            self.queue.append(now)
            print(f"Request accepted. Bucket size: {len(self.queue)}")
            return True
        else:
            print(f"Bucket full. Request rejected. Bucket size: {len(self.queue)}")
            return False

def main():
    # Create a LeakyBucket instance with a bucket size of 5 and a leak rate of 1 request per second
    bucket = LeakyBucket(bucket_size=2, leak_rate=3)

    # Simulate requests
    for i in range(10):
        if bucket.allow_request():
            print(f"Request {i + 1} processed")
        else:
            print(f"Request {i + 1} rejected")
        time.sleep(0.5)  # Simulate time between requests

if __name__ == "__main__":
    main()
