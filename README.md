# 技能包大師 公開版 v1.0

中文版的技能包（Skill）全生命週期管理系統。整合 Anthropic 官方 skill-creator、OpenAI 官方做法，加上實戰經驗，幫你做出第一個可用的技能包，並具備測試與調校的能力。

## 這個技能包能幫你做什麼

一個技能包，五種模式，覆蓋從「想做」到「做好」到「叫得到」的完整流程：

| 模式 | 用途 | 觸發詞 |
|------|------|--------|
| 引導探索型 | 對話式快速開發，沒想清楚也能開始 | 「做技能包」「創建技能包」 |
| 專業整理型 | 把現有的文章、教學、方法論轉成技能包 | 「把這個內容做成技能包」 |
| 規格驅動型 | 複雜技能包、需長期維護，先寫設計圖再產出 | 「用規格驅動模式」「我先給你規格」 |
| 評估與優化 | 跑 eval 與 benchmark，知道技能包到底好不好 | 「測試技能包」「跑 eval」「benchmark」 |
| 觸發調校 | 技能包沒被叫到？優化 description 提高觸發率 | 「調校觸發」「技能包沒被叫到」 |

## 內建的核心觀念

- **Progressive Disclosure 三層載入**：SKILL.md 放決策邏輯，references/ 放操作細節，控制 context 佔用
- **自由度設計**：根據任務脆弱度，決定要給模型高/中/低自由度，不是越細越好
- **資源規劃表**：先決定 scripts / references / assets，再寫 SKILL.md
- **Explain the Why**：用「為什麼」取代 MUST / NEVER / ALWAYS
- **Forward-testing 防汙染**：測試要乾淨，不能讓 agent 偷看先前推論
- **從回饋中歸納，不針對個案修補**：改技能包要通用化，不是貼補丁

## 跨環境支援

本技能包設計成可獨立運作，所有模式四（評估）、模式五（觸發調校）需要的腳本、agent 指令、HTML 模板都已內建，不需要另外安裝官方 skill-creator。

支援環境：
- **Claude Code**：放到 `~/.claude/skills/skill-master/`
- **Codex / OpenAI Agents**：放到 `$HOME/.agents/skills/skill-master/` 或專案的 `.agents/skills/`
- **Cowork / Claude.ai**：依各環境的 Skill 上傳方式
- **其他相容 Agent Skills 標準的環境**：放進該環境支援的 Skill 路徑

放好後，跟 AI 說「做技能包」「測試技能包」「調校觸發」之類的話，技能包大師就會自動接手。

## 檔案結構

```
skill-master/
├── SKILL.md                          ← 主檔案（五種模式 + 寫作指引 + 品質清單）
├── README.md                         ← 本檔案
├── NOTICE.md                         ← 第三方內容歸屬
├── LICENSE-skill-creator.txt         ← Anthropic skill-creator 的 Apache 2.0 授權
├── references/
│   ├── skill-spec-template.md        ← 規格驅動模式的 SPEC.md 模板
│   ├── why-spec-driven.md            ← 為什麼需要規格驅動
│   ├── skill-writing-guide.md        ← 寫作指引延伸說明
│   ├── eval-guide.md                 ← 模式四完整操作
│   ├── trigger-tuning-guide.md       ← 模式五完整操作
│   └── schemas.md                    ← evals / grading / benchmark JSON 結構
├── scripts/                          ← 評估、調校、打包、驗證腳本
│   ├── run_eval.py
│   ├── run_loop.py
│   ├── aggregate_benchmark.py
│   ├── generate_report.py
│   ├── improve_description.py
│   ├── package_skill.py
│   ├── quick_validate.py
│   └── utils.py
├── agents/                           ← 評估與比較用的 subagent 指令
│   ├── grader.md
│   ├── comparator.md
│   └── analyzer.md
├── assets/
│   └── eval_review.html              ← 觸發測試查詢的 HTML 編輯器
└── eval-viewer/                      ← 評估結果檢視器
    └── generate_review.py
```

## 整合自誰

- **Anthropic 官方 skill-creator**（Apache 2.0）：檔案結構標準、Progressive Disclosure、eval / benchmark / 觸發調校的可執行腳本與 subagent 指令。已內建於 `scripts/`、`agents/`、`assets/`、`eval-viewer/`、`references/schemas.md`，完整出處見 [NOTICE.md](NOTICE.md)
- **OpenAI Codex Skills 觀念**：`agents/openai.yaml` UI metadata 一致性檢查、跨環境部署考量
- **實戰經驗**：五種模式分流、規格驅動（SPEC.md）、自由度設計、資源規劃表、scripts 實跑驗證、forward-testing 防汙染、Explain the Why、應用情境偏離提醒

## 授權

- 本技能包原創內容（SKILL.md、references/ 中除 schemas.md 外的所有文件、本 README、NOTICE.md）：MIT
- 內含的 Anthropic skill-creator 內容（scripts/、agents/、assets/、eval-viewer/、references/schemas.md）：Apache License 2.0，見 `LICENSE-skill-creator.txt`

兩者皆允許自由使用、修改、再散佈。

## 回饋

用了之後遇到坑，或覺得哪裡可以更好，歡迎開 issue 或直接 PR。
