# tests/test_milvus_connection.py
import pytest
from connectors.milvus.milvus_connection import MilvusConnection
from pymilvus import connections, list_collections

# ====== TEST MILVUS CONNECTION AND COLLECTION ======
def test_milvus_connection_and_collection(tmp_path):
    # Create config file
    config_content = """
    milvus:
        host: localhost
        port: 19530
        collection_name: test_collection
        dimension: 8
        index_type: IVF_FLAT
        metric_type: COSINE
        batch_size: 16
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content)

    # Intialize connection
    client = MilvusConnection(str(config_path))

    # Check connection
    assert connections.has_connection("default"), "La connexion à Milvus a échoué"

    # Check if collection exists
    collections = list_collections()
    assert "test_collection" in collections, "La collection Milvus n’a pas été créée"

    # Clean once checked
    client.collection.drop()