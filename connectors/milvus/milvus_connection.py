# src/vector_store/milvus_connection.py
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import yaml
from logs.logger import logger
from utils.config import settings


# ====== MILVUS CONNECTION ======
class MilvusConnection:
    """Handles connection and schema setup for Milvus vector database."""

    def __init__(self):
        # Load configuration from path defined in .env
        config_path = settings.milvus_yaml
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)["milvus"]

        # Core configuration (no redundant defaults)
        self.host = cfg["host"]
        self.port = cfg["port"]
        self.collection_name = cfg["collection_name"]
        self.dimension = cfg["dimension"]
        self.index_type = cfg["index_type"]
        self.metric_type = cfg["metric_type"]
        self.batch_size = cfg["batch_size"]

        self.collection = None
        self.connect()

    def connect(self):
        """Establish connection to Milvus and initialize the collection."""
        try:
            connections.connect(alias="default", host=self.host, port=self.port)
            logger.info(f"✅ Connected to Milvus at {self.host}:{self.port}")
            self._init_collection()
        except Exception as e:
            logger.error(f"❌ Milvus connection error: {e}")
            raise

    def _init_collection(self):
        """Create or load a Milvus collection based on the configured schema."""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.dimension),
            FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="message_id", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="order", dtype=DataType.INT64),
            FieldSchema(name="lang", dtype=DataType.VARCHAR, max_length=8),
        ]
        schema = CollectionSchema(fields, description="Vector collection for RAG")

        try:
            self.collection = Collection(self.collection_name, schema=schema)
            logger.info(f"📦 Milvus collection created: {self.collection_name}")
        except Exception:
            self.collection = Collection(self.collection_name)
            logger.info(f"⚙️ Milvus collection already exists: {self.collection_name}")