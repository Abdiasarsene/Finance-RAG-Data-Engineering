# src/workers/base_worker.py
import time
import traceback
from abc import ABC, abstractmethod

from rabbitmq.rabbitmq_client import RabbitMQCLient
from metrics.monitoring import increment_messages, observe_processing_time, set_queue_size
from logs.logger import logger


class BaseWorker(ABC):
    """
    Base class for all workers.
    Manages the complete message lifecycle:
        - RabbitMQ connection
        - Message consumption
        - Error handling and retries
        - Logging structured
        - Prometheus metrics
        - Optional message publishing
    """

    input_queue: str = None        # queue to consume from
    output_queue: str = None       # optional queue to publish to
    max_retries: int = 3           # number of automatic retries on failure
    worker_name: str = "BaseWorker"

    def __init__(self, worker_name: str = None):
        if worker_name:
            self.worker_name = worker_name
        self.rabbitmq = RabbitMQCLient()
        if self.input_queue:
            self.rabbitmq.declare_queue(self.input_queue)
        if self.output_queue:
            self.rabbitmq.declare_queue(self.output_queue)

    def start(self):
        """
        Start consuming messages from the input queue.
        """
        if not self.input_queue:
            raise ValueError("input_queue must be defined in the subclass")

        logger.info("Starting worker", worker=self.worker_name, queue=self.input_queue)
        try:
            self.rabbitmq.consume(self.input_queue, self._process_message_wrapper)
        except KeyboardInterrupt:
            logger.info("Worker stopped by user", worker=self.worker_name)
        finally:
            self.rabbitmq.close()

    def _process_message_wrapper(self, msg: dict):
        """
        Wrapper around process_message to handle logging, metrics, retries and publishing.
        """
        retries = 0
        while retries <= self.max_retries:
            start_time = time.time()
            try:
                logger.info("Processing message started", worker=self.worker_name, message_id=msg.get("id"))
                
                # Call the actual processing implemented in the subclass
                result = self.process_message(msg)

                # Success logging + metrics
                duration = time.time() - start_time
                observe_processing_time(self.worker_name, duration)
                increment_messages(self.worker_name, status="success")
                logger.info(
                    "Message processed successfully",
                    worker=self.worker_name,
                    message_id=msg.get("id"),
                    duration=duration
                )

                # Publish to output queue if defined
                if self.output_queue and result is not None:
                    self.rabbitmq.publish(self.output_queue, result)

                break  # success → exit retry loop

            except Exception as e:
                # log the error
                duration = time.time() - start_time
                increment_messages(self.worker_name, status="failure")
                logger.error(
                    "Message processing failed",
                    worker=self.worker_name,
                    message_id=msg.get("id"),
                    error=str(e),
                    traceback=traceback.format_exc(),
                    duration=duration,
                    attempt=retries + 1
                )
                retries += 1
                if retries > self.max_retries:
                    logger.error(
                        "Max retries reached, skipping message",
                        worker=self.worker_name,
                        message_id=msg.get("id")
                    )
                    break
                else:
                    # optional backoff
                    time.sleep(1)

    @abstractmethod
    def process_message(self, msg: dict):
        """
        Actual message processing logic.
        Must be implemented in the subclass.
        """
        pass
