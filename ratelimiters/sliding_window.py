import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size, max_requests):
        self.window_size = window_size  # The size of the time window in seconds
        self.max_requests = max_requests  # Maximum number of requests allowed in the window
        self.requests = deque()  # Queue to store timestamps of requests

    def allow_request(self):
        now = time.time()
        # Remove requests that are outside the sliding window
        while self.requests and self.requests[0] < now - self.window_size:
            self.requests.popleft()

        # Check if the number of requests within the window is below the limit
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        else:
            return False

def main():
    # Create a SlidingWindowRateLimiter instance with a window size of 10 seconds and a max of 5 requests
    rate_limiter = SlidingWindowRateLimiter(window_size=10, max_requests=5)

    # Simulate requests
    for i in range(20):
        if rate_limiter.allow_request():
            print(f"Request {i + 1} processed")
        else:
            print(f"Request {i + 1} rejected")
        time.sleep(1)  # Simulate time between requests

if __name__ == "__main__":
    main()
