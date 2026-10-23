"""平台统一返回码。

所有接口共用同一套返回码，出现在响应顶层 ``code`` 字段中。
:attr:`ResponseCode.SUCCESS` 表示成功，其余为失败；
:attr:`ResponseCode.NO_RECORD`（2，无记录）属于正常业务结果。
"""

from __future__ import annotations

from enum import IntEnum
from typing import Optional

__all__ = ["ResponseCode", "ResponseCodes", "describe_response_code"]


class ResponseCode(IntEnum):
    """平台返回码。"""

    SUCCESS = 0
    """成功。"""

    PARAM_ERROR = 1
    """参数错误：检查必填参数是否缺失、格式是否合法。"""

    NO_RECORD = 2
    """无记录：权威库中未查到该条记录，属正常返回。"""

    UPSTREAM_ERROR = 3
    """第三方服务异常：上游通道波动，建议重试或联系技术支持。"""

    SIGN_ERROR = 4
    """签名错误：核对 appSecret，检查时间戳偏差是否超过 5 分钟。"""

    INSUFFICIENT_BALANCE = 5
    """余额不足：前往控制台充值或购买新的套餐包。"""

    RATE_LIMITED = 6
    """调用频率超限：降低并发或联系商务提升 QPS 上限。"""

    ACCOUNT_DISABLED = 7
    """账号停用：联系客服核实账号状态。"""

    API_DISABLED = 8
    """接口已停用：该接口已下线，请改用替代接口。"""

    API_NOT_AUTHORIZED = 9
    """未开通接口权限：在控制台申请开通该接口，或联系客服协助。"""

    IP_NOT_ALLOWED = 10
    """IP 不在白名单：在控制台把调用方 IP 加入白名单。"""

    SYSTEM_ERROR = 11
    """系统异常：服务端异常，请携带 seqNo 联系技术支持。"""

    REAL_NAME_REQUIRED = 12
    """实名状态错误：先完成企业实名认证再调用。"""

    OTHER = 99
    """其他异常：以 msg 返回的具体信息为准。"""

    @property
    def description(self) -> str:
        """返回返回码的中文说明。"""
        return _DESCRIPTIONS[self]


_DESCRIPTIONS = {
    ResponseCode.SUCCESS: "成功",
    ResponseCode.PARAM_ERROR: "参数错误",
    ResponseCode.NO_RECORD: "无记录",
    ResponseCode.UPSTREAM_ERROR: "第三方服务异常",
    ResponseCode.SIGN_ERROR: "签名错误",
    ResponseCode.INSUFFICIENT_BALANCE: "余额不足",
    ResponseCode.RATE_LIMITED: "调用频率超限",
    ResponseCode.ACCOUNT_DISABLED: "账号停用",
    ResponseCode.API_DISABLED: "接口已停用",
    ResponseCode.API_NOT_AUTHORIZED: "未开通接口权限",
    ResponseCode.IP_NOT_ALLOWED: "IP 不在白名单",
    ResponseCode.SYSTEM_ERROR: "系统异常",
    ResponseCode.REAL_NAME_REQUIRED: "实名状态错误",
    ResponseCode.OTHER: "其他异常",
}


def describe_response_code(code: Optional[int]) -> str:
    """返回返回码的中文说明；未知返回码返回 ``"未知错误"``。

    :param code: 平台返回码，``None`` 表示响应缺少该字段
    """
    if code is None:
        return "未知错误"
    try:
        return ResponseCode(int(code)).description
    except (TypeError, ValueError):
        return "未知错误"


#: 兼容 Java SDK 的命名习惯。
ResponseCodes = ResponseCode
