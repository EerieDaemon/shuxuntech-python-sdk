"""客户端请求、响应解析与异常行为测试。"""

from __future__ import annotations

import json
import time
import unittest
from unittest import mock

from shuxuntech import ApiResponse, ShuxunApiError, ShuxunClient, ShuxunTransportError, sign
from shuxuntech.models import IdCardCheckResult
from shuxuntech.params import Params
from shuxuntech.transport import HttpResponse

from .support import StubTransport, json_response


class ClientRequestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.transport = StubTransport()
        self.client = ShuxunClient(
            "test-app-key",
            "test-app-secret",
            base_url="https://api.example.com",
            transport=self.transport,
        )

    def test_posts_signed_form_and_parses_typed_result(self) -> None:
        self.transport.responses.append(
            json_response(
                {
                    "code": 0,
                    "msg": "成功",
                    "seqNo": "seq-001",
                    "data": {
                        "result": 1,
                        "resultDesc": "核验一致",
                        "birthday": "19930123",
                        "gender": 1,
                        "age": 32,
                        "province": "浙江省",
                    },
                }
            )
        )

        response = self.client.post(
            "/v1/idCard/check",
            {"name": "张三", "idCard": "110101199001011234"},
            IdCardCheckResult,
        )

        self.assertTrue(response.is_success)
        self.assertEqual(response.seq_no, "seq-001")
        self.assertEqual(response.http_status, 200)
        assert response.data is not None
        self.assertEqual(response.data.result, 1)
        self.assertEqual(response.data.province, "浙江省")

        url, headers, form = self.transport.requests[0]
        self.assertEqual(url, "https://api.example.com/v1/idCard/check")
        self.assertEqual(headers["appKey"], "test-app-key")
        timestamp = int(headers["timestamp"])
        self.assertLess(abs(timestamp - int(time.time() * 1000)), 5000)
        self.assertEqual(
            headers["sign"],
            sign("test-app-key", "test-app-secret", timestamp),
        )
        self.assertEqual(form, {"name": "张三", "idCard": "110101199001011234"})

    def test_accepts_params_object_and_none(self) -> None:
        self.transport.responses.append(json_response({"code": 0, "data": {}}))
        self.transport.responses.append(json_response({"code": 0, "data": {}}))

        self.client.post("/v1/x", Params.create().put("flag", True))
        self.client.post("/v1/x", None)

        self.assertEqual(self.transport.requests[0][2], {"flag": "true"})
        self.assertEqual(self.transport.requests[1][2], {})

    def test_builds_url_without_leading_slash(self) -> None:
        self.transport.responses.append(json_response({"code": 0}))
        self.client.post("v1/x")
        self.assertEqual(self.transport.requests[0][0], "https://api.example.com/v1/x")

    def test_strips_trailing_slash_from_base_url(self) -> None:
        transport = StubTransport([json_response({"code": 0})])
        client = ShuxunClient(
            "k", "s", base_url="https://api.example.com/", transport=transport
        )
        client.post("/v1/x")
        self.assertEqual(transport.requests[0][0], "https://api.example.com/v1/x")

    def test_raw_payload_is_exposed(self) -> None:
        payload = {"code": 0, "msg": "成功", "seqNo": "s", "data": {"a": 1}}
        self.transport.responses.append(json_response(payload))
        response = self.client.post("/v1/x")
        self.assertEqual(response.raw, payload)
        self.assertEqual(response.data, {"a": 1})

    def test_business_error_does_not_raise(self) -> None:
        self.transport.responses.append(
            json_response({"code": 2, "msg": "无记录", "seqNo": "seq-002"})
        )
        response = self.client.post("/v1/idCard/check")
        self.assertFalse(response.is_success)
        self.assertEqual(response.code, 2)
        self.assertEqual(response.msg, "无记录")
        self.assertEqual(response.code_description, "无记录")

    def test_post_or_throw_raises_on_business_error(self) -> None:
        self.transport.responses.append(
            json_response({"code": 4, "msg": "签名错误", "seqNo": "seq-003"})
        )
        with self.assertRaises(ShuxunApiError) as ctx:
            self.client.post_or_throw("/v1/idCard/check")
        error = ctx.exception
        self.assertEqual(error.code, 4)
        self.assertEqual(error.msg, "签名错误")
        self.assertEqual(error.seq_no, "seq-003")
        self.assertEqual(error.http_status, 200)
        self.assertIn("签名错误", str(error))

    def test_post_or_throw_missing_code_uses_minus_one(self) -> None:
        self.transport.responses.append(json_response({"msg": "未知"}))
        with self.assertRaises(ShuxunApiError) as ctx:
            self.client.post_or_throw("/v1/x")
        self.assertEqual(ctx.exception.code, -1)

    def test_no_automatic_retry(self) -> None:
        self.transport.responses.append(json_response({"code": 3, "msg": "上游异常"}))
        self.transport.responses.append(json_response({"code": 0}))
        self.client.post("/v1/x")
        self.assertEqual(len(self.transport.requests), 1)


class ClientEnvelopeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.transport = StubTransport()
        self.client = ShuxunClient(
            "k", "s", base_url="https://api.example.com", transport=self.transport
        )

    def test_returns_envelope_on_non_2xx(self) -> None:
        self.transport.responses.append(
            json_response(
                {"code": 1, "msg": "参数错误", "seqNo": "seq-400"}, status=400
            )
        )
        response = self.client.post("/v1/idCard/check", {})
        self.assertFalse(response.is_success)
        self.assertEqual(response.code, 1)
        self.assertEqual(response.http_status, 400)
        self.assertEqual(response.seq_no, "seq-400")

    def test_non_2xx_non_envelope_raises_transport_error(self) -> None:
        self.transport.responses.append(
            HttpResponse(status=502, body="<html>bad gateway</html>")
        )
        with self.assertRaises(ShuxunTransportError) as ctx:
            self.client.post("/v1/x")
        error = ctx.exception
        self.assertEqual(error.http_status, 502)
        self.assertIn("bad gateway", error.response_body or "")
        self.assertIn("502", str(error))

    def test_invalid_json_raises_transport_error(self) -> None:
        self.transport.responses.append(
            HttpResponse(status=200, body="<html>bad gateway</html>")
        )
        with self.assertRaises(ShuxunTransportError) as ctx:
            self.client.post("/v1/x")
        self.assertEqual(ctx.exception.http_status, 200)
        self.assertIn("JSON", str(ctx.exception))

    def test_empty_body_raises_transport_error(self) -> None:
        self.transport.responses.append(HttpResponse(status=200, body="   "))
        with self.assertRaises(ShuxunTransportError) as ctx:
            self.client.post("/v1/x")
        self.assertEqual(ctx.exception.http_status, 200)
        self.assertIn("为空", str(ctx.exception))

    def test_json_array_is_not_platform_envelope(self) -> None:
        self.transport.responses.append(HttpResponse(status=200, body="[1, 2]"))
        with self.assertRaises(ShuxunTransportError):
            self.client.post("/v1/x")

    def test_missing_code_on_2xx_returns_envelope(self) -> None:
        self.transport.responses.append(json_response({"msg": "无 code", "data": {"a": 1}}))
        response = self.client.post("/v1/x")
        self.assertFalse(response.is_success)
        self.assertIsNone(response.code)
        self.assertEqual(response.data, {"a": 1})
        self.assertEqual(response.http_status, 200)

    def test_numeric_string_code_is_coerced(self) -> None:
        self.transport.responses.append(json_response({"code": "0", "msg": "成功"}))
        response = self.client.post("/v1/x")
        self.assertTrue(response.is_success)
        self.assertEqual(response.code, 0)

    def test_data_mapping_failure_raises_transport_error(self) -> None:
        self.transport.responses.append(json_response({"code": 0, "data": "oops"}))
        with self.assertRaises(ShuxunTransportError) as ctx:
            self.client.post("/v1/x", None, IdCardCheckResult)
        self.assertIn("IdCardCheckResult", str(ctx.exception))

    def test_result_type_must_be_model(self) -> None:
        with self.assertRaises(TypeError):
            self.client.post("/v1/x", None, dict)  # type: ignore[arg-type]

    def test_invalid_path_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.client.post("")
        with self.assertRaises(ValueError):
            self.client.post("   ")


class ClientConfigurationTest(unittest.TestCase):
    def test_requires_credentials(self) -> None:
        with self.assertRaises(ValueError):
            ShuxunClient("", "secret")
        with self.assertRaises(ValueError):
            ShuxunClient("key", "  ")

    def test_rejects_invalid_base_url(self) -> None:
        with self.assertRaises(ValueError):
            ShuxunClient("k", "s", base_url="ftp://api.example.com")
        with self.assertRaises(ValueError):
            ShuxunClient("k", "s", base_url="api.example.com")

    def test_rejects_invalid_timeouts(self) -> None:
        with self.assertRaises(ValueError):
            ShuxunClient("k", "s", read_timeout=0)
        with self.assertRaises(TypeError):
            ShuxunClient("k", "s", connect_timeout="5")  # type: ignore[arg-type]

    def test_properties_and_repr(self) -> None:
        transport = StubTransport()
        client = ShuxunClient("key", "secret", transport=transport)
        self.assertEqual(client.app_key, "key")
        self.assertEqual(client.base_url, "https://api.shuxuntech.com")
        self.assertIn("key", repr(client))
        self.assertNotIn("secret", repr(client))

    def test_create_classmethod(self) -> None:
        transport = StubTransport()
        client = ShuxunClient.create("key", "secret", transport=transport)
        self.assertIsInstance(client, ShuxunClient)
        self.assertEqual(client.base_url, "https://api.shuxuntech.com")

    def test_does_not_close_injected_transport(self) -> None:
        transport = StubTransport()
        with ShuxunClient("k", "s", transport=transport):
            pass
        self.assertFalse(transport.closed)

    def test_closes_owned_transport(self) -> None:
        fake = mock.Mock()
        fake.closed = False
        with mock.patch("shuxuntech.client.HttpClientTransport", return_value=fake):
            client = ShuxunClient("k", "s")
            client.close()
        fake.close.assert_called_once()

    def test_client_is_context_manager(self) -> None:
        transport = StubTransport()
        with ShuxunClient("k", "s", transport=transport) as client:
            self.assertIsInstance(client, ShuxunClient)

    def test_apis_exposes_all_categories(self) -> None:
        transport = StubTransport()
        client = ShuxunClient("k", "s", transport=transport)
        for name in (
            "identity",
            "mobile",
            "bankcard",
            "ocr",
            "enterprise",
            "vehicle",
            "express",
            "ip",
        ):
            self.assertTrue(hasattr(client.apis, name), name)


class ApiResponseConstructionTest(unittest.TestCase):
    def test_defaults(self) -> None:
        response: ApiResponse[object] = ApiResponse()
        self.assertIsNone(response.code)
        self.assertFalse(response.is_success)
        self.assertEqual(response.http_status, 0)
        self.assertEqual(response.raw, {})

    def test_json_payload_is_serialisable(self) -> None:
        payload = {"code": 0, "data": {"中文": "值"}}
        self.assertEqual(json.loads(json.dumps(payload)), payload)


if __name__ == "__main__":
    unittest.main()
