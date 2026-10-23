"""SDK 异常类型。

:class:`ShuxunApiError` 表示平台返回业务错误（``code != 0``）；
:class:`ShuxunTransportError` 表示网络不可达、网关返回非平台结构等传输层错误。
"""

from __future__ import annotations

from typing import Optional

from .response_codes import describe_response_code

__all__ = ["ShuxunApiError", "ShuxunError", "ShuxunTransportError"]


class ShuxunError(Exception):
    """SDK 所有异常的基类。"""


class ShuxunApiError(ShuxunError):
    """平台返回业务错误。

    SDK 默认通过 :class:`~shuxuntech.response.ApiResponse` 的 ``code`` 表达业务结果，
    只有调用 ``post_or_throw`` 系列方法时才会抛出本异常。

    :ivar code: 平台返回码，响应缺少 ``code`` 时为 ``-1``
    :ivar msg: 平台返回的错误描述
    :ivar seq_no: 平台流水号，联系技术支持时提供
    :ivar http_status: 本次请求的 HTTP 状态码
    """

    def __init__(
        self,
        code: int,
        msg: Optional[str] = None,
        seq_no: Optional[str] = None,
        http_status: int = 0,
    ) -> None:
        self.code = int(code)
        self.msg = msg
        self.seq_no = seq_no
        self.http_status = int(http_status)
        super().__init__(self.__str__())

    def __str__(self) -> str:
        detail = self.msg or describe_response_code(self.code)
        text = f"[{self.code}] {detail}"
        if self.seq_no:
            text += f" (seqNo={self.seq_no})"
        return text


class ShuxunTransportError(ShuxunError):
    """网络不可达、响应不是平台统一结构等传输层异常。

    平台会把业务错误放在统一响应体中返回，HTTP 状态码可能不是 2xx。
    只要响应体包含顶层 ``code`` 字段，SDK 就会正常返回
    :class:`~shuxuntech.response.ApiResponse`，不会抛出本异常；只有响应体无法
    识别为平台响应（例如网关返回的 HTML 错误页）时才会抛出。

    :ivar http_status: HTTP 状态码，未拿到响应时为 ``0``
    :ivar response_body: 原始响应体，未拿到响应或响应为空时为 ``None``
    """

    def __init__(
        self,
        message: str,
        *,
        http_status: int = 0,
        response_body: Optional[str] = None,
    ) -> None:
        self.http_status = int(http_status)
        self.response_body = response_body
        super().__init__(message)
