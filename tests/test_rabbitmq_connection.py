# tests/manual_test_rabbitmq_connection.py
import json
import time
from connectors.rabbitmq.rabbitmq_client import RabbitMQClient

if __name__ == "__main__":
    print("🔍 Testing real RabbitMQ connection...\n")

    try:
        # Initialize client (reads host/port from .env via settings)
        client = RabbitMQClient()
        queue_name = "test_queue"

        # Declare queue
        client.declare_queue(queue_name)
        print(f"📦 Queue '{queue_name}' declared.")

        # Publish a test message
        message = {"event": "ping", "timestamp": time.time()}
        client.publish(queue_name, message)
        print(f"🚀 Published test message: {json.dumps(message)}")

        # Consume one message (with a temporary callback)
        def callback(msg):
            print(f"📨 Received message: {msg}")

        print("🌀 Waiting for message (Ctrl+C to stop)...\n")
        client.consume(queue_name, callback, auto_ack=True)
        client.start_consuming()

    except KeyboardInterrupt:
        print("\n🛑 Test manually stopped by user.")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        try:
            client.close()
        except Exception:
            pass