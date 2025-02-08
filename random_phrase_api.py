from flask import Flask, jsonify, Response
import random
import time, os
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

app = Flask(__name__)

API_PORT = os.getenv("API_PORT", "6061")

# Read phrases from the file and store them in memory
with open('phrases.txt', 'r') as file:
    phrases = [line.strip() for line in file]

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
PHRASE_COUNTER = Counter('phrase_counter', 'Count of each phrase', ['phrase'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Time taken for a request')
PHRASE_SELECTION_LATENCY = Histogram('phrase_selection_latency_seconds', 'Time taken to select the phrase')
FAILED_REQUESTS = Counter('failed_requests', 'Number of failed requests')

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

@app.route('/random_phrase', methods=['GET'])
@REQUEST_LATENCY.time()
def get_random_phrase():
    REQUEST_COUNT.inc()
    try:
        start_time = time.time()
        with PHRASE_SELECTION_LATENCY.time():
            phrase = random.choice(phrases)
        PHRASE_COUNTER.labels(phrase=phrase).inc()
        end_time = time.time()

        return jsonify({
            'phrase': phrase,
            'selection_time': end_time - start_time
        })
    except Exception as e:
        FAILED_REQUESTS.inc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=API_PORT)
