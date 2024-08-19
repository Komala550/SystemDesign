from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            # Move the accessed item to the end of the OrderedDict to show it was recently used
            value = self.cache.pop(key)
            self.cache[key] = value
            return value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Remove the old value
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # Remove the oldest (least recently used) item
            self.cache.popitem(last=False)
        # Add the new item
        self.cache[key] = value

# Example usage
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # Output: 1
cache.put(3, 3)     # Removes key 2
print(cache.get(2))  # Output: -1 (not found)
cache.put(4, 4)     # Removes key 1
print(cache.get(1))  # Output: -1 (not found)
print(cache.get(3))  # Output: 3
print(cache.get(4))  # Output: 4
