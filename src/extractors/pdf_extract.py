# src/collectors/pdf_extract.py
import io
from datetime import datetime, timezone
from pathlib import Path
import PyPDF2
from json_container.schema_loader import load_base_schema
from connectors.minio.minio_connector.minio_connection import MinioConnection
from metrics.monitoring import increment_messages, observe_processing_time, increment_errors
from logs.logger import logger
import time

class PdfExtractor:
    def __init__(self, project_name="finance-rag", bucket_name="raw-pdfs"):
        self.project_name = project_name
        self.bucket_name = bucket_name
        # Prépare le client MinIO (connexion déjà validée en amont)
        self.client = MinioConnection().client

    def list_pdfs(self):
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket_name)
            pdf_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(".pdf")]
            return pdf_files
        except Exception as e:
            logger.error(
                "Failed to list PDFs",
                worker="pdf_extract",
                error=str(e),
                bucket=self.bucket_name
            )
            increment_errors(worker="pdf_extract", error_type=type(e).__name__)
            raise

    def extract_text(self, pdf_bytes):
        try:
            text = ""
            with io.BytesIO(pdf_bytes) as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            logger.error(
                "Text extraction failed",
                worker="pdf_extract",
                error=str(e)
            )
            increment_errors(worker="pdf_extract", error_type=type(e).__name__)
            raise

    def pdf_to_json(self, pdf_name, pdf_bytes):
        try:
            schema = load_base_schema()
            text = self.extract_text(pdf_bytes)
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            
            schema["source_type"] = "pdf"
            schema["source_name"] = pdf_name
            schema["project"] = self.project_name
            schema["date_collected"] = datetime.now(timezone.utc).isoformat()
            schema["raw_content"] = text
            schema["metadata"] = {
                "num_pages": len(reader.pages)
            }
            return schema
        except Exception as e:
            logger.error(
                "Failed to convert PDF to JSON",
                worker="pdf_extract",
                file=pdf_name,
                error=str(e)
            )
            increment_errors(worker="pdf_extract", error_type=type(e).__name__)
            raise

    def run(self):
        start_time = time.time()
        try:
            pdf_files = self.list_pdfs()
            all_jsons = []

            for pdf_name in pdf_files:
                obj = self.client.get_object(Bucket=self.bucket_name, Key=pdf_name)
                pdf_bytes = obj['Body'].read()
                json_doc = self.pdf_to_json(pdf_name, pdf_bytes)
                all_jsons.append(json_doc)

            # METRICS : succès global du run
            duration = time.time() - start_time
            observe_processing_time(worker="pdf_extract", seconds=duration)
            increment_messages(worker="pdf_extract", status="success")

            return all_jsons
        except Exception as e:
            logger.error(
                "Unexpected error during PDF extraction",
                worker="pdf_extract",
                error=str(e)
            )
            increment_messages(worker="pdf_extract", status="error")
            increment_errors(worker="pdf_extract", error_type=type(e).__name__)
            raise