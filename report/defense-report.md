## 4. 测试用例

### 4.1 正常访问测试

**测试目标：**
验证正常用户请求能够通过 Nginx Edge 层和 WAF 层，并成功访问后端 Flask 源站应用。

**测试命令：**

```bash
curl -i http://localhost:8080/
```

**预期结果：**

```text
HTTP/1.1 200 OK
```

**说明：**
该测试用于确认整体访问链路正常，即客户端请求能够依次经过 Edge 反向代理、WAF 检测层，并最终到达 Origin Flask 应用。

---

### 4.2 健康检查测试

**测试目标：**
验证后端源站应用是否处于正常运行状态。

**测试命令：**

```bash
curl -i http://localhost:8080/health
```

**预期结果：**

```text
HTTP/1.1 200 OK
{"status":"ok","service":"origin-app"}
```

**说明：**
`/health` 接口用于服务健康检查，可用于确认 Origin 应用是否正常启动，并能够被 Edge/WAF 层正确转发访问。

---

### 4.3 XSS 攻击拦截测试

**测试目标：**
验证 ModSecurity WAF 与 OWASP Core Rule Set 是否能够识别并阻断跨站脚本攻击请求。

**测试命令：**

```bash
curl -i "http://localhost:8080/search?q=<script>alert(1)</script>"
```

**预期结果：**

```text
HTTP/1.1 403 Forbidden
```

**说明：**
该请求在 `q` 参数中注入典型 XSS Payload。WAF 应识别该请求存在恶意脚本注入风险，并在请求到达后端 Flask 应用之前将其阻断。

---

### 4.4 SQL 注入攻击拦截测试

**测试目标：**
验证 WAF 是否能够检测并阻断常见 SQL Injection 类型的恶意请求。

**测试命令：**

```bash
curl -i "http://localhost:8080/search?q=' OR '1'='1"
```

**预期结果：**

```text
HTTP/1.1 403 Forbidden
```

**说明：**
该请求模拟常见 SQL 注入攻击语句。OWASP CRS 应根据规则匹配和异常评分机制识别该请求，并由 ModSecurity 在阻断模式下返回拒绝访问响应。

---

### 4.5 请求限速测试

**测试目标：**
验证 Nginx Edge 层是否能够对来自同一 IP 的高频请求进行限制。

**测试命令：**

```bash
for i in {1..30}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/; done
```

**预期结果：**

```text
部分请求返回 200
超出限制的请求返回 429 Too Many Requests
```

**说明：**
该测试通过短时间内连续发送多个请求，模拟异常高频访问行为。Nginx Edge 层应根据配置的限速策略，对超过阈值的请求进行限制，从而降低恶意流量或异常访问对后端服务的影响。

---

## 5. 测试结果汇总

| 测试项目     | 预期结果     | 实际结果     | 测试状态 |
| -------- | -------- | -------- | ---- |
| 正常访问测试   | HTTP 200 | HTTP 200 | 通过   |
| 健康检查测试   | HTTP 200 | HTTP 200 | 通过   |
| XSS 攻击测试 | HTTP 403 | HTTP 403 | 通过   |
| SQL 注入测试 | HTTP 403 | HTTP 403 | 通过   |
| 请求限速测试   | HTTP 429 | HTTP 429 | 通过   |

通过以上测试可以看出，该实验环境能够正确放行正常请求，同时对典型 Web 攻击请求和异常高频请求进行有效拦截或限制。

---

## 6. 日志分析

本项目通过集中化日志观察 Edge 层、WAF 层和 Origin 应用的访问情况。

Nginx Access Log 用于记录正常请求、请求来源 IP、请求路径、HTTP 状态码以及响应结果。
Nginx Error Log 可用于观察限流、连接限制、请求超时等边缘防护事件。
ModSecurity Audit Log 用于记录被 WAF 规则命中的恶意请求，包括触发的 CRS 规则编号、异常评分、请求参数以及阻断原因。

通过日志分析，可以验证以下安全能力：

1. 正常请求能够被 Edge 层正确转发到后端应用。
2. 恶意请求会在 WAF 层被检测和阻断。
3. 高频请求会被 Nginx 限速策略限制。
4. 后端 Origin 应用不会直接暴露给外部访问者，从而降低源站被绕过防护直接攻击的风险。

---

## 7. 项目局限性

本实验是一个本地化模拟环境，主要用于展示云 Web 防护架构的基本思想和核心技术流程。相比真实云厂商级别的 Anti-DDoS、WAF 和 Unified Cloud Defense 产品，该实验仍存在以下局限：

1. 本项目未实现真实的大规模 DDoS 清洗能力。
2. 当前环境运行在本地 Docker 容器中，不代表真实云环境中的高可用部署。
3. Flask Origin 应用仅作为测试源站，业务逻辑较为简单。
4. 项目未实现生产级 TLS 证书管理与 HTTPS 终止。
5. 当前日志分析以本地日志为主，尚未接入专业 SIEM、告警系统或可视化监控平台。
6. WAF 规则主要基于 OWASP CRS，仍需要根据真实业务场景进行规则调优，以减少误报和漏报。

---

## 8. 项目总结

本项目构建了一个分层 Web 防护实验环境，通过 Nginx Edge、ModSecurity WAF、OWASP Core Rule Set 和 Flask Origin 应用模拟了云端 Web 防护平台的基本架构。

实验结果表明，该系统能够完成以下目标：

1. 使用 Nginx Edge 层对外暴露统一访问入口。
2. 对客户端请求进行请求频率限制、连接数控制和请求大小限制。
3. 使用 ModSecurity 与 OWASP CRS 对 HTTP 请求进行安全检测。
4. 阻断典型 XSS 和 SQL 注入攻击请求。
5. 隐藏后端 Flask 源站，避免攻击者绕过防护层直接访问源站服务。
6. 通过日志记录和分析观察正常访问、攻击拦截和限流事件。

总体而言，该实验展示了一个基础但完整的云 Web 防护思路：
**Edge 层负责流量控制，WAF 层负责应用层攻击检测，Origin 隔离负责保护源站安全。**

该架构体现了纵深防御思想，可以作为理解 Anti-DDoS、WAF、反向代理、源站保护和日志分析等云安全能力的基础实验项目。


# Cloud Web Defense Lab Report

## 1. Project Objective

This project simulates a cloud-based web defense platform inspired by Anti-DDoS, WAF, and Unified Cloud Defense products.

The goal is to protect an origin web application using:

- Nginx Edge reverse proxy
- HTTP rate limiting
- Connection limiting
- ModSecurity WAF
- OWASP Core Rule Set
- Centralized log analysis

## 2. Architecture

Client traffic first reaches the Nginx Edge layer.  
The Edge layer applies rate limiting and connection controls.  
Then traffic is forwarded to the WAF layer.  
The WAF inspects HTTP requests using OWASP CRS.  
Only clean requests are forwarded to the origin Flask application.

## 3. Security Controls

### 3.1 Edge Protection

Implemented with Nginx:

- Per-IP request rate limit
- Burst control
- Connection limit
- Header/body timeout
- Maximum body size limit

### 3.2 WAF Protection

Implemented with:

- ModSecurity
- OWASP Core Rule Set
- Blocking mode enabled
- Inbound anomaly threshold configured

Tested against:

- XSS payload
- SQL Injection payload

### 3.3 Origin Protection

The origin app is not directly exposed to the host machine.  
Only the Edge service exposes port 8080.

## 4. Test Cases

### Normal Request

Expected result: HTTP 200

```bash
curl -i http://localhost:8080/
XSS Test
Expected result: HTTP 403 Forbidden

curl -i "http://localhost:8080/search?q=<script>alert(1)</script>"

SQL Injection Test
Expected result: HTTP 403 Forbidden

curl -i "http://localhost:8080/search?q=' OR '1'='1"

Rate Limiting Test
Expected result: Some requests should be blocked with HTTP 429 Too Many Requests

for i in {1..30}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/; done

