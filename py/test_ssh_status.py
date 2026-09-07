#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_ssh_status.py
------------------
用于测试 OpenWrt 软路由 SSH 连接及 Sing-Box 核心运行状态的测试脚本。

安全提示：
本脚本严禁硬编码密码或敏感凭证！
支持通过交互式输入、命令行参数或环境变量读取凭据。
"""

import os
import sys
import argparse
import getpass

try:
    import paramiko
except ImportError:
    print("错误: 未安装 paramiko 库。请先执行: pip install paramiko")
    sys.exit(1)


def get_credentials():
    parser = argparse.ArgumentParser(description="OpenWrt Sing-Box 路由器 SSH 状态测试脚本")
    parser.add_argument("--host", default=os.getenv("ROUTER_HOST"), help="路由器 IP 地址 (或设置环境变量 ROUTER_HOST)")
    parser.add_argument("--port", type=int, default=int(os.getenv("ROUTER_PORT", "22")), help="SSH 端口 (默认: 22)")
    parser.add_argument("--user", default=os.getenv("ROUTER_USER", "root"), help="SSH 用户名 (默认: root)")
    parser.add_argument("--password", default=os.getenv("ROUTER_PASS"), help="SSH 密码 (建议留空通过交互式输入)")
    args = parser.parse_args()

    host = args.host
    if not host:
        host = input("请输入软路由 IP 地址 (例如 192.168.1.1): ").strip()

    user = args.user
    if not user:
        user = input("请输入 SSH 用户名 [默认 root]: ").strip() or "root"

    password = args.password
    if not password:
        password = getpass.getpass(f"请输入 {user}@{host} 的 SSH 密码 (输入不显示): ")

    return host, args.port, user, password


def run_ssh_test():
    host, port, user, password = get_credentials()

    print(f"\n[*] 正在连接软路由: {user}@{host}:{port} ...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, port=port, username=user, password=password, timeout=8)
        print("[+] SSH 连接成功！\n")
    except Exception as e:
        print(f"[-] SSH 连接失败: {e}")
        sys.exit(1)

    commands = [
        ("系统负载与开机时间", "uptime"),
        ("Sing-Box 服务状态", "/etc/init.d/sing-box status"),
        ("TUN0 虚拟网卡检测", "ip addr show tun0 2>/dev/null | grep -E 'inet|UP' || echo '未检测到 tun0 网卡'"),
        ("境外出海连通性探测", "curl -I -m 4 -s https://www.google.com | head -n 1 || echo '海外连接超时或未通'"),
        ("国内直连分流探测", "curl -I -m 4 -s https://www.baidu.com | head -n 1 || echo '国内连接超时或未通'"),
    ]

    for title, cmd in commands:
        print(f"================== [ {title} ] ==================")
        print(f"$ {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode("utf-8", errors="ignore").strip()
        err = stderr.read().decode("utf-8", errors="ignore").strip()
        if out:
            print(out)
        if err:
            print(f"[提示/警告]: {err}")
        print()

    client.close()
    print("[*] 所有检测完成，SSH 会话已安全关闭。")


if __name__ == "__main__":
    run_ssh_test()
