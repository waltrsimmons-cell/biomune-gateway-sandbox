"""Credential-free Render target used only for BIOMUNE hosted acceptance."""

from __future__ import annotations

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class AcceptanceHandler(BaseHTTPRequestHandler):
    server_version = "BIOMUNE"
    sys_version = ""

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path == "/healthz":
            self._write_json(200, {"status": "ok"})
            return
        if self.path == "/version":
            commit = os.environ.get("RENDER_GIT_COMMIT", "")
            self._write_json(
                200,
                {"commit": commit if COMMIT_PATTERN.fullmatch(commit) else "unavailable"},
            )
            return
        self._write_json(404, {"error": "not_found"})

    def _write_json(self, status: int, payload: dict[str, str]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(host: str, port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), AcceptanceHandler)


def main() -> None:
    port = int(os.environ.get("PORT", "10000"))
    with create_server("0.0.0.0", port) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
