"""最简调用示例：身份证实名核验。

运行前设置环境变量：

    set SHUXUN_APP_KEY=your-app-key
    set SHUXUN_APP_SECRET=your-app-secret
    python examples/quickstart.py
"""

from __future__ import annotations

import json
import os

from shuxuntech import ShuxunClient


def main() -> None:
    app_key = os.environ.get("SHUXUN_APP_KEY")
    app_secret = os.environ.get("SHUXUN_APP_SECRET")
    if not app_key or not app_secret:
        raise SystemExit("请先设置 SHUXUN_APP_KEY 和 SHUXUN_APP_SECRET")

    with ShuxunClient(app_key, app_secret) as client:
        response = client.post(
            "/v1/idCard/check",
            {"name": "张三", "idCard": "110101199001011234"},
        )

        print(
            f"HTTP {response.http_status}, code={response.code}, "
            f"msg={response.msg}, seqNo={response.seq_no}"
        )
        print(json.dumps(response.data, ensure_ascii=False, indent=2))

        if not response.is_success:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
