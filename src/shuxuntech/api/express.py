"""生活服务接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["ExpressApi"]


class ExpressApi:
    """生活服务接口，通过 ``client.apis.express`` 获取实例。"""

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def express_query(
        self,
        no: str,
        code: Optional[str] = None,
        tel: Optional[str] = None,
    ) -> ApiResponse[Any]:
        """快递物流查询。

        :param no: 快递单号
        :param code: 快递公司编码，不传时由平台自动识别
        :param tel: 收件人手机号后四位，顺丰等部分快递必填
        """
        params = Params.create().put("no", no).put("code", code).put("tel", tel)
        return self._client.post("/v1/express/query", params)

    def express_subscribe(
        self,
        no: str,
        callback_url: str,
        code: Optional[str] = None,
        tel: Optional[str] = None,
    ) -> ApiResponse[Any]:
        """快递物流订阅。

        :param no: 快递单号
        :param callback_url: 物流订阅回调地址
        :param code: 快递公司编码，不传时由平台自动识别
        :param tel: 收件人手机号后四位，顺丰等部分快递必填
        """
        params = (
            Params.create()
            .put("no", no)
            .put("callbackUrl", callback_url)
            .put("code", code)
            .put("tel", tel)
        )
        return self._client.post("/v1/express/subscribe", params)
