# luci-app-singbox-plus 交接文档 (ai.md)

> 本文件是严格遵循 [aimd 标准规范 (https://ai.drx.ac.cn/aimd)](https://ai.drx.ac.cn/aimd) 编写的 AI 工作交接文档。请任何新接手的 AI 助手（或开发者）先通读本文件，再继续对本仓库及软路由进行操作。
>
> 目录 / Navigation:
> - [中文交接文档 (Chinese Version)](#中文交接文档)
> - [English Handover Documentation](#english-handover-documentation)

---

<a name="中文交接文档"></a>
# 中文交接文档

## 一、还没做完的事 & 动手前注意

### 尚未完成 / 待办 (TODO)
- [x] **OpenWrt IPK 自动化打包支持**：已编写 `build_ipk.py`，支持直接生成标准 `luci-app-singbox-plus_1.0.0-1_all.ipk` 包，存放于 `dist/` 目录，支持在 LuCI 网页后台（`admin/system/packages`）直接上传安装。
- [x] **WebUI 中英双语国际化 (i18n)**：已全面实现类似 MetaCubeX 的中文与 English 无缝即时切换，状态由 `localStorage` 自动持久化保存。
- [x] **全版本通用架构论证与规范整理**：已在文档中明确本插件“不挑任何 OpenWrt 版本与 CPU 架构”的底层解耦原理。
- [x] **敏感信息防范与纯净化构建**：仓库内所有示例配置均采用 RFC 保留域名和占位符，严禁泄露任何私有凭证。
- [ ] **节点健康检查与被动自动倒换 (Watchdog)**：实现一个微型守护进程，当主节点连续探测失败时，无需人工干预自动切换至备用节点；当主节点恢复时自动切回。
- [ ] **订阅链接加密存储 (可选)**：在 `/etc/sing-box/subscriptions.json` 中提供可选的 token 混淆或仅 root 读写权限加固。
- [ ] **LuCI 界面主题自适应样式增强**：针对不同 OpenWrt 第三方主题（如 Argon、Rosy、Edge 等）优化深色/浅色配色细节。

### 动手前注意事项（极其重要）
1. **绝对保密与脱敏原则（最高优先级）**：
   - 严禁将包含真实私有订阅 Token、真实服务器 UUID、私密隧道域名以及包含上述信息的运行截图提交至公开 Git 仓库或公开文档中。
   - 所有公开示例配置文件统一使用 `.example` 后缀，且内容必须是纯虚构占位符（如 `example.com`, `00000000-0000-0000-0000-000000000000`）。
2. **不挑任何版本的 OpenWrt（架构核心原则）**：
   - 插件设计严格秉承**内核解耦**与**全架构通用**理念。切勿在 `luasrc`、`root` 或打包配置中引入特定内核版本的 `kmod-*` 或私有 C 动态链接依赖。所有控制逻辑通过标准 LuCI Lua API、用户态 TUN 网络接口和通用的 sing-box 二进制完成，以维持其 100% 跨版本兼容性。
3. **GitHub Releases 状态说明**：
   - 当前仓库暂未开启 GitHub Releases 功能。因此文档与安装说明中**统一指引用户直接使用仓库内的 `dist/luci-app-singbox-plus_1.0.0-1_all.ipk` 原始下载直链**（`raw.githubusercontent.com`），切勿在文档中引用未开启的 `releases` 链接。
4. **网络路由死循环防护（极其重要）**：
   - 在透明代理模式（TUN `tun0` 接管默认路由）下，所有 `outbounds` 中 `direct` 出站**必须显式指定物理 WAN 接口绑定（如 `"bind_interface": "eth3"`）**！
   - 若移除此项，DNS 本地回环或直连流量会被再次截获送回 TUN，导致整个软路由彻底断网崩溃并报错 `detour to an empty direct outbound makes no sense`。
5. **动态隧道优选 IP 映射机制**：
   - 节点的动态临时隧道域名（如 `*.trycloudflare.com`）在国内直连解析易被阻断。系统在解析订阅时已自动将其连接 IP 重定向到 Anycast 优选 IP，同时在 TLS/SNI 及 HTTP Host 头中注入原临时域名。
   - 修改 `/usr/bin/sb-sub` 或 `/usr/bin/sb-node` 时严禁破坏此映射逻辑。
6. **备用节点保护约定**：
   - 系统支持用户配置抗封锁备用节点。`sb-sub update` 执行订阅同步时，只拉取并更新动态订阅节点，**绝对不能覆盖或删除用户手动配置的兜底备用节点**。
7. **问题反馈与支持渠道**：
   - 统一引导用户通过 [GitHub Issues (https://github.com/3588/luci-app-singbox-plus/issues)](https://github.com/3588/luci-app-singbox-plus/issues) 提交 Bug 和需求建议。

---

## 二、历史记录（我们做了什么、怎么做的）

### 时间线过程还原

- **2026-09-06**：
  - **清理冗余组件**：彻底卸载清理了路由器上冲突且占用磁盘的冗余插件，通过 OverlayFS Whiteout 屏蔽清理了只读 ROM 残留。
  - **卸载无用守护进程**：排查并停止了单宽带环境下无用的 `mwan3dns` 守护进程，从 LuCI 侧边栏完全移除了残存菜单项。
  - **部署 GFW 模式分流**：拉取并编译了高性能二进制规则集（`geosite-gfw.srs`, `geoip-google.srs`, `geoip-telegram.srs`, `geoip-twitter.srs`），配置并验证了毫秒级国内直连/被墙走代理策略。
  - **解决应用连接问题**：定位并排查了本地旧代理客户端回环拦截导致的问题，指引关闭本地代理，完全由软路由全屋透明接管。
  - **构建 LuCI 初始管理模块**：开发并部署了控制器与前端模板，实现 LuCI 原生控制后台（直达：`http://59.0.0.1/cgi-bin/luci/admin/services/singbox`）。

- **2026-09-07**：
  - **节点管理系统开发 (`sb-node`)**：编写了 `/usr/bin/sb-node`，在 LuCI 网页端增加了「节点管理与手动导入」标签，支持直接粘贴链接批量导入。
  - **多协议原生支持**：配置并实测了新一代协议 `Hysteria 2` 与 `TUIC v5`，在保证高性能的同时实现了主备高可用容灾。
  - **订阅管理系统开发 (`sb-sub`)**：针对临时隧道易重置域名的特性，编写了 `/usr/bin/sb-sub` 核心同步程序，并在 LuCI 前端开发了「⚡ 订阅管理」控制板，支持一键拉取最新隧道域名。
  - **无人值守自动化**：配置系统级 Crontab 计划任务（`0 */2 * * * /usr/bin/sb-sub update`），每 2 小时静默自动同步最新隧道域名，彻底实现全自动零维护。
  - **实现 Web 免 SSH 安装支持 (`build_ipk.py`)**：实现了标准的 OpenWrt IPK 打包脚本 `build_ipk.py`，生成了可在 `http://59.0.0.1/cgi-bin/luci/admin/system/packages` 页面直接点击「上传软件包」一键安装的 `.ipk` 包。
  - **WebUI 中英双语国际化重构**：参照 MetaCubeX 设计，在 `singbox.htm` 中引入前端国际化字典与右上角中英切换开关，实现界面元素一键切换并自动记忆。
  - **强化全版本通用特性**：在核心文档中正式阐明“不挑任何版本 OpenWrt”的架构原理解耦，完善 Issue 反馈引导，文末致谢 Gemini 3.8 Flash。
  - **安全审查与敏感数据彻底清理**：对示例配置文件进行全面脱敏处理（统一替换为 RFC 规范占位符），删除所有涉及敏感配置的截图，完全重置 Git 提交历史，确保开源发布 100% 安全合规。

### 当前仓库文件结构树

```text
E:\code\luci-app-singbox-plus/
├── LICENSE                                     # GPL-3.0 开源许可证
├── README.md                                   # 先中文后英文的双语项目完整文档 (含全版本说明/致谢)
├── ai.md                                       # 本工作交接规范文档 (aimd 标准，先中文后英文)
├── build_ipk.py                                # 标准 OpenWrt .ipk 自动化打包程序
├── dist/
│   └── luci-app-singbox-plus_1.0.0-1_all.ipk  # 网页端可直接上传的安装包 (约 51 KB)
├── py/                                         # 诊断与测试脚本工具集 (免密/安全设计)
│   ├── README.md                               # 测试工具使用说明与安全规范
│   ├── test_ssh_status.py                      # 路由器 SSH 状态与出海连通性测试
│   ├── test_clash_api.py                       # Sing-Box Clash API 延迟与节点测试
│   ├── test_luci_api.py                        # LuCI Web 控制器接口测试
│   └── test_subscription_parser.py            # 节点解析与 Base64 解码单元测试
├── install.sh                                  # 路由器端一键安装脚本
├── uninstall.sh                                # 一键卸载与清理脚本
├── .gitignore                                  # Git 忽略配置
├── luasrc/
│   ├── controller/
│   │   └── singbox.lua                         # LuCI 控制器与 REST API (状态/服务/节点/订阅/语言)
│   └── view/
│       └── singbox/
│           └── singbox.htm                     # LuCI 双语控制台模板 (i18n / 订阅 / 节点 / 仪表盘)
├── root/
│   ├── etc/
│   │   ├── init.d/
│   │   │   └── sing-box                        # OpenWrt procd 系统服务脚本
│   │   └── sing-box/
│   │       ├── config.json.example             # 预优化 sing-box 配置文件模板 (脱敏)
│   │       └── subscriptions.json.example      # 订阅配置文件示例 (脱敏)
│   └── usr/
│       └── bin/
│           ├── sb-sub                          # 订阅管理与自动更新工具 (Lua)
│           └── sb-node                         # 节点增删查命令行工具 (Lua)
└── rulesets/                                   # GFW 二进制规则集 (.srs)
    ├── geosite-gfw.srs
    ├── geoip-google.srs
    ├── geoip-telegram.srs
    └── geoip-twitter.srs
```

---

## 三、项目核心技术架构与原理

### 1. 为什么“不挑任何版本的 OpenWrt”？
传统 OpenWrt 代理插件的普遍通病在于**对固件编译环境和内核版本的极高敏感度**：
- **旧模式的致命短板**：
  - PassWall / SSR+ 等依赖 `iptables-mod-tproxy`、私有 kmod 模块，往往要求固件在出厂编译时就将对应的 Linux 内核头文件打包进去。一旦用户刷入不同编译作者的固件或升级了小版本内核，内核对象符号错位，直接导致插件无法安装或启动时崩溃。
  - OpenClash 架构庞大，对内存和存储要求较高，且控制层和核心联动复杂，低配置或特定旧版本系统容易 OOM（内存溢出）。
- **本项目的不挑版本解耦方案**：
  - **纯用户态 TUN 驱动**：Sing-Box 原生支持纯用户态网络堆栈（gVisor / System TUN），只需内核开启基础的通用虚拟网卡支持，无需任何定制内核模块。
  - **纯 Lua 脚本与原生 LuCI 架构**：控制台采用标准 Lua 5.1 语法开发，仅依赖 OpenWrt 自带的 `luci-base` 和基础 `curl` 工具，跨越 OpenWrt 18.06 至 23.05+ 无任何 API 废弃冲突。
  - **架构通用包 (`_all.ipk`)**：IPK 控制信息中声明 `Architecture: all`，无论是 64 位 x86 软路由、ARM 嵌入式设备，还是 MIPS 老旧路由，均可直接识别并安装。

### 2. 双语国际化 (i18n) 设计
- 借鉴 MetaCubeX 的设计，前端在 `<script>` 顶层声明 `i18nData` 字典对象，覆盖页面所有 UI 字符串。
- 用户点击右上角 `[中文]` / `[English]` 时，执行 `setLang(lang)`，动态遍历所有带有 `data-i18n` 属性的 DOM 节点并更新其显示文本。
- 当前语言偏好即时保存在 `localStorage.getItem('sb_lang')` 中，刷新或重新打开自动恢复。

---

## 💖 致谢 / Acknowledgements

本项目由 **Gemini 3.8 Flash** 完成全套技术架构设计、核心逻辑编写、LuCI 原生控制面板开发、多语言支持与文档编撰。

---

<br />
<hr />
<br />

<a name="english-handover-documentation"></a>
# English Handover Documentation

## 1. Pending Tasks & Operational Notices

### Pending Tasks (TODO)
- [x] **Automated OpenWrt IPK Packaging**: Scripted `build_ipk.py` to create the standard `luci-app-singbox-plus_1.0.0-1_all.ipk` bundle in the `dist/` directory for direct upload in LuCI web backend (`admin/system/packages`).
- [x] **Bilingual WebUI (i18n)**: Implemented seamless Chinese & English dynamic UI toggling with persistent state preserved in `localStorage`.
- [x] **Universal Compatibility Specification**: Fully articulated the underlying decoupling architecture that enables compatibility across any OpenWrt release and CPU platform.
- [x] **Security Hardening & Complete Sanitization**: All example configurations desensitized using RFC placeholders; Git history fully purged.
- [ ] **Node Health Watchdog & Passive Failover**: A background micro-daemon to automatically switch to backup routes when primary tunnels fail, restoring when recovered.
- [ ] **Subscription Link Encryption (Optional)**: Optional token obfuscation or permission hardening in `/etc/sing-box/subscriptions.json`.
- [ ] **LuCI Adaptive Styling**: Enhanced dark/light theme polish for various third-party LuCI themes (Argon, Rosy, Edge).

### Operational Notices (Critical)
1. **Strict Privacy & Sanitization (Highest Priority)**:
   - Never commit private subscription tokens, real server UUIDs, or actual dynamic tunnel hostnames to public branches or public documents.
2. **Universal OpenWrt Compatibility Principle**:
   - The plugin strictly adheres to kernel decoupling and universal CPU architecture standards. Never introduce specific `kmod-*` kernel object dependencies or custom C shared libraries into `luasrc` or `root`.
3. **GitHub Releases Status**:
   - Releases are currently disabled on GitHub. Documentation must direct users to download directly via GitHub Raw links pointing to `dist/luci-app-singbox-plus_1.0.0-1_all.ipk`.
4. **Routing Loop Protection (Crucial)**:
   - In transparent proxy mode (TUN `tun0`), the `direct` outbound **must explicitly set the physical WAN interface binding (e.g. `"bind_interface": "eth3"`)** to avoid infinite loops and network crashes.
5. **Fallback Route Protection**:
   - Never overwrite or prune user-configured fallback nodes during subscription updates (`sb-sub update`).

---

## 2. Technical Architecture & Principles

### 1. Why is it universally compatible across all OpenWrt releases?
- **Zero Kernel Module Bindings**: Unlike PassWall or SSR+ that bind to specific compiled `iptables-mod-tproxy` and `kmod` symbols, this project uses Sing-Box's native user-space TUN engine and standard Linux routing tables.
- **Pure Standard Lua**: Implemented using standard Lua 5.1 compatible with `luci-base` across OpenWrt 18.06, 19.07, 21.02, 22.03, and 23.05+.
- **All-Architecture Packaging (`_all.ipk`)**: Fully decoupled from CPU binaries, ready to install on x86_64, aarch64, armv7, and mips platforms out-of-the-box.

### 2. Bilingual Internationalization (i18n)
- Similar to MetaCubeX, dynamic frontend translation handles UI elements instantly without reloading or altering LuCI backend translation catalogs.
- State is preserved seamlessly in the browser's `localStorage`.

---

## 💬 Issue Feedback & Support

Please submit any bugs, issues, or suggestions to:
👉 **[GitHub Issues](https://github.com/3588/luci-app-singbox-plus/issues)**

---

## 💖 Acknowledgements

Special thanks to **Gemini 3.8 Flash** for completing the system architecture, core Lua scripting, LuCI console development, internationalization, and documentation for this project.
