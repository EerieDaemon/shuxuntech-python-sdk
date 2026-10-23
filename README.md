# 数勋科技 Python SDK

[![CI](https://github.com/EerieDaemon/shuxuntech-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/EerieDaemon/shuxuntech-python-sdk/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

数勋科技开放平台（[shuxuntech.com](https://shuxuntech.com/)）的 Python SDK，封装了平台要求的签名鉴权、表单提交、统一响应解析与异常处理，让业务代码只关心参数和结果。

- 自动生成 `appKey` / `timestamp` / `sign` 请求头，按 `sha256(appKey + timestamp + appSecret)` 规则签名
- 参数按 `application/x-www-form-urlencoded` 提交，统一解析 `code` / `msg` / `data` / `seqNo`
- 支持原始 `dict` 返回和 dataclass 强类型映射（含嵌套对象、列表）
- 内置 34 个接口响应模型（`shuxuntech.models`），字段与平台契约保持一致
- 内置 50 个强类型接口方法，按身份核验、运营商、银行卡、OCR、企业、交通等分类
- 连接超时、读取超时、写入超时可配置；支持注入自定义传输层（代理、链路追踪、测试替身）
- 线程安全，全局复用一个实例即可；不自动重试，避免重复计费
- **零运行时依赖**，只用 Python 标准库，支持 Python 3.9+

## 环境要求

| 项目 | 要求 |
| --- | --- |
| Python | 3.9 及以上 |
| 依赖 | 无（`http.client` + `json` + `hashlib`） |

## 安装

当前从 GitHub 直接安装：

```bash
pip install "git+https://github.com/EerieDaemon/shuxuntech-python-sdk.git"
```

也可以先克隆再以可编辑模式安装，便于跟进源码：

```bash
git clone https://github.com/EerieDaemon/shuxuntech-python-sdk.git
cd shuxuntech-python-sdk
pip install -e .
```

> PyPI 包名已预留为 `shuxuntech`，发布后可直接 `pip install shuxuntech`。

## 快速开始

```python
import os

from shuxuntech import ShuxunClient

with ShuxunClient(
    app_key=os.environ["SHUXUN_APP_KEY"],
    app_secret=os.environ["SHUXUN_APP_SECRET"],
) as client:
    response = client.post(
        "/v1/idCard/check",  # 身份证实名核验
        {"name": "张三", "idCard": "110101199001011234"},
    )

    if response.is_success:
        print(response.data)
    else:
        print(f"调用失败：code={response.code} msg={response.msg} seqNo={response.seq_no}")
```

`appKey` 与 `appSecret` 请从环境变量、配置中心或密钥管理系统读取，不要硬编码进仓库。

## 强类型返回

SDK 内置了各接口的响应模型（`shuxuntech.models`），字段与平台契约一一对应，直接 `import` 即可：

```python
from shuxuntech.models import IdCardCheckResult

response = client.post(
    "/v1/idCard/check",
    {"name": "张三", "idCard": "110101199001011234"},
    result_type=IdCardCheckResult,
)

if response.is_success and response.data.result == 1:
    print("核验一致")  # result_desc 会在缺失时自动补全
```

已覆盖的模型（34 个）：

| 分类 | 模型 |
| --- | --- |
| 身份核验 | `IdCardCheckResult`、`IdCardCommonResult`、`FaceIdCardResult`、`FaceCompareResult`、`LivingCheckResult` |
| 运营商 | `Mobile23Result`、`MobileEmptyResult`、`MobileEmptyResultV2`、`MobileOnlineResult`、`MobileStatusResult`、`MobileTransformResult` |
| 银行卡 | `Bankcard234Result`、`BankcardOcrResult`、`BankPlaceResult` |
| OCR | `IdCardOcrResult`、`WordOcrResult`、`BusinessOcrResult`、`DrivingOcrResult`、`PlateOcrResult`、`VehicleOcrResult`、`VinOcrResult` |
| 企业 | `Enterprise2Result`、`Enterprise3Result`、`Enterprise4Result`、`EnterpriseBaseInfoResult`、`EnterpriseContactsInfoResult`、`EnterpriseLikeResult`、`EnterpriseNameLikeResult`、`EnterpriseReportResult` |
| 交通 | `Vin2Result`、`Vin2_1Result`、`Vin5Result`、`CarFiveResult` |
| 其他 | `IpQueryCityResult` |

未覆盖的接口可以不传 `result_type`，直接拿到原始 `dict` / `list`：

```python
response = client.post("/v1/xxx", {"keyword": "..."})
print(response.data["someField"])
```

也可以自定义模型，继承 `Model` 后即可自动完成 `camelCase` 字段映射、嵌套解析和未知字段忽略：

```python
from dataclasses import dataclass
from typing import List, Optional

from shuxuntech.models import Model


@dataclass
class Item(Model):
    request_id: Optional[str] = None
    count: Optional[int] = None
    tags: Optional[List[str]] = None


result = Item.from_dict({"requestId": "req-1", "count": 2, "tags": ["a"]})
print(result.request_id, result.to_dict())
```

## 强类型接口

在响应模型之上，SDK 按业务分类封装了 50 个强类型方法，路径和参数与平台 Controller 保持一致：

```python
# 身份证实名核验
resp = client.apis.identity.id_card_check("张三", "110101199001011234")

# 银行卡三要素
resp = client.apis.bankcard.bankcard3_check("张三", "622202...", "110101...")

# 通用文字 OCR：image 与 img_url 二选一
resp = client.apis.ocr.word_ocr(base64_image)

# 企业工商信息
resp = client.apis.enterprise.enterprise_base_info_query("杭州数勋科技有限公司")
```

| 分类 | 入口 | 方法数 |
| --- | --- | --- |
| 身份核验 | `client.apis.identity` | 4 |
| 运营商 | `client.apis.mobile` | 8 |
| 银行卡 | `client.apis.bankcard` | 6 |
| 文字识别 | `client.apis.ocr` | 8 |
| 企业服务 | `client.apis.enterprise` | 9 |
| 交通出行 | `client.apis.vehicle` | 11 |
| 生活服务 | `client.apis.express` | 2 |
| IP 归属地 | `client.apis.ip` | 2 |

接口路径与参数取自官方文档；返回结构不固定或没有内置模型的接口返回 `ApiResponse[Any]`，`data` 为原始 `dict`。

## 异常处理

平台在 HTTP 400/500 时同样会返回统一 JSON，SDK 不会因为状态码非 2xx 丢弃响应体：

| 场景 | 行为 |
| --- | --- |
| 网络不可达、连接超时 | 抛出 `ShuxunTransportError`，`http_status` 为 0 |
| HTTP 非 2xx，但响应体是平台统一结构（含 `code`） | 正常返回 `ApiResponse`，`http_status` 保存真实状态码，用 `code` 判断结果 |
| HTTP 非 2xx 且响应体不是平台结构（如网关的 HTML 错误页） | 抛出 `ShuxunTransportError`，可用 `http_status`、`response_body` 取状态码和原始响应 |
| HTTP 2xx 但响应不是合法 JSON | 抛出 `ShuxunTransportError`，`response_body` 为原始响应 |
| HTTP 2xx 但响应缺少 `code` 字段 | 返回 `ApiResponse`，`code` 为 `None`，`is_success` 为 `False` |
| 业务返回 `code != 0`，调用 `post` | 正常返回 `ApiResponse`，由调用方判断 `is_success` |
| 业务返回 `code != 0`，调用 `post_or_throw` | 抛出 `ShuxunApiError`，包含 `code`、`msg`、`seq_no`、`http_status` |

```python
response = client.post("/v1/idCard/check", params, result_type=IdCardCheckResult)

if not response.is_success:
    # HTTP 400/500 也可能走到这里，code、msg、seq_no 依然可用
    print(
        f"HTTP {response.http_status}, "
        f"code={response.code}({response.code_description}), "
        f"msg={response.msg}, seqNo={response.seq_no}"
    )
```

需要异常时改用 `post_or_throw`：

```python
from shuxuntech import ShuxunApiError, ShuxunTransportError

try:
    response = client.post_or_throw(
        "/v1/idCard/check", params, result_type=IdCardCheckResult
    )
except ShuxunApiError as exc:
    # 业务错误：参数、签名、余额、频率等
    print(exc.code, exc.msg, exc.seq_no)
except ShuxunTransportError as exc:
    # 网络或网关层错误，可按需重试
    print(exc.http_status, exc)
    print(exc.response_body)
```

## 配置项

| 构造参数 | 默认值 | 说明 |
| --- | --- | --- |
| `base_url` | `https://api.shuxuntech.com` | 网关地址，以控制台或接口文档为准 |
| `app_key` | 必填 | 控制台创建应用后分配 |
| `app_secret` | 必填 | 请勿提交到代码仓库 |
| `connect_timeout` | 5 秒 | 建连超时 |
| `read_timeout` | 15 秒 | 读取超时 |
| `write_timeout` | 15 秒 | 写入超时 |
| `transport` | `HttpClientTransport` | 自定义传输层，注入后由调用方负责关闭 |

```python
client = ShuxunClient(
    app_key="your-app-key",
    app_secret="your-app-secret",
    base_url="https://api.shuxuntech.com",
    connect_timeout=3,
    read_timeout=10,
)
```

## 签名与鉴权

平台要求每个请求在请求头中携带三个字段：

| Header | 说明 |
| --- | --- |
| `appKey` | 应用标识 |
| `timestamp` | 当前毫秒时间戳 |
| `sign` | `sha256(appKey + timestamp + appSecret)`，小写十六进制 |

`timestamp` 与服务端时间偏差超过 5 分钟会返回 `code = 4`（签名错误），部署前请确保服务器时间同步（例如启用 NTP）。SDK 会在每次请求时自动生成新的时间戳与签名。

需要自行排障时，可以直接调用签名工具：

```python
from shuxuntech.auth import sign

value = sign("appKey", "appSecret", 1700000000000)
```

## 返回码

| code | 含义 | 排查建议 |
| --- | --- | --- |
| 0 | 成功 | — |
| 1 | 参数错误 | 检查必填参数、格式 |
| 2 | 无记录 | 权威库未查到，属正常业务返回 |
| 3 | 第三方服务异常 | 上游通道波动，可重试或联系技术支持 |
| 4 | 签名错误 | 核对 appSecret、时间戳偏差 |
| 5 | 余额不足 | 充值或购买套餐 |
| 6 | 调用频率超限 | 降低并发或申请提升 QPS |
| 7 | 账号停用 | 联系客服 |
| 8 | 接口已停用 | 改用替代接口 |
| 9 | 未开通接口权限 | 控制台申请开通 |
| 10 | IP 不在白名单 | 控制台加入调用方 IP |
| 11 | 系统异常 | 携带 `seqNo` 联系技术支持 |
| 12 | 实名状态错误 | 先完成企业实名认证 |
| 99 | 其他异常 | 以 `msg` 为准 |

代码中可使用 `ResponseCode` 枚举或 `describe_response_code(code)`：

```python
from shuxuntech import ResponseCode, describe_response_code

print(ResponseCode.NO_RECORD.description)  # 无记录
print(describe_response_code(response.code))
```

完整说明见 [官方错误码文档](https://shuxuntech.com/help#errorcode)。

## 自定义传输层

默认传输层基于标准库 `http.client`：每个请求新建连接、不跟随重定向、不自动重试。需要统一代理、链路追踪或接入公司 HTTP 基础设施时，实现 `HttpTransport` 即可：

```python
from typing import Mapping

from shuxuntech import ShuxunClient
from shuxuntech.transport import HttpTransport, HttpResponse


class MyTransport(HttpTransport):
    def post(self, url: str, headers: Mapping[str, str], form: Mapping[str, str]) -> HttpResponse:
        # 在这里接入 requests、httpx 或内部网关
        ...


client = ShuxunClient("key", "secret", transport=MyTransport())
```

注入的传输层由调用方负责关闭，`client.close()` 不会关闭它。

## 线程安全与重试

- `ShuxunClient` 只保存不可变配置，可在多个线程间共享，建议作为单例使用，应用关闭时调用 `close()` 或使用 `with` 语句。
- SDK **不会自动重试**：平台接口通常按次计费，是否重试以及重试次数应由业务根据接口特性决定。
- 默认不输出日志；需要记录请求耗时或排障时，可通过自定义 `HttpTransport` 包装实现。

## 项目结构

```
shuxuntech-python-sdk
├── pyproject.toml
├── src/shuxuntech
│   ├── __init__.py             # 公开入口
│   ├── client.py               # 入口：签名、请求、响应解析
│   ├── apis.py                 # 强类型接口集合
│   ├── api/                    # 按业务分类的强类型接口（50 个方法）
│   ├── auth.py                 # SHA-256 签名工具
│   ├── transport.py            # 传输层抽象与标准库实现
│   ├── params.py               # Params、参数序列化
│   ├── response.py             # ApiResponse
│   ├── response_codes.py       # 返回码
│   ├── exceptions.py           # 业务异常与传输异常
│   └── models/                 # 34 个响应模型（含嵌套类）
├── tests/                      # 单元测试与本地 HTTP 集成测试
├── examples/                   # 可运行示例
└── .github/workflows/ci.yml    # GitHub Actions
```

## 本地开发

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -e ".[dev]"
python -m unittest discover -s tests -t . -v   # 运行测试
python -m build                                 # 构建 sdist / wheel
python -m twine check dist/*                    # 检查包元数据
```

发布新版本：

```bash
# 1. 更新 pyproject.toml 与 src/shuxuntech/_version.py
# 2. 提交并打 tag
git tag v0.1.0
git push origin main --tags
# 3. 构建并上传（需要 PyPI API Token）
python -m build
python -m twine upload dist/*
```

## 后续计划

- [x] 核心客户端、签名、统一响应与异常
- [x] 34 个响应模型与 50 个强类型接口
- [ ] 发布到 PyPI
- [ ] 提供 asyncio 异步客户端
- [ ] 支持文件上传（multipart）类 OCR 接口
- [ ] 补充各接口的请求参数模型与文档链接

## 关于数勋科技

[杭州数勋科技有限公司](https://shuxuntech.com/) 提供企业级数据 API 服务，覆盖身份核验、运营商、银行卡、文字识别、企业工商、交通出行、生活服务等 8 大类 200+ 标准化接口，平均响应 200ms 以内、服务可用性 99.9%，支持免费试用与 7×24 小时技术支持。

| 入口 | 地址 |
| --- | --- |
| 官网 | https://shuxuntech.com/ |
| API 市场 | https://shuxuntech.com/product |
| 帮助文档 | https://shuxuntech.com/help |
| 控制台 | https://platform.shuxuntech.com/ |

注册并完成企业认证后可领取免费调用额度，本 SDK 覆盖的接口在控制台开通后即可调用；遇到接入问题可直接联系技术支持。

## 许可证

[Apache License 2.0](LICENSE)
