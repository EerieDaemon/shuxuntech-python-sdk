"""强类型接口的路径、参数与返回模型测试。"""

from __future__ import annotations

import unittest
from typing import Any, Optional, Tuple, Type

from shuxuntech.api import (
    BankcardApi,
    EnterpriseApi,
    ExpressApi,
    IdentityApi,
    IpApi,
    MobileApi,
    OcrApi,
    VehicleApi,
)
from shuxuntech.models import (
    BankPlaceResult,
    Bankcard234Result,
    BankcardOcrResult,
    BusinessOcrResult,
    CarFiveResult,
    DrivingOcrResult,
    Enterprise2Result,
    Enterprise3Result,
    Enterprise4Result,
    EnterpriseBaseInfoResult,
    EnterpriseContactsInfoResult,
    EnterpriseLikeResult,
    EnterpriseNameLikeResult,
    EnterpriseReportResult,
    FaceCompareResult,
    FaceIdCardResult,
    IdCardCheckResult,
    IdCardOcrResult,
    IpQueryCityResult,
    LivingCheckResult,
    Mobile23Result,
    MobileEmptyResult,
    MobileEmptyResultV2,
    MobileOnlineResult,
    MobileStatusResult,
    MobileTransformResult,
    PlateOcrResult,
    VehicleOcrResult,
    Vin2_1Result,
    Vin5Result,
    VinOcrResult,
    WordOcrResult,
)

from .support import RecordingClient

Case = Tuple[str, str, Tuple[Any, ...], str, dict, Optional[Type[Any]]]

CASES: list[Case] = [
    # 身份核验
    ("identity", "id_card_check", ("张三", "110101199001011234"), "/v1/idCard/check",
     {"name": "张三", "idCard": "110101199001011234"}, IdCardCheckResult),
    ("identity", "face_id_card_check", ("张三", "110101", "base64"), "/v1/faceIdCard/check",
     {"name": "张三", "idCard": "110101", "image": "base64"}, FaceIdCardResult),
    ("identity", "face_compare", ("img1", "img2"), "/v1/faceCompare/check",
     {"image1": "img1", "image2": "img2"}, FaceCompareResult),
    ("identity", "living_check", ("img1",), "/v1/living/check",
     {"image1": "img1"}, LivingCheckResult),
    # 运营商
    ("mobile", "mobile2_check", ("张三", "13800000000"), "/v1/mobile2/check",
     {"name": "张三", "mobile": "13800000000"}, Mobile23Result),
    ("mobile", "mobile3_check", ("张三", "13800000000", "110101"), "/v1/mobile3/check",
     {"name": "张三", "mobile": "13800000000", "idCard": "110101"}, Mobile23Result),
    ("mobile", "mobile_empty_check", ("13800000000",), "/v1/mobileEmpty/check",
     {"mobile": "13800000000"}, MobileEmptyResult),
    ("mobile", "mobile_empty_check_v2", ("13800000000",), "/v1/mobileEmpty/check/v2",
     {"mobile": "13800000000"}, MobileEmptyResultV2),
    ("mobile", "mobile_empty_check_v3", ("13800000000",), "/v1/mobileEmpty/check/v3",
     {"mobile": "13800000000"}, MobileEmptyResultV2),
    ("mobile", "mobile_online_query", ("13800000000",), "/v1/mobileOnline/query",
     {"mobile": "13800000000"}, MobileOnlineResult),
    ("mobile", "mobile_status_query", ("13800000000",), "/v1/mobileStatus/query",
     {"mobile": "13800000000"}, MobileStatusResult),
    ("mobile", "mobile_transform_query", ("13800000000",), "/v1/mobileTransform/query",
     {"mobile": "13800000000"}, MobileTransformResult),
    # 银行卡
    ("bankcard", "bankcard2_check", ("张三", "622202"), "/v1/bankcard2/check",
     {"name": "张三", "bankcard": "622202"}, Bankcard234Result),
    ("bankcard", "bankcard3_check", ("张三", "622202", "110101"), "/v1/bankcard3/check",
     {"name": "张三", "bankcard": "622202", "idCard": "110101"}, Bankcard234Result),
    ("bankcard", "bankcard3_check_v2", ("张三", "622202", "13800000000"), "/v1/bankcard3/check/v2",
     {"name": "张三", "bankcard": "622202", "mobile": "13800000000"}, Bankcard234Result),
    ("bankcard", "bankcard4_check", ("张三", "622202", "110101", "13800000000"), "/v1/bankcard4/check",
     {"name": "张三", "bankcard": "622202", "idCard": "110101", "mobile": "13800000000"}, Bankcard234Result),
    ("bankcard", "bank_place_query", ("622202",), "/v1/bankPlace/query",
     {"bankcard": "622202"}, BankPlaceResult),
    ("bankcard", "ent_tax_status_query", ("acct", "bank", "企业"), "/v1/ent_tax_status/query",
     {"acctNo": "acct", "acctBank": "bank", "entName": "企业"}, None),
    # OCR
    ("ocr", "id_card_ocr", ("base64",), "/v1/idCard/ocr", {"image": "base64"}, IdCardOcrResult),
    ("ocr", "bankcard_ocr", ("base64", "https://img"), "/v1/bankcard/ocr",
     {"image": "base64", "imgUrl": "https://img"}, BankcardOcrResult),
    ("ocr", "business_ocr", (None, "https://img"), "/v1/business/ocr",
     {"imgUrl": "https://img"}, BusinessOcrResult),
    ("ocr", "driving_ocr", ("base64",), "/v1/driving/ocr", {"image": "base64"}, DrivingOcrResult),
    ("ocr", "plate_ocr", ("base64",), "/v1/plate/ocr", {"image": "base64"}, PlateOcrResult),
    ("ocr", "vehicle_ocr", ("base64", None, "BACK"), "/v1/vehicle/ocr",
     {"image": "base64", "cardSide": "BACK"}, VehicleOcrResult),
    ("ocr", "word_ocr", ("base64",), "/v1/word/ocr", {"image": "base64"}, WordOcrResult),
    ("ocr", "vin_ocr", ("base64",), "/v1/vin/ocr", {"image": "base64"}, VinOcrResult),
    # 企业
    ("enterprise", "enterprise2_check", ("数勋科技", "91330100"), "/v1/enterprise2/check",
     {"title": "数勋科技", "creditCode": "91330100"}, Enterprise2Result),
    ("enterprise", "enterprise3_check", ("数勋科技", "91330100", "张三"), "/v1/enterprise3/check",
     {"entName": "数勋科技", "creditCode": "91330100", "personName": "张三"}, Enterprise3Result),
    ("enterprise", "enterprise4_check", ("张三", "110101", "数勋科技", "91330100"), "/v1/enterprise4/check",
     {"fName": "张三", "fIdCard": "110101", "title": "数勋科技", "creditCode": "91330100"}, Enterprise4Result),
    ("enterprise", "enterprise_base_info_query", ("数勋科技",), "/v1/enterprise_base_info/query",
     {"keyword": "数勋科技"}, EnterpriseBaseInfoResult),
    ("enterprise", "enterprise_contacts_query", ("数勋科技",), "/v1/enterprise_contacts_info/query",
     {"keyword": "数勋科技"}, EnterpriseContactsInfoResult),
    ("enterprise", "enterprise_like_query", ("数勋科技", 2, 20), "/v1/enterprise_like/query",
     {"keyword": "数勋科技", "pageNo": "2", "pageSize": "20"}, EnterpriseLikeResult),
    ("enterprise", "enterprise_name_like_query", ("数勋科技", 10, 5), "/v1/enterprise_name_like/query",
     {"keyword": "数勋科技", "pageSize": "10", "limit": "5"}, EnterpriseNameLikeResult),
    ("enterprise", "enterprise_report_query", ("数勋科技",), "/v1/enterprise_report/query",
     {"keyword": "数勋科技"}, EnterpriseReportResult),
    ("enterprise", "ent_abnormal_query", ("数勋科技",), "/v1/ent_abnormal/query",
     {"keyword": "数勋科技"}, None),
    # 交通
    ("vehicle", "vin_query", ("VIN123",), "/v1/vin/query", {"vin": "VIN123"}, None),
    ("vehicle", "vin21_query", ("VIN123",), "/v1/vin2_1/query", {"vin": "VIN123"}, Vin2_1Result),
    ("vehicle", "vin3_query", ("VIN123",), "/v1/vin3/query", {"vin": "VIN123"}, None),
    ("vehicle", "vin4_custom_query", ("VIN123",), "/v1/vin4_custom/query", {"vin": "VIN123"}, None),
    ("vehicle", "vin5_query", ("VIN123",), "/v1/vin5/query", {"vin": "VIN123"}, Vin5Result),
    ("vehicle", "car_five_query", ("浙A12345",), "/v1/car_five/query", {"carNo": "浙A12345"}, CarFiveResult),
    ("vehicle", "car_brand_query", (), "/v1/car_brand/query", {}, None),
    ("vehicle", "car_series_query", ("1",), "/v1/car_series/query", {"brandId": "1"}, None),
    ("vehicle", "car_type_query", ("2", "price"), "/v1/car_type/query",
     {"seriesId": "2", "sort": "price"}, None),
    ("vehicle", "car_config_query", ("keyword",), "/v1/car_config/query", {"keyword": "keyword"}, None),
    ("vehicle", "car_detail_query", ("100",), "/v1/car_detail/query", {"carid": "100"}, None),
    # 生活服务
    ("express", "express_query", ("SF123",), "/v1/express/query", {"no": "SF123"}, None),
    ("express", "express_subscribe", ("SF123", "https://callback"), "/v1/express/subscribe",
     {"no": "SF123", "callbackUrl": "https://callback"}, None),
    # IP
    ("ip", "ip_query", ("1.1.1.1",), "/v1/ip_location/query", {"ip": "1.1.1.1"}, IpQueryCityResult),
    ("ip", "ipv6_query", ("::1",), "/v1/ip_location/query/ipv6", {"ip": "::1"}, IpQueryCityResult),
]


class TypedApiTest(unittest.TestCase):
    def test_all_methods_match_paths_and_models(self) -> None:
        self.assertEqual(len(CASES), 50)
        client = RecordingClient()
        services = {
            "identity": IdentityApi(client),  # type: ignore[arg-type]
            "mobile": MobileApi(client),  # type: ignore[arg-type]
            "bankcard": BankcardApi(client),  # type: ignore[arg-type]
            "ocr": OcrApi(client),  # type: ignore[arg-type]
            "enterprise": EnterpriseApi(client),  # type: ignore[arg-type]
            "vehicle": VehicleApi(client),  # type: ignore[arg-type]
            "express": ExpressApi(client),  # type: ignore[arg-type]
            "ip": IpApi(client),  # type: ignore[arg-type]
        }

        for service_name, method_name, args, path, form, model in CASES:
            with self.subTest(method=f"{service_name}.{method_name}"):
                service = services[service_name]
                method = getattr(service, method_name)
                response = method(*args)
                self.assertTrue(response.is_success)
                actual_path, actual_form, actual_model = client.calls[-1]
                self.assertEqual(actual_path, path)
                self.assertEqual(actual_form, form)
                self.assertIs(actual_model, model)

    def test_optional_arguments_are_omitted(self) -> None:
        client = RecordingClient()
        identity = IdentityApi(client)  # type: ignore[arg-type]
        identity.face_compare("img1")
        _, form, model = client.calls[-1]
        self.assertEqual(form, {"image1": "img1"})
        self.assertIs(model, FaceCompareResult)

    def test_each_service_is_reused(self) -> None:
        from shuxuntech import ShuxunClient

        real = ShuxunClient("k", "s", transport=RecordingClient())  # type: ignore[arg-type]
        self.assertIs(real.apis.identity, real.apis.identity)
        self.assertIsInstance(real.apis.identity, IdentityApi)


if __name__ == "__main__":
    unittest.main()
