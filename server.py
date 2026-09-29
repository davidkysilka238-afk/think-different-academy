from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import os
import sqlite3


class ApiHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        static_files = Path(__file__).with_name("dist")
        super().__init__(*args, directory=str(static_files), **kwargs)

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/v1/health":
            self.send_json(200, {"status": "ok"})
            return

        if self.path == "/api/v1/team":
            database = Path(__file__).with_name("team.db")
            with sqlite3.connect(database) as connection:
                rows = connection.execute("""
                    SELECT teams.name, members.name
                    FROM teams
                    JOIN members ON members.team_id = teams.id
                    ORDER BY members.id
                """).fetchall()

            if not rows:
                self.send_json(404, {"error": "Team not found"})
                return

            self.send_json(200, {
                "team": rows[0][0],
                "members": [row[1] for row in rows],
            })
            return

        super().do_GET()


port = int(os.environ.get("PORT", "8000"))
HTTPServer(("0.0.0.0", port), ApiHandler).serve_forever()