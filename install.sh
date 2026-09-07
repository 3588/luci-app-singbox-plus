#!/bin/sh
# ==============================================================================
# luci-app-singbox-plus 一键安装脚本
# ==============================================================================

echo "==> 1. 安装核心文件与命令工具..."
mkdir -p /usr/lib/lua/luci/controller /usr/lib/lua/luci/view/singbox /usr/bin /etc/init.d /etc/sing-box /opt/sing-box

cp -f luasrc/controller/singbox.lua /usr/lib/lua/luci/controller/
cp -f luasrc/view/singbox/singbox.htm /usr/lib/lua/luci/view/singbox/
cp -f root/usr/bin/sb-sub /usr/bin/
cp -f root/usr/bin/sb-node /usr/bin/
cp -f root/etc/init.d/sing-box /etc/init.d/

chmod +x /usr/bin/sb-sub /usr/bin/sb-node /etc/init.d/sing-box

echo "==> 2. 部署 GFW 模式二进制规则集..."
if [ -d "rulesets" ]; then
    cp -f rulesets/*.srs /opt/sing-box/
fi

echo "==> 3. 初始化配置文件..."
if [ ! -f "/etc/sing-box/config.json" ]; then
    cp -f root/etc/sing-box/config.json.example /etc/sing-box/config.json
fi

if [ ! -f "/etc/sing-box/subscriptions.json" ]; then
    cp -f root/etc/sing-box/subscriptions.json.example /etc/sing-box/subscriptions.json
fi

echo "==> 4. 配置定时自动订阅同步任务 (每2小时)..."
(crontab -l 2>/dev/null | grep -v "sb-sub update" ; echo "0 */2 * * * /usr/bin/sb-sub update >/dev/null 2>&1") | crontab -
/etc/init.d/cron restart 2>/dev/null

echo "==> 5. 清理 LuCI 缓存并重启服务..."
rm -rf /tmp/luci-indexcache /tmp/luci-modulecache
/etc/init.d/uhttpd restart
/etc/init.d/sing-box enable
/etc/init.d/sing-box restart

echo "=============================================================================="
echo "✔ 安装完成！请访问软路由后台: http://<路由器IP>/cgi-bin/luci/admin/services/singbox"
echo "=============================================================================="
