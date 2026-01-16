from flask import Flask, jsonify, Response
import random
import time, os
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
PHRASE_COUNTER = Counter('phrase_counter', 'Count of each phrase', ['phrase'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Time taken for a request')
PHRASE_SELECTION_LATENCY = Histogram('phrase_selection_latency_seconds', 'Time taken to select the phrase')
FAILED_REQUESTS = Counter('failed_requests', 'Number of failed requests')



API_PORT = os.getenv("API_PORT", "7070")

log_dir = "/logs"
os.makedirs(log_dir, exist_ok=True)

# Configure log file handler
log_file = os.path.join(log_dir, "random_phrase_app.log")
handler = TimedRotatingFileHandler(log_file, when="D", interval=1, backupCount=4)
handler.setLevel(logging.INFO)

# Set log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
handler.setFormatter(formatter)

# Attach handler to Flask app logger
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Redirect Werkzeug logs (Flask's built-in server logs)
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.DEBUG)
werkzeug_logger.addHandler(handler)

# Read phrases from the file and store them in memory
phrases = []
file_path = "phrases.txt"

try:
    logging.info(f"Attempting to read phrases from {file_path}")

    with open(file_path, "r") as file:
        phrases = [line.strip() for line in file]

    logging.info(f"Successfully read {len(phrases)} phrases from {file_path}")

except FileNotFoundError:
    logging.error(f"Error: File {file_path} not found")

except Exception as e:
    logging.error(f"Unexpected error reading {file_path}: {str(e)}")




@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

@app.route('/random_phrase', methods=['GET'])
@REQUEST_LATENCY.time()
def get_random_phrase():
    REQUEST_COUNT.inc()
    try:
        logging.info("Received request for /random_phrase")

        start_time = time.time()
        with PHRASE_SELECTION_LATENCY.time():
            phrase = random.choice(phrases)  # Select random phrase

        PHRASE_COUNTER.labels(phrase=phrase).inc()
        end_time = time.time()
        selection_time = end_time - start_time

        logging.info(f"Selected phrase: '{phrase}' in {selection_time:.6f} seconds")

        return jsonify({
            'phrase': phrase,
            'selection_time': selection_time
        })

    except Exception as e:
        FAILED_REQUESTS.inc()
        logging.error(f"Error in /random_phrase: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=API_PORT)
