
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
from threading import Lock

events = []
events_lock = Lock()
MAX_EVENTS = 100
INGEST_TOKEN = os.environ.get("INGEST_TOKEN", "")


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/events":
            self.send_json(404, {"error": "Not found"})
            return

        with events_lock:
            snapshot = list(events)

        self.send_json(200, snapshot)

    def do_POST(self):
        if self.path != "/ingest":
            self.send_json(404, {"error": "Not found"})
            return

        if not INGEST_TOKEN:
            self.send_json(503, {"error": "Ingestion is not configured"})
            return

        if self.headers.get("Authorization") != f"Bearer {INGEST_TOKEN}":
            self.send_json(401, {"error": "Unauthorized"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 16384:
                self.send_json(413, {"error": "Invalid payload size"})
                return

            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")

            event = {
                "timestamp": str(data.get("timestamp", ""))[:64],
                "event_type": str(data.get("event_type", "unknown"))[:40],
                "alert": str(data.get("alert", ""))[:200],
                "severity": str(data.get("severity", "unknown"))[:30],
                "action": str(data.get("action", "unknown"))[:30]
            }

            with events_lock:
                events.insert(0, event)
                del events[MAX_EVENTS:]

            self.send_json(202, {"accepted": True})

        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid JSON"})

    def log_message(self, format, *args):
        pass


port = int(os.environ.get("PORT", "10000"))
server = HTTPServer(("0.0.0.0", port), Handler)
print(f"SOC API listening on port {port}", flush=True)
server.serve_forever()
