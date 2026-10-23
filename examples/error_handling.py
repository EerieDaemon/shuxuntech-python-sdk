"""异常处理示例：区分业务错误、传输错误与成功响应。

运行前设置环境变量 SHUXUN_APP_KEY、SHUXUN_APP_SECRET。
"""

from __future__ import annotations

import os

from shuxuntech import ShuxunApiError, ShuxunClient, ShuxunTransportError
from shuxuntech.models import IdCardCheckResult


def main() -> None:
    app_key = os.environ.get("SHUXUN_APP_KEY")
    app_secret = os.environ.get("SHUXUN_APP_SECRET")
    if not app_key or not app_secret:
        raise SystemExit("请先设置 SHUXUN_APP_KEY 和 SHUXUN_APP_SECRET")

    params = {"name": "张三", "idCard": "110101199001011234"}

    with ShuxunClient(app_key, app_secret, read_timeout=10) as client:
        # 方式一：不抛异常，按返回码判断
        response = client.post("/v1/idCard/check", params, IdCardCheckResult)
        if not response.is_success:
            print(f"业务失败：[{response.code}] {response.msg}，seqNo={response.seq_no}")
            return

        # 方式二：code != 0 时抛 ShuxunApiError
        try:
            typed = client.post_or_throw(
                "/v1/idCard/check", params, result_type=IdCardCheckResult
            )
        except ShuxunApiError as exc:
            print(f"业务异常：[{exc.code}] {exc.msg}，seqNo={exc.seq_no}")
            return
        except ShuxunTransportError as exc:
            print(f"传输异常：HTTP {exc.http_status}，{exc}")
            print("原始响应：", exc.response_body)
            return

        print("成功：", typed.data)


if __name__ == "__main__":
    main()
