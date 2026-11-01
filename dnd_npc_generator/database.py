"""
D&D 5E NPC 繁體中文完整資料庫 (D&D 5e Ruleset & TRPG Extended Database)
包含：
1. 六大屬性定義
2. 種族資訊與彈性加值清單 (不強制寫死，列出可提升選項)
3. 職業特徵、等級解鎖能力庫 (Lv 1 - 20)、熟練加值、法術位表 (包含全 13 大核心職業)
4. 子職業 / 範型系統 (Subclasses / Paradigms / Archetypes)
5. 背景資料庫 (含自選技能、工具熟練與語言彈性選項，涵蓋中文Compendium完整背景)
6. 裝備與武器庫 (含對應攻擊傷害骰、傷害類型與護甲 AC)
7. 諸神信仰與語言庫
8. 獨特超常特質庫 (預設為「無」，僅在指定時生成)
9. 所屬陣營庫
10. 趣味非典型武器庫與非傳統施法法器庫
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
        "lifespan": (40, 500),
        "traits": ["侏儒狡黠 (對智力/感知/魅力的所有法術豁免具備優勢)", "工匠知識", "小巧修補匠 (製造發條玩具、打火器或音樂盒)"]
    },
    "半精靈 (Half-Elf)": {
        "bonus_options": "魅力 +2，並可自由選擇另外任意兩項屬性各 +1",
        "speed": 30,
        "darkvision": 60,
        "languages": ["通用語", "精靈語", "自選任意語言 1 種"],
        "lifespan": (20, 180),
        "traits": ["精靈血統 (抗魅惑優勢，免疫睡眠魔法)", "技能多才多藝 (自選任意 2 項技能熟練)"]
    }
}

# ==========================================
# 3. 職業特徵、等級能力與法術環位資料庫 (Lv 1 - 20，共 13 大職業)
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
            3: ["武藝範型 (Martial Archetype)"],
            4: ["屬性值提升 (ASI) 或專長選擇"],
            5: ["額外攻擊 (Extra Attack: 每次攻擊動作可攻擊 2 次)"],
            6: ["額外屬性值提升 (ASI)"],
            7: ["武藝範型進階特性"],
            9: ["堅韌不屈 (Indomitable: 豁免失敗時可重骰一次，每日 1 次)"],
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
            2: ["奧術傳承 (Arcane Tradition)"],
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
    "遊盪者 (Rogue)": {
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
            3: ["盜賊範型 (Roguish Archetype)"],
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
            1: ["神聖神術施法 (Spellcasting)", "神聖領域 (Divine Domain)"],
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
            2: ["魯莽攻擊 (Reckless Attack: 攻擊具優勢，但敵人攻擊自身亦具優勢)", "危險感知 (Danger Sense: 對陷阱敏捷豁免具備優勢)"],
            3: ["原初本道 (Primal Path)"],
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
            3: ["神聖之誓 (Sacred Oath)", "神聖健康 (免疫一切自然與魔法疾病)"],
            6: ["守護靈光 (Aura of Protection: 自身與 10 呎內盟友豁免獲得魅力調整值加成)"],
            10: ["勇氣靈光 (Aura of Courage: 自身與 10 呎內盟友免疫恐慌)"],
            11: ["改良至聖斬 (Improved Divine Smite: 近戰攻擊常態自帶 1d8 光耀傷害)"],
            14: ["淨化之觸 (Cleansing Touch: 每日以動作驅散身上的異常法術效果)"],
            18: ["靈光範圍擴展 (靈光半徑擴展至 30 呎)"],
            20: ["神聖化身 (Oath Avatar: 化身誓約聖光或復仇死神形態)"]
        }
    },
    "德魯伊 (Druid)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【感知】（自然神術核心），副屬性【體質】（專注與生存）與【敏捷】（無裝甲防禦）。",
        "saves": ["智力 (INT)", "感知 (WIS)"],
        "is_spellcaster": True,
        "spell_type": "全施法者 (Full Caster)",
        "default_equipment": [
            {"name": "彎刀 (Scimitar)", "type": "近戰軍用武器", "damage": "1d6 揮砍", "properties": "輕型、靈巧"},
            {"name": "槲寄生小枝與德魯伊法器 (Druidic Focus)", "type": "自然神術法器", "damage": "—", "properties": "引導原初荒野神術媒介"},
            {"name": "皮甲 (Leather Armor)", "type": "輕甲", "ac": "11 + 敏捷調整值", "properties": "不穿金屬盔甲"},
            {"name": "木製盾牌 (Wooden Shield)", "type": "盾牌", "ac": "+2 AC", "properties": "純木製自然盾牌"}
        ],
        "features_by_level": {
            1: ["德魯伊施法 (Druid Spellcasting)", "德魯伊語 (Druidic: 荒野守護者的秘傳語言)"],
            2: ["荒野形態 (Wild Shape: 每日 2 次化身野獸)", "德魯伊結社 (Druid Circle)"],
            4: ["荒野形態改良 (可化身水生游水野獸)"],
            8: ["荒野形態改良 (可化身飛行空禽野獸)"],
            18: ["永恆身軀 (Timeless Body: 衰老速度放慢 10 倍)", "野獸施法 (Beast Spells: 荒野形態下可施展法術)"],
            20: ["大德魯伊 (Archdruid: 無限次數使用荒野形態)"]
        }
    },
    "吟遊詩人 (Bard)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【魅力】（表演、施法與說服核心），副屬性【敏捷】（輕甲與靈巧武器），其次【體質】。",
        "saves": ["敏捷 (DEX)", "魅力 (CHA)"],
        "is_spellcaster": True,
        "spell_type": "全施法者 (Full Caster)",
        "default_equipment": [
            {"name": "細劍 (Rapier)", "type": "近戰軍用武器", "damage": "1d8 穿刺", "properties": "靈巧"},
            {"name": "魯特琴 / 風笛 (Lute / Musical Instrument)", "type": "樂器與施法媒介", "damage": "—", "properties": "引導魔網音波共振"},
            {"name": "皮甲 (Leather Armor)", "type": "輕甲", "ac": "11 + 敏捷調整值", "properties": "靈活輕便"},
            {"name": "匕首 (Dagger)", "type": "近戰簡易武器", "damage": "1d4 穿刺", "properties": "靈巧、輕型、投擲"}
        ],
        "features_by_level": {
            1: ["詩人施法 (Spellcasting)", "詩人激勵 (Bardic Inspiration: 賦予盟友 d6 激勵骰)"],
            2: ["萬事通 (Jack of All Trades: 未熟練技能檢定獲得半數 PB 加值)", "休養曲 (Song of Rest: 短休額外恢復生命)"],
            3: ["吟遊詩人學院 (Bard College)", "專精 (Expertise: 2項技能熟練翻倍)"],
            5: ["激勵之泉 (Font of Inspiration: 短休恢復激勵骰)", "激勵骰升級為 d8"],
            6: ["反制之音 (Countercharm)"],
            10: ["魔法奧秘 (Magical Secrets: 跨職業學習任意法術)", "激勵骰升級為 d10"],
            15: ["激勵骰升級為 d12"],
            20: ["卓越靈感 (Superior Inspiration)"]
        }
    },
    "武僧 (Monk)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【敏捷】（身手與徒手打擊）與【感知】（氣能量與防禦），副屬性【體質】。",
        "saves": ["力量 (STR)", "敏捷 (DEX)"],
        "is_spellcaster": False,
        "default_equipment": [
            {"name": "長棍 (Quarterstaff)", "type": "近戰武僧武器", "damage": "1d6 (雙手 1d8) 鈍擊", "properties": "多用"},
            {"name": "徒手打擊 (Unarmed Strike)", "type": "近戰徒手戰技", "damage": "1d4 (隨等級成長至 1d10) 鈍擊", "properties": "靈巧、附贈動作連擊"},
            {"name": "飛鏢 (Dart x10)", "type": "遠程簡易武器", "damage": "1d4 穿刺", "properties": "靈巧、投擲 (20/60)"},
            {"name": "無甲身法 (Unarmored Defense)", "type": "身法防禦", "ac": "10 + 敏捷調整值 + 感知調整值", "properties": "身無寸甲但步伐鬼魅"}
        ],
        "features_by_level": {
            1: ["無甲防禦 (Unarmored Defense)", "武藝 (Martial Arts: 敏捷徒手打擊與附贈連擊)"],
            2: ["氣能量 (Ki: 疾風連擊、護身勁、踏風步)", "無甲移動 (Unarmored Movement: 移速 +10 呎)"],
            3: ["修道院修習 (Monastic Tradition)", "截擊飛矢 (Deflect Missiles: 反應動作接擋遠程彈丸)"],
            4: ["慢速降落 (Slow Fall)"],
            5: ["額外攻擊 (Extra Attack)", "震懾拳 (Stunning Strike: 命中時消耗氣使目標震懾)"],
            6: ["真氣打擊 (Ki-Empowered Strikes: 徒手視為魔法武器)"],
            7: ["反射閃避 (Evasion)", "心如止水 (Stillness of Mind: 驅散魅惑與恐慌)"],
            14: ["金剛魂魄 (Diamond Body: 獲得全豁免熟練項)"],
            18: ["空靈之軀 (Empty Body: 隱形與傷害抗性)"],
            20: ["超越自我 (Perfect Self)"]
        }
    },
    "遊俠 (Ranger)": {
        "hit_die": "d10",
        "primary_recommendation": "主屬性建議配置：【敏捷】（箭術與身手）與【感知】（野外偵察與自然神術），副屬性【體質】。",
        "saves": ["力量 (STR)", "敏捷 (DEX)"],
        "is_spellcaster": True,
        "spell_type": "半施法者 (Half Caster: 2級開始獲得法術位)",
        "default_equipment": [
            {"name": "長弓 (Longbow)", "type": "遠程軍用武器", "damage": "1d8 穿刺", "properties": "彈藥 (150/600)、重型、雙手"},
            {"name": "雙持短劍 (Shortsword x2)", "type": "近戰軍用武器", "damage": "1d6 穿刺", "properties": "靈巧、輕型"},
            {"name": "鱗甲 (Scale Mail)", "type": "中甲", "ac": "14 + 敏捷調整值 (上限+2)", "properties": "荒野巡林防護"},
            {"name": "箭袋 (Quiver x20 支箭)", "type": "彈藥裝備", "damage": "—", "properties": "荒野追獵裝備"}
        ],
        "features_by_level": {
            1: ["宿敵 (Favored Enemy: 追蹤與知識優勢)", "自然探索者 (Natural Explorer: 荒野地貌適應與領航優勢)"],
            2: ["戰鬥風格 (Fighting Style: 箭術、對決、雙武器)", "遊俠施法能力 (Spellcasting)"],
            3: ["遊俠原型 (Ranger Archetype)", "原始感知 (Primeval Awareness)"],
            5: ["額外攻擊 (Extra Attack: 每次攻擊動作可射/砍 2 次)"],
            8: ["大地行者 (Land's Stride: 穿過非魔法險惡地形不降速)"],
            10: ["自然掩蔽 (Hide in Plain Sight)"],
            14: ["匿跡消失 (Vanish: 附贈動作執行隱匿)"],
            18: ["野性知覺 (Feral Senses)"],
            20: ["屠敵斬擊 (Foe Slayer)"]
        }
    },
    "術士 (Sorcerer)": {
        "hit_die": "d6",
        "primary_recommendation": "主屬性建議配置：【魅力】（體內天生術法源泉），副屬性【體質】（法術專注與生命）與【敏捷】（防禦）。",
        "saves": ["體質 (CON)", "魅力 (CHA)"],
        "is_spellcaster": True,
        "spell_type": "全施法者 (Full Caster)",
        "default_equipment": [
            {"name": "輕弩 (Light Crossbow)", "type": "遠程簡易武器", "damage": "1d8 穿刺", "properties": "彈藥 (80/320)、裝填、雙手"},
            {"name": "匕首 (Dagger x2)", "type": "近戰簡易武器", "damage": "1d4 穿刺", "properties": "靈巧、輕型、投擲 (20/60)"},
            {"name": "奧術法器結晶 (Arcane Focus Crystal)", "type": "施法媒介", "damage": "—", "properties": "引導體內原生魔力"},
            {"name": "無甲旅者便服 (Traveler's Clothes)", "type": "常規服飾", "ac": "10 + 敏捷調整值", "properties": "依靠法術防護"}
        ],
        "features_by_level": {
            1: ["術法施法 (Spellcasting)", "術法起源 (Sorcerous Origin)"],
            2: ["法術之泉 (Font of Magic: 術法點數 Sorcery Points，轉化法術位)"],
            3: ["超魔技巧 (Metamagic: 瞬發、強效、延長、細微法術等)"],
            4: ["屬性值提升 (ASI)"],
            10: ["額外超魔技巧 (Additional Metamagic)"],
            17: ["超魔大師 (第四項超魔技巧)"],
            20: ["術法復甦 (Sorcerous Restoration)"]
        }
    },
    "契術師 (Warlock)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【魅力】（與宗主交涉與邪術衝擊），副屬性【體質】（專注與生存）與【敏捷】（護甲AC）。",
        "saves": ["感知 (WIS)", "魅力 (CHA)"],
        "is_spellcaster": True,
        "spell_type": "契約施法者 (Pact Magic: 法術位極少但短休完全回滿且永遠最高環階)",
        "default_equipment": [
            {"name": "魔能震爆法器 (Arcane Focus Rod)", "type": "魔能法器", "damage": "—", "properties": "引導邪術衝擊 (Eldritch Blast) 專用"},
            {"name": "短劍 (Shortsword)", "type": "近戰軍用武器", "damage": "1d6 穿刺", "properties": "靈巧、輕型"},
            {"name": "皮甲 (Leather Armor)", "type": "輕甲", "ac": "11 + 敏捷調整值", "properties": "靈巧防護"},
            {"name": "學者背包 (Scholar's Pack)", "type": "日常行囊", "damage": "—", "properties": "記載密契契約文書"}
        ],
        "features_by_level": {
            1: ["異界宗主 (Otherworldly Patron)", "契約施法 (Pact Magic)"],
            2: ["魔能祈喚 (Eldritch Invocations: 苦痛魔爆、魔能視界、護甲陰影等特異能力)"],
            3: ["契約饋贈 (Pact Boon: 刃之契、書之契、鏈之契、魔符之契)"],
            11: ["秘奧秘法 (Mystic Arcanum: 每日 1 次 6 環法術)"],
            13: ["秘奧秘法 (7 環法術)"],
            15: ["秘奧秘法 (8 環法術)"],
            17: ["秘奧秘法 (9 環法術)"],
            20: ["魔能大師 (Eldritch Master: 乞求宗主 1 分鐘回滿契約法術位)"]
        }
    },
    "奇械師 (Artificer)": {
        "hit_die": "d8",
        "primary_recommendation": "主屬性建議配置：【智力】（發明造物與奧術發明核心），副屬性【體質】與【敏捷/力量】。",
        "saves": ["體質 (CON)", "智力 (INT)"],
        "is_spellcaster": True,
        "spell_type": "半施法者 (Artificer Spellcasting: 1級即具備法術位)",
        "default_equipment": [
            {"name": "手弩 (Hand Crossbow)", "type": "遠程軍用武器", "damage": "1d6 穿刺", "properties": "彈藥 (30/120)、輕型、裝填"},
            {"name": "工匠工具組 (Thieves' Tools / Tinker's Tools)", "type": "核心發明工具", "damage": "—", "properties": "施展法術與注法必備"},
            {"name": "鑲嵌皮甲 (Studded Leather)", "type": "輕甲", "ac": "12 + 敏捷調整值", "properties": "鉚釘加固工匠甲"},
            {"name": "多功能扳手錘 (Light Hammer)", "type": "簡易近戰武器", "damage": "1d4 鈍擊", "properties": "輕型、投擲 (20/60)"}
        ],
        "features_by_level": {
            1: ["奇械施法 (Magical Tinkering: 賦予微型魔法特效)", "法術施展 (Spellcasting)"],
            2: ["注入魔法物品 (Infuse Item: 製造發明魔法武器/護甲/發明裝備)"],
            3: ["專業領域 (Artificer Specialist)", "得心應手 (The Right Tool for the Job)"],
            6: ["工具專精 (Tool Expertise: 工具檢定熟練翻倍)"],
            7: ["天才閃光 (Flash of Genius: 反應動作為檢定/豁免加上智力調整值)"],
            10: ["魔法物品大師 (Magic Item Adept: 調諧 4 件魔法物品)"],
            14: ["魔法物品狂熱者 (Magic Item Savant: 調諧 5 件魔法物品)"],
            18: ["魔法物品大師 (Magic Item Master: 調諧 6 件魔法物品)"],
            20: ["靈魂化身 (Soul of Artifice: 每調諧一件物品豁免 +1，HP歸零時消耗充能免死)"]
        }
    }
}

# ==========================================
# 4. 子職業 / 範型系統 (Subclasses / Paradigms)
# ==========================================
SUBCLASSES = {
    "戰士 (Fighter)": {
        "category": "武藝範型 (Martial Archetype)",
        "unlock_level": 3,
        "options": {
            "勇士 (Champion)": {
                "desc": "專注於肉體極限力量與致命暴擊，將體能磨練至登峰造極。",
                "features_by_level": {
                    3: ["精通重擊 (Improved Critical: 攻擊擲骰 19~20 皆為重擊)"],
                    7: ["卓越運動身手 (Remarkable Athlete: 力量敏捷體質檢定半數PB加成)"],
                    10: ["額外戰鬥風格 (Additional Fighting Style)"],
                    15: ["高等重擊 (Superior Critical: 18~20 皆為重擊)"],
                    18: ["生生不息 (Survivor: 戰鬥中每回合恢復生命)"]
                }
            },
            "戰鬥大師 (Battle Master)": {
                "desc": "將戰鬥視為精密軍事學問，掌握卓越骰與戰術機動戰策。",
                "features_by_level": {
                    3: ["戰鬥卓越 (Combat Superiority: 4 顆 d8 卓越骰)", "戰術戰策 (繳械打擊、拌摔、推撞、招架、指揮官命令)"],
                    7: ["知己知彼 (Know Your Enemy: 評估對手攻防體魄)"],
                    10: ["卓越骰升級為 d10"],
                    15: ["卓越骰增至 6 顆"],
                    18: ["卓越骰升級為 d12"]
                }
            },
            "魔能騎士 (Eldritch Knight)": {
                "desc": "融合近戰戰法與塑能/防護系奧術，以魔力加持武器與刀刃。",
                "features_by_level": {
                    3: ["武器誓約 (Weapon Bond: 絕不繳械且可瞬間召回武器)", "奧術施法 (塑能與防護學派)"],
                    7: ["戰法相融 (War Magic: 施展戲法後可附贈動作發動武器攻擊)"],
                    10: ["魔能力竭 (Eldritch Strike)"],
                    15: ["奧術衝刺 (Arcane Charge)"],
                    18: ["改良戰法相融 (Improved War Magic)"]
                }
            },
            "武士 (Samurai)": {
                "desc": "以不屈意志與武士道精神克敵，燃燒鬥志發動連環爆發斬擊。",
                "features_by_level": {
                    3: ["戰鬥鬥志 (Fighting Spirit: 附贈動作使當回合攻擊皆具優勢並獲得臨時 HP)"],
                    7: ["優雅廷臣 (Elegant Courtier: 說服檢定附加感知加成)"],
                    10: ["不滅鬥志 (Tireless Spirit)"],
                    15: ["疾風斬擊 (Rapid Strike)"],
                    18: ["孤注一擲 (Strength Before Death)"]
                }
            },
            "符文騎士 (Rune Knight)": {
                "desc": "掌握遠古巨人符文秘法，能在戰場巨大化為大型戰將。",
                "features_by_level": {
                    3: ["符文刻印 (火/霜/石/雲符文特效)", "巨人身形 (Giant's Might: 化身大型生物，命中附加傷害)"],
                    7: ["防禦符文盾 (Runic Shield: 反應動作迫使重骰攻擊)"],
                    10: ["巨人之軀 (Great Stature)"],
                    15: ["大師刻印 (Master of Runes)"],
                    18: ["符文半神 (Runic Juggernaut)"]
                }
            },
            "回音騎士 (Echo Knight)": {
                "desc": "操縱時間與命運虛影，召喚平行時空的回音化身夾擊強敵。",
                "features_by_level": {
                    3: ["顯現回音 (Manifest Echo: 召喚回音幻象位移並自幻影位置攻擊)", "深潛回音 (Unleash Incarnation)"],
                    7: ["回音斥候 (Echo Avatar)"],
                    10: ["暗影護衛 (Shadow Martyr)"],
                    15: ["回音重構 (Reclaim Potential)"],
                    18: ["雙重回音 (Legion of One)"]
                }
            },
            "靈能武士 (Psi Warrior)": {
                "desc": "以心靈靈能念力注入兵器，發動念力投擲與力場護盾。",
                "features_by_level": {
                    3: ["靈能力場 (Psionic Power: 靈能骰)", "護衛心盾 (Protective Field)", "念力打擊 (Psionic Strike)"],
                    7: ["念力躍動 (Telekinetic Movement)"],
                    10: ["靈能防禦 (Guarded Mind)"],
                    15: ["意志推撞 (Bulwark of Force)"],
                    18: ["念力風暴 (Telekinetic Master)"]
                }
            },
            "騎兵 (Cavalier)": {
                "desc": "戰場上的鋼鐵壁壘與坐騎守護者，專精嘲諷控場保護盟友。",
                "features_by_level": {
                    3: ["生來馬背 (Born to the Saddle)", "未動先知 (Unwavering Mark: 標記敵人限制其攻擊盟友)"],
                    7: ["堅毅護衛 (Warding Maneuver)"],
                    10: ["固若金湯 (Hold the Line)"],
                    15: ["兇猛奔襲 (Ferocious Charger)"],
                    18: ["防禦警戒 (Vigilant Defender)"]
                }
            },
            "魔射手 (Arcane Archer)": {
                "desc": "精靈流傳的精湛箭術，將奧術能量注入箭鏃引爆奇效。",
                "features_by_level": {
                    3: ["奧術箭術 (Arcane Shot: 破魔箭、爆裂箭、糾纏箭等奇效)", "魔箭專家"],
                    7: ["魔法箭鏃 (Magic Arrow)", "折射弧箭 (Curving Shot)"],
                    15: ["連環魔箭 (Ever-Ready Shot)"]
                }
            },
            "紫龍騎士 (Purple Dragon Knight)": {
                "desc": "恪守騎士精神的部隊領袖，以鼓舞戰吼強化士氣與治癒盟友。",
                "features_by_level": {
                    3: ["號令重整 (Rallying Cry: 使用回氣時同時治癒 3 名盟友)"],
                    7: ["領軍使節 (Royal Envoy)"],
                    10: ["鼓舞突擊 (Inspiring Surge)"],
                    15: ["堅毅同盟 (Bulwark)"]
                }
            }
        }
    },
    "法師 (Wizard)": {
        "category": "奧術傳承 (Arcane Tradition)",
        "unlock_level": 2,
        "options": {
            "塑能學派 (School of Evocation)": {
                "desc": "掌握毀滅性元素能量，並能精準調控範圍讓盟友免受法術傷害。",
                "features_by_level": {
                    2: ["塑能學者 (Evocation Savant)", "法術塑形 (Sculpt Spells: 範圍法術自動避開盟友)"],
                    6: ["強效戲法 (Potent Cantrip: 豁免成功亦受半數傷害)"],
                    10: ["強效塑能 (Empowered Evocation: 傷害加入智力調整值)"],
                    14: ["超限施法 (Overchannel: 1~5環法術傷害骰直接取最大值)"]
                }
            },
            "防護學派 (School of Abjuration)": {
                "desc": "專精結界與護盾防禦，編織奧術結界吸收一切迎面而來的打擊。",
                "features_by_level": {
                    2: ["防護學者 (Abjuration Savant)", "秘法結界 (Arcane Ward: 生成獨立生命護盾吸收傷害)"],
                    6: ["投射結界 (Projected Ward: 為周遭盟友承受打擊)"],
                    10: ["改良破術 (Improved Abjuration: 反制與解除魔法檢定附加 PB)"],
                    14: ["法術抗性 (Spell Resistance: 對所有法術豁免具備優勢並獲法術抗性)"]
                }
            },
            "咒法學派 (School of Conjuration)": {
                "desc": "召喚異界生物與物品，並掌握瞬息位移的空間技巧。",
                "features_by_level": {
                    2: ["微型造物 (Minor Conjuration: 憑空憑想像召喚無生命物件)"],
                    6: ["良性換位 (Benign Transposition: 瞬間傳送或與自願盟友換位)"],
                    10: ["專注召喚 (Focused Conjuration: 咒法專注絕不因受傷中斷)"],
                    14: ["耐久召喚 (Durable Summons)"]
                }
            },
            "死靈學派 (School of Necromancy)": {
                "desc": "洞悉生與死的循環界限，操縱不死生物僕從並汲取敵人生機。",
                "features_by_level": {
                    2: ["冷酷收割 (Grim Harvest: 擊殺敵人時汲取生命回覆自身 HP)"],
                    6: ["亡者操戈 (Undead Thralls: 操縱死屍額外召喚僕從且生命與命中大幅提升)"],
                    10: ["不死抗性 (Inured to Undeath: 免疫生命上限降低效應)"],
                    14: ["敕令亡靈 (Command Undead: 強制控制敵方強大不死生物)"]
                }
            },
            "預言學派 (School of Divination)": {
                "desc": "窺視時空命運因果，以預兆之骰直接篡改攻擊與豁免結果。",
                "features_by_level": {
                    2: ["預兆 (Portent: 長休擲 2 顆 d20，白天可直接替換任意檢定結果)"],
                    6: ["洞察施法 (Expert Divination: 施展預言法術可返還低環法術位)"],
                    10: ["天眼通 (The Third Eye: 獲得黑暗視覺、以太視覺或破除隱形能力)"],
                    14: ["至高預兆 (Greater Portent: 每日擁有 3 顆預兆骰)"]
                }
            },
            "惑控學派 (School of Enchantment)": {
                "desc": "玩弄心智與意志，以眼神催眠敵人並使其互相殘殺。",
                "features_by_level": {
                    2: ["凝視催眠 (Hypnotic Gaze: 眼神凝視癱瘓近身敵人行動)"],
                    6: ["本能移情 (Instinctive Charm: 被攻擊時反彈給身旁敵人)"],
                    10: ["分裂惑控 (Split Enchantment: 單體惑控法術自動分裂為雙重目標)"],
                    14: ["心靈篡改 (Alter Memories)"]
                }
            },
            "幻術學派 (School of Illusion)": {
                "desc": "編織虛妄光影，最終甚至能讓幻象短暫轉化為實體造物。",
                "features_by_level": {
                    2: ["改良幻術 (Improved Minor Illusion: 戲法同時發出聲音與影像)"],
                    6: ["虛妄易位 (Malleable Illusions: 動態調整現存幻象內容)"],
                    10: ["幻影雙身 (Illusory Self: 反應動作以幻影替死完全規避一次攻擊)"],
                    14: ["幻化成真 (Illusory Reality: 讓無害幻象在 1 分鐘內化為真實實體)"]
                }
            },
            "變化學派 (School of Transmutation)": {
                "desc": "操縱物質形態，持有變化之石賦予抗性或治癒傷痛。",
                "features_by_level": {
                    2: ["物質暫變 (Minor Alchemy: 短暫改變木/鐵/石等材料形態)"],
                    6: ["賢者之石 (Transmuter's Stone: 賦予體質豁免熟練或黑暗視覺)"],
                    10: ["自我變身 (Shapechanger: 隨意施展變形術把自己化身野獸)"],
                    14: ["終極變化 (Master Transmuter: 消耗石頭完全治癒疾病或死者甦生)"]
                }
            },
            "劍詠傳承 (Bladesinging)": {
                "desc": "精靈秘傳戰技，在優雅劍詠步伐中揮舞細劍並施展致命奧術。",
                "features_by_level": {
                    2: ["劍詠步 (Bladesong: 移速增加、AC與專注檢定附加智力調整值)"],
                    6: ["額外攻擊 (Extra Attack: 可將其中一次攻擊替換為奧術戲法)"],
                    10: ["詠歌之歌 (Song of Defense: 消耗法術位吸收傷害)"],
                    14: ["勝利之歌 (Song of Victory: 武器傷害加入智力調整值)"]
                }
            },
            "戰爭魔法 (War Magic)": {
                "desc": "軍隊戰法師的實戰法門，兼具迅捷先攻與堅固的奧術偏轉護盾。",
                "features_by_level": {
                    2: ["奧術偏轉 (Arcane Deflection: 反應動作提升 AC 或豁免加值)", "戰略先攻 (先攻附加智力加成)"],
                    6: ["能量湧潮 (Power Surge: 成功反制法術時充能額外力場傷害)"],
                    10: ["持久魔法 (Durable Magic: 維持專注時 AC 與全豁免 +2)"],
                    14: ["偏折帷幕 (Deflecting Shroud)"]
                }
            },
            "時間魔法 (Chronurgy Magic)": {
                "desc": "扭曲時光洪流，迫使時間倒流或將法術封裝入時光懸凝晶珠。",
                "features_by_level": {
                    2: ["時光倒流 (Chronal Shift: 每日 2 次迫使剛完成的擲骰強制重擲)"],
                    6: ["時光凝滯 (Temporal Stasis: 將生物暫時凍結在時間夾縫中)"],
                    10: ["奧術封珠 (Arcane Abeyance: 將 4 環以下法術封裝成晶珠由盟友觸發)"],
                    14: ["命運同調 (Convergent Future)"]
                }
            },
            "書士會 (Order of Scribes)": {
                "desc": "與活化法術書建立心靈契約，可任意變更法術傷害屬性元素。",
                "features_by_level": {
                    2: ["活化法術書 (Wizardly Quill & Awakened Book: 任意替換法術傷害類型)"],
                    6: ["法術卷軸製造 (Master Scrivener)"],
                    10: ["靈魂投影 (Manifest Mind: 投射法術書的心靈意識替身施法)"],
                    14: ["生命筆錄 (One with the Word)"]
                }
            }
        }
    },
    "遊盪者 (Rogue)": {
        "category": "盜賊範型 (Roguish Archetype)",
        "unlock_level": 3,
        "options": {
            "刺客 (Assassin)": {
                "desc": "致命毒藥與伏擊刺殺專家，在突襲中必定發動毀滅性重擊。",
                "features_by_level": {
                    3: ["刺殺 (Assassinate: 對未行動目標攻擊具優勢，突襲命中必定重擊)", "製毒與偽裝工具熟練"],
                    9: ["偽裝滲透 (Infiltration Expertise: 完美偽造虛假身分文書)"],
                    13: ["冒名頂替 (Impostor: 完美模仿他人嗓音筆跡神態)"],
                    17: ["奪命打擊 (Death Strike: 突襲重擊命中造成雙倍致命傷害)"]
                }
            },
            "竊賊 (Thief)": {
                "desc": "屋頂飛賊與開鎖巧匠，具備超凡攀爬身手與盜用魔法道具能力。",
                "features_by_level": {
                    3: ["快手巧技 (Fast Hands: 附贈動作開鎖、拆陷阱或使用物品)", "飛簷走壁 (Second-Story Work: 攀爬不消耗額外移動)"],
                    9: ["至高潛行 (Supreme Sneak: 隱匿檢定具備優勢)"],
                    13: ["盜用魔法物品 (Use Magic Device: 無視職業、種族、等級調諧使用任何魔法物品)"],
                    17: ["盜賊反射 (Thief's Reflexes: 戰鬥首輪可行動 2 次)"]
                }
            },
            "詭術師 (Arcane Trickster)": {
                "desc": "將盜賊的潛行與幻術/惑控奧術融會貫通，操控隱形法師之手竊取物品。",
                "features_by_level": {
                    3: ["法師之手巧藝 (Mage Hand Legerdemain: 隱形法師之手開鎖扒竊)", "奧術施法 (幻術與惑控)"],
                    9: ["魔法伏擊 (Magical Ambush: 隱蔽狀態施法使目標豁免處於劣勢)"],
                    13: ["多才詭計 (Versatile Trickster)"],
                    17: ["法術竊賊 (Spell Thief: 反應動作奪取並封印敵人的法術)"]
                }
            },
            "風流劍客 (Swashbuckler)": {
                "desc": "優雅瀟灑的決鬥家，無需盟友夾擊即可單挑發動偷襲。",
                "features_by_level": {
                    3: ["華麗步伐 (Fancy Footwork: 近戰打擊後直接安全撤離免受藉機攻擊)", "豪俠氣概 (Rakish Audacity: 先攻加魅力，單挑自帶偷襲)"],
                    9: ["圓滑嘲弄 (Panache: 戰鬥中以魅力挑釁敵方強制其攻擊自身)"],
                    13: ["飄逸身段 (Elegant Maneuver)"],
                    17: ["絕境反擊 (Master Duelist)"]
                }
            },
            "魂刃 (Soulknife)": {
                "desc": "以心靈靈能原力凝聚心靈飛刃，千里傳心並百發百中。",
                "features_by_level": {
                    3: ["靈能心靈刃 (Psychic Blades: 憑空凝聚純心靈傷害飛刃)", "心靈通訊 (Psychic Telepathy)"],
                    9: ["靈能跳躍 (Soul Blades)"],
                    13: ["心靈帷幕 (Psychic Veil: 隱形持續 1 小時)"],
                    17: ["摧毀心智 (Rend Mind)"]
                }
            },
            "斥候 (Scout)": {
                "desc": "荒野追蹤者與斥候哨兵，在敵人逼近時能以反應動作迅速拉開距離。",
                "features_by_level": {
                    3: ["突圍遊擊 (Skirmisher: 敵人靠近時反應動作移動半速且不受藉機攻擊)", "求生與自然熟練加倍"],
                    9: ["高等機動 (Superior Mobility: 步行移速 +10 呎)"],
                    13: ["伏擊高手 (Ambush Master: 首輪先攻優勢並為盟友帶來攻擊優勢)"],
                    17: ["突擊打擊 (Sudden Strike: 附贈動作對另一目標再發動一次偷襲)"]
                }
            },
            "審訊者 (Inquisitive)": {
                "desc": "洞察人心的偵探，一眼識破謊言並能精準鎖定敵方弱點發動偷襲。",
                "features_by_level": {
                    3: ["識破謊言 (Ear for Deceit: 洞察檢定保底 8 點以上)", "洞悉弱點 (Insightful Fighting: 洞察檢定鎖定敵方弱點)"],
                    9: ["明察秋毫 (Eye for Detail)"],
                    13: ["堅定眼神 (Unerring Eye: 感知 30 呎內幻象與變形生物)"],
                    17: ["弱點重創 (Eye for Weakness)"]
                }
            },
            "策士 (Mastermind)": {
                "desc": "幕後謀士與情報大師，能以附贈動作在 30 呎外指揮協助盟友發動攻擊。",
                "features_by_level": {
                    3: ["謀士之策 (Master of Intrigue)", "遠距協助 (Master of Tactics: 附贈動作在 30 呎遠協助盟友)"],
                    9: ["洞悉動機 (Insightful Manipulator)"],
                    13: ["移花接木 (Misdirection: 被攻擊時拉攏掩體生物替死)"],
                    17: ["心靈壁壘 (Soul of Deceit)"]
                }
            },
            "鬼魅 (Phantom)": {
                "desc": "行走於生死界限的死靈盜賊，能收集亡魂靈片並將死者怨念化為傷害。",
                "features_by_level": {
                    3: ["亡者微語 (Whispers of the Dead)", "幽靈哀鳴 (Wails from the Grave: 偷襲時死者怨念重創第二目標)"],
                    9: ["死者靈片 (Tokens of the Departed: 收集亡魂水晶充能)"],
                    13: ["幽魂之軀 (Ghost Walk: 化身幽靈懸浮穿牆)"],
                    17: ["死神之友 (Death's Friend)"]
                }
            }
        }
    },
    "牧師 (Cleric)": {
        "category": "神聖領域 (Divine Domain)",
        "unlock_level": 1,
        "options": {
            "生命領域 (Life Domain)": {
                "desc": "奉獻於治癒與生命守護，其治療神術受到神恩額外強化增益。",
                "features_by_level": {
                    1: ["重甲熟練 (Bonus Proficiency)", "生命門徒 (Disciple of Life: 治療法術額外回覆 2 + 環階 HP)"],
                    2: ["引導神力：維生光環 (Preserve Life: 大範圍群體治療受創盟友)"],
                    6: ["福佑生靈 (Blessed Healer: 治療他人時自身同享回血)"],
                    8: ["神聖打擊 (Divine Strike: 近戰命中附加 1d8 光耀傷害)"],
                    17: ["至高治癒 (Supreme Healing: 治療骰直接取滿值不用擲)"]
                }
            },
            "光明領域 (Light Domain)": {
                "desc": "引導熾熱純淨烈陽真火，以致盲光耀反制來犯者並降下烈焰火球。",
                "features_by_level": {
                    1: ["守護耀光 (Warding Flare: 反應動作爆發強光迫使敵人攻擊處於劣勢)"],
                    2: ["引導神力：黎明破曉 (Radiance of the Dawn: 驅散黑暗並造成大範圍光耀傷害)"],
                    6: ["改良守護耀光 (可守護周遭盟友)"],
                    8: ["強效神聖戲法 (Potent Spellcasting: 戲法傷害附加感知調整值)"],
                    17: ["日輪光環 (Corona of Light: 周身 60 呎籠罩陽光領域)"]
                }
            },
            "戰爭領域 (War Domain)": {
                "desc": "戰神的高階司祭，披掛全套重甲揮舞戰錘，以神力引導必中打擊。",
                "features_by_level": {
                    1: ["重甲與軍用武器熟練", "戰神狂怒 (War Priest: 攻擊後以附贈動作發動額外近戰攻擊)"],
                    2: ["引導神力：精準打擊 (Guided Strike: 攻擊擲骰獲得 +10 命中神聖加值)"],
                    6: ["引導神力：戰神祝福 (為盟友提供 +10 攻擊命中加成)"],
                    8: ["神聖打擊 (Divine Strike: 近戰附加 1d8 額外武器傷害)"],
                    17: ["鋼鐵化身 (Avatar of Battle: 獲得鈍刺斬非魔法傷害抗性)"]
                }
            },
            "暴風領域 (Tempest Domain)": {
                "desc": "掌控狂雷與風暴之威，每逢引導神力必降下最大極限雷霆閃電。",
                "features_by_level": {
                    1: ["重甲與軍用武器熟練", "暴怒狂雷 (Wrath of the Storm: 被擊中時反應動作反震雷電傷害)"],
                    2: ["引導神力：破滅風暴 (Destructive Wrath: 雷電傷害骰直接取最大滿值)"],
                    6: ["雷電斥退 (Thunderbolt Strike: 造成雷電傷害時震飛敵人 10 呎)"],
                    8: ["神聖打擊 (Divine Strike: 命中附加 1d8 雷鳴傷害)"],
                    17: ["風暴之子 (Stormborn: 在露天室外獲得常態飛行能力)"]
                }
            },
            "詭術領域 (Trickery Domain)": {
                "desc": "信奉惡作劇與陰影欺瞞之神，投射無暇幻影分身迷惑世人視線。",
                "features_by_level": {
                    1: ["詭術祝福 (Blessing of the Trickster: 賦予盟友隱匿檢定優勢)"],
                    2: ["引導神力：幻影分身 (Invoke Duplicity: 召喚完美幻影替身並自替身位置施法)"],
                    6: ["引導神力：隱形斗篷 (Cloak of Shadows: 瞬間隱形至下回合結束)"],
                    8: ["神聖打擊 (Divine Strike: 命中附加 1d8 毒素傷害)"],
                    17: ["四重幻影 (Improved Duplicity: 一口氣召喚 4 具幻影替身)"]
                }
            },
            "知識領域 (Knowledge Domain)": {
                "desc": "古老圖書館與知識神祇的忠僕，能瞬間通曉任何語言技能與讀心術。",
                "features_by_level": {
                    1: ["博學祝福 (Blessings of Knowledge: 2項知識技能熟練翻倍並通曉2種語言)"],
                    2: ["引導神力：往昔知識 (Knowledge of the Ages: 瞬間短暫精通任意工具或技能)"],
                    6: ["引導神力：讀心術 (Read Thoughts: 讀取心智並強制下達心靈暗示)"],
                    8: ["強效神聖戲法 (Potent Spellcasting)"],
                    17: ["時光回溯洞察 (Visions of the Past)"]
                }
            },
            "墳墓領域 (Grave Domain)": {
                "desc": "維護死生分界的死神使者，剝奪垂死痛苦並能標記敵人使其承受雙倍重創。",
                "features_by_level": {
                    1: ["冥界圓環 (Circle of Mortality: 救治 HP 歸零生物時治療骰直接取滿值)", "感知亡魂"],
                    2: ["引導神力：亡魂之門 (Path to the Grave: 詛咒敵人使其下次受擊傷害翻倍)"],
                    6: ["護衛幽冥 (Sentinel at Death's Door: 反應動作取消敵人對盟友的重擊暴擊)"],
                    8: ["強效神聖戲法 (Potent Spellcasting)"],
                    17: ["生命汲取 (Keeper of Souls: 敵人死亡時將其生機轉移給受創盟友)"]
                }
            },
            "鍛造領域 (Forge Domain)": {
                "desc": "矮人造物主與鍛爐的祭司，身著金剛重甲並能在休息時點石成兵。",
                "features_by_level": {
                    1: ["重甲與鐵匠工具熟練", "鍛爐祝福 (Blessing of the Forge: 賦予武器或護甲 +1 魔法加值)"],
                    2: ["引導神力：造物工藝 (Artisan's Blessing: 祈禱儀式將金屬直接煉造成裝備)"],
                    6: ["鍛爐之魂 (Soul of the Forge: 獲得火焰抗性，著重甲時 AC 額外 +1)"],
                    8: ["神聖打擊 (Divine Strike: 命中附加 1d8 火焰傷害)"],
                    17: ["聖火聖徒 (Saint of Forge and Fire: 完全免疫火焰，著重甲時鈍刺斬非魔法抗性)"]
                }
            },
            "暮光領域 (Twilight Domain)": {
                "desc": "夜幕星光與撫慰微光的司祭，展開星光帷幕驅散恐慌並賦予全隊臨時生命。",
                "features_by_level": {
                    1: ["重甲與軍用武器熟練", "超遠黑暗視覺 (300呎超遠視界並可分享給隊友)"],
                    2: ["引導神力：暮光庇護 (Twilight Sanctuary: 展開星光結界每回合給予臨時 HP 或解恐)"],
                    6: ["夜空飛行 (Steps of Night: 在微光或黑暗中獲得飛行能力)"],
                    8: ["神聖打擊 (Divine Strike)"],
                    17: ["暮光帷幕 (Twilight Shroud: 結界內全隊獲得半掩護 +2 AC)"]
                }
            },
            "和平領域 (Peace Domain)": {
                "desc": "化解紛爭與串聯靈魂同盟的和平使徒，以和平羈絆讓全隊共享骰運與替傷。",
                "features_by_level": {
                    1: ["和平羈絆 (Emboldening Bond: 連結盟友，檢定與攻擊每回合可額外加 d4)"],
                    2: ["引導神力：和平之香 (Balm of Peace: 穿梭戰場不引發藉機攻擊並治癒全隊)"],
                    6: ["守護保護 (Protective Bond: 羈絆盟友可瞬間傳送替受傷盟友承受打擊)"],
                    8: ["強效神聖戲法 (Potent Spellcasting)"],
                    17: ["至高同盟 (Expansive Bond: 替傷時傷害減半)"]
                }
            }
        }
    },
    "德魯伊 (Druid)": {
        "category": "德魯伊結社 (Druid Circle)",
        "unlock_level": 2,
        "options": {
            "大地結社 (Circle of the Land)": {
                "desc": "守護遠古自然知識與大地魔力，冥想短休回覆法術位並通曉特定地貌神術。",
                "features_by_level": {
                    2: ["額外戲法", "自然回想 (Natural Recovery: 短休恢復部分消耗法術位)"],
                    3: ["結社地貌法術 (北極、海岸、沙漠、森林、草原、高山、沼澤或幽暗地域)"],
                    6: ["大地行者 (Land's Stride: 穿過非魔法地形不降速無傷)"],
                    10: ["自然聖衛 (Nature's Ward: 免疫毒素/疾病，免疫妖精與元素恐慌魅惑)"],
                    14: ["自然避難 (Nature's Sanctuary: 野獸與植物攻擊前須通過感知豁免)"]
                }
            },
            "月亮結社 (Circle of the Moon)": {
                "desc": "狂野變形大師，以附贈動作化身兇暴猛獸、巨熊甚至強大的四元素長老。",
                "features_by_level": {
                    2: ["戰鬥荒野形態 (Combat Wild Shape: 附贈動作化身且可消耗法術位回血)", "月光形態 (解鎖高 CR 猛獸)"],
                    6: ["狂野打擊 (Primal Strike: 荒野野獸形態徒手視為魔法武器)"],
                    10: ["元素荒野形態 (Elemental Wild Shape: 消耗 2 次形態化身火/水/土/風元素長老)"],
                    14: ["千面之客 (Thousand Forms: 隨意施展變顏術)"]
                }
            },
            "夢境結社 (Circle of Dreams)": {
                "desc": "深諳妖精荒野夢境力量的德魯伊，撫平身心創傷並引導夢境位移。",
                "features_by_level": {
                    2: ["夏日香膏 (Balm of the Summer Court: 充能生機池，以附贈動作遠程撫慰治癒)"],
                    6: ["月光之爐 (Hearth of Moonlight and Shadow: 休息時張開隱匿結界掩蔽全隊)"],
                    10: ["夢境漫步 (Hidden Paths: 附贈動作瞬移傳送或傳送盟友)"],
                    14: ["夢境漫遊 (Dreamwalker)"]
                }
            },
            "牧人結社 (Circle of the Shepherd)": {
                "desc": "荒野萬獸之靈的守護者，通曉獸語並召喚熊/鷹/獨角獸圖騰靈光庇護全隊。",
                "features_by_level": {
                    2: ["森林之語 (Speech of the Woods: 通曉木族語與動物交談)", "精神圖騰 (Spirit Totem: 熊/鷹/獨角獸光環強化全隊)"],
                    6: ["強韌召喚 (Mighty Summoner: 召喚野獸生命大幅提升且武器視為魔法)"],
                    10: ["守護獸靈 (Guardian Spirit: 圖騰光環內召喚生物每回合自動回血)"],
                    14: ["忠誠獸靈 (Faithful Summons)"]
                }
            },
            "孢子結社 (Circle of Spores)": {
                "desc": "洞悉真菌孢子與生死循環的死靈德魯伊，釋放劇毒孢子光環並復活孢子殭屍。",
                "features_by_level": {
                    2: ["光環孢子 (Halo of Spores: 敵人逼近時以反應動作引爆死靈孢子傷害)", "共生實體 (Symbiotic Entity: 消耗形態獲得巨額臨時生命並追加近戰傷害)"],
                    6: ["真菌感染 (Fungal Infestation: 敵人死亡時寄生化為孢子殭屍奴僕)"],
                    10: ["孢子擴散 (Spreading Spores: 將毒孢光環投擲至 30 呎戰場封鎖走道)"],
                    14: ["真菌之軀 (Fungal Body: 免疫目盲、耳聾、恐慌、中毒與重擊暴擊)"]
                }
            },
            "星辰結社 (Circle of Stars)": {
                "desc": "手持星圖占卜星宿奧秘的星辰德魯伊，引導弓箭手、巨杯或巨龍星座化身作戰。",
                "features_by_level": {
                    2: ["星圖 (Star Map: 獲導向飛彈與指引神術)", "星光形態 (Starry Form: 弓箭手光耀射線 / 巨杯群體治療 / 巨龍專注保底 10)"],
                    6: ["星宿預兆 (Cosmic Omen: 每日擲微光預兆為他人檢定加減 d6)"],
                    10: ["璀璨星宿 (Twinkling Constellations: 星光形態傷害與治療提升至 2d8)"],
                    14: ["群星之光 (Full of Stars: 星光形態下獲得鈍擊/穿刺/揮砍物理抗性)"]
                }
            },
            "野火結社 (Circle of Wildfire)": {
                "desc": "理解烈火焚林方有新生的自然循環，召喚活潑燃燒的野火之靈伴隨作戰。",
                "features_by_level": {
                    2: ["召喚野火之靈 (Summon Wildfire Spirit: 召喚火焰飛禽/小精靈，燃燒位移全隊)", "野火法術 (Wildfire Spells)"],
                    6: ["火之羈絆 (Enhanced Bond: 火焰與治療法術額外增加 1d8 骰值)"],
                    10: ["烈焰復甦 (Cauterizing Flames: 敵人倒下處綻放幽火，觸碰治療或灼燒)"],
                    14: ["烈火永生 (Blazing Revival: 瀕死倒地時野火之靈犧牲替死瞬間回血半數)"]
                }
            }
        }
    },
    "野蠻人 (Barbarian)": {
        "category": "原初本道 (Primal Path)",
        "unlock_level": 3,
        "options": {
            "狂戰士道途 (Path of the Berserker)": {
                "desc": "沉浸於純粹殺戮狂熱的狂戰士，在狂亂中以附贈動作瘋狂揮斧狂斬。",
                "features_by_level": {
                    3: ["狂暴狂亂 (Frenzy: 狂暴中每回合可以附贈動作額外發動一次近戰攻擊)"],
                    6: ["無腦狂暴 (Mindless Rage: 狂暴期間完全免疫魅惑與恐慌)"],
                    10: ["威嚇凝視 (Intimidating Presence: 怒吼恐嚇戰場敵人使其畏縮)"],
                    14: ["報復反擊 (Retaliation: 近戰受傷時以反應動作立即反擊一刀)"]
                }
            },
            "圖騰勇士道途 (Path of the Totem Warrior)": {
                "desc": "與自然靈獸精神同契，熊之強韌、鷹之銳眼或狼之群狩引導狂暴。",
                "features_by_level": {
                    3: ["圖騰之靈 (Totem Spirit: 熊圖騰獲得除心靈外全傷害抗性；狼圖騰給盟友優勢)"],
                    6: ["猛獸姿態 (Aspect of the Beast: 獲得熊之巨力負重或鷹之遠眺)"],
                    10: ["靈行者 (Spirit Walker: 施展共享自然感知神術)"],
                    14: ["圖騰協調 (Totemic Attunement)"]
                }
            },
            "狂野魔法道途 (Path of Wild Magic)": {
                "desc": "體內封存著失控的荒野混沌魔力，每次狂暴皆引發不可預測的隨機魔能狂潮。",
                "features_by_level": {
                    3: ["魔力感知 (Magic Awareness)", "狂野魔能爆發 (Wild Magic Surge: 狂暴時擲骰觸發射線/傳送/光芒等8種奇效)"],
                    6: ["灌注魔法 (Bolstering Presence: 骰 d3 為盟友恢復法術位或檢定加骰)"],
                    10: ["不穩定反衝 (Unstable Backlash: 受到傷害時迫使魔能狂潮重骰切換)"],
                    14: ["掌控混亂 (Controlled Surge)"]
                }
            },
            "狂熱者道途 (Path of the Zealot)": {
                "desc": "戰神或毀滅神祇的神聖狂信者，死後復生無需昂貴鑽石構材。",
                "features_by_level": {
                    3: ["神聖狂怒 (Divine Fury: 狂暴命中額外造成 1d6 + 等級/2 的光耀/死靈傷害)", "神聖戰士 (Warrior of the Gods: 復活免耗鑽石原料)"],
                    6: ["堅定狂信 (Fanatical Focus: 狂暴中豁免失敗可強制重骰一次)"],
                    10: ["狂熱戰吼 (Zealous Presence: 鼓舞戰吼賦予全隊命中與豁免優勢)"],
                    14: ["超越死亡 (Rage beyond Death: 狂暴期間即使 HP 歸零亦絕不倒地身亡)"]
                }
            },
            "先祖守衛道途 (Path of the Ancestral Guardian)": {
                "desc": "召喚部落古代戰魂繚繞周身，牽制首要敵人保護身後脆皮盟友。",
                "features_by_level": {
                    3: ["先祖守護 (Ancestral Protectors: 狂暴命中之目標攻擊隊友時處於劣勢且半傷)"],
                    6: ["靈魂護盾 (Spirit Shield: 反應動作召喚英靈吸收盟友承受的傷害)"],
                    10: ["先祖通靈 (Consult the Spirits: 施展占卜與千里眼神術)"],
                    14: ["復仇英靈 (Vengeful Ancestors)"]
                }
            },
            "巨人道途 (Path of the Giant)": {
                "desc": "體內流淌著風暴與山嶺巨人的狂暴血脈，狂暴時化身為大型巨人投擲兵器。",
                "features_by_level": {
                    3: ["巨人力量 (Giant's Power: 化身體型大型，攻擊觸及增加 5 呎)", "投擲武器巨力"],
                    6: ["元素劈砍 (Elemental Cleaver: 武器附加火/冰/電/酸傷害並自帶回力)"],
                    10: ["巨力投擲 (Mighty Impel: 抓起隊友或敵人直接遠程投擲出去)"],
                    14: ["巨神化身 (Demiurgic Colossus: 體型擴張為超大型生物)"]
                }
            },
            "風暴先驅道途 (Path of the Storm Herald)": {
                "desc": "將沙漠酷熱、暴風雨雷霆或冰原極寒的狂暴靈氣具現化於周身戰場。",
                "features_by_level": {
                    3: ["風暴靈光 (Storm Aura: 沙漠烈火灼燒/海洋雷擊震懾/冰原賦予臨時HP)"],
                    6: ["風暴抗性 (Storm Soul: 獲得對應環境傷害抗性與環境生存能力)"],
                    10: ["靈光庇護 (Shielding Storm: 將抗性分享給靈光內所有盟友)"],
                    14: ["狂怒風暴 (Raging Storm)"]
                }
            },
            "野獸之路 (Path of the Beast)": {
                "desc": "體內潛伏著史前野獸的獸性變異，狂暴時生出利齒獠牙、利爪或骨刺長尾。",
                "features_by_level": {
                    3: ["獸性形態 (Form of the Beast: 咬擊吸血/利爪連環三次爪擊/尾巴防守招架)"],
                    6: ["野獸身手 (Bestial Soul: 攀爬速度/水下游泳/巨力彈跳)"],
                    10: ["感染野性 (Infectious Fury: 利爪撕咬迫使敵人狂暴自相殘殺)"],
                    14: ["荒野獸群 (Call of the Hunt)"]
                }
            }
        }
    },
    "聖騎士 (Paladin)": {
        "category": "神聖之誓 (Sacred Oath)",
        "unlock_level": 3,
        "options": {
            "奉獻之誓 (Oath of Devotion)": {
                "desc": "古典正義騎士的終極典範，以神聖白銀聖光加持長劍破除黑暗邪祟。",
                "features_by_level": {
                    3: ["引導神力：神聖武器 (Sacred Weapon: 武器散發陽光，命中附加魅力加成)", "引導神力：驅散邪魔"],
                    7: ["虔誠靈光 (Aura of Devotion: 自身與 10 呎內盟友完全免疫魅惑)"],
                    15: ["至聖純潔 (Purity of Spirit: 常態獲得反制善惡法術庇護)"],
                    20: ["聖光光暈 (Holy Nimbus: 展開耀眼陽光光環並每回合造成光耀傷害)"]
                }
            },
            "復仇之誓 (Oath of Vengeance)": {
                "desc": "以血還血、追獵罪魁禍首直至地獄深淵的無情鐵血復仇判官。",
                "features_by_level": {
                    3: ["引導神力：仇敵誓言 (Vow of Enmity: 附贈動作鎖定仇敵，對其攻擊皆具優勢)", "驅敵之令"],
                    7: ["無情追擊 (Relentless Avenger: 藉機攻擊命中後可立即跟隨移動半速)"],
                    15: ["靈魂反擊 (Soul of Vengeance: 誓言仇敵發動攻擊時反應動作揮砍一劍)"],
                    20: ["復仇死神 (Avenging Angel: 生出暗影黑翼飛行並散發恐慌靈光)"]
                }
            },
            "遠古之誓 (Oath of the Ancients)": {
                "desc": "崇尚自然光明、生命喜悅與精靈荒野綠騎士，展開抗魔庇護靈光。",
                "features_by_level": {
                    3: ["引導神力：自然之怒 (Nature's Wrath: 召喚鬼魅藤蔓纏繞束縛敵人)", "驅散精魂"],
                    7: ["抗魔靈光 (Aura of Warding: 自身與周圍盟友受法術傷害皆減半)"],
                    15: ["不屈之軀 (Undying Sentinel: 致命傷倒地降至 1 點 HP，免除衰老衰弱)"],
                    20: ["遠古長老 (Elder Champion: 化身荒野森林守護神，附贈動作瞬發神術)"]
                }
            },
            "征服之誓 (Oath of Conquest)": {
                "desc": "以絕對鐵腕、恐懼統治與不可動搖的力量粉碎敵人的反抗意志。",
                "features_by_level": {
                    3: ["引導神力：征服恐懼 (Conquering Presence: 迫使周遭敵人陷入恐慌)", "引導神力：卓越打擊 (+10 命中)"],
                    7: ["征服靈光 (Aura of Conquest: 恐慌敵人移速歸零且每回合承受心靈傷害)"],
                    15: ["鄙夷反噬 (Scornful Rebuke: 被打擊時對攻擊者反彈心靈傷害)"],
                    20: ["無敵征服者 (Invincible Conqueror: 獲得全傷害抗性與額外攻擊)"]
                }
            },
            "救贖之誓 (Oath of Redemption)": {
                "desc": "信奉和平與慈悲，不到最後關頭絕不揮劍，願以身軀替罪人擋刀受難。",
                "features_by_level": {
                    3: ["引導神力：和平使節 (Emissary of Peace: 說服檢定 +5)", "引導神力：正義反彈 (Rebuke the Violent)"],
                    7: ["護衛之誓 (Aura of the Guardian: 反應動作替身旁受傷盟友承受全部傷害)"],
                    15: ["保護靈光 (Protective Spirit: 戰鬥中瀕危時每回合自動回血)"],
                    20: ["和平化身 (Emissary of Redemption: 受到非豁免攻擊傷害皆自動減半)"]
                }
            },
            "守望之誓 (Oath of the Watchers)": {
                "desc": "警惕異界邪魔、外域異形與靈界入侵的位面斥候，強化全隊先攻防備。",
                "features_by_level": {
                    3: ["引導神力：守望者之眼 (Watcher's Will: 全隊智力/感知/魅力豁免具備優勢)", "斥退外域位面生物"],
                    7: ["警覺靈光 (Aura of the Sentinel: 自身與周圍全隊先攻檢定附加 PB 加成)"],
                    15: ["斥退反擊 (Vigilant Rebuke: 豁免成功時對施法者反震力場傷害)"],
                    20: ["人間界守護衛士 (Mortal Bulwark: 獲得真實視覺並放逐異界入侵者)"]
                }
            },
            "王冠之誓 (Oath of the Crown)": {
                "desc": "效忠王國、律法秩序與文明社會的忠誠禁衛，誓死捍衛君王與無辜百姓。",
                "features_by_level": {
                    3: ["引導神力：捍衛王權 (Champion Challenge: 嘲諷挑釁 30 呎內敵人限制逃竄)", "戰潮鼓舞 (Turn the Tide)"],
                    7: ["忠誠誓約 (Divine Allegiance: 替 5 呎內盟友吸收傷害)"],
                    15: ["堅毅意志 (Unyielding Saint: 對麻痺與昏迷豁免具備優勢)"],
                    20: ["不破堡壘 (Exalted Champion)"]
                }
            },
            "榮耀之誓 (Oath of Glory)": {
                "desc": "崇尚英雄史詩、運動健美與名垂千古的英雄傳奇聖騎士。",
                "features_by_level": {
                    3: ["引導神力：無雙運動能力 (Peerless Athlete)", "引導神力：英勇打擊 (Inspiring Smite)"],
                    7: ["敏捷靈光 (Aura of Alacrity: 提升自身與盟友移動速度)"],
                    15: ["榮耀防禦 (Glorious Defense)"],
                    20: ["傳奇活化身 (Living Legend)"]
                }
            }
        }
    },
    "遊俠 (Ranger)": {
        "category": "遊俠原型 (Ranger Archetype)",
        "unlock_level": 3,
        "options": {
            "獵人 (Hunter)": {
                "desc": "磨練經典獵殺戰技的荒野老獵人，專精對付巨獸或橫掃大群鼠輩怪群。",
                "features_by_level": {
                    3: ["獵人天賦 (巨人殺手 Colossus Slayer: 受損目標額外 +1d8 傷；或部落破壞者)"],
                    7: ["防禦戰法 (逃脫攻擊、鋼鐵心智或多重打擊防禦)"],
                    11: ["多重打擊 (旋風斬揮砍周圍或排箭齊射範圍目標)"],
                    15: ["高等獵人防禦 (反射閃避 Evasion 或藉機閃避)"]
                }
            },
            "幽域追蹤者 (Gloom Stalker)": {
                "desc": "穿梭於幽暗地域與暗影中的潛伏大師，在黑暗中連黑暗視覺都無法看見他。",
                "features_by_level": {
                    3: ["幽暗伏擊 (Dread Ambusher: 先攻加感知，首輪額外攻擊且 +1d8 傷)", "暗影偽裝 (對黑暗視覺隱形)"],
                    7: ["鐵壁心靈 (Iron Mind: 獲得感知豁免熟練項)"],
                    11: ["追獵連擊 (Stalker's Flurry: 攻擊失準時可立即再補射一箭)"],
                    15: ["暗影閃避 (Shadowy Dodge: 反應動作迫使敵人攻擊處於劣勢)"]
                }
            },
            "獸王 (Beast Master)": {
                "desc": "與自然靈獸同伴締結終生心靈夥伴契約，並肩衝鋒發動夾擊撕咬。",
                "features_by_level": {
                    3: ["野獸同伴 (Ranger's Companion: 與野獸心靈相通，生命防禦隨等級成長)"],
                    7: ["協同突擊 (Exceptional Training: 附贈動作命令同伴疾走/撤離/協助)"],
                    11: ["狂野狂暴打擊 (Bestial Fury: 野獸同伴每回合可攻擊 2 次)"],
                    15: ["法術共享 (Share Spells: 施展強化法術時野獸同伴同享增益)"]
                }
            },
            "妖精漫遊者 (Fey Wanderer)": {
                "desc": "體內浸潤著妖精荒野的奇異魔幻魅力，將精神心靈傷害注入箭矢與說服口吻中。",
                "features_by_level": {
                    3: ["恐懼恐嚇之禮 (Dreadful Strike: 武器附加 1d4 心靈傷害)", "異界風采 (社交檢定加感知)"],
                    7: ["魅惑反制 (Beguiling Twist: 敵人魅惑豁免成功時可反彈轉移目標)"],
                    11: ["妖精援軍 (Fey Reinforcements: 召喚小精靈軍團作戰)"],
                    15: ["迷霧穿梭 (Mist Wanderer: 每日多次施展迷蹤步且可帶同伴)"]
                }
            },
            "境界行者 (Horizon Walker)": {
                "desc": "防衛多元宇宙裂隙的位面巡警，將攻擊轉化為純淨力場並穿梭次元閃現。",
                "features_by_level": {
                    3: ["位面感知 (Detect Portal)", "位面戰士 (Planar Warrior: 附贈動作將武器傷害轉化為純力場傷害 +1d8)"],
                    7: ["飄渺位移 (Ethereal Step: 附贈動作短暫步入以太位面)"],
                    11: ["遙距打擊 (Distant Strike: 每次攻擊前可傳送 10 呎並攻擊 3 個不同目標)"],
                    15: ["幽靈防衛 (Spectral Defense: 受傷時反應動作使傷害減半)"]
                }
            },
            "怪物殺手 (Monster Slayer)": {
                "desc": "洞悉各類異形、邪魔與吸血鬼死穴的超自然怪物獵魔人。",
                "features_by_level": {
                    3: ["獵手感官 (Hunter's Sense: 立即洞悉目標弱點與抗性)", "殺手宿敵 (Slayer's Prey: 標記目標附加額外傷害)"],
                    7: ["超自然防禦 (Supernatural Defense: 對目標豁免與逃脫檢定加 d6)"],
                    11: ["打斷復仇 (Magic-User's Nemesis: 反應動作直接打斷敵方的施法或傳送)"],
                    15: ["屠夫反殺 (Slayer's Counter: 被迫豁免時可先射出一箭打斷對方)"]
                }
            },
            "集群守衛 (Swarmkeeper)": {
                "desc": "周身環繞著無數由精靈/蟲群/樹靈構成的自然集群，推撞敵人並護衛本體。",
                "features_by_level": {
                    3: ["集群同伴 (Gathered Swarm: 命中時造成額外穿刺傷害、推撞敵人或位移自身)"],
                    7: ["疾行之潮 (Writhing Tide: 獲得攀爬速度與空中懸浮飛行能力)"],
                    11: ["集群狂怒 (Mighty Swarm: 群體推撞倒地並給予自身全掩護)"],
                    15: ["化身集群 (Swarming Dispersal: 受傷時瞬間化為無形蟲群傳送脫身)"]
                }
            },
            "龍獸守衛 (Drakewarden)": {
                "desc": "孵化並駕馭一隻伴隨冒險成長的致命幼龍，最終成為翺翔天際的龍騎士。",
                "features_by_level": {
                    3: ["龍之禮物 (Draconic Gift: 通曉龍語並獲戲法)", "召喚幼龍同伴 (Drake Companion)"],
                    7: ["巨龍飛躍 (幼龍體型成長為中型，命中附加咬擊元素傷害)"],
                    11: ["巨龍吐息 (Drake's Breath: 釋放毀滅性 8d6 錐狀元素吐息)"],
                    15: ["完美巨龍騎乘 (幼龍體型成長為大型，可乘騎空中飛行空中作戰)"]
                }
            }
        }
    },
    "吟遊詩人 (Bard)": {
        "category": "吟遊詩人學院 (Bard College)",
        "unlock_level": 3,
        "options": {
            "知識學院 (College of Lore)": {
                "desc": "追求世間萬物奧秘的博學者，以尖銳言詞削弱敵人命中並跨界研習萬用魔法。",
                "features_by_level": {
                    3: ["額外技能熟練 (額外獲得 3 項任意技能熟練)", "尖刻言詞 (Cutting Words: 消耗激勵骰扣減敵人命中或傷害)"],
                    6: ["額外魔法奧秘 (Additional Magical Secrets: 提前從任意職業學習 2 個法術)"],
                    14: ["卓越技能 (Peerless Skill: 自身檢定失準時消耗激勵骰加成)"]
                }
            },
            "勇氣學院 (College of Valor)": {
                "desc": "吟唱古代北方戰士英勇史詩的戰歌詩人，披掛中甲盾牌並能激勵盟友武器打擊。",
                "features_by_level": {
                    3: ["中甲、盾牌與軍用武器熟練", "戰鬥激勵 (Combat Inspiration: 盟友可將激勵骰加入武器傷害骰或 AC)"],
                    6: ["額外攻擊 (Extra Attack: 每次攻擊動作可揮砍 2 次)"],
                    14: ["戰法同鳴 (Battle Magic: 施展詩人法術後以附贈動作發動武器攻擊)"]
                }
            },
            "劍舞學院 (College of Swords)": {
                "desc": "揮舞細劍如舞步般華麗的劍舞者，以優雅花式劍招位移控場並提升防禦。",
                "features_by_level": {
                    3: ["中甲與細劍熟練、戰鬥風格 (對決或雙武器)", "劍刃花招 (Blade Flourish: 穿刺花招、防禦花招提升 AC、推撞花招)"],
                    6: ["額外攻擊 (Extra Attack)"],
                    14: ["大師花招 (Master's Flourish: 無需消耗激勵骰即可施展 d6 花招)"]
                }
            },
            "迷惑學院 (College of Glamour)": {
                "desc": "承襲妖精荒野的超凡魅力與令人敬畏的風采，以天籟歌聲震懾萬民心智。",
                "features_by_level": {
                    3: ["動人披風 (Mantle of Inspiration: 賦予多名盟友臨時生命並自由位移)", "妖精風采 (Enthralling Performance)"],
                    6: ["王者尊榮 (Mantle of Majesty: 附贈動作隨意施展命令術 Command 免耗法術位)"],
                    14: ["不可侵犯美貌 (Unbreakable Majesty: 攻擊者必須通過魅力豁免否則無法下手)"]
                }
            },
            "低語學院 (College of Whispers)": {
                "desc": "潛伏於宮廷陰影中的情報販子與間諜刺客，將心靈恐懼與毒刺注入音符。",
                "features_by_level": {
                    3: ["毒刃暗刺 (Psychic Blades: 武器命中消耗激勵骰附加 2d6~8d6 心靈重創)", "恐怖恐懼字句 (Words of Terror)"],
                    6: ["竊魂魅影 (Mantle of Whispers: 捕獲死者影子並完美冒充其外貌與記憶)"],
                    14: ["心靈暗影支配 (Shadow Lore: 永久掌控被要脅者的深層心智)"]
                }
            },
            "雄辯學院 (College of Eloquence)": {
                "desc": "言辭字字珠璣的辯論大師，說服與欺瞞永不大失敗，且其激勵絕不白費。",
                "features_by_level": {
                    3: ["銀舌 (Silver Tongue: 說服與欺瞞檢定 d20 低於 9 一律視為 10)", "驚擾言語 (扣減敵人豁免檢定)"],
                    6: ["深厚靈感 (Unfailing Inspiration: 激勵檢定失敗時激勵骰不被消耗)"],
                    14: ["致命雄辯 (Infectious Inspiration)"]
                }
            },
            "創造學院 (College of Creation)": {
                "desc": "以創世神曲的音符共振現實，憑空塑造實體物品並賦予無生物生命。",
                "features_by_level": {
                    3: ["潛能激勵 (Note of Potential)", "創造實體 (Performance of Creation: 憑空歌唱塑造出金屬道具或器具)"],
                    6: ["活化之歌 (Animating Song: 賦予大型無生物生命化為戰鬥魔偶)", "活化道具飛行"],
                    14: ["創世合奏 (Creative Crescendo)"]
                }
            },
            "靈魂學院 (College of Spirits)": {
                "desc": "手持塔羅牌或通靈板的通靈詩人，聆聽往昔逝者之魂並引導鬼魅故事神力。",
                "features_by_level": {
                    3: ["通靈法器 (Guiding Whispers)", "逝者之語 (Tales from Beyond: 擲靈魂表引導巨龍、英雄、刺客等12種怨靈奇效)"],
                    6: ["通靈降神會 (Spirit Session: 與隊友冥想學會任意死靈或預言法術)"],
                    14: ["神秘聯通 (Mystical Connection)"]
                }
            }
        }
    },
    "武僧 (Monk)": {
        "category": "修道院修習 (Monastic Tradition)",
        "unlock_level": 3,
        "options": {
            "散打宗 (Way of the Open Hand)": {
                "desc": "將肉身氣勁發揮至純粹極致，疾風連擊擊倒敵人、震飛目標並掌握碎心掌。",
                "features_by_level": {
                    3: ["散打技巧 (Open Hand Technique: 疾風連擊擊倒伏地、震退 15 呎或剝奪反應動作)"],
                    6: ["身心整復 (Wholeness of Body: 動作打坐回覆等於武僧等級 3 倍 HP)"],
                    10: ["寧靜致遠 (Tranquility: 常態自帶避難所法術 Sanctuary 光環)"],
                    17: ["絕殺碎心掌 (Quivering Palm: 將致命真氣注入敵人體內，日後隨時意念引爆奪命)"]
                }
            },
            "暗影宗 (Way of Shadow)": {
                "desc": "操縱陰影帷幕的東方忍者，在陰影微光中瞬息傳送並悄無聲息暗殺目標。",
                "features_by_level": {
                    3: ["暗影藝術 (Shadow Arts: 消耗氣施展黑暗術、寂靜術、暗視術與行蹤無跡)"],
                    6: ["陰影躍遷 (Shadow Step: 在微光或陰影中以附贈動作傳送 60 呎且下次攻擊具優勢)"],
                    11: ["隱身遁形 (Cloak of Shadows: 在陰影中直接化身完全隱形)"],
                    17: ["伺機突襲 (Opportunist: 旁人攻擊敵人時反應動作揮出一擊)"]
                }
            },
            "劍聖宗 (Way of the Kensei)": {
                "desc": "將手中長劍、長弓視為肉體延伸的劍聖，刀光劍影中兼具無雙攻防加成。",
                "features_by_level": {
                    3: ["劍聖武器 (Kensei Weapons: 將近戰軍用武器與遠程武器納入武僧武器)", "敏捷招架 (Parry: +2 AC)"],
                    6: ["破魔真氣劍 (One with the Blade: 武器視為魔法武器，命中消耗氣附加傷害)"],
                    11: ["銳利刀刃 (Sharpen the Blade: 消耗氣賦予武器最高 +3 命中傷害加成)"],
                    17: ["不落之刃 (Unerring Accuracy: 攻擊失準時強制重骰一次)"]
                }
            },
            "命流宗 (Way of Mercy)": {
                "desc": "身著鳥嘴面具的慈悲行醫僧侶，以一掌撫平創傷生機，以另一手降下衰竭壞疽。",
                "features_by_level": {
                    3: ["慈悲之手 (Hands of Healing: 消耗氣治癒盟友生機)", "傷害之手 (Hands of Harm: 徒手命中追加壞疽死靈傷害)"],
                    6: ["良藥苦口 (Physician's Touch: 治療同時清除中毒、麻痺與目盲)"],
                    11: ["疾風合奏 (Flurry of Healing and Harm)"],
                    17: ["起死回生 (Hand of Ultimate Mercy: 消耗氣讓剛死亡的生物重獲新生)"]
                }
            },
            "日魂宗 (Way of the Sun Soul)": {
                "desc": "將體內氣勁轉化為烈陽雷射金光，揮拳遠程射出耀眼的熾光衝擊。",
                "features_by_level": {
                    3: ["日晷耀光衝擊 (Radiant Sun Bolt: 遠程 30 呎射出光耀傷害氣勁射線)"],
                    6: ["烈陽灼熱射線 (Searing Sunburst)"],
                    11: ["烈陽爆裂 (Searing Sunburst: 召喚大範圍烈日金光火球)"],
                    17: ["太陽之軀 (Sun Shield: 散發耀眼金光並反彈光耀傷害)"]
                }
            },
            "星我宗 (Way of the Astral Self)": {
                "desc": "喚醒精神星光投影，周身凝聚出如替身般威嚴的星光臂甲與星光頭盔。",
                "features_by_level": {
                    3: ["召喚星我手臂 (Arms of the Astral Self: 凝聚星光手臂觸及 +5 呎，用感知近戰揮打)"],
                    6: ["星我面容 (Visage of the Astral Self: 黑暗視覺、洞察與威嚇優勢)"],
                    11: ["星我軀幹 (Body of the Astral Self: 吸收元素傷害並連環猛攻)"],
                    17: ["星我真容 (Awakened Astral Self: 四臂星光化身狂暴連打)"]
                }
            },
            "醉拳宗 (Way of the Drunken Master)": {
                "desc": "步伐踉蹌難測的醉仙狂俠，在跌撞翻滾中靈活躲避圍剿並反借敵人之力。",
                "features_by_level": {
                    3: ["醉步翻滾 (Drunken Technique: 疾風連擊自動獲撤離效果且移速 +10 呎)", "醉拳表演熟練"],
                    6: ["搖曳借力 (Leap to the Feet: 倒地起立僅耗 5 呎)", "借力打力 (敵人失準時引導其砍中另一敵人)"],
                    11: ["醉仙運氣 (Drunkard's Luck: 消耗氣取消檢定劣勢)"],
                    17: ["狂醉旋風舞 (Intoxicated Frenzy: 疾風連擊一輪內最多攻擊 5 個不同目標)"]
                }
            },
            "神龍宗 (Way of the Ascendant Dragon)": {
                "desc": "修習遠古巨龍吐息與威壓的武僧，揮拳附帶龍息元素並展翼滑翔。",
                "features_by_level": {
                    3: ["龍之弟子 (Draconic Disciple: 徒手轉化為酸/冰/火/電/毒傷害)", "龍息吐息 (Breath of the Dragon)"],
                    6: ["展翼高飛 (Wings Unfurled: 踏風步時生出龍翼空中飛行)"],
                    11: ["巨龍靈光 (Aspect of the Wyrm: 展開催眠威壓或抗性結界)"],
                    17: ["天龍化身 (Ascendant Aspect)"]
                }
            }
        }
    },
    "術士 (Sorcerer)": {
        "category": "術法起源 (Sorcerous Origin)",
        "unlock_level": 1,
        "options": {
            "龍族血脈 (Draconic Bloodline)": {
                "desc": "祖先與太古巨龍交融，體表覆蓋堅固龍鱗且掌握毀滅龍脈元素。",
                "features_by_level": {
                    1: ["龍裔體魄 (Draconic Resilience: 生命上限每級 +1，無甲 AC 為 13 + 敏捷)", "龍語通曉"],
                    6: ["元素親和 (Elemental Affinity: 施展對應龍種法術附加魅力傷害並獲抗性)"],
                    14: ["巨龍之翼 (Dragon Wings: 背後生出巨大龍翼隨時展翅飛行)"],
                    18: ["龍威親臨 (Draconic Presence: 散發巨龍恐慌或崇敬壓迫靈光)"]
                }
            },
            "狂野魔法 (Wild Magic)": {
                "desc": "體內魔力如同狂暴混亂風暴，每次施法皆可能引發不可預測的超現實狂潮。",
                "features_by_level": {
                    1: ["狂野魔法狂潮 (Wild Magic Surge: 施法時擲出 1 觸發狂野魔能表50種奇效)", "命運之潮 (Tides of Chaos: 任意檢定直接獲優勢)"],
                    6: ["扭曲命運 (Bend Luck: 消耗術法點為他人檢定加減 1d4)"],
                    14: ["掌控混亂 (Controlled Chaos: 狂野狂潮可擲 2 次並自選喜好效果)"],
                    18: ["法術暴走 (Spell Bombardment)"]
                }
            },
            "神聖之魂 (Divine Soul)": {
                "desc": "神祇或天界生靈的祝福血脈，能跨界直接習得牧師神術並引導恩寵之光。",
                "features_by_level": {
                    1: ["神聖魔力 (Divine Magic: 可從術士或牧師法術列表中自由挑選學習)", "天恩眷顧 (Favored by the Gods: 豁免失準加 2d4)"],
                    6: ["受祝生靈 (Empowered Healing: 消耗術法點重骰治癒骰)"],
                    14: ["天界之翼 (Otherworldly Wings: 召喚神聖光羽之翼空中飛行)"],
                    18: ["神聖超脫 (Unholy/Angelic Recovery: 瀕危時瞬間回滿半數 HP)"]
                }
            },
            "幽影魔法 (Shadow Magic)": {
                "desc": "誕生於幽影位面的漆黑死寂魔力，能召喚幽影惡犬追獵並化身暗影。",
                "features_by_level": {
                    1: ["幽暗視覺 (Eyes of the Dark: 120呎黑暗視覺並可用術法點施展黑暗術看穿)", "死境歸來 (瀕死時體質豁免保命)"],
                    6: ["召喚厄運幽影犬 (Hound of Ill Omen: 召喚影子獵犬貼身咬擊並削弱敵人豁免)"],
                    14: ["幽影漫步 (Shadow Walk: 在陰影中以附贈動作瞬間傳送 120 呎)"],
                    18: ["暗影形態 (Umbral Form: 化身半透明陰影幽魂獲得全傷害抗性)"]
                }
            },
            "風暴術法 (Storm Sorcery)": {
                "desc": "體內奔騰著閃電與颶風的狂暴氣象，施法前後能伴隨微風疾掠空中。",
                "features_by_level": {
                    1: ["風之使者 (Wind Speaker: 通曉風族語)", "狂風疾掠 (Tempestuous Magic: 施法前後附贈動作飛行 10 呎免受藉機攻擊)"],
                    6: ["風暴之心 (Heart of the Storm: 施展雷電法術反震周圍敵人)", "導風禦雨"],
                    14: ["風暴怒濤 (Storm's Fury: 受近戰攻擊時反彈雷擊並震退敵人)"],
                    18: ["風暴之靈 (Wind Soul: 全隊共享飛行能力與雷電抗性)"]
                }
            },
            "畸變心智 (Aberrant Mind)": {
                "desc": "心靈受遠界不可名狀星界外神侵染，能心靈傳音並以純意念施展靈能法術。",
                "features_by_level": {
                    1: ["異界言談 (Telepathic Speech: 無障礙心靈通訊)", "畸變法術 (Psionic Spells: 附贈心靈法術清單)"],
                    6: ["靈能術法 (Psionic Sorcery: 消耗術法點免構材施法)", "靈能防禦 (心靈抗性與抗魅惑優勢)"],
                    14: ["扭曲變異 (Revelation in Flesh: 肉體流質化穿牆、章魚觸鬚游泳或飛行)"],
                    18: ["心靈黑洞 (Warping Implosion: 撕裂時空引爆引力黑洞扯碎敵人)"]
                }
            },
            "時械之魂 (Clockwork Soul)": {
                "desc": "秩序位面機械境的絕對定律之力，能消除戰場上的極端優勢或劣勢。",
                "features_by_level": {
                    1: ["秩序法術 (Clockwork Spells)", "恢復平衡 (Restore Balance: 反應動作取消 60 呎內目標的優勢或劣勢)"],
                    6: ["固若金湯護盾 (Bastion of Law: 構建秩序能量盾吸收傷害)"],
                    14: ["命運齒輪 (Trance of Order: 進入機械律法專注，所有 d20 檢定低於 9 視為 10)"],
                    18: ["秩序時鐘 (Clockwork Cavalcade: 召喚時鐘之靈修復萬物並驅散法術)"]
                }
            }
        }
    },
    "契術師 (Warlock)": {
        "category": "異界宗主 (Otherworldly Patron)",
        "unlock_level": 1,
        "options": {
            "邪魔宗主 (The Fiend)": {
                "desc": "與下層界位面的大魔鬼或深淵惡魔領主簽訂契約，汲取殺戮生機與地獄烈焰。",
                "features_by_level": {
                    1: ["深淵祝福 (Dark One's Blessing: 擊殺敵人時汲取其靈魂獲得臨時 HP)"],
                    6: ["惡魔幸運 (Dark One's Own Luck: 檢定或豁免時可額外加 1d10)"],
                    10: ["邪魔體魄 (Fiendish Resilience: 短休自由挑選一項非魔法傷害抗性)"],
                    14: ["穿越地獄 (Hurl Through Hell: 命中時將敵人短暫打入九層地獄遭受 10d10 精神心靈摧殘)"]
                }
            },
            "至高妖精 (The Archfey)": {
                "desc": "效忠於妖精荒野的古老妖精貴族，掌握令人魂牽夢縈的幻術與魅惑詭計。",
                "features_by_level": {
                    1: ["仙靈威儀 (Fey Presence: 周身爆發迷人或駭人光霧魅惑/恐慌周圍敵人)"],
                    6: ["迷霧遁形 (Misty Escape: 受傷時瞬間隱形並在原地留下迷霧傳送脫身)"],
                    10: ["魅惑反噬 (Beguiling Defenses: 免疫魅惑並反向魅惑施法者)"],
                    14: ["黑暗迷宮 (Dark Delirium: 將敵人意識困入封閉的妖精迷霧幻境)"]
                }
            },
            "舊日支配者 (The Great Old One)": {
                "desc": "與星界深處不可名狀的外神或古老巨識建立聯結，跨維度心靈通訊並摧毀敵人心智。",
                "features_by_level": {
                    1: ["心靈低語 (Awakened Mind: 無視語言障礙與 30 呎內任何生物心靈對話)"],
                    6: ["心靈壁壘 (Entropic Ward: 反應動作迫使攻擊者處於劣勢，失準後下次攻擊具優勢)"],
                    10: ["思想之盾 (Thought Shield: 免疫心靈讀取並反彈心靈傷害)"],
                    14: ["創造奴僕 (Create Thrall: 將昏迷人形生物轉化為忠誠心靈僕從)"]
                }
            },
            "咒劍士 (The Hexblade)": {
                "desc": "宗主源自墮影冥界的遠古神兵意志，能以魅力揮砍魔法兵器並詛咒宿敵。",
                "features_by_level": {
                    1: ["咒劍詛咒 (Hexblade's Curse: 標記目標附加 PB 傷害與 19~20 重擊)", "咒劍戰士 (中甲盾牌熟練，武器命中與傷害改用魅力)"],
                    6: ["被詛詛咒幽靈 (Accursed Specter: 擊殺敵人時將其靈魂拘禁為幽靈僕從)"],
                    10: ["護衛鎧甲 (Armor of Hexes: 被詛咒目標攻擊自身有 50% 機率直接落空)"],
                    14: ["大師魔咒 (Master of Hexes)"]
                }
            },
            "天界宗主 (The Celestial)": {
                "desc": "與上層界的天使、獨角獸或日冕生靈締結盟約，引導神聖治癒光池。",
                "features_by_level": {
                    1: ["光耀戲法", "治癒之光 (Healing Light: 充能光池以附贈動作遠程治癒盟友)"],
                    6: ["光耀靈魂 (Radiant Soul: 火焰與光耀抗性，施展光耀法術附加魅力加成)"],
                    10: ["天界堅毅 (Celestial Resilience: 短休長休時全隊獲得高額臨時 HP)"],
                    14: ["熾光重臨 (Searing Vengeance: 瀕死倒地時爆發光耀傷害彈起並完全回血)"]
                }
            },
            "不死宗主 (The Undead)": {
                "desc": "奉獻於古老死靈法王、巫妖或吸血鬼領主，化身死亡恐懼的恐怖形態。",
                "features_by_level": {
                    1: ["恐怖形態 (Form of Dread: 化身不死骨骸形態獲得臨時生命與恐嚇打擊)"],
                    6: ["死亡重擊 (Grave Touched: 傷害轉為壞疽並在暴擊時追加傷害骰)"],
                    10: ["壞疽防護 (Necrotic Husk: 免疫壞疽傷害，HP歸零時引爆死靈衝擊免死)"],
                    14: ["靈魂出竅 (Spirit Projection: 靈魂離體自由穿牆飛行施法)"]
                }
            },
            "巨靈宗主 (The Genie)": {
                "desc": "與元素位面的貴族巨靈（火巨靈/風巨靈/土巨靈/水巨靈）簽訂契約，寄宿於微縮神燈容器中。",
                "features_by_level": {
                    1: ["巨靈法器 (Genie's Vessel: 隨身神燈油燈，命中附加元素傷害並能躲入神燈避難)"],
                    6: ["元素恩賜 (Elemental Gift: 獲得元素抗性與常態懸浮飛行能力)"],
                    10: ["避難庇護所 (Sanctuary Vessel: 帶領全隊進入神燈以 10 分鐘完成短休)"],
                    14: ["限量許願 (Limited Wish: 乞求宗主直接施展任意 6 環以下法術免耗材料)"]
                }
            },
            "深海意志 (The Fathomless)": {
                "desc": "向無光深淵海底的遠古克拉肯海怪巨獸效忠，召喚深海冰冷觸手鞭笞敵人。",
                "features_by_level": {
                    1: ["深海之觸 (Tentacle of the Deeps: 附贈動作召喚深海觸手打擊並減速敵人)", "水生適應 (游泳速度與水下呼吸)"],
                    6: ["深海之洋 (Oceanic Soul: 寒冷傷害抗性與水下通訊)", "觸手守護 (觸手替盟友吸收傷害)"],
                    10: ["狂暴深淵 (Grasping Tentacles: 施展黑觸手並獲臨時生命)"],
                    14: ["海流躍遷 (Fathomless Plunge: 召喚水流漩渦將全隊瞬間傳送至 1 英哩外水源)"]
                }
            }
        }
    },
    "奇械師 (Artificer)": {
        "category": "專業領域 (Artificer Specialist)",
        "unlock_level": 3,
        "options": {
            "戰地匠師 (Battle Smith)": {
                "desc": "前線的鋼鐵鐵匠與戰術工匠，以智力揮舞魔兵並攜帶忠誠的鋼鐵守衛魔像犬。",
                "features_by_level": {
                    3: ["戰鬥專家 (軍用武器熟練，魔法武器命中與傷害改用智力)", "鋼鐵守衛 (Steel Defender: 製造戰鬥機械魔像同伴並肩作戰)"],
                    5: ["額外攻擊 (Extra Attack)"],
                    9: ["奧術震波 (Arcane Jolt: 武器命中引爆治療或力場傷害)"],
                    15: ["精良防衛 (Improved Defender)"]
                }
            },
            "裝甲師 (Armorer)": {
                "desc": "打造精密全身動力動力機甲的發明家，可在守護者型重裝或滲透者型潛行間隨意切換。",
                "features_by_level": {
                    3: ["奧術動力裝甲 (Arcane Armor: 裝甲與肉體完美融合無視力量限制)", "裝甲型態 (守護者雷霆拳控場 / 滲透者閃電發射器潛行)"],
                    5: ["額外攻擊 (Extra Attack)"],
                    9: ["裝甲改裝 (Armor Modifications: 可在裝甲各部位額外注入多件魔法注法)"],
                    15: ["完美動力裝甲 (Perfected Armor)"]
                }
            },
            "魔炮師 (Artillerist)": {
                "desc": "精通遠程魔法火砲與魔杖改裝的重砲手，隨時隨地組裝微型奧術火砲轟炸戰場。",
                "features_by_level": {
                    3: ["魔能火砲 (Eldritch Cannon: 隨身組裝噴火砲、力場重砲或提供臨時HP的護盾砲)"],
                    5: ["奧術火器 (Arcane Firearm: 將魔杖手杖改造成魔炮，法術傷害骰 +1d8)"],
                    9: ["爆裂地雷 (Explosive Cannon: 火砲可過載自爆造成範圍巨量傷害)"],
                    15: ["雙管防禦重砲 (Fortified Position: 同時召喚 2 座火砲且全隊獲得半掩護)"]
                }
            },
            "煉金師 (Alchemist)": {
                "desc": "調配各類奇異魔藥與實驗性靈藥的藥劑大師，救死扶傷並噴灑強酸火焰。",
                "features_by_level": {
                    3: ["實驗性靈藥 (Experimental Elixir: 長休調配治癒、移速、飛行、護甲等強效魔藥)"],
                    5: ["煉金專家 (Alchemical Savant: 施展治癒或酸/火/死靈/毒法術附加智力調整值)"],
                    9: ["復元藥劑 (Restorative Reagents: 喝魔藥額外獲得臨時生命並清除負面狀態)"],
                    15: ["化學抗性 (Chemical Mastery: 免疫中毒與毒素傷害，每日免費施展高等復原術)"]
                }
            }
        }
    }
}

# ==========================================
# 5. 法術位對照表 (全施法者標準 Full Caster Spell Slots)
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
# 6. 完整背景資料庫 (涵蓋 D&D 5E 核心與繁體中文資料網全背景)
# ==========================================
BACKGROUNDS = {
    "侍僧 (Acolyte)": {
        "skills_options": "固定熟練：【洞察】、【宗教】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "信徒之家 (Shelter of the Faithful)：在同信仰神廟與信徒社群中享有免費食宿與神術照護援助。"
    },
    "派系特工 (Faction Agent)": {
        "skills_options": "固定熟練：【洞察】；加上自選一項智力/感知/魅力技能",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "避風港 (Safe Haven)：接觸秘密情報網中的特工支援，獲得免費食宿與安全情報庇護。"
    },
    "公會工匠 (Guild Artisan)": {
        "skills_options": "固定熟練：【洞察】、【說服】",
        "tool_options": "自選一項專業工匠工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "公會特權 (Guild Membership)：受到商業行會庇護，享有批發折扣、法律辯護援助與行會大廳接待。"
    },
    "變體公會工匠 (公會商人) (Guild Merchant)": {
        "skills_options": "固定熟練：【洞察】、【說服】",
        "tool_options": "領航工具或自選一項額外語言",
        "language_options": "自選任意 1 種額外語言",
        "feature": "行會特權 (Guild Membership)：受到商貿公會庇護，享有商隊通行優待與批發採購特權。"
    },
    "氏族工匠 (Clan Crafter)": {
        "skills_options": "固定熟練：【歷史】、【洞察】",
        "tool_options": "自選一項專業工匠工具",
        "language_options": "矮人語（若已通曉則自選一種）",
        "feature": "矮人的敬重 (Respect of the Stout Folk)：矮人族群視你為傳統手藝傳承者，無償提供食宿與工坊。"
    },
    "朝臣 (Courtier)": {
        "skills_options": "固定熟練：【洞察】、【說服】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "宮廷官員 (Court Functionary)：熟稔貴族議會官僚運作，輕易取得公文紀錄並會見關鍵掌權人士。"
    },
    "化外之民 (Outlander)": {
        "skills_options": "固定熟練：【運動】、【求生】",
        "tool_options": "自選一種樂器熟練",
        "language_options": "自選任意 1 種額外語言",
        "feature": "漂泊者 (Wanderer)：擁有精準地貌記憶，荒野中每日可為自己與多達5名同伴覓得足夠的淡水與野味。"
    },
    "烏斯伽部落成員 (Uthgardt Tribe Member)": {
        "skills_options": "固定熟練：【運動】、【求生】",
        "tool_options": "一種樂器或工匠工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "烏斯伽傳統 (Uthgardt Heritage)：熟悉荒野古老聖丘與圖騰禁忌，獲得荒野獵人與德魯伊同儕的禮遇。"
    },
    "士兵 (Soldier)": {
        "skills_options": "固定熟練：【運動】、【威嚇】",
        "tool_options": "自選一項博弈工具；以及陸上載具駕馭熟練",
        "language_options": "無額外語言",
        "feature": "軍事階級 (Military Rank)：前部隊袍澤與衛兵認可你的軍銜榮譽，必要時可借調營地物資或通行哨站。"
    },
    "教團騎士 (Knight of the Order)": {
        "skills_options": "固定熟練：【說服】；加上自選奧秘/歷史/自然/宗教一項",
        "tool_options": "自選一項博弈工具或樂器",
        "language_options": "自選任意 1 種額外語言",
        "feature": "騎士的敬重 (Knightly Regard)：在教團要塞與支持者聚落中受到崇高禮遇，隨時可獲得療傷、補給與庇護。"
    },
    "傭兵老將 (Mercenary Veteran)": {
        "skills_options": "固定熟練：【運動】、【說服】",
        "tool_options": "自選一項博弈工具；陸上載具熟練",
        "language_options": "無額外語言",
        "feature": "傭兵生涯 (Mercenary Life)：熟知各地傭兵兵團動向，輕易在城中找到雇傭兵營地並識別危險武裝勢力。"
    },
    "城市守衛 (City Watch)": {
        "skills_options": "固定熟練：【運動】、【洞察】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "守望者之眼 (Watcher's Eye)：敏銳察覺城鎮違法犯罪跡象，迅速找到當地巡邏隊哨所並調動衛兵協助。"
    },
    "變體城市守衛 (調查員) (Investigator)": {
        "skills_options": "固定熟練：【洞察】、【調查】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "守望者之眼 (Watcher's Eye)：精於勘查兇案現場與蒐集罪證，迅速辨識地方幫派與地下線人動向。"
    },
    "流浪兒 / 孤兒 (Urchin)": {
        "skills_options": "固定熟練：【巧手】、【隱匿】",
        "tool_options": "固定熟練：偽造工具組、盜賊工具組",
        "language_options": "無額外語言",
        "feature": "城市密徑 (City Secrets)：熟悉市井巷弄與屋頂小徑，非戰鬥狀態下在城鎮中穿梭速度為常人的兩倍。"
    },
    "學者 (Sage)": {
        "skills_options": "固定熟練：【奧秘】、【歷史】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "研究者 (Researcher)：即便你不知道某項遠古機密，你也清楚知道哪座圖書館或學者握有該項情報。"
    },
    "平民英雄 (Folk Hero)": {
        "skills_options": "固定熟練：【馴獸】、【求生】",
        "tool_options": "自選一項工匠工具熟練；陸上載具熟練",
        "language_options": "無額外語言",
        "feature": "鄉民款待 (Rustic Hospitality)：平民視你為同路英雄，願意無償提供藏身庇護與粗茶淡飯避開衛兵追捕。"
    },
    "繼承者 (Inheritor)": {
        "skills_options": "固定熟練：【求生】；加上自選奧秘/歷史/宗教一項",
        "tool_options": "一種博弈工具或樂器",
        "language_options": "自選任意 1 種額外語言",
        "feature": "繼承權 (Inheritance)：繼承了一件蘊含未解秘辛的遠古遺物或領地權狀，指引著日後冒險的核心主線。"
    },
    "水手 (Sailor)": {
        "skills_options": "固定熟練：【運動】、【察覺】",
        "tool_options": "固定熟練：領航工具、水上載具駕駛",
        "language_options": "無額外語言",
        "feature": "船行水路 (Ship's Passage)：能在信賴的商船或漁船上為自己與同伴爭取免費搭乘的航運便船。"
    },
    "變體水手 (海盜) (Pirate)": {
        "skills_options": "固定熟練：【運動】、【察覺】",
        "tool_options": "固定熟練：領航工具、水上載具駕駛",
        "language_options": "無額外語言",
        "feature": "惡名昭彰 (Bad Reputation)：港口平民與酒保因畏懼你的兇殘惡名，不敢反抗你的小額索求或報警舉發。"
    },
    "隱士 (Hermit)": {
        "skills_options": "固定熟練：【醫藥】、【宗教】",
        "tool_options": "固定熟練：草藥工具組",
        "language_options": "自選任意 1 種額外語言",
        "feature": "發現 (Discovery)：長期獨處冥想中領悟了一項震撼世界格局的驚天大秘密（如邪神復甦或遺失聖域）。"
    },
    "藝人 (Entertainer)": {
        "skills_options": "固定熟練：【特技】、【表演】",
        "tool_options": "固定熟練：易容工具組、一種自選樂器",
        "language_options": "無額外語言",
        "feature": "受人愛戴 (By Popular Demand)：每到一座城鎮皆能輕易在酒館獲得免費客房食宿，只要你每晚登台獻藝。"
    },
    "變體藝人 (角鬥士) (Gladiator)": {
        "skills_options": "固定熟練：【特技】、【表演】",
        "tool_options": "固定熟練：易容工具組、一種非傳統角鬥武器（如三叉戟/鐵網）",
        "language_options": "無額外語言",
        "feature": "受人愛戴 (By Popular Demand)：在鬥技場與平民觀眾間廣受追捧，可隨時在傭兵聚集地受到狂熱款待。"
    },
    "失敗商人 (Failed Merchant)": {
        "skills_options": "固定熟練：【調查】、【欺瞞】",
        "tool_options": "一種工匠工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "吃一塹長一智 (Supply and Demand)：熟知商業破產騙局與黑市差價，隨時能評估物品真實殘值。"
    },
    "賭徒 (Gambler)": {
        "skills_options": "固定熟練：【欺瞞】、【洞察】",
        "tool_options": "兩種博弈工具熟練",
        "language_options": "無額外語言",
        "feature": "永不空手 (Never Tell Me the Odds)：能輕易找到城中最隱蔽的地下賭場，並能透過下注打探情報。"
    },
    "原告 (Plaintiff)": {
        "skills_options": "固定熟練：【歷史】、【說服】",
        "tool_options": "一種工匠工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "法律漏洞 (Legal Counsel)：熟悉城鎮律法訴訟程序，能在被捕時以程序漏洞周旋爭取保釋時間。"
    },
    "競爭對手實習生 (Rival Intern)": {
        "skills_options": "固定熟練：【歷史】、【調查】",
        "tool_options": "一種工匠工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "商業情報 (Corporate Espionage)：熟知各大商會行會的內部運作與官僚秘密，能輕易取得行會內部文件。"
    },
    "修院學士 (Cloistered Scholar)": {
        "skills_options": "固定熟練：【歷史】；加上奧秘/自然/宗教自選一項",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "圖書館使用權 (Library Access)：廣受各地修道院與大學認可，享有閱覽各大禁書庫文獻的特權。"
    },
    "城市賞金獵人 (Urban Bounty Hunter)": {
        "skills_options": "從【欺瞞】、【洞察】、【說服】、【隱匿】中任選 2 項",
        "tool_options": "博弈工具、盜賊工具組、樂器中任選 2 項",
        "language_options": "無額外語言",
        "feature": "城市眼線 (Ear to the Ground)：在街頭流氓、酒館女侍與貴族侍從間擁有綿密線人，迅速掌握目標行蹤。"
    },
    "罪犯 (Criminal)": {
        "skills_options": "固定熟練：【欺瞞】、【隱匿】",
        "tool_options": "固定熟練：【盜賊工具組】；一種博弈工具",
        "language_options": "無額外語言",
        "feature": "黑道線人 (Criminal Contact)：擁有專屬且可靠的地下黑市聯絡人，能在城鎮中迅速調集走私情報。"
    },
    "變體罪犯 (間諜) (Spy)": {
        "skills_options": "固定熟練：【欺瞞】、【隱匿】",
        "tool_options": "固定熟練：【盜賊工具組】；易容工具組",
        "language_options": "無額外語言",
        "feature": "特務聯絡網 (Spy Contact)：掌握密碼信件渠道與秘密暗號，能隨時向所屬情報機構傳遞與收取密令。"
    },
    "詐欺師 (Charlatan)": {
        "skills_options": "固定熟練：【欺瞞】、【手上把戲】",
        "tool_options": "固定熟練：偽造工具組、易容工具組",
        "language_options": "無額外語言",
        "feature": "虛假身分 (False Identity)：擁有第二套完整的偽造身分與官方文件，並能輕易偽造他人書信簽名與印章。"
    },
    "貴族 (Noble)": {
        "skills_options": "固定熟練：【歷史】、【說服】",
        "tool_options": "自選一項博弈工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "特權階級 (Position of Privilege)：在上流社會廣受尊重，平民給予禮遇並可輕易獲見當地統治領主。"
    },
    "變體貴族 (騎士) (Knight)": {
        "skills_options": "固定熟練：【歷史】、【說服】",
        "tool_options": "自選一項博弈工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "騎士隨從 (Retainers)：擁有 3 名忠誠侍從（管家、信使與馬夫），照料日常生活並代為跑腿雜務。"
    },
    "深水城貴族 (Waterdhavian Noble)": {
        "skills_options": "固定熟練：【歷史】、【說服】",
        "tool_options": "自選一項博弈工具或樂器",
        "language_options": "自選任意 1 種額外語言",
        "feature": "名門風華 (Kept in Style)：靠著家族龐大信貸與聲望，在各大城邦可過上極其奢華的生活且由家族莊園埋單。"
    },
    "遠行者 (Far Traveler)": {
        "skills_options": "固定熟練：【洞察】、【察覺】",
        "tool_options": "一種樂器或博弈工具",
        "language_options": "自選任意 1 種額外語言",
        "feature": "眾目焦點 (All Eyes on You)：異域獨特打扮與舉止引發學者與貴族的好奇熱忱，能輕易獲邀出席重要社交名宴。"
    },
    "噩夢纏身 (Haunted One)": {
        "skills_options": "從【奧秘】、【調查】、【宗教】、【求生】中自選 2 項",
        "tool_options": "無特定工具",
        "language_options": "自選一種珍奇語言（深淵語/煉獄語/龍語/木族語等）",
        "feature": "恐懼同理 (Heart of Darkness)：常人感受得到你眼中經歷過的不可名狀恐怖，平民敬畏你並願竭力伸出援手。"
    },
    "阿沙里人 (Ashari)": {
        "skills_options": "固定熟練：【自然】、【求生】",
        "tool_options": "固定熟練：草藥師工具組",
        "language_options": "自選一種元素原初語言",
        "feature": "元素親和 (Elemental Harmony)：熟知四元素裂隙動向，在元素荒野聚落中享有同胞般的崇高禮遇。"
    },
    "魔法學院學者 (Lyceum Scholar)": {
        "skills_options": "固定熟練：【奧秘】；加上歷史/說服自選一項",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "學術特權 (Academic Privilege)：享有使用各大法師塔實驗室、施法材料庫與奧術傳送門的特權。"
    },
    "扣環黨成員 (Clasp Member)": {
        "skills_options": "固定熟練：【欺瞞】、【手上把戲】",
        "tool_options": "從易容工具、偽造工具或盜賊工具中自選一項",
        "language_options": "無額外語言",
        "feature": "盜賊密話 (A Thief and Their Tools)：透過地下盜賊網絡迅速獲取地下安全屋鑰匙與黑市走私渠道。"
    },
    "重回正途的邪教徒 (Reformed Cultist)": {
        "skills_options": "固定熟練：【欺瞞】、【宗教】",
        "tool_options": "偽造工具組",
        "language_options": "深淵語或煉獄語",
        "feature": "昔日邪教徒人脈 (Dark Secrets)：通曉邪教儀式密碼暗號，能識破潛伏在正常城鎮中的狂熱秘密崇拜聚會。"
    },
    "一無所有者 (Deprived)": {
        "skills_options": "固定熟練：【運動】、【求生】",
        "tool_options": "即興工具製作",
        "language_options": "無額外語言",
        "feature": "絕境求生 (Tenacious Survivor)：在沒有任何裝備物資的赤貧極端狀態下，仍能憑雙手存活並製作簡易工具。"
    },
    "俄佐立參議院官員 (Azorius Functionary)": {
        "skills_options": "固定熟練：【洞察】、【威嚇】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "律法威嚴 (Legal Authority)：執掌市政法典，可依法審問嫌疑犯並調閱官方公共治安檔案。"
    },
    "波洛斯教團軍團兵 (Boros Legionnaire)": {
        "skills_options": "固定熟練：【運動】、【威嚇】",
        "tool_options": "自選一項博弈工具",
        "language_options": "天界語或地精語",
        "feature": "要塞駐防 (Fortress Garrison)：可在教團各大守備要塞獲得免費食宿、裝備維修與天界戰友治療支援。"
    },
    "析米克聯合科學家 (Simic Scientist)": {
        "skills_options": "固定熟練：【奧秘】、【醫藥】",
        "tool_options": "煉金工具組或草藥工具組",
        "language_options": "自選任意 2 種額外語言",
        "feature": "生化實驗室 (Researcher's Access)：調用聯合培養生化實驗室設備，隨時進行物種基因與藥劑研究。"
    },
    "歐佐夫辛迪加代表 (Orzhov Representative)": {
        "skills_options": "固定熟練：【欺瞞】、【洞察】",
        "tool_options": "無特定工具",
        "language_options": "自選任意 2 種額外語言",
        "feature": "債務拘束 (Leverage & Debt)：掌握大量平民與商人的借據契約，能以債務威脅迫使當地人提供協助。"
    },
    "伊捷聯盟工程師 (Izzet Engineer)": {
        "skills_options": "固定熟練：【奧秘】、【調查】",
        "tool_options": "自選一項工匠工具",
        "language_options": "龍語或侏儒語",
        "feature": "魔導設施調用 (Urban Infrastructure)：熟知城市地下管線、魔導蒸汽鍋爐架構，通行地下機關密道。"
    },
    "拉鐸司宗派狂歡者 (Cult of Rakdos)": {
        "skills_options": "固定熟練：【特技】、【表演】",
        "tool_options": "自選一種樂器或製毒工具",
        "language_options": "深淵語",
        "feature": "恐怖狂歡盛宴 (Fearless Feat)：以血腥華麗的火圈特技表演吸引大批群眾，輕易製造混亂分散衛兵注意。"
    },
    "古魯部族混亂者 (Gruul Anarch)": {
        "skills_options": "固定熟練：【馴獸】、【自然】",
        "tool_options": "草藥工具組",
        "language_options": "巨人語",
        "feature": "廢墟生存 (Rubble Dweller)：在城市廢墟與荒廢街區中穿行自如，辨識殘骸中隱蔽的巢穴與獵物蹤跡。"
    },
    "瑟雷尼亞盟會新倡者 (Selesnya Initiate)": {
        "skills_options": "固定熟練：【自然】、【說服】",
        "tool_options": "一種工匠工具或樂器",
        "language_options": "精靈語或木族語",
        "feature": "萬物同心 (Communal Life)：同道盟友如親兄弟，在盟會任意花園神殿均享有豐盛免費食宿與心靈撫慰。"
    },
    "葛加理群落特工 (Golgari Agent)": {
        "skills_options": "固定熟練：【自然】、【求生】",
        "tool_options": "製毒工具組",
        "language_options": "精靈語",
        "feature": "下水道暗行 (Undercity Paths)：熟悉遍佈城市地底的腐朽下水道網絡，能避開一切地表監視暗中長途移動。"
    },
    "底密爾會堂特工 (House Dimir)": {
        "skills_options": "固定熟練：【欺瞞】、【隱匿】",
        "tool_options": "易容工具組",
        "language_options": "自選任意 1 種額外語言",
        "feature": "偽裝身分 (False Persona)：擁有完美潛入另一公會的第二套合法身分，秘密傳遞深層諜報暗號。"
    }
}

# ==========================================
# 7. 信仰神祇與語言庫
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
# 8. 獨特非傳統特質庫 (超常能力/自訂天賦)
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
# 9. 所屬陣營庫 (D&D 5E Alignments)
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
# 10. 趣味非典型武器庫 (Thematic & Unorthodox Weapons for NPCs)
# 讓市井農夫、屠夫、老兵、工匠也能擁有合情合理且帶感的戰鬥工具
# ==========================================
THEMATIC_CUSTOM_WEAPONS = [
    {
        "keywords": ["草耙", "長草耙", "麥耙", "鐵耙", "耙子", "耙", "rake"],
        "name": "鋼齒長草耙 (Steel-Toothed Farm Rake)",
        "type": "農具 / 改裝雙手長柄武器",
        "damage": "1d8 (雙手 1d10) 穿刺",
        "properties": "多用 (Versatile)、長柄武器、重擊時可嘗試進行推撞伏地"
    },
    {
        "keywords": ["草叉", "乾草叉", "叉子", "草叉子", "pitchfork", "fork"],
        "name": "強化鐵製乾草叉 (Reinforced Pitchfork)",
        "type": "農具 / 近戰刺擊武器",
        "damage": "1d6 (雙手 1d8) 穿刺",
        "properties": "投擲 (射程 20/60)、多用"
    },
    {
        "keywords": ["鐵鎬", "鶴嘴鎬", "鎬子", "十字鎬", "鎬", "pick", "pickaxe"],
        "name": "厚重礦工鎬 (Heavy Mining Pick)",
        "type": "採礦工具 / 破甲武器",
        "damage": "1d8 穿刺",
        "properties": "多用 (雙手 1d10)、對厚重護甲具有破甲破壞感"
    },
    {
        "keywords": ["剁刀", "剁骨刀", "砍刀", "菜刀", "斬骨刀", "屠刀", "骨刀", "cleaver", "knife"],
        "name": "沈重剁骨刀 (Heavy Bone-Cleaver)",
        "type": "屠宰刀具 / 近戰劈砍武器",
        "damage": "1d6 (雙手 1d8) 揮砍",
        "properties": "輕型 (Light)、靈巧 (Finesse)、破骨重擊"
    },
    {
        "keywords": ["手杖", "盲杖", "拐杖", "木杖", "長杖", "cane", "walking stick"],
        "name": "包鉛厚橡木手杖 (Lead-Weighted Walking Cane)",
        "type": "隨身手杖 / 隱蔽近戰武器",
        "damage": "1d6 (雙手 1d8) 鈍擊",
        "properties": "多用、外表極似日常拄行工具，不易被衛兵查扣"
    },
    {
        "keywords": ["鐵錘", "大方錘", "鍛造大錘", "大鐵錘", "大錘", "鍛錘", "sledgehammer", "hammer"],
        "name": "鍛造大方錘 (Blacksmith's Sledgehammer)",
        "type": "鐵匠工具 / 近戰重鈍武器",
        "damage": "2d6 鈍擊",
        "properties": "重型、雙手、猛擊碎骨"
    },
    {
        "keywords": ["魚叉", "捕鯨矛", "捕鯨叉", "獵叉", "harpoon"],
        "name": "倒鉤捕鯨矛 (Barbed Whaling Harpoon)",
        "type": "漁民獵具 / 遠程投擲武器",
        "damage": "1d8 穿刺",
        "properties": "投擲 (射程 30/120)、帶細麻繩可將命中目標拉扯回身旁"
    },
    {
        "keywords": ["撬棍", "鐵撬", "重鐵撬", "crowbar"],
        "name": "染血生鏽鐵撬 (Bloodstained Heavy Crowbar)",
        "type": "破拆工具 / 即興近戰鈍器",
        "damage": "1d4 (雙手 1d6) 鈍擊",
        "properties": "破拆門扉檢定優勢、實心硬生鐵"
    }
]

# ==========================================
# 11. 獨特非傳統施法法器庫 (Eccentric & Non-Traditional Arcane Focuses)
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
