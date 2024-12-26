from flask import Flask, jsonify, request, render_template, session
import sys
import datetime
import secrets
import requests
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves
from producer import KafkaProducerService
from config import Config

app = Flask(__name__)  # Create a Flask instance
app.config.from_object(Config)
app.secret_key = secrets.token_hex(16)

# Initialize Kafka Producer
kafka_producer = KafkaProducerService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get("username")
        if username:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({"status": "success", "message": "Logged in successfully!"}), 200
        return jsonify({"status": "error", "message": "Invalid login credentials"}), 400
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred"}), 500

@app.route('/buy', methods=['POST'])
def buy_item():
    try:
        if not session.get('logged_in'):
            return jsonify({"status": "error", "message": "User not logged in"}), 403

        item_id = request.json.get("itemID")
        timestamp = request.json.get("timestamp")

        if not item_id or not timestamp:
            return jsonify({"status": "error", "message": "Missing itemID or timestamp"}), 400

        purchase_data = {
            "username": session.get('username'),
            "item_id": item_id,
            "timestamp": timestamp,
        }

        # Send purchase data to Kafka
        kafka_producer.send_purchase(purchase_data)
        return jsonify({"status": "success", "message": "Item bought successfully!"}), 200
    except Exception as e:
        logger.error(f"Error during purchase: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred"}), 500

@app.route('/purchases', methods=['GET'])
def get_purchases():
    try:
        # Call the consumer service API to get purchase data
        response = requests.get("http://consumer:6000/purchases")
        response.raise_for_status()  # Will raise an error if the request fails
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching purchases: {e}")
        return jsonify({"status": "error", "message": "Unable to fetch purchase data"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clears the session
    return jsonify({"status": "success", "message": "Logged out successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
