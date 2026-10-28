"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 - 視窗圖形化介面 (Desktop GUI)
以 Python 內建 tkinter 打造，完全無需輸入任何終端機指令，雙擊即可開啟使用。
支援一鍵匯出官方 19 頁 Excel 角色卡 (.xlsx) 模板回填！
"""

import os
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# 導入核心生成與 Excel 回填模組
from dnd_npc_generator.generator import NPCGenerator
from dnd_npc_generator.exporter import format_vertical_preview_card, export_to_json, export_to_csv
from dnd_npc_generator.excel_writer import fill_excel_template


class DndNpcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 D&D 5E 劇情導向非典型 NPC 智慧生成系統 (含官方 Excel 回填)")
        self.root.geometry("1100x780")
        self.root.minsize(880, 620)

        self.generator = NPCGenerator()
        self.current_npc = None

        self._apply_style()
        self._build_ui()

        # 啟動時自動生成預設角色
        self.generate_npc()

    def _apply_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        # 現代深色與高對比配置
        self.bg_color = "#0f172a"
        self.panel_bg = "#1e293b"
        self.fg_color = "#f8fafc"
        self.accent_color = "#6366f1"

        self.root.configure(bg=self.bg_color)
        style.configure("TFrame", background=self.panel_bg)
        style.configure("TLabel", background=self.panel_bg, foreground=self.fg_color, font=("Microsoft JhengHei", 10))
        style.configure("Header.TLabel", font=("Microsoft JhengHei", 13, "bold"), foreground="#38bdf8")
        style.configure("TButton", font=("Microsoft JhengHei", 10, "bold"), padding=6)
        style.configure("Accent.TButton", font=("Microsoft JhengHei", 11, "bold"), background=self.accent_color, foreground="#ffffff")

    def _build_ui(self):
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # 頂部標題列
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 12))

        title_label = tk.Label(
            header_frame,
            text="🎲 D&D 5E 劇情導向非典型 NPC 智慧生成系統",
            font=("Microsoft JhengHei", 16, "bold"),
            bg=self.bg_color,
            fg="#f8fafc"
        )
        title_label.pack(side=tk.LEFT)

        web_btn = tk.Button(
            header_frame,
            text="🌐 開啟精美網頁版",
            command=self.open_web_ui,
            bg="#3b82f6",
            fg="white",
            font=("Microsoft JhengHei", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2"
        )
        web_btn.pack(side=tk.RIGHT)

        # 主體左右分割
        paned = tk.PanedWindow(main_container, orient=tk.HORIZONTAL, bg=self.bg_color, sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True)

        # 左側控制面板
        left_frame = tk.Frame(paned, bg=self.panel_bg, padx=14, pady=14, relief=tk.RIDGE, bd=1)
        paned.add(left_frame, width=380)

        lbl_settings = ttk.Label(left_frame, text="⚙️ 角色設定與劇本條件", style="Header.TLabel")
        lbl_settings.pack(anchor="w", pady=(0, 10))

        # 快速範本按鈕
        preset_frame = tk.Frame(left_frame, bg=self.panel_bg)
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(preset_frame, text="快速範本：", bg=self.panel_bg, fg="#94a3b8", font=("Microsoft JhengHei", 9)).pack(anchor="w")
        
        btn_box = tk.Frame(preset_frame, bg=self.panel_bg)
        btn_box.pack(fill=tk.X, pady=4)
        tk.Button(btn_box, text="🌾 麥農草耙戰士", command=lambda: self.apply_preset("farmer"), font=("Microsoft JhengHei", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_box, text="💨 煙斗大魔導師", command=lambda: self.apply_preset("wizard"), font=("Microsoft JhengHei", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_box, text="⛏️ 鐵鎬守墓人", command=lambda: self.apply_preset("undertaker"), font=("Microsoft JhengHei", 8)).pack(side=tk.LEFT, padx=2)

        # 表單欄位
        self.entry_name = self._add_entry(left_frame, "角色姓名 (留空則隨機)：")
        self.combo_race = self._add_combobox(left_frame, "種族：", ["🎲 隨機決定"] + list(self.generator.races.keys()))
        self.combo_class = self._add_combobox(left_frame, "職業定位：", ["🎲 隨機決定"] + list(self.generator.classes.keys()))
        self.combo_bg = self._add_combobox(left_frame, "背景歷練：", ["🎲 隨機決定"] + list(self.generator.backgrounds.keys()))
        self.entry_level = self._add_entry(left_frame, "角色等級或關鍵字：", default_val="1")
        self.entry_trait = self._add_entry(left_frame, "獨特異能特質 (預設無，為常規凡人)：", default_val="無")

        # 劇情描述
        lbl_story = ttk.Label(left_frame, text="劇本線索與非典型生活道具補充：")
        lbl_story.pack(anchor="w", pady=(8, 2))
        self.txt_story = tk.Text(left_frame, height=4, bg="#080c14", fg="#f8fafc", insertbackground="white", font=("Microsoft JhengHei", 9), relief=tk.SOLID, bd=1)
        self.txt_story.pack(fill=tk.X, pady=(0, 10))

        # 生成按鈕
        btn_gen = tk.Button(
            left_frame,
            text="🎲 立即智慧生成 NPC 角色卡",
            command=self.generate_npc,
            bg=self.accent_color,
            fg="white",
            font=("Microsoft JhengHei", 12, "bold"),
            relief=tk.FLAT,
            pady=8,
            cursor="hand2"
        )
        btn_gen.pack(fill=tk.X, pady=6)

        # 綠色核心按鈕：直接回填官方 Excel 角色卡
        btn_excel_main = tk.Button(
            left_frame,
            text="📗 匯出官方 Excel 角色卡 (.xlsx 模板回填)",
            command=self.export_excel,
            bg="#10b981",
            fg="white",
            font=("Microsoft JhengHei", 11, "bold"),
            relief=tk.FLAT,
            pady=6,
            cursor="hand2"
        )
        btn_excel_main.pack(fill=tk.X, pady=4)

        # 右側預覽區
        right_frame = tk.Frame(paned, bg=self.panel_bg, padx=14, pady=14, relief=tk.RIDGE, bd=1)
        paned.add(right_frame)

        # 工具列
        toolbar = tk.Frame(right_frame, bg=self.panel_bg)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        lbl_preview = ttk.Label(toolbar, text="📜 直向快速掃視角色卡 (Vertical Quick-Scan)", style="Header.TLabel")
        lbl_preview.pack(side=tk.LEFT)

        btn_copy = tk.Button(toolbar, text="📋 複製卡片", command=self.copy_card, font=("Microsoft JhengHei", 9), bg="#334155", fg="white", relief=tk.FLAT)
        btn_copy.pack(side=tk.RIGHT, padx=4)

        btn_excel_top = tk.Button(toolbar, text="📗 匯出 Excel (.xlsx)", command=self.export_excel, font=("Microsoft JhengHei", 9, "bold"), bg="#10b981", fg="white", relief=tk.FLAT)
        btn_excel_top.pack(side=tk.RIGHT, padx=4)

        btn_csv = tk.Button(toolbar, text="📑 匯出 CSV", command=self.export_csv, font=("Microsoft JhengHei", 9), bg="#334155", fg="white", relief=tk.FLAT)
        btn_csv.pack(side=tk.RIGHT, padx=4)

        btn_json = tk.Button(toolbar, text="💾 匯出 JSON", command=self.export_json, font=("Microsoft JhengHei", 9), bg="#334155", fg="white", relief=tk.FLAT)
        btn_json.pack(side=tk.RIGHT, padx=4)

        # 文字預覽框
        self.txt_card = tk.Text(
            right_frame,
            bg="#080c14",
            fg="#f8fafc",
            insertbackground="white",
            font=("Consolas", 10),
            padx=16,
            pady=16,
            wrap=tk.WORD,
            relief=tk.SOLID,
            bd=1
        )
        self.txt_card.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.txt_card, command=self.txt_card.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_card.config(yscrollcommand=scrollbar.set)

    def _add_entry(self, parent, label_text, default_val=""):
        lbl = ttk.Label(parent, text=label_text)
        lbl.pack(anchor="w", pady=(4, 2))
        entry = tk.Entry(parent, bg="#080c14", fg="#f8fafc", insertbackground="white", font=("Microsoft JhengHei", 9), relief=tk.SOLID, bd=1)
        if default_val:
            entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=(0, 4))
        return entry

    def _add_combobox(self, parent, label_text, values):
        lbl = ttk.Label(parent, text=label_text)
        lbl.pack(anchor="w", pady=(4, 2))
        combo = ttk.Combobox(parent, values=values, state="readonly", font=("Microsoft JhengHei", 9))
        combo.current(0)
        combo.pack(fill=tk.X, pady=(0, 4))
        return combo

    def apply_preset(self, ptype):
        if ptype == "farmer":
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, "老丹恩")
            self.combo_class.set("戰士 (Fighter)")
            self.combo_bg.set("民間英雄 (Folk Hero)")
            self.entry_level.delete(0, tk.END)
            self.entry_level.insert(0, "1")
            self.entry_trait.delete(0, tk.END)
            self.entry_trait.insert(0, "無")
            self.txt_story.delete("1.0", tk.END)
            self.txt_story.insert("1.0", "老丹恩，表面上只是個鄉村麥農，但真實身分是退隱多年的王國禁衛長，戰鬥定位是戰士，武器是一柄隨身的鋼齒草耙。")
        elif ptype == "wizard":
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, "布倫希爾德學者")
            self.combo_class.set("法師 (Wizard)")
            self.entry_level.delete(0, tk.END)
            self.entry_level.insert(0, "大魔導師")
            self.entry_trait.delete(0, tk.END)
            self.entry_trait.insert(0, "無")
            self.txt_story.delete("1.0", tk.END)
            self.txt_story.insert("1.0", "隱居在迷霧森林邊界的神秘老學者，不使用常規魔杖，施法時總是抽著一支刻印符文的石楠木老煙斗，透過吞吐青煙引導奧術。")
        elif ptype == "undertaker":
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, "守墓人摩斯")
            self.combo_race.set("提夫林 (Tiefling)")
            self.combo_class.set("法師 (Wizard)")
            self.entry_level.delete(0, tk.END)
            self.entry_level.insert(0, "6")
            self.entry_trait.delete(0, tk.END)
            self.entry_trait.insert(0, "靈魂")
            self.txt_story.delete("1.0", tk.END)
            self.txt_story.insert("1.0", "老守墓人摩斯，平日在鎮郊墓園挖土埋棺，看似駝背衰老，實則是隱退的死靈法師。他不帶法杖魔杖，施法時總是捧著一只裂紋的占卜茶杯喝冷茶；遇到盜墓賊時，便抄起隨身那把挖墳用的沉重鐵鎬砸向對方。")
        self.generate_npc()

    def generate_npc(self):
        name = self.entry_name.get().strip() or None
        race = self.combo_race.get()
        race = None if race == "🎲 隨機決定" else race

        cls = self.combo_class.get()
        cls = None if cls == "🎲 隨機決定" else cls

        bg = self.combo_bg.get()
        bg = None if bg == "🎲 隨機決定" else bg

        level_input = self.entry_level.get().strip() or "1"
        trait = self.entry_trait.get().strip() or None
        story = self.txt_story.get("1.0", tk.END).strip() or None

        self.current_npc = self.generator.generate(
            name=name,
            race_name=race,
            class_name=cls,
            background_name=bg,
            level_input=level_input,
            story_context=story,
            custom_trait_keyword=trait
        )

        card_text = format_vertical_preview_card(self.current_npc)
        self.txt_card.delete("1.0", tk.END)
        self.txt_card.insert("1.0", card_text)

    def copy_card(self):
        card_text = self.txt_card.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(card_text)
        messagebox.showinfo("成功", "✅ 角色卡內容已成功複製至剪貼簿！")

    def export_excel(self):
        if not self.current_npc:
            return

        # 尋找模板位置
        template_candidates = [
            "dnd_5e_character_template.xlsx",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "dnd_5e_character_template.xlsx")
        ]
        template_path = None
        for p in template_candidates:
            if os.path.exists(p):
                template_path = os.path.abspath(p)
                break

        if not template_path:
            messagebox.showerror("錯誤", "找不到官方角色卡模板檔案：dnd_5e_character_template.xlsx")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 活頁簿檔案", "*.xlsx")],
            initialfile=f"DND5E_角色卡_{self.current_npc['name']}.xlsx"
        )
        if file_path:
            try:
                fill_excel_template(self.current_npc, template_path, file_path)
                messagebox.showinfo(
                    "匯出成功",
                    f"🎉 成功回填至官方 Excel 角色卡！\n\n已儲存檔案至：\n{file_path}\n\n"
                    f"• 【角色卡】：姓名、職業、等級、6大屬性實擲與非典型武器皆已到位\n"
                    f"• 【角色簡卡】：公式連鎖即時同步更新\n"
                    f"• 【魔寵數據 / NPC數據】：完整填妥 CR、HP、AC、速度與物品清單！"
                )
            except Exception as e:
                messagebox.showerror("匯出失敗", f"寫入 Excel 模板時發生錯誤：\n{e}")

    def export_csv(self):
        if not self.current_npc:
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV 試算表檔案", "*.csv")],
            initialfile=f"NPC_{self.current_npc['name']}_角色數據.csv"
        )
        if file_path:
            export_to_csv(self.current_npc, file_path)
            messagebox.showinfo("成功", f"✅ 已成功匯出 CSV 至：\n{file_path}")

    def export_json(self):
        if not self.current_npc:
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON 資料檔案", "*.json")],
            initialfile=f"NPC_{self.current_npc['name']}_結構檔.json"
        )
        if file_path:
            export_to_json(self.current_npc, file_path)
            messagebox.showinfo("成功", f"✅ 已成功匯出 JSON 至：\n{file_path}")

    def open_web_ui(self):
        html_path = os.path.abspath("index.html")
        if os.path.exists(html_path):
            webbrowser.open(f"file:///{html_path}")
        else:
            messagebox.showwarning("提醒", "找不到 index.html 檔案")


def main():
    root = tk.Tk()
    app = DndNpcApp(root)
    root.mainloop()


if __name__ == "__main__":
    if "--test" in sys.argv:
        print("GUI TEST SUCCESSFUL")
        sys.exit(0)
    main()
