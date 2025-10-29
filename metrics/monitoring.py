# metrics/monitoring.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# ====== GENERIC METRICS ======
messages_processed = Counter(
    "worker_messages_total",
    "Total number of worker messages",
    ["worker", "status"]
)

processing_time = Histogram(
    "worker_processing_seconds",
    "Time spent processing messages by worker",
    ["worker"]
)

queue_size = Gauge(
    "queue_size",
    "Current size of the queue",
    ["queue"]
)

# ====== CHUNK STEP ======
chunks_generated = Counter(
    "chunks_generated_total",
    "Total number of chunks created by the chunker engine",
    ["worker"]
)

# ====== EMBEDDING STEP ======
embedding_chunks_processed = Counter(
    "embedding_chunks_processed_total",
    "Total number of chunks embedded by worker",
    ["worker"]
)

embedding_vectors_generated = Gauge(
    "embedding_vectors_generated",
    "Current number of vectors generated per worker",
    ["worker"]
)

embedding_processing_seconds = Histogram(
    "embedding_processing_seconds",
    "Time spent embedding chunks by worker",
    ["worker"]
)

embedding_errors_total = Counter(
    "embedding_errors_total",
    "Total number of errors during embedding",
    ["worker", "error_type"]
)

# ====== VECTOR STORE METRICS ======
vectors_inserted_total = Counter(
    "vectors_inserted_total",
    "Total number of vectors successfully inserted in the vector store",
    ["worker"]
)

vector_store_insert_errors_total = Counter(
    "vector_store_insert_errors_total",
    "Total number of errors during vector store insertion",
    ["worker", "error_type"]
)

vector_store_insert_time_seconds = Histogram(
    "vector_store_insert_time_seconds",
    "Time spent inserting vectors into the vector store",
    ["worker"]
)

vector_store_queue_size = Gauge(
    "vector_store_queue_size",
    "Current size of the queue waiting to be inserted into the vector store",
    ["worker"]
)

vector_store_current_count = Gauge(
    "vector_store_current_count",
    "Current number of vectors in the vector store collection",
    ["worker"]
)

# ====== INIT SERVER ======
def init_monitoring(port: int = 8000, addr: str = "0.0.0.0"):
    start_http_server(port, addr=addr)
    print(f"✅ Prometheus metrics server started on {addr}:{port}")

# ====== HELPER FUNCTIONS FOR WORKERS ======
def increment_messages(worker: str, status: str = "success"):
    messages_processed.labels(worker=worker, status=status).inc()

def observe_processing_time(worker: str, seconds: float):
    processing_time.labels(worker=worker).observe(seconds)

def set_queue_size(queue_name: str, size: int):
    queue_size.labels(queue=queue_name).set(size)

def increment_chunks(worker: str, count: int):
    chunks_generated.labels(worker=worker).inc(count)

def increment_embedding_chunks(worker: str, count: int):
    embedding_chunks_processed.labels(worker=worker).inc(count)

def set_embedding_vectors(worker: str, count: int):
    embedding_vectors_generated.labels(worker=worker).set(count)

def observe_embedding_time(worker: str, seconds: float):
    embedding_processing_seconds.labels(worker=worker).observe(seconds)

def increment_embedding_errors(worker: str, error_type: str = "unknown"):
    embedding_errors_total.labels(worker=worker, error_type=error_type).inc()

def increment_vectors_inserted(worker: str, count: int):
    vectors_inserted_total.labels(worker=worker).inc(count)

def increment_vector_store_errors(worker: str, error_type: str = "unknown"):
    vector_store_insert_errors_total.labels(worker=worker, error_type=error_type).inc()

def observe_vector_store_insert_time(worker: str, seconds: float):
    vector_store_insert_time_seconds.labels(worker=worker).observe(seconds)

def set_vector_store_queue_size(worker: str, size: int):
    vector_store_queue_size.labels(worker=worker).set(size)

def set_vector_store_current_count(worker: str, count: int):
    vector_store_current_count.labels(worker=worker).set(count)


# ====== GENERIC ERROR HANDLING ======
errors_total = Counter(
    "worker_errors_total",
    "Total number of errors",
    ["worker", "error_type"]
)

def increment_errors(worker: str, error_type: str = "unknown"):
    errors_total.labels(worker=worker, error_type=error_type).inc()
