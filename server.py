"""
D&D 5E 劇情向 NPC 產生器 - 本地輕量 Web 伺服器 (Local Web Server)
以 Python 純標準庫 http.server 打造，提供網頁版完整直接下載已回填官方 Excel 角色卡 (.xlsx) 之功能。
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

from dnd_npc_generator.generator import NPCGenerator
from dnd_npc_generator.excel_writer import fill_excel_template


class DndWebHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/generate-and-download-excel":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode("utf-8"))

            gen = NPCGenerator()
            npc = gen.generate(
                name=params.get("name") or None,
                race_name=params.get("race") or None,
                class_name=params.get("class") or None,
                background_name=params.get("background") or None,
                level_input=params.get("level") or "1",
                story_context=params.get("story") or None,
                custom_trait_keyword=params.get("trait") or None
            )

            template_path = os.path.abspath("dnd_5e_character_template.xlsx")
            temp_output = os.path.abspath("temp_download_character_card.xlsx")

            fill_excel_template(npc, template_path, temp_output)

            with open(temp_output, "rb") as f:
                xlsx_bytes = f.read()

            filename = f"DND5E_角色卡_{npc['name']}.xlsx"
            encoded_filename = urllib.parse.quote(filename)

            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_filename}")
            self.send_header("Content-Length", str(len(xlsx_bytes)))
            self.end_headers()
            self.wfile.write(xlsx_bytes)
            return

        self.send_error(404, "Endpoint not found")


def run_server(port=8765):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, DndWebHandler)
    url = f"http://127.0.0.1:{port}/index.html"
    print(f"🎲 D&D 5E NPC 產生器伺服器已啟動於：{url}")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止。")


if __name__ == "__main__":
    port = 8765
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
