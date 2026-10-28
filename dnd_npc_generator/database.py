"""
D&D 5E NPC 繁體中文完整資料庫 (D&D 5e Ruleset & TRPG Extended Database)
包含：
1. 六大屬性定義
2. 種族資訊與彈性加值清單 (不強制寫死，列出可提升選項)
3. 職業特徵、等級解鎖能力庫 (Lv 1 - 20)、熟練加值、法術位表
4. 背景資料庫 (含自選技能、工具熟練與語言彈性選項)
5. 裝備與武器庫 (含對應攻擊傷害骰、傷害類型與護甲 AC)
6. 諸神信仰與語言庫
7. 獨特超常特質庫 (預設為「無」，僅在指定時生成)
"""

# ==========================================
# 1. 六大核心屬性定義
# ==========================================
ATTRIBUTES = [
    ("STR", "力量", "肌肉爆發力、負重與近戰打擊"),
    ("DEX", "敏捷", "手眼協調、敏捷度、反應與反射"),
    ("CON", "體質", "健康度、耐力、生命力與體魄"),
    ("INT", "智力", "記憶力、邏輯推理、受教育程度與奧術理解"),
    ("WIS", "感知", "直覺、洞察力、環境警覺與意志堅韌"),
    ("CHA", "魅力", "自信心、說服力、領導氣質與靈魂存在感")
]

# ==========================================
# 2. 種族加值清單與特性 (彈性提供額外可提升屬性建議)
# ==========================================
RACES = {
    "人類 (Human)": {
        "bonus_options": "標準人類：全屬性各 +1；亦可採用變體規則：任選兩項屬性各 +1 並自選一項專長。",
        "speed": 30,
        "darkvision": 0,
        "languages": ["通用語", "自選任意額外語言 1 種"],
        "lifespan": (16, 90),
        "traits": ["萬用適應力", "多才多藝"]
    },
    "高等精靈 (High Elf)": {
        "bonus_options": "敏捷 +2、智力 +1",
        "speed": 30,
        "darkvision": 60,
        "languages": ["通用語", "精靈語", "自選額外語言 1 種"],
        "lifespan": (100, 750),
        "traits": ["敏銳感官", "精靈血統 (免疫催眠魔法，抗魅惑優勢)", "冥想 (出神 4 小時長休)", "一項自選法師戲法"]
    },
    "木精靈 (Wood Elf)": {
        "bonus_options": "敏捷 +2、感知 +1",
        "speed": 35,
        "darkvision": 60,
        "languages": ["通用語", "精靈語"],
        "lifespan": (100, 750),
        "traits": ["敏銳感官", "精靈血統", "荒野掩蔽 (在微弱自然遮蔽下可隱匿)", "迅捷步伐 (移速 35 呎)"]
    },
    "黑暗精靈 / 卓爾 (Drow)": {
        "bonus_options": "敏捷 +2、魅力 +1",
        "speed": 30,
        "darkvision": 120,
        "languages": ["通用語", "精靈語", "幽暗通用語"],
        "lifespan": (100, 750),
        "traits": ["高級黑暗視覺 (120呎)", "日光敏感", "卓爾天生魔法 (舞光術、妖火、黑暗術)"]
    },
    "山地矮人 (Mountain Dwarf)": {
        "bonus_options": "力量 +2、體質 +2",
        "speed": 25,
        "darkvision": 60,
        "languages": ["通用語", "矮人語"],
        "lifespan": (40, 350),
        "traits": ["矮人體魄 (抗毒傷害與豁免優勢)", "矮人戰鬥訓練", "石工直覺", "矮人士兵輕/中甲熟練"]
    },
    "丘陵矮人 (Hill Dwarf)": {
        "bonus_options": "體質 +2、感知 +1",
        "speed": 25,
        "darkvision": 60,
        "languages": ["通用語", "矮人語"],
        "lifespan": (40, 350),
        "traits": ["矮人體魄 (抗毒)", "矮人強韌 (每等級生命上限額外 +1)", "石工直覺"]
    },
    "輕足半身人 (Lightfoot Halfling)": {
        "bonus_options": "敏捷 +2、魅力 +1",
        "speed": 25,
        "darkvision": 0,
        "languages": ["通用語", "半身人語"],
        "lifespan": (20, 150),
        "traits": ["天生幸運 (d20 擲出 1 可強制重骰)", "勇敢 (抗恐慌優勢)", "天生隱匿 (可躲在體型大於自己的生物身後)"]
    },
    "頑強半身人 (Stout Halfling)": {
        "bonus_options": "敏捷 +2、體質 +1",
        "speed": 25,
        "darkvision": 0,
        "languages": ["通用語", "半身人語"],
        "lifespan": (20, 150),
        "traits": ["天生幸運", "勇敢", "強韌抗毒 (毒素抗性與豁免優勢)"]
    },
    "龍裔 (Dragonborn)": {
        "bonus_options": "力量 +2、魅力 +1",
        "speed": 30,
        "darkvision": 0,
        "languages": ["通用語", "龍語"],
        "lifespan": (15, 80),
        "traits": ["巨龍吐息武器 (5x30呎線狀或15呎錐狀)", "對應龍脈傷害抗性 (火/冰/電/酸/毒)"]
    },
    "半獸人 (Half-Orc)": {
        "bonus_options": "力量 +2、體質 +1",
        "speed": 30,
        "darkvision": 60,
        "languages": ["通用語", "獸人語"],
        "lifespan": (14, 75),
        "traits": ["威嚇天賦", "堅韌不屈 (倒地時維持 1 點 HP，每日一次)", "凶蠻暴擊 (近戰重擊時額外擲一顆武器傷害骰)"]
    },
    "提夫林 (Tiefling)": {
        "bonus_options": "魅力 +2、智力 +1",
        "speed": 30,
        "darkvision": 60,
        "languages": ["通用語", "煉獄語"],
        "lifespan": (16, 100),
        "traits": ["地獄抗性 (火焰抗性)", "地獄奇術 (尋常戲法、地獄叱喝、黑暗術)"]
    },
    "岩石侏儒 (Rock Gnome)": {
        "bonus_options": "智力 +2、體質 +1",
        "speed": 25,
        "darkvision": 60,
        "languages": ["通用語", "侏儒語"],
        "lifespan": (30, 450),
        "traits": ["侏儒狡黠 (對抗魔法的心智豁免優勢)", "工匠知識", "修補工匠 (製作發條玩具、打火器等小裝置)"]
    },
    "半精靈 (Half-Elf)": {
        "bonus_options": "魅力 +2，並可自由任選其他任意兩項不同屬性各 +1",
        "speed": 30,
        "darkvision": 60,
        "languages": ["通用語", "精靈語", "自選任意額外語言 1 種"],
        "lifespan": (20, 180),
        "traits": ["精靈血統 (抗魅惑優勢，免疫睡眠魔法)", "技能多才多藝 (自選任意 2 項技能熟練)"]
    }
}

# ==========================================
# 3. 職業特徵、等級能力與法術環位資料庫 (Lv 1 - 20)
# ==========================================
CLASSES = {
    "戰士 (Fighter)": {
        "hit_die": "d10",
        "primary_recommendation": "主屬性建議配置：【力量】或【敏捷】（視武器類型而定），副屬性【體質】，其次【感知/智力/魅力】。",
        "saves": ["力量 (STR)", "體質 (CON)"],
        "is_spellcaster": False,
        "default_equipment": [
            {"name": "長劍 (Longsword)", "type": "近戰軍用武器", "damage": "1d8 (雙手 1d10) 揮砍", "properties": "多用 (Versatile)"},
            {"name": "重弩 (Heavy Crossbow)", "type": "遠程軍用武器", "damage": "1d10 穿刺", "properties": "彈藥 (100/400)、重型、裝填、雙手"},
            {"name": "鏈甲 (Chain Mail)", "type": "重甲", "ac": "16 AC", "properties": "需求力量 13、隱匿劣勢"},
            {"name": "鋼製盾牌 (Shield)", "type": "盾牌", "ac": "+2 AC", "properties": "提供額外防禦加值"}
        ],
        "features_by_level": {
            1: ["戰鬥風格 (Fighting Style: 如防禦、箭術、巨武器、對決等)", "回氣 (Second Wind: 附贈動作恢復 1d10 + 等級 HP)"],
            2: ["動作湧潮 (Action Surge: 額外執行一個完整動作，短休或長休恢復)"],
            3: ["武藝範型 (Martial Archetype: 如冠軍、奧法騎士、戰鬥大師)"],
            4: ["屬性值提升 (ASI) 或專長選擇"],
            5: ["額外攻擊 (Extra Attack: 每次攻擊動作可攻擊 2 次)"],
            6: ["額外屬性值提升 (ASI)"],
            7: ["武藝範型進階特性"],
            9: ["堅韌不屈 (Indomitable: 豁免失敗時可重骰一次，每日一次)"],
            11: ["額外攻擊 (2) (每次攻擊動作可攻擊 3 次)"],
            13: ["堅韌不屈 (Indomitable: 每日 2 次)"],
            14: ["額外屬性值提升 (ASI)"],
            17: ["動作湧潮 (2 次/長休)", "堅韌不屈 (每日 3 次)"],
            20: ["額外攻擊 (3) (每次攻擊動作可攻擊 4 次)"]
        }
    },
    "法師 (Wizard)": {
        "hit_die": "d6",
        "primary_recommendation": "主屬性建議配置：【智力】（施法核心），副屬性【體質】（專注與生存）與【敏捷】（護甲AC防護）。",
        "saves": ["智力 (INT)", "感知 (WIS)"],
        "is_spellcaster": True,
        "spell_type": "全施法者 (Full Caster)",
        "default_equipment": [
            {"name": "長棍 / 法杖 (Quarterstaff)", "type": "近戰簡易武器", "damage": "1d6 (雙手 1d8) 鈍擊", "properties": "多用、可充當奧術法器"},
            {"name": "匕首 (Dagger)", "type": "近戰簡易武器", "damage": "1d4 穿刺", "properties": "靈巧、輕型、投擲 (20/60)"},
            {"name": "法術書 (Spellbook)", "type": "奧術核心道具", "damage": "—", "properties": "記錄所知各環位奧術法術"},
            {"name": "學者長袍與法器 (Scholar's Robe)", "type": "無裝甲", "ac": "10 + 敏捷調整值", "properties": "常態以法師護甲或護盾術防護"}
        ],
        "features_by_level": {
            1: ["奧術施法能力 (Spellcasting)", "奧術回想 (Arcane Recovery: 短休恢復部分消耗法術位)"],
            2: ["奧術傳統學派 (Arcane Tradition: 如塑能、防護、幻術、死靈學派等)"],
            4: ["屬性值提升 (ASI) 或專長選擇"],
            6: ["學派進階特性 (School Feature)"],
            8: ["屬性值提升 (ASI)"],
            10: ["學派進階防護/強化特性"],
            12: ["屬性值提升 (ASI)"],
            14: ["學派終極特性 (Master School Feature)"],
            18: ["法術精通 (Spell Mastery: 自由隨意施展指定的 1 環與 2 環法術)"],
            20: ["標誌性法術 (Signature Spells: 每日兩項 3 環法術免耗法術位施展)"]
        }
    },
    "遊盪者 / 盜賊 (Rogue)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【敏捷】（潛行、閃避與靈巧攻擊），副屬性【智力】（陷阱調研）或【魅力】（偽裝騙徒）。",
        "saves": ["敏捷 (DEX)", "智力 (INT)"],
        "is_spellcaster": False,
        "default_equipment": [
            {"name": "細劍 (Rapier)", "type": "近戰軍用武器", "damage": "1d8 穿刺", "properties": "靈巧 (Finesse，可用敏捷加成)"},
            {"name": "短弓 (Shortbow)", "type": "遠程軍用武器", "damage": "1d6 穿刺", "properties": "彈藥 (80/320)、雙手"},
            {"name": "盜賊工具組 (Thieves' Tools)", "type": "開鎖與陷阱拆解工具", "damage": "—", "properties": "用於破解各類鎖具與機關"},
            {"name": "皮甲 (Leather Armor)", "type": "輕甲", "ac": "11 + 敏捷調整值", "properties": "完全無隱匿劣勢，輕便靈活"}
        ],
        "features_by_level": {
            1: ["專精 (Expertise: 2項技能熟練加值翻倍)", "偷襲 (Sneak Attack: 具優勢或有盟友夾擊時額外骰傷)", "盜賊黑話 (Thieves' Cant)"],
            2: ["巧手狡黠 (Cunning Action: 附贈動作執行疾走、撤離或隱匿)"],
            3: ["遊盪者範型 (Roguish Archetype: 如刺客、詭術師、盜賊)"],
            5: ["離奇閃避 (Uncanny Dodge: 受命中時反應動作使傷害減半)"],
            7: ["反射閃避 (Evasion: 範圍敏捷豁免成功完全無傷，失敗僅半傷)"],
            11: ["可靠天賦 (Reliable Talent: 熟練技能檢定 d20 低於 9 一律視為 10)"],
            14: ["盲知感應 (Blindsense: 10 呎內感知隱形生物)"],
            15: ["滑溜心智 (Slippery Mind: 獲得感知豁免熟練)"],
            20: ["幸運絕殺 (Stroke of Luck: 檢定或攻擊失準時可直接改為成功/命中)"]
        }
    },
    "牧師 (Cleric)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【感知】（神術核心），副屬性【體質】（生命與專注）與【力量】（身著重甲與持槌近戰）。",
        "saves": ["感知 (WIS)", "魅力 (CHA)"],
        "is_spellcaster": True,
        "spell_type": "全施法者 (Full Caster)",
        "default_equipment": [
            {"name": "硬頭錘 (Mace)", "type": "近戰簡易武器", "damage": "1d6 鈍擊", "properties": "堅固神殿武器"},
            {"name": "聖徽與聖物 (Holy Symbol)", "type": "神術法器", "damage": "—", "properties": "引導神力與施展神術媒介"},
            {"name": "鱗甲 (Scale Mail)", "type": "中甲", "ac": "14 + 敏捷調整值 (上限+2)", "properties": "隱匿檢定劣勢"},
            {"name": "木製聖徽盾牌 (Shield)", "type": "盾牌", "ac": "+2 AC", "properties": "表面繪製所信仰神祇的神聖符號"}
        ],
        "features_by_level": {
            1: ["神聖神術施法 (Spellcasting)", "神聖領域 (Divine Domain: 如生命、光明、戰爭、風暴等)"],
            2: ["引導神力 (Channel Divinity: 驅散不死生物、領域專屬神力)"],
            5: ["摧毀不死生物 (Destroy Undead: 驅散時直接粉碎低 CR 亡靈)"],
            6: ["引導神力 (每日 2 次)"],
            8: ["神聖打擊 (Divine Strike) 或 強效聖火戲法 (Potent Cantrip)"],
            10: ["神聖干預 (Divine Intervention: 祈求神祇親自降臨顯聖奇蹟)"],
            17: ["摧毀不死生物 (CR 4 亡靈)"],
            20: ["保證神聖干預 (Divine Intervention 必定 100% 成功顯靈)"]
        }
    },
    "野蠻人 (Barbarian)": {
        "hit_die": "d12",
        "primary_recommendation": "主屬性建議配置：【力量】（狂暴揮砍與近戰加成），副屬性【體質】（生命厚度與無甲防禦），其次【敏捷】。",
        "saves": ["力量 (STR)", "體質 (CON)"],
        "is_spellcaster": False,
        "default_equipment": [
            {"name": "巨斧 (Greataxe)", "type": "近戰軍用武器", "damage": "1d12 揮砍", "properties": "重型、雙手、狂暴重劈"},
            {"name": "雙持手斧 (Handaxe x2)", "type": "近戰簡易武器", "damage": "1d6 揮砍", "properties": "輕型、投擲 (20/60)"},
            {"name": "標槍 (Javelin x4)", "type": "投擲武器", "damage": "1d6 穿刺", "properties": "投擲 (30/120)"},
            {"name": "無甲身軀 (Unarmored Defense)", "type": "天生體魄", "ac": "10 + 敏捷調整值 + 體質調整值", "properties": "不著護甲時直接以鋼鐵筋肉抵禦傷害"}
        ],
        "features_by_level": {
            1: ["狂暴 (Rage: 近戰傷害增益、鈍刺斬抗性、力量檢定優勢)", "無甲防禦 (Unarmored Defense)"],
            2: ["魯莽攻擊 (Reckless Attack: 攻擊具優勢，但敵人攻擊自身亦具優勢)", "危險感知 (Danger Sense: 對看見的陷阱敏捷豁免具備優勢)"],
            3: ["原始道途 (Primal Path: 如狂戰士、圖騰勇者、狂野魔法)"],
            5: ["額外攻擊 (Extra Attack)", "快速移動 (Fast Movement: 未著重甲時移速 +10 呎)"],
            7: ["野性本能 (Feral Instinct: 先攻檢定具備優勢，突襲不受制)"],
            9: ["蠻力重擊 (Brutal Critical: 近戰重擊額外擲 1 顆武器傷害骰)"],
            11: ["無情狂暴 (Relentless Rage: 狂暴中 HP 歸零可通過 DC 10 體質豁免降至 1)"],
            15: ["不屈狂暴 (Persistent Rage: 狂暴唯有昏迷或主動終止方才結束)"],
            20: ["原始勇士 (Primal Champion: 力量與體質上限永久 +4，最高至 24)"]
        }
    },
    "聖騎士 (Paladin)": {
        "hit_die": "d10",
        "primary_recommendation": "主屬性建議配置：【力量】（武器戰技），副屬性【魅力】（誓約神聖靈光與神術），其次【體質】。",
        "saves": ["感知 (WIS)", "魅力 (CHA)"],
        "is_spellcaster": True,
        "spell_type": "半施法者 (Half Caster: 2級開始獲得法術位)",
        "default_equipment": [
            {"name": "戰錘 / 長劍 (Warhammer / Longsword)", "type": "近戰軍用武器", "damage": "1d8 (雙手 1d10) 鈍擊/揮砍", "properties": "多用"},
            {"name": "標槍 (Javelin x5)", "type": "投擲武器", "damage": "1d6 穿刺", "properties": "投擲 (30/120)"},
            {"name": "板條甲 (Splint Mail)", "type": "重甲", "ac": "17 AC", "properties": "需求力量 15、隱匿劣勢"},
            {"name": "神聖徽章盾牌 (Shield)", "type": "盾牌", "ac": "+2 AC", "properties": "刻印神聖誓言符文"}
        ],
        "features_by_level": {
            1: ["神聖感知 (Divine Sense: 探測 60 呎內天界、邪魔、不死生物氣息)", "聖療 (Lay on Hands: 聖療能量池 = 等級 x 5 點生命回覆)"],
            2: ["戰鬥風格 (Fighting Style)", "神聖施法 (Spellcasting)", "至聖斬 (Divine Smite: 命中時消耗法術位注入神聖光芒爆發傷害)"],
            3: ["神聖誓約 (Sacred Oath: 如奉獻之誓、復仇之誓、古老之誓)", "神聖健康 (免疫一切自然與魔法疾病)"],
            6: ["守護靈光 (Aura of Protection: 自身與 10 呎內盟友豁免獲得魅力調整值加成)"],
            10: ["勇氣靈光 (Aura of Courage: 自身與 10 呎內盟友免疫恐慌)"],
            11: ["改良至聖斬 (Improved Divine Smite: 近戰攻擊常態自帶 1d8 光耀傷害)"],
            14: ["淨化之觸 (Cleansing Touch: 每日以動作驅散身上的異常法術效果)"],
            18: ["靈光範圍擴展 (靈光半徑擴展至 30 呎)"],
            20: ["神聖化身 (Oath Avatar: 化身誓約聖光或復仇死神形態)"]
        }
    }
}

# ==========================================
# 4. 法術位對照表 (全施法者標準 Full Caster Spell Slots)
# ==========================================
SPELL_SLOTS_TABLE = {
    1: {"1環": 2},
    2: {"1環": 3},
    3: {"1環": 4, "2環": 2},
    4: {"1環": 4, "2環": 3},
    5: {"1環": 4, "2環": 3, "3環": 2},
    6: {"1環": 4, "2環": 3, "3環": 3},
    7: {"1環": 4, "2環": 3, "3環": 3, "4環": 1},
    8: {"1環": 4, "2環": 3, "3環": 3, "4環": 2},
    9: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 1},
    10: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2},
    11: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1},
    12: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1},
    13: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1, "7環": 1},
    14: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1, "7環": 1},
    15: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1, "7環": 1, "8環": 1},
    16: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1, "7環": 1, "8環": 1},
    17: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 2, "6環": 1, "7環": 1, "8環": 1, "9環": 1},
    18: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 3, "6環": 1, "7環": 1, "8環": 1, "9環": 1},
    19: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 3, "6環": 2, "7環": 1, "8環": 1, "9環": 1},
    20: {"1環": 4, "2環": 3, "3環": 3, "4環": 3, "5環": 3, "6環": 2, "7環": 2, "8環": 1, "9環": 1}
}

# ==========================================
# 5. 角色背景資料庫 (具備多向技能與工具/語言自選彈性)
# ==========================================
BACKGROUNDS = {
    "侍祭 (Acolyte)": {
        "skills_options": "固定熟練：【洞察】、【宗教】",
        "tool_options": "無特定工具",
        "language_options": "可自選任意 2 種額外語言（通常選擇天界語、深淵語或古老語）",
        "feature": "庇護所 (Shelter of the Faithful)：在同信仰神廟與信徒社群中享有免費食宿與神術照護援助。"
    },
    "貴族 (Noble)": {
        "skills_options": "固定熟練：【歷史】、【說服】",
        "tool_options": "自選一項博弈工具（如龍棋、三龍牌或骰子）",
        "language_options": "自選任意 1 種額外語言",
        "feature": "特權階級 (Position of Privilege)：在上流社會廣受尊重，平民百姓會給予禮遇並可獲見當地統治貴族。"
    },
    "罪犯 / 間諜 (Criminal / Spy)": {
        "skills_options": "固定熟練：【欺瞞】、【隱匿】",
        "tool_options": "固定熟練：【盜賊工具組】；並自選一項博弈工具",
        "language_options": "無額外語言（但掌握地下黑話密碼渠道）",
        "feature": "黑道線人 (Criminal Contact)：擁有專屬且忠誠的地下聯絡人，能在城鎮中迅速調集黑市情報與走私管道。"
    },
    "民間英雄 (Folk Hero)": {
        "skills_options": "固定熟練：【馴獸】、【求生】",
        "tool_options": "自選一項工匠工具熟練；以及陸上載具駕馭熟練",
        "language_options": "無額外語言",
        "feature": "鄉野聲望 (Rustic Hospitality)：平民與農民視你為同路人，願意無償提供藏身庇護與粗茶淡飯。"
    },
    "學者 (Sage)": {
        "skills_options": "固定熟練：【奧秘】、【歷史】",
        "tool_options": "無特定工具",
        "language_options": "可自選任意 2 種額外語言（廣納遠古或異界文獻）",
        "feature": "學術研究 (Researcher)：即便你不知道某項遠古機密，你也清楚知道哪座圖書館或哪位學者握有該情報。"
    },
    "士兵 (Soldier)": {
        "skills_options": "固定熟練：【運動】、【威嚇】",
        "tool_options": "自選一項博弈工具；以及陸上載具駕馭熟練",
        "language_options": "無額外語言",
        "feature": "軍旅威望 (Military Rank)：前部隊袍澤與同盟衛兵認同你的軍階榮譽，必要時可借調軍營物資或通行檢查哨。"
    },
    "水手 (Sailor)": {
        "skills_options": "固定熟練：【運動】、【察覺】",
        "tool_options": "固定熟練：領航工具、水上載具駕駛",
        "language_options": "無額外語言",
        "feature": "航運通行 (Ship's Passage)：能在信賴的商船或漁船上為自己與同伴爭取免費搭乘的航運便船。"
    },
    "行會工匠 (Guild Artisan)": {
        "skills_options": "固定熟練：【洞察】、【說服】",
        "tool_options": "自選一項特定專業工匠工具（如鐵匠、煉金、木工、製皮等）",
        "language_options": "自選任意 1 種額外語言",
        "feature": "行會特權 (Guild Membership)：受到商業行會庇護，享有批發價格、法律辯護援助與行會大廳招待。"
    },
    "流浪兒 (Urchin)": {
        "skills_options": "固定熟練：【巧手】、【隱匿】",
        "tool_options": "固定熟練：偽造工具組、盜賊工具組",
        "language_options": "無額外語言",
        "feature": "城市秘道 (City Secrets)：熟悉市井街巷與屋頂陰影，非戰鬥狀態下在城鎮中穿梭速度為常人的兩倍。"
    }
}

# ==========================================
# 6. 信仰神祇與語言庫
# ==========================================
DEITIES = [
    ("提爾 (Tyr)", "正義、公理、法制與律法之神（守序善良）"),
    ("洛山達 (Lathander)", "黎明、新生、春天與活力之神（中立善良）"),
    ("塞倫涅 (Selûne)", "月光、繁星、夜遊者與導航女神（混亂善良）"),
    ("坦帕斯 (Tempus)", "戰爭、榮譽戰鬥與勇武之神（絕對中立）"),
    ("密斯拉 (Mystra)", "魔法之母、奧術奧秘與魔網女神（中立善良）"),
    ("歐格瑪 (Oghma)", "知識、發明、學術與思辨之神（絕對中立）"),
    ("凱蘭沃 (Kelemvor)", "死亡、死者安息與公正評判之神（守序中立）"),
    ("渥金 (Waukeen)", "貿易、財富、契約與商貿女神（絕對中立）"),
    ("摩拉丁 (Moradin)", "鍛造、矮人創造者與磐石守護之神（守序善良）"),
    ("科瑞隆 (Corellon)", "精靈主神、魔法、藝術與自由之神（混亂善良）"),
    ("萬物有靈 / 自然信仰", "崇敬荒野四季、林間生靈與元素循環"),
    ("無特定信仰 / 實用世俗派", "不盲從諸神神諭，堅信手中的刀劍、技藝與同伴信任")
]

STANDARD_LANGUAGES = [
    "通用語 (Common)", "精靈語 (Elvish)", "矮人語 (Dwarvish)", "巨人語 (Giant)",
    "侏儒語 (Gnomish)", "地精語 (Goblin)", "半身人語 (Halfling)", "獸人語 (Orc)"
]

EXOTIC_LANGUAGES = [
    "深淵語 (Abyssal)", "天界語 (Celestial)", "龍語 (Draconic)", "深境語 (Deep Speech)",
    "煉獄語 (Infernal)", "原初語 (Primordial)", "木族語 (Sylvan)", "幽暗通用語 (Undercommon)"
]

# ==========================================
# 7. 獨特非傳統特質庫 (超常能力/自訂天賦)
# 預設為「無」，僅在使用者指定關鍵字或需求時啟用
# ==========================================
UNIQUE_TRAITS_PRESETS = [
    {
        "keywords": ["火", "火焰", "烈焰", "炎", "灼熱", "fire"],
        "name": "炎脈共鳴 (Fire Affinity)",
        "category": "元素異能",
        "description": "體內流淌著不滅的火元素微光，生來對火焰有著本能的吸引力。",
        "game_effect": "天生具有火焰傷害抗性（受火焰傷害減半）；近戰武器命中時刀刃浮現微火，可額外造成 1d4 點火焰傷害。"
    },
    {
        "keywords": ["冰", "霜", "極寒", "凍", "冷", "frost", "ice"],
        "name": "霜痕凍軀 (Frost-Scarred)",
        "category": "元素異能",
        "description": "體溫長年維持在冰點，呼氣凝霜，皮膚帶有藍白色的凍紋。",
        "game_effect": "天生具有寒冷傷害抗性；周身 5 呎範圍內帶有微寒霜氣，徒手觸碰液體可在 1 回合內使其結為薄冰。"
    },
    {
        "keywords": ["靈", "幽靈", "魂", "亡靈", "死靈", "ghost", "spirit"],
        "name": "靈視眼眸 (Ghost Sight)",
        "category": "超感官知",
        "description": "雙眼中有一圈淡紫色的幽冥光環，能窺探肉眼無法辨識的乙太夾縫。",
        "game_effect": "可感知周圍 30 呎內的亡魂、靈體與隱形生物殘影；對任何幻術學派魔法的豁免檢定具有優勢。"
    },
    {
        "keywords": ["骨", "鐵", "堅硬", "防禦", "肉體", "iron", "bone"],
        "name": "鐵石骨髓 (Ironbound Bones)",
        "category": "肉體突變",
        "description": "骨骼密度是常人的三倍，敲擊時會發出沉悶的生鐵回響。",
        "game_effect": "未著護甲時基礎 AC 為 13 + 敏捷調整值；受到來自非魔法鈍擊傷害減少 2 點（負重游泳檢定劣勢）。"
    },
    {
        "keywords": ["空間", "傳送", "閃爍", "瞬移", "teleport", "blink"],
        "name": "虛空微步 (Flicker Step)",
        "category": "空間異能",
        "description": "與靈界平面有著短暫的微弱諧振，專注或受驚時身形會出現重疊虛影。",
        "game_effect": "每日可使用 1 次：以附贈動作瞬間傳送至 15 呎內看得到且未被佔據的空間，伴隨無聲的蒼白微電。"
    },
    {
        "keywords": ["運氣", "命運", "宿命", "幸運", "luck", "fate"],
        "name": "逆命重骰 (Fateful Turning)",
        "category": "因果宿命",
        "description": "身上帶著難以言喻的命運歪曲氣場，常在絕境中引發巧合逆轉。",
        "game_effect": "每日 1 次：當自己或 10 呎內的一名盟友在 d20 檢定中擲出「1（大失敗）」時，可以立即強制該對象重新擲骰一次並採用新結果。"
    }
]

# ==========================================
# 8. 所屬陣營庫 (D&D 5E Alignments)
# ==========================================
ALIGNMENTS = [
    ("守序善良 (Lawful Good)", "恪守榮譽、正義法律，並致力保護無辜平民。"),
    ("中立善良 (Neutral Good)", "行事出於善心，不拘泥於教條或法律，只求為善。"),
    ("混亂善良 (Chaotic Good)", "崇尚自由與良善，為反抗不公不惜打破一切繁文縟節。"),
    ("守序中立 (Lawful Neutral)", "嚴守規章、秩序、傳統或個人誓約，不偏袒私情。"),
    ("絕對中立 (True Neutral)", "務實求生，維持生態平衡或專注於眼前的生存與本職。"),
    ("混亂中立 (Chaotic Neutral)", "完全隨興隨心所欲，追求無拘無束的個人自由。"),
    ("守序邪惡 (Lawful Evil)", "巧妙利用規則、契約或階層權力，冷酷達成自私野心。"),
    ("中立邪惡 (Neutral Evil)", "純粹追求個人利益，為達目的毫無底線，背信棄義。"),
    ("混亂邪惡 (Chaotic Evil)", "受毀滅、貪婪或瘋狂驅使，熱衷帶來血腥與混亂。")
]

# ==========================================
# 9. 趣味非典型武器庫 (Thematic & Unorthodox Weapons for NPCs)
# 讓市井農夫、屠夫、老兵、工匠也能擁有合情合理且帶感的戰鬥工具
# ==========================================
THEMATIC_CUSTOM_WEAPONS = {
    "草耙": {
        "name": "鋼齒長草耙 (Steel-Toothed Farm Rake)",
        "type": "農具 / 改裝雙手長柄武器",
        "damage": "1d8 (雙手 1d10) 穿刺",
        "properties": "多用 (Versatile)、長柄武器、重擊時可嘗試進行推撞伏地"
    },
    "草叉": {
        "name": "強化鐵製乾草叉 (Reinforced Pitchfork)",
        "type": "農具 / 近戰刺擊武器",
        "damage": "1d6 (雙手 1d8) 穿刺",
        "properties": "投擲 (射程 20/60)、多用"
    },
    "鐵鎬": {
        "name": "厚重礦工鎬 (Heavy Mining Pick)",
        "type": "採礦工具 / 破甲武器",
        "damage": "1d8 穿刺",
        "properties": "多用 (雙手 1d10)、對厚重護甲具有破甲破壞感"
    },
    "剁刀": {
        "name": "沈重剁骨刀 (Heavy Bone-Cleaver)",
        "type": "屠宰刀具 / 近戰劈砍武器",
        "damage": "1d6 揮砍",
        "properties": "輕型 (Light)、靈巧 (Finesse)"
    },
    "手杖": {
        "name": "包鉛厚橡木手杖 (Lead-Weighted Walking Cane)",
        "type": "隨身手杖 / 隱蔽近戰武器",
        "damage": "1d6 (雙手 1d8) 鈍擊",
        "properties": "多用、外表極似日常拄行工具，不易被衛兵查扣"
    },
    "鐵錘": {
        "name": "鍛造大方錘 (Blacksmith's Sledgehammer)",
        "type": "鐵匠工具 / 近戰重鈍武器",
        "damage": "2d6 鈍擊",
        "properties": "重型、雙手、猛擊碎骨"
    },
    "魚叉": {
        "name": "倒鉤捕鯨矛 (Barbed Whaling Harpoon)",
        "type": "漁民獵具 / 遠程投擲武器",
        "damage": "1d8 穿刺",
        "properties": "投擲 (射程 30/120)、帶細麻繩可將命中目標拉扯回身旁"
    },
    "撬棍": {
        "name": "染血生鏽鐵撬 (Bloodstained Heavy Crowbar)",
        "type": "破拆工具 / 即興近戰鈍器",
        "damage": "1d4 鈍擊",
        "properties": "破拆門扉檢定優勢、實心硬生鐵"
    }
}

# ==========================================
# 10. 獨特非傳統施法法器庫 (Eccentric & Non-Traditional Arcane Focuses)
# 擺脫「法師只能拿水晶球/法杖」的死板限制，大幅提升角色故事味
# ==========================================
THEMATIC_ARCANE_FOCUSES = [
    {
        "keywords": ["煙斗", "菸斗", "草藥", "抽煙", "pipe", "smoke"],
        "name": "刻印符文的石楠木老煙斗 (Carved Briar Smoking Pipe)",
        "description": "長年叼在嘴角的老舊雕花木煙斗。深吸一口特殊煙草並徐徐吐出時，裊裊青煙會在半空中凝結成微光奧術幾何符文，充當施法法器與法術塑形的媒介。"
    },
    {
        "keywords": ["算盤", "帳本", "商人", "硬幣", "金幣", "abacus", "coin"],
        "name": "純黃銅精工算盤 (Brass Calculation Abacus)",
        "description": "框架上刻滿矩陣與微型數秘術刻度的精巧算盤。每當指尖飛快撥動算珠發出清脆金屬聲時，空間中的魔力幾何隨之精準坍縮施放。"
    },
    {
        "keywords": ["茶杯", "茶", "杯", "占卜", "tea", "cup"],
        "name": "裂紋青花占卜瓷杯 (Cracked Divination Teacup)",
        "description": "外表有著金繕修補痕跡的小瓷茶杯。施法時晃動杯中殘留的深色茶漬，茶葉碎屑會如活物般排列出相應的咒術符印。"
    },
    {
        "keywords": ["懷錶", "時鐘", "鐘錶", "時間", "watch", "clock"],
        "name": "逆行滴答的青銅懷錶 (Reverse-Ticking Bronze Pocket Watch)",
        "description": "表面玻璃佈滿蛛網裂痕，秒針偶爾反向跳動。打開錶蓋時微弱的齒輪摩擦聲能干擾周遭時空維度，作為極具壓迫感的奧術法器。"
    },
    {
        "keywords": ["羽毛筆", "墨水", "書記", "筆", "quill", "pen"],
        "name": "吸血渡鴉羽毛筆 (Vampiric Raven Quill)",
        "description": "筆尖浸透了特殊發光墨水，無需墨水瓶即可在虛空中凌空勾勒符文軌跡，墨痕隨即燃燒化作實體法術衝擊。"
    },
    {
        "keywords": ["骨頭", "骨飾", "爪", "巫毒", "bone", "claw"],
        "name": "串連風乾烏鴉爪的骨符 (Dried Crow Talon Talisman)",
        "description": "以粗麻繩和細狼皮串起的風乾烏鴉爪與鳥喙骨飾。輕輕晃動時發出陰鬱的碎骨碰撞聲，引導古老的荒野神術或靈界死靈能量。"
    }
]

