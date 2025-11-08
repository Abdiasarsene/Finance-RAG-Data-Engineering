# src/collectors/url_extract.py
import io
import json
import time
from datetime import datetime, timezone
from json_container.schema_loader import load_base_schema
from connectors.minio.minio_connector.minio_connection import MinioConnection
from metrics.monitoring import increment_messages, observe_processing_time, increment_errors
from logs.logger import logger

class UrlExtractor:
    def __init__(self, project_name="finance-rag", bucket_name="raw-urls"):
        self.project_name = project_name
        self.bucket_name = bucket_name
        self.client = MinioConnection().client

    def list_jsons(self):
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket_name)
            json_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(".json")]
            return json_files
        except Exception as e:
            logger.error(
                "Failed to list JSON files",
                worker="url_extract",
                error=str(e),
                bucket=self.bucket_name
            )
            increment_errors(worker="url_extract", error_type=type(e).__name__)
            raise

    def read_json_from_bucket(self, key):
        try:
            obj = self.client.get_object(Bucket=self.bucket_name, Key=key)
            data = json.load(io.BytesIO(obj['Body'].read()))
            return data
        except Exception as e:
            logger.error(
                "Failed to read JSON from bucket",
                worker="url_extract",
                file=key,
                error=str(e)
            )
            increment_errors(worker="url_extract", error_type=type(e).__name__)
            raise

    def json_to_schema(self, file_name, data):
        try:
            schema = load_base_schema()
            
            # Conformité au schéma JSON commun
            schema["source_type"] = "web"
            schema["source_name"] = file_name
            schema["project"] = self.project_name
            schema["date_collected"] = datetime.now(timezone.utc).isoformat()
            schema["raw_content"] = data.get("raw_content", "")  # récupère texte existant ou vide
            # metadata spécifique au web
            schema["metadata"] = {
                "url": data.get("metadata", {}).get("url", ""),
                "title": data.get("metadata", {}).get("title", ""),
                "http_status": data.get("metadata", {}).get("http_status", None)
            }
            return schema
        except Exception as e:
            logger.error(
                "Failed to convert URL JSON to schema",
                worker="url_extract",
                file=file_name,
                error=str(e)
            )
            increment_errors(worker="url_extract", error_type=type(e).__name__)
            raise

    def run(self):
        start_time = time.time()
        try:
            json_files = self.list_jsons()
            all_jsons = []

            for json_name in json_files:
                raw_data = self.read_json_from_bucket(json_name)
                json_doc = self.json_to_schema(json_name, raw_data)
                all_jsons.append(json_doc)

            # Métriques succès global
            duration = time.time() - start_time
            observe_processing_time(worker="url_extract", seconds=duration)
            increment_messages(worker="url_extract", status="success")

            return all_jsons
        except Exception as e:
            logger.error(
                "Unexpected error during URL extraction",
                worker="url_extract",
                error=str(e)
            )
            increment_messages(worker="url_extract", status="error")
            increment_errors(worker="url_extract", error_type=type(e).__name__)
            raise