"""按业务分类的强类型接口集合。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .api.bankcard import BankcardApi
from .api.enterprise import EnterpriseApi
from .api.express import ExpressApi
from .api.identity import IdentityApi
from .api.ip import IpApi
from .api.mobile import MobileApi
from .api.ocr import OcrApi
from .api.vehicle import VehicleApi

if TYPE_CHECKING:  # pragma: no cover
    from .client import ShuxunClient

__all__ = ["ShuxunApis"]


class ShuxunApis:
    """按业务分类的强类型接口集合，通过 ``client.apis`` 获取。"""

    __slots__ = (
        "_bankcard",
        "_enterprise",
        "_express",
        "_identity",
        "_ip",
        "_mobile",
        "_ocr",
        "_vehicle",
    )

    def __init__(self, client: "ShuxunClient") -> None:
        self._identity = IdentityApi(client)
        self._mobile = MobileApi(client)
        self._bankcard = BankcardApi(client)
        self._ocr = OcrApi(client)
        self._enterprise = EnterpriseApi(client)
        self._vehicle = VehicleApi(client)
        self._express = ExpressApi(client)
        self._ip = IpApi(client)

    @property
    def identity(self) -> IdentityApi:
        """身份核验接口。"""
        return self._identity

    @property
    def mobile(self) -> MobileApi:
        """运营商接口。"""
        return self._mobile

    @property
    def bankcard(self) -> BankcardApi:
        """银行卡接口。"""
        return self._bankcard

    @property
    def ocr(self) -> OcrApi:
        """文字识别接口。"""
        return self._ocr

    @property
    def enterprise(self) -> EnterpriseApi:
        """企业服务接口。"""
        return self._enterprise

    @property
    def vehicle(self) -> VehicleApi:
        """交通出行接口。"""
        return self._vehicle

    @property
    def express(self) -> ExpressApi:
        """生活服务接口。"""
        return self._express

    @property
    def ip(self) -> IpApi:
        """IP 归属地接口。"""
        return self._ip
