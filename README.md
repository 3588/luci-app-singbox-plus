# luci-app-singbox-plus ⚡

[![OpenWrt](https://img.shields.io/badge/OpenWrt-18.06%20~%2023.05+%20|%20Universal-blue.svg)](https://openwrt.org/)
[![Sing-Box](https://img.shields.io/badge/Sing--Box-1.10%20~%201.14+-orange.svg)](https://sing-box.sagernet.org/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-green.svg)](LICENSE)
[![i18n](https://img.shields.io/badge/WebUI-中文%20|%20English-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-x86__64%20|%20aarch64%20|%20arm%20|%20mips-lightgrey.svg)]()
[![Issues](https://img.shields.io/github/issues/3588/luci-app-singbox-plus.svg)](https://github.com/3588/luci-app-singbox-plus/issues)

---

> **[中文文档 (Chinese)](#中文文档)** | **[English Documentation](#english-documentation)**

---

<a name="中文文档"></a>
# 中文文档

## 📖 项目简介

**`luci-app-singbox-plus`** 是一款专为 OpenWrt 路由器打造的现代、轻量、高性能的 Sing-Box 透明代理网关与原生 LuCI 控制面板。

本项目旨在解决传统 OpenWrt 代理插件（如 SSR+、PassWall、OpenClash）在处理新一代协议（Hysteria 2、TUIC v5）、动态临时隧道（如 Cloudflare 临时隧道域名频繁重置）时的痛点，提供**不挑任何 OpenWrt 版本的超强通用性**、**零客户端配置的全屋透明代理**、**毫秒级 GFW 智能分流**、**中英双语原生 WebUI**、**全自动订阅拉取与域名追踪**以及**直观好用的三合一控制台**。

---

## ✨ 核心特性

### 🌟 不挑任何版本的 OpenWrt（全版本、全架构通用）
- 💡 **零内核模块强依赖 (Zero Kernel Module Dependencies)**：
  - 传统代理插件（如旧版 PassWall、SSR+、OpenClash）深度绑定特定版本的 Linux 内核对象（如 `iptables-mod-tproxy`、私有 `kmod` 等）。一旦软路由内核微版本升级，往往直接报错 `cannot satisfy dependencies` 甚至引发内核崩溃（Kernel Panic）。
  - 本项目采用**纯用户态 TUN 驱动结合标准 Linux 基础路由表**，完全解耦底层内核，免编译、无外部 C 动态库绑定！
- 💻 **全 CPU 架构通用 (All-Architecture Support)**：
  - 架构打包为通用 `all` 规范，一套代码通吃：**x86_64 / amd64**（软路由）、**aarch64 / ARM64**（树莓派、斐讯 N1、NanoPi R2S/R4S/R5S、友善 RK3568/RK3588）、**ARMv7** 以及 **MIPS / MIPSEL** 路由器。
- 📦 **全版本、全分支系统兼容**：
  - 无论您运行的是官方版 **OpenWrt 18.06 / 19.07 / 21.02 / 22.03 / 23.05 / Master / SNAPSHOT**，亦或是 **ImmortalWrt**、**LEDE (大雕固件)**、**eSir 高大全固件**，只要安装了标准的 `luci` 和 `curl`，均可**100% 即插即用**。

---

### 🌐 原生中英双语 WebUI (i18n)
- 类似 MetaCubeX 的设计哲学，在控制台右上角常驻 **`🌐 语言 / Language: [中文] [English]`** 切换按钮。
- 点击即时全量切换所有选项卡、状态徽章、表格列名、输入框提示与操作反馈。
- 自动持久化存储至浏览器本地（`localStorage`），下次打开无需重复选择。

---

### 🚀 内核级 TUN 透明网关
- 基于 Sing-Box 原生 TUN 虚拟网络接口（`tun0`），接管路由默认网关。
- 局域网内所有设备（PC、手机、电视盒子、游戏主机）连接 Wi-Fi 或插上网线即可实现无感科学出海，无需在每台终端上安装任何客户端软件。

---

### 🛡️ GFW 模式高性能二进制规则分流
- 内置 MetaCubeX 官方预编译的高性能 `.srs` 二进制规则集（`geosite-gfw`、`geoip-google`、`geoip-telegram`、`geoip-twitter`）。
- 国内所有流量与主流国内应用绝对直连（DNS 毫秒级直接返回，不绕路、不影响国内 CDN 测速），境外受阻网站与服务自动分流至代理出站。

---

### 🔄 动态订阅自动管理与追踪 (`sb-sub`)
- 支持多订阅源管理，原生自动 Base64 解码与节点解析。
- **Cloudflare 临时隧道动态追踪**：针对 TryCloudflare 等动态临时节点，自动拉取最新分配的随机域名，并智能注入 Anycast 优选直连 IP 加速，彻底杜绝 DNS 污染与节点超时。
- **无人值守定时静默同步**：内置系统级 Cron 定时守护（默认每 2 小时自动拉取更新），服务端隧道重启更新后，路由器自动无感热切换，永不失联。
- **备用线路保护**：更新订阅时自动保留手动配置的 Hysteria 2 / TUIC 等兜底备份节点不被覆盖。

---

### ⚡ 新一代抗封锁协议原生全支持
- **Hysteria 2 (hy2)**：基于定制 UDP/QUIC 协议与拥塞控制算法，抗弱网抖动，延迟极低。
- **TUIC v5**：基于 QUIC/BBR，单连接多路复用，零 RTT 握手。
- **VLESS**：支持 WebSocket + TLS + xudp，兼容 Cloudflare CDN / 临时隧道转发。

---

### 🖥️ 原生现代化三合一 LuCI 控制台
- **⚡ 订阅管理 (Subscriptions)**：可视化查看所有订阅链接、节点数量、最后更新时间，支持一键立即同步更新与新增/删除订阅。
- **📋 节点列表与手动导入 (Node Manager)**：支持一键批量粘贴 `vless://`、`tuic://`、`hysteria2://` 等链接一键导入，表格化查看生效节点。
- **📊 仪表盘与测速 (Dashboard & Benchmarks)**：内置 Clash API 与轻量化 Web 仪表盘，支持实时延迟测速、手动选路与网络流量走势图。

---

## 🚀 安装指南

> [!NOTE]
> **关于 Releases 下载说明**：
> 本仓库当前**尚未开启 GitHub Releases 页面**。所有最新的预编译安装包均统一存放于本仓库的 `dist/` 目录中，您可以通过下方的 GitHub Raw 原始直链直接下载或安装，无须等待 Releases 发布。

本项目提供 **纯网页端一键安装（免 SSH，最推荐）**、**终端单行在线安装** 与 **源码编译安装** 三种方式：

### 方式一：通过 LuCI 网页后台一键上传安装（最推荐，免 SSH）

> **适合所有不想接触终端命令或路由器没有安装 Git 的用户，全程在浏览器中点两下即可完成！**

1. **下载安装包**：
   👉 **[点击直接下载最新 IPK 安装包](https://github.com/3588/luci-app-singbox-plus/raw/master/dist/luci-app-singbox-plus_1.0.0-1_all.ipk)**
   *(文件存放于本仓库 `dist/` 目录下，文件名为 `luci-app-singbox-plus_1.0.0-1_all.ipk`)*
2. **打开路由器后台**：进入 **系统 -> 软件包**（直达链接：`http://<路由器IP>/cgi-bin/luci/admin/system/packages`）。
3. 点击页面顶部的 **【上传软件包... (Upload Package...)】** 按钮。
4. 选择刚才下载的 `luci-app-singbox-plus_1.0.0-1_all.ipk` 文件，点击 **【上传并安装】**。
5. 等待约 3 秒提示安装成功，刷新浏览器页面即可在左侧导航看到 **服务 -> Sing-Box** 入口！

---

### 方式二：终端单行在线命令安装（适合习惯用 SSH 的用户）

无需手动克隆代码，直接在路由器的 SSH 终端中粘贴执行以下命令：

```bash
curl -fsSL https://raw.githubusercontent.com/3588/luci-app-singbox-plus/master/dist/luci-app-singbox-plus_1.0.0-1_all.ipk -o /tmp/sb.ipk && opkg install /tmp/sb.ipk && rm -f /tmp/sb.ipk
```

---

### 方式三：从源码克隆安装（开发者模式）

```bash
cd /tmp
git clone https://github.com/3588/luci-app-singbox-plus.git
cd luci-app-singbox-plus
chmod +x install.sh
./install.sh
```

---

## 🖥️ 快速使用

安装完成后，浏览器直接访问：
👉 **`http://<路由器IP>/cgi-bin/luci/admin/services/singbox`**

1. **语言切换**：页面右上角可自由切换 **【中文】** 或 **【English】**。
2. **导入订阅**：在「⚡ 订阅管理」中填入您的订阅链接，点击【立即同步所有订阅 🔄】即可自动拉取节点。
3. **手动添加**：若有单独的节点，可在「📋 节点列表与手动添加」中直接粘贴链接一键导入。
4. **切换节点**：在「📊 仪表盘与测速」中可测速并自由点击切换主节点。

---

## 🛠️ 常用命令行工具

除了在 LuCI 网页后台操作外，也可以在 SSH 终端中直接使用以下管理命令：

- **订阅管理 (`sb-sub`)**：
  ```bash
  sb-sub update                 # 立即同步并更新所有订阅节点
  sb-sub list                   # 查看已保存的订阅列表
  sb-sub add "订阅名" "订阅URL" # 添加新的订阅源
  sb-sub del "订阅名"           # 删除指定的订阅源
  ```
- **节点管理 (`sb-node`)**：
  ```bash
  sb-node list                  # 查看当前所有代理节点的详细参数
  sb-node add "vless://..."     # 手动添加单条节点链接 (支持 vless/tuic/hy2)
  sb-node del "节点Tag名称"     # 删除指定的节点
  ```
- **服务启停**：
  ```bash
  /etc/init.d/sing-box restart  # 重启服务
  /etc/init.d/sing-box status   # 查看运行状态
  ```

---

## 💬 问题反馈 (Issues)

如果您在使用过程中遇到任何问题、发现 Bug 或有新的功能建议，欢迎前往 GitHub 提交反馈：
👉 **[提交 Issue / 反馈问题](https://github.com/3588/luci-app-singbox-plus/issues)**

请在提交时尽量提供：
- 路由器 CPU 架构与 OpenWrt 固件版本
- 相关的错误信息或日志输出（`/var/log/sing-box.log`）

---

## 📄 开源许可证

本项目基于 [GNU General Public License v3.0 (GPL-3.0)](LICENSE) 授权开源。

---

## 💖 致谢 / Acknowledgements

感谢 **Gemini 3.8 Flash** 完成本项目的全套架构设计、核心 Lua 脚本、LuCI 控制台开发与规范文档编写。

---

<br />
<hr />
<br />

<a name="english-documentation"></a>
# English Documentation

## 📖 Introduction

**`luci-app-singbox-plus`** is a modern, lightweight, and high-performance Sing-Box transparent proxy gateway and native LuCI web dashboard tailored for OpenWrt router systems.

It is designed to overcome the limitations of traditional OpenWrt proxy packages (such as SSR+, PassWall, or OpenClash) when dealing with next-gen protocols (Hysteria 2, TUIC v5) and ephemeral tunnels (e.g. TryCloudflare dynamic tunnel renewals). It provides **universal compatibility across all OpenWrt versions and CPU architectures**, **zero-client transparent proxying for the entire household**, **millisecond-level GFW rule splitting**, **native bilingual WebUI (Chinese & English)**, **automated subscription synchronization**, and an **intuitive 3-in-1 LuCI dashboard**.

---

## ✨ Key Features

### 🌟 Universal Compatibility (Runs on Any OpenWrt Version & Architecture)
- 💡 **Zero Kernel Module Dependencies**:
  - Traditional proxy packages depend heavily on specific kernel object modules (`iptables-mod-tproxy`, custom `kmod-tun` versions). Kernel upgrades frequently cause `cannot satisfy dependencies` errors or kernel panics.
  - This project leverages **pure user-space TUN interfaces and standard Linux routing tables**, completely decoupling itself from kernel versions. No recompilation or C dynamic library linking required!
- 💻 **All CPU Architectures Supported**:
  - Packaged under the universal `all` architecture standard: runs seamlessly on **x86_64 / amd64**, **aarch64 / ARM64** (Raspberry Pi, Phicomm N1, NanoPi R2S/R4S/R5S, FriendlyElec RK3568/RK3588), **ARMv7**, and **MIPS / MIPSEL**.
- 📦 **Compatible Across All OpenWrt Branches & Releases**:
  - Works out-of-the-box on **OpenWrt 18.06, 19.07, 21.02, 22.03, 23.05, SNAPSHOT, and Master**, as well as forks like **ImmortalWrt**, **LEDE**, and **eSir** firmware distributions.

---

### 🌐 Native Bilingual WebUI (Chinese & English i18n)
- Built with a design philosophy similar to MetaCubeX: features a persistent **`🌐 语言 / Language: [中文] [English]`** switch at the top right of the dashboard.
- Seamlessly switches all tabs, badges, table columns, placeholder guides, and notifications with a single click.
- Preferences are automatically saved in the browser's `localStorage`.

---

### 🚀 Kernel-Level TUN Transparent Gateway
- Leverages Sing-Box native TUN interface (`tun0`) to route default gateway traffic.
- All devices in the LAN (PCs, smartphones, smart TVs, game consoles) gain immediate circumvention upon connecting to Wi-Fi or Ethernet—zero client app required.

---

### 🛡️ GFW High-Performance Binary Rule Routing
- Preloaded with MetaCubeX official `.srs` binary rule sets (`geosite-gfw`, `geoip-google`, `geoip-telegram`, `geoip-twitter`).
- Direct routing for domestic traffic and domestic CDNs with zero latency; automatic proxying exclusively for restricted overseas destinations.

---

### 🔄 Dynamic Subscription Manager (`sb-sub`)
- Multi-subscription management with automatic Base64 decoding and node parsing.
- **Dynamic Cloudflare Tunnel Tracking**: Automatically detects randomized hostnames generated by TryCloudflare tunnels, maps them to optimized Anycast IPs, and injects proper SNI/Host camouflage.
- **Unattended Scheduled Sync**: Configured with a system Cron job (every 2 hours by default) for silent synchronization and seamless hot-reloading.
- **Backup Route Protection**: Automatically preserves custom fallback nodes (e.g., Hysteria 2 & TUIC) during subscription updates.

---

### ⚡ Full Support for Next-Gen Protocols
- **Hysteria 2 (hy2)**: Custom UDP/QUIC protocol with advanced congestion control, ultra-low latency, and excellent resistance against packet loss.
- **TUIC v5**: QUIC/BBR architecture with 0-RTT handshakes and connection multiplexing.
- **VLESS**: WebSocket + TLS + xudp, fully compatible with Cloudflare CDN and ingress tunnels.

---

### 🖥️ 3-in-1 Native LuCI Web Console
- **⚡ Subscriptions**: Real-time status, one-click manual update, and subscription CRUD operations.
- **📋 Node Manager**: Direct clipboard batch import (`vless://`, `tuic://`, `hysteria2://`) and structured tabular overview.
- **📊 Dashboard & Benchmarks**: Built-in Clash API integration and Web UI for real-time latency tests, manual node switching, and traffic statistics.

---

## 🚀 Installation Guide

> [!NOTE]
> **Notice Regarding GitHub Releases**:
> **GitHub Releases are currently disabled for this repository**. All up-to-date installation packages are directly maintained under the `dist/` directory. You can download or install the IPK directly via the GitHub Raw link below without waiting for releases.

We provide **Web UI One-Click Upload (No SSH Required, Recommended)**, **One-Line CLI Command**, and **Source Code Installation**:

### Method 1: Web UI Upload via LuCI Packages (Recommended, No SSH)

> **Ideal for users who prefer not to use terminal commands or whose routers lack git.**

1. **Download the Package**:
   👉 **[Click to download the latest IPK package directly](https://github.com/3588/luci-app-singbox-plus/raw/master/dist/luci-app-singbox-plus_1.0.0-1_all.ipk)**
   *(Located in the `dist/` directory as `luci-app-singbox-plus_1.0.0-1_all.ipk`)*
2. Open your router web interface: Navigate to **System -> Software / Packages** (Direct URL: `http://<Router-IP>/cgi-bin/luci/admin/system/packages`).
3. Click the **【Upload Package...】** button at the top of the page.
4. Choose the downloaded `luci-app-singbox-plus_1.0.0-1_all.ipk` file and click **【Upload & Install】**.
5. Wait ~3 seconds for completion, refresh the web interface, and you will see **Services -> Sing-Box** in the menu!

---

### Method 2: Single-Line Online Command (For SSH Users)

No need to `git clone`. Run this single command in your router terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/3588/luci-app-singbox-plus/master/dist/luci-app-singbox-plus_1.0.0-1_all.ipk -o /tmp/sb.ipk && opkg install /tmp/sb.ipk && rm -f /tmp/sb.ipk
```

---

### Method 3: Clone from Source

```bash
cd /tmp
git clone https://github.com/3588/luci-app-singbox-plus.git
cd luci-app-singbox-plus
chmod +x install.sh
./install.sh
```

---

## 🖥️ Quick Start

Once installed, access your router control panel:
👉 **`http://<Router-IP>/cgi-bin/luci/admin/services/singbox`**

1. **Language Switching**: Toggle between **【中文】** and **【English】** anytime at the top-right corner.
2. **Import Subscriptions**: In "⚡ Subscriptions", enter your subscription link and click 【Sync All Subscriptions 🔄】.
3. **Manual Node Import**: Paste node URLs in "📋 Node Manager" for instant loading.
4. **Switch Nodes**: Check latencies and switch active outbound routes in "📊 Dashboard & Benchmarks".

---

## 🛠️ Command-Line Interface (CLI)

- **Subscription Management (`sb-sub`)**:
  ```bash
  sb-sub update                 # Update all subscriptions immediately
  sb-sub list                   # Show configured subscriptions
  sb-sub add "Name" "Sub-URL"   # Add a new subscription
  sb-sub del "Name"             # Delete a subscription
  ```
- **Node Management (`sb-node`)**:
  ```bash
  sb-node list                  # List all active outbound nodes
  sb-node add "vless://..."     # Add node manually (vless / tuic / hysteria2)
  sb-node del "Node-Tag"        # Delete node by tag
  ```
- **Service Control**:
  ```bash
  /etc/init.d/sing-box restart  # Restart proxy service
  /etc/init.d/sing-box status   # Check status
  ```

---

## 💬 Issues & Support

If you encounter any issues, bugs, or feature requests, feel free to open an issue on GitHub:
👉 **[Open an Issue](https://github.com/3588/luci-app-singbox-plus/issues)**

Please provide:
- Your router CPU architecture & OpenWrt version
- Error logs or output if applicable (`/var/log/sing-box.log`)

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0 (GPL-3.0)](LICENSE).

---

## 💖 Acknowledgements

Special thanks to **Gemini 3.8 Flash** for completing the system architecture, core Lua scripting, LuCI console development, and documentation for this project.
