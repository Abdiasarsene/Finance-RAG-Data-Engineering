"""
Manual test for verifying a real Milvus connection (Docker instance).
Run this file directly:  python tests/manual_test_milvus_connection.py
"""

from connectors.milvus.milvus_connection import MilvusConnection
from pymilvus import connections, list_collections
import sys
import time


def main():
    print("🔍 Testing real Milvus connection...\n")

    try:
        # --- 1. Initialize connection ---
        milvus = MilvusConnection()
        assert connections.has_connection("default"), "No active Milvus connection"
        print(f"✅ Connected successfully to Milvus at {milvus.host}:{milvus.port}")

        # --- 2. Wait a bit for collection registration ---
        time.sleep(1)
        collections = list_collections()
        if milvus.collection_name in collections:
            print(f"📦 Collection '{milvus.collection_name}' detected.")
        else:
            print(f"⚠️ Collection '{milvus.collection_name}' not found yet. Retrying...")
            time.sleep(1)
            collections = list_collections()
            if milvus.collection_name in collections:
                print(f"📦 Collection '{milvus.collection_name}' found after retry.")
            else:
                raise RuntimeError("❌ Collection not created in Milvus")

        # --- 3. Inspect schema briefly ---
        print("\n🧱 Collection Schema:")
        for field in milvus.collection.schema.fields:
            print(f"  - {field.name} ({field.dtype})", "(Primary Key)" if field.is_primary else "")

        # --- 4. Drop for cleanup (optional) ---
        # utility.drop_collection(milvus.collection_name)
        # print(f"\n🧹 Collection '{milvus.collection_name}' dropped after test.")

        print("\n🎯 Test completed successfully.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
