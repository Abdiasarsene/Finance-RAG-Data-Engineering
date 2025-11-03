# tests/test_rabbitmq_integration.py
import pytest
import time
from connectors.rabbitmq.rabbitmq_client import RabbitMQClient

# ====== TEST RABBITMQ CONNECTION AND PUBLISH CONSUME ======
QUEUE_NAME = "test_queue"

def test_rabbitmq_connection_and_publish_consume():
    client = RabbitMQClient()

    # Declare tail
    client.declare_queue(QUEUE_NAME)

    # Publish message
    message = {"test": "hello"}
    client.publish(QUEUE_NAME, message)

    # 3️⃣ Consume  message
    received_messages = []

    def callback(msg):
        received_messages.append(msg)

    client.consume(QUEUE_NAME, callback, auto_ack=True)

    # Start_consuming
    import threading
    consume_thread = threading.Thread(target=client.start_consuming, daemon=True)
    consume_thread.start()

    # Wait for the message to be consumed
    timeout = 5
    start = time.time()
    while not received_messages and time.time() - start < timeout:
        time.sleep(0.1)

    client.close()

    assert received_messages, "No message was received from RabbitMQ"
    assert received_messages[0] == message