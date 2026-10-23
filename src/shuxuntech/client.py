"""数勋科技开放平台 Python 客户端。

每个请求自动完成：

1. 以毫秒时间戳生成 ``timestamp``；
2. 按 ``sha256(appKey + timestamp + appSecret)`` 生成 ``sign``；
3. 把 ``appKey``、``timestamp``、``sign`` 放入请求头；
4. 把参数按 ``application/x-www-form-urlencoded`` 提交，并把响应解析为
   :class:`~shuxuntech.response.ApiResponse`。

最简用法：

.. code-block:: python

    from shuxuntech import ShuxunClient

    client = ShuxunClient("your-app-key", "your-app-secret")
    response = client.post("/v1/idCard/check", {"name": "张三", "idCard": "110101..."})
    if response.is_success:
        print(response.data)

客户端线程安全，建议全局复用一个实例，并在应用退出时调用 :meth:`close`。
SDK 不会自动重试：平台接口通常按次计费，是否重试应由业务决定。
"""

from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional, Type, TypeVar, overload
from urllib.parse import urlsplit

from .apis import ShuxunApis
from .auth import now_millis, sign
from .exceptions import ShuxunApiError, ShuxunTransportError
from .models.base import Model
from .params import Params, ParamsLike, stringify_param
from .response import ApiResponse
from .transport import HttpClientTransport, HttpTransport

__all__ = ["DEFAULT_BASE_URL", "ShuxunClient"]

DEFAULT_BASE_URL = "https://api.shuxuntech.com"

HEADER_APP_KEY = "appKey"
HEADER_TIMESTAMP = "timestamp"
HEADER_SIGN = "sign"

DEFAULT_CONNECT_TIMEOUT = 5.0
DEFAULT_READ_TIMEOUT = 15.0
DEFAULT_WRITE_TIMEOUT = 15.0

T = TypeVar("T")


class ShuxunClient:
    """数勋开放平台客户端，线程安全，建议全局复用同一个实例。

    :param app_key: 应用 appKey，必填
    :param app_secret: 应用 appSecret，必填，请勿提交到代码仓库
    :param base_url: 网关地址，默认 :data:`DEFAULT_BASE_URL`
    :param connect_timeout: 建连超时（秒），默认 5
    :param read_timeout: 读取超时（秒），默认 15
    :param write_timeout: 写入超时（秒），默认 15
    :param transport: 自定义传输层；注入后由调用方负责关闭，超时参数不再生效
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        read_timeout: float = DEFAULT_READ_TIMEOUT,
        write_timeout: float = DEFAULT_WRITE_TIMEOUT,
        transport: Optional[HttpTransport] = None,
    ) -> None:
        _require_text(app_key, "appKey")
        _require_text(app_secret, "appSecret")
        _require_text(base_url, "baseUrl")

        normalized_base_url = base_url.strip().rstrip("/")
        parts = urlsplit(normalized_base_url)
        if parts.scheme not in ("http", "https") or not parts.netloc:
            raise ValueError("base_url 必须是 http(s) 地址")

        _require_positive(connect_timeout, "connect_timeout")
        _require_positive(read_timeout, "read_timeout")
        _require_positive(write_timeout, "write_timeout")

        self._app_key = app_key
        self._app_secret = app_secret
        self._base_url = normalized_base_url
        self._transport: HttpTransport = transport or HttpClientTransport(
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
        )
        self._owns_transport = transport is None
        self._apis = ShuxunApis(self)

    @classmethod
    def create(cls, app_key: str, app_secret: str, **kwargs: Any) -> "ShuxunClient":
        """使用默认配置创建客户端，网关地址取 :data:`DEFAULT_BASE_URL`。"""
        return cls(app_key, app_secret, **kwargs)

    @property
    def base_url(self) -> str:
        """当前使用的网关地址。"""
        return self._base_url

    @property
    def app_key(self) -> str:
        """当前使用的 appKey。"""
        return self._app_key

    @property
    def apis(self) -> ShuxunApis:
        """按业务分类的强类型接口集合。

        .. code-block:: python

            client.apis.identity.id_card_check("张三", "110101...")
        """
        return self._apis

    @overload
    def post(
        self,
        path: str,
        params: ParamsLike = None,
        result_type: None = None,
    ) -> ApiResponse[Any]:
        ...

    @overload
    def post(
        self,
        path: str,
        params: ParamsLike,
        result_type: Type[T],
    ) -> ApiResponse[T]:
        ...

    def post(
        self,
        path: str,
        params: ParamsLike = None,
        result_type: Optional[Type[Any]] = None,
    ) -> ApiResponse[Any]:
        """调用接口，业务错误通过返回值的 ``code`` 表达。

        :param path: 接口路径，如 ``"/v1/idCard/check"``
        :param params: 表单参数，可为 ``None``
        :param result_type: ``data`` 的目标模型类；不传时 ``data`` 为原始
            ``dict`` / ``list``
        :return: 统一响应
        """
        return self._execute(path, params, result_type)

    @overload
    def post_or_throw(
        self,
        path: str,
        params: ParamsLike = None,
        result_type: None = None,
    ) -> ApiResponse[Any]:
        ...

    @overload
    def post_or_throw(
        self,
        path: str,
        params: ParamsLike,
        result_type: Type[T],
    ) -> ApiResponse[T]:
        ...

    def post_or_throw(
        self,
        path: str,
        params: ParamsLike = None,
        result_type: Optional[Type[Any]] = None,
    ) -> ApiResponse[Any]:
        """调用接口；``code != 0`` 时抛出 :class:`ShuxunApiError`。"""
        response = self._execute(path, params, result_type)
        if not response.is_success:
            code = response.code if response.code is not None else -1
            raise ShuxunApiError(
                code=code,
                msg=response.msg,
                seq_no=response.seq_no,
                http_status=response.http_status,
            )
        return response

    def close(self) -> None:
        """关闭内部创建的传输层；注入自定义传输层时由调用方负责关闭。"""
        if self._owns_transport:
            self._transport.close()

    def __enter__(self) -> "ShuxunClient":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"ShuxunClient(base_url={self._base_url!r}, app_key={self._app_key!r})"

    def _execute(
        self,
        path: str,
        params: ParamsLike,
        result_type: Optional[Type[Any]],
    ) -> ApiResponse[Any]:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path 不能为空")
        if result_type is not None:
            if not isinstance(result_type, type) or not issubclass(result_type, Model):
                raise TypeError("result_type 必须是 Model 的子类")

        timestamp = now_millis()
        headers = {
            HEADER_APP_KEY: self._app_key,
            HEADER_TIMESTAMP: str(timestamp),
            HEADER_SIGN: sign(self._app_key, self._app_secret, timestamp),
        }
        form = _build_form(params)
        url = self._build_url(path.strip())

        raw = self._transport.post(url, headers, form)
        status = raw.status
        body = raw.body

        if not body or not body.strip():
            raise ShuxunTransportError(
                f"HTTP {status} 响应内容为空",
                http_status=status,
            )

        try:
            payload = json.loads(body)
        except ValueError as exc:
            raise ShuxunTransportError(
                f"HTTP {status}，响应不是合法的 JSON: {_abbreviate(body)}",
                http_status=status,
                response_body=body,
            ) from exc

        if not isinstance(payload, Mapping):
            raise ShuxunTransportError(
                f"HTTP {status}，响应不是平台统一结构: {_abbreviate(body)}",
                http_status=status,
                response_body=body,
            )

        code = _coerce_code(payload.get("code"))
        if code is None and not 200 <= status < 300:
            raise ShuxunTransportError(
                f"HTTP {status}，响应不是平台统一结构: {_abbreviate(body)}",
                http_status=status,
                response_body=body,
            )

        data = self._convert_data(payload.get("data"), result_type, status, body)
        return ApiResponse(
            code=code,
            msg=_as_text(payload.get("msg")),
            data=data,
            seq_no=_as_text(payload.get("seqNo")),
            http_status=status,
            raw=dict(payload),
        )

    def _convert_data(
        self,
        data: Any,
        result_type: Optional[Type[Any]],
        status: int,
        body: str,
    ) -> Any:
        if result_type is None or data is None:
            return data
        try:
            return result_type.from_dict(data)
        except (TypeError, ValueError) as exc:
            raise ShuxunTransportError(
                f"响应 data 无法映射到 {result_type.__name__}: {exc}",
                http_status=status,
                response_body=body,
            ) from exc

    def _build_url(self, path: str) -> str:
        return f"{self._base_url}{path}" if path.startswith("/") else f"{self._base_url}/{path}"


def _build_form(params: ParamsLike) -> Dict[str, str]:
    if params is None:
        return {}
    if isinstance(params, Params):
        return params.as_dict()
    if isinstance(params, Mapping):
        form: Dict[str, str] = {}
        for name, value in params.items():
            if not isinstance(name, str) or not name.strip():
                raise ValueError("参数名不能为空")
            if value is None:
                continue
            form[name] = stringify_param(value)
        return form
    raise TypeError("params 必须是 Params、Mapping 或 None")


def _require_text(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} 不能为空")


def _require_positive(value: Any, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} 必须是数字")
    if value <= 0:
        raise ValueError(f"{name} 必须大于 0")


def _coerce_code(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _as_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    return value if isinstance(value, str) else str(value)


def _abbreviate(text: str, max_length: int = 512) -> str:
    trimmed = text.strip()
    return trimmed if len(trimmed) <= max_length else f"{trimmed[:max_length]}..."
