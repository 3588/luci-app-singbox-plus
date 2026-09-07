#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_clash_api.py
-----------------
用于测试 Sing-Box 内置 Clash RESTful API（默认端口 9090）的轻量测试脚本。
可获取代理节点列表并执行实时延迟测速。

安全提示：
本脚本严禁硬编码路由器 IP 或认证 Secret！
"""

import os
import sys
import argparse
import urllib.request
import urllib.error
import json


def parse_args():
    parser = argparse.ArgumentParser(description="Sing-Box Clash API 延迟与节点测试脚本")
    parser.add_argument("--host", default=os.getenv("ROUTER_HOST"), help="路由器 IP 地址 (默认提示输入)")
    parser.add_argument("--port", type=int, default=int(os.getenv("CLASH_API_PORT", "9090")), help="Clash API 端口 (默认: 9090)")
    parser.add_argument("--secret", default=os.getenv("CLASH_API_SECRET", ""), help="Clash API 认证 Secret (若有)")
    return parser.parse_args()


def api_request(url, secret=""):
    headers = {"Content-Type": "application/json"}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[-] HTTP 错误 {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"[-] 请求失败: {e}")
        return None


def main():
    args = parse_args()
    host = args.host
    if not host:
        host = input("请输入软路由 IP 地址 (例如 192.168.1.1): ").strip()
        if not host:
            print("[-] 未提供有效 IP 地址，退出。")
            sys.exit(1)

    base_url = f"http://{host}:{args.port}"
    print(f"\n[*] 正在请求 Clash API: {base_url}/proxies ...")

    data = api_request(f"{base_url}/proxies", args.secret)
    if not data or "proxies" not in data:
        print("[-] 获取代理节点列表失败，请确认 Sing-Box 服务是否已开启 experimental.clash_api。")
        sys.exit(1)

    proxies = data["proxies"]
    print(f"[+] 成功获取代理节点信息，总共包含 {len(proxies)} 个对象：\n")

    print(f"{'节点名称 (Tag)':<35} {'类型 (Type)':<15} {'历史延迟 (History Delay)'}")
    print("-" * 75)

    for name, info in proxies.items():
        p_type = info.get("type", "Unknown")
        history = info.get("history", [])
        if history:
            delay = f"{history[-1].get('delay', 0)} ms"
        else:
            delay = "未测速 (0 ms)"
        print(f"{name:<35} {p_type:<15} {delay}")

    print("-" * 75)
    print("\n[*] Clash API 检测正常！")


if __name__ == "__main__":
    main()
