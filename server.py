from contextlib import closing
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import os
import sqlite3


DATABASE = Path(os.environ.get("DATABASE_PATH", Path(__file__).with_name("team.db")))


def initialize_database():
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    with closing(sqlite3.connect(DATABASE)) as connection:
        connection.executescript(schema)


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
            with closing(sqlite3.connect(DATABASE)) as connection:
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

    def do_POST(self):
        if self.path != "/api/v1/team/members":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self.send_json(415, {"error": "Content-Type must be application/json"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self.send_json(411, {"error": "A valid Content-Length header is required"})
            return

        if content_length < 0:
            self.send_json(400, {"error": "Content-Length cannot be negative"})
            return

        if content_length > 16384:
            self.send_json(413, {"error": "Request body is too large"})
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"error": "Request body must be valid JSON"})
            return

        if not isinstance(payload, dict) or not isinstance(payload.get("name"), str):
            self.send_json(400, {"error": "A member name is required"})
            return

        name = payload["name"].strip()
        if not name or len(name) > 100:
            self.send_json(400, {"error": "Member name must be between 1 and 100 characters"})
            return

        try:
            with closing(sqlite3.connect(DATABASE)) as connection:
                with connection:
                    inserted = connection.execute("""
                        INSERT INTO members (team_id, name)
                        SELECT id, ?
                        FROM teams
                        WHERE name = 'SPŠE Elyta'
                    """, (name,)).rowcount > 0
        except sqlite3.IntegrityError:
            self.send_json(409, {"error": "This member is already in the team"})
            return

        if not inserted:
            self.send_json(404, {"error": "Team not found"})
            return

        self.send_json(201, {"name": name})


port = int(os.environ.get("PORT", "8000"))
initialize_database()
HTTPServer(("0.0.0.0", port), ApiHandler).serve_forever()