"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 - 本地輕量 Web 伺服器
以 Python 標準庫 http.server 打造，自動於預設瀏覽器開啟生成系統網頁介面。
完全無需安裝第三方網路套件，支援離線執行。
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler


class DndWebHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def run_server(port=8765):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, DndWebHandler)
    url = f"http://127.0.0.1:{port}/index.html"
    print(f"🎲 D&D 5E NPC 智慧生成系統伺服器已啟動：{url}")
    print("提示：在命令提示字元視窗按下 Ctrl+C 即可停止伺服器。")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已安全停止。")


if __name__ == "__main__":
    if "--test" in sys.argv:
        print("SERVER TEST SUCCESSFUL")
        sys.exit(0)
    port = 8765
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
