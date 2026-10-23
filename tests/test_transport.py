"""默认 HTTP 传输层测试（本地回环服务器，不访问外网）。"""

from __future__ import annotations

import json
import socket
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List

from shuxuntech import ShuxunClient, ShuxunTransportError, sign
from shuxuntech.models import IdCardCheckResult
from shuxuntech.transport import HttpClientTransport


class _Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _Handler)
        self.requests: List[Dict[str, Any]] = []
        self.status = 200
        self.body = b"{}"
        self.content_type = "application/json; charset=utf-8"
        self.delay = 0.0


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self) -> None:  # noqa: N802 - stdlib naming
        server: _Server = self.server  # type: ignore[assignment]
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length)
        server.requests.append(
            {
                "path": self.path,
                "headers": dict(self.headers),
                "body": raw,
            }
        )
        if server.delay:
            time.sleep(server.delay)
        self.send_response(server.status)
        self.send_header("Content-Type", server.content_type)
        self.send_header("Content-Length", str(len(server.body)))
        self.end_headers()
        try:
            self.wfile.write(server.body)
        except (BrokenPipeError, ConnectionResetError):  # pragma: no cover
            pass

    def log_message(self, *args: Any) -> None:
        pass


class TransportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = _Server()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def test_posts_utf8_form_and_preserves_response(self) -> None:
        self.server.body = json.dumps(
            {"code": 0, "msg": "成功", "data": {"name": "张三"}}, ensure_ascii=False
        ).encode("utf-8")
        transport = HttpClientTransport(read_timeout=5)

        response = transport.post(
            f"{self.url}/v1/test?q=1",
            {"appKey": "k", "timestamp": "1", "sign": "s"},
            {"name": "张三", "n": 1},
        )

        self.assertEqual(response.status, 200)
        self.assertIn("张三", response.body)
        self.assertEqual(len(self.server.requests), 1)
        request = self.server.requests[0]
        self.assertEqual(request["path"], "/v1/test?q=1")
        self.assertEqual(
            request["body"],
            "name=%E5%BC%A0%E4%B8%89&n=1".encode("ascii"),
        )
        self.assertTrue(
            request["headers"]["Content-Type"].startswith(
                "application/x-www-form-urlencoded"
            )
        )
        self.assertIn("shuxuntech-python-sdk", request["headers"]["User-Agent"])
        self.assertEqual(request["headers"]["appKey"], "k")

    def test_decodes_gbk_charset(self) -> None:
        self.server.content_type = "application/json; charset=gbk"
        self.server.body = '{"msg":"成功"}'.encode("gbk")
        transport = HttpClientTransport(read_timeout=5)

        response = transport.post(f"{self.url}/v1/test", {}, {})

        self.assertEqual(response.status, 200)
        self.assertIn("成功", response.body)

    def test_preserves_non_2xx_status(self) -> None:
        self.server.status = 400
        self.server.body = b'{"code":1,"msg":"bad request"}'
        transport = HttpClientTransport(read_timeout=5)

        response = transport.post(f"{self.url}/v1/test", {}, {})

        self.assertEqual(response.status, 400)
        self.assertIn("bad request", response.body)

    def test_does_not_follow_redirects(self) -> None:
        self.server.status = 302
        self.server.body = b""
        transport = HttpClientTransport(read_timeout=5)

        response = transport.post(f"{self.url}/v1/test", {}, {})

        self.assertEqual(response.status, 302)
        self.assertEqual(len(self.server.requests), 1)

    def test_read_timeout_raises_transport_error(self) -> None:
        self.server.delay = 2.0
        transport = HttpClientTransport(read_timeout=0.2)

        started = time.monotonic()
        with self.assertRaises(ShuxunTransportError):
            transport.post(f"{self.url}/v1/test", {}, {})
        self.assertLess(time.monotonic() - started, 2.0)

    def test_connection_failure_reports_zero_status(self) -> None:
        probe = socket.socket()
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
        probe.close()

        transport = HttpClientTransport(connect_timeout=1)
        with self.assertRaises(ShuxunTransportError) as ctx:
            transport.post(f"http://127.0.0.1:{port}/v1/test", {}, {})
        self.assertEqual(ctx.exception.http_status, 0)

    def test_invalid_url_rejected(self) -> None:
        transport = HttpClientTransport()
        with self.assertRaises(ShuxunTransportError):
            transport.post("ftp://example.com/x", {}, {})

    def test_timeout_validation(self) -> None:
        with self.assertRaises(ValueError):
            HttpClientTransport(read_timeout=0)
        with self.assertRaises(TypeError):
            HttpClientTransport(connect_timeout="5")  # type: ignore[arg-type]

    def test_repr(self) -> None:
        self.assertIn("HttpClientTransport", repr(HttpClientTransport()))


class ClientOverHttpTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = _Server()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.server.body = json.dumps(
            {"code": 0, "msg": "成功", "seqNo": "seq-http", "data": {"ok": True}}
        ).encode("utf-8")

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def test_end_to_end(self) -> None:
        base_url = f"http://127.0.0.1:{self.server.server_port}"
        with ShuxunClient("app-key", "app-secret", base_url=base_url) as client:
            response = client.post("/v1/idCard/check", {"name": "张三"})

        self.assertTrue(response.is_success)
        self.assertEqual(response.http_status, 200)
        self.assertEqual(response.seq_no, "seq-http")
        self.assertEqual(response.data, {"ok": True})

        request = self.server.requests[0]
        headers = request["headers"]
        self.assertEqual(headers["appKey"], "app-key")
        self.assertEqual(
            headers["sign"],
            sign("app-key", "app-secret", int(headers["timestamp"])),
        )
        self.assertEqual(request["body"], "name=%E5%BC%A0%E4%B8%89".encode("ascii"))

    def test_typed_api_over_http(self) -> None:
        self.server.body = json.dumps(
            {
                "code": 0,
                "msg": "成功",
                "seqNo": "seq-typed",
                "data": {
                    "result": 1,
                    "resultDesc": "核验一致",
                    "birthday": "19930123",
                    "province": "浙江省",
                },
            },
            ensure_ascii=False,
        ).encode("utf-8")
        base_url = f"http://127.0.0.1:{self.server.server_port}"

        with ShuxunClient("app-key", "app-secret", base_url=base_url) as client:
            response = client.apis.identity.id_card_check("张三", "110101")

        self.assertTrue(response.is_success)
        self.assertIsInstance(response.data, IdCardCheckResult)
        assert response.data is not None
        self.assertEqual(response.data.result_desc, "核验一致")
        self.assertEqual(response.data.province, "浙江省")


if __name__ == "__main__":
    unittest.main()
