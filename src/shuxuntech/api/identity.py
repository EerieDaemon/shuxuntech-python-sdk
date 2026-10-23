"""身份核验接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..models import FaceCompareResult, FaceIdCardResult, IdCardCheckResult, LivingCheckResult
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["IdentityApi"]


class IdentityApi:
    """身份核验接口，通过 ``client.apis.identity`` 获取实例。"""

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def id_card_check(self, name: str, id_card: str) -> ApiResponse[IdCardCheckResult]:
        """身份证实名核验。

        :param name: 姓名
        :param id_card: 身份证号
        """
        params = Params.create().put("name", name).put("idCard", id_card)
        return self._client.post("/v1/idCard/check", params, IdCardCheckResult)

    def face_id_card_check(
        self,
        name: str,
        id_card: str,
        image: Optional[str] = None,
        img_url: Optional[str] = None,
    ) -> ApiResponse[FaceIdCardResult]:
        """人脸与身份证比对。

        :param name: 姓名
        :param id_card: 身份证号
        :param image: Base64 图片，与 ``img_url`` 二选一
        :param img_url: 图片 URL，与 ``image`` 二选一
        """
        params = (
            Params.create()
            .put("name", name)
            .put("idCard", id_card)
            .put("image", image)
            .put("imgUrl", img_url)
        )
        return self._client.post("/v1/faceIdCard/check", params, FaceIdCardResult)

    def face_compare(
        self,
        image1: str,
        image2: Optional[str] = None,
        img_url1: Optional[str] = None,
        img_url2: Optional[str] = None,
    ) -> ApiResponse[FaceCompareResult]:
        """两张人脸比对，两张图片可传 Base64 或 URL。

        :param image1: 第一张图片（Base64 或 URL）
        :param image2: 第二张图片（Base64 或 URL）
        :param img_url1: 第一张图片 URL
        :param img_url2: 第二张图片 URL
        """
        params = (
            Params.create()
            .put("image1", image1)
            .put("image2", image2)
            .put("imgUrl1", img_url1)
            .put("imgUrl2", img_url2)
        )
        return self._client.post("/v1/faceCompare/check", params, FaceCompareResult)

    def living_check(
        self,
        image1: str,
        image2: Optional[str] = None,
        image3: Optional[str] = None,
    ) -> ApiResponse[LivingCheckResult]:
        """图片活体检测。

        :param image1: 第一张图片（Base64 或 URL）
        :param image2: 第二张图片（Base64 或 URL）
        :param image3: 第三张图片（Base64 或 URL）
        """
        params = (
            Params.create()
            .put("image1", image1)
            .put("image2", image2)
            .put("image3", image3)
        )
        return self._client.post("/v1/living/check", params, LivingCheckResult)
