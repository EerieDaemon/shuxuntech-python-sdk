"""企业服务返回模型。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .base import Model


@dataclass
class Enterprise2Result(Model):
    """企业2要素。"""

    #: 1：一致 2：不一致
    result: Optional[int] = None

    #: 核验结果描述
    result_desc: Optional[str] = None

    #: 状态 1:存续; 2:注销; 3:吊销; 4:撤销; 5:迁出; 6:设立中; 7:清算中; 8:停业; 9:其他; 10:空; 11:歇业; 12:责令关闭; 13:已取缔非法社会组织;
    #: 14:涉嫌非法社会组织; 15:待注销
    status: Optional[str] = None

    def __post_init__(self) -> None:
        if self.result_desc is None and self.result is not None:
            self.result_desc = "核验一致" if self.result == 1 else "核验不一致"


@dataclass
class Enterprise3Result(Model):
    """企业3要素。"""

    #: 企业名称是否匹配 1：是 0：否
    match_ent_name: Optional[int] = None

    #: 统一社会信用代码是否匹配 1：是 0：否
    match_credit_code: Optional[int] = None

    #: 核验人员姓名是否匹配 1：是 0：否
    match_person_name: Optional[int] = None

    #: 核验人员是否法人 1：是 0：否
    is_fr: Optional[int] = None

    #: 核验人员是否高管 1：是 0：否
    is_manager: Optional[int] = None

    #: 核验人员是否股东 1：是 0：否
    is_shareholders: Optional[int] = None

    #: 企业是否在营 1: 是 0: 否
    ent_status: Optional[int] = None

    #: 企业类型 1: 企业 0: 个体
    ent_type: Optional[int] = None

    #: 成立日期
    es_date: Optional[str] = None

    #: 经营期限从
    op_from: Optional[str] = None

    #: 经营期限至
    op_to: Optional[str] = None


@dataclass
class Enterprise4Result(Model):
    """企业四要素。"""

    #: 1：查询成功 2：查询无记录，不计费
    result: Optional[int] = None

    match: Optional[Enterprise4Match] = None


@dataclass
class Enterprise4Match(Model):
    #: 法人姓名是否一致 1：一致 2：不一致
    match_f_name: Optional[int] = None

    #: 证件号是否一致， 1：一致 2：不一致
    match_f_id_card: Optional[int] = None

    #: 企业名称是否一致 1：一致 2：不一致
    match_title: Optional[int] = None

    #: 统一信用代码是否一致 1：一致 2：不一致
    match_credit_code: Optional[int] = None

    #: 是否全部匹配 1：一致 2：不一致
    match_all: Optional[int] = None


@dataclass
class EnterpriseBaseInfoResult(Model):
    """企业工商信息返回结果。"""

    #: 1:查询成功，有数据 2:查询成功，无数据
    result: Optional[int] = None

    #: 查询数据
    info: Optional[EnterpriseBaseInfoInfo] = None


@dataclass
class EnterpriseBaseInfoInfo(Model):
    #: 公司名称
    company_name: Optional[str] = None

    #: 统一社会信用代码
    credit_code: Optional[str] = None

    #: 组织机构代码
    org_number: Optional[str] = None

    #: 企业类型
    company_type: Optional[str] = None

    #: 企业关键人名称
    key_person_name: Optional[str] = None

    #: 企业关键人类型
    key_person_type: Optional[str] = None

    #: 注册资本(万元)
    reg_capital: Optional[str] = None

    #: 实缴资本
    actual_capital: Optional[str] = None

    #: 所属省份
    province: Optional[str] = None

    #: 所属省份code
    province_code: Optional[str] = None

    #: 所属城市
    city: Optional[str] = None

    #: 所属城市code
    city_code: Optional[str] = None

    #: 所属区
    district: Optional[str] = None

    #: 所属区code
    district_code: Optional[str] = None

    #: 注册号
    reg_number: Optional[str] = None

    #: 登记机关
    authority: Optional[str] = None

    #: 注册地址
    reg_location: Optional[str] = None

    #: 营业状态
    reg_status: Optional[str] = None

    #: 经营范围
    business_scope: Optional[str] = None

    #: 成立日期
    establish_time: Optional[str] = None

    #: 核准日期
    approved_time: Optional[str] = None

    #: 营业期限始
    term_start: Optional[str] = None

    #: 营业期限至
    term_end: Optional[str] = None

    #: 更新时间
    last_updated_time: Optional[str] = None

    #: 企业历史名称
    history_names: Optional[str] = None

    #: 行业门类
    industry: Optional[EnterpriseBaseInfoIndustry] = None

    #: 联系方式，地址、电话、邮箱、官网
    contacts: Optional[EnterpriseBaseInfoContacts] = None


@dataclass
class EnterpriseBaseInfoIndustry(Model):
    #: 行业门类描述
    industry: Optional[str] = None

    #: 行业门类code
    industry_code: Optional[str] = None

    #: 行业大类描述
    sub_industry: Optional[str] = None

    #: 行业大类code
    sub_industry_code: Optional[str] = None

    #: 行业中类描述
    middle_category: Optional[str] = None

    #: 行业中类code
    middle_category_code: Optional[str] = None

    #: 行业小类描述
    small_category: Optional[str] = None

    #: 行业小类code
    small_category_code: Optional[str] = None


@dataclass
class EnterpriseBaseInfoContacts(Model):
    #: 地址
    address: Optional[List[EnterpriseBaseInfoNote]] = None

    #: 电话号码
    phone_number: Optional[List[EnterpriseBaseInfoNote]] = None

    #: 邮箱
    email: Optional[List[EnterpriseBaseInfoNote]] = None

    #: 官网
    website: Optional[List[EnterpriseBaseInfoNote]] = None


@dataclass
class EnterpriseBaseInfoNote(Model):
    #: 备注
    note: Optional[str] = None

    #: 值
    value: Optional[str] = None


@dataclass
class EnterpriseContactsInfoResult(Model):
    """企业联系人信息返回结果。"""

    #: 1:查询成功，有数据 2:查询成功，无数据
    result: Optional[int] = None

    #: 查询数据
    info: Optional[EnterpriseContactsInfoInfo] = None


@dataclass
class EnterpriseContactsInfoInfo(Model):
    #: 邮箱
    emails: Optional[str] = None

    #: 公司 id
    company_id: Optional[str] = None

    #: 公司名称
    company_name: Optional[str] = None

    #: 联系方式
    phones: Optional[str] = None

    #: 企业关键人
    key_person_name: Optional[str] = None


@dataclass
class EnterpriseLikeResult(Model):
    """企业工商信息模糊查询返回结果。"""

    #: 查询总条数
    total: Optional[int] = None

    #: 查询数据
    items: Optional[List[EnterpriseLikeItem]] = None


@dataclass
class EnterpriseLikeItem(Model):
    reg_status1: Optional[str] = None

    reg_status2: Optional[str] = None

    establish_time: Optional[str] = None

    reg_capital: Optional[str] = None

    company_type: Optional[str] = None

    company_name: Optional[str] = None

    type: Optional[int] = None

    legal_person_name: Optional[str] = None

    reg_number: Optional[str] = None

    credit_code: Optional[str] = None

    org_number: Optional[str] = None

    province: Optional[str] = None


@dataclass
class EnterpriseNameLikeResult(Model):
    """企业名称模糊查询返回结果。"""

    #: 查询总条数
    total: Optional[int] = None

    #: 查询数据
    items: Optional[List[EnterpriseNameLikeItem]] = None


@dataclass
class EnterpriseNameLikeItem(Model):
    company_status: Optional[str] = None

    credit_nno: Optional[str] = None

    company_name: Optional[str] = None

    company_code: Optional[str] = None

    history_name: Optional[List[str]] = None


@dataclass
class EnterpriseReportResult(Model):
    """企业工商年报信息返回结果。"""

    total: Optional[int] = None

    items: Optional[List[EnterpriseReportItem]] = None


@dataclass
class EnterpriseReportItem(Model):
    stock_chang_list: Optional[List[EnterpriseReportStockChang]] = None

    invest_info_list: Optional[List[EnterpriseReportInvestInfo]] = None

    partner_list: Optional[List[EnterpriseReportPartner]] = None

    year: Optional[str] = None

    provide_assurance_list: Optional[List[EnterpriseReportProvideAssurance]] = None

    has_detail_info: Optional[bool] = None

    change_list: Optional[List[EnterpriseReportChange]] = None

    publish_date: Optional[str] = None

    assets_data: Optional[List[EnterpriseReportAssetsData]] = None

    web_site_list: Optional[List[EnterpriseReportWebSite]] = None

    social_security: Optional[List[EnterpriseReportSocialSecurity]] = None

    basic_info_data: Optional[EnterpriseReportBasicInfoData] = None


@dataclass
class EnterpriseReportStockChang(Model):
    before: Optional[str] = None

    change_date: Optional[str] = None

    name: Optional[str] = None

    after: Optional[str] = None


@dataclass
class EnterpriseReportInvestInfo(Model):
    reg_no: Optional[str] = None

    credit_code: Optional[str] = None

    name: Optional[str] = None


@dataclass
class EnterpriseReportPartner(Model):
    should_date: Optional[str] = None

    real_type: Optional[str] = None

    should_type: Optional[str] = None

    real_capi: Optional[str] = None

    name: Optional[str] = None

    should_capi: Optional[str] = None

    real_date: Optional[str] = None


@dataclass
class EnterpriseReportProvideAssurance(Model):
    assurance_durn: Optional[str] = None

    assurance_type: Optional[str] = None

    assurance_scope: Optional[str] = None

    creditor: Optional[str] = None

    debtor: Optional[str] = None

    creditor_category: Optional[str] = None

    creditor_amount: Optional[str] = None

    fulfill_obligation: Optional[str] = None


@dataclass
class EnterpriseReportChange(Model):
    change_name: Optional[str] = None

    before: Optional[str] = None

    after: Optional[str] = None

    change_date: Optional[str] = None


@dataclass
class EnterpriseReportAssetsData(Model):
    banking_credit: Optional[str] = None

    main_business_income: Optional[str] = None

    government_subsidy: Optional[str] = None

    total_profit: Optional[str] = None

    total_assets: Optional[str] = None

    total_liabilities: Optional[str] = None

    total_owners_equity: Optional[str] = None

    gross_trading_income: Optional[str] = None

    total_tax_amount: Optional[str] = None

    net_profit: Optional[str] = None


@dataclass
class EnterpriseReportWebSite(Model):
    web_site: Optional[str] = None

    name: Optional[str] = None

    type: Optional[str] = None


@dataclass
class EnterpriseReportSocialSecurity(Model):
    insurance_amount: Optional[str] = None

    insurance_real_capital: Optional[str] = None

    insurance_name: Optional[str] = None

    insurance_base: Optional[str] = None

    insurance_arrearage: Optional[str] = None


@dataclass
class EnterpriseReportBasicInfoData(Model):
    reg_no: Optional[str] = None

    address: Optional[str] = None

    has_provide_assurance: Optional[str] = None

    operation_duration: Optional[str] = None

    company_name: Optional[str] = None

    main_type: Optional[str] = None

    operator_name: Optional[str] = None

    employee_count: Optional[str] = None

    has_web_site: Optional[str] = None

    email_address: Optional[str] = None

    belong_to: Optional[str] = None

    post_code: Optional[str] = None

    has_new_stock_or_by_stock: Optional[str] = None

    is_stock_right_transfer: Optional[str] = None

    capital_amount: Optional[str] = None

    contact_no: Optional[str] = None

    status: Optional[str] = None

    operation_places: Optional[str] = None
