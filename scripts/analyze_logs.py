"""
Cloud Web Defense Lab - Nginx Edge Log Analyzer

功能说明：
该脚本用于分析 Nginx Edge 层的 access.log 访问日志。

它会统计：

1. 总请求数量
2. HTTP 状态码分布，例如 200、403、429
3. 限流结果，例如 PASSED、REJECTED
4. 请求最多的客户端 IP
5. 基础安全解释，例如 WAF 拦截和限流是否生效

适用场景：
该脚本用于 Cloud Web Defense Lab 项目中，
帮助证明 Nginx Edge、Rate Limiting、WAF 安全防护是否正常工作。
"""

# Counter 是 Python 标准库中的计数器工具

# 它可以方便地统计某个值出现了多少次

# 例如统计 200、403、429 分别出现了多少次

from collections import Counter

# re 是 Python 的正则表达式模块

# 用于从 Nginx 日志文本中提取 status=xxx、limit=xxx、客户端 IP 等信息

import re

# Path 是 pathlib 模块中的路径处理工具

# 相比普通字符串路径，Path 更清晰、更适合文件操作

from pathlib import Path

# 指定 Nginx Edge 访问日志文件的位置

# 这里假设日志文件存放在项目目录下的 logs/nginx/access.log

log_path = Path("logs/nginx/access.log")

# 在读取日志之前，先检查日志文件是否存在

# 如果文件不存在，直接提示错误并退出程序

# 这样可以避免后面 open 文件时报错

if not log_path.exists():
print("No Nginx access log found.")
exit(1)

# 用于统计不同 HTTP 状态码出现的次数

# 例如：

# 200 -> 正常请求成功

# 403 -> 请求被 WAF 或安全规则阻断

# 429 -> 请求被 Nginx 限流策略拒绝

status_counter = Counter()

# 用于统计限流结果

# 例如：

# PASSED   -> 请求通过限流检查

# REJECTED -> 请求被限流策略拒绝

limit_counter = Counter()

# 用于统计客户端 IP 的请求次数

# 可以帮助我们观察哪些 IP 产生了最多请求

ip_counter = Counter()

# 用于统计总请求数量

# 每读取一行日志，就代表处理了一个请求

total_requests = 0

# 定义用于提取 HTTP 状态码的正则表达式

# 该表达式会匹配类似 status=200、status=403、status=429 的内容

# (\d+) 表示提取一个或多个数字

status_pattern = re.compile(r"status=(\d+)")

# 定义用于提取限流结果的正则表达式

# 该表达式会匹配类似 limit=PASSED、limit=REJECTED 的内容

# [A-Z_]+ 表示提取由大写字母和下划线组成的值

limit_pattern = re.compile(r"limit=([A-Z_]+)")

# 定义用于提取客户端 IP 的正则表达式

# ^ 表示从每一行开头开始匹配

# \S+ 表示一个或多个非空白字符

# 这里默认日志每一行的第一个字段是客户端 IP

ip_pattern = re.compile(r"^(\S+)")

# 打开 Nginx access.log 日志文件

# "r" 表示只读模式

# encoding="utf-8" 表示使用 UTF-8 编码读取文件

# errors="ignore" 表示遇到无法识别的字符时忽略，避免程序中断

with log_path.open("r", encoding="utf-8", errors="ignore") as f:

```
# 逐行读取日志文件
# Nginx access.log 通常是一行代表一次 HTTP 请求
for line in f:

    # 每处理一行，说明发现一个请求，总请求数加 1
    total_requests += 1

    # 从当前日志行中提取客户端 IP
    ip_match = ip_pattern.search(line)

    # 如果成功提取到 IP，则将该 IP 的请求次数加 1
    if ip_match:
        ip_counter[ip_match.group(1)] += 1

    # 从当前日志行中提取 HTTP 状态码
    status_match = status_pattern.search(line)

    # 如果成功提取到状态码，则将该状态码的出现次数加 1
    if status_match:
        status_counter[status_match.group(1)] += 1

    # 从当前日志行中提取限流结果
    limit_match = limit_pattern.search(line)

    # 如果成功提取到限流结果，则将该结果的出现次数加 1
    if limit_match:
        limit_counter[limit_match.group(1)] += 1
```

# 打印报告分隔线

# "=" * 60 表示输出 60 个等号，让报告更清晰

print("=" * 60)
print("Cloud Web Defense Lab - Nginx Edge Log Report")
print("=" * 60)

# 输出总请求数量

print(f"Total requests: {total_requests}")

# 输出 HTTP 状态码分布

# most_common() 会按照出现次数从多到少排序

print("\nHTTP status distribution:")
for status, count in status_counter.most_common():
print(f"  {status}: {count}")

# 输出限流结果统计

# 例如：

# REJECTED: 445

# PASSED: 68

print("\nRate limit result:")
for result, count in limit_counter.most_common():
print(f"  {result}: {count}")

# 输出请求次数最多的前 5 个客户端 IP

# 这可以帮助我们识别主要请求来源

print("\nTop client IPs:")
for ip, count in ip_counter.most_common(5):
print(f"  {ip}: {count}")

# 输出基础安全解释

print("\nBasic security interpretation:")

# 从状态码统计中取出 403 的数量

# 403 Forbidden 通常表示请求被 WAF 或安全规则阻断

# 如果没有 403，则默认数量为 0

blocked = int(status_counter.get("403", 0))

# 从状态码统计中取出 429 的数量

# 429 Too Many Requests 通常表示请求触发了限流策略

# 如果没有 429，则默认数量为 0

rate_limited = int(status_counter.get("429", 0))

# 如果存在 403 响应，说明观察到了 WAF 或安全规则阻断行为

if blocked > 0:
print(f"  WAF/security blocking observed: {blocked} requests returned 403.")

# 如果存在 429 响应，说明观察到了 Anti-DDoS 或限流行为

if rate_limited > 0:
print(f"  Anti-DDoS/rate limiting observed: {rate_limited} requests returned 429.")

# 如果既没有 403，也没有 429

# 说明当前日志中还没有明显的安全拦截或限流现象

if blocked == 0 and rate_limited == 0:
print("  No obvious blocked or rate-limited traffic observed yet.")

# 打印报告结束分隔线

print("=" * 60)
