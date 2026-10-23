"""数勋开放平台的签名工具。

签名规则：``sign = sha256(appKey + timestamp + appSecret)``，结果取小写十六进制
字符串，``timestamp`` 为毫秒时间戳。服务端要求客户端时间与服务器时间偏差不超过
5 分钟，否则返回 ``code = 4``（签名错误）。

本模块无状态，通常不需要直接调用，:class:`~shuxuntech.client.ShuxunClient`
会在每次请求时自动完成签名。
"""

from __future__ import annotations

import hashlib
import time
from typing import Union

__all__ = ["now_millis", "sha256_hex", "sign"]


def now_millis() -> int:
    """返回当前时间的毫秒时间戳。"""
    return int(time.time() * 1000)


def sha256_hex(value: Union[str, bytes]) -> str:
    """计算 SHA-256，返回 64 位小写十六进制字符串。

    ``str`` 按 UTF-8 编码后计算。
    """
    if isinstance(value, str):
        value = value.encode("utf-8")
    elif not isinstance(value, (bytes, bytearray)):
        raise TypeError("value 必须是 str 或 bytes")
    return hashlib.sha256(bytes(value)).hexdigest()


def sign(app_key: str, app_secret: str, timestamp_ms: int) -> str:
    """按平台规则生成签名。

    :param app_key: 应用 appKey
    :param app_secret: 应用 appSecret
    :param timestamp_ms: 毫秒时间戳
    :return: 64 位小写十六进制签名字符串
    """
    if not isinstance(app_key, str) or not isinstance(app_secret, str):
        raise TypeError("appKey 和 appSecret 必须是字符串")
    return sha256_hex(f"{app_key}{int(timestamp_ms)}{app_secret}")
