"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 - 本地輕量 Web 伺服器
以 Python 標準庫 http.server 打造，提供 Web 介面伺服與 Gemini AI 智慧敘事 API 後端。
完全無需額外安裝龐大的 Web 框架，雙擊即可直接執行。
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 確保可載入生成模組
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dnd_npc_generator.ai_generator import AINPCGenerator
from dnd_npc_generator.exporter import format_vertical_preview_card


class DndWebHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/generate":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                req_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
                data = json.loads(req_body)

                api_key = data.get("api_key")
                model_name = data.get("model", "gemini-3.5-flash-lite")
                force_ai = data.get("force_ai", True)

                gen = AINPCGenerator(api_key=api_key, model_name=model_name)
                npc = gen.generate(
                    name=data.get("name"),
                    race_name=data.get("race"),
                    class_name=data.get("class_name"),
                    background_name=data.get("background"),
                    level_input=data.get("level", "1"),
                    importance=data.get("importance", "次要劇情 NPC (Supporting)"),
                    story_context=data.get("story_context"),
                    custom_trait_keyword=data.get("custom_trait"),
                    force_ai=force_ai
                )
                card_text = format_vertical_preview_card(npc)

                resp = json.dumps({
                    "status": "success",
                    "npc": npc,
                    "card": card_text
                }, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(resp.encode("utf-8"))
            except Exception as e:
                err_resp = json.dumps({
                    "status": "error",
                    "message": str(e)
                }, ensure_ascii=False)
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(err_resp.encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")


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
