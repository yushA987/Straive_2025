from flask import Flask, jsonify
import redis
import logging

# ----------------------------
#  Flask and Redis Setup
# ----------------------------
app = Flask(__name__)

# Connect to Redis (adjust host/port if needed)
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()  # Test connection
    print(" Connected to Redis successfully!")
except redis.ConnectionError:
    print(" Failed to connect to Redis. Make sure the server is running.")


# ----------------------------
#  Logging Configuration
# ----------------------------
logging.basicConfig(
    filename="flask_redis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def home():
    """Home route showing basic info."""
    return jsonify(message="Welcome to Flask + Redis Example!", endpoints=["/set/<key>/<value>", "/get/<key>", "/visits"])


@app.route('/set/<key>/<value>')
def set_value(key, value):
    """Set a key-value pair in Redis."""
    try:
        r.set(key, value)
        logging.info(f"Key set: {key} -> {value}")
        return jsonify(status="success", message=f"Stored {key} = {value} in Redis")
    except Exception as e:
        logging.error(f"Error setting value: {e}")
        return jsonify(status="error", message=str(e)), 500


@app.route('/get/<key>')
def get_value(key):
    """Get a value from Redis."""
    try:
        value = r.get(key)
        if value:
            value = value.decode('utf-8')
            logging.info(f"Key fetched: {key} -> {value}")
            return jsonify(status="success", key=key, value=value)
        else:
            return jsonify(status="error", message=f"Key '{key}' not found"), 404
    except Exception as e:
        logging.error(f"Error fetching value: {e}")
        return jsonify(status="error", message=str(e)), 500


@app.route('/visits')
def visit_counter():
    """Count how many times this endpoint was accessed."""
    try:
        visits = r.incr('visit_count')
        logging.info(f"Visit count updated: {visits}")
        return jsonify(message="Page visit counter", total_visits=visits)
    except Exception as e:
        logging.error(f"Error updating visit count: {e}")
        return jsonify(status="error", message=str(e)), 500


# ----------------------------
# Run the Flask App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)