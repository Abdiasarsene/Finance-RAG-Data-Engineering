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

chunks_generated = Counter(
    "chunks_generated_total",
    "Total number of chunks created by the chunker engine",
    ["worker"]
)

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

errors_total = Counter("worker_errors_total", "Total number of errors", ["worker", "error_type"])
def increment_errors(worker: str, error_type: str = "unknown"):
    errors_total.labels(worker=worker, error_type=error_type).inc()