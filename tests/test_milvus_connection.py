# tests/test_milvus_connection.py
import pytest
from connectors.milvus.milvus_connection import MilvusConnection
from pymilvus import connections, list_collections

def test_milvus_connection_and_collection(tmp_path):
    # 1️⃣ Créer un fichier de config temporaire pour ce test
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

    # 2️⃣ Initialiser la connexion
    client = MilvusConnection(str(config_path))

    # 3️⃣ Vérifier la connexion
    assert connections.has_connection("default"), "La connexion à Milvus a échoué"

    # 4️⃣ Vérifier que la collection existe
    collections = list_collections()
    assert "test_collection" in collections, "La collection Milvus n’a pas été créée"

    # 5️⃣ Nettoyer après le test
    client.collection.drop()