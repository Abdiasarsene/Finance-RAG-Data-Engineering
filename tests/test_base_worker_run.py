# tests/integration/test_workers_run.py

import time
from tests.mocks.mock_services import services

# 🔧 Patch global de RabbitMQClient avant l'import de BaseWorker
import workers.base_worker
workers.base_worker.RabbitMQCLient = lambda *a, **kw: services.rabbitmq

from workers.base_worker import BaseWorker

# -------------------------------
# Worker minimal pour test BaseWorker
# -------------------------------
class DummyWorker(BaseWorker):
    input_queue = "input_queue"
    output_queue = "output_queue"
    worker_name = "DummyWorker"

    def __init__(self, should_fail=False):
        super().__init__(worker_name=self.worker_name)

        # S'assurer que les queues existent dans le mock
        self.rabbitmq.declare_queue(self.input_queue)
        self.rabbitmq.declare_queue(self.output_queue)

        self.should_fail = should_fail

    def process_message(self, msg: dict):
        if self.should_fail:
            raise ValueError("Simulated processing error")
        return {"processed": True, "original": msg}

# -------------------------------
# Test d'intégration isolé
# -------------------------------
def run_baseworker_test():
    print("🚀 Starting BaseWorker isolated integration test...\n")

    # Mode succès
    worker = DummyWorker()
    mock_msg = {"id": "msg001", "content": "Hello BaseWorker"}
    services.rabbitmq.publish(worker.input_queue, mock_msg)
    print(f"📥 Published message: {mock_msg}")

    # Traitement via BaseWorker
    msg = services.rabbitmq.consume(worker.input_queue)
    worker._process_message_wrapper(msg)

    # Vérification sortie
    result = services.rabbitmq.consume(worker.output_queue)
    print(f"\n✅ Output message from BaseWorker: {result}")

    # État mocks
    print("\n🧭 Mock state summary:")
    print(services.summary())

    # Mode erreur / retry
    print("\n🚧 Testing retry/error handling...\n")
    failing_worker = DummyWorker(should_fail=True)
    failing_worker._process_message_wrapper({"id": "msg_fail", "content": "This should fail"})


if __name__ == "__main__":
    start = time.time()
    run_baseworker_test()
    print(f"\n✅ Test finished in {time.time() - start:.2f}s")