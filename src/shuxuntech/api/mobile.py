"""运营商接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import (
    Mobile23Result,
    MobileEmptyResult,
    MobileEmptyResultV2,
    MobileOnlineResult,
    MobileStatusResult,
    MobileTransformResult,
)
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["MobileApi"]


class MobileApi:
    """运营商接口，通过 ``client.apis.mobile`` 获取实例。"""

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def mobile2_check(self, name: str, mobile: str) -> ApiResponse[Mobile23Result]:
        """手机号二要素核验。

        :param name: 姓名
        :param mobile: 手机号
        """
        params = Params.create().put("name", name).put("mobile", mobile)
        return self._client.post("/v1/mobile2/check", params, Mobile23Result)

    def mobile3_check(
        self,
        name: str,
        mobile: str,
        id_card: str,
    ) -> ApiResponse[Mobile23Result]:
        """手机号三要素核验。

        :param name: 姓名
        :param mobile: 手机号
        :param id_card: 身份证号
        """
        params = (
            Params.create()
            .put("name", name)
            .put("mobile", mobile)
            .put("idCard", id_card)
        )
        return self._client.post("/v1/mobile3/check", params, Mobile23Result)

    def mobile_empty_check(self, mobile: str) -> ApiResponse[MobileEmptyResult]:
        """空号检测。

        :param mobile: 手机号
        """
        params = Params.create().put("mobile", mobile)
        return self._client.post("/v1/mobileEmpty/check", params, MobileEmptyResult)

    def mobile_empty_check_v2(self, mobile: str) -> ApiResponse[MobileEmptyResultV2]:
        """空号检测 V2。

        :param mobile: 手机号
        """
        params = Params.create().put("mobile", mobile)
        return self._client.post("/v1/mobileEmpty/check/v2", params, MobileEmptyResultV2)

    def mobile_empty_check_v3(self, mobile: str) -> ApiResponse[MobileEmptyResultV2]:
        """空号检测 V3，能否调用以控制台开通为准。

        :param mobile: 手机号
        """
        params = Params.create().put("mobile", mobile)
        return self._client.post("/v1/mobileEmpty/check/v3", params, MobileEmptyResultV2)

    def mobile_online_query(self, mobile: str) -> ApiResponse[MobileOnlineResult]:
        """手机号在网时长查询。

        :param mobile: 手机号
        """
        params = Params.create().put("mobile", mobile)
        return self._client.post("/v1/mobileOnline/query", params, MobileOnlineResult)

    def mobile_status_query(self, mobile: str) -> ApiResponse[MobileStatusResult]:
        """手机号状态查询。

        :param mobile: 手机号
        """
        params = Params.create().put("mobile", mobile)
        return self._client.post("/v1/mobileStatus/query", params, MobileStatusResult)

    def mobile_transform_query(self, mobile: str) -> ApiResponse[MobileTransformResult]:
        """携号转网查询。

        :param mobile: 手机号
        """
        params = Params.create().put("mobile", mobile)
        return self._client.post("/v1/mobileTransform/query", params, MobileTransformResult)
