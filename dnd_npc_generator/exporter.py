"""
NPC 角色卡格式化與直向預覽文檔模組 (Exporter & Vertical Preview)
特色：
1. 直向閱讀預覽文檔 (Vertical Quick-Scan Document)：
   專為 DM 跑團備戰設計，一眼掌握身分、戰力、特殊武器與外貌神韻。
2. 靈活展示：
   原始擲骰池、職業建議配置、種族加值備選、非典型裝備（草耙、老煙斗等）。
3. 扁平化資料對接介面：
   準備好在確認後精準寫入使用者上傳的 Excel 模板。
"""

import json
from typing import Dict, Optional


def format_vertical_preview_card(npc: Dict) -> str:
    """
    格式化為清晰且資訊豐富的直向快速掃視 NPC 角色卡 (Vertical Quick-Scan Card)
    """
    app = npc.get("appearance", {})
    lines = []
    lines.append(f"# 📜 D&D 5E 劇情向 NPC 角色卡：{npc['name']}")
    lines.append(f"> **定位**：{npc['importance']} | **等級**：{npc['level_display']} | **預估挑戰等級**：{npc.get('cr', 'CR 1/4')}")
    lines.append(f"> **陣營**：{npc['alignment']} | **熟練加值 (PB)**：{npc['proficiency_bonus']}")
    lines.append(f"> **生命值 (HP)**：約 {npc['hp']} ({npc['hit_dice']}) | **速度**：{npc['speed']} | **感官**：{npc['darkvision']}")
    lines.append("")

    # 1. 生理外貌與視覺神態
    lines.append("## 👤 基礎身分與外貌特徵")
    lines.append(f"- **種族**：{npc['race']}")
    lines.append(f"- **職業**：{npc['class']}")
    lines.append(f"- **性別與年齡**：{npc['gender']}，{npc['age']['display']}")
    lines.append(f"- **體型與體魄**：{app.get('size', '中型')}，身高約 {app.get('height', '—')}，體重約 {app.get('weight', '—')}")
    lines.append(f"- **容貌細節**：髮色【{app.get('hair', '—')}】、瞳色【{app.get('eyes', '—')}】、膚色【{app.get('skin', '—')}】")
    lines.append(f"- **視覺神態**：{app.get('feature_look', '沉穩警戒。')}")
    lines.append(f"- **背景歷練**：{npc['background']}")
    lines.append(f"- **信仰**：{npc['deity']}")
    lines.append(f"- **已知語言**：{', '.join(npc['racial_languages'])}")
    lines.append(f"- **背景特性**：{npc['bg_feature']}")
    lines.append(f"- **背景熟練選項**：{npc['bg_skills']} ； 工具：{npc['bg_tools']} ； 語言：{npc['bg_languages']}")
    lines.append("")

    # 2. 靈活屬性面板 (不強制寫死，列出建議配置與種族加值清單)
    lines.append("## 🎲 靈活屬性面板 (4d6 drop lowest 1 實擲)")
    lines.append(f"**原始擲骰點數池 (Raw Rolls)**：{npc['raw_scores']}")
    lines.append(f"*{npc['primary_recommendation']}*")
    lines.append("")
    lines.append("| 屬性 (Stat) | 建議基礎點數 (Recommended) | 基礎調整值 | 適用種族加值清單 (Available Racial Bonuses) |")
    lines.append("| :--- | :---: | :---: | :--- |")
    
    rec = npc["recommended_allocation"]
    racial_bonus_note = npc["racial_bonus_options"]
    
    stat_names = [
        ("STR", "力量 STR"), ("DEX", "敏捷 DEX"), ("CON", "體魄 CON"),
        ("INT", "智力 INT"), ("WIS", "感知 WIS"), ("CHA", "魅力 CHA")
    ]
    for key, label in stat_names:
        item = rec[key]
        lines.append(f"| **{label}** | {item['recommended_base']} | **{item['base_mod_str']}** | （可自由選擇套用：{racial_bonus_note}） |")
    lines.append("")

    # 3. 隨身非典型裝備與武器庫 (含攻擊傷害骰與趣味故事法器)
    lines.append("## 🎒 隨身裝備、武器與故事道具 (Weapons & Props)")
    equip_list = npc.get("equipment", [])
    if equip_list:
        lines.append("| 道具 / 武器名稱 | 類型 | 傷害骰 / 防護 (Damage / AC) | 故事特性與規則備註 (Properties) |")
        lines.append("| :--- | :--- | :---: | :--- |")
        for eq in equip_list:
            dmg_or_ac = eq.get("damage") if (eq.get("damage") and eq.get("damage") != "—") else (eq.get("ac") or "—")
            lines.append(f"| **{eq['name']}** | {eq['type']} | **{dmg_or_ac}** | {eq.get('properties', '')} |")
    else:
        lines.append("- 隨身常服、粗布行囊、日常錢袋。")
    lines.append("")

    # 4. 職業特長與等級解鎖能力庫 (Class Progression & Features)
    lines.append(f"## ⚔️ 職業等級晉升特長 (Lv.{npc['level']} 已解鎖)")
    lines.append(f"- **豁免檢定熟練**：{', '.join(npc['class_saves'])}")
    if npc["unlocked_features"]:
        for feat in npc["unlocked_features"]:
            lines.append(f"- {feat}")
    else:
        lines.append("- （無額外職業特長）")
    lines.append("")

    # 5. 施法者法術位 (Spellcasting Slots)
    spell_info = npc.get("spellcasting_info")
    if spell_info:
        lines.append("## 🔮 施法者法術環位 (Spell Slots)")
        lines.append(f"- **施法類別**：{spell_info['spell_type']}")
        lines.append(f"- **當前可用法術位**：{spell_info['slots_by_circle']}")
        if "⚠️" in spell_info["status_remark"]:
            lines.append(f"- **狀態限制**：{spell_info['status_remark']}")
        lines.append("")

    # 6. 獨特非傳統特質 (Unique Characteristic)
    lines.append("## ✨ 獨特非傳統特質 (Unique Characteristic)")
    trait = npc.get("unique_trait")
    if trait:
        lines.append(f"### 🌟 【{trait['name']}】（類別：{trait['category']}）")
        lines.append(f"- **特質描述**：{trait['description']}")
        lines.append(f"- **遊戲規則效果**：{trait['game_effect']}")
    else:
        lines.append("🌿 **此角色為常規市井人物/普通冒險者**：無額外超常神異特質，完全依循常規 D&D 5E 規則。")
    lines.append("")

    # 7. 背景短史與劇本整合 (Backstory & Campaign Hook)
    lines.append("## 📖 簡約背景短史與劇本線索 (Backstory & Hook)")
    bg = npc["backstory"]
    lines.append(f"- **身分綜述**：{bg['summary']}")
    lines.append(f"- **個性特質**：{bg['personality']}")
    lines.append(f"- **理想 (Ideal)**：{bg['ideal']}")
    lines.append(f"- **牽絆 (Bond)**：{bg['bond']}")
    lines.append(f"- **缺點 (Flaw)**：{bg['flaw']}")
    lines.append(f"- **🎯 劇本引子**：{bg['story_hook']}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


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


# 模組外觀別名
format_vertical_preview = format_vertical_preview_card
render_markdown_card = format_vertical_preview_card
export_json = export_to_json
export_csv = export_to_csv



def get_flattened_dict_for_excel(npc: Dict) -> Dict[str, str]:
    rec = npc["recommended_allocation"]
    trait = npc.get("unique_trait") or {}
    bg = npc.get("backstory") or {}
    spell_info = npc.get("spellcasting_info") or {}
    app = npc.get("appearance", {})

    flat_data = {
        "角色姓名": npc["name"],
        "性別": npc["gender"],
        "所屬陣營": npc["alignment"],
        "重要性定位": npc["importance"],
        "等級標籤": npc["level_display"],
        "等級數字": str(npc["level"]),
        "挑戰等級_CR": npc.get("cr", "CR 1/4"),
        "熟練加值_PB": npc["proficiency_bonus"],
        "種族": npc["race"],
        "種族可選加值清單": npc["racial_bonus_options"],
        "職業": npc["class"],
        "背景": npc["background"],
        "年齡": str(npc["age"]["age_number"]),
        "年齡階段": npc["age"]["stage"],
        "體型": app.get("size", "中型"),
        "身高": app.get("height", ""),
        "體重": app.get("weight", ""),
        "髮色": app.get("hair", ""),
        "瞳色": app.get("eyes", ""),
        "膚色": app.get("skin", ""),
        "外貌神態": app.get("feature_look", ""),
        "信仰神祇": npc["deity"],
        "預估生命值_HP": str(npc["hp"]),
        "生命骰": npc["hit_dice"],
        "移動速度": npc["speed"],
        "感官視覺": npc["darkvision"],
        
        # 原始骰點與建議配置
        "4d6dl1原始點數池": ", ".join(map(str, npc["raw_scores"])),
        "建議力量_STR": str(rec["STR"]["recommended_base"]),
        "建議力量調整值": rec["STR"]["base_mod_str"],
        "建議敏捷_DEX": str(rec["DEX"]["recommended_base"]),
        "建議敏捷調整值": rec["DEX"]["base_mod_str"],
        "建議體魄_CON": str(rec["CON"]["recommended_base"]),
        "建議體魄調整值": rec["CON"]["base_mod_str"],
        "建議智力_INT": str(rec["INT"]["recommended_base"]),
        "建議智力調整值": rec["INT"]["base_mod_str"],
        "建議感知_WIS": str(rec["WIS"]["recommended_base"]),
        "建議感知調整值": rec["WIS"]["base_mod_str"],
        "建議魅力_CHA": str(rec["CHA"]["recommended_base"]),
        "建議魅力調整值": rec["CHA"]["base_mod_str"],
        
        # 熟練與特長
        "豁免熟練": "、".join(npc["class_saves"]),
        "職業解鎖特長清單": " \n ".join(npc["unlocked_features"]),
        "施法環位": spell_info.get("slots_by_circle", "無"),
        "施法限制狀態": spell_info.get("status_remark", "無"),
        
        # 裝備清單
        "武器與裝備明細": " \n ".join([
            f"{eq['name']} ({eq.get('damage', eq.get('ac', ''))}) [{eq.get('properties', '')}]"
            for eq in npc.get("equipment", [])
        ]),
        
        # 獨特特質
        "獨特特質名稱": trait.get("name", "無 (常規市井角色)"),
        "獨特特質類別": trait.get("category", "無"),
        "獨特特質描述": trait.get("description", "無"),
        "獨特特質規則效果": trait.get("game_effect", "無"),
        
        # 背景與劇情
        "背景特性": npc["bg_feature"],
        "身分短史綜述": bg.get("summary", ""),
        "個性特質": bg.get("personality", ""),
        "理想": bg.get("ideal", ""),
        "牽絆": bg.get("bond", ""),
        "缺點": bg.get("flaw", ""),
        "劇本關聯線索": bg.get("story_hook", "")
    }

    return flat_data
