# tests/mocks/mock_minio.py
from io import BytesIO

# ====== MOCK MINIO CLIENT ======
class MockMinIOClient:
    # Set up
    def __init__(self):
        self.storage = {}

    # Put object
    def put_object(self, bucket_name, object_name, data, length):
        if bucket_name not in self.storage:
            self.storage[bucket_name] = {}
        self.storage[bucket_name][object_name] = data.read(length)

    # Get object
    def get_object(self, bucket_name, object_name):
        content = self.storage[bucket_name][object_name]
        return BytesIO(content)

    # Test object
    def list_objects(self, bucket_name, prefix=""):
        if bucket_name not in self.storage:
            return []
        return [
            {"object_name": obj}
            for obj in self.storage[bucket_name]
            if obj.startswith(prefix)
        ]

    # Remove object
    def remove_object(self, bucket_name, object_name):
        del self.storage[bucket_name][object_name]