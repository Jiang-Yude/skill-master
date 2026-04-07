# 跨 Agent 相容性說明

本檔說明技能包大師在不同 Agent 環境中的相容邊界、降級策略與部署重點。目標不是要求所有環境功能完全一致，而是讓這個技能包在功能有差異時，仍然能自己判斷怎麼退化執行。

---

## 1. 核心相容原則

技能包大師分成三層：

1. 通用層：`SKILL.md`、`references/` 內的工作流程與方法論
2. 執行層：`scripts/`、`agents/`、`eval-viewer/`、`assets/`
3. 介面層：`agents/openai.yaml`

其中：

- 通用層是最可攜的。只要環境支援讀取 Markdown skill，就能使用
- 執行層需要環境支援 Python、檔案系統與必要的批次執行能力
- 介面層是 OpenAI / Codex 類技能環境的 UI metadata，幫助技能在介面中被正確理解與呼叫

---

## 2. 各環境支援程度

| 環境 | 可用程度 | 說明 |
|------|---------|------|
| Claude Code / Codex 類本地 Agent | 完整支援 | 可用五種模式、scripts、自動驗證、HTML 檢視器 |
| 有檔案系統與 Python 的其他 Agent | 高度支援 | 大多數流程可用，差異主要在 UI metadata 與 subagent 叫法 |
| 只有技能 Markdown、無本地腳本能力的環境 | 部分支援 | 可用方法論、模式分流、規格驅動；評估與觸發調校需改手動流程 |
| 純聊天環境 | 低度支援 | 只能把技能包大師當作教練或手冊，不能直接跑內建腳本 |

---

## 3. 降級策略

### 沒有 `agents/openai.yaml`

- 技能本體仍可運作
- 但 UI 上的顯示名稱、短描述、預設 prompt 可能缺失
- 在 OpenAI / Codex 類產品中，建議補上 `agents/openai.yaml`

### 沒有 subagent

- 模式四的盲測比較改成人工對照
- 模式五的自動化觸發調校改成手動改寫 description
- forward-testing 改成新 thread 手動重跑，不做平行多代理比較

### 沒有 Python 或無法執行 scripts

- 模式一、模式二、模式三仍可作為技能設計教練使用
- 模式四、模式五改讀 `references/eval-guide.md` 與 `references/trigger-tuning-guide.md`，用人工步驟執行
- `quick_validate.py` 改由人工檢查 frontmatter、命名、檔案結構

### 沒有 HTML 檢視能力

- `eval-viewer/` 與 `assets/eval_review.html` 改成純 Markdown 或對話摘要
- 核心仍是比較 with_skill / baseline 的差異，不依賴 HTML 本身

---

## 4. OpenAI / Codex 類環境額外注意

如果環境支援 `agents/openai.yaml`：

- `display_name` 要對應技能定位
- `short_description` 要能讓人一眼知道用途
- `default_prompt` 要明確提到 `$skill-name`
- 更新 `SKILL.md` 的定位後，要一起檢查 `agents/openai.yaml` 是否同步

如果環境不讀 `agents/openai.yaml`，這份檔案可視為相容層，不影響 `SKILL.md` 的主要功能。

---

## 5. 建議的獨立運作最低條件

若你想把這個技能包丟到另一個 Agent 環境，最低建議至少包含：

1. `SKILL.md`
2. `references/`
3. `scripts/quick_validate.py`
4. `agents/openai.yaml`（若目標環境會讀）
5. `NOTICE.md` 與授權檔（若有再散佈第三方內容）

這五項能確保：

- 主要方法論能被讀
- 基本驗證能做
- UI metadata 有地方承接
- 再散佈時授權邊界清楚

---

## 6. 什麼叫「可獨立運作」

技能包大師的「可獨立運作」不是指每個環境都一模一樣，而是指：

- 不必再額外安裝另一個技能包才知道怎麼做
- 需要的腳本與說明大多已內建
- 缺少某些能力時，有清楚的降級路徑
- 使用者或 Agent 不需要靠作者在旁邊口頭補充

如果要再往前一步，變成真正的跨平台產品版，下一步優先補的是：

1. 更完整的 `agents/openai.yaml`
2. 驗證器對 UI metadata 的一致性檢查
3. 環境能力檢測與對應的自動提示
