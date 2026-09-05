from __future__ import annotations

import json
import os
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from server import create_server


class AcceptanceServerTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["RENDER_GIT_COMMIT"] = "a" * 40
        self.server = create_server("127.0.0.1", 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        os.environ.pop("RENDER_GIT_COMMIT", None)

    def get_json(self, path: str) -> tuple[int, dict[str, str], dict[str, str]]:
        with urlopen(f"{self.base_url}{path}", timeout=2) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            return response.status, json.load(response), headers

    def test_health_is_exact_and_not_cacheable(self) -> None:
        status, payload, headers = self.get_json("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"status": "ok"})
        self.assertEqual(headers["cache-control"], "no-store")
        self.assertEqual(headers["x-content-type-options"], "nosniff")

    def test_version_exposes_only_render_commit(self) -> None:
        status, payload, _ = self.get_json("/version")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"commit": "a" * 40})

    def test_version_rejects_malformed_environment_value(self) -> None:
        os.environ["RENDER_GIT_COMMIT"] = "not-a-commit"
        status, payload, _ = self.get_json("/version")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"commit": "unavailable"})

    def test_unknown_path_is_json_404(self) -> None:
        with self.assertRaises(HTTPError) as raised:
            urlopen(f"{self.base_url}/missing", timeout=2)
        self.assertEqual(raised.exception.code, 404)
        self.assertEqual(json.load(raised.exception), {"error": "not_found"})


if __name__ == "__main__":
    unittest.main()
