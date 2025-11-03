import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_rabbitmq_client():
    """
    Retourne un client RabbitMQ mocké, toutes les méthodes sont simulées
    """
    client = MagicMock()
    client.publish = MagicMock()
    client.consume = MagicMock()
    client.start_consuming = MagicMock()
    client.close = MagicMock()
    return client

@pytest.fixture
def mock_milvus_client():
    """
    Retourne un client Milvus mocké pour tests des workers
    """
    client = MagicMock()
    client.insert = MagicMock(return_value=None)
    client.collection = MagicMock()
    client.collection.drop = MagicMock()
    return client

@pytest.fixture
def mock_process_worker(mock_rabbitmq_client, mock_milvus_client):
    """
    Crée un ProcessWorker avec tous les clients externes mockés
    """
    from workers.processing_worker import ProcessWorker

    worker = ProcessWorker(
        rabbitmq_client=mock_rabbitmq_client,
        milvus_client=mock_milvus_client,
        similarity_threshold=0.8
    )
    return worker