"""
D&D 5E NPC 核心生成引擎 (Core NPC Generator) - 劇情導向與非典型客製化版
特色：
1. 敘事優先 (Narrative-First)：打破死板規則書限制，支援自訂故事形象（如：戰士數值但拿草耙的農夫、叼著老煙斗施法的大法師）。
2. 4d6dl1 屬性池與彈性配置：提供建議配置，不強制鎖定；獨立標註種族可選加值。
3. 自由等級與情境解析 (大魔導師 Lv 12-16、能力遭封印、老兵、平民等)。
4. 職業特長、熟練加值 (PB +2~+6)、施法環位與受限狀態標記。
5. 動態趣味武器與非法杖法器庫 (草耙、乾草叉、老手杖、符文煙斗、黃銅算盤等)。
6. 陣營、外貌細節與預估挑戰等級 (CR) 生成。
7. 獨特非傳統特質（預設為「無」，僅在指定關鍵字或需求時啟用）。
"""

import random
import re
from typing import Dict, List, Optional, Tuple
from .database import (
    ATTRIBUTES, RACES, CLASSES, BACKGROUNDS, DEITIES,
    STANDARD_LANGUAGES, EXOTIC_LANGUAGES, UNIQUE_TRAITS_PRESETS,
    SPELL_SLOTS_TABLE, ALIGNMENTS, THEMATIC_CUSTOM_WEAPONS, THEMATIC_ARCANE_FOCUSES
)
from .roller import (
    generate_ability_rolls, build_recommended_allocation,
    calculate_modifier, format_modifier
)


class NPCGenerator:
    """
    D&D 5E 劇本向 NPC 產生器
    """

    def __init__(self):
        self.races = RACES
        self.classes = CLASSES
        self.backgrounds = BACKGROUNDS
        self.deities = DEITIES
        self.unique_traits = UNIQUE_TRAITS_PRESETS
        self.spell_slots = SPELL_SLOTS_TABLE
        self.alignments = ALIGNMENTS
        self.thematic_weapons = THEMATIC_CUSTOM_WEAPONS
        self.thematic_focuses = THEMATIC_ARCANE_FOCUSES

    def generate(
        self,
        name: Optional[str] = None,
        race_name: Optional[str] = None,
        class_name: Optional[str] = None,
        background_name: Optional[str] = None,
        level_input: Optional[str] = None,
        alignment_input: Optional[str] = None,
        gender_input: Optional[str] = None,
        importance: str = "次要劇情 NPC (Supporting)",
        story_context: Optional[str] = None,
        custom_trait_keyword: Optional[str] = None,
    ) -> Dict:
        """
        生成完整的 NPC 角色資訊
        """
        # 1. 解析等級與客製化狀態 (支援關鍵字如「大魔導師」、「被封印的大魔導師」、「老兵」等)
        level, level_note = self._parse_level_and_state(level_input)

        # 2. 決定職業與機械定位
        if not class_name or class_name not in self.classes:
            if "魔導" in (level_input or "") or "法師" in (level_input or ""):
                class_name = "法師 (Wizard)"
            elif any(k in (story_context or "") for k in ["戰士", "打手", "守衛", "草耙", "民兵"]):
                class_name = "戰士 (Fighter)"
            else:
                class_name = random.choice(list(self.classes.keys()))
        class_data = self.classes[class_name]

        # 3. 決定種族
        if not race_name or race_name not in self.races:
            race_name = random.choice(list(self.races.keys()))
        race_data = self.races[race_name]

        # 4. 決定背景
        if not background_name or background_name not in self.backgrounds:
            background_name = random.choice(list(self.backgrounds.keys()))
        bg_data = self.backgrounds[background_name]

        # 5. 陣營與性別
        alignment = alignment_input or random.choice(self.alignments)[0]
        gender = gender_input or random.choice(["男性 (Male)", "女性 (Female)"])

        # 6. 生理外貌與視覺特徵 (身高、體重、膚色、瞳色、體態特徵)
        appearance = self._generate_appearance(race_name, gender, story_context)

        # 7. 熟練加值 (PB) 與挑戰等級 (CR) 估算
        pb = 2 + (level - 1) // 4
        pb_str = f"+{pb}"
        cr_display = self._estimate_cr(level, class_name, level_note)

        # 8. 4d6dl1 屬性擲骰池與建議配置
        rolls = generate_ability_rolls()
        raw_scores = [r["score"] for r in rolls]
        recommended_allocation = build_recommended_allocation(raw_scores, class_name)
        
        stat_preview = {}
        for stat, val in recommended_allocation.items():
            mod = calculate_modifier(val)
            stat_preview[stat] = {
                "recommended_base": val,
                "base_mod_str": format_modifier(mod)
            }

        # 9. 生命值計算
        suggested_con_mod = calculate_modifier(recommended_allocation["CON"])
        hit_die_val = int(class_data["hit_die"].replace("d", ""))
        avg_per_level = (hit_die_val // 2) + 1
        est_hp = max(1, hit_die_val + suggested_con_mod + (level - 1) * max(1, (avg_per_level + suggested_con_mod)))

        # 10. 年齡與壽命
        min_age, max_age = race_data["lifespan"]
        age = self._generate_age(min_age, max_age)

        # 11. 信仰
        deity_name, deity_desc = random.choice(self.deities)

        # 12. 語言能力
        languages = list(race_data["languages"])

        # 13. 等級解鎖職業特長清單
        unlocked_features = self._get_unlocked_features(class_data, level)

        # 14. 施法者法術位與封印狀態
        spellcasting_info = self._get_spellcasting_info(class_data, level, level_note)

        # 15. 動態趣味裝備與非典型道具 (融入故事線索，如草耙、老煙斗等)
        equipment = self._resolve_thematic_equipment(class_data, story_context, custom_trait_keyword)

        # 16. 獨特非傳統特質 (預設為「無」，僅在提供關鍵字或明確需求時生成)
        unique_trait = self._resolve_unique_trait(custom_trait_keyword, story_context)

        # 17. 背景短史與劇本線索整合
        backstory = self._generate_backstory(
            race_name=race_name,
            class_name=class_name,
            background_name=background_name,
            bg_data=bg_data,
            level=level,
            level_note=level_note,
            story_context=story_context,
            unique_trait=unique_trait,
            appearance=appearance,
            equipment=equipment
        )

        # 18. NPC 姓名
        if not name:
            name = self._generate_npc_name(race_name, gender)

        return {
            "name": name,
            "gender": gender,
            "alignment": alignment,
            "importance": importance,
            "level": level,
            "level_display": f"Lv.{level}" + (f" ({level_note})" if level_note else ""),
            "level_note": level_note,
            "cr": cr_display,
            "proficiency_bonus": pb_str,
            "race": race_name,
            "racial_bonus_options": race_data["bonus_options"],
            "class": class_name,
            "background": background_name,
            "age": age,
            "appearance": appearance,
            "deity": f"{deity_name} - {deity_desc}",
            "speed": f"{race_data['speed']} 呎",
            "darkvision": f"{race_data['darkvision']} 呎" if race_data["darkvision"] > 0 else "無 (常規視力)",
            "hp": est_hp,
            "hit_dice": f"{level}{class_data['hit_die']}",
            
            # 屬性靈活模組
            "raw_dice_rolls": rolls,
            "raw_scores": raw_scores,
            "recommended_allocation": stat_preview,
            "primary_recommendation": class_data["primary_recommendation"],
            
            # 職業與戰鬥細節
            "class_saves": class_data["saves"],
            "unlocked_features": unlocked_features,
            "spellcasting_info": spellcasting_info,
            "equipment": equipment,
            
            # 背景自選項目
            "bg_skills": bg_data["skills_options"],
            "bg_tools": bg_data["tool_options"],
            "bg_languages": bg_data["language_options"],
            "bg_feature": bg_data["feature"],
            "racial_languages": languages,
            "racial_traits": race_data["traits"],
            
            # 獨特特質 (無或有)
            "unique_trait": unique_trait,
            
            # 劇情與背景
            "backstory": backstory
        }

    def _parse_level_and_state(self, level_input: Optional[str]) -> Tuple[int, Optional[str]]:
        if not level_input or not str(level_input).strip():
            return 1, None

        raw = str(level_input).strip()
        digits = re.findall(r"\d+", raw)
        extracted_num = int(digits[0]) if digits else None

        level = 1
        note = None

        if any(k in raw for k in ["大魔導", "大法師", "archmage", "grand mage"]):
            level = extracted_num if (extracted_num and 1 <= extracted_num <= 20) else random.randint(13, 16)
            note = "大魔導師階級"
        elif any(k in raw for k in ["老兵", "騎士長", "veteran"]):
            level = extracted_num if (extracted_num and 1 <= extracted_num <= 20) else random.randint(5, 8)
            note = "資深歷練者"
        elif any(k in raw for k in ["菁英", "隊長", "elite"]):
            level = extracted_num if (extracted_num and 1 <= extracted_num <= 20) else random.randint(3, 5)
            note = "隊伍精銳"
        elif any(k in raw for k in ["平民", "農夫", "學徒", "commoner"]):
            level = 1
            note = "市井平民/學徒"
        elif extracted_num and 1 <= extracted_num <= 20:
            level = extracted_num

        if any(k in raw for k in ["封印", "詛咒", "殘缺", "虛弱", "sealed", "cursed", "weakened"]):
            seal_info = "【能力封印/受限中】：此角色過往實力強大，但因受古老詛咒、法術封印或暗傷壓制，目前無法發揮全盛實力（如高環位法術位暫時鎖定、每日施法次數受限或特定能力受阻）。"
            note = (note + "；" + seal_info) if note else seal_info

        return level, note

    def _estimate_cr(self, level: int, class_name: str, level_note: Optional[str]) -> str:
        """
        根據等級與狀態預估 NPC 挑戰等級 (CR)
        """
        if level <= 1:
            return "CR 1/4 (或 CR 1/2)"
        elif level <= 2:
            return "CR 1"
        elif level <= 4:
            return "CR 2"
        elif level <= 6:
            return "CR 3 ~ 4"
        elif level <= 9:
            return "CR 5 ~ 6"
        elif level <= 12:
            return "CR 7 ~ 8"
        elif level <= 15:
            return "CR 9 ~ 11 (受封印時實際約 CR 5)" if (level_note and "封印" in level_note) else "CR 9 ~ 11"
        else:
            return "CR 12 ~ 15"

    def _generate_appearance(self, race_name: str, gender: str, story_context: Optional[str]) -> Dict:
        """
        生成生動具體的外觀細節
        """
        is_small = any(k in race_name for k in ["半身人", "侏儒"])
        is_large = any(k in race_name for k in ["半獸人", "龍裔"])

        if is_small:
            height = f"{random.randint(90, 115)} 公分 (約 3 呎)"
            weight = f"{random.randint(35, 48)} 磅"
            size = "小型 (Small)"
        elif is_large:
            height = f"{random.randint(185, 215)} 公分 (約 6.5 呎)"
            weight = f"{random.randint(210, 270)} 磅"
            size = "中型 (偏魁梧壯碩)"
        else:
            height = f"{random.randint(165, 185)} 公分 (約 5.8 呎)"
            weight = f"{random.randint(130, 180)} 磅"
            size = "中型 (Medium)"

        hair_colors = ["深黑", "灰白微霜", "棕褐", "銀白", "枯黃", "赤紅"]
        eye_colors = ["深棕", "碧綠", "琥珀金", "灰藍", "幽黑", "淡紫"]
        skin_tones = ["日曬古銅色", "風霜蒼白", "黝黑結實", "粗糙粗獷", "白皙"]

        # 依據身分融入體態視覺描寫
        looks = [
            "雙手覆滿經年累月的厚重老繭，指節粗大，舉止沉穩有力。",
            "眼神如鷹隼般銳利警惕，嘴角常年帶著似有若無的平靜苦笑。",
            "身形雖略顯駝背風霜，但行走間腳步極為輕盈穩健，呼吸綿長。",
            "臉頰至下顎有一道早已癒合的陳年暗痕，神情肅穆寡言。"
        ]

        if story_context and ("煙斗" in story_context or "菸斗" in story_context):
            looks.append("嘴角常年叼著一只磨損的雕花木煙斗，周身繚繞著淡淡草藥苦香。")
        if story_context and ("農夫" in story_context or "田" in story_context):
            looks.append("身著粗麻布短褐布衣，鞋履沾著黑石泥土，但臂膀筋肉線條分明。")

        return {
            "size": size,
            "height": height,
            "weight": weight,
            "hair": random.choice(hair_colors),
            "eyes": random.choice(eye_colors),
            "skin": random.choice(skin_tones),
            "feature_look": random.choice(looks)
        }

    def _resolve_thematic_equipment(
        self,
        class_data: Dict,
        story_context: Optional[str],
        custom_trait_keyword: Optional[str]
    ) -> List[Dict]:
        """
        打破常規裝備死板配置：若劇情或概念提及特殊工具（如草耙、手杖、煙斗等），動態置換並配給精確傷害骰
        """
        combined_text = f"{story_context or ''} {custom_trait_keyword or ''}".lower()
        equipment = list(class_data.get("default_equipment", []))

        # 1. 檢測是否有特殊非典型武器 (如草耙、草叉、手杖、鎬、剁刀、魚叉等)
        matched_weapon = None
        for key, w_data in self.thematic_weapons.items():
            if key in combined_text:
                matched_weapon = w_data
                break

        if matched_weapon:
            # 將第一把常規軍用武器替換為該故事專屬武器
            equipment[0] = matched_weapon

        # 2. 檢測是否有非典型施法法器 (如煙斗、算盤、茶杯、懷錶等)
        for focus in self.thematic_focuses:
            if any(k in combined_text for k in focus["keywords"]):
                equipment.append({
                    "name": focus["name"],
                    "type": "特殊故事法器 / 奇物",
                    "damage": "—",
                    "properties": focus["description"]
                })
                break

        return equipment

    def _get_unlocked_features(self, class_data: Dict, level: int) -> List[str]:
        features_dict = class_data.get("features_by_level", {})
        unlocked = []
        for lv in sorted(features_dict.keys()):
            if lv <= level:
                for feat in features_dict[lv]:
                    unlocked.append(f"[Lv.{lv}] {feat}")
        return unlocked

    def _get_spellcasting_info(self, class_data: Dict, level: int, level_note: Optional[str]) -> Optional[Dict]:
        if not class_data.get("is_spellcaster"):
            return None

        standard_slots = self.spell_slots.get(level, {})
        slots_display = [f"{k}：{v} 個" for k, v in standard_slots.items()]

        status_remark = "正常充沛"
        if level_note and any(k in level_note for k in ["封印", "詛咒", "受限"]):
            status_remark = "⚠️ 封印警示：部分高環法術環位已遭封印，建議 DM 僅開放 3 環以下法術位，或限定其施法須通過專注豁免。"

        return {
            "spell_type": class_data.get("spell_type", "施法者"),
            "slots_by_circle": ", ".join(slots_display),
            "status_remark": status_remark
        }

    def _resolve_unique_trait(
        self,
        keyword: Optional[str] = None,
        story_context: Optional[str] = None
    ) -> Optional[Dict]:
        """
        決定是否生成獨特非傳統特質：預設為 None（普通凡人/商人/農夫），僅在有明確意向時啟用
        """
        combined = f"{keyword or ''} {story_context or ''}".strip().lower()
        if not combined:
            return None

        if any(k in combined for k in ["無", "沒有", "none", "nothing", "普通", "常規"]):
            return None

        # 比對預設特質庫
        for preset in self.unique_traits:
            if any(k in combined for k in preset["keywords"]):
                return {
                    "name": preset["name"],
                    "category": preset["category"],
                    "description": preset["description"],
                    "game_effect": preset["game_effect"]
                }

        # 若使用者有明確傳入自訂 keyword，動態生成該關鍵字的規則加成
        if keyword and keyword.strip() not in ["無", "none"]:
            return {
                "name": f"{keyword}之印 (Mark of {keyword})",
                "category": "自訂獨特異能",
                "description": f"此角色在「{keyword}」領域具有不同尋常的超常適應力與特質。",
                "game_effect": f"在進行與「{keyword}」相關之行動判定或豁免時具備優勢，並可在特定情境下自帶額外環境增益或 1d4 特殊效果。"
            }

        return None

    def _generate_backstory(
        self,
        race_name: str,
        class_name: str,
        background_name: str,
        bg_data: Dict,
        level: int,
        level_note: Optional[str],
        story_context: Optional[str],
        unique_trait: Optional[Dict],
        appearance: Dict,
        equipment: List[Dict]
    ) -> Dict:
        personality_traits = [
            "說話簡短直率，討厭拐彎抹角，眼神常警惕地掃視四周環境。",
            "習慣用平靜微笑掩蓋敏銳的觀察，總是坐在酒館最靠近出口的角落。",
            "極度重視諾言與契約，凡是受人恩惠必設法以雙倍回報。",
            "對古老傳聞或未知生物抱有強烈好奇心，容易被奇特金屬或古書吸引。",
            "行事沉穩老練，但在關鍵時刻能果斷做出常人不敢想像的決策。"
        ]

        ideals = [
            "【責任】：既然生活在這片土地上，就有義務守護那些無力反抗的無辜者。（善良）",
            "【生存】：混亂世道中，唯有強大的實力與冷靜才能活到明天。（中立）",
            "【秩序】：混亂只會帶來流血與災難，必須有人維持最起碼的規矩。（守序）",
            "【自由】：沒有人能用枷鎖或誓言束縛我的意志。（混亂）"
        ]

        bonds = [
            "身上隨身攜帶一枚帶有裂痕的古老勳章或印信，是尋找故人的唯一線索。",
            "暗中每月都將部分酬勞資助給偏遠聚落的孤兒院或老醫者。",
            "曾有一位親密夥伴替自己擋下致命一擊，立誓替其完成未竟之願。"
        ]

        flaws = [
            "一旦涉及過去的痛處便極易動怒，有時會低估對手的陰險。",
            "對資源與情報有著過度的焦慮感，習慣隨身藏匿應急小錦囊。",
            "難以全然相信陌生人，即便達成合作也總是私下留有後手。"
        ]

        # 劇本融入勾子
        if story_context and story_context.strip():
            story_hook = (
                f"【劇本關聯線索】：此角色與目前劇情事件（{story_context.strip()}）有著直接交集。"
                f"他/她曾親身涉入或目擊相關動態，手中握有能指引玩家隊伍、推進調查或提供後勤支援的具體情資。"
            )
        else:
            story_hook = (
                f"【劇本關聯線索】：常駐於本地市井或冒險者集結之處，"
                f"表面上以 {background_name} 的身分生活，實際上對周遭局勢瞭若指掌，"
                f"可作為 DM 提供任務情報、引薦關鍵人物或觸發支線委託的重要樞紐。"
            )

        summary_parts = [
            f"身為一名 {race_name}，在故事中展現出 {class_name} 的本領（Lv.{level}），歷經 {background_name} 的歲月。"
        ]
        if level_note:
            summary_parts.append(f"人物背景殊異：{level_note}。")
        if unique_trait:
            summary_parts.append(f"身上展現著罕見特質【{unique_trait['name']}】。")
        else:
            summary_parts.append("身上並無超常神異異能，憑藉純粹的凡人歷練與手中熟稔工具立足。")

        return {
            "summary": "".join(summary_parts),
            "personality": random.choice(personality_traits),
            "ideal": random.choice(ideals),
            "bond": random.choice(bonds),
            "flaw": random.choice(flaws),
            "story_hook": story_hook
        }

    def _generate_age(self, min_age: int, max_age: int) -> Dict:
        actual_age = random.randint(min_age, int(max_age * 0.75))
        ratio = actual_age / max_age
        if ratio < 0.2:
            stage = "青年 (Young Adult)"
        elif ratio < 0.45:
            stage = "壯年 (Prime Adult)"
        elif ratio < 0.7:
            stage = "中年 (Middle-aged)"
        else:
            stage = "長者 / 晚年 (Venerable)"

        return {
            "age_number": actual_age,
            "stage": stage,
            "display": f"{actual_age} 歲 ({stage})"
        }

    def _generate_npc_name(self, race_name: str, gender: str) -> str:
        is_female = "女" in gender

        if is_female:
            human_names = ["艾蓮娜 (Elena)", "西爾維亞 (Sylvia)", "瑪格麗特 (Margaret)", "克拉拉 (Clara)", "薇薇安 (Vivian)"]
            elf_names = ["希爾薇雅 (Silvya)", "瑟蘭妮 (Therani)", "莉蘭蒂 (Liranthi)", "愛拉 (Aela)"]
            dwarf_names = ["黑爾加 (Helga)", "達格瑪 (Dagmar)", "布倫希爾德 (Brunhilde)"]
            halfling_names = ["蘿西 (Rosie)", "貝拉 (Bella)", "波比 (Poppy)", "瑪格波 (Marigold)"]
        else:
            human_names = ["羅蘭 (Roland)", "維克托 (Viktor)", "馬庫斯 (Marcus)", "加文 (Gavin)", "老丹恩 (Old Dan)"]
            elf_names = ["埃拉利昂 (Elalion)", "法拉米爾 (Faeramir)", "艾蘭迪爾 (Aelandir)"]
            dwarf_names = ["布魯諾 (Bruenor)", "托爾丁 (Thoradin)", "巴林 (Balin)", "達格恩 (Dargun)"]
            halfling_names = ["米羅 (Milo)", "芬恩 (Finn)", "派瑞格林 (Peregrin)", "阿爾菲 (Alfie)"]

        if "精靈" in race_name:
            return random.choice(elf_names)
        elif "矮人" in race_name:
            return random.choice(dwarf_names)
        elif "半身人" in race_name or "侏儒" in race_name:
            return random.choice(halfling_names)
        elif "獸人" in race_name:
            return "格羅克 (Grok)" if not is_female else "烏爾卡 (Urka)"
        elif "龍裔" in race_name:
            return "巴拉薩 (Balasar)" if not is_female else "朵拉希 (Doraxi)"
        else:
            return random.choice(human_names)
