"""
D&D 5E Excel 官方角色卡模板直接回填引擎 (Excel Template Direct Populator - Lossless OpenXML Engine)

採用無失真 OpenXML 底層串流注入技術，完整保留模板中所有 19 個工作表、
所有的圖片 (Drawings/Media)、向量繪圖 (VML Drawings)、公式鏈結、條件式格式化與樣式排版。
徹底解決 openpyxl 遺失圖片、損壞繪圖關聯與破壞格式之問題！

回填目標：
1. 【角色卡】：身分、外貌、陣營、職業 (Z16)、等級 (AJ16)、6大屬性實擲 (F15:F20)、
   生命值與護甲、非典型故事武器庫 (V37:AV40)、種族背景特長 (V56+) 與職業進階特長 (AT56+)。
2. 【角色簡卡】：由 Excel 內建公式自動同步連鎖更新。
3. 【魔寵數據 / NPC數據】：怪物/NPC 專用數據卡，包含 CR (B42)、HP、AC、速度、感官能力與隨身道具。
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Tuple


def col2num(col_str: str) -> int:
    """將英文字母欄位 (如 A, B, AX) 轉換為數值索引 (1-based)"""
    num = 0
    for c in col_str.upper():
        num = num * 26 + (ord(c) - ord('A') + 1)
    return num


def split_coord(coord: str) -> Tuple[str, int]:
    """將單元格座標 (如 AX7) 拆分為 ('AX', 7)"""
    m = re.match(r"^([A-Z]+)(\d+)$", coord.upper())
    if not m:
        raise ValueError(f"無效的單元格座標: {coord}")
    return m.group(1), int(m.group(2))


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
    """將體型映射為 NPC 數據頁面認識的字串"""
    if "小" in size_str:
        return "小型Small"
    elif "大" in size_str:
        return "大型Large"
    return "中型Medium"


def clean_cr_string(cr_str: str) -> str:
    """解析 CR 字串，如 'CR 1/4' -> '1/4'"""
    if not cr_str:
        return "1/4"
    match = re.search(r"(\d+/\d+|\d+)", cr_str)
    if match:
        return match.group(1)
    return "1/4"


class LosslessOpenXmlPopulator:
    """
    無損 OpenXML ZIP 直接回填器
    100% 保持所有原有 media、drawings、vmlDrawings、comments 與 rels 檔案完全不變
    僅精準注入文字至 sharedStrings.xml 與更新 sheet XML 中的數值及字串引用
    """
    def __init__(self, template_path: str):
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"找不到 Excel 模板檔案：{template_path}")
        self.template_path = template_path
        self.ns = {
            "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        }
        ET.register_namespace("", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
        ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
        ET.register_namespace("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006")
        ET.register_namespace("x14ac", "http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac")
        ET.register_namespace("x16r2", "http://schemas.microsoft.com/office/spreadsheetml/2015/02/main")

    def populate(self, sheet_updates_by_name: Dict[str, Dict[str, any]], output_path: str):
        with zipfile.ZipFile(self.template_path, "r") as zin:
            all_files = zin.namelist()

            # 1. 讀取 workbook.xml 與 rels 以定位工作表檔案名稱
            wb_xml = zin.read("xl/workbook.xml")
            rels_xml = zin.read("xl/_rels/workbook.xml.rels")
            wb_root = ET.fromstring(wb_xml)
            rels_root = ET.fromstring(rels_xml)

            rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels_root}
            sheet_target_map = {}
            for s in wb_root.findall(".//main:sheet", self.ns):
                name = s.attrib["name"]
                rid = s.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
                target = rel_map.get(rid, "")
                if not target.startswith("xl/"):
                    target = "xl/" + target.lstrip("/")
                sheet_target_map[name] = target

            # 2. 讀取並解析 sharedStrings.xml
            sst_raw = zin.read("xl/sharedStrings.xml")
            sst_root = ET.fromstring(sst_raw)

            sst_map = {}
            total_count = 0
            for i, si in enumerate(sst_root.findall("main:si", self.ns)):
                total_count += 1
                text_parts = [t.text for t in si.findall(".//main:t", self.ns) if t.text]
                full_text = "".join(text_parts)
                if full_text not in sst_map:
                    sst_map[full_text] = i

            def get_or_add_sst(text: str) -> int:
                nonlocal total_count
                if text in sst_map:
                    return sst_map[text]
                si = ET.SubElement(sst_root, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si")
                t = ET.SubElement(si, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
                t.text = text
                if text.startswith(" ") or text.endswith(" ") or "\n" in text:
                    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_idx = total_count
                total_count += 1
                sst_map[text] = new_idx
                return new_idx

            def update_sheet_xml(sheet_raw: bytes, updates: dict) -> bytes:
                sheet_root = ET.fromstring(sheet_raw)
                sheet_data = sheet_root.find("main:sheetData", self.ns)
                if sheet_data is None:
                    return sheet_raw

                # 依 row 分組
                rows_map = {}
                for coord, val in updates.items():
                    col_str, row_idx = split_coord(coord)
                    if row_idx not in rows_map:
                        rows_map[row_idx] = {}
                    rows_map[row_idx][col_str] = val

                existing_rows = {}
                for r in sheet_data.findall("main:row", self.ns):
                    r_idx = int(r.attrib.get("r", 0))
                    existing_rows[r_idx] = r

                for row_idx, col_vals in rows_map.items():
                    if row_idx in existing_rows:
                        row_elem = existing_rows[row_idx]
                    else:
                        row_elem = ET.Element("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row", {"r": str(row_idx)})
                        inserted = False
                        for idx_elem, child in enumerate(sheet_data):
                            if child.tag.endswith("row"):
                                c_idx = int(child.attrib.get("r", 0))
                                if c_idx > row_idx:
                                    sheet_data.insert(idx_elem, row_elem)
                                    inserted = True
                                    break
                        if not inserted:
                            sheet_data.append(row_elem)
                        existing_rows[row_idx] = row_elem

                    existing_cells = {}
                    for c in row_elem.findall("main:c", self.ns):
                        c_r = c.attrib.get("r", "")
                        c_col, _ = split_coord(c_r)
                        existing_cells[c_col] = c

                    for col_str, val in col_vals.items():
                        coord = f"{col_str}{row_idx}"
                        if col_str in existing_cells:
                            c_elem = existing_cells[col_str]
                        else:
                            c_elem = ET.Element("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c", {"r": coord})
                            inserted = False
                            for idx_elem, child in enumerate(row_elem):
                                if child.tag.endswith("c"):
                                    other_col, _ = split_coord(child.attrib.get("r", "A1"))
                                    if col2num(other_col) > col2num(col_str):
                                        row_elem.insert(idx_elem, c_elem)
                                        inserted = True
                                        break
                            if not inserted:
                                row_elem.append(c_elem)
                            existing_cells[col_str] = c_elem

                        # 清空現有子節點 (保留 cell 原始樣式屬性 s="...")
                        for child in list(c_elem):
                            c_elem.remove(child)

                        if isinstance(val, (int, float)):
                            if "t" in c_elem.attrib:
                                del c_elem.attrib["t"]
                            v = ET.SubElement(c_elem, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                            v.text = str(val)
                        elif isinstance(val, str):
                            c_elem.attrib["t"] = "s"
                            sst_idx = get_or_add_sst(val)
                            v = ET.SubElement(c_elem, "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                            v.text = str(sst_idx)
                        elif val is None:
                            if "t" in c_elem.attrib:
                                del c_elem.attrib["t"]

                return ET.tostring(sheet_root, encoding="utf-8", xml_declaration=True)

            # 3. 準備需要更新的各 sheet 內容
            updated_sheets_data = {}
            for sheet_name, updates in sheet_updates_by_name.items():
                if sheet_name in sheet_target_map:
                    target_file = sheet_target_map[sheet_name]
                    if target_file in all_files:
                        raw_data = zin.read(target_file)
                        updated_sheets_data[target_file] = update_sheet_xml(raw_data, updates)

            # 更新 sst 計數
            sst_root.attrib["count"] = str(total_count)
            sst_root.attrib["uniqueCount"] = str(total_count)
            new_sst_raw = ET.tostring(sst_root, encoding="utf-8", xml_declaration=True)

            # 4. 寫入全新的輸出 ZIP 檔
            out_dir = os.path.dirname(os.path.abspath(output_path))
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)

            with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for item in all_files:
                    if item in updated_sheets_data:
                        zout.writestr(item, updated_sheets_data[item])
                    elif item == "xl/sharedStrings.xml":
                        zout.writestr(item, new_sst_raw)
                    else:
                        # 所有圖片、繪圖、VML、主題與關係檔完全原裝複製，一個位元都不更動
                        zout.writestr(item, zin.read(item))

        return output_path


def fill_excel_template(
    npc: Dict,
    template_path: str,
    output_path: str
) -> str:
    """
    將 npc 字典中的資料以無損 OpenXML 引擎精確回填至 template_path，並另存為 output_path
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"找不到 Excel 模板檔案：{template_path}")

    rec = npc.get("recommended_allocation", {})
    app = npc.get("appearance", {})
    trait = npc.get("unique_trait")
    bg = npc.get("backstory", {})
    equipment_list = npc.get("equipment", [])

    # ==========================================
    # 1. 整理【角色卡】(Master Character Sheet) 回填欄位
    # ==========================================
    sheet_char_updates = {
        # 身分與外貌 (Row 7, 9)
        "C7": npc.get("name", "未命名角色"),
        "O7": "DM (劇情非玩家角色)",
        "W7": npc.get("race", "人類"),
        "AN7": npc.get("race", "人類"),
        "AX7": npc.get("alignment", "中立"),
        "BG7": npc.get("deity", "無特定信仰"),

        "C9": app.get("size", "中型"),
        "H9": app.get("hair", "灰黑"),
        "N9": app.get("skin", "風霜古銅色"),
        "T9": app.get("eyes", "深邃"),
        "AA9": app.get("height", "175 公分"),
        "AI9": app.get("weight", "150 磅"),
        "AN9": str(npc.get("age", {}).get("display", "30 歲")),
        "AX9": npc.get("background", "平民"),

        # 職業與等級
        "Z16": map_class_to_template_format(npc.get("class", "戰士")),
        "AJ16": int(npc.get("level", 1)),

        # 6 大核心屬性點數實擲 (F15:F20)
        "F15": int(rec.get("STR", {}).get("recommended_base", 10)),
        "F16": int(rec.get("DEX", {}).get("recommended_base", 10)),
        "F17": int(rec.get("CON", {}).get("recommended_base", 10)),
        "F18": int(rec.get("INT", {}).get("recommended_base", 10)),
        "F19": int(rec.get("WIS", {}).get("recommended_base", 10)),
        "F20": int(rec.get("CHA", {}).get("recommended_base", 10)),

        # 生命值
        "V27": int(npc.get("hp", 10)),
    }

    # 尋找護甲與盾牌
    armor_found = False
    for eq in equipment_list:
        eq_type = eq.get("type", "")
        if "甲" in eq_type or "護甲" in eq.get("name", ""):
            sheet_char_updates["BH27"] = eq.get("name", "")
            ac_match = re.search(r"\d+", eq.get("ac", "10"))
            if ac_match:
                sheet_char_updates["AN27"] = int(ac_match.group(0))
            armor_found = True
        elif "盾" in eq.get("name", ""):
            sheet_char_updates["AT27"] = 2

    if not armor_found:
        sheet_char_updates["BH27"] = "隨身日常衣物"
        sheet_char_updates["AN27"] = 10

    # 回填非典型武器庫 (Slot 1 ~ Slot 4 -> Row 37 ~ Row 40)
    weapon_idx = 0
    str_val = int(rec.get("STR", {}).get("recommended_base", 10))
    dex_val = int(rec.get("DEX", {}).get("recommended_base", 10))
    str_mod = (str_val - 10) // 2
    dex_mod = (dex_val - 10) // 2
    pb = int(npc.get("proficiency_bonus", "+2").replace("+", ""))

    for eq in equipment_list:
        if any(k in eq.get("type", "") for k in ["武器", "農具", "工具", "法器", "道具"]):
            target_row = 37 + weapon_idx
            if target_row <= 41:
                sheet_char_updates[f"V{target_row}"] = eq.get("name", "")
                dmg = eq.get("damage", "—")
                if dmg != "—":
                    sheet_char_updates[f"AL{target_row}"] = dmg

                hit_bonus = pb + (dex_mod if "靈巧" in eq.get("properties", "") or "遠程" in eq.get("type", "") else str_mod)
                sheet_char_updates[f"AI{target_row}"] = f"+{hit_bonus}" if hit_bonus >= 0 else str(hit_bonus)
                sheet_char_updates[f"AS{target_row}"] = f"+{str_mod}" if str_mod >= 0 else str(str_mod)
                sheet_char_updates[f"AV{target_row}"] = eq.get("properties", "")
                weapon_idx += 1

    # 回填種族、背景、非典型特質與劇本線索 (V56+)
    sheet_char_updates["V56"] = "【種族、背景與非典型特長】"
    sheet_char_updates["V57"] = f"背景特性：{npc.get('bg_feature', '市井生活歷練')}"
    sheet_char_updates["V58"] = f"已知語言：{', '.join(npc.get('racial_languages', ['通用語']))}"
    if trait:
        sheet_char_updates["V59"] = f"🌟【{trait['name']}】({trait['category']})：{trait['game_effect']}"
    else:
        sheet_char_updates["V59"] = "🌿 常規凡人：完全遵循標準冒險者/市井規則，無超常異變。"
    sheet_char_updates["V60"] = f"🎯 劇本線索：{bg.get('story_hook', '')}"

    # 職業已解鎖特長 (AT56+)
    features = npc.get("unlocked_features", [])
    for i, feat in enumerate(features[:12]):
        sheet_char_updates[f"AT{56 + i}"] = feat

    # ==========================================
    # 2. 整理【魔寵數據】(專用 NPC 數據卡) 回填欄位
    # ==========================================
    sheet_npc_updates = {
        "B3": npc.get("name", "未命名 NPC"),
        "O3": map_size_to_npc_format(app.get("size", "中型")),
        "B5": str(npc.get("age", {}).get("display", "中年")),
        "G5": npc.get("gender", "未知"),
        "L5": f"人型生物 ({npc.get('race', '人類')})",
        "X5": npc.get("alignment", "中立"),

        # 生命值與護甲
        "H9": int(npc.get("hp", 10)),
        "H11": 16 if "重甲" in str(equipment_list) else 13,

        # 6 大屬性實數 (B36:Q36)
        "B36": str_val,
        "E36": dex_val,
        "H36": int(rec.get("CON", {}).get("recommended_base", 10)),
        "K36": int(rec.get("INT", {}).get("recommended_base", 10)),
        "N36": int(rec.get("WIS", {}).get("recommended_base", 10)),
        "Q36": int(rec.get("CHA", {}).get("recommended_base", 10)),

        # 速度與 CR
        "B42": clean_cr_string(npc.get("cr", "1/4")),
        "AH4": "隨身物品 / 非典型故事武器"
    }

    speed_match = re.search(r"\d+", npc.get("speed", "30"))
    sheet_npc_updates["B39"] = int(speed_match.group(0)) if speed_match else 30

    if "60" in npc.get("darkvision", ""):
        sheet_npc_updates["P41"] = 60
    elif "120" in npc.get("darkvision", ""):
        sheet_npc_updates["P41"] = 120
    else:
        sheet_npc_updates["P41"] = 0

    # 隨身武器與物品清單 (AH5 起)
    for i, eq in enumerate(equipment_list[:12]):
        dmg = f" ({eq.get('damage')})" if eq.get("damage") and eq.get("damage") != "—" else ""
        sheet_npc_updates[f"AH{5 + i}"] = f"{eq['name']}{dmg} - {eq.get('properties', '')}"

    # 語言清單 (AH33 起)
    langs = npc.get("racial_languages", ["通用語"])
    for i, lang in enumerate(langs[:4]):
        sheet_npc_updates[f"AH{33 + i}"] = lang

    # 執行無失真 OpenXML 直接注入
    populator = LosslessOpenXmlPopulator(template_path)
    return populator.populate(
        {
            "角色卡": sheet_char_updates,
            "魔寵數據": sheet_npc_updates
        },
        output_path
    )
