# tests/test_full_pipeline_mock.py
import time
from tests.mocks.mock_services import services
from tests.mocks.mock_base_worker import BaseWorkerMock
from workers.extractor_worker import ExtractDataWorker
from workers.processing_worker import ProcessWorker
from workers.chunking_worker import ChunkerWorker
from workers.embedding_worker import EmbeddingWorker
from tests.mocks.mock_vector_worker import MockVectorStoreWorker

# ========== MOCKED WRAPPERS ==========
class MockExtractDataWorker(BaseWorkerMock, ExtractDataWorker): pass
class MockProcessWorker(BaseWorkerMock, ProcessWorker): pass
class MockChunkerWorker(BaseWorkerMock, ChunkerWorker): pass
class MockEmbeddingWorker(BaseWorkerMock, EmbeddingWorker): pass
class MockVectorWorker(BaseWorkerMock, MockVectorStoreWorker): pass

# ====== GENERIC WRAPPER FOR A PIPELINE STEP ======
def step(worker, msg, publish=True):
    result = worker._process_message_wrapper(msg)
    final_msg = result if result else msg

    if publish and hasattr(worker, "output_queue"):
        services.rabbitmq.publish(worker.output_queue, final_msg)

    print(f"✅ After {worker.worker_name} → {final_msg}\n")
    return final_msg

# ====== SIMULATION OF ALL PIPELINE ======
def run_pipeline_mock():
    print("🚀 Starting FULL PIPELINE (mocked integration test)...\n")

    # Initialize workers
    extract = MockExtractDataWorker()
    process = MockProcessWorker()
    chunker = MockChunkerWorker()
    embed = MockEmbeddingWorker()
    vector = MockVectorWorker()

    # Initial mock message
    raw_message = {
        "id": "doc001",
        "source": "mock_source",
        "text": "Le machine learning transforme la manière dont les entreprises exploitent leurs données.",
        "timestamp": time.time()
    }

    # Inject into first queue
    services.rabbitmq.publish(extract.input_queue, raw_message)
    print(f"📥 Initial message injected into `{extract.input_queue}`: {raw_message}\n")

    # Pipeline Execution
    msg = services.rabbitmq.consume(extract.input_queue)
    msg = step(extract, msg)
    msg = step(process, msg)
    msg = step(chunker, msg)
    msg = step(embed, msg)
    msg = step(vector, msg, publish=False)

    # Summary
    print("\n🧭 Mock System State Summary:")
    print(services.summary())


if __name__ == "__main__":
    start = time.time()
    run_pipeline_mock()
    print(f"\n🏁 Pipeline test completed in {time.time() - start:.2f}s")