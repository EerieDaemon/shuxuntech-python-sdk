"""Params 测试。"""

from __future__ import annotations

import unittest

from shuxuntech.params import Params, stringify_param


class ParamsTest(unittest.TestCase):
    def test_chained_put_keeps_order(self) -> None:
        params = Params.create().put("name", "张三").put("idCard", "110101")
        self.assertEqual(params.as_dict(), {"name": "张三", "idCard": "110101"})
        self.assertEqual(list(params), ["name", "idCard"])

    def test_none_removes_parameter(self) -> None:
        params = Params.create().put("a", "1").put("a", None)
        self.assertEqual(params.as_dict(), {})
        self.assertEqual(len(params), 0)

    def test_values_are_stringified(self) -> None:
        params = (
            Params.create()
            .put("flag", True)
            .put("off", False)
            .put("count", 3)
            .put("ratio", 1.5)
        )
        self.assertEqual(
            params.as_dict(),
            {"flag": "true", "off": "false", "count": "3", "ratio": "1.5"},
        )

    def test_mapping_protocol(self) -> None:
        params = Params({"a": 1})
        self.assertIn("a", params)
        self.assertEqual(params["a"], "1")
        params["b"] = "2"
        del params["a"]
        self.assertEqual(params.as_dict(), {"b": "2"})

    def test_invalid_name_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Params.create().put("", "value")
        with self.assertRaises(ValueError):
            Params.create().put("   ", "value")

    def test_repr_hides_values(self) -> None:
        params = Params.create().put("idCard", "110101199001011234")
        self.assertEqual(repr(params), "Params(['idCard'])")
        self.assertNotIn("110101", repr(params))

    def test_bytes_rejected(self) -> None:
        with self.assertRaises(TypeError):
            Params.create().put("image", b"\x00")
        with self.assertRaises(TypeError):
            stringify_param(b"abc")


if __name__ == "__main__":
    unittest.main()
