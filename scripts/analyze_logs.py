from collections import Counter
import re
from pathlib import Path

log_path = Path("logs/nginx/access.log")

if not log_path.exists():
    print("No Nginx access log found.")
    exit(1)

status_counter = Counter()
limit_counter = Counter()
ip_counter = Counter()
total_requests = 0

status_pattern = re.compile(r"status=(\d+)")
limit_pattern = re.compile(r"limit=([A-Z_]+)")
ip_pattern = re.compile(r"^(\S+)")

with log_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        total_requests += 1

        ip_match = ip_pattern.search(line)
        if ip_match:
            ip_counter[ip_match.group(1)] += 1

        status_match = status_pattern.search(line)
        if status_match:
            status_counter[status_match.group(1)] += 1

        limit_match = limit_pattern.search(line)
        if limit_match:
            limit_counter[limit_match.group(1)] += 1

print("=" * 60)
print("Cloud Web Defense Lab - Nginx Edge Log Report")
print("=" * 60)

print(f"Total requests: {total_requests}")

print("\nHTTP status distribution:")
for status, count in status_counter.most_common():
    print(f"  {status}: {count}")

print("\nRate limit result:")
for result, count in limit_counter.most_common():
    print(f"  {result}: {count}")

print("\nTop client IPs:")
for ip, count in ip_counter.most_common(5):
    print(f"  {ip}: {count}")

print("\nBasic security interpretation:")

blocked = int(status_counter.get("403", 0))
rate_limited = int(status_counter.get("429", 0))

if blocked > 0:
    print(f"  WAF/security blocking observed: {blocked} requests returned 403.")

if rate_limited > 0:
    print(f"  Anti-DDoS/rate limiting observed: {rate_limited} requests returned 429.")

if blocked == 0 and rate_limited == 0:
    print("  No obvious blocked or rate-limited traffic observed yet.")

print("=" * 60)
