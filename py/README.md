# 测试与诊断工具集 / Python Test & Diagnostic Suite 🧪

> **[中文说明 (Chinese)](#中文说明)** | **[English Documentation](#english-documentation)**

---

<a name="中文说明"></a>
# 中文说明

## 📖 目录简介

本目录提供了一套专为 `luci-app-singbox-plus` 开发的轻量级 Python 测试与诊断脚本。涵盖软路由 SSH 连通性、Sing-Box 运行状态、TUN0 虚拟网卡、Clash RESTful API 延迟探测、LuCI Web 控制器响应，以及离线协议解析单元测试。

---

## 🔒 安全规范（严防涉密，最高优先级）

> [!CAUTION]
> **本目录内所有脚本均严禁硬编码任何敏感凭据！**  
> 绝对不要在脚本中写入真实用户名、密码、私有订阅 Token、UUID 或私网/公网 IP 地址。  
> 脚本全面支持通过以下三种安全方式动态注入凭据：
> 1. **交互式无回显安全输入**（`getpass`，推荐）
> 2. **命令行参数**（`--host`, `--user`, `--password` 等，仅在内存中生效）
> 3. **临时环境变量**（`ROUTER_HOST`, `ROUTER_USER`, `ROUTER_PASS` 等）

---

## 📂 脚本清单

| 脚本名称 | 功能说明 | 依赖库 |
| :--- | :--- | :--- |
| **`test_ssh_status.py`** | 测试路由器 SSH 连接、系统负载、Sing-Box 服务状态、TUN0 网卡及境内外出海网络连通性 | `paramiko` |
| **`test_clash_api.py`** | 测试 Sing-Box 内置 Clash RESTful API（默认端口 9090），获取代理节点及历史延迟 | Python 标准库 (`urllib`) |
| **`test_luci_api.py`** | 模拟登录 LuCI 后台并验证控制器端点（`/status`、`/nodes`）返回的 JSON 响应 | Python 标准库 (`urllib`) |
| **`test_subscription_parser.py`** | 本地离线单元测试：验证 Base64 订阅解码与 VLESS/TUIC/Hysteria2 节点 URL 参数解析 | Python 标准库 |

---

## 🚀 使用说明

### 1. 运行 SSH 状态与网络检测 (`test_ssh_status.py`)

可以通过安全交互式输入（推荐）：
```bash
python py/test_ssh_status.py
# 终端会提示输入 IP、用户名及密码（密码输入时不回显）
```

或通过命令行参数临时指定：
```bash
python py/test_ssh_status.py --host 192.168.1.1 --user root
```

或通过环境变量指定：
```bash
# Linux / macOS
export ROUTER_HOST="192.168.1.1"
export ROUTER_USER="root"
python py/test_ssh_status.py

# Windows PowerShell
$env:ROUTER_HOST="192.168.1.1"
$env:ROUTER_USER="root"
python py/test_ssh_status.py
```

---

### 2. 运行 Clash API 延迟与节点测试 (`test_clash_api.py`)

无需 SSH，直接通过 HTTP 请求路由器上的 Clash 端口（默认 9090）：
```bash
python py/test_clash_api.py --host 192.168.1.1 --port 9090
```

---

### 3. 运行 LuCI Web 控制器 API 测试 (`test_luci_api.py`)

模拟登录并测试 LuCI 后台的 JSON 数据响应：
```bash
python py/test_luci_api.py --host 192.168.1.1
```

---

### 4. 运行本地协议解析算法单元测试 (`test_subscription_parser.py`)

纯本地运行，使用 RFC 保留地址，不产生外部网络连接与真实凭据：
```bash
python py/test_subscription_parser.py
```

---

## 💬 问题反馈 (Issues)

如果您在测试过程中发现任何脚本报错或有新的测试需求，欢迎前往提交反馈：  
👉 **[GitHub Issues](https://github.com/3588/luci-app-singbox-plus/issues)**

---

## 💖 致谢 / Acknowledgements

感谢 **Gemini 3.8 Flash** 完成本测试工具套件的设计、免密安全机制实现与双语文档编写。

---

<br />
<hr />
<br />

<a name="english-documentation"></a>
# English Documentation

## 📖 Introduction

This directory contains a suite of lightweight Python diagnostic and testing utilities designed for `luci-app-singbox-plus`. It covers OpenWrt router SSH connectivity, Sing-Box service lifecycle, TUN0 virtual network interface status, Clash RESTful API latency probing, LuCI web controller endpoints, and offline protocol parsing unit tests.

---

## 🔒 Security Policy (Zero Credential Leakage, Highest Priority)

> [!CAUTION]
> **Hardcoding passwords or sensitive secrets in these scripts is strictly forbidden!**  
> Never write real passwords, usernames, private subscription tokens, UUIDs, or actual server IPs into script files.  
> All scripts support dynamic, safe credential ingestion via:
> 1. **Interactive hidden prompt** (`getpass`, recommended)
> 2. **CLI argument flags** (`--host`, `--user`, `--password`, etc.)
> 3. **Temporary environment variables** (`ROUTER_HOST`, `ROUTER_USER`, `ROUTER_PASS`)

---

## 📂 Script Catalog

| Script Name | Description | Dependencies |
| :--- | :--- | :--- |
| **`test_ssh_status.py`** | Tests router SSH connection, load average, Sing-Box daemon status, TUN0 interface, and domestic/overseas connectivity | `paramiko` |
| **`test_clash_api.py`** | Queries built-in Clash RESTful API (default port 9090) to list outbound proxies and benchmark latencies | Standard Library (`urllib`) |
| **`test_luci_api.py`** | Simulates LuCI authentication and validates JSON responses from controller endpoints (`/status`, `/nodes`) | Standard Library (`urllib`) |
| **`test_subscription_parser.py`** | Offline unit tests for Base64 subscription decoding and VLESS/TUIC/Hysteria2 node URL parsing | Standard Library |

---

## 🚀 Usage Guide

### 1. SSH Status & Connectivity Probing (`test_ssh_status.py`)

Interactive prompt mode (Recommended, zero credential exposure):
```bash
python py/test_ssh_status.py
# Follow the prompt to enter IP, username, and hidden password
```

Using command-line flags:
```bash
python py/test_ssh_status.py --host 192.168.1.1 --user root
```

Using temporary environment variables:
```bash
# Linux / macOS
export ROUTER_HOST="192.168.1.1"
export ROUTER_USER="root"
python py/test_ssh_status.py

# Windows PowerShell
$env:ROUTER_HOST="192.168.1.1"
$env:ROUTER_USER="root"
python py/test_ssh_status.py
```

---

### 2. Clash RESTful API Latency Benchmark (`test_clash_api.py`)

Connects directly via HTTP without requiring SSH:
```bash
python py/test_clash_api.py --host 192.168.1.1 --port 9090
```

---

### 3. LuCI Web Controller API Testing (`test_luci_api.py`)

Authenticates session and validates controller JSON responses:
```bash
python py/test_luci_api.py --host 192.168.1.1
```

---

### 4. Local Protocol & Subscription Parsing Unit Tests (`test_subscription_parser.py`)

Runs completely offline using RFC reserved dummy data without network calls:
```bash
python py/test_subscription_parser.py
```

---

## 💬 Issues & Support

If you encounter any issues or have suggestions regarding the test scripts, please submit an issue on GitHub:  
👉 **[GitHub Issues](https://github.com/3588/luci-app-singbox-plus/issues)**

---

## 💖 Acknowledgements

Special thanks to **Gemini 3.8 Flash** for completing the design, credential-free security mechanisms, and bilingual documentation for this test suite.
