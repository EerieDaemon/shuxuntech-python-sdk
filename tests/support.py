"""Shared test helpers."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping, Optional, Tuple

from shuxuntech import ApiResponse, ShuxunClient
from shuxuntech.transport import HttpTransport, HttpResponse


class StubTransport(HttpTransport):
    """Records requests and replays prepared responses."""

    def __init__(self, responses: Optional[List[HttpResponse]] = None) -> None:
        self.responses: List[HttpResponse] = list(responses or [])
        self.requests: List[Tuple[str, Dict[str, str], Dict[str, str]]] = []
        self.closed = False

    def post(
        self,
        url: str,
        headers: Mapping[str, str],
        form: Mapping[str, str],
    ) -> HttpResponse:
        self.requests.append((url, dict(headers), dict(form)))
        if not self.responses:
            raise AssertionError("没有预置响应")
        return self.responses.pop(0)

    def close(self) -> None:
        self.closed = True


def json_response(payload: Any, status: int = 200) -> HttpResponse:
    return HttpResponse(
        status=status,
        body=json.dumps(payload, ensure_ascii=False),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )


def make_client(
    transport: HttpTransport,
    *,
    base_url: str = "https://api.example.com",
) -> ShuxunClient:
    return ShuxunClient(
        "test-app-key",
        "test-app-secret",
        base_url=base_url,
        transport=transport,
    )


class RecordingClient:
    """Minimal stand-in for ShuxunClient used by API wrapper tests."""

    def __init__(self) -> None:
        self.calls: List[Tuple[str, Dict[str, str], Any]] = []

    def post(
        self,
        path: str,
        params: Any = None,
        result_type: Any = None,
    ) -> ApiResponse[Any]:
        form = params.as_dict() if hasattr(params, "as_dict") else dict(params or {})
        self.calls.append((path, form, result_type))
        return ApiResponse(code=0, msg="成功", data=None, http_status=200)
