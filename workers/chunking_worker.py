# workers/chunking_worker.py
from workers.base_worker import BaseWorker
from src.chunking.chunker_engine import ChunkerEngine
from src.core.config_loader import load_config
from logs.logger import logger
from metrics.monitoring import increment_chunks

# ====== CHILD WORK - CHUNKERWORKER ======
class ChunkerWorker(BaseWorker):
    input_queue = "processed_messages"    # queue from ProcessWorker
    output_queue = "chunked_messages"     # queue for next step
    worker_name = "ChunkerWorker"

    # Set up
    def __init__(self, config_path="src/chunking/configs/chunker_config.yaml"):
        super().__init__(worker_name=self.worker_name)
        self.config = load_config(config_path)
        self.engine = ChunkerEngine(self.config)

    def process_message(self, msg: dict):
        message_id = msg.get("id")
        text = msg.get("text", "")

        if not text.strip():
            logger.warning("Empty message received for chunking", message_id=message_id)
            return None

        # Chunk via moteur
        chunks = self.engine.chunk(text)

        # Message enrichment
        msg["chunks"] = chunks
        msg["num_chunks"] = len(chunks)

        # Métriques
        increment_chunks(self.worker_name, len(chunks))

        # Returns enriched message for publication
        return msg