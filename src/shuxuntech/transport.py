"""HTTP 传输层抽象与默认实现。

默认实现只依赖 Python 标准库（``http.client``），不引入第三方依赖。
需要接入自定义代理、链路追踪或测试替身时，实现 :class:`HttpTransport`
并通过 ``ShuxunClient(..., transport=...)`` 注入。
"""

from __future__ import annotations

import http.client
import ssl
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping
from urllib.parse import quote_plus, urlencode, urlsplit

from ._version import __version__
from .exceptions import ShuxunTransportError

__all__ = ["HttpClientTransport", "HttpResponse", "HttpTransport"]

_CONTENT_TYPE = "application/x-www-form-urlencoded; charset=utf-8"


@dataclass(frozen=True)
class HttpResponse:
    """传输层返回的原始响应。"""

    status: int
    body: str
    headers: Mapping[str, str] = field(default_factory=dict)


class HttpTransport(ABC):
    """HTTP 传输层接口。

    实现类只需提供同步的 :meth:`post`；SDK 不会自动重试。
    """

    @abstractmethod
    def post(
        self,
        url: str,
        headers: Mapping[str, str],
        form: Mapping[str, str],
    ) -> HttpResponse:
        """以 ``application/x-www-form-urlencoded`` 方式提交 POST 请求。

        :param url: 完整请求地址
        :param headers: 请求头，含 appKey / timestamp / sign
        :param form: 表单参数
        :return: 原始响应
        :raises ShuxunTransportError: 网络或 IO 失败
        """
        raise NotImplementedError

    def close(self) -> None:
        """释放连接资源，默认无需处理。"""


def _check_timeout(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} 必须是数字")
    if value <= 0:
        raise ValueError(f"{name} 必须大于 0")
    return float(value)


class HttpClientTransport(HttpTransport):
    """基于标准库 ``http.client`` 的默认传输实现。

    每个请求新建一条连接，不自动重试，也不跟随重定向：平台的每次调用通常按次
    计费，是否重试应由业务决定。

    :param connect_timeout: 建连超时，默认 5 秒
    :param read_timeout: 读取超时，默认 15 秒
    :param write_timeout: 写入超时，默认 15 秒
    """

    def __init__(
        self,
        connect_timeout: float = 5.0,
        read_timeout: float = 15.0,
        write_timeout: float = 15.0,
    ) -> None:
        self._connect_timeout = _check_timeout(connect_timeout, "connect_timeout")
        self._read_timeout = _check_timeout(read_timeout, "read_timeout")
        self._write_timeout = _check_timeout(write_timeout, "write_timeout")
        self._ssl_context = ssl.create_default_context()

    def post(
        self,
        url: str,
        headers: Mapping[str, str],
        form: Mapping[str, str],
    ) -> HttpResponse:
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise ShuxunTransportError(f"无效的请求地址: {url}")
        if parts.scheme == "https":
            connection: http.client.HTTPConnection = http.client.HTTPSConnection(
                parts.hostname,
                parts.port,
                timeout=self._connect_timeout,
                context=self._ssl_context,
            )
        else:
            connection = http.client.HTTPConnection(
                parts.hostname,
                parts.port,
                timeout=self._connect_timeout,
            )

        target = parts.path or "/"
        if parts.query:
            target = f"{target}?{parts.query}"
        body = urlencode(dict(form), quote_via=quote_plus).encode("utf-8")
        request_headers: Dict[str, str] = {
            "Content-Type": _CONTENT_TYPE,
            "Accept": "application/json",
            "User-Agent": f"shuxuntech-python-sdk/{__version__}",
        }
        request_headers.update(headers)

        try:
            try:
                connection.connect()
            except (OSError, http.client.HTTPException) as exc:
                raise ShuxunTransportError(f"连接 {url} 失败: {exc}") from exc

            sock = connection.sock
            if sock is None:  # pragma: no cover - 正常连接后不会为空
                raise ShuxunTransportError(f"连接 {url} 失败: 未建立套接字")

            try:
                sock.settimeout(self._write_timeout)
                connection.request("POST", target, body=body, headers=request_headers)
                sock.settimeout(self._read_timeout)
                response = connection.getresponse()
                raw_body = response.read()
            except (OSError, http.client.HTTPException) as exc:
                raise ShuxunTransportError(f"请求 {url} 失败: {exc}") from exc

            charset = response.headers.get_content_charset() or "utf-8"
            try:
                text = raw_body.decode(charset, errors="replace")
            except LookupError:
                text = raw_body.decode("utf-8", errors="replace")

            return HttpResponse(
                status=response.status,
                body=text,
                headers=dict(response.getheaders()),
            )
        finally:
            connection.close()

    def __repr__(self) -> str:
        return (
            f"HttpClientTransport(connect_timeout={self._connect_timeout}, "
            f"read_timeout={self._read_timeout}, write_timeout={self._write_timeout})"
        )
