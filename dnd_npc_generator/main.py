"""
D&D 5E NPC 智慧生成系統主執行程式 (CLI & 示範腳本)
支援互動式終端機指令、即時直向卡片預覽與 Markdown / CSV / JSON 多格式匯出
"""

import argparse
import sys

# 確保 Windows 終端機 UTF-8 編碼正常顯示 Emoji 與繁體中文字元
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dnd_npc_generator.generator import NPCGenerator
from dnd_npc_generator.exporter import format_vertical_preview_card, export_to_json, export_to_csv


def run_generator(
    name=None,
    race=None,
    cls=None,
    bg=None,
    level_input="1",
    importance="次要劇情 NPC (Supporting)",
    story_context=None,
    custom_trait=None,
    output_json=None,
    output_md=None,
    output_csv=None
):
    gen = NPCGenerator()
    npc = gen.generate(
        name=name,
        race_name=race,
        class_name=cls,
        background_name=bg,
        level_input=level_input,
        importance=importance,
        story_context=story_context,
        custom_trait_keyword=custom_trait
    )

    card_text = format_vertical_preview_card(npc)
    print(card_text)

    # 1. 匯出結構化 JSON
    if output_json:
        export_to_json(npc, output_json)
        print(f"\n✅ 成功匯出 JSON 數據檔至：{output_json}")

    # 2. 匯出直向 Markdown 角色卡
    if output_md:
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(card_text)
        print(f"✅ 成功匯出直向 Markdown 角色卡至：{output_md}")

    # 3. 匯出通用 CSV
    if output_csv:
        export_to_csv(npc, output_csv)
        print(f"✅ 成功匯出通用 CSV 試算表至：{output_csv}")

    return npc


def main():
    parser = argparse.ArgumentParser(description="D&D 5E 劇情導向非典型 NPC 智慧生成系統 (繁體中文版)")
    parser.add_argument("--name", type=str, default=None, help="指定 NPC 姓名 (選填)")
    parser.add_argument("--race", type=str, default=None, help="指定種族 (選填，例如：人類、山地矮人、高等精靈)")
    parser.add_argument("--class-name", type=str, default=None, help="指定職業 (選填，例如：戰士、法師、遊盪者)")
    parser.add_argument("--bg", type=str, default=None, help="指定背景 (選填，例如：士兵、侍祭、民間英雄)")
    parser.add_argument("--level", type=str, default="1", help="指定等級數字或關鍵字 (例如：'1'、'大魔導師'、'大魔導師（封印狀態）'、'老兵')")
    parser.add_argument("--importance", type=str, default="次要劇情 NPC (Supporting)", help="NPC 重要性階層")
    parser.add_argument("--story", type=str, default=None, help="補充劇本當前事件或人物線索 (將自然融入角色背景短史)")
    parser.add_argument("--trait", type=str, default=None, help="指定非傳統特質關鍵字 (例如：火焰、霜凍、靈魂；預設無則為一般凡人/平民)")
    parser.add_argument("--output-json", type=str, default=None, help="匯出 JSON 檔案路徑")
    parser.add_argument("--output-csv", type=str, default=None, help="匯出 CSV 試算表路徑")
    parser.add_argument("--output-md", type=str, default=None, help="匯出 Markdown 檔案路徑")

    args = parser.parse_args()

    run_generator(
        name=args.name,
        race=args.race,
        cls=args.class_name,
        bg=args.bg,
        level_input=args.level,
        importance=args.importance,
        story_context=args.story,
        custom_trait=args.trait,
        output_json=args.output_json,
        output_md=args.output_md,
        output_csv=args.output_csv
    )


if __name__ == "__main__":
    main()
