from collections import deque
from datetime import datetime

class SearchHistoryStack:
    """LIFO Stack for storing user's recent route searches."""
    def __init__(self, capacity=20):
        self.stack = []
        self.capacity = capacity

    def push(self, source, destination, algo, distance, stops):
        entry = {
            "source": source,
            "destination": destination,
            "algo": algo,
            "distance": distance,
            "stops": stops,
            "timestamp": datetime.now().strftime("%I:%M %p, %b %d")
        }
        self.stack.append(entry)
        if len(self.stack) > self.capacity:
            self.stack.pop(0)  # Maintain stack capacity size

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self):
        if self.stack:
            return self.stack[-1]
        return None

    def get_all_reversed(self):
        """Returns items in LIFO order (most recent first)."""
        return list(reversed(self.stack))

    def clear(self):
        self.stack = []

class BookingQueue:
    """FIFO Queue for managing passenger ticket bookings."""
    def __init__(self):
        self.queue = deque()

    def enqueue(self, passenger_name, source, destination):
        ticket = {
            "passenger_name": passenger_name,
            "source": source,
            "destination": destination,
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        self.queue.append(ticket)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def get_all(self):
        return list(self.queue)
