"""签名工具测试。"""

from __future__ import annotations

import hashlib
import time
import unittest

from shuxuntech.auth import now_millis, sha256_hex, sign


class SignatureTest(unittest.TestCase):
    def test_known_vector(self) -> None:
        self.assertEqual(
            sign("test-app-key", "test-app-secret", 1700000000000),
            "64b8f3bb8eab6de2268be65cd84b0054a6dfd15d589460679d1ae887e384a1e3",
        )

    def test_matches_sha256_definition(self) -> None:
        expected = hashlib.sha256(
            b"test-app-key1700000000000test-app-secret"
        ).hexdigest()
        self.assertEqual(sign("test-app-key", "test-app-secret", 1700000000000), expected)

    def test_sha256_hex_supports_text_and_bytes(self) -> None:
        self.assertEqual(
            sha256_hex("abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )
        self.assertEqual(sha256_hex(b"abc"), sha256_hex("abc"))
        self.assertEqual(sha256_hex("张三"), hashlib.sha256("张三".encode()).hexdigest())

    def test_signature_is_lowercase_hex(self) -> None:
        value = sign("k", "s", 1)
        self.assertEqual(len(value), 64)
        self.assertEqual(value, value.lower())
        int(value, 16)

    def test_now_millis_is_ms(self) -> None:
        self.assertLess(abs(now_millis() - int(time.time() * 1000)), 2000)

    def test_non_string_credentials_rejected(self) -> None:
        with self.assertRaises(TypeError):
            sign(None, "secret", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sha256_hex(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
