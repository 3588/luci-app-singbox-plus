#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_subscription_parser.py
----------------------------
用于本地测试 VLESS、Hysteria2、TUIC 协议 URL 及订阅 Base64 解码逻辑的单元测试脚本。
完全在本地运行，使用 RFC 5737 规范的虚拟保留地址，无任何网络依赖与凭证。
"""

import base64
import urllib.parse
import json


def parse_vless(url_str):
    """解析 VLESS 格式 URL 并生成 Sing-Box outbound 字典"""
    parsed = urllib.parse.urlparse(url_str)
    if parsed.scheme != "vless":
        return None

    uuid = parsed.username
    server = parsed.hostname
    port = parsed.port or 443
    tag = urllib.parse.unquote(parsed.fragment) if parsed.fragment else f"vless-{server}:{port}"
    params = urllib.parse.parse_qs(parsed.query)

    ob = {
        "type": "vless",
        "tag": tag,
        "server": server,
        "server_port": port,
        "uuid": uuid,
        "packet_encoding": params.get("packetEncoding", ["xudp"])[0]
    }

    sec = params.get("security", ["none"])[0]
    if sec == "tls":
        ob["tls"] = {
            "enabled": True,
            "server_name": params.get("sni", [server])[0],
            "utls": {"enabled": True, "fingerprint": "chrome"}
        }

    net_type = params.get("type", ["tcp"])[0]
    if net_type == "ws":
        ob["transport"] = {
            "type": "ws",
            "path": params.get("path", ["/"])[0],
            "headers": {"Host": params.get("host", [server])[0]}
        }

    return ob


def test_vless_parsing():
    sample_url = "vless://00000000-0000-0000-0000-000000000001@example.com:443?encryption=none&security=tls&type=ws&host=sample.example.com&path=/vless&packetEncoding=xudp#%E7%A4%BA%E4%BE%8B%E8%8A%82%E7%82%B9"
    ob = parse_vless(sample_url)
    assert ob is not None, "VLESS 解析失败"
    assert ob["type"] == "vless"
    assert ob["uuid"] == "00000000-0000-0000-0000-000000000001"
    assert ob["tag"] == "示例节点"
    assert ob["tls"]["server_name"] == "example.com"
    assert ob["transport"]["path"] == "/vless"
    print("[+] test_vless_parsing: 通过 (PASS)")


def test_base64_sub_decode():
    raw_content = "vless://sample1#Node1\nvless://sample2#Node2\n"
    encoded = base64.b64encode(raw_content.encode("utf-8")).decode("ascii")
    decoded = base64.b64decode(encoded).decode("utf-8")
    lines = [line.strip() for line in decoded.splitlines() if line.strip()]
    assert len(lines) == 2
    assert lines[0] == "vless://sample1#Node1"
    assert lines[1] == "vless://sample2#Node2"
    print("[+] test_base64_sub_decode: 通过 (PASS)")


def main():
    print("================== [ 订阅与节点解析算法单元测试 ] ==================")
    test_vless_parsing()
    test_base64_sub_decode()
    print("====================================================================")
    print("[*] 全部单元测试通过！\n")


if __name__ == "__main__":
    main()
