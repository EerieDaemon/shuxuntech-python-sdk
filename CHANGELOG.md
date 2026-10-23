# Changelog

本项目的版本变更记录，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [0.1.0] - 2026-10-23

首个公开版本。

### 新增

- `ShuxunClient`：自动生成 `appKey` / `timestamp` / `sign` 请求头，按
  `sha256(appKey + timestamp + appSecret)` 签名，表单提交并解析统一响应。
- `ApiResponse`：统一承载 `code` / `msg` / `data` / `seqNo` / `http_status` / `raw`。
- `Params`：保持插入顺序的链式参数集合，自动过滤 `None`、转换布尔与数字。
- 传输层抽象 `HttpTransport`，默认实现 `HttpClientTransport` 基于标准库
  `http.client`，零运行时依赖，支持连接 / 读取 / 写入超时。
- 异常体系：`ShuxunError`、`ShuxunApiError`、`ShuxunTransportError`。
- 返回码枚举 `ResponseCode` 与 `describe_response_code`。
- 34 个强类型响应模型，覆盖身份核验、运营商、银行卡、OCR、企业、交通、IP 归属地。
- 50 个强类型接口方法，按 8 个业务分类组织，通过 `client.apis` 获取。
  企业模糊查询返回对应的列表模型 `EnterpriseLikeResult` / `EnterpriseNameLikeResult`。
- 单元测试与基于本地回环 HTTP 服务器的集成测试，GitHub Actions CI。
- 中文 README 与 4 个可运行示例。
