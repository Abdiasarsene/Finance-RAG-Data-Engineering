# src/workers/process_worker.py
from workers.base_worker import BaseWorker
from src.processing.cleaner import clean_text
from src.processing.deduper import dedupe_document
from src.processing.language_detector import detect_language
from json_container.json_validator import validate_json

# ====== PROCESS WORKER ======
class ProcessWorker(BaseWorker):
    input_queue = "validated_messages"   # queue from CollectDataWorker
    output_queue = "processed_messages"  # queue for the end
    worker_name = "ProcessWorker"

    # Set up
    def __init__(self, dedupe_threshold: float = 0.8):
        super().__init__(worker_name=self.worker_name)
        self.dedupe_threshold = dedupe_threshold

    # Process message
    def process_message(self, msg: dict):
        message_id = msg.get("id")

        # Additional validation if required
        if not validate_json(msg, message_id=message_id):
            return None

        # Clean
        text = clean_text(msg.get("text"), message_id=message_id)

        # Detect language
        lang = detect_language(text, message_id=message_id)
        msg["lang"] = lang

        # Deduper
        deduped_text = dedupe_document(text, message_id=message_id)
        msg["text"] = deduped_text

        # Returns processed message for publication
        return msg