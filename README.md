# 🎲 D&D 5E 劇情導向非典型 NPC 智慧生成系統
*(TRPG Story-Driven Unorthodox NPC Generator)*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![D&D 5E Compatible](https://img.shields.io/badge/D&D%205E-Compatible-red.svg)](https://dnd.wizards.com/)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Lib)-success.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

專為 **桌上角色扮演遊戲（TRPG / D&D 5E）** 地下城主（DM / Storyteller）設計的劇情向 NPC 智慧生成引擎。  
**核心理念**：規則是用來約束玩家的平衡性，而 NPC 是 DM 推動劇情的資產。本專案將「故事生活身分」與「戰鬥底層數值」徹底解耦，支援非典型生活武器（如鋼齒長草耙）、生活故事法器（如刻印符文石楠木老煙斗），並提供真隨機 4d6dl1 屬性建議池與專為跑團主持設計的**直向快速掃視角色卡 (Vertical Quick-Scan Card)**。

---

## 🔒 資安與合規聲明 (Security Statement)

本專案嚴格遵循學術與開源資安規範：
- 程式庫、截圖、文件與範例中**絕無包含**任何 API 金鑰、通行碼、存取權杖、Google Apps Script `/exec` 網址或任何真實機密。
- 本專案倉儲名稱 (`dnd-5e-npc-generator`) 不包含任何學生姓名或學號。
- 核心 NPC 生成引擎採用 **Python 3 純標準函式庫** 開發，完全離線運作，零外部相依性，無需連網或載入外部金鑰。

---

## 📑 專題繳交檔案與交付清單 (Deliverables Suite)

| 項目 | 檔案名稱 | 格式 | 說明 |
| :---: | :---| :---: | :---|
| **1** | [**`dnd_npc_generator/`**](dnd_npc_generator/) | 程式源碼 | **專題本體**：包含 5 大核心模組之完整 D&D 5E 生成引擎。 |
| **2** | [**`gui.py`**](gui.py) / [**`index.html`**](index.html) | GUI / Web | **雙平台使用者介面**：Tkinter 桌面原生視窗與免安裝 Web 視覺介面。 |
| **3** | [**`DND_5E_NPC_Project_Report.pdf`**](DND_5E_NPC_Project_Report.pdf) | PDF (A4) | **專題報告**：完整闡述做什麼、給誰用、怎麼做、怎麼測、下一步。 |
| **4** | [**`DND_5E_NPC_Presentation_90S.pdf`**](DND_5E_NPC_Presentation_90S.pdf) | PDF (16:9) | **90秒展示投影片**：專為課堂 90 秒「打開什麼、做什麼、看到什麼」打造。 |
| **5** | [**`DND_5E_NPC_AI_Summary.pdf`**](DND_5E_NPC_AI_Summary.pdf) | PDF (A4) | **AI 協同開發摘要**：詳述與 AI 互動之四大設計轉折與除錯歷程。 |
| **6** | [**`PRESENTATION_90S_SCRIPT.md`**](PRESENTATION_90S_SCRIPT.md) | Markdown | **課堂 90 秒逐字稿**：精準時間碼對照表與 Q&A 備戰手冊。 |

---

## 🚀 90 秒快速展示演示（打開什麼、做什麼、看到什麼）

本系統提供 **全圖形化免終端機介面**（雙擊即開）與 **高階 CLI 命令列** 多種使用方式：

### 🖥️ 方式一：網頁圖形化版（最直觀、最推薦！）
1. **打開什麼？**  
   直接在資料夾雙擊 **`點我開啟網頁版.bat`** 或直接以瀏覽器點開 **`index.html`**，立即啟動暗黑奇幻質感的直觀操作介面（無需開啟終端機、無需安裝任何套件）。
2. **做什麼？**  
   挑選種族、職業，或在下方劇情欄位輸入一句話（例如：*「退隱禁衛長麥農，武器是鋼齒草耙」*），點擊 **【🎲 立即智慧生成 NPC 角色卡】**。
3. **看到什麼？**  
   **只要 0.01 秒**，畫面右側立即呈現精美的直向角色卡，自動適配「鋼齒長草耙 (1d8/1d10 穿刺)」、真隨機 4d6dl1 點數池與劇本推進線索，支援一鍵複製、列印 / PDF 與匯出 CSV / JSON！

---

### 💻 方式二：桌面原生視窗版
1. **打開什麼？**  
   雙擊 **`點我啟動桌面程式.bat`**（或無黑窗版本 `點我啟動桌面程式(無黑窗).vbs`）。
2. **做什麼？**  
   在桌面視窗中調整參數（支援點擊「🌾 老農戰士」、「📜 封印老法師」、「⛏️ 守墓人」快速載入範本），點擊 **【🎲 立即生成非典型 NPC】**。
3. **看到什麼？**  
   視窗右側即時載入直向卡片，支援一鍵複製剪貼簿、一鍵匯出 CSV 試算表或 JSON 檔案。

---

### ⚡ 方式三：極客 CLI 命令列 (選用)
```bash
python -m dnd_npc_generator.main --class-name "戰士 (Fighter)" --story "老丹恩，表面上只是個鄉村麥農，但真實身分是退隱多年的王國禁衛長，戰鬥定位是戰士，武器是一柄隨身的鋼齒草耙"
```

---

## 💡 核心特色與創新突破

```
┌────────────────────────────────────────────────────────────────────────┐
│                        核心架構亮點概覽                                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 直向快速掃視角色卡 ── 解決多頁試算表翻找痛點，跑團 DM 一眼掌握全局   │
│ 2. 故事與規則徹底解耦 ── 市井生活外貌 ＋ 專業職業戰力底層              │
│ 3. 非典型生活武器映射 ── 鋼齒長草耙 (1d8/1d10)、柴刀、鐵鎬等生活工具化  │
│ 4. 故事生活奧術法器   ── 刻印符文石楠木老煙斗、黃銅算盤、占卜茶杯      │
│ 5. 真隨機 4d6dl1 實擲 ── 拒絕硬編碼，提供職業推薦配置與種族加值候選清單│
│ 6. 語意等級與封印解析 ── 支援「大魔導師 (Lv.13)」、「被封印狀態警示」  │
│ 7. 支援「無」常規凡人 ── 隨心所欲生成完全無特異功能的農夫、商人與鐵匠  │
│ 8. 通用輕量化數據匯出 ── 支援 Markdown、通用 CSV、JSON 與列印 PDF      │
│ 9. 零外部依賴環境     ── 純 Python 標準函式庫，離線隨點隨用            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 多格式匯出與整合支援 (Exports)

為滿足 TRPG 跑團多元場景，系統提供多種輕量、通用且無失真的資料交換格式：

1. **📜 Markdown / 直向預覽文字卡**：
   - 專門為跑團主持設計，垂直排版包含基本身分、4d6dl1 靈活屬性推薦、非典型武器庫（含命中與傷害骰）、職業已解鎖特長與劇本推進線索。
   - 點擊「📋 複製卡片」即可秒貼到 Notion、Obsidian 或 Discord 頻道。
2. **📑 通用 CSV 試算表 (`.csv`)**：
   - 格式通用純淨，無任何專有 XML 繪圖損毀或巨集錯誤風險。
   - 可直接由 Microsoft Excel、Google Sheets、LibreOffice Calc 開啟進行後續編輯。
3. **💾 JSON 結構資料檔 (`.json`)**：
   - 完整結構化 NPC 物件（包含六大屬性、推薦值、裝備清單、背景歷練與自訂標籤）。
   - 適合匯入 Roll20、Foundry VTT 或自行串接其他 TRPG 數位跑團輔助工具。
4. **🖨️ 網頁列印與 PDF 匯出**：
   - 在網頁介面點擊「🖨️ 列印 / 存 PDF」，自動套用專屬列印樣式（隱藏操作按鈕，呈現高對比精緻排版），便於實體團攜帶紙本。

---

## 🛠️ 模組架構與檔案配置

```
dnd-5e-npc-generator/
│
├── dnd_npc_generator/               # 核心生成引擎套件
│   ├── __init__.py
│   ├── database.py                 # D&D 5E 規則字典庫 (種族/職業/背景/武器/非典型特長)
│   ├── roller.py                   # 4d6 drop lowest 1 隨機骰點與屬性推薦配置器
│   ├── generator.py                # 劇情向 NPC 生成主核心 (語意等級/生活武器/封印狀態)
│   ├── exporter.py                 # 格式化輸出器 (直向 Markdown 卡 / CSV / JSON)
│   └── main.py                     # CLI 命令列入口
│
├── gui.py                          # 桌面圖形化介面 (Tkinter 原生深色介面)
├── index.html                      # 網頁視覺化介面 (免伺服器，直接雙擊即可用)
├── server.py                       # 本地輕量 Web 伺服器 (自動啟動瀏覽器)
│
├── start_gui.bat                   # 桌面版啟動批次檔
├── start_web.bat                   # 網頁版啟動批次檔
├── 點我啟動桌面程式.bat              # 中文命名啟動檔
├── 點我開啟網頁版.bat                # 中文命名網頁啟動檔
├── 點我啟動桌面程式(無黑窗).vbs       # 靜默無命令提示字元黑窗啟動器
│
├── DND_5E_NPC_Project_Report.pdf   # 專案完整報告書 (做什麼/給誰用/怎麼做/怎麼測/下一步)
├── DND_5E_NPC_Presentation_90S.pdf # 90 秒簡報投影片
├── DND_5E_NPC_AI_Summary.pdf       # AI 協同開發摘要
├── PRESENTATION_90S_SCRIPT.md      # 課堂 90 秒展示逐字稿與 Q&A 備戰手冊
├── requirements.txt                # 說明文件 (標示零第三方套件依賴)
└── README.md                       # 本專案完整說明文件
```

---

## 📜 授權協議 (License)

本專案基於 **MIT License** 開源釋出。  
所引用的 D&D 5E 系統內容遵循 Wizards of the Coast 發布之 **System Reference Document 5.1 (SRD 5.1)** 與開放遊戲許可 (Open Game License / Creative Commons)。
