"""强类型接口示例：直接调用 client.apis 下封装好的方法。

运行前设置环境变量 SHUXUN_APP_KEY、SHUXUN_APP_SECRET。
"""

from __future__ import annotations

import os

from shuxuntech import ShuxunClient


def main() -> None:
    app_key = os.environ.get("SHUXUN_APP_KEY")
    app_secret = os.environ.get("SHUXUN_APP_SECRET")
    if not app_key or not app_secret:
        raise SystemExit("请先设置 SHUXUN_APP_KEY 和 SHUXUN_APP_SECRET")

    with ShuxunClient(app_key, app_secret) as client:
        id_card = client.apis.identity.id_card_check("张三", "110101199001011234")
        print("实名核验：", id_card.code_description, id_card.data)

        bankcard = client.apis.bankcard.bankcard3_check(
            "张三", "6222020000000000000", "110101199001011234"
        )
        print("银行卡三要素：", bankcard.code_description, bankcard.data)

        ip_info = client.apis.ip.ip_query("1.1.1.1")
        print("IP 归属地：", ip_info.code_description, ip_info.data)


if __name__ == "__main__":
    main()
