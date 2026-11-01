"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 - AI 核心生成器 (AI Narrative Engine)
整合 Google Gemini 旗艦大語言模型與 D&D 5E 規則體系，
真正實現由 AI 深度設計背景身世、非典型生活裝備映射、言行小動作、子職業範型流派與跑團伏筆線索。
"""

import os
import sys
import re
import json
from typing import Dict, Optional, Tuple

# 導入規則與擲骰模組
from .roller import generate_ability_rolls, build_recommended_allocation
from .database import (
    RACES, CLASSES, SUBCLASSES, BACKGROUNDS, ALIGNMENTS, DEITIES,
    UNIQUE_TRAITS_PRESETS, THEMATIC_CUSTOM_WEAPONS, THEMATIC_ARCANE_FOCUSES
)

# 嘗試載入 dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    # 同步尋找專案根目錄的 .env
    for env_path in [
        ".env",
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.expanduser(r"~\OneDrive\Documents\0921test\.env"),
        os.path.expanduser(r"~\OneDrive\Documents\dnd-5e-npc-generator\.env")
    ]:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            break
except Exception:
    pass

# 嘗試載入 google-genai SDK
HAS_GENAI = False
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    pass


DEFAULT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-flash-latest"
]


class AINPCGenerator:
    """
    真正的 AI 智慧 NPC 角色生成器
    1. 實擲 4d6dl1 屬性點數池，並計算主副屬性建議配置與種族加值候選清單 (不硬編碼)
    2. 隨機或指定基礎種族、職業、子職業範型流派、背景、年齡、信仰與語言
    3. 呼叫 Gemini AI 模型深度撰寫：
       - 融入 DM 劇情的情境背景短史 (Backstory)
       - 富有生活感與反差魅力的言行舉止、口吻與細節小動作 (Personality & Quirks)
       - 符合 5E 傷害骰與規則規格的非典型武器/法器/特殊能力 (Unorthodox Equipment)
       - 深度結合子職業範型（如戰鬥大師、死靈學派、生命領域、復仇之誓）的戰鬥習慣與哲學
       - 專為 DM 設計的跑團推進伏筆與任務線索 (Quest Hook)
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.5-flash-lite"):
        import logging
        logging.getLogger("google.genai").setLevel(logging.ERROR)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self._client = None
        if HAS_GENAI and self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[警告] 初始化 Gemini Client 失敗: {e}", file=sys.stderr)

    def set_api_key(self, api_key: str):
        """動態更新 API Key"""
        self.api_key = api_key.strip()
        if HAS_GENAI and self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self._client = None
                raise e

    def _resolve_choice(self, user_choice: Optional[str], db_dict: Dict) -> Tuple[str, Dict]:
        import random
        if not user_choice or "隨機" in user_choice or user_choice == "RANDOM":
            k = random.choice(list(db_dict.keys()))
            return k, db_dict[k]
        for k, v in db_dict.items():
            if k in user_choice or user_choice in k:
                return k, v
        # 找不到直接回傳首個
        return user_choice, list(db_dict.values())[0]

    def _parse_level_and_state(self, level_input: Optional[str]) -> Tuple[int, Optional[str]]:
        """解析使用者輸入的等級，支援自然語言關鍵字如『大魔導師』、『老兵』等"""
        if not level_input:
            return 1, None
        txt = str(level_input).strip()
        
        # 特殊情境關鍵字判定
        note = None
        level = 1
        if any(w in txt for w in ["大魔導師", "大魔導", "傳奇法師", "大法師", "archmage"]):
            level = 14
            note = "大魔導師階級 (Lv.14)"
        elif any(w in txt for w in ["精銳老兵", "老兵", "退役禁衛", "veteran"]):
            level = 5
            note = "精銳老兵階級 (Lv.5)"
        elif any(w in txt for w in ["學徒", "初學者", "apprentice", "novice"]):
            level = 2
            note = "見習學徒 (Lv.2)"
        elif any(w in txt for w in ["傳奇", "半神", "英雄", "legend"]):
            level = 17
            note = "傳奇英雄階級 (Lv.17)"
        else:
            match = re.search(r"\d+", txt)
            if match:
                val = int(match.group(0))
                level = max(1, min(20, val))
            else:
                level = 1

        if any(w in txt for w in ["封印", "衰老", "重傷", "詛咒", "受限", "力量盡失"]):
            tag = "部分法術環位已遭封印/實力受限"
            note = f"{note}；{tag}" if note else tag

        return level, note

    def _estimate_cr(self, level: int, class_name: str, level_note: Optional[str]) -> str:
        """估算挑戰等級 CR"""
        if level_note and "封印" in level_note:
            return f"CR {max(1, level // 3)} (受限評級)"
        if level <= 1:
            return "CR 1/4"
        elif level == 2:
            return "CR 1/2"
        elif level == 3:
            return "CR 1"
        elif level == 4:
            return "CR 2"
        else:
            cr_val = max(1, int(level * 0.65))
            return f"CR {cr_val}"

    def _generate_npc_name(self, race: str, gender: str) -> str:
        import random
        first_names_human = ["丹恩", "艾德加", "奧爾森", "貝拉", "達格瑪", "芬恩", "莉莉安", "維克多", "賽蓮娜", "諾亞"]
        first_names_elf = ["瑟蘭迪爾", "凱蘭崔爾", "法蘭德", "艾洛伊", "阿爾溫", "伊利安", "辛達", "席薇雅"]
        first_names_dwarf = ["托林", "巴林", "葛羅姆", "布洛克", "黛拉", "希爾達", "莫格林", "杜瓦林"]
        first_names_tiefling = ["摩斯", "阿扎澤爾", "卡莉達", "瓦沙克", "妮克絲", "墨菲斯托", "雷文"]

        if "精靈" in race:
            fn = random.choice(first_names_elf)
        elif "矮人" in race:
            fn = random.choice(first_names_dwarf)
        elif "提夫林" in race:
            fn = random.choice(first_names_tiefling)
        else:
            fn = random.choice(first_names_human)

        epithets = ["老", "鐵腕", "沉默的", "赤發", "灰瞳", "破曉", "獨眼", "笑面"]
        if random.random() < 0.4:
            return f"{random.choice(epithets)}{fn}"
        return fn

    def _resolve_subclass(self, class_key: str, level: int, user_subclass: Optional[str] = None) -> Tuple[Optional[str], Optional[Dict], str, str]:
        """
        解析子職業 / 範型流派
        返回: (chosen_subclass, subclass_data, subclass_category, subclass_display)
        """
        import random
        sub_info = SUBCLASSES.get(class_key)
        if not sub_info:
            return None, None, "", ""
        
        category = sub_info.get("category", "範型流派")
        unlock_lv = sub_info.get("unlock_level", 3)
        options = sub_info.get("options", {})

        if level < unlock_lv:
            return None, None, category, f"尚未解鎖範型 (Lv.{unlock_lv} 解鎖)"

        # 等級達到解鎖標準
        if not user_subclass or "隨機" in user_subclass or user_subclass == "RANDOM":
            choice_key = random.choice(list(options.keys()))
            return choice_key, options[choice_key], category, f"{category}：{choice_key}"

        # 嘗試比對使用者指定
        for k, v in options.items():
            if k == user_subclass or k in user_subclass or user_subclass in k or k.split(" ")[0] in user_subclass:
                return k, v, category, f"{category}：{k}"

        # 若未精確匹配，則隨機選擇
        choice_key = random.choice(list(options.keys()))
        return choice_key, options[choice_key], category, f"{category}：{choice_key}"

    def _get_unlocked_features(self, class_data: Dict, level: int, subclass_data: Optional[Dict] = None, subclass_name: Optional[str] = None) -> list:
        features = []
        saves = class_data.get("saves") or class_data.get("saving_throws", [])
        if saves:
            features.append(f"豁免判定熟練：{', '.join(saves)}")
        prog = class_data.get("features_by_level") or class_data.get("progression", {})
        for lvl in range(1, level + 1):
            if lvl in prog:
                for feat in prog[lvl]:
                    features.append(f"[Lv.{lvl}] {feat}")
            # 檢查子職業特性
            if subclass_data and "features_by_level" in subclass_data:
                sub_prog = subclass_data["features_by_level"]
                if lvl in sub_prog:
                    tag = f" ({subclass_name.split(' ')[0]})" if subclass_name else ""
                    for sub_feat in sub_prog[lvl]:
                        features.append(f"[Lv.{lvl} 範型{tag}] {sub_feat}")
        return features

    def generate(
        self,
        name: Optional[str] = None,
        race_name: Optional[str] = None,
        class_name: Optional[str] = None,
        subclass_name: Optional[str] = None,
        background_name: Optional[str] = None,
        level_input: Optional[str] = "1",
        importance: str = "次要劇情 NPC (Supporting)",
        story_context: Optional[str] = None,
        custom_trait_keyword: Optional[str] = None,
        force_ai: bool = True
    ) -> Dict:
        """
        生成完整的非典型 NPC 物件 (包含子職業範型流派)
        """
        # 1. 基礎身分隨機與對齊
        race_key, race_data = self._resolve_choice(race_name, RACES)
        class_key, class_data = self._resolve_choice(class_name, CLASSES)
        bg_key, bg_data = self._resolve_choice(background_name, BACKGROUNDS)

        # 2. 解析等級與特殊狀態
        level, level_note = self._parse_level_and_state(level_input)

        # 3. 解析子職業 / 範型流派 (Subclass / Paradigm)
        chosen_subclass, subclass_data, subclass_category, subclass_display = self._resolve_subclass(
            class_key, level, subclass_name
        )

        # 4. 擲骰 4d6dl1
        rolls = generate_ability_rolls()
        raw_scores = [r["score"] for r in rolls]
        raw_rolls_desc = ", ".join([f"{r['score']} (骰值 {r['dice']} 扣除 {r['dropped']})" for r in rolls])
        alloc_map = build_recommended_allocation(raw_scores, class_key)
        recommended_alloc = {}
        for stat, val in alloc_map.items():
            mod = (val - 10) // 2
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            recommended_alloc[stat] = {
                "recommended_base": val,
                "base_mod_str": mod_str,
                "modifier": mod
            }

        # 5. 年齡、性別與名稱
        import random
        gender = random.choice(["男性 (Male)", "女性 (Female)"])
        if not name:
            name = self._generate_npc_name(race_key, gender)

        age_min, age_max = race_data.get("lifespan", (18, 80))
        age_val = random.randint(age_min, int(age_max * 0.75))
        align_item = random.choice(ALIGNMENTS)
        alignment = align_item[0] if isinstance(align_item, (list, tuple)) else str(align_item)

        deity_item = random.choice(DEITIES)
        if isinstance(deity_item, (list, tuple)):
            deity = f"{deity_item[0]}（{deity_item[1]}）"
        else:
            deity = str(deity_item)

        # 6. 生命值與熟練加值
        hd_str = class_data.get("hit_die", "d8")
        hd_match = re.search(r"\d+", str(hd_str))
        hd = int(hd_match.group(0)) if hd_match else 8
        con_mod = recommended_alloc.get("CON", {}).get("modifier", 0)
        hp = hd + con_mod + max(1, (hd // 2 + 1 + con_mod)) * (level - 1)
        pb = 2 + (level - 1) // 4

        # 7. 估算挑戰等級 CR
        cr = self._estimate_cr(level, class_key, level_note)

        # 8. 呼叫 AI 生成深度背景、個性小動作、非典型武器故事與子職業哲學融入
        ai_narrative = None
        if self._client and force_ai:
            try:
                ai_narrative = self._generate_ai_story(
                    name=name,
                    race=race_key,
                    class_name=class_key,
                    subclass_name=chosen_subclass,
                    subclass_category=subclass_category,
                    subclass_display=subclass_display,
                    subclass_data=subclass_data,
                    level=level,
                    level_note=level_note,
                    background=bg_key,
                    gender=gender,
                    age=age_val,
                    story_context=story_context,
                    custom_trait=custom_trait_keyword
                )
            except Exception as e:
                print(f"[AI 呼叫失敗，切換為後備規則生成]: {e}", file=sys.stderr)

        # 9. 若無 AI 或呼叫失敗，使用基礎規則生成做為後備
        if not ai_narrative:
            ai_narrative = self._fallback_narrative(
                name=name,
                race=race_key,
                class_name=class_key,
                subclass_display=subclass_display,
                level=level,
                background=bg_key,
                story_context=story_context,
                custom_trait=custom_trait_keyword
            )

        # 10. 組裝完整 NPC 字典
        darkv = race_data.get("darkvision", 0)
        darkv_str = f"{darkv} 呎" if isinstance(darkv, int) and darkv > 0 else ("無 (常規視力)" if darkv == 0 else str(darkv))
        speed_val = race_data.get("speed", 30)
        speed_str = f"{speed_val} 呎" if isinstance(speed_val, int) else str(speed_val)
        bg_skills = bg_data.get("skills_options", "市井生活熟練")
        if isinstance(bg_skills, list):
            bg_skills_str = "、".join(bg_skills)
        else:
            bg_skills_str = str(bg_skills)

        unlocked_feats = self._get_unlocked_features(class_data, level, subclass_data, chosen_subclass)

        npc = {
            "name": name,
            "race": race_key,
            "class": class_key,
            "class_name": class_key,
            "subclass": chosen_subclass,
            "subclass_category": subclass_category,
            "subclass_display": subclass_display,
            "subclass_desc": subclass_data.get("desc", "") if subclass_data else "",
            "background": bg_key,
            "level": level,
            "level_note": level_note,
            "importance": importance,
            "gender": gender,
            "age": {
                "value": age_val,
                "display": f"{age_val} 歲",
                "category": "壯年" if age_val < age_max * 0.5 else "中年/資深"
            },
            "alignment": alignment,
            "deity": deity,
            "racial_languages": race_data.get("languages", ["通用語"]),
            "darkvision": darkv_str,
            "speed": speed_str,
            "hp": hp,
            "proficiency_bonus": f"+{pb}",
            "raw_ability_rolls": raw_rolls_desc,
            "raw_scores": raw_scores,
            "recommended_allocation": recommended_alloc,
            "racial_bonus_options": race_data.get("bonus_options", "可自由配置加值"),
            "bg_feature": bg_data.get("feature", "市井歷練"),
            "bg_proficiencies": bg_skills_str,
            "unlocked_features": unlocked_feats,
            "cr": cr,
            # AI 設計的深度內容
            "ai_crafted": True if self._client and force_ai else False,
            "ai_backstory": ai_narrative.get("backstory", ""),
            "ai_personality_quirks": ai_narrative.get("personality_quirks", ""),
            "ai_unorthodox_equipment": ai_narrative.get("unorthodox_equipment", []),
            "ai_quest_hook": ai_narrative.get("quest_hook", ""),
            "unique_trait": ai_narrative.get("trait_obj"),
            "equipment": ai_narrative.get("unorthodox_equipment", []),
            "token_usage": ai_narrative.get("token_usage")
        }

        return npc

    def _generate_ai_story(
        self,
        name: str,
        race: str,
        class_name: str,
        subclass_name: Optional[str],
        subclass_category: str,
        subclass_display: str,
        subclass_data: Optional[Dict],
        level: int,
        level_note: Optional[str],
        background: str,
        gender: str,
        age: int,
        story_context: Optional[str],
        custom_trait: Optional[str]
    ) -> Dict:
        """
        向 Gemini 發送 Prompt，取得由 AI 深度撰寫的繁體中文背景、個性小動作、非典型武器與範型哲學融入
        """
        system_instruction = (
            "你是一位頂尖的《龍與地下城》(D&D 5E) 地下城主 (DM) 與奇幻敘事小說家。"
            "你的任務是根據提供的角色數值與玩家的劇情提示，創作兼具『生活市井反差感』、『深刻情感張力』與『嚴謹 5E 規則規格』的 NPC 資料。"
            "請嚴格以繁體中文 (zh-TW) 輸出，且必須返回合法的 JSON 格式。"
        )

        sub_desc = subclass_data.get("desc", "") if subclass_data else ""
        subclass_prompt_line = f"- 子職業/範型流派：{subclass_display}"
        if sub_desc:
            subclass_prompt_line += f"（範型背景：{sub_desc}）"

        prompt = f"""
請為以下 D&D 5E NPC 角色設計深度的故事背景、非典型生活裝備與範型風格：

【基本設定】
- 角色姓名：{name}
- 種族：{race}
- 職業：{class_name} (等級: Lv.{level}{f'，特殊狀態: {level_note}' if level_note else ''})
{subclass_prompt_line}
- 性別與年齡：{gender}，{age} 歲
- 背景歷練：{background}
- DM 提供的情境故事：{story_context or "無特定情境，請根據種族職業自由發揮市井生活身分"}
- 非傳統特質/武器關鍵字：{custom_trait or "無 (常規凡人，生活道具)"}

【設計規範】
1. **身分與戰力徹底解耦**：如果 DM 提到農夫、守墓人、商人、廚師或學者，請讓他表面上完全融入市井生活，但戰鬥底層是該職業的實力。
2. **範型流派深度融會**：角色具備【{subclass_display}】。請將該範型的專屬戰技風格、奧術傳統、神聖誓約、神聖領域、德魯伊結社或原初本道本能，深刻融入角色的日常言行、戰鬥本能、生活小動作與武器故事中！
3. **非典型武器/法器**：如果故事提及日常物品（如鋼齒草耙、剁刀、鐵鎬、刻印符文石楠木老煙斗、黃銅算盤），請將其規格化為 D&D 5E 的武器或專注法器（寫明名稱、傷害骰如 1d8/1d10、特性如多用/長柄/偽裝農具、背後的來歷故事）。
4. **常規凡人原則**：若關鍵字包含「無」或未要求超常神力，絕不強加超自然變異，展現純粹的凡人歷練與人情味；若關鍵字提及特殊特質（如火焰、靈魂、封印），則設計符合 5E 規則的獨特特性。
5. **DM 跑團伏筆**：給予地下城主可以直接在跑團當天使用的劇情引入線索 (Quest Hook)。

請嚴格輸出以下 JSON 結構：
{{
  "backstory": "200~350 字的生動故事身世，描述其過去的經歷、隱退或當前的生活，以及為何擁有這身本領，並體現其子職業範型淵源。",
  "personality_quirks": "條列 2~3 項極具畫面感的個性特徵與生活細節小動作（例如抽煙斗的小習慣、撫摸草耙鋼齒的下意識動作、說話語調或戰鬥起手式）。",
  "unorthodox_equipment": [
    {{
      "name": "武器或道具名稱 (含英文)",
      "type": "近戰武器 / 遠程武器 / 專注法器 / 護甲",
      "damage": "傷害骰 (例如 1d8 (雙手 1d10) 穿刺) 或 AC",
      "properties": "5E 武器特性 (如 多用、長柄、平時偽裝為農具)",
      "story_lore": "一句話說明這件道具的故事來歷"
    }}
  ],
  "trait_name": "非典型特長名稱 (若為常規凡人請填『常規市井人物』)",
  "trait_effect": "特長效果或生活歷練特徵",
  "quest_hook": "DM 跑團互動線索：玩家如何與他接觸，他掌握何種情報或能觸發什麼委托事件。"
}}
"""
        models_to_try = [self.model_name] + [m for m in DEFAULT_MODELS if m != self.model_name]
        last_err = None

        from google.genai import types
        gen_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.7
        )

        for m in models_to_try:
            try:
                response = self._client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=gen_config
                )
                text = response.text.strip()
                # 解析 Token 消耗量與費用
                p_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) if hasattr(response, "usage_metadata") else 0
                c_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) if hasattr(response, "usage_metadata") else 0
                t_tokens = getattr(response.usage_metadata, "total_token_count", 0) if hasattr(response, "usage_metadata") else (p_tokens + c_tokens)
                est_cost = (p_tokens * 0.000000075) + (c_tokens * 0.00000030)

                data = json.loads(text)
                return {
                    "backstory": data.get("backstory", ""),
                    "personality_quirks": data.get("personality_quirks", ""),
                    "unorthodox_equipment": data.get("unorthodox_equipment", []),
                    "quest_hook": data.get("quest_hook", ""),
                    "trait_obj": {
                        "name": data.get("trait_name", "常規市井人物"),
                        "category": "AI 劇情設計特質",
                        "game_effect": data.get("trait_effect", "依循常規規則")
                    } if data.get("trait_name") and "常規" not in data.get("trait_name") else None,
                    "token_usage": {
                        "prompt_tokens": p_tokens,
                        "candidates_tokens": c_tokens,
                        "total_tokens": t_tokens,
                        "estimated_cost_usd": f"${est_cost:.6f}",
                        "model": m,
                        "free_tier_status": "Google AI Studio 免費額度內 (0 元 / 每日 1,500 次免費生成)"
                    }
                }
            except Exception as e:
                last_err = e
                continue

        raise last_err or RuntimeError("Gemini 模型皆無法產生回應")

    def _fallback_narrative(
        self,
        name: str,
        race: str,
        class_name: str,
        subclass_display: str,
        level: int,
        background: str,
        story_context: Optional[str],
        custom_trait: Optional[str]
    ) -> Dict:
        """離線無 API Key 時的規則備用生成"""
        is_normal = not custom_trait or "無" in custom_trait
        is_farmer = story_context and any(w in story_context for w in ["農", "草耙", "麥"])
        is_wizard_pipe = story_context and any(w in story_context for w in ["煙斗", "法師", "學者"])

        sub_note = f"身兼【{subclass_display}】之傳承，" if subclass_display and "尚未" not in subclass_display else ""

        if is_farmer:
            backstory = (
                f"{name} 表面上只是在田野間耕作的沉默麥農，手掌長滿厚繭，眼神沉穩而冷靜。"
                f"然而鮮少有人知曉，他曾是名震一時的精銳老戰士，{sub_note}在經歷無數血戰後決定解甲歸田。"
                f"他隱姓埋名，將長劍換成日常的鋼齒草耙；但若這座平靜的村莊遭遇土匪或異怪威脅，"
                f"老人眼中的利芒將瞬間甦醒，以雷霆萬鈞的戰技守護這片土地。"
            )
            quirks = (
                "1. 休息時總會隨手抓起一把麥穗或泥土嗅聞，確認氣候與土壤濕度。\n"
                "2. 談及過去的戰事時會下意識撫摸草耙鐵齒，語調低沉而簡潔。\n"
                "3. 面對陌生冒險者時始終保持背靠實牆的站姿，警戒周遭任何突發異動。"
            )
            equipment = [
                {
                    "name": "鋼齒長草耙 (Steel-Toothed Farm Rake)",
                    "type": "近戰武器 (偽裝農具)",
                    "damage": "1d8 (雙手 1d10) 穿刺",
                    "properties": "多用 (Versatile)、長柄、推撞擊倒判定優勢",
                    "story_lore": "以百煉軍用熟鐵重新鍛造的重型草耙，平時用於梳理乾草，戰時揮舞撕裂敵陣。"
                }
            ]
            hook = f"村中近來傳出地精狼騎兵襲擊哨站的傳聞，村民推舉老農 {name} 協調防務，玩家若能向他出示值得信賴的證物，他將引導隊伍前往一處隱蔽的地下軍火庫。"
        elif is_wizard_pipe:
            backstory = (
                f"{name} 是一位隱居在古老林間的博學長者，長袍邊緣雖已磨損，但眼神深邃如星海。"
                f"{sub_note}他不拘泥於死板的奧術魔杖，反而偏愛在吐納煙草之間引導魔網元素。"
                f"村民們常看見他一邊吞吐青煙，一邊在石板上演算繁複的法陣幾何。"
            )
            quirks = (
                "1. 說話前總會先敲一敲石楠木老煙斗，吐出一圈形如古代符文的淡藍色煙圈。\n"
                "2. 對年輕施法者拙劣的發音不屑一顧，習慣用手指輕點桌面糾正對方的法術模型。\n"
                "3. 翻閱古籍時會將老花眼鏡推到額頭上，隨手抓起羽毛筆在手背上推演算式。"
            )
            equipment = [
                {
                    "name": "刻印符文的石楠木老煙斗 (Carved Briar Smoking Pipe)",
                    "type": "奧術專注法器",
                    "damage": "—",
                    "properties": "法術專注、吞吐青煙勾勒塑形",
                    "story_lore": "老法師遊歷極北冰原時獲得的耐火石楠木，其煙氣帶有淨化心智的微光微粒。"
                }
            ]
            hook = f"{name} 的書齋最近遺失了一張記錄著遠古封印解咒語的羊皮紙，他懷疑被當地的盜墓賊竊走，若玩家能尋回該卷軸，他願意無償為隊伍鑑定一件魔法遺物。"
        else:
            backstory = (
                f"{name} 是一位歷經風霜的冒險者，出身於【{background}】，{sub_note}"
                f"在無數次與危險的交鋒中磨練出一身過人本領。他外表樸素，舉止從容，"
                f"懂得在市井小巷與險惡荒野間尋找平衡，是一位值得信賴的可靠盟友。"
            )
            quirks = (
                "1. 習慣在思考時輕叩腰間的武器握柄或工具皮囊。\n"
                "2. 說話語調平穩，習慣用銳利的眼神打量每個進出酒館的陌生人。\n"
                "3. 對食物與烈酒極具講究，總能準確說出不同酒莊麥酒的年份。"
            )
            equipment = [
                {
                    "name": "隨身淬火短刀 (Well-Tempered Utility Knife)",
                    "type": "近戰簡易武器",
                    "damage": "1d4 穿刺",
                    "properties": "輕型、靈巧",
                    "story_lore": "陪伴他多年的隨身工具刀，刀身刻有一道代表平安歸來的微型守護盧恩符文。"
                }
            ]
            hook = f"{name} 正在追查一批自黑市流出的走私違禁品，他希望能與值得信任的冒險小隊合作，共同探查城郊廢棄倉庫的動靜。"

        trait_obj = None
        if not is_normal:
            trait_obj = {
                "name": f"{custom_trait}之印",
                "category": "規則備用特質",
                "game_effect": f"在涉及【{custom_trait}】的情境中，檢定或應對具有優勢。"
            }

        return {
            "backstory": backstory,
            "personality_quirks": quirks,
            "unorthodox_equipment": equipment,
            "quest_hook": hook,
            "trait_obj": trait_obj,
            "token_usage": None
        }
