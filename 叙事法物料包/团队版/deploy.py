#!/usr/bin/env python3
"""54项业务叙事法 · 内网一键部署脚本"""
import http.server, socketserver, os, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIR)
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
print(f"\n✅ 54项业务叙事法 已启动")
print(f"   ├─ 本地访问: http://localhost:{PORT}")
print(f"   ├─ 内网访问: http://{os.popen('hostname -I 2>nul||ipconfig|findstr IPv4').read().strip().split()[-1]}:{PORT}")
print(f"   ├─ 目录: {DIR}")
print(f"   └─ 按 Ctrl+C 停止\n")
httpd.serve_forever()
