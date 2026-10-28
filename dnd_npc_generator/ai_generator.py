"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 - AI 核心生成器 (AI Narrative Engine)
整合 Google Gemini 旗艦大語言模型與 D&D 5E 規則體系，
真正實現由 AI 深度設計背景身世、非典型生活裝備映射、言行小動作與跑團伏筆線索。
"""

import os
import sys
import re
import json
from typing import Dict, Optional, Tuple

# 導入規則與擲骰模組
from .roller import generate_ability_rolls, build_recommended_allocation
from .database import (
    RACES, CLASSES, BACKGROUNDS, ALIGNMENTS, DEITIES,
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
    2. 隨機或指定基礎種族、職業、背景、年齡、信仰與語言
    3. 呼叫 Gemini AI 模型深度撰寫：
       - 融入 DM 劇情的情境背景短史 (Backstory)
       - 富有生活感與反差魅力的言行舉止、口吻與細節小動作 (Personality & Quirks)
       - 符合 5E 傷害骰與規則規格的非典型武器/法器/特殊能力 (Unorthodox Equipment)
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

    def generate(
        self,
        name: Optional[str] = None,
        race_name: Optional[str] = None,
        class_name: Optional[str] = None,
        background_name: Optional[str] = None,
        level_input: Optional[str] = "1",
        importance: str = "次要劇情 NPC (Supporting)",
        story_context: Optional[str] = None,
        custom_trait_keyword: Optional[str] = None,
        force_ai: bool = True
    ) -> Dict:
        """
        生成完整的非典型 NPC 物件
        """
        # 1. 基礎身分隨機與對齊
        race_key, race_data = self._resolve_choice(race_name, RACES)
        class_key, class_data = self._resolve_choice(class_name, CLASSES)
        bg_key, bg_data = self._resolve_choice(background_name, BACKGROUNDS)

        # 2. 解析等級與特殊狀態
        level, level_note = self._parse_level_and_state(level_input)

        # 3. 擲骰 4d6dl1
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

        # 4. 年齡、性別與名稱
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

        # 5. 生命值與熟練加值
        hd_str = class_data.get("hit_die", "d8")
        hd_match = re.search(r"\d+", str(hd_str))
        hd = int(hd_match.group(0)) if hd_match else 8
        con_mod = recommended_alloc.get("CON", {}).get("modifier", 0)
        hp = hd + con_mod + max(1, (hd // 2 + 1 + con_mod)) * (level - 1)
        pb = 2 + (level - 1) // 4

        # 6. 估算挑戰等級 CR
        cr = self._estimate_cr(level, class_key, level_note)

        # 7. 呼叫 AI 生成深度背景、個性小動作與非典型武器故事
        ai_narrative = None
        if self._client and force_ai:
            try:
                ai_narrative = self._generate_ai_story(
                    name=name,
                    race=race_key,
                    class_name=class_key,
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

        # 8. 若無 AI 或呼叫失敗，使用基礎規則生成做為後備
        if not ai_narrative:
            ai_narrative = self._fallback_narrative(
                name=name,
                race=race_key,
                class_name=class_key,
                level=level,
                background=bg_key,
                story_context=story_context,
                custom_trait=custom_trait_keyword
            )

        # 9. 組裝完整 NPC 字典
        darkv = race_data.get("darkvision", 0)
        darkv_str = f"{darkv} 呎" if isinstance(darkv, int) and darkv > 0 else ("無 (常規視力)" if darkv == 0 else str(darkv))
        speed_val = race_data.get("speed", 30)
        speed_str = f"{speed_val} 呎" if isinstance(speed_val, int) else str(speed_val)
        bg_skills = bg_data.get("skills_options", "市井生活熟練")
        if isinstance(bg_skills, list):
            bg_skills_str = "、".join(bg_skills)
        else:
            bg_skills_str = str(bg_skills)

        npc = {
            "name": name,
            "race": race_key,
            "class": class_key,
            "class_name": class_key,
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
            "unlocked_features": self._get_unlocked_features(class_data, level),
            "cr": cr,
            # AI 設計的深度內容
            "ai_crafted": True if self._client and force_ai else False,
            "ai_backstory": ai_narrative.get("backstory", ""),
            "ai_personality_quirks": ai_narrative.get("personality_quirks", ""),
            "ai_unorthodox_equipment": ai_narrative.get("unorthodox_equipment", []),
            "ai_quest_hook": ai_narrative.get("quest_hook", ""),
            "unique_trait": ai_narrative.get("trait_obj"),
            "equipment": ai_narrative.get("unorthodox_equipment", [])
        }

        return npc

    def _generate_ai_story(
        self,
        name: str,
        race: str,
        class_name: str,
        level: int,
        level_note: Optional[str],
        background: str,
        gender: str,
        age: int,
        story_context: Optional[str],
        custom_trait: Optional[str]
    ) -> Dict:
        """
        向 Gemini 發送 Prompt，取得由 AI 深度撰寫的繁體中文背景、個性小動作與非典型武器
        """
        system_instruction = (
            "你是一位頂尖的《龍與地下城》(D&D 5E) 地下城主 (DM) 與奇幻敘事小說家。"
            "你的任務是根據提供的角色數值與玩家的劇情提示，創作兼具『生活市井反差感』、『深刻情感張力』與『嚴謹 5E 規則規格』的 NPC 資料。"
            "請嚴格以繁體中文 (zh-TW) 輸出，且必須返回合法的 JSON 格式。"
        )

        prompt = f"""
請為以下 D&D 5E NPC 角色設計深度的故事背景與非典型生活裝備：

【基本設定】
- 角色姓名：{name}
- 種族：{race}
- 職業：{class_name} (等級: Lv.{level}{f'，特殊狀態: {level_note}' if level_note else ''})
- 性別與年齡：{gender}，{age} 歲
- 背景歷練：{background}
- DM 提供的情境故事：{story_context or "無特定情境，請根據種族職業自由發揮市井生活身分"}
- 非傳統特質/武器關鍵字：{custom_trait or "無 (常規凡人，生活道具)"}

【設計規範】
1. **身分與戰力徹底解耦**：如果 DM 提到農夫、守墓人、商人、廚師或學者，請讓他表面上完全融入市井生活，但戰鬥底層是該職業的實力。
2. **非典型武器/法器**：如果故事提及日常物品（如鋼齒草耙、剁刀、鐵鎬、刻印符文石楠木老煙斗、黃銅算盤），請將其規格化為 D&D 5E 的武器或專注法器（寫明名稱、傷害骰如 1d8/1d10、特性如多用/長柄/偽裝農具、背後的來歷故事）。
3. **常規凡人原則**：若關鍵字包含「無」或未要求超常神力，絕不強加超自然變異，展現純粹的凡人歷練與人情味；若關鍵字提及特殊特質（如火焰、靈魂、封印），則設計符合 5E 規則的獨特特性。
4. **DM 跑團伏筆**：給予地下城主可以直接在跑團當天使用的劇情引入線索 (Quest Hook)。

請嚴格輸出以下 JSON 結構：
{{
  "backstory": "200~350 字的生動故事身世，描述其過去的經歷、隱退或當前的生活，以及為何擁有這身本領。",
  "personality_quirks": "條列 2~3 項極具畫面感的個性特徵與生活細節小動作（例如抽煙斗的小習慣、撫摸草耙鋼齒的下意識動作、說話語調）。",
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
                # 解析 JSON
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
                    } if data.get("trait_name") and "常規" not in data.get("trait_name") else None
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
        level: int,
        background: str,
        story_context: Optional[str],
        custom_trait: Optional[str]
    ) -> Dict:
        """離線或無 API Key 時的智慧後備生成"""
        is_normal = not custom_trait or "無" in custom_trait
        is_farmer = story_context and any(w in story_context for w in ["農", "草耙", "田"])
        is_wizard_pipe = story_context and any(w in story_context for w in ["煙斗", "法師", "學者"])

        if is_farmer:
            backstory = (
                f"{name} 表面上只是個在邊陲村落耕作的老邁麥農，滿手厚繭，性情溫和寡言。"
                f"然而村中無人知曉，他曾是王都禁衛部隊的資深士官長，在一場慘烈的政治肅清後卸甲歸田。"
                f"他早已埋葬了騎士戰甲，唯獨將隨身那把農用鋼草耙淬火鍛打得堅韌無比。若有不長眼的盜匪膽敢破壞這份平靜，"
                f"老人的槍術底子會讓他們明白，耙草與破甲在老兵手裡並無分別。"
            )
            quirks = "• 沉思或觀察陌生人時，習慣用老繭拇指輕撫草耙的鋼齒尖端。\n• 行走時略顯駝背衰老，但下盤穩如磐石，腳步踏出極難引起聲響。"
            eq = [{
                "name": "鋼齒農用長草耙 (Steel-Toothed Farm Rake)",
                "type": "近戰武器 (長柄)",
                "damage": "1d8 (雙手 1d10) 穿刺",
                "properties": "多用 (Versatile)、長柄武器、平時偽裝為普通農具",
                "story_lore": "以昔日軍用鋼槍頭重新回火鍛造為農用草耙，既是農活生計工具，亦是致命戰矛。"
            }]
            hook = "當冒險者來到小鎮打聽附近匪幫動向時，村長會推薦他們去酒館找老丹恩借農具，而眼尖的戰士玩家會立刻察覺老人雙手的握繭絕非單純農夫。"
        elif is_wizard_pipe:
            backstory = (
                f"隱居在林間邊界的 {name}，是一位早已淡出奧術評議會的資深施法者。"
                f"他早已厭棄了傳統魔杖與水晶球的造作繁複，而是將法術符文精雕於一支老舊的石楠木煙斗上。"
                f"透過吞吐蘊含草藥清香的青煙，他能輕巧地引導以太之流。對他而言，生活的智慧遠比浮誇的法術更具力量。"
            )
            quirks = "• 施法或交談時，習慣緩慢點燃老煙斗，透過青煙飄動的方向判斷周遭微弱的魔法流向。\n• 對浮誇自大的年輕法師總會投以寬容而促狹的微笑。"
            eq = [{
                "name": "符文雕刻石楠木老煙斗 (Carved Briar Smoking Pipe)",
                "type": "奧術專注法器 (Arcane Focus)",
                "damage": "1d4 鈍擊 (敲擊用)",
                "properties": "專注施法道具、內嵌草藥香氛可穩定心神",
                "story_lore": "以千年石楠木根瘤手工雕刻，內壁刻有微縮奧術法印，深吸青煙即可凝神導引法術。"
            }]
            hook = "隊伍在迷霧中迷路時，循著一縷帶有薄荷與松針香氣的奇異青煙找到老人的林間木屋，老法師願意給予指引，前提是冒險者替他帶回一小袋罕見的菸草葉。"
        else:
            backstory = (
                f"{name} 是一位生活在市井之中的 {race} {background}。多年來，他憑藉著身為 {class_name} 的真才實學立足，"
                f"見證過城鎮的興衰與冒險者的來去。雖然平日顯得低調純樸，但每當危機降臨，他隨時能展現令人信服的堅毅本領。"
            )
            quirks = "• 說話語調平緩沉著，習慣在開口前先停頓兩秒打量對方的神情。\n• 隨身衣物打理得整潔俐落，對身邊使用的工具格外愛惜。"
            eq = [{
                "name": "慣用生活鐵器與隨身佩刀",
                "type": "近戰武器",
                "damage": "1d6 揮砍/穿刺",
                "properties": "輕型、靈巧",
                "story_lore": "多年日常生活中形影不離的隨身利器。"
            }]
            hook = "作為地方上的熟面孔，他熟知當地的街頭傳聞與地下勢力暗號，可作為冒險者打聽情報的第一站。"

        return {
            "backstory": backstory,
            "personality_quirks": quirks,
            "unorthodox_equipment": eq,
            "quest_hook": hook,
            "trait_obj": None if is_normal else {
                "name": f"非傳統天賦：{custom_trait}",
                "category": "故事生活特長",
                "game_effect": "因特殊生活經驗或血脈特異，在特定情境獲得優勢判定。"
            }
        }

    def _resolve_choice(self, user_choice: Optional[str], db_dict: Dict) -> Tuple[str, Dict]:
        import random
        if not user_choice or "隨機" in user_choice or user_choice == "RANDOM":
            k = random.choice(list(db_dict.keys()))
            return k, db_dict[k]
        for k, v in db_dict.items():
            if k in user_choice or user_choice in k:
                return k, v
        return user_choice, list(db_dict.values())[0]

    def _parse_level_and_state(self, level_input: Optional[str]) -> Tuple[int, Optional[str]]:
        if not level_input:
            return 1, None
        s = str(level_input).strip()
        num_match = re.search(r"\d+", s)
        base_level = int(num_match.group(0)) if num_match else 1

        level_note = None
        if "大魔導師" in s:
            base_level = max(base_level, 13)
            level_note = "大魔導師階級"
        elif "資深" in s or "老兵" in s or "隊長" in s:
            base_level = max(base_level, 5)
            level_note = "百戰老兵階級"

        if any(w in s for w in ["封印", "詛咒", "受損", "壓制", "舊傷"]):
            note_extra = "【能力封印/受限中】：此角色過往實力強大，但因受詛咒或封印，高階能力暫時受限。"
            level_note = f"{level_note}；{note_extra}" if level_note else note_extra

        return min(max(base_level, 1), 20), level_note

    def _estimate_cr(self, level: int, class_name: str, level_note: Optional[str]) -> str:
        if level <= 1:
            cr_base = "1/4"
        elif level <= 2:
            cr_base = "1/2"
        elif level <= 4:
            cr_base = "1"
        elif level <= 6:
            cr_base = "2"
        elif level <= 8:
            cr_base = "3"
        elif level <= 10:
            cr_base = "4"
        elif level <= 12:
            cr_base = "5"
        elif level <= 14:
            cr_base = "6 ~ 8"
        elif level <= 16:
            cr_base = "9 ~ 11"
        else:
            cr_base = "12 ~ 14"

        if level_note and any(w in level_note for w in ["封印", "受限", "詛咒"]):
            return f"{cr_base} (受封印時實戰約 CR 2 ~ 3)"
        return cr_base

    def _get_unlocked_features(self, class_data: Dict, level: int) -> list:
        features = []
        saves = class_data.get("saves") or class_data.get("saving_throws", [])
        if saves:
            features.append(f"豁免檢定熟練：{', '.join(saves)}")
        prog = class_data.get("features_by_level") or class_data.get("progression", {})
        for lvl in range(1, level + 1):
            if lvl in prog:
                for feat in prog[lvl]:
                    features.append(f"[Lv.{lvl}] {feat}")
        return features

    def _generate_npc_name(self, race_name: str, gender: str) -> str:
        import random
        is_female = "女" in gender

        if is_female:
            human_names = ["艾蓮娜 (Elena)", "席爾維亞 (Sylvia)", "瑪格麗特 (Margaret)", "克拉拉 (Clara)", "薇薇安 (Vivian)", "艾瑪 (Emma)"]
            elf_names = ["希爾薇 (Silvya)", "希蘭妮 (Therani)", "莉蘭蒂 (Liranthi)", "艾拉 (Aela)", "賽拉菲娜 (Seraphina)"]
            dwarf_names = ["海爾嘉 (Helga)", "達格瑪 (Dagmar)", "布倫希爾德 (Brunhilde)", "瓦爾達 (Varda)"]
            halfling_names = ["羅絲 (Rosie)", "貝拉 (Bella)", "波比 (Poppy)", "瑪莉金 (Marigold)"]
            tiefling_names = ["希望 (Hope)", "安息 (Rest)", "無垢 (Verity)", "凱莉絲 (Kallista)"]
            dragonborn_names = ["蘇拉希 (Surina)", "米蘇拉 (Misla)", "朵拉希 (Doraxi)"]
        else:
            human_names = ["老丹恩 (Old Dan)", "羅蘭 (Roland)", "維克托 (Viktor)", "馬庫斯 (Marcus)", "蓋文 (Gavin)", "愛德華 (Edward)"]
            elf_names = ["埃拉利恩 (Elalion)", "費拉米爾 (Faeramir)", "愛蘭迪爾 (Aelandir)", "索隆迪爾 (Thorondir)"]
            dwarf_names = ["布魯諾 (Bruenor)", "托拉丁 (Thoradin)", "巴林 (Balin)", "達剛 (Dargun)", "格羅姆 (Grom)"]
            halfling_names = ["米羅 (Milo)", "芬恩 (Finn)", "佩里格林 (Peregrin)", "阿爾菲 (Alfie)"]
            tiefling_names = ["悲哀 (Sorrow)", "恐懼 (Dread)", "馬拉基 (Malachi)", "巴拉卡斯 (Barakas)"]
            dragonborn_names = ["巴拉薩 (Balasar)", "阿爾漢 (Arjhan)", "朵納爾 (Donaar)"]

        if "精靈" in race_name:
            return random.choice(elf_names)
        elif "矮人" in race_name:
            return random.choice(dwarf_names)
        elif "半身人" in race_name or "侏儒" in race_name:
            return random.choice(halfling_names)
        elif "提夫林" in race_name:
            return random.choice(tiefling_names)
        elif "龍裔" in race_name:
            return random.choice(dragonborn_names)
        elif "半獸人" in race_name or "獸人" in race_name:
            return "格羅克 (Grok)" if not is_female else "烏爾卡 (Urka)"
        else:
            return random.choice(human_names)

