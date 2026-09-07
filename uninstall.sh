#!/bin/sh
echo "==> 正在卸载 luci-app-singbox-plus..."
/etc/init.d/sing-box stop 2>/dev/null
/etc/init.d/sing-box disable 2>/dev/null

rm -f /usr/lib/lua/luci/controller/singbox.lua
rm -rf /usr/lib/lua/luci/view/singbox
rm -f /usr/bin/sb-sub /usr/bin/sb-node

# 移除 cron 任务
(crontab -l 2>/dev/null | grep -v "sb-sub update") | crontab -

rm -rf /tmp/luci-indexcache /tmp/luci-modulecache
/etc/init.d/uhttpd restart

echo "✔ 卸载完成！配置文件保留在 /etc/sing-box/。"
