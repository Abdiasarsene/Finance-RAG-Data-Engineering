# src/utils/minio-client.py
import boto3
from utils.config import settings

# ====== CLASS CONFIG ======
class MinioClient:
    # Connection to minIO
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.minio_tracking,
            aws_access_key_id=settings.minio_id,
            aws_secret_access_key=settings.minio_mdp
        )
        
        # Buckets and prefixes
        self.buckets = {
            "pdfs":settings.prefix_bucket/settings.bucket1,
            "apis":settings.prefix_bucket/settings.bucket2,
            "urls":settings.prefix_bucket/settings.bucket3
        }

    # Returns a list of bucket_type files: pdfs, apis, urls
    def list_files(self, bucket_type: str):
        if bucket_type not in self.buckets:
            raise ValueError(f"Invalid bucket type: {bucket_type}")
        bucket = self.buckets[bucket_type]

        response = self.client.list_objects_v2(Bucket=bucket)
        return [obj['Key'] for obj in response.get('Contents', [])]

    # Reads the contents of a file from a given bucket_type
    def read_file(self, bucket_type: str, key: str):
        """
        """
        if bucket_type not in self.buckets:
            raise ValueError(f"Invalid bucket type: {bucket_type}")
        bucket = self.buckets[bucket_type]

        response = self.client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()