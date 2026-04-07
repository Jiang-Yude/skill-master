# 內容歸屬說明（Attribution）

本技能包是「整合作品」。為了避免爭議，這份檔案逐項列出每一塊內容的來源，分成三層：

1. **GPT / OpenAI 官方** — 來自 OpenAI Codex Skills 的產品規格
2. **Claude / Anthropic 官方** — 來自 Anthropic skill-creator（Apache 2.0）
3. **江昱德自訂方法論** — 原創的整合、分流、補強內容（MIT）

授權對應：
- OpenAI / Codex 部分為公開規格（欄位定義、寫法要求），不涉及檔案再散佈授權
- Anthropic 部分為 Apache 2.0，已附完整 `LICENSE-skill-creator.txt` 與 `NOTICE.md`
- 自訂方法論部分為 MIT

---

## 三層歸屬對照表

| 類別 | GPT / OpenAI 官方 | Claude / Anthropic 官方 | 江昱德自訂方法論 |
|---|---|---|---|
| **檔案結構** | `agents/openai.yaml`（檔案本身） | `SKILL.md` + frontmatter（name / description）<br>`scripts/` `references/` `assets/` 三層 anatomy<br>Progressive Disclosure 三層載入<br>「SKILL.md 控制在 ~500 行」建議 | `SPEC.md` 設計圖層（規格驅動專用）<br>標準結構整合表（把官方 anatomy + openai.yaml + SPEC.md 合在一起呈現） |
| **frontmatter / metadata** | `interface.display_name`<br>`interface.short_description`（25-64 字元）<br>`interface.default_prompt`（要含 `$skill-name`）<br>`policy.allow_implicit_invocation` | `name`<br>`description`（含觸發條件，寫得稍微積極） | UI metadata 與 SKILL.md 一致性檢查清單（display_name / short_description / default_prompt 是否同步） |
| **創建流程** | — | 官方一條主流程：Capture Intent → Interview → Write → Test → Iterate | 五種模式分流：引導探索／專業整理／規格驅動／評估優化／觸發調校<br>共通最小流程（六步驟 SOP）<br>資源規劃表（先決定 scripts/refs/assets，再寫 SKILL.md） |
| **寫作哲學** | — | Explain the Why（不要堆 MUST/NEVER）<br>從回饋中歸納，不針對個案修補<br>觀察重複工作抽成腳本<br>用範例定義輸出格式 | 自由度設計（高/中/低）<br>把 Explain the Why 升級成獨立小節<br>scripts 實跑驗證的最低標準（明確列三條） |
| **規格驅動** | — | — | SPEC.md 三件事（設計意圖／邊界定義／驗收基準）<br>應用情境偏離提醒機制 |
| **評估（模式四）腳本** | — | `scripts/run_eval.py`<br>`scripts/aggregate_benchmark.py`<br>`scripts/generate_report.py`<br>`scripts/improve_description.py`<br>`scripts/package_skill.py`<br>`scripts/quick_validate.py`（原版只驗 frontmatter）<br>`scripts/utils.py`<br>`agents/grader.md`<br>`agents/comparator.md`<br>`agents/analyzer.md`<br>`assets/eval_review.html`<br>`eval-viewer/`<br>`references/schemas.md` | Forward-testing 防汙染原則（五條）<br>把 baseline 對照、benchmark 解讀寫成中文簡述 |
| **觸發調校（模式五）** | — | `scripts/run_loop.py`（train/test split、最多 5 輪、選 test 分數最佳）<br>HTML 模板 `eval_review.html`<br>「描述要稍微積極」這條原則<br>20 個查詢（8-10 正 + 8-10 負，重點是 near-miss） | 把流程簡化成中文五步驟版 |
| **跨環境支援** | — | Cowork 用 `--static` 產 HTML<br>Claude.ai 沒 subagent 的降級寫法 | `references/compatibility.md`<br>「跨 Agent 獨立運作：先想降級策略」四問<br>`quick_validate.py` 升級成三層驗證<br>`--require-openai-yaml` 旗標 |
| **驗證層** | OpenAI metadata 必要欄位的存在性 | 原版 `quick_validate.py`（只驗 frontmatter） | 三層驗證設計：核心結構 + openai.yaml + 一致性檢查 |
| **長期維護觀念** | — | 模型更新後可能可以退役技能包（官方 SKILL.md 開頭那段） | 本地端版本管理建議（YYYY-MM-DD-HHMM 命名 + 更新日誌獨立檔）<br>版本號規則（小/中/大改）<br>中文化處理規範（全形標點、禁粗體破折號） |
| **品質清單** | openai.yaml 同步檢查那一行 | — | 五段清單（創建前／規格驅動／評估優化／觸發調校／更新時）的整合與分類 |

---

## 三句話總結

- **GPT / OpenAI 官方** 提供的是 **產品介面層**：`agents/openai.yaml` 的欄位規格，讓技能包在 Codex 類介面長得對
- **Claude / Anthropic 官方** 提供的是 **執行引擎層**：`scripts/`、`agents/`、`eval-viewer/`、寫作哲學，讓技能包真的能跑能測
- **江昱德自訂方法論** 提供的是 **方法論層 + 整合層**：五種模式分流、規格驅動、自由度設計、forward-testing、跨 Agent 降級策略、三層驗證，把上面兩家的東西串起來給中文使用者用

---

## 使用本技能包時的歸屬建議

如果你 fork 或基於本技能包再修改：

- 保留 `LICENSE-skill-creator.txt` 與 `NOTICE.md`（Apache 2.0 要求）
- 保留本檔案 `references/attribution.md` 的連結，方便下一手追溯
- 如果你新增了內容，建議在本檔案末尾追加你自己的條目

## 來源連結

- Anthropic skill-creator（Apache 2.0）：https://github.com/anthropics/claude-plugins （`plugins/skill-creator/skills/skill-creator`）
- OpenAI Codex Skills 文件：https://developers.openai.com/codex/skills
- OpenAI Codex 建立 skills 文件：https://developers.openai.com/codex/skills/create-skill
- Agent Skills 開放標準：https://agentskills.io
