from flask import Flask
from prometheus_client import start_http_server, Counter, Gauge, Histogram
import random
import time
import argparse

app = Flask(__name__)

# Licznik zapytań HTTP
http_requests_total = Counter('http_requests_total', 'Total number of HTTP requests')

# Licznik błędnych zapytań HTTP
http_requests_failed_total = Counter('http_requests_failed_total', 'Total number of failed HTTP requests')

# Gauge dla symulowanego użycia CPU
cpu_usage_gauge = Gauge('cpu_usage_percentage', 'Simulated CPU usage percentage')

# Histogram dla czasu odpowiedzi na zapytania
http_request_duration_seconds = Histogram('http_request_duration_seconds', 'Histogram of HTTP request durations')

# Gauge dla symulowanego zużycia pamięci RAM
memory_usage_gauge = Gauge('memory_usage_bytes', 'Simulated memory usage in bytes')

import threading

def simulate_metrics():
    while True:
        http_requests_total.inc()
        if random.random() < 0.1:
            http_requests_failed_total.inc()
        cpu_usage_gauge.set(random.randint(10, 100))
        memory_usage_gauge.set(random.randint(1, 8) * 1024**3)
        with http_request_duration_seconds.time():
            time.sleep(random.uniform(0.1, 1))
        time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--metrics-port', type=int, default=8080)
    args = parser.parse_args()

    # Start metrics HTTP server
    start_http_server(args.metrics_port)

    # Start background metrics simulation
    threading.Thread(target=simulate_metrics, daemon=True).start()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)


