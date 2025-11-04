# tests/mocks/mock_rabbuitmq
from collections import defaultdict, deque

# ====== MOCK RABBITMQ =====
class MockRabbitMQ:
    # Set up
    def __init__(self):
        self.queues = defaultdict(deque)

    # Declare queue
    def declare_queue(self, queue_name):
        self.queues[queue_name]

    # Publish
    def publish(self, queue_name, message):
        self.queues[queue_name].append(message)

    # Consume
    def consume(self, queue_name):
        if self.queues[queue_name]:
            return self.queues[queue_name].popleft()
        return None

    # Queue size
    def queue_size(self, queue_name):
        return len(self.queues[queue_name])

    # Close
    def close(self):
        pass