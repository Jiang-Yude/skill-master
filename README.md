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

## 安裝方式

把整個資料夾放到你的 Skills 目錄底下即可：

- Claude Code：`~/.claude/skills/skill-master/`
- Cowork / Claude.ai：依各環境的 Skill 上傳方式
- 其他環境：放進該環境支援的 Skill 路徑

放好後，跟 Claude 說「做技能包」「測試技能包」「調校觸發」之類的話，技能包大師就會自動接手。

## 檔案結構

```
skill-master/
├── SKILL.md                          ← 主檔案（五種模式 + 寫作指引 + 品質清單）
└── references/
    ├── skill-spec-template.md        ← 規格驅動模式的 SPEC.md 模板
    ├── why-spec-driven.md            ← 為什麼需要規格驅動
    ├── skill-writing-guide.md        ← 寫作指引延伸說明
    ├── eval-guide.md                 ← 模式四（評估與優化）完整操作
    └── trigger-tuning-guide.md       ← 模式五（觸發調校）完整操作
```

## 整合自誰

- **Anthropic 官方 skill-creator**：檔案結構標準、Progressive Disclosure、eval / benchmark / 觸發調校系統
- **OpenAI 官方做法**：UI metadata 一致性檢查、規格驅動觀念
- **實戰經驗**：自由度設計、資源規劃表、scripts 實跑驗證、forward-testing 防汙染、Explain the Why 寫法哲學

## 授權

MIT。歡迎自由使用、修改、再分享。

## 回饋

用了之後遇到坑，或覺得哪裡可以更好，歡迎開 issue 或直接 PR。
