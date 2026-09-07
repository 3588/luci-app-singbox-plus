# 测试与诊断工具集 (Python Test Suite)

本目录提供用于验证 OpenWrt 软路由、Sing-Box 运行状态、LuCI API 及订阅解析算法的 Python 测试脚本。

---

## 🔒 安全规范（严禁涉密）

> [!CAUTION]
> **本目录内所有脚本均严禁硬编码用户名、密码、私有 Token、UUID 或服务器 IP！**  
> 脚本支持通过**交互式无回显安全输入**（`getpass`）、**命令行参数**或**临时环境变量**提供凭证，严禁将个人凭证写入脚本文件中提交至 Git。

---

## 📂 脚本清单

| 脚本名称 | 用途说明 | 依赖库 |
| :--- | :--- | :--- |
| **`test_ssh_status.py`** | 测试路由器 SSH 连通性、系统负载、Sing-Box 运行状态、TUN0 网卡及境内外出海网络连通性 | `paramiko` |
| **`test_clash_api.py`** | 测试 Sing-Box 内置 Clash RESTful API（默认端口 9090），获取代理节点及历史延迟 | 标准库 (`urllib`) |
| **`test_luci_api.py`** | 模拟登录 LuCI 后台并测试控制器端点（`/status`、`/nodes`）返回的 JSON 响应 | 标准库 (`urllib`) |
| **`test_subscription_parser.py`** | 订阅 Base64 解码与 VLESS/TUIC/Hysteria2 节点 URL 参数解析的本地单元测试（RFC 虚拟数据） | 标准库 |

---

## 🚀 使用说明

### 1. 运行 SSH 状态检测 (`test_ssh_status.py`)

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

### 3. 运行本地解析算法单元测试 (`test_subscription_parser.py`)

纯本地运行，不依赖路由器网络与真实凭据：
```bash
python py/test_subscription_parser.py
```
