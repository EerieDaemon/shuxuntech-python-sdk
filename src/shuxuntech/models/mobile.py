"""运营商返回模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import Model


@dataclass
class Mobile23Result(Model):
    """运营商2、3要素验证返回结果。"""

    #: 1：一致 2：不一致 3：无记录，不计费
    result: Optional[int] = None

    #: 结果描述
    result_desc: Optional[str] = None

    #: 运营商，cmcc、cucc、ctcc
    mobile_channel: Optional[str] = None


@dataclass
class MobileEmptyResult(Model):
    """运营商空号检测。"""

    #: 1：空号 2：实号 3：停机 4：沉默号 5：风险号 6：无记录，不计费
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None

    #: 运营商，cmcc、cucc、ctcc
    mobile_channel: Optional[str] = None

    #: 归属地
    area: Optional[str] = None


@dataclass
class MobileEmptyResultV2(Model):
    """运营商空号检测优质版。"""

    #: 1:正常 2：空号 3：关机 4：停机 5：在网但不可用 6：未知，包含以下4种情况，a:特殊号码无法查询 b:号码失败次数超频 c:号码管控 d:号码不存在
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None

    #: 运营商，cmcc、cucc、ctcc
    mobile_channel: Optional[str] = None

    #: 归属地
    area: Optional[str] = None

    #: 是否携号转网，1：是 0：否
    is_transfer: Optional[int] = None

    #: 运营商备注
    remark: Optional[str] = None


@dataclass
class MobileOnlineResult(Model):
    """运营商在网时长。"""

    #: 1: [0-3) 2: [3-6) 3: [6-12) 4: [12-24) 5: 24 个月及以上 6: 无记录 7: 号码状态异常（1、销号6个月以上 2、携号转网 3、未放号的号码等）
    #: 6、7不计费
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None

    #: 运营商，cmcc、cucc、ctcc
    mobile_channel: Optional[str] = None


@dataclass
class MobileStatusResult(Model):
    """运营商在网状态。"""

    #: 1：正常 2：停机 3：在网不可用 4：销号/未启用 5：无记录，不计费
    result: Optional[int] = None

    #: 运营商，cmcc、cucc、ctcc
    mobile_channel: Optional[str] = None


@dataclass
class MobileTransformResult(Model):
    """运营商携号转网。"""

    #: 1：转网 2：未转网
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None

    #: 新运营商
    new_channel: Optional[str] = None

    #: 原运营商
    old_channel: Optional[str] = None
