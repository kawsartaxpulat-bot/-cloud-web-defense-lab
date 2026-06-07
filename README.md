# Cloud Web Defense Lab

A containerized cloud web defense lab that simulates a layered web protection architecture using Nginx Edge, ModSecurity WAF, OWASP Core Rule Set, Docker, and Python log analysis.

This project is designed to demonstrate core capabilities related to:

- Anti-DDoS / HTTP flood mitigation
- Web Application Firewall protection
- Origin server hiding
- Reverse proxy based cloud defense
- Security log analysis
- Unified web defense reporting

---

## 1. Project Overview

The goal of this lab is to simulate a cloud-based web defense platform.

Client traffic first reaches an Nginx Edge reverse proxy.  
The Edge layer applies request rate limiting, connection limiting, and timeout hardening.  
Then requests are forwarded to a ModSecurity WAF container using OWASP Core Rule Set.  
Only clean traffic is forwarded to the origin Flask web application.

---

## 2. Architecture

```text
Client / curl / ab
        |
        v
+-----------------------------+
| Nginx Edge Layer             |
| - Reverse proxy              |
| - Request rate limiting      |
| - Connection limiting        |
| - Timeout hardening          |
| - Access logging             |
+-----------------------------+
        |
        v
+-----------------------------+
| WAF Layer                    |
| ModSecurity + OWASP CRS      |
| - SQL Injection detection    |
| - XSS detection              |
| - Malicious request blocking |
+-----------------------------+
        |
        v
+-----------------------------+
| Origin Web Application       |
| Flask Demo App               |
| - /                          |
| - /health                    |
| - /search?q=                 |
| - /login                     |
+-----------------------------+









```text
Client / curl / ab
        |
        v
+-----------------------------+
| Nginx Edge Layer             |
| - Reverse proxy              |
| - Request rate limiting      |
| - Connection limiting        |
| - Timeout hardening          |
| - Access logging             |
+-----------------------------+
        |
        v
+-----------------------------+
| WAF Layer                    |
| ModSecurity + OWASP CRS      |
| - SQL Injection detection    |
| - XSS detection              |
| - Malicious request blocking |
+-----------------------------+
        |
        v
+-----------------------------+
| Origin Web Application       |
| Flask Demo App               |
| - /                          |
| - /health                    |
| - /search?q=                 |
| - /login                     |
+-----------------------------+
Eof
