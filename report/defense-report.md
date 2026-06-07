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

