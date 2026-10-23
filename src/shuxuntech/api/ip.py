"""IP 归属地接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import IpQueryCityResult
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["IpApi"]


class IpApi:
    """IP 归属地接口，通过 ``client.apis.ip`` 获取实例。"""

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def ip_query(self, ip: str) -> ApiResponse[IpQueryCityResult]:
        """IPv4 归属地查询。

        :param ip: 待查询 IP
        """
        params = Params.create().put("ip", ip)
        return self._client.post("/v1/ip_location/query", params, IpQueryCityResult)

    def ipv6_query(self, ip: str) -> ApiResponse[IpQueryCityResult]:
        """IPv6 归属地查询。

        :param ip: 待查询 IP
        """
        params = Params.create().put("ip", ip)
        return self._client.post("/v1/ip_location/query/ipv6", params, IpQueryCityResult)
