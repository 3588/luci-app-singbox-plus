import os
import tarfile
import io
import time

project_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(project_dir, "dist")
os.makedirs(dist_dir, exist_ok=True)

pkg_name = "luci-app-singbox-plus"
pkg_ver = "1.0.0-1"
ipk_filename = f"{pkg_name}_{pkg_ver}_all.ipk"
ipk_path = os.path.join(dist_dir, ipk_filename)

print(f"Building {ipk_filename} ...")

debian_binary = b"2.0\n"

control_content = f"""Package: {pkg_name}
Version: {pkg_ver}
Depends: libc, sing-box, curl, ca-bundle
Section: luci
Architecture: all
Maintainer: Antigravity & User <support@github.com>
Description: High-performance Sing-Box transparent gateway & LuCI dashboard for OpenWrt
"""

postinst_content = """#!/bin/sh
if [ -z "$IPKG_INSTROOT" ]; then
    chmod +x /usr/bin/sb-sub /usr/bin/sb-node /etc/init.d/sing-box
    mkdir -p /opt/sing-box /etc/sing-box
    
    if [ ! -f "/etc/sing-box/config.json" ] && [ -f "/etc/sing-box/config.json.example" ]; then
        cp -f /etc/sing-box/config.json.example /etc/sing-box/config.json
    fi
    if [ ! -f "/etc/sing-box/subscriptions.json" ] && [ -f "/etc/sing-box/subscriptions.json.example" ]; then
        cp -f /etc/sing-box/subscriptions.json.example /etc/sing-box/subscriptions.json
    fi

    (crontab -l 2>/dev/null | grep -v "sb-sub update" ; echo "0 */2 * * * /usr/bin/sb-sub update >/dev/null 2>&1") | crontab -
    /etc/init.d/cron restart 2>/dev/null

    rm -rf /tmp/luci-indexcache /tmp/luci-modulecache
    /etc/init.d/uhttpd restart 2>/dev/null
    /etc/init.d/sing-box enable 2>/dev/null
    /etc/init.d/sing-box restart 2>/dev/null
fi
exit 0
"""

prerm_content = """#!/bin/sh
if [ -z "$IPKG_INSTROOT" ]; then
    /etc/init.d/sing-box stop 2>/dev/null
    /etc/init.d/sing-box disable 2>/dev/null
    (crontab -l 2>/dev/null | grep -v "sb-sub update") | crontab -
fi
exit 0
"""

control_buf = io.BytesIO()
with tarfile.open(fileobj=control_buf, mode="w:gz") as tar:
    info = tarfile.TarInfo(name="./control")
    c_bytes = control_content.encode('utf-8')
    info.size = len(c_bytes)
    info.mode = 0o644
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(c_bytes))

    info = tarfile.TarInfo(name="./postinst")
    p_bytes = postinst_content.encode('utf-8')
    info.size = len(p_bytes)
    info.mode = 0o755
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(p_bytes))

    info = tarfile.TarInfo(name="./prerm")
    pr_bytes = prerm_content.encode('utf-8')
    info.size = len(pr_bytes)
    info.mode = 0o755
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(pr_bytes))

control_tar_gz = control_buf.getvalue()

data_buf = io.BytesIO()
with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
    def add_target_file(src_path, arc_path, mode=0o644):
        if not os.path.exists(src_path):
            return
        with open(src_path, "rb") as f:
            data = f.read()
        info = tarfile.TarInfo(name=arc_path)
        info.size = len(data)
        info.mode = mode
        info.mtime = int(time.time())
        tar.addfile(info, io.BytesIO(data))

    add_target_file(os.path.join(project_dir, "luasrc", "controller", "singbox.lua"), "./usr/lib/lua/luci/controller/singbox.lua", 0o644)
    add_target_file(os.path.join(project_dir, "luasrc", "view", "singbox", "singbox.htm"), "./usr/lib/lua/luci/view/singbox/singbox.htm", 0o644)
    add_target_file(os.path.join(project_dir, "root", "usr", "bin", "sb-sub"), "./usr/bin/sb-sub", 0o755)
    add_target_file(os.path.join(project_dir, "root", "usr", "bin", "sb-node"), "./usr/bin/sb-node", 0o755)
    add_target_file(os.path.join(project_dir, "root", "etc", "init.d", "sing-box"), "./etc/init.d/sing-box", 0o755)
    add_target_file(os.path.join(project_dir, "root", "etc", "sing-box", "config.json.example"), "./etc/sing-box/config.json.example", 0o644)
    add_target_file(os.path.join(project_dir, "root", "etc", "sing-box", "subscriptions.json.example"), "./etc/sing-box/subscriptions.json.example", 0o644)
    
    rules_dir = os.path.join(project_dir, "rulesets")
    if os.path.exists(rules_dir):
        for r in os.listdir(rules_dir):
            if r.endswith(".srs"):
                add_target_file(os.path.join(rules_dir, r), f"./opt/sing-box/{r}", 0o644)

data_tar_gz = data_buf.getvalue()

with tarfile.open(ipk_path, mode="w:gz") as tar:
    info = tarfile.TarInfo(name="./debian-binary")
    info.size = len(debian_binary)
    info.mode = 0o644
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(debian_binary))

    info = tarfile.TarInfo(name="./control.tar.gz")
    info.size = len(control_tar_gz)
    info.mode = 0o644
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(control_tar_gz))

    info = tarfile.TarInfo(name="./data.tar.gz")
    info.size = len(data_tar_gz)
    info.mode = 0o644
    info.mtime = int(time.time())
    tar.addfile(info, io.BytesIO(data_tar_gz))

print(f"Successfully generated IPK package: {ipk_path}")
print(f"Package size: {os.path.getsize(ipk_path)} bytes")
