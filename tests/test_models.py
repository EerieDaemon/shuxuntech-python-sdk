"""强类型响应模型测试。"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Optional

from shuxuntech.models import (
    Enterprise2Result,
    EnterpriseBaseInfoResult,
    EnterpriseNameLikeResult,
    EnterpriseReportResult,
    FaceCompareResult,
    IdCardCheckResult,
    IdCardCommonResult,
    Model,
    Vin2_1Result,
    WordOcrResult,
)


class IdCardModelTest(unittest.TestCase):
    def test_parses_inherited_fields(self) -> None:
        result = IdCardCheckResult.from_dict(
            {
                "result": 1,
                "resultDesc": "核验一致",
                "birthday": "19930123",
                "gender": 1,
                "age": 32,
                "province": "浙江省",
                "city": "杭州市",
                "district": "余杭区",
                "area": "浙江杭州",
                "unknownField": "ignored",
            }
        )
        self.assertEqual(result.result, 1)
        self.assertEqual(result.result_desc, "核验一致")
        self.assertEqual(result.birthday, "19930123")
        self.assertEqual(result.gender, 1)
        self.assertFalse(hasattr(result, "unknownField"))

    def test_derives_result_desc_when_absent(self) -> None:
        self.assertEqual(IdCardCheckResult.from_dict({"result": 1}).result_desc, "核验一致")
        self.assertEqual(IdCardCheckResult.from_dict({"result": 2}).result_desc, "核验不一致")
        self.assertEqual(IdCardCheckResult.from_dict({"result": 3}).result_desc, "无记录")

    def test_keeps_explicit_result_desc(self) -> None:
        result = IdCardCheckResult.from_dict({"result": 1, "resultDesc": "自定义描述"})
        self.assertEqual(result.result_desc, "自定义描述")

    def test_accepts_snake_case_keys(self) -> None:
        result = IdCardCheckResult.from_dict({"result_desc": "自定义"})
        self.assertEqual(result.result_desc, "自定义")

    def test_to_dict_round_trip(self) -> None:
        payload = {
            "result": 1,
            "resultDesc": "核验一致",
            "gender": 1,
            "province": "浙江省",
        }
        result = IdCardCheckResult.from_dict(payload)
        self.assertEqual(result.to_dict(), payload)

    def test_to_dict_omits_none(self) -> None:
        self.assertEqual(IdCardCommonResult().to_dict(), {})

    def test_scalar_coercion(self) -> None:
        result = IdCardCheckResult.from_dict({"result": "2", "gender": "0", "age": "32"})
        self.assertEqual(result.result, 2)
        self.assertEqual(result.gender, 0)
        self.assertEqual(result.age, 32)

    def test_enterprise2_derives_desc(self) -> None:
        self.assertEqual(
            Enterprise2Result.from_dict({"result": 2}).result_desc,
            "核验不一致",
        )


class NestedModelTest(unittest.TestCase):
    def test_enterprise_base_info(self) -> None:
        data = {
            "result": 1,
            "info": {
                "companyName": "杭州数勋科技有限公司",
                "creditCode": "91330100MA2XXXXXXX",
                "industry": {
                    "industry": "信息传输、软件和信息技术服务业",
                    "industryCode": "I",
                },
                "contacts": {
                    "address": [{"note": "注册地址", "value": "浙江省杭州市余杭区"}],
                    "phoneNumber": [{"note": "总机", "value": "0571-88888888"}],
                    "email": [{"note": "商务", "value": "hi@example.com"}],
                },
            },
        }
        result = EnterpriseBaseInfoResult.from_dict(data)
        self.assertIsNotNone(result.info)
        assert result.info is not None
        self.assertEqual(result.info.company_name, "杭州数勋科技有限公司")
        self.assertIsNotNone(result.info.industry)
        assert result.info.industry is not None
        self.assertEqual(result.info.industry.industry_code, "I")
        self.assertIsNotNone(result.info.contacts)
        assert result.info.contacts is not None
        self.assertEqual(len(result.info.contacts.address or []), 1)
        note = (result.info.contacts.address or [])[0]
        self.assertEqual(note.note, "注册地址")
        self.assertEqual(result.to_dict(), data)

    def test_word_ocr_uses_snake_case_json_keys(self) -> None:
        data = {
            "result": 1,
            "text_info": [
                {
                    "line_no": 1,
                    "confidence": 0.98,
                    "line_content": "数勋科技",
                    "line_position": {
                        "x": 10,
                        "width": 120,
                        "y": 20,
                        "height": 30,
                        "line_direction": 0,
                    },
                }
            ],
        }
        result = WordOcrResult.from_dict(data)
        self.assertIsNotNone(result.text_info)
        assert result.text_info is not None
        line = result.text_info[0]
        self.assertEqual(line.line_no, 1)
        self.assertEqual(line.confidence, 0.98)
        self.assertIsNotNone(line.line_position)
        assert line.line_position is not None
        self.assertEqual(line.line_position.x, 10)
        self.assertEqual(result.to_dict(), data)

    def test_list_of_strings(self) -> None:
        result = EnterpriseNameLikeResult.from_dict(
            {"total": 1, "items": [{"companyName": "数勋", "historyName": ["旧名一", "旧名二"]}]}
        )
        assert result.items is not None
        self.assertEqual(result.items[0].history_name, ["旧名一", "旧名二"])

    def test_face_compare_threshold(self) -> None:
        result = FaceCompareResult.from_dict(
            {
                "result": 1,
                "confidence": 88.5,
                "threshold": {"threshold1": 60, "threshold2": 70, "threshold3": 80},
            }
        )
        assert result.threshold is not None
        self.assertEqual(result.threshold.threshold3, 80.0)
        self.assertEqual(result.confidence, 88.5)

    def test_vin_vehicle_list(self) -> None:
        result = Vin2_1Result.from_dict(
            {
                "brand": "大众",
                "vehicle": [{"key": "排放标准", "value": "国六"}],
            }
        )
        assert result.vehicle is not None
        self.assertEqual(result.vehicle[0].key, "排放标准")

    def test_enterprise_report_deep_nesting(self) -> None:
        result = EnterpriseReportResult.from_dict(
            {
                "total": 1,
                "items": [
                    {
                        "year": "2024",
                        "hasDetailInfo": True,
                        "partnerList": [{"name": "张三", "shouldCapi": "100"}],
                        "basicInfoData": {"employeeCount": "50", "status": "存续"},
                    }
                ],
            }
        )
        assert result.items is not None
        item = result.items[0]
        self.assertTrue(item.has_detail_info)
        assert item.partner_list is not None
        self.assertEqual(item.partner_list[0].name, "张三")
        assert item.basic_info_data is not None
        self.assertEqual(item.basic_info_data.employee_count, "50")


class ModelContractTest(unittest.TestCase):
    def test_non_mapping_rejected(self) -> None:
        with self.assertRaises(TypeError):
            IdCardCheckResult.from_dict([])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            Model.from_dict({})  # type: ignore[arg-type]

    def test_custom_model(self) -> None:
        @dataclass
        class Custom(Model):
            request_id: Optional[str] = None
            count: Optional[int] = None

        value = Custom.from_dict({"requestId": "req-1", "count": "3"})
        self.assertEqual(value.request_id, "req-1")
        self.assertEqual(value.count, 3)
        self.assertEqual(value.to_dict(), {"requestId": "req-1", "count": 3})


if __name__ == "__main__":
    unittest.main()
