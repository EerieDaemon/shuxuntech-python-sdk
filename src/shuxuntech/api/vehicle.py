"""交通出行接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from ..models import CarFiveResult, Vin2_1Result, Vin5Result
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["VehicleApi"]


class VehicleApi:
    """交通出行接口，通过 ``client.apis.vehicle`` 获取实例。"""

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def vin_query(self, vin: str) -> ApiResponse[Any]:
        """车架号 VIN 查询。

        :param vin: 车架号
        """
        params = Params.create().put("vin", vin)
        return self._client.post("/v1/vin/query", params)

    def vin21_query(self, vin: str) -> ApiResponse[Vin2_1Result]:
        """车架号 VIN 查询 V2.1。

        :param vin: 车架号
        """
        params = Params.create().put("vin", vin)
        return self._client.post("/v1/vin2_1/query", params, Vin2_1Result)

    def vin3_query(self, vin: str) -> ApiResponse[Any]:
        """车架号 VIN 查询 V3。

        :param vin: 车架号
        """
        params = Params.create().put("vin", vin)
        return self._client.post("/v1/vin3/query", params)

    def vin4_custom_query(self, vin: str) -> ApiResponse[Any]:
        """车架号 VIN 查询 V4（定制）。

        :param vin: 车架号
        """
        params = Params.create().put("vin", vin)
        return self._client.post("/v1/vin4_custom/query", params)

    def vin5_query(self, vin: str) -> ApiResponse[Vin5Result]:
        """车架号 VIN 查询 V5（精准版，含公告号）。

        :param vin: 车架号
        """
        params = Params.create().put("vin", vin)
        return self._client.post("/v1/vin5/query", params, Vin5Result)

    def car_five_query(self, car_no: str) -> ApiResponse[CarFiveResult]:
        """车辆五项信息查询。

        :param car_no: 车牌号
        """
        params = Params.create().put("carNo", car_no)
        return self._client.post("/v1/car_five/query", params, CarFiveResult)

    def car_brand_query(self) -> ApiResponse[Any]:
        """车品牌查询。"""
        return self._client.post("/v1/car_brand/query", Params.create())

    def car_series_query(self, brand_id: str) -> ApiResponse[Any]:
        """根据品牌查车系。

        :param brand_id: 品牌 ID
        """
        params = Params.create().put("brandId", brand_id)
        return self._client.post("/v1/car_series/query", params)

    def car_type_query(
        self,
        series_id: str,
        sort: Optional[str] = None,
    ) -> ApiResponse[Any]:
        """根据车系查车型。

        :param series_id: 车系 ID
        :param sort: 排序字段
        """
        params = Params.create().put("seriesId", series_id).put("sort", sort)
        return self._client.post("/v1/car_type/query", params)

    def car_config_query(self, keyword: str) -> ApiResponse[Any]:
        """车型配置查询。

        :param keyword: 关键词
        """
        params = Params.create().put("keyword", keyword)
        return self._client.post("/v1/car_config/query", params)

    def car_detail_query(self, car_id: str) -> ApiResponse[Any]:
        """车型详情查询。

        :param car_id: 车型 ID
        """
        params = Params.create().put("carid", car_id)
        return self._client.post("/v1/car_detail/query", params)
