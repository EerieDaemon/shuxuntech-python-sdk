"""强类型模型示例：把 data 解析为 IdCardCheckResult。

运行前设置环境变量 SHUXUN_APP_KEY、SHUXUN_APP_SECRET。
"""

from __future__ import annotations

import os

from shuxuntech import ShuxunClient
from shuxuntech.models import IdCardCheckResult


def main() -> None:
    app_key = os.environ.get("SHUXUN_APP_KEY")
    app_secret = os.environ.get("SHUXUN_APP_SECRET")
    if not app_key or not app_secret:
        raise SystemExit("请先设置 SHUXUN_APP_KEY 和 SHUXUN_APP_SECRET")

    with ShuxunClient(app_key, app_secret) as client:
        response = client.post(
            "/v1/idCard/check",
            {"name": "张三", "idCard": "110101199001011234"},
            result_type=IdCardCheckResult,
        )

        if not response.is_success:
            raise SystemExit(f"调用失败：{response}")

        result = response.data
        assert result is not None
        print("核验结果：", result.result_desc)
        print("生日：", result.birthday)
        print("性别：", "男" if result.gender == 1 else "女")
        print("地区：", result.province, result.city, result.district)


if __name__ == "__main__":
    main()
