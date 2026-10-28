"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 (TRPG Story-Driven Unorthodox NPC Generator)
"""

from .generator import NPCGenerator
from .roller import (
    roll_4d6_drop_lowest,
    calculate_modifier,
    format_modifier,
    generate_ability_rolls,
    build_recommended_allocation
)
from .exporter import (
    format_vertical_preview_card,
    export_to_json,
    export_to_csv,
    get_flattened_dict_for_excel,
    render_markdown_card,
    export_json,
    export_csv
)
from .excel_writer import fill_excel_template

__all__ = [
    "NPCGenerator",
    "roll_4d6_drop_lowest",
    "calculate_modifier",
    "format_modifier",
    "generate_ability_rolls",
    "build_recommended_allocation",
    "format_vertical_preview_card",
    "export_to_json",
    "export_to_csv",
    "get_flattened_dict_for_excel",
    "render_markdown_card",
    "export_json",
    "export_csv",
    "fill_excel_template"
]
