"""
D&D 5E 劇情導向非典型 NPC 智慧生成系統 - 視窗圖形化介面 (Desktop GUI)
以 Python 內建 tkinter 打造，完全無需輸入任何終端機指令，雙擊即可開啟使用。
專為 TRPG 地下城主 (DM) 設計，支援快速直向掃視角色卡、靈活屬性推薦、客製化等級與多格式匯出 (Markdown/CSV/JSON)。
"""

import os
import sys
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# 導入核心生成模組
from dnd_npc_generator.ai_generator import AINPCGenerator
from dnd_npc_generator.exporter import format_vertical_preview_card, export_to_json, export_to_csv


class DndNpcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 D&D 5E 劇情導向非典型 NPC 智慧生成系統 (Gemini AI 原創敘事版)")
        self.root.geometry("1120x800")
        self.root.minsize(900, 640)

        self.generator = AINPCGenerator()
        self.current_npc = None
        self.is_generating = False

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
        self.accent_hover = "#4f46e5"

        self.root.configure(bg=self.bg_color)

        style.configure("TFrame", background=self.panel_bg)
        style.configure("TLabel", background=self.panel_bg, foreground=self.fg_color, font=("Microsoft JhengHei", 9))
        style.configure("Header.TLabel", font=("Microsoft JhengHei", 12, "bold"), foreground="#38bdf8")
        style.configure("Subheader.TLabel", font=("Microsoft JhengHei", 9, "bold"), foreground="#94a3b8")
        style.configure("TButton", font=("Microsoft JhengHei", 9), padding=5)

    def _build_ui(self):
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.bg_color, sashwidth=4)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ==========================================
        # 左側控制台 (Control Panel)
        # ==========================================
        left_container = tk.Frame(paned, bg=self.panel_bg, relief=tk.RIDGE, bd=1)
        paned.add(left_container, minsize=360, width=380)

        # 滾動畫布支援小螢幕
        canvas = tk.Canvas(left_container, bg=self.panel_bg, highlightthickness=0)
        scrollbar_left = tk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
        left_frame = tk.Frame(canvas, bg=self.panel_bg, padx=14, pady=12)

        left_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=left_frame, anchor="nw", width=360)
        canvas.configure(yscrollcommand=scrollbar_left.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_left.pack(side="right", fill="y")

        lbl_title = ttk.Label(left_frame, text="⚙️ NPC 劇情與規則客製控制台", style="Header.TLabel")
        lbl_title.pack(anchor="w", pady=(0, 6))

        # ==========================================
        # AI 智慧敘事核心設定區 (Gemini AI Engine)
        # ==========================================
        ai_box = tk.LabelFrame(
            left_frame,
            text=" 🤖 Gemini AI 智慧敘事設定 ",
            bg=self.panel_bg,
            fg="#38bdf8",
            font=("Microsoft JhengHei", 9, "bold"),
            padx=8,
            pady=6
        )
        ai_box.pack(fill=tk.X, pady=(0, 8))

        self.var_enable_ai = tk.BooleanVar(value=True)
        cb_ai = tk.Checkbutton(
            ai_box,
            text="啟用 Gemini AI 深度背景與裝備撰寫",
            variable=self.var_enable_ai,
            bg=self.panel_bg,
            fg="#f8fafc",
            selectcolor="#0f172a",
            activebackground=self.panel_bg,
            activeforeground="#38bdf8",
            font=("Microsoft JhengHei", 9, "bold")
        )
        cb_ai.pack(anchor="w", pady=(0, 4))

        key_row = tk.Frame(ai_box, bg=self.panel_bg)
        key_row.pack(fill=tk.X, pady=2)
        lbl_key = ttk.Label(key_row, text="Gemini API Key：", font=("Microsoft JhengHei", 8))
        lbl_key.pack(side=tk.LEFT)

        self.entry_api_key = tk.Entry(
            key_row,
            show="•",
            bg="#080c14",
            fg="#f8fafc",
            insertbackground="white",
            font=("Microsoft JhengHei", 8),
            relief=tk.SOLID,
            bd=1
        )
        # 嘗試填入環境已有的 API Key
        default_key = os.getenv("GEMINI_API_KEY", "")
        if default_key:
            self.entry_api_key.insert(0, default_key)
        self.entry_api_key.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 4))

        self.btn_toggle_key = tk.Button(
            key_row,
            text="👁️",
            command=self._toggle_key_visibility,
            bg="#334155",
            fg="white",
            font=("Microsoft JhengHei", 7),
            relief=tk.FLAT,
            padx=4,
            pady=1
        )
        self.btn_toggle_key.pack(side=tk.RIGHT)

        model_row = tk.Frame(ai_box, bg=self.panel_bg)
        model_row.pack(fill=tk.X, pady=2)
        lbl_model = ttk.Label(model_row, text="AI 模型：", font=("Microsoft JhengHei", 8))
        lbl_model.pack(side=tk.LEFT)
        self.combo_model = ttk.Combobox(
            model_row,
            values=["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash"],
            state="readonly",
            font=("Microsoft JhengHei", 8)
        )
        self.combo_model.current(0)
        self.combo_model.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # 快速範本預設集 (Presets)
        lbl_presets = ttk.Label(left_frame, text="快速載入非典型劇情範本：", style="Subheader.TLabel")
        lbl_presets.pack(anchor="w", pady=(4, 2))

        preset_box = tk.Frame(left_frame, bg=self.panel_bg)
        preset_box.pack(fill=tk.X, pady=(0, 8))

        btn_p1 = tk.Button(preset_box, text="🌾 老農戰士(鋼耙)", command=lambda: self.apply_preset("farmer"), font=("Microsoft JhengHei", 8), bg="#334155", fg="white", relief=tk.FLAT)
        btn_p1.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        btn_p2 = tk.Button(preset_box, text="📜 封印老法師(煙斗)", command=lambda: self.apply_preset("wizard"), font=("Microsoft JhengHei", 8), bg="#334155", fg="white", relief=tk.FLAT)
        btn_p2.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        btn_p3 = tk.Button(preset_box, text="⛏️ 守墓人(挖墳鐵鎬)", command=lambda: self.apply_preset("undertaker"), font=("Microsoft JhengHei", 8), bg="#334155", fg="white", relief=tk.FLAT)
        btn_p3.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        # 1. 角色名稱
        self.entry_name = self._add_entry(left_frame, "角色名稱 (留空則隨機生成)：", "")

        # 2. 種族下拉選單
        races = ["🎲 隨機決定", "人類 (Human)", "高等精靈 (High Elf)", "矮人 (Dwarf)", "半身人 (Halfling)", "提夫林 (Tiefling)", "龍裔 (Dragonborn)", "半獸人 (Half-Orc)", "侏儒 (Gnome)"]
        self.combo_race = self._add_combobox(left_frame, "種族：", races)

        # 3. 職業下拉選單
        classes = ["🎲 隨機決定", "戰士 (Fighter)", "法師 (Wizard)", "盜賊 (Rogue)", "野蠻人 (Barbarian)", "聖騎士 (Paladin)", "牧師 (Cleric)", "遊俠 (Ranger)", "武僧 (Monk)", "吟遊詩人 (Bard)", "德魯伊 (Druid)", "術士 (Sorcerer)", "契術師 (Warlock)", "平民百姓 (Commoner)"]
        self.combo_class = self._add_combobox(left_frame, "職業定位：", classes)

        # 4. 背景下拉選單
        backgrounds = ["🎲 隨機決定", "平民民兵 (Folk Hero)", "侍祭 (Acolyte)", "騙徒 (Charlatan)", "罪犯 (Criminal)", "藝人 (Entertainer)", "公會工匠 (Guild Artisan)", "隱士 (Hermit)", "貴族 (Noble)", "流浪兒 (Urchin)", "水手 (Sailor)", "士兵 (Soldier)"]
        self.combo_bg = self._add_combobox(left_frame, "背景歷練：", backgrounds)

        # 5. 等級自由輸入 (支援關鍵字如「大魔導師」、「Lv.14 (封印)」)
        self.entry_level = self._add_entry(left_frame, "等級或位階關鍵字 (如：1、大魔導師、6)：", "1")

        # 6. 非典型特質關鍵字 (支援「無」、「煙斗」、「鋼草耙」)
        self.entry_trait = self._add_entry(left_frame, "非典型特質關鍵字 (輸入「無」為常規凡人)：", "")

        # 7. 劇情情境與裝備自由描述
        lbl_story = ttk.Label(left_frame, text="故事設定與生活武器描述：")
        lbl_story.pack(anchor="w", pady=(4, 2))
        self.txt_story = tk.Text(left_frame, height=3, bg="#080c14", fg="#f8fafc", insertbackground="white", font=("Microsoft JhengHei", 9), relief=tk.SOLID, bd=1)
        self.txt_story.pack(fill=tk.X, pady=(0, 6))

        # 核心按鈕：立即生成
        self.btn_gen = tk.Button(
            left_frame,
            text="🎲 立即生成非典型 NPC (Generate)",
            command=self.generate_npc,
            bg=self.accent_color,
            fg="white",
            font=("Microsoft JhengHei", 11, "bold"),
            relief=tk.FLAT,
            pady=8,
            cursor="hand2"
        )
        self.btn_gen.pack(fill=tk.X, pady=(4, 8))

        # 快捷功能按鈕區
        action_box = tk.LabelFrame(left_frame, text=" 匯出與分享選項 ", bg=self.panel_bg, fg="#94a3b8", font=("Microsoft JhengHei", 9, "bold"), padx=8, pady=8)
        action_box.pack(fill=tk.X, pady=(0, 8))

        btn_copy_main = tk.Button(
            action_box,
            text="📋 複製直向預覽卡全文",
            command=self.copy_card,
            bg="#2563eb",
            fg="white",
            font=("Microsoft JhengHei", 10, "bold"),
            relief=tk.FLAT,
            pady=5,
            cursor="hand2"
        )
        btn_copy_main.pack(fill=tk.X, pady=(0, 4))

        export_row = tk.Frame(action_box, bg=self.panel_bg)
        export_row.pack(fill=tk.X, pady=2)

        btn_csv = tk.Button(
            export_row,
            text="📑 匯出 CSV 試算表",
            command=self.export_csv,
            bg="#334155",
            fg="white",
            font=("Microsoft JhengHei", 9),
            relief=tk.FLAT,
            pady=4,
            cursor="hand2"
        )
        btn_csv.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        btn_json = tk.Button(
            export_row,
            text="💾 匯出 JSON 資料檔",
            command=self.export_json,
            bg="#334155",
            fg="white",
            font=("Microsoft JhengHei", 9),
            relief=tk.FLAT,
            pady=4,
            cursor="hand2"
        )
        btn_json.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        btn_web = tk.Button(
            action_box,
            text="🌐 開啟 Web 視覺網頁版 (含列印/PDF)",
            command=self.open_web_ui,
            bg="#0f766e",
            fg="white",
            font=("Microsoft JhengHei", 9, "bold"),
            relief=tk.FLAT,
            pady=5,
            cursor="hand2"
        )
        btn_web.pack(fill=tk.X, pady=(4, 0))

        # ==========================================
        # 右側預覽區 (Vertical Card Preview)
        # ==========================================
        right_frame = tk.Frame(paned, bg=self.panel_bg, padx=14, pady=14, relief=tk.RIDGE, bd=1)
        paned.add(right_frame)

        # 工具列
        toolbar = tk.Frame(right_frame, bg=self.panel_bg)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        lbl_preview = ttk.Label(toolbar, text="📜 直向快速掃視角色卡 (Vertical Quick-Scan)", style="Header.TLabel")
        lbl_preview.pack(side=tk.LEFT)

        btn_web_top = tk.Button(toolbar, text="🌐 開啟 Web 版", command=self.open_web_ui, font=("Microsoft JhengHei", 9), bg="#0f766e", fg="white", relief=tk.FLAT)
        btn_web_top.pack(side=tk.RIGHT, padx=3)

        btn_json_top = tk.Button(toolbar, text="💾 匯出 JSON", command=self.export_json, font=("Microsoft JhengHei", 9), bg="#334155", fg="white", relief=tk.FLAT)
        btn_json_top.pack(side=tk.RIGHT, padx=3)

        btn_csv_top = tk.Button(toolbar, text="📑 匯出 CSV", command=self.export_csv, font=("Microsoft JhengHei", 9), bg="#334155", fg="white", relief=tk.FLAT)
        btn_csv_top.pack(side=tk.RIGHT, padx=3)

        btn_copy = tk.Button(toolbar, text="📋 複製卡片", command=self.copy_card, font=("Microsoft JhengHei", 9), bg="#2563eb", fg="white", relief=tk.FLAT)
        btn_copy.pack(side=tk.RIGHT, padx=3)

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
            self.combo_race.set("半身人 (Halfling)")
            self.combo_class.set("戰士 (Fighter)")
            self.combo_bg.set("平民民兵 (Folk Hero)")
            self.entry_level.delete(0, tk.END)
            self.entry_level.insert(0, "1")
            self.entry_trait.delete(0, tk.END)
            self.entry_trait.insert(0, "無")
            self.txt_story.delete("1.0", tk.END)
            self.txt_story.insert("1.0", "老丹恩，表面上只是個鄉村麥農，但真實身分是退隱多年的王國禁衛長，戰鬥定位是戰士，武器是一柄隨身的鋼齒草耙。")
        elif ptype == "wizard":
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, "布倫希爾德學者")
            self.combo_race.set("高等精靈 (High Elf)")
            self.combo_class.set("法師 (Wizard)")
            self.combo_bg.set("隱士 (Hermit)")
            self.entry_level.delete(0, tk.END)
            self.entry_level.insert(0, "大魔導師 (能力封印)")
            self.entry_trait.delete(0, tk.END)
            self.entry_trait.insert(0, "無")
            self.txt_story.delete("1.0", tk.END)
            self.txt_story.insert("1.0", "隱居在迷霧森林邊界的神秘老學者，不使用常規魔杖，施法時總是抽著一支刻印符文的石楠木老煙斗，透過吞吐青煙引導奧術。")
        elif ptype == "undertaker":
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, "守墓人摩斯")
            self.combo_race.set("提夫林 (Tiefling)")
            self.combo_class.set("法師 (Wizard)")
            self.combo_bg.set("流浪兒 (Urchin)")
            self.entry_level.delete(0, tk.END)
            self.entry_level.insert(0, "6")
            self.entry_trait.delete(0, tk.END)
            self.entry_trait.insert(0, "靈魂")
            self.txt_story.delete("1.0", tk.END)
            self.txt_story.insert("1.0", "老守墓人摩斯，平日在鎮郊墓園挖土埋棺，看似駝背衰老，實則是隱退的死靈法師。他不帶法杖魔杖，施法時總是捧著一只裂紋的占卜茶杯喝冷茶；遇到盜墓賊時，便抄起隨身那把挖墳用的沉重鐵鎬砸向對方。")
        self.generate_npc()

    def _toggle_key_visibility(self):
        if self.entry_api_key.cget("show") == "":
            self.entry_api_key.config(show="•")
            self.btn_toggle_key.config(text="👁️")
        else:
            self.entry_api_key.config(show="")
            self.btn_toggle_key.config(text="🔒")

    def generate_npc(self):
        if self.is_generating:
            return

        name = self.entry_name.get().strip() or None
        race = self.combo_race.get()
        race = None if "隨機" in race else race

        cls = self.combo_class.get()
        cls = None if "隨機" in cls else cls

        bg = self.combo_bg.get()
        bg = None if "隨機" in bg else bg

        level_input = self.entry_level.get().strip() or "1"
        trait = self.entry_trait.get().strip() or None
        story = self.txt_story.get("1.0", tk.END).strip() or None

        enable_ai = self.var_enable_ai.get()
        api_key = self.entry_api_key.get().strip() or None
        model = self.combo_model.get()

        self.is_generating = True
        self.btn_gen.config(text="⏳ 🤖 AI 正在創作身世與裝備規格中...", state=tk.DISABLED, bg="#475569")
        
        self.txt_card.delete("1.0", tk.END)
        self.txt_card.insert(
            "1.0",
            "# 🤖 【Gemini AI 智慧敘事核心運算中】\n\n"
            f"> 正在為角色【{name or '隨機市井人物'}】創作具有生活反差的身世短史...\n"
            "> 正在將日常生活物品規格化為符合 D&D 5E 平衡的非典型武器/法器...\n"
            "> 正在整理 4d6dl1 靈活屬性推薦面板與 DM 跑團互動伏筆...\n\n"
            "⏳ 請稍候約 3~10 秒..."
        )

        def worker():
            try:
                gen = AINPCGenerator(api_key=api_key, model_name=model)
                npc = gen.generate(
                    name=name,
                    race_name=race,
                    class_name=cls,
                    background_name=bg,
                    level_input=level_input,
                    story_context=story,
                    custom_trait_keyword=trait,
                    force_ai=enable_ai
                )
                card_text = format_vertical_preview_card(npc)

                def on_done():
                    self.current_npc = npc
                    self.txt_card.delete("1.0", tk.END)
                    self.txt_card.insert("1.0", card_text)
                    self.btn_gen.config(text="🎲 立即生成非典型 NPC (Generate)", state=tk.NORMAL, bg=self.accent_color)
                    self.is_generating = False

                self.root.after(0, on_done)
            except Exception as e:
                def on_err():
                    try:
                        gen = AINPCGenerator()
                        npc = gen.generate(
                            name=name,
                            race_name=race,
                            class_name=cls,
                            background_name=bg,
                            level_input=level_input,
                            story_context=story,
                            custom_trait_keyword=trait,
                            force_ai=False
                        )
                        self.current_npc = npc
                        card_text = format_vertical_preview_card(npc)
                        self.txt_card.delete("1.0", tk.END)
                        self.txt_card.insert("1.0", card_text)
                    except Exception as fallback_err:
                        self.txt_card.delete("1.0", tk.END)
                        self.txt_card.insert("1.0", f"❌ 生成失敗: {e}\n後備生成失敗: {fallback_err}")
                    
                    self.btn_gen.config(text="🎲 立即生成非典型 NPC (Generate)", state=tk.NORMAL, bg=self.accent_color)
                    self.is_generating = False

                self.root.after(0, on_err)

        threading.Thread(target=worker, daemon=True).start()

    def copy_card(self):
        card_text = self.txt_card.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(card_text)
        messagebox.showinfo("成功", "✅ 直式角色卡預覽內容已成功複製至剪貼簿！")

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
            messagebox.showinfo("成功", f"✅ 已成功匯出通用 CSV 至：\n{file_path}\n可直接使用 Excel 或 Google 試算表開啟。")

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
            messagebox.showinfo("成功", f"✅ 已成功匯出 JSON 至：\n{file_path}\n可用於 Roll20/FoundryVTT 或其他數位 TRPG 工具匯入。")

    def open_web_ui(self):
        # 優先尋找同目錄或專案根目錄的 index.html
        candidates = [
            "index.html",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"),
            os.path.expanduser(r"~\OneDrive\Documents\dnd-5e-npc-generator\index.html"),
            os.path.expanduser(r"~\OneDrive\Documents\0921test\index.html")
        ]
        target = next((c for c in candidates if os.path.exists(c)), None)
        if target:
            webbrowser.open(f"file:///{os.path.abspath(target)}")
        else:
            messagebox.showwarning("提醒", "找不到 index.html 檔案")


def main():
    if "--test" in sys.argv:
        print("GUI TEST SUCCESSFUL")
        sys.exit(0)
    root = tk.Tk()
    app = DndNpcApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
