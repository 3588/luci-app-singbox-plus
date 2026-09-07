module("luci.controller.singbox", package.seeall)

function index()
	entry({"admin", "services", "singbox"}, template("singbox/singbox"), _("Sing-Box"), 2).dependent = true
	entry({"admin", "services", "singbox", "status"}, call("action_status")).leaf = true
	entry({"admin", "services", "singbox", "service"}, call("action_service")).leaf = true
	entry({"admin", "services", "singbox", "nodes"}, call("action_nodes")).leaf = true
	entry({"admin", "services", "singbox", "add_node"}, call("action_add_node")).leaf = true
	entry({"admin", "services", "singbox", "del_node"}, call("action_del_node")).leaf = true
	entry({"admin", "services", "singbox", "subs"}, call("action_subs")).leaf = true
	entry({"admin", "services", "singbox", "sub_add"}, call("action_sub_add")).leaf = true
	entry({"admin", "services", "singbox", "sub_del"}, call("action_sub_del")).leaf = true
	entry({"admin", "services", "singbox", "sub_update"}, call("action_sub_update")).leaf = true
end

function action_status()
	local sys = require "luci.sys"
	local running = (sys.call("pidof sing-box >/dev/null") == 0)
	luci.http.prepare_content("application/json")
	luci.http.write_json({ running = running })
end

function action_service()
	local sys = require "luci.sys"
	local act = luci.http.formvalue("act")
	if act == "restart" then
		sys.call("/etc/init.d/sing-box restart")
	elseif act == "start" then
		sys.call("/etc/init.d/sing-box start")
	elseif act == "stop" then
		sys.call("/etc/init.d/sing-box stop")
	end
	luci.http.prepare_content("application/json")
	luci.http.write_json({ success = true })
end

function action_nodes()
	local sys = require "luci.sys"
	local out = sys.exec("/usr/bin/sb-node list")
	luci.http.prepare_content("application/json")
	luci.http.write(out)
end

function action_add_node()
	local http = require "luci.http"
	local json = require "luci.jsonc"
	local sys = require "luci.sys"
	local fs = require "nixio.fs"

	local links_raw = http.formvalue("links") or ""
	local tmp_file = "/tmp/new_links.txt"
	fs.writefile(tmp_file, links_raw)

	local results = {}
	local any_success = false
	local f = io.open(tmp_file, "r")
	if f then
		for line in f:lines() do
			line = line:gsub("^%s+", ""):gsub("%s+$", "")
			if line:match("^vless://") or line:match("^tuic://") or line:match("^hysteria2://") or line:match("^hy2://") then
				local esc_line = line:gsub("'", "'\''")
				local res = sys.exec("/usr/bin/sb-node add '" .. esc_line .. "'")
				local r = json.parse(res)
				if r and r.success then
					any_success = true
					table.insert(results, { link = line, success = true, tag = r.tag })
				else
					table.insert(results, { link = line, success = false, error = (r and r.error) or "Error" })
				end
			end
		end
		f:close()
	end
	os.remove(tmp_file)
	luci.http.prepare_content("application/json")
	luci.http.write_json({ success = any_success, results = results })
end

function action_del_node()
	local http = require "luci.http"
	local sys = require "luci.sys"
	local tag = http.formvalue("tag") or ""
	local esc_tag = tag:gsub("'", "'\''")
	local out = sys.exec("/usr/bin/sb-node del '" .. esc_tag .. "'")
	luci.http.prepare_content("application/json")
	luci.http.write(out)
end

function action_subs()
	local sys = require "luci.sys"
	local out = sys.exec("/usr/bin/sb-sub list")
	luci.http.prepare_content("application/json")
	luci.http.write(out)
end

function action_sub_add()
	local http = require "luci.http"
	local sys = require "luci.sys"
	local name = http.formvalue("name") or "Sub"
	local url = http.formvalue("url") or ""
	local esc_name = name:gsub("'", "'\''")
	local esc_url = url:gsub("'", "'\''")
	local out = sys.exec("/usr/bin/sb-sub add '" .. esc_name .. "' '" .. esc_url .. "'")
	luci.http.prepare_content("application/json")
	luci.http.write(out)
end

function action_sub_del()
	local http = require "luci.http"
	local sys = require "luci.sys"
	local name = http.formvalue("name") or ""
	local esc_name = name:gsub("'", "'\''")
	local out = sys.exec("/usr/bin/sb-sub del '" .. esc_name .. "'")
	luci.http.prepare_content("application/json")
	luci.http.write(out)
end

function action_sub_update()
	local sys = require "luci.sys"
	local out = sys.exec("/usr/bin/sb-sub update")
	luci.http.prepare_content("application/json")
	luci.http.write(out)
end
