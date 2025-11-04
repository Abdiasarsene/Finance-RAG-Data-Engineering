# src/vector_store/milvus_connection.py
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import yaml
from logs.logger import logger

# ====== MILVUS CONNECTION ======
class MilvusConnection:
    # Set up
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)["milvus"]
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 19530)
        self.collection_name = config.get("collection_name", "default_collection")
        self.dimension = config.get("dimension", 768)
        self.index_type = config.get("index_type", "IVF_FLAT")
        self.metric_type = config.get("metric_type", "COSINE")
        self.batch_size = config.get("batch_size", 128)
        self.collection = None
        self.connect()

    # Connect
    def connect(self):
        try:
            connections.connect(alias="default", host=self.host, port=self.port)
            logger.info("✅ Connected to Milvus", host=self.host, port=self.port)
            self._init_collection()
        except Exception as e:
            logger.error("Erreur connexion Milvus", error=str(e))
            raise

    # Define schema
    def _init_collection(self):
        fields = [
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.dimension),
            FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="message_id", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="order", dtype=DataType.INT64),
            FieldSchema(name="lang", dtype=DataType.VARCHAR, max_length=8)
        ]
        schema = CollectionSchema(fields, description="Vector collection for RAG")
        try:
            self.collection = Collection(self.collection_name, schema=schema)
            logger.info("Collection Milvus ready", collection=self.collection_name)
        except Exception:
            self.collection = Collection(self.collection_name)
            logger.info("Collection Milvus déjà existante", collection=self.collection_name)