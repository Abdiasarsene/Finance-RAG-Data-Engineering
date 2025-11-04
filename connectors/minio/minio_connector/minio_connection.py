# src/minio_connector/minio_connection.py
import boto3
from botocore.exceptions import ClientError
from utils.config import settings
import logging

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== MINIO CONNECTION ======
class MinioConnection:
    # Set up
    def __init__(self, project_name: str = "finance-rag"):
        self.project_name = project_name
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.minio_tracking,
            aws_access_key_id=settings.minio_id,
            aws_secret_access_key=settings.minio_mdp,
        )
        self.required_buckets = ["raw-urls", "raw-pdfs"]

    # Validate connection
    def validate_connection(self) -> bool:
        try:
            self.client.list_buckets()
            logger.info("MinIO connection established.")
            return True
        except ClientError as e:
            logger.error(f"MinIO connection failed: {e}")
            return False

    # Validate buckets
    def validate_buckets(self) -> bool:
        if not self.validate_connection():
            return False
        try:
            existing_buckets = [b["Name"] for b in self.client.list_buckets()["Buckets"]]
        except ClientError as e:
            logger.error(f"Failed to list buckets: {e}")
            return False

        all_buckets_exist = True
        for bucket in self.required_buckets:
            if bucket not in existing_buckets:
                logger.warning(f"Missing bucket: {bucket}")
                all_buckets_exist = False
            else:
                logger.info(f"Bucket '{bucket}' found.")

        return all_buckets_exist

    # Example for listing bucket objects with prefix
    def list_objects(self, bucket_name: str):
        return self.client.list_objects_v2(Bucket=bucket_name, Prefix=f"{self.project_name}/")