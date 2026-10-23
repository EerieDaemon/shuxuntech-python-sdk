"""银行卡接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models import BankPlaceResult, Bankcard234Result
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["BankcardApi"]


class BankcardApi:
    """银行卡接口，通过 ``client.apis.bankcard`` 获取实例。"""

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def bankcard2_check(self, name: str, bankcard: str) -> ApiResponse[Bankcard234Result]:
        """银行卡二要素核验。

        :param name: 姓名
        :param bankcard: 银行卡号
        """
        params = Params.create().put("name", name).put("bankcard", bankcard)
        return self._client.post("/v1/bankcard2/check", params, Bankcard234Result)

    def bankcard3_check(
        self,
        name: str,
        bankcard: str,
        id_card: str,
    ) -> ApiResponse[Bankcard234Result]:
        """银行卡三要素核验。

        :param name: 姓名
        :param bankcard: 银行卡号
        :param id_card: 身份证号
        """
        params = (
            Params.create()
            .put("name", name)
            .put("bankcard", bankcard)
            .put("idCard", id_card)
        )
        return self._client.post("/v1/bankcard3/check", params, Bankcard234Result)

    def bankcard3_check_v2(
        self,
        name: str,
        bankcard: str,
        mobile: str,
    ) -> ApiResponse[Bankcard234Result]:
        """银行卡三要素核验（手机号版）。

        :param name: 姓名
        :param bankcard: 银行卡号
        :param mobile: 手机号
        """
        params = (
            Params.create()
            .put("name", name)
            .put("bankcard", bankcard)
            .put("mobile", mobile)
        )
        return self._client.post("/v1/bankcard3/check/v2", params, Bankcard234Result)

    def bankcard4_check(
        self,
        name: str,
        bankcard: str,
        id_card: str,
        mobile: str,
    ) -> ApiResponse[Bankcard234Result]:
        """银行卡四要素核验。

        :param name: 姓名
        :param bankcard: 银行卡号
        :param id_card: 身份证号
        :param mobile: 手机号
        """
        params = (
            Params.create()
            .put("name", name)
            .put("bankcard", bankcard)
            .put("idCard", id_card)
            .put("mobile", mobile)
        )
        return self._client.post("/v1/bankcard4/check", params, Bankcard234Result)

    def bank_place_query(self, bankcard: str) -> ApiResponse[BankPlaceResult]:
        """银行卡归属地查询。

        :param bankcard: 银行卡号
        """
        params = Params.create().put("bankcard", bankcard)
        return self._client.post("/v1/bankPlace/query", params, BankPlaceResult)

    def ent_tax_status_query(
        self,
        acct_no: str,
        acct_bank: str,
        ent_name: str,
    ) -> ApiResponse[Any]:
        """企业税务状态查询。

        :param acct_no: 银行账号
        :param acct_bank: 开户银行
        :param ent_name: 企业名称
        """
        params = (
            Params.create()
            .put("acctNo", acct_no)
            .put("acctBank", acct_bank)
            .put("entName", ent_name)
        )
        return self._client.post("/v1/ent_tax_status/query", params)
