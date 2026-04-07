# Changelog

本檔案記錄技能包大師公開版的所有重要變更。版本號規則：小改 v1.0 → v1.1，中改 v1.0 → v1.5，大改 v1.0 → v2.0。

---

## v1.1 — 2026-04-07

補強跨 Agent 獨立運作需要的相容層與驗證層，不刪除既有五種模式架構，只在原有版本上補充。

### 新增

- `agents/openai.yaml`：補上 OpenAI / Codex 類環境的 UI metadata
- `references/compatibility.md`：整理跨 Agent 相容邊界、降級策略、最低獨立運作條件

### 修改

- `scripts/quick_validate.py`
  - 從只驗 `SKILL.md` frontmatter，升級成：
    - 核心結構驗證
    - `agents/openai.yaml` 驗證
    - 基本一致性檢查
  - 新增 `--require-openai-yaml` 旗標，讓需要 OpenAI / Codex metadata 的環境可強制驗證
- `SKILL.md`
  - 在標準檔案結構中補上 `agents/openai.yaml`
  - 新增跨 Agent 獨立運作與降級策略的設計原則
  - 補上 `references/compatibility.md` 的索引與進階驗證用法
- `README.md`
  - 補上 `agents/openai.yaml` 與 `references/compatibility.md`
  - 補列本次補強內容，方便外部使用者快速理解差異

### 目的

這次不是把 GPT 官方做法整包照抄進來，而是補上真正對跨 Agent 運作最有幫助的兩層：

1. 介面層：`agents/openai.yaml`
2. 驗證層：可檢查 UI metadata 的 `quick_validate.py`

這樣技能包大師在其他 Agent 環境中，比較不需要靠作者額外口頭補充。

---

## v1.0 — 2026-04-07

首次公開發行。整合 Anthropic 官方 skill-creator 與 OpenAI Codex Skills 觀念，加上實戰經驗，做成中文版的技能包全生命週期管理系統。

### 設計決策

**為什麼做這個技能包**

Anthropic 官方 skill-creator 是英文的工程手冊，重心在 draft → test → iterate 的執行迴圈，提供完整可執行的腳本。OpenAI Codex Skills 則定義了開放的 Agent Skills 標準，但沒有附完整的製作教練。中文使用者在做技能包時缺一個東西：把「想清楚要做什麼」「如何規劃結構」「如何長期維護」這層方法論講明白的中文系統。

技能包大師補的就是這層。它不取代官方腳本，而是把官方腳本包進來，再加上五種模式的分流邏輯、規格驅動觀念、自由度設計、forward-testing 防汙染等實戰經驗。

**為什麼吸收官方腳本進來**

最初版本只寫方法論，模式四（評估）和模式五（觸發調校）依賴使用者另外安裝官方 skill-creator。這帶來兩個問題：

1. 對方拿到技能包卻跑不起來，得先去安裝另一個東西
2. 跨環境部署（Codex、openclde 等）時，依賴關係更難交代

考量這個技能包的目標是「丟到任何相容 Agent Skills 標準的環境就能用」，決定把官方的 scripts/、agents/、assets/、eval-viewer/、references/schemas.md 全部吸收進來。Apache 2.0 授權允許再散佈，附上 NOTICE.md 與 LICENSE-skill-creator.txt 標明來源即可。

**為什麼拿掉「技能包養成法」**

公開版 v1.0 的目標是讓大家先做出第一個可用的技能包。養成法（生命週期管理、能力提升型 vs 偏好編碼型、四個生命階段、裂變、整合規則）屬於「已經有好幾個技能包之後」的議題，初次接觸會分散注意力。先讓大家把第一個做好，養成法之後可能獨立成另一個技能包，或在 v2.0 補回來。

**為什麼保留五種模式**

引導探索、專業整理、規格驅動三種建立模式，加上評估與觸發調校兩個迭代模式，覆蓋了技能包從零到上線的完整路徑。官方版本只有一條主流程，不分情境；分模式的好處是新手可以直接從「我手上有什麼」對應到「該走哪條路」，而不是讀完整本手冊才知道要做什麼。

### 內容組成

**原創內容（MIT 授權）**

- `SKILL.md` — 五種模式架構、共通最小流程、技能包寫作指引、品質檢查清單
- `references/skill-spec-template.md` — 規格驅動模式的 SPEC.md 模板
- `references/why-spec-driven.md` — 為什麼需要規格驅動
- `references/skill-writing-guide.md` — 寫作指引延伸說明
- `references/eval-guide.md` — 模式四完整操作指南
- `references/trigger-tuning-guide.md` — 模式五完整操作指南
- `README.md`、`NOTICE.md`、本 `CHANGELOG.md`

**整合自 Anthropic skill-creator（Apache 2.0）**

- `scripts/` — run_eval、run_loop、aggregate_benchmark、improve_description、generate_report、package_skill、quick_validate、utils
- `agents/` — grader、comparator、analyzer
- `assets/eval_review.html`
- `eval-viewer/` — generate_review.py、viewer.html
- `references/schemas.md`
- `LICENSE-skill-creator.txt`

### 跨環境支援

設計目標：丟到任何相容 Agent Skills 標準的環境都能直接運作，不用額外安裝。

- Claude Code：`~/.claude/skills/skill-master/`
- Codex / OpenAI Agents：`$HOME/.agents/skills/skill-master/` 或專案的 `.agents/skills/`
- Cowork / Claude.ai：依各環境的上傳方式
- 其他相容環境：放進該環境支援的 Skill 路徑

### 已知限制

- 模式四的 baseline 對照、模式五的自動化迴圈在沒有 subagent 的環境（例如 Claude.ai）會降級成手動流程。這不是技能包本身的限制，是執行環境的限制
- 中文化處理規範（全形標點、禁粗體、禁破折號）是個人偏好，公開版保留為「建議」，使用者可自行決定要不要遵守
- 暫時拿掉技能包養成法，不適合需要長期管理多個技能包的進階使用者，這部分留到後續版本補回
