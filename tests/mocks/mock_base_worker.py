# tests/mocks/mock_base_worker.py
from workers.base_worker import BaseWorker
from tests.mocks.mock_services import services

# ====== MOCK BASE WORK FOR SIMULATION ======
class BaseWorkerMock(BaseWorker):
    input_queue: str = None
    output_queue: str = None
    worker_name: str = "BaseWorkerMock"

    # Set up
    def __init__(self, worker_name: str = None):
        # If a noun is passed, it is used
        if worker_name:
            self.worker_name = worker_name

        # Inject the RabbitMQ mock before any connection attempt
        self.rabbitmq = services.rabbitmq

        # Declares cues to avoid KeyError
        if self.input_queue:
            self.rabbitmq.declare_queue(self.input_queue)
        if self.output_queue:
            self.rabbitmq.declare_queue(self.output_queue)