# 模式四：評估與優化 操作指南

這是技能包大師 v3.0 模式四的完整操作指南。底層依賴 Anthropic 官方 skill-creator 的評估引擎。

---

## 概念說明

### 什麼是 eval？

eval 就是「模擬真實使用者的提示詞，讓技能包實際跑一次，看結果好不好」。

跟在對話中隨便試兩句不同的是，eval 有系統性：
- 每個測試案例都存下來，可以重複跑
- 有量化指標可以追蹤（通過率、耗時、token 用量）
- 有 baseline 對照，知道是因為技能包才變好的

### 什麼是 assertion？

assertion 是「怎麼判斷結果好不好」的具體標準。

好的 assertion 是可以客觀驗證的，例如：
- 「輸出檔案是 PDF 格式」
- 「輸出包含表格，欄數正確」
- 「使用了技能包指定的腳本」

不適合量化的就不要硬塞，例如「寫作風格自然」這種主觀判斷，交給人工檢視。

### 什麼是 benchmark？

benchmark 是「有技能包」跟「沒技能包（或舊版技能包）」的數據對比。讓你用數字說話，而不是憑感覺。

---

## 操作步驟

### 第一步：設計測試案例

寫 2-3 個測試提示詞，模擬真實使用者會怎麼說。

設計原則：
- 用真實使用者會用的語氣和用詞
- 涵蓋不同的使用情境（簡單的、複雜的、邊緣情況）
- 要有足夠的細節，讓技能包有東西可以做

存檔格式（evals/evals.json）：

```json
{
  "skill_name": "your-skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "使用者的測試提示詞",
      "expected_output": "預期結果的文字描述",
      "files": [],
      "expectations": []
    }
  ]
}
```

expectations 先留空，後面再加。

### 第二步：跑測試

每個測試案例跑兩個版本：

1. with_skill — 有技能包
2. baseline — 沒技能包（新建技能包時），或舊版技能包（改版時）

在 Claude Code 或 Cowork 環境中，兩個版本可以平行跑（用 subagent）。在 Claude.ai 只能逐一跑。

目錄結構：

```
skill-name-workspace/
└── iteration-1/
    ├── eval-1-descriptive-name/
    │   ├── eval_metadata.json
    │   ├── with_skill/
    │   │   ├── outputs/     ← 技能包產出的檔案
    │   │   └── timing.json  ← 時間和 token 數據
    │   └── without_skill/
    │       ├── outputs/
    │       └── timing.json
    └── eval-2-another-name/
        └── ...
```

eval_metadata.json 的格式：

```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name-here",
  "prompt": "使用者的測試提示詞",
  "assertions": []
}
```

### 第三步：設計 assertion

趁測試在跑的時候，替每個測試案例設計量化指標。

好的 assertion 有兩個特質：
1. 可以客觀驗證（不是主觀感覺）
2. 有辨別力（好結果會通過，差結果不會通過）

反面案例：
- 「輸出檔案存在」— 辨別力太低，即使內容完全錯也會通過
- 「輸出品質好」— 無法客觀驗證

寫好之後，更新 eval_metadata.json 和 evals/evals.json 的 expectations 欄位。

### 第四步：評分（grading）

測試跑完之後，對每個結果打分。

用官方 grader 的規則（詳見 skill-creator/agents/grader.md）：
- 每個 assertion 判定 PASS 或 FAIL
- 必須引用具體證據
- 不確定的時候判 FAIL（寧嚴勿鬆）

存檔格式（grading.json）：

```json
{
  "expectations": [
    {
      "text": "assertion 的文字描述",
      "passed": true,
      "evidence": "在哪裡找到什麼證據"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  }
}
```

注意：欄位名稱必須用 text、passed、evidence，HTML 檢視器認這三個名字。

可以用腳本驗證的 assertion，盡量寫腳本去驗證，比人眼看更快也更穩定。

### 第五步：彙整 benchmark

用官方腳本：

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

這會產出 benchmark.json 和 benchmark.md，包含：
- 通過率（mean ± stddev）
- 耗時統計
- token 用量統計
- 兩個版本的差異比較

如果要手動產出 benchmark.json，格式詳見：skill-creator/references/schemas.md

### 第六步：分析數據模式

光看平均數不夠。要看：
- 有沒有 assertion 不管有沒有技能包都會通過（辨別力不夠）
- 有沒有 assertion 不管有沒有技能包都會失敗（可能 assertion 寫錯了）
- 有沒有 eval 的變異很大（不穩定，可能是隨機因素）
- 技能包增加了多少時間和 token 開銷

### 第七步：產生 HTML 檢視器

用官方腳本：

```bash
# Claude Code 環境
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &

# Cowork 環境（無瀏覽器）
python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --static <output_path>.html
```

第二輪開始，加上 `--previous-workspace <workspace>/iteration-<N-1>`。

不要自己寫 HTML，用 generate_review.py。

### 第八步：讀回饋，改進

使用者看完結果後，回饋會存在 feedback.json：

```json
{
  "reviews": [
    {"run_id": "eval-1-with_skill", "feedback": "表格少了一欄", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

空白回饋 = 使用者覺得沒問題。聚焦在有具體意見的案例上。

改進技能包的原則：
- 從回饋中提取通用的改進方向，不要只針對特定案例做修改
- 看 transcript 不只看最終輸出，注意技能包讓模型做了哪些多餘的事
- 解釋「為什麼」比寫死規則更有效

---

## 迭代循環

```
設計測試 → 跑測試 → 評分 → 給人看 → 讀回饋 → 改技能包 → 重新跑測試 → ...
```

每輪改進放到 iteration-N+1/ 目錄。

停止條件（任一即可）：
- 使用者說滿意了
- 回饋全部是空的（所有案例都沒問題）
- 連續兩次迭代沒有實質進步

---

## 環境差異對照

| 步驟 | Claude Code | Cowork | Claude.ai |
|------|------------|--------|-----------|
| 跑測試 | subagent 平行 | subagent 平行 | 逐一跑 |
| baseline | 有 | 有 | 省略 |
| grading | subagent 或 inline | subagent 或 inline | inline |
| benchmark 彙整 | 腳本 | 腳本 | 省略 |
| HTML 檢視器 | 開瀏覽器 | --static 輸出 HTML | 在對話中展示 |
| 回饋收集 | feedback.json | 下載 feedback.json | 在對話中詢問 |

---

## 進階：盲測比較

當你要嚴謹比較兩個版本的技能包時，可以用盲測。

做法：把兩個版本的輸出標記為 A 和 B，交給獨立 agent 評判，不告訴它哪個是哪個版本。

詳見：
- skill-creator/agents/comparator.md — 盲測 agent 的指令
- skill-creator/agents/analyzer.md — 分析為什麼贏家贏了

需要 subagent 支援。Claude.ai 環境無法使用。

---

## 常見陷阱

1. assertion 沒有辨別力 — 「檔案存在」幾乎永遠會通過，改成「檔案存在且包含正確的表頭欄位」
2. 跳過 baseline — 沒有對照組就無法證明是技能包的功勞
3. 測試案例太理想化 — 真實使用者不會寫得那麼清楚整齊
4. 改技能包時過度針對特定案例 — 改一個案例的問題結果其他案例反而退化
5. 只看通過率不看 transcript — 有時候通過了但過程很浪費（多餘步驟、大量重試）
