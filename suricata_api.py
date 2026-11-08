from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

LOG_FILE = "/var/log/suricata/eve.json"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/events":
            self.send_error(404)
            return

        events = []
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                for line in f.readlines()[-50:]:
                    try:
                        event = json.loads(line)
                        events.append({
                            "timestamp": event.get("timestamp"),
                            "event_type": event.get("event_type"),
                            "src_ip": event.get("src_ip"),
                            "dest_ip": event.get("dest_ip"),
                                                        "alert": event.get("alert", {}).get("signature"),
                            "action": event.get("alert", {}).get("action", "unknown"),
                            "severity": event.get("alert", {}).get("severity", "—")
                        })
                    except json.JSONDecodeError:
                        continue
        except OSError:
            self.send_error(500, "Cannot read Suricata log")
            return

        data = json.dumps(events).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass
HTTPServer(("0.0.0.0", 8765), Handler).serve_forever()
