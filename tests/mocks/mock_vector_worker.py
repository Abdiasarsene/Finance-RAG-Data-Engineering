# tests/mocks/mock_vector_worker.py
from workers.vectorstore_worker import VectorStoreWorker
from tests.mocks.mock_services import services
from logs.logger import logger
from datetime import datetime

# ====== MOCK VECTORSTORE WORKER ======
class MockVectorStoreWorker(VectorStoreWorker):
    # Set up
    def __init__(self):
        super().__init__()

        # Replace true connexion by the mock
        self.milvus_conn = services.milvus
        logger.info("🧠 [MockVectorStoreWorker] Using services.milvus (mocked Milvus)")

    # Procees message
    def process_message(self, msg: dict):
        embeddings = msg.get("embeddings", [])
        if not embeddings:
            logger.warning("⚠️ [MockVectorStoreWorker] No embeddings found in message")
            return None

        # Inserts in the Milvus mock via MockServices
        metadata = [{"id": msg.get("id"), "timestamp": msg.get("timestamp")} for _ in embeddings]
        self.milvus_conn.insert(embeddings, metadata)

        # Adds a flag for the test
        msg["mock_vectorstore_status"] = f"{len(embeddings)} embeddings stored (mock)"
        msg["stored_at"] = datetime.utcnow().isoformat()

        logger.info(f"✅ [MockVectorStoreWorker] Mock stored {len(embeddings)} embeddings successfully")
        return msg