"""
4d6dl1 骰子產生器與靈活配置模組
特色：
1. 完整保留 4d6 去除最低值 (4d6 drop lowest 1) 的原始擲骰明細
2. 不強行寫死卡片屬性，而是提供「建議配置方案」供 DM/玩家自由參考
3. 獨立列出「種族加值可提升清單」，保留玩家自主調整空間
"""

import random
from typing import Dict, List, Tuple


def roll_4d6_drop_lowest() -> Tuple[int, List[int], int]:
    """
    擲 4 顆六面骰 (4d6)，扣除最低點數，回傳 (總和, 4顆骰子列表, 扣除的最低點數)
    """
    dice = [random.randint(1, 6) for _ in range(4)]
    dice_sorted = sorted(dice, reverse=True)
    kept = dice_sorted[:3]
    dropped = dice_sorted[3]
    return sum(kept), dice, dropped


def calculate_modifier(score: int) -> int:
    """
    計算 D&D 5E 屬性調整值：(屬性值 - 10) // 2
    """
    return (score - 10) // 2


def format_modifier(mod: int) -> str:
    """
    格式化調整值為字串，如 +3, +0, -1
    """
    return f"+{mod}" if mod >= 0 else str(mod)


def generate_ability_rolls() -> List[Dict]:
    """
    擲出 6 組完整的 4d6dl1 點數
    """
    results = []
    for _ in range(6):
        total, dice, dropped = roll_4d6_drop_lowest()
        results.append({
            "score": total,
            "dice": dice,
            "dropped": dropped
        })
    # 按點數高低排序，方便檢視點數池
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def build_recommended_allocation(rolled_scores: List[int], class_name: str) -> Dict[str, int]:
    """
    依照職業特性給予最佳化配置「建議」（非強制寫死）
    """
    sorted_scores = sorted(rolled_scores, reverse=True)
    
    # 職業核心主副屬性推薦優先權
    priority_map = {
        "戰士": ["STR", "CON", "DEX", "WIS", "CHA", "INT"],
        "野蠻人": ["STR", "CON", "DEX", "WIS", "CHA", "INT"],
        "遊盪者": ["DEX", "CON", "INT", "WIS", "CHA", "STR"],
        "盜賊": ["DEX", "CON", "INT", "WIS", "CHA", "STR"],
        "法師": ["INT", "CON", "DEX", "WIS", "CHA", "STR"],
        "牧師": ["WIS", "CON", "STR", "DEX", "CHA", "INT"],
        "聖騎士": ["STR", "CHA", "CON", "WIS", "DEX", "INT"]
    }

    # 模糊比對職業名稱
    chosen_priority = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for k, p in priority_map.items():
        if k in class_name:
            chosen_priority = p
            break

    recommendation = {}
    for i, stat in enumerate(chosen_priority):
        recommendation[stat] = sorted_scores[i]

    return recommendation
