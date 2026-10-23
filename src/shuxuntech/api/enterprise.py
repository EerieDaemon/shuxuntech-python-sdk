"""企业服务接口。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from ..models import (
    Enterprise2Result,
    Enterprise3Result,
    Enterprise4Result,
    EnterpriseBaseInfoResult,
    EnterpriseContactsInfoResult,
    EnterpriseLikeResult,
    EnterpriseNameLikeResult,
    EnterpriseReportResult,
)
from ..params import Params
from ..response import ApiResponse

if TYPE_CHECKING:  # pragma: no cover
    from ..client import ShuxunClient

__all__ = ["EnterpriseApi"]


class EnterpriseApi:
    """企业服务接口，通过 ``client.apis.enterprise`` 获取实例。

    企业类接口的 ``keyword`` 一般可以传企业名称或统一社会信用代码。
    """

    __slots__ = ("_client",)

    def __init__(self, client: "ShuxunClient") -> None:
        self._client = client

    def enterprise2_check(
        self,
        title: str,
        credit_code: str,
    ) -> ApiResponse[Enterprise2Result]:
        """企业二要素核验。

        :param title: 企业名称
        :param credit_code: 统一社会信用代码
        """
        params = Params.create().put("title", title).put("creditCode", credit_code)
        return self._client.post("/v1/enterprise2/check", params, Enterprise2Result)

    def enterprise3_check(
        self,
        ent_name: str,
        credit_code: str,
        person_name: str,
    ) -> ApiResponse[Enterprise3Result]:
        """企业三要素核验。

        :param ent_name: 企业名称
        :param credit_code: 统一社会信用代码
        :param person_name: 法人/股东姓名
        """
        params = (
            Params.create()
            .put("entName", ent_name)
            .put("creditCode", credit_code)
            .put("personName", person_name)
        )
        return self._client.post("/v1/enterprise3/check", params, Enterprise3Result)

    def enterprise4_check(
        self,
        f_name: str,
        f_id_card: str,
        title: str,
        credit_code: str,
    ) -> ApiResponse[Enterprise4Result]:
        """企业四要素核验。

        :param f_name: 法人姓名
        :param f_id_card: 法人身份证号
        :param title: 企业名称
        :param credit_code: 统一社会信用代码
        """
        params = (
            Params.create()
            .put("fName", f_name)
            .put("fIdCard", f_id_card)
            .put("title", title)
            .put("creditCode", credit_code)
        )
        return self._client.post("/v1/enterprise4/check", params, Enterprise4Result)

    def enterprise_base_info_query(
        self,
        keyword: str,
    ) -> ApiResponse[EnterpriseBaseInfoResult]:
        """企业工商信息查询。

        :param keyword: 企业名称或统一社会信用代码
        """
        params = Params.create().put("keyword", keyword)
        return self._client.post(
            "/v1/enterprise_base_info/query", params, EnterpriseBaseInfoResult
        )

    def enterprise_contacts_query(
        self,
        keyword: str,
    ) -> ApiResponse[EnterpriseContactsInfoResult]:
        """企业联系人信息查询。

        :param keyword: 企业名称或统一社会信用代码
        """
        params = Params.create().put("keyword", keyword)
        return self._client.post(
            "/v1/enterprise_contacts_info/query", params, EnterpriseContactsInfoResult
        )

    def enterprise_like_query(
        self,
        keyword: str,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> ApiResponse[EnterpriseLikeResult]:
        """企业工商信息模糊查询（分页）。

        :param keyword: 企业名称或统一社会信用代码
        :param page_no: 页码，默认 1
        :param page_size: 每页条数，默认 10
        """
        params = (
            Params.create()
            .put("keyword", keyword)
            .put("pageNo", page_no)
            .put("pageSize", page_size)
        )
        return self._client.post(
            "/v1/enterprise_like/query", params, EnterpriseLikeResult
        )

    def enterprise_name_like_query(
        self,
        keyword: str,
        page_size: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> ApiResponse[EnterpriseNameLikeResult]:
        """企业名称模糊查询。

        :param keyword: 企业名称或统一社会信用代码
        :param page_size: 每页条数，默认 10
        :param limit: 返回条数上限
        """
        params = (
            Params.create()
            .put("keyword", keyword)
            .put("pageSize", page_size)
            .put("limit", limit)
        )
        return self._client.post(
            "/v1/enterprise_name_like/query", params, EnterpriseNameLikeResult
        )

    def enterprise_report_query(
        self,
        keyword: str,
    ) -> ApiResponse[EnterpriseReportResult]:
        """企业报告查询。

        :param keyword: 企业名称或统一社会信用代码
        """
        params = Params.create().put("keyword", keyword)
        return self._client.post(
            "/v1/enterprise_report/query", params, EnterpriseReportResult
        )

    def ent_abnormal_query(self, keyword: str) -> ApiResponse[Any]:
        """企业经营异常查询。

        :param keyword: 企业名称或统一社会信用代码
        """
        params = Params.create().put("keyword", keyword)
        return self._client.post("/v1/ent_abnormal/query", params)
