# src/utils/rabbitmq.py
import pika
import json
import time
from utils.config import settings

class RabbitMQClient:
    def __init__(self):
        self.host = settings.rabbitmq_host
        self.port = int(settings.rabbitmq_port)
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port)
        )
        self.channel = self.connection.channel()
        print(f"✅ Connected to RabbitMQ at {self.host}:{self.port}")

    def reconnect(self):
        while True:
            try:
                self.connect()
                print("♻️ Reconnected to RabbitMQ")
                break
            except Exception as e:
                print(f"❌ Reconnect failed: {e}")
                time.sleep(5)

    def declare_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def publish(self, queue_name: str, data: dict):
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(data),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(f"✅ Published message to {queue_name}")
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.StreamLostError):
            print("⚠️ Lost connection, trying to reconnect...")
            self.reconnect()
            self.publish(queue_name, data)

    def consume(self, queue_name: str, callback, auto_ack=False):
        def _callback(ch, method, properties, body):
            try:
                msg = json.loads(body)
                callback(msg)
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"❌ Error processing message: {e}")
                if not auto_ack:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=_callback)

    def start_consuming(self):
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
        print("✅ Connection closed")