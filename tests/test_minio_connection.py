# tests/test_minio_connection.py
from src.minio_connector.minio_connection import MinioConnection

# Test
def test_minio_connect():
    conn = MinioConnection()
    assert conn.validate_connection() is True
    assert conn.validate_buckets() is True