#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_luci_api.py
----------------
用于测试 LuCI 网页后台 Sing-Box 控制器 API 响应的测试脚本。

安全提示：
本脚本严禁硬编码用户名和密码！
运行时通过命令行参数、环境变量或交互式安全输入获取凭据。
"""

import os
import sys
import argparse
import getpass
import urllib.request
import urllib.parse
import http.cookiejar
import json


def get_credentials():
    parser = argparse.ArgumentParser(description="LuCI Sing-Box Web API 测试脚本")
    parser.add_argument("--host", default=os.getenv("ROUTER_HOST"), help="路由器 IP 地址 (默认提示输入)")
    parser.add_argument("--user", default=os.getenv("ROUTER_USER", "root"), help="LuCI 用户名 (默认: root)")
    parser.add_argument("--password", default=os.getenv("ROUTER_PASS"), help="LuCI 密码 (建议留空通过交互式输入)")
    args = parser.parse_args()

    host = args.host
    if not host:
        host = input("请输入软路由 IP 地址 (例如 192.168.1.1): ").strip()
    user = args.user
    password = args.password
    if not password:
        password = getpass.getpass(f"请输入 LuCI 用户 {user} 的密码 (输入不显示): ")

    return host, user, password


def main():
    host, user, password = get_credentials()
    base_url = f"http://{host}/cgi-bin/luci"

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    print(f"\n[*] 正在尝试登录 LuCI: {base_url} ...")
    login_data = urllib.parse.urlencode({"luci_username": user, "luci_password": password}).encode("utf-8")
    try:
        resp = opener.open(base_url, data=login_data, timeout=8)
    except Exception as e:
        print(f"[-] 连接或登录请求失败: {e}")
        sys.exit(1)

    # 检查是否成功获取 sysauth Cookie
    cookies = {c.name: c.value for c in cj}
    if "sysauth" not in cookies and "sysauth_http" not in cookies:
        print("[-] 登录失败：未收到系统鉴权 sysauth Cookie，请核对用户名与密码。")
        sys.exit(1)

    print("[+] 登录成功，已获取会话鉴权 Cookie！")

    # 测试 status 接口
    status_url = f"{base_url}/admin/services/singbox/status"
    print(f"[*] 正在请求状态接口: {status_url} ...")
    try:
        resp = opener.open(status_url, timeout=5)
        raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        print("[+] 状态接口响应成功：")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[-] 请求状态接口失败: {e}")

    # 测试 nodes 接口
    nodes_url = f"{base_url}/admin/services/singbox/nodes"
    print(f"\n[*] 正在请求节点列表接口: {nodes_url} ...")
    try:
        resp = opener.open(nodes_url, timeout=5)
        raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        print(f"[+] 节点接口响应成功，共获取到 {len(data.get('nodes', []))} 个配置节点。")
    except Exception as e:
        print(f"[-] 请求节点接口失败: {e}")

    print("\n[*] LuCI Web 控制器接口测试完毕。")


if __name__ == "__main__":
    main()
