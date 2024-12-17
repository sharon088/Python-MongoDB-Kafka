import os
from dotenv import load_dotenv

# Load values of .env file.
load_dotenv()

class Config:

    # MongoDB settings
    MONGO_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    # Construct the MongoDB URI using % formatting
    MONGO_URI = 'mongodb://%s:%s@mongodb:27017/' % (MONGO_USERNAME, MONGO_PASSWORD)

    # Kafka settings
    KAFKA_TOPIC = "purchases"
    KAFKA_BOOTSTRAP_SERVERS = "broker:9092"
    KAFKA_SESSION_TIMEOUT_MS = 50000
    KAFKA_RECONNECT_BACKOFF_MS = 5000
    KAFKA_API_VERSION_AUTO_TIMEOUT_MS = 30000
