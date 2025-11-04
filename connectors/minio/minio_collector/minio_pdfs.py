# minio.py 
import os
import boto3
from botocore.exceptions import ClientError

# Connect to MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin"
)

# ====== ENSURE BUCKET EXISTS ======
def ensure_bucket_exists(bucket_name):
    """Vérifie si le bucket existe, sinon le crée."""
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3.create_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' created.")
        else:
            print(f"❌ Failed to check/create bucket: {e}")
            raise

# ====== UPLOAD FOLDER ======
def upload_folder(local_folder, bucket, project):
    """_summary_

    Args:
        local_folder (str): local path
        bucket (str): bucket name (ex: raw-pdfs)
        project (str): project name (eg: finance-rag)
    """
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            
            # Key S3 : project/ + chemin relatif
            relative_path = os.path.relpath(local_path, local_folder)
            s3_key = f"{project}/{relative_path}"
            
            # Upload
            s3.upload_file(local_path, bucket, s3_key)

# Using sample
if __name__ == "__main__":
    bucket_name = "raw-pdfs"
    project_name = "finance-rag"
    
    ensure_bucket_exists(bucket_name)
    upload_folder("./data/pdfs", bucket_name, project_name)