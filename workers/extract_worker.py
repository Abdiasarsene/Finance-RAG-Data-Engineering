# src/workers/extract_worker.py
from workers.base_worker import BaseWorker
from src.extract_data.pdf_extract import PdfExtractor
from src.extract_data.url_extract import UrlExtractor
from src.minio_connector.bucket_manager import BucketManager
from json_container.json_validator import validate_json

class ExtractDataWorker(BaseWorker):
    input_queue = "raw_messages"           # Queue déclencheuse
    output_queue = "validated_messages"    # Queue pour ProcessWorker
    worker_name = "ExtractDataWorker"

    def __init__(self, processed_bucket="processed-jsons"):
        super().__init__(worker_name=self.worker_name)
        self.processed_bucket = processed_bucket
        self.bucket_manager = BucketManager()
        # Initialiser les extracteurs
        self.pdf_extractor = PdfExtractor(project_name="finance-rag", bucket_name="raw-pdfs")
        self.url_extractor = UrlExtractor(project_name="finance-rag", bucket_name="raw-urls")

    def process_message(self, msg: dict):
        processed_files = []

        # --- 1️⃣ Extraction PDFs ---
        for pdf_name, pdf_bytes in self.pdf_extractor.list_pdfs():
            try:
                json_data = self.pdf_extractor.pdf_to_json(pdf_name, pdf_bytes)
                self.bucket_manager.upload_json(self.processed_bucket, f"{pdf_name}.json", json_data)
                validate_json(json_data, message_id=pdf_name)
                processed_files.append(pdf_name)
            except Exception as e:
                # Les logs et métriques sont gérés dans PdfExtractor et monitoring.py
                continue

        # --- 2️⃣ Extraction URLs ---
        for url_name, url_bytes in self.url_extractor.list_urls():
            try:
                json_data = self.url_extractor.url_to_json(url_name, url_bytes)
                self.bucket_manager.upload_json(self.processed_bucket, f"{url_name}.json", json_data)
                validate_json(json_data, message_id=url_name)
                processed_files.append(url_name)
            except Exception as e:
                # Les logs et métriques sont gérés dans UrlExtractor et monitoring.py
                continue

        # --- 3️⃣ Retour pour le pipeline ---
        return {
            "status": "extraction_done",
            "processed_files": processed_files,
            "bucket": self.processed_bucket
        }