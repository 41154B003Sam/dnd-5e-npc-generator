# 🎲 D&D 5E 劇情導向非典型 NPC 智慧生成系統
*(TRPG Story-Driven Unorthodox NPC Generator)*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![D&D 5E Compatible](https://img.shields.io/badge/D&D%205E-Compatible-red.svg)](https://dnd.wizards.com/)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Lib)-success.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

專為 **桌上角色扮演遊戲（TRPG / D&D 5E）** 地下城主（DM / Storyteller）設計的劇情向 NPC 生成引擎。  
**核心理念**：規則是用來約束玩家的平衡性，而 NPC 是 DM 推動劇情的資產。本專案將「故事生活身分」與「戰鬥底層數值」徹底解耦，支援非典型生活武器（如鋼齒長草耙）、生活故事法器（如刻印符文石楠木老煙斗），並提供真隨機 4d6dl1 屬性建議池。

---

## 🔒 資安與合規聲明 (Security Statement)

本專案嚴格遵循學術與開源資安規範：
- 程式庫、截圖、文件與範例中**絕無包含**任何 API 金鑰、通行碼、存取權杖、Google Apps Script `/exec` 網址或任何真實機密。
- 本專案倉儲名稱 (`dnd-5e-npc-generator`) 不包含任何學生姓名或學號。
- 核心 NPC 生成引擎採用 **Python 3 純標準函式庫** 開發，完全離線運作，無需連網或載入外部金鑰。

---

## 📑 專題繳交檔案與交付清單 (Deliverables Suite)

| 項目 | 檔案名稱 | 格式 | 說明 |
| :---: | :---| :---: | :---|
| **1** | [**`dnd_npc_generator/`**](dnd_npc_generator/) | 程式源碼 | **專題本體**：包含 5 大核心模組之完整 D&D 5E 生成引擎。 |
| **2** | [**`DND_5E_NPC_Project_Report.pdf`**](DND_5E_NPC_Project_Report.pdf) | PDF (A4) | **專題報告**：完整闡述做什麼、給誰用、怎麼做、怎麼測、下一步。 |
| **3** | [**`DND_5E_NPC_Presentation_90S.pdf`**](DND_5E_NPC_Presentation_90S.pdf) | PDF (16:9) | **90秒展示投影片**：專為課堂 90 秒「打開什麼、做什麼、看到什麼」打造。 |
| **4** | [**`DND_5E_NPC_AI_Summary.pdf`**](DND_5E_NPC_AI_Summary.pdf) | PDF (A4) | **AI 協同開發摘要**：詳述與 AI 互動之四大設計轉折與除錯歷程。 |
| **5** | [**`PRESENTATION_90S_SCRIPT.md`**](PRESENTATION_90S_SCRIPT.md) | Markdown | **課堂 90 秒逐字稿**：精準時間碼對照表與 Q&A 備戰手冊。 |

---

## 🚀 90 秒快速展示演示（打開什麼、做什麼、看到什麼）

本系統提供 **全圖形化免終端機介面**（雙擊即開）與 **高階 CLI 命令列** 兩種使用方式：

### 🖥️ 方式一：網頁圖形化版（最直觀、最推薦！）
1. **打開什麼？**  
   直接在資料夾雙擊 **`點我開啟網頁版.bat`** 或直接點開 **`index.html`**，立即在瀏覽器中啟動暗黑奇幻質感的直觀操作介面（無需開啟終端機、無需安裝任何套件）。
2. **做什麼？**  
   挑選種族、職業，或在下方劇情欄位輸入一句話（例如：*「退隱禁衛長麥農，武器是鋼齒草耙」*），點擊 **【🎲 立即智慧生成 NPC 角色卡】**。
3. **看到什麼？**  
   **只要 0.01 秒**，畫面右側立即呈現精美的直向角色卡，自動適配「鋼齒長草耙 (1d8/1d10 穿刺)」、真隨機 4d6dl1 點數池與劇本推進線索，支援一鍵複製與匯出 CSV！

---

### 💻 方式二：桌面原生視窗版
1. **打開什麼？**  
   雙擊 **`點我啟動桌面程式.bat`**（或無黑窗版本 `點我啟動桌面程式(無黑窗).vbs`）。
2. **做什麼？**  
   在桌面視窗中調整參數，點擊「🎲 立即生成角色卡」。
3. **看到什麼？**  
   視窗右側即時載入直向卡片，支援一鍵複製剪貼簿、一鍵匯出 CSV / JSON 檔案。

---

### ⚡ 方式三：極客 CLI 命令列 (選用)
```bash
python -m dnd_npc_generator.main --class-name "戰士 (Fighter)" --story "老丹恩，表面上只是個鄉村麥農，但真實身分是退隱多年的王國禁衛長，戰鬥定位是戰士，武器是一柄隨身的鋼齒草耙"
```

---

## 💡 核心亮點與創新突破

```
┌────────────────────────────────────────────────────────────────────────┐
│                        核心架構亮點概覽                                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 故事與規則徹底解耦 ── 市井生活外貌 ＋ 專業職業戰力底層              │
│ 2. 非典型生活武器映射 ── 鋼齒長草耙 (1d8/1d10)、柴刀、鐵鎬等生活工具化  │
│ 3. 故事生活奧術法器   ── 刻印符文石楠木老煙斗、黃銅算盤、占卜茶杯      │
│ 4. 真隨機 4d6dl1 實擲 ── 拒絕硬編碼，提供職業推薦配置與種族加值候選清單│
│ 5. 語意等級與封印解析 ── 支援「大魔導師 (Lv.14)」、「被封印狀態警示」  │
│ 6. 零外部依賴 ────────── Python 3.12 純標準函式庫，離線安全且極速執行 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ CLI 常用指令範例集

### 案例 A：抽老煙斗的 14 環大魔導師
```bash
python -m dnd_npc_generator.main --class-name "法師 (Wizard)" --level "14" --story "神秘老學者，不使用常規魔杖，施法時總是抽著一支刻印符文的石楠木老煙斗"
```

### 案例 B：被詛咒封印的高階聖武士
```bash
python -m dnd_npc_generator.main --class-name "聖騎士 (Paladin)" --level "大魔導師（封印狀態）"
```

### 案例 C：一鍵匯出 JSON 與 CSV (供 Excel 角色卡匯入)
```bash
python -m dnd_npc_generator.main --class-name "遊盪者 (Rogue)" --output-json "npc_sample.json" --output-csv "npc_sample.csv"
```

---

## 🏛️ 模組架構

```
dnd-5e-npc-generator/
├── __init__.py      # 套件導出模組
├── database.py      # D&D 5E 繁體中文標準資料庫 (種族/職業/背景/1~20特長/非典型武器/生活法器)
├── roller.py        # 4d6dl1 真隨機擲骰引擎、調整值計算器、職業推薦演算法
├── generator.py     # 語意與規則解析器 (解耦故事與數值、生活道具適配、等級解析)
├── exporter.py      # 直向預覽卡輸出、JSON 結構檔與 10 頁 Excel 扁平化介面
└── main.py          # CLI 命令列進入點 (支援 Windows UTF-8 編碼與 Emoji)
```
