"""
D&D 5E Excel 官方角色卡模板直接回填引擎 (Excel Template Direct Populator)
將生成的 NPC 完整資料精準填入使用者上傳之 19 個工作表 D&D 5E 官方試算表模板：
1. 填入【角色卡】：驅動主要數值、職業 (Z16)、等級 (AJ16)、6大屬性 (F15:F20)、非典型裝備武器庫 (V37:AV40)、已解鎖特長 (AT56+) 與種族背景 (V56+)。
2. 自動連動【角色簡卡】：由 Excel 內建公式自動同步連鎖更新。
3. 填入【魔寵數據 / NPC數據】：填寫怪物/NPC 專用數據卡，包含 CR (B42)、HP、AC、速度、感官能力與隨身道具。
"""

import os
import shutil
import re
from typing import Dict, Optional
import openpyxl


def map_class_to_template_format(class_name: str) -> str:
    """
    將繁中職業名稱映射至 Excel 模板 Z16 公式所認得的名稱格式 (例如：戰士-Fighter、法師-Wizard)
    """
    class_map = {
        "戰士": "戰士-Fighter",
        "法師": "法師-Wizard",
        "遊盪者": "盜賊-Rogue",
        "盜賊": "盜賊-Rogue",
        "野蠻人": "野蠻人-Barbarian",
        "聖騎士": "聖騎士-Paladin",
        "牧師": "牧師-Cleric",
        "遊俠": "遊俠-Ranger",
        "武僧": "武僧-Monk",
        "吟遊詩人": "吟遊詩人-Bard",
        "詩人": "吟遊詩人-Bard",
        "德魯伊": "德魯伊-Druid",
        "術士": "術士-Sorcerer",
        "契術師": "契術師-Warlock",
        "邪術師": "契術師-Warlock"
    }
    for k, v in class_map.items():
        if k in class_name:
            return v
    return "戰士-Fighter"


def map_size_to_npc_format(size_str: str) -> str:
    """
    將體型映射為 NPC 數據頁面認識的字串
    """
    if "小" in size_str:
        return "小型Small"
    elif "大" in size_str:
        return "大型Large"
    return "中型Medium"


def clean_cr_string(cr_str: str) -> str:
    """
    解析 CR 字串，如 'CR 1/4 (或 CR 1/2)' -> '1/4'
    """
    if not cr_str:
        return "1/4"
    match = re.search(r"(\d+/\d+|\d+)", cr_str)
    if match:
        return match.group(1)
    return "1/4"


def fill_excel_template(
    npc: Dict,
    template_path: str,
    output_path: str
) -> str:
    """
    將 npc 字典中的資料精確回填至 template_path，並另存為 output_path
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"找不到 Excel 模板檔案：{template_path}")

    # 複製模板檔案以確保原始範本不受破壞
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(template_path, output_path)

    wb = openpyxl.load_workbook(output_path)

    rec = npc.get("recommended_allocation", {})
    app = npc.get("appearance", {})
    trait = npc.get("unique_trait")
    bg = npc.get("backstory", {})

    # ==========================================
    # 1. 回填【角色卡】(Master Character Sheet)
    # ==========================================
    if "角色卡" in wb.sheetnames:
        ws_char = wb["角色卡"]

        # 基本身分與外貌 (Row 7, 9)
        ws_char["C7"] = npc.get("name", "未命名角色")
        ws_char["O7"] = "DM (劇情非玩家角色)"
        ws_char["W7"] = npc.get("race", "人類")
        ws_char["AN7"] = npc.get("race", "人類")
        ws_char["AX7"] = npc.get("alignment", "中立")
        ws_char["BG7"] = npc.get("deity", "無特定信仰")

        ws_char["C9"] = app.get("size", "中型")
        ws_char["H9"] = app.get("hair", "灰黑")
        ws_char["N9"] = app.get("skin", "風霜古銅色")
        ws_char["T9"] = app.get("eyes", "深邃")
        ws_char["AA9"] = app.get("height", "175 公分")
        ws_char["AI9"] = app.get("weight", "150 磅")
        ws_char["AN9"] = str(npc.get("age", {}).get("display", "30 歲"))
        ws_char["AX9"] = npc.get("background", "平民")

        # 職業與等級
        template_class = map_class_to_template_format(npc.get("class", "戰士"))
        ws_char["Z16"] = template_class
        ws_char["AJ16"] = int(npc.get("level", 1))

        # 6 大核心屬性點數 (F15:F20)
        ws_char["F15"] = int(rec.get("STR", {}).get("recommended_base", 10))
        ws_char["F16"] = int(rec.get("DEX", {}).get("recommended_base", 10))
        ws_char["F17"] = int(rec.get("CON", {}).get("recommended_base", 10))
        ws_char["F18"] = int(rec.get("INT", {}).get("recommended_base", 10))
        ws_char["F19"] = int(rec.get("WIS", {}).get("recommended_base", 10))
        ws_char["F20"] = int(rec.get("CHA", {}).get("recommended_base", 10))

        # 生命值與護甲防禦
        ws_char["V27"] = int(npc.get("hp", 10))
        equipment_list = npc.get("equipment", [])

        # 尋找護甲與盾牌
        armor_found = False
        for eq in equipment_list:
            eq_type = eq.get("type", "")
            if "甲" in eq_type or "護甲" in eq.get("name", ""):
                ws_char["BH27"] = eq.get("name", "")
                # 抽取 AC 數值
                ac_match = re.search(r"\d+", eq.get("ac", "10"))
                if ac_match:
                    ws_char["AN27"] = int(ac_match.group(0))
                armor_found = True
            elif "盾" in eq.get("name", ""):
                ws_char["AT27"] = 2

        if not armor_found:
            ws_char["BH27"] = "隨身日常衣物"
            ws_char["AN27"] = 10

        # 回填武器庫 (Slot 1 ~ Slot 4 -> Row 37 ~ Row 40)
        weapon_idx = 0
        for eq in equipment_list:
            if "武器" in eq.get("type", "") or "農具" in eq.get("type", "") or "工具" in eq.get("type", "") or "法器" in eq.get("type", ""):
                target_row = 37 + weapon_idx
                if target_row <= 41:
                    ws_char[f"V{target_row}"] = eq.get("name", "")
                    
                    # 傷害骰與調整值
                    dmg = eq.get("damage", "—")
                    if dmg != "—":
                        ws_char[f"AL{target_row}"] = dmg
                    
                    # 命中加值估算：PB + 力量/敏捷調整值
                    str_mod = (int(rec.get("STR", {}).get("recommended_base", 10)) - 10) // 2
                    dex_mod = (int(rec.get("DEX", {}).get("recommended_base", 10)) - 10) // 2
                    pb = int(npc.get("proficiency_bonus", "+2").replace("+", ""))
                    hit_bonus = pb + (dex_mod if "靈巧" in eq.get("properties", "") or "遠程" in eq.get("type", "") else str_mod)
                    ws_char[f"AI{target_row}"] = f"+{hit_bonus}" if hit_bonus >= 0 else str(hit_bonus)
                    ws_char[f"AS{target_row}"] = f"+{str_mod}" if str_mod >= 0 else str(str_mod)
                    ws_char[f"AV{target_row}"] = eq.get("properties", "")
                    weapon_idx += 1

        # 回填特徵與能力 (V56+ 為種族背景特質，AT56+ 為職業等級特長)
        ws_char["V56"] = "【種族、背景與非典型特長】"
        ws_char["V57"] = f"背景特性：{npc.get('bg_feature', '市井生活歷練')}"
        ws_char["V58"] = f"已知語言：{', '.join(npc.get('racial_languages', ['通用語']))}"
        if trait:
            ws_char["V59"] = f"🌟【{trait['name']}】({trait['category']})：{trait['game_effect']}"
        else:
            ws_char["V59"] = "🌿 常規凡人：完全遵循標準冒險者/市井規則，無超常異變。"
        
        ws_char["V60"] = f"🎯 劇本線索：{bg.get('story_hook', '')}"

        # 職業已解鎖特長 (AT56 起)
        features = npc.get("unlocked_features", [])
        for i, feat in enumerate(features[:12]):
            ws_char[f"AT{56 + i}"] = feat

    # ==========================================
    # 2. 回填【魔寵數據】(專用 NPC數據卡)
    # ==========================================
    if "魔寵數據" in wb.sheetnames:
        ws_npc = wb["魔寵數據"]

        ws_npc["B3"] = npc.get("name", "未命名 NPC")
        ws_npc["O3"] = map_size_to_npc_format(app.get("size", "中型"))
        ws_npc["B5"] = str(npc.get("age", {}).get("display", "中年"))
        ws_npc["G5"] = npc.get("gender", "未知")
        ws_npc["L5"] = f"人型生物 ({npc.get('race', '人類')})"
        ws_npc["X5"] = npc.get("alignment", "中立")

        # 生命值與護甲
        ws_npc["H9"] = int(npc.get("hp", 10))
        ws_npc["H11"] = 16 if "重甲" in str(equipment_list) else 13

        # 6 大屬性實數 (B36:Q36)
        ws_npc["B36"] = int(rec.get("STR", {}).get("recommended_base", 10))
        ws_npc["E36"] = int(rec.get("DEX", {}).get("recommended_base", 10))
        ws_npc["H36"] = int(rec.get("CON", {}).get("recommended_base", 10))
        ws_npc["K36"] = int(rec.get("INT", {}).get("recommended_base", 10))
        ws_npc["N36"] = int(rec.get("WIS", {}).get("recommended_base", 10))
        ws_npc["Q36"] = int(rec.get("CHA", {}).get("recommended_base", 10))

        # 移動速度 (B39) 與挑戰等級 CR (B42)
        speed_match = re.search(r"\d+", npc.get("speed", "30"))
        ws_npc["B39"] = int(speed_match.group(0)) if speed_match else 30
        ws_npc["B42"] = clean_cr_string(npc.get("cr", "1/4"))

        # 黑暗視覺 (P41)
        if "60" in npc.get("darkvision", ""):
            ws_npc["P41"] = 60
        elif "120" in npc.get("darkvision", ""):
            ws_npc["P41"] = 120
        else:
            ws_npc["P41"] = 0

        # 隨身武器與物品清單 (AH5 起)
        ws_npc["AH4"] = "隨身物品 / 非典型故事武器"
        for i, eq in enumerate(equipment_list[:12]):
            dmg = f" ({eq.get('damage')})" if eq.get('damage') and eq.get('damage') != '—' else ""
            ws_npc[f"AH{5 + i}"] = f"{eq['name']}{dmg} - {eq.get('properties', '')}"

        # 語言清單 (AH33 起)
        langs = npc.get("racial_languages", ["通用語"])
        for i, lang in enumerate(langs[:4]):
            ws_npc[f"AH{33 + i}"] = lang

    # 儲存回填完畢的 Excel 檔案
    wb.save(output_path)
    wb.close()

    return output_path
