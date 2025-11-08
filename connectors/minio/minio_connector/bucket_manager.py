# src/utils/bucket_manager.py
import json
from connectors.minio.minio_connector.minio_connection import MinioConnection
from metrics.monitoring import increment_errors
from logs.logger import logger

# ====== BUCKET MANAGER ======
class BucketManager:
    # Set up
    def __init__(self):
        self.client = MinioConnection().client

    # Create bucket
    def create_bucket(self, bucket_name: str):
        try:
            existing_buckets = [b['Name'] for b in self.client.list_buckets().get('Buckets', [])]
            if bucket_name in existing_buckets:
                logger.info(f"Bucket '{bucket_name}' already exists.")
                return True
            self.client.create_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully.")
            return True
        except Exception as e:
            logger.error(
                "Failed to create bucket",
                bucket=bucket_name,
                error=str(e)
            )
            increment_errors(worker="bucket_manager", error_type=type(e).__name__)
            return False

    # Upload json
    def upload_json(self, bucket_name: str, file_name: str, data: dict):
        try:
            json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json_bytes,
                ContentType="application/json"
            )
            return True
        except Exception as e:
            logger.error(
                "Failed to upload JSON",
                bucket=bucket_name,
                file=file_name,
                error=str(e)
            )
            increment_errors(worker="bucket_manager", error_type=type(e).__name__)
            return False