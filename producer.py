from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaProducerService:
    def __init__(self):
        # Configure the Kafka producer with JSON serialization
        self.producer = KafkaProducer(
            bootstrap_servers=[Config.KAFKA_BOOTSTRAP_SERVERS],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            reconnect_backoff_ms=Config.KAFKA_RECONNECT_BACKOFF_MS,
            api_version_auto_timeout_ms=Config.KAFKA_API_VERSION_AUTO_TIMEOUT_MS
        )

    def send_purchase(self, purchase_data):
        try:
            # Send the purchase data asynchronously and add callback for success/error
            future = self.producer.send(Config.KAFKA_TOPIC, key=b'buy_item', value=purchase_data)
            
            # Handle success or failure
            future.add_callback(self.on_send_success)
            future.add_errback(self.on_send_error)

            # Ensure all messages are sent before finishing
            self.producer.flush()
        except KafkaError as e:
            logger.error(f"Failed to send message to Kafka: {e}")
            raise Exception("Kafka producer error occurred")

    def on_send_success(self, record_metadata):
        logger.info(f"Message sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

    def on_send_error(self, excp):
        logger.error("Failed to send message", exc_info=excp)
