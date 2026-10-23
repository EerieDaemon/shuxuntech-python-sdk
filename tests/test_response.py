"""响应与返回码测试。"""

from __future__ import annotations

import unittest

from shuxuntech import ApiResponse, ResponseCode, describe_response_code


class ApiResponseTest(unittest.TestCase):
    def test_success(self) -> None:
        response = ApiResponse(code=0, msg="成功", data={"ok": True}, seq_no="seq-1")
        self.assertTrue(response.is_success)
        self.assertEqual(response.code_description, "成功")
        self.assertIn("seq-1", str(response))

    def test_failure(self) -> None:
        response = ApiResponse(code=2, msg="无记录")
        self.assertFalse(response.is_success)
        self.assertEqual(response.code_description, "无记录")

    def test_missing_code_is_not_success(self) -> None:
        response = ApiResponse(code=None)
        self.assertFalse(response.is_success)
        self.assertEqual(response.code_description, "未知错误")


class ResponseCodeTest(unittest.TestCase):
    def test_descriptions(self) -> None:
        self.assertEqual(ResponseCode.SUCCESS.description, "成功")
        self.assertEqual(ResponseCode.PARAM_ERROR.description, "参数错误")
        self.assertEqual(ResponseCode.NO_RECORD.description, "无记录")
        self.assertEqual(ResponseCode.OTHER.description, "其他异常")
        self.assertEqual(describe_response_code(99), "其他异常")

    def test_unknown_codes(self) -> None:
        self.assertEqual(describe_response_code(12345), "未知错误")
        self.assertEqual(describe_response_code(None), "未知错误")

    def test_accepts_numeric_string(self) -> None:
        self.assertEqual(describe_response_code("4"), "签名错误")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
