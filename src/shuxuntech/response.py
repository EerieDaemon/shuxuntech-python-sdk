"""平台统一响应结构。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Mapping, Optional, TypeVar

from .response_codes import describe_response_code

__all__ = ["ApiResponse"]

T = TypeVar("T")


@dataclass
class ApiResponse(Generic[T]):
    """平台统一响应。

    .. code-block:: json

        {"code": 0, "msg": "成功", "seqNo": "20261022123456", "data": {...}}

    ``code == 0`` 表示成功；其余取值见
    :class:`~shuxuntech.response_codes.ResponseCode`。
    注意 ``code == 2``（无记录）属于正常业务返回，调用方应按业务含义处理。

    平台可能用非 2xx 的 HTTP 状态码返回业务错误（例如 400），此时响应体仍是本结构，
    SDK 会照常解析并返回，``http_status`` 保存原始状态码。

    :ivar code: 返回码，0 表示成功；响应缺失该字段时为 ``None``
    :ivar msg: 返回信息，失败时为具体错误描述
    :ivar data: 业务数据；未指定强类型模型时为 ``dict`` / ``list``
    :ivar seq_no: 平台流水号，联系技术支持排查问题时提供
    :ivar http_status: 本次请求的 HTTP 状态码
    :ivar raw: 原始响应体解析后的字典
    """

    code: Optional[int] = None
    msg: Optional[str] = None
    data: Optional[T] = None
    seq_no: Optional[str] = None
    http_status: int = 0
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False)

    @property
    def is_success(self) -> bool:
        """是否调用成功，即 ``code == 0``。"""
        return self.code == 0

    @property
    def code_description(self) -> str:
        """返回码的中文说明。"""
        return describe_response_code(self.code)

    def __str__(self) -> str:
        return (
            f"ApiResponse(http_status={self.http_status}, code={self.code}, "
            f"msg={self.msg!r}, seqNo={self.seq_no!r})"
        )
