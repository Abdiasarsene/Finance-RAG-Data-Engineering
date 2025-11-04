# tests/mocks/mock_services.py
from tests.mocks.mock_minio import MockMinIOClient
from tests.mocks.mock_rabbitmq import MockRabbitMQ
from tests.mocks.mock_milvus import MockMilvusConnection
from tests.mocks.mock_elasticsearch import MockElasticsearch

# ====== ALL EXTERNE SERVICES MOCK ======
class MockServices:
    # Set up
    def __init__(self):
        self.minio = MockMinIOClient()
        self.rabbitmq = MockRabbitMQ()
        self.milvus = MockMilvusConnection()
        self.elasticsearch = MockElasticsearch()

    # Initialize
    def reset_all(self):
        self.minio = MockMinIOClient()
        self.rabbitmq = MockRabbitMQ()
        self.milvus = MockMilvusConnection()
        self.elasticsearch = MockElasticsearch()

    # Share overview
    def summary(self):
        return {
            "minio_buckets": {b: list(v.keys()) for b, v in self.minio.storage.items()},
            "rabbitmq_queues": {q: len(v) for q, v in self.rabbitmq.queues.items()},
            "milvus_vectors": len(self.milvus.vectors),
            "elasticsearch_indices": list(self.elasticsearch.index.keys()),
        }

services = MockServices()