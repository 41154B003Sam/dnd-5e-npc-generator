"""
NPC 角色卡格式化與直向預覽文檔模組 (Exporter & Vertical Preview)
特色：
1. 直向閱讀預覽文檔 (Vertical Quick-Scan Document)：
   專為 DM 跑團備戰設計，一眼掌握身分、戰力、特殊武器、AI 原創背景與生活神韻。
2. 靈活展示：
   原始擲骰池、職業建議配置、種族加值備選、非典型裝備（草耙、老煙斗等）。
3. 通用匯出：
   支援 Markdown 卡片、通用 CSV 試算表與標準結構化 JSON。
"""

import json
from typing import Dict, Optional


def format_vertical_preview_card(npc: Dict) -> str:
    """
    格式化為清晰且資訊豐富的直向快速掃視 NPC 角色卡 (Vertical Quick-Scan Card)
    """
    app = npc.get("appearance", {})
    lines = []
    lines.append(f"# 📜 D&D 5E 劇情向 NPC 角色卡：{npc.get('name', '未命名')}")
    
    level_str = f"Lv.{npc.get('level', 1)}"
    if npc.get("level_note"):
        level_str += f" ({npc['level_note']})"
        
    lines.append(f"> **定位**：{npc.get('importance', '次要劇情 NPC')} | **等級**：{level_str} | **預估挑戰等級**：{npc.get('cr', 'CR 1/4')}")
    lines.append(f"> **陣營**：{npc.get('alignment', '中立')} | **熟練加值 (PB)**：{npc.get('proficiency_bonus', '+2')}")
    lines.append(f"> **生命值 (HP)**：約 {npc.get('hp', 10)} | **速度**：{npc.get('speed', '30 呎')} | **感官**：{npc.get('darkvision', '常規視力')}")
    if npc.get("ai_crafted"):
        lines.append(f"> 🤖 **生成模式**：【Gemini AI 原創深度敘事版】")
    lines.append("")

    # 1. 生理外貌與視覺神態
    lines.append("## 👤 基礎身分與外貌特徵")
    lines.append(f"- **種族**：{npc.get('race', '人類')}")
    lines.append(f"- **職業**：{npc.get('class', npc.get('class_name', '戰士'))}")
    lines.append(f"- **性別與年齡**：{npc.get('gender', '未知')}，{npc.get('age', {}).get('display', '中年')}")
    if app:
        lines.append(f"- **體型與體魄**：{app.get('size', '中型')}，身高約 {app.get('height', '—')}，體重約 {app.get('weight', '—')}")
        lines.append(f"- **容貌細節**：髮色【{app.get('hair', '—')}】、瞳色【{app.get('eyes', '—')}】、膚色【{app.get('skin', '—')}】")
        lines.append(f"- **視覺神態**：{app.get('feature_look', '沉穩警戒。')}")
    lines.append(f"- **背景歷練**：{npc.get('background', '平民民兵')}")
    lines.append(f"- **信仰**：{npc.get('deity', '萬物有靈')}")
    lines.append(f"- **已知語言**：{', '.join(npc.get('racial_languages', ['通用語']))}")
    if npc.get("bg_feature"):
        lines.append(f"- **背景特性**：{npc['bg_feature']}")
    if npc.get("bg_proficiencies"):
        lines.append(f"- **背景熟練**：{npc['bg_proficiencies']}")
    lines.append("")

    # 2. 靈活屬性面板 (不強制寫死，列出建議配置與種族加值清單)
    lines.append("## 🎲 靈活屬性面板 (4d6 drop lowest 1 實擲)")
    lines.append(f"**原始擲骰點數池 (Raw Rolls)**：{npc.get('raw_ability_rolls', npc.get('raw_scores', []))}")
    lines.append(f"*主屬性建議配置：依據 {npc.get('class', '職業')} 機制提供最優推薦配置與加值清單*")
    lines.append("")
    lines.append("| 屬性 (Stat) | 建議基礎點數 (Recommended) | 基礎調整值 | 適用種族加值清單 (Available Racial Bonuses) |")
    lines.append("| :--- | :---: | :---: | :--- |")
    
    rec = npc.get("recommended_allocation", {})
    racial_bonus_note = npc.get("racial_bonus_options", "可自由配置")
    
    stat_names = [
        ("STR", "力量 STR"), ("DEX", "敏捷 DEX"), ("CON", "體魄 CON"),
        ("INT", "智力 INT"), ("WIS", "感知 WIS"), ("CHA", "魅力 CHA")
    ]
    for key, label in stat_names:
        if key in rec:
            item = rec[key]
            lines.append(f"| **{label}** | {item.get('recommended_base', 10)} | **{item.get('base_mod_str', '+0')}** | （可自由選擇套用：{racial_bonus_note}） |")
    lines.append("")

    # 3. 隨身非典型裝備與武器庫 (含攻擊傷害骰與生活故事道具)
    lines.append("## 🎒 隨身裝備、生活武器與故事道具 (Weapons & Props)")
    equip_list = npc.get("ai_unorthodox_equipment") or npc.get("equipment", [])
    if equip_list:
        lines.append("| 道具 / 武器名稱 | 類型 | 傷害骰 / 防護 (Damage / AC) | 故事特性與規則備註 (Properties) |")
        lines.append("| :--- | :--- | :---: | :--- |")
        for eq in equip_list:
            dmg_or_ac = eq.get("damage") if (eq.get("damage") and eq.get("damage") != "—") else (eq.get("ac") or "—")
            lore = f" ； {eq.get('story_lore')}" if eq.get("story_lore") else ""
            lines.append(f"| **{eq['name']}** | {eq.get('type', '道具')} | **{dmg_or_ac}** | {eq.get('properties', '')}{lore} |")
    else:
        lines.append("- 隨身常服、粗布行囊、日常錢袋。")
    lines.append("")

    # 4. 職業特長與等級解鎖能力庫 (Class Progression & Features)
    lines.append(f"## ⚔️ 職業等級晉升特長 (Lv.{npc.get('level', 1)} 已解鎖)")
    unlocked = npc.get("unlocked_features", [])
    if unlocked:
        for feat in unlocked:
            lines.append(f"- {feat}")
    else:
        lines.append("- （無額外職業特長）")
    lines.append("")

    # 5. 獨特非傳統特質 (Unique Characteristic)
    lines.append("## ✨ 獨特非傳統特質 (Unique Characteristic)")
    trait = npc.get("unique_trait")
    if trait:
        lines.append(f"### 🌟 【{trait.get('name', '特殊特長')}】（類別：{trait.get('category', '特長')}）")
        if trait.get("description"):
            lines.append(f"- **特質描述**：{trait['description']}")
        lines.append(f"- **遊戲規則效果**：{trait.get('game_effect', '無特殊規則')}")
    else:
        lines.append("🌿 **此角色為常規市井人物/普通冒險者**：無額外超常神異特質，完全依循常規 D&D 5E 規則。")
    lines.append("")

    # 6. 【AI 原創深度劇情身世與劇本線索】
    if npc.get("ai_backstory"):
        lines.append("## 📖 【AI 原創深度劇情身世 (Backstory)】")
        lines.append(f"{npc['ai_backstory']}")
        lines.append("")

    if npc.get("ai_personality_quirks"):
        lines.append("## 🎭 【個性、言行舉止與生活細節小動作 (Personality & Quirks)】")
        lines.append(f"{npc['ai_personality_quirks']}")
        lines.append("")

    if npc.get("ai_quest_hook"):
        lines.append("## 🎯 【DM 跑團互動與推進伏筆 (Quest Hook)】")
        lines.append(f"{npc['ai_quest_hook']}")
        lines.append("")
    elif npc.get("backstory") and isinstance(npc.get("backstory"), dict):
        bg = npc["backstory"]
        lines.append("## 📖 簡約背景短史與劇本線索 (Backstory & Hook)")
        if "summary" in bg: lines.append(f"- **身分綜述**：{bg['summary']}")
        if "personality" in bg: lines.append(f"- **個性特質**：{bg['personality']}")
        if "story_hook" in bg: lines.append(f"- **🎯 劇本引子**：{bg['story_hook']}")
        lines.append("")

    if npc.get("token_usage"):
        u = npc["token_usage"]
        lines.append("## 📊 【Gemini API 額度與 Token 消耗統計】")
        lines.append(f"- **呼叫模型**：`{u.get('model', 'gemini-3.5-flash-lite')}`")
        lines.append(f"- **輸入提示詞**：{u.get('prompt_tokens', 0)} Tokens（包含 5E 規則規格與劇情提示）")
        lines.append(f"- **創作輸出**：{u.get('candidates_tokens', 0)} Tokens（包含身世、言行舉止與裝備）")
        lines.append(f"- **本次總消耗 Token**：**{u.get('total_tokens', 0)} Tokens**")
        lines.append(f"- **單次預估費用**：約 **{u.get('estimated_cost_usd', '$0.00015')} USD**（換算新台幣約 0.004 元）")
        lines.append(f"- **Google 免費額度**：**{u.get('free_tier_status', 'Google AI Studio 免費額度內 (0 元 / 每日 1,500 次上限)')}**")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)


def get_flattened_dict_for_excel(npc: Dict) -> Dict[str, str]:
    """將 NPC 物件扁平化為鍵值對，以供 CSV 匯出"""
    rec = npc.get("recommended_allocation", {})
    flat = {
        "角色姓名": npc.get("name", ""),
        "種族": npc.get("race", ""),
        "職業": npc.get("class", npc.get("class_name", "")),
        "等級": str(npc.get("level", 1)),
        "等級備註": npc.get("level_note", ""),
        "挑戰等級CR": npc.get("cr", "1/4"),
        "陣營": npc.get("alignment", ""),
        "生命值HP": str(npc.get("hp", 10)),
        "熟練加值PB": npc.get("proficiency_bonus", "+2"),
        "力量STR建議": str(rec.get("STR", {}).get("recommended_base", 10)),
        "敏捷DEX建議": str(rec.get("DEX", {}).get("recommended_base", 10)),
        "體魄CON建議": str(rec.get("CON", {}).get("recommended_base", 10)),
        "智力INT建議": str(rec.get("INT", {}).get("recommended_base", 10)),
        "感知WIS建議": str(rec.get("WIS", {}).get("recommended_base", 10)),
        "魅力CHA建議": str(rec.get("CHA", {}).get("recommended_base", 10)),
        "背景歷練": npc.get("background", ""),
        "信仰神祇": npc.get("deity", ""),
        "已知語言": ", ".join(npc.get("racial_languages", [])),
        "AI劇情身世": npc.get("ai_backstory", ""),
        "AI言行小動作": npc.get("ai_personality_quirks", ""),
        "DM跑團伏筆": npc.get("ai_quest_hook", "")
    }
    return flat


def export_to_json(npc: Dict, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(npc, f, ensure_ascii=False, indent=2)


def export_to_csv(npc: Dict, output_path: str):
    import csv
    flat = get_flattened_dict_for_excel(npc)
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["欄位名稱", "數值內容"])
        for k, v in flat.items():
            writer.writerow([k, v])


format_vertical_preview = format_vertical_preview_card
render_markdown_card = format_vertical_preview_card
export_json = export_to_json
export_csv = export_to_csv
