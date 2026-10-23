"""文字识别接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..models import (
    BankcardOcrResult,
    BusinessOcrResult,
    DrivingOcrResult,
    IdCardOcrResult,
    PlateOcrResult,
    VehicleOcrResult,
    VinOcrResult,
    WordOcrResult,
)
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["OcrApi"]


class OcrApi:
    """文字识别接口，通过 ``client.apis.ocr`` 获取实例。

    所有 OCR 接口的 ``image`` 与 ``img_url`` 二选一：传 Base64 图片或图片 URL。
    """

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def id_card_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[IdCardOcrResult]:
        """身份证 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/idCard/ocr", params, IdCardOcrResult)

    def bankcard_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[BankcardOcrResult]:
        """银行卡 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/bankcard/ocr", params, BankcardOcrResult)

    def business_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[BusinessOcrResult]:
        """营业执照 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/business/ocr", params, BusinessOcrResult)

    def driving_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[DrivingOcrResult]:
        """驾驶证 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/driving/ocr", params, DrivingOcrResult)

    def plate_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[PlateOcrResult]:
        """车牌号 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/plate/ocr", params, PlateOcrResult)

    def vehicle_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
        card_side: Optional[str] = None,
    ) -> ApiResponse[VehicleOcrResult]:
        """行驶证 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        :param card_side: 证件面：``FRONT`` / ``BACK``，默认 ``FRONT``
        """
        params = (
            Params.create()
            .put("image", image)
            .put("imgUrl", img_url)
            .put("cardSide", card_side)
        )
        return self._client.post("/v1/vehicle/ocr", params, VehicleOcrResult)

    def word_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[WordOcrResult]:
        """通用文字 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/word/ocr", params, WordOcrResult)

    def vin_ocr(
        self,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[VinOcrResult]:
        """车架号 OCR。

        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = Params.create().put("image", image).put("imgUrl", img_url)
        return self._client.post("/v1/vin/ocr", params, VinOcrResult)
