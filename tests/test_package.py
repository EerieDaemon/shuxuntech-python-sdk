"""打包产物与公开入口测试。"""

from __future__ import annotations

import unittest
from importlib import resources

import shuxuntech
from shuxuntech import (
    ApiResponse,
    Params,
    ResponseCode,
    ShuxunApiError,
    ShuxunApis,
    ShuxunClient,
    ShuxunError,
    ShuxunTransportError,
)


class PackageTest(unittest.TestCase):
    def test_version_format(self) -> None:
        self.assertRegex(shuxuntech.__version__, r"^\d+\.\d+\.\d+$")

    def test_public_api(self) -> None:
        for name in (
            "ShuxunClient",
            "ShuxunApis",
            "ApiResponse",
            "Params",
            "ResponseCode",
            "ShuxunError",
            "ShuxunApiError",
            "ShuxunTransportError",
        ):
            self.assertTrue(hasattr(shuxuntech, name), name)
        self.assertIs(ResponseCode, shuxuntech.ResponseCodes)
        self.assertTrue(issubclass(ShuxunApiError, ShuxunError))
        self.assertTrue(issubclass(ShuxunTransportError, ShuxunError))
        self.assertIsNotNone(ShuxunApis)
        self.assertIsNotNone(ShuxunClient)
        self.assertIsNotNone(ApiResponse)
        self.assertIsNotNone(Params)

    def test_py_typed_marker_is_packaged(self) -> None:
        marker = resources.files("shuxuntech").joinpath("py.typed")
        self.assertTrue(marker.is_file())


if __name__ == "__main__":
    unittest.main()
