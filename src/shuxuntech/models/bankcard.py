"""银行卡返回模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import Model


@dataclass
class Bankcard234Result(Model):
    """银行卡234简版。"""

    #: 1：一致 2：不一致 3：无效卡号或卡状态异常
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None


@dataclass
class BankcardOcrResult(Model):
    """银行卡OCR。"""

    #: 1: 识别成功，有数据 2: 识别成功，无数据 3：识别失败，无法正确解析、未按要求传入参数、下载图片超时
    result: Optional[int] = None

    #: 识别结果描述
    result_desc: Optional[str] = None

    info: Optional[BankcardOcrInfo] = None


@dataclass
class BankcardOcrInfo(Model):
    bankcard: Optional[str] = None

    bank: Optional[str] = None


@dataclass
class BankPlaceResult(Model):
    """银行卡归属地信息。"""

    #: 1：查询成功，计费 2：不符合Luhn / 不符合卡BIN 3：查无信息（该卡号暂未收录）
    result: Optional[int] = None

    #: 归属地信息
    place_info: Optional[BankPlacePlaceInfo] = None


@dataclass
class BankPlacePlaceInfo(Model):
    bin_digits: Optional[int] = None

    bank: Optional[str] = None

    card_bin: Optional[str] = None

    province: Optional[str] = None

    card_name: Optional[str] = None

    city: Optional[str] = None

    tel: Optional[str] = None

    bank_logo: Optional[str] = None

    type: Optional[str] = None

    card_digits: Optional[int] = None

    luhn: Optional[bool] = None

    card: Optional[str] = None
