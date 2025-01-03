import sys
import threading
import json
import logging
from flask import Flask, jsonify
from kafka import KafkaConsumer
from pymongo import MongoClient
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

app = Flask(__name__)

class KafkaConsumerService:
    def __init__(self):
        # Configure KafkaConsumer with JSON deserialization and a group ID
        self.consumer = KafkaConsumer(
            Config.KAFKA_TOPIC,
            bootstrap_servers=[Config.KAFKA_BOOTSTRAP_SERVERS],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            session_timeout_ms=Config.KAFKA_SESSION_TIMEOUT_MS,
            reconnect_backoff_ms=Config.KAFKA_RECONNECT_BACKOFF_MS,
            api_version_auto_timeout_ms=Config.KAFKA_API_VERSION_AUTO_TIMEOUT_MS
        )
        
        # Set up MongoDB client
        self.mongo_client = MongoClient(Config.MONGO_URI)
        self.db = self.mongo_client["purchases_db"]
        self.collection = self.db["purchases"]

    def consume_messages(self):
        try:
            # Process each message as it's received
            for message in self.consumer:
                purchase_data = message.value
                logger.info(f"Received purchase message: {purchase_data}")
                self.collection.insert_one(purchase_data)
        except Exception as e:
            logger.error(f"Error while consuming messages: {e}")

    def fetch_purchases(self):
        try:
            # Fetch all purchase documents from MongoDB
            return list(self.collection.find({}, {"_id": 0}))  # Exclude ObjectId from output
        except Exception as e:
            logger.error(f"Error fetching purchases: {e}")
            return []

consumer_service = KafkaConsumerService()

@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = consumer_service.fetch_purchases()
    return jsonify(purchases), 200

# Run the Kafka consumer in a separate thread
def run_kafka_consumer():
    consumer_service.consume_messages()

if __name__ == "__main__":
    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=run_kafka_consumer)
    consumer_thread.start()

    # Run Flask app on port 6000
    app.run(host="0.0.0.0", port=6000)
