# 技能包大師 公開版 v1.0 發行脆文

我把自己做技能包的流程整理成一包，丟上 GitHub，叫技能包大師。

起點很簡單。Anthropic 官方的 skill-creator 架構完整，eval、benchmark、觸發調校的腳本一應俱全，但全英文，重心偏工程手冊。GPT 5.4 做技能包更快又省 token，可是沒把方法論寫清楚。

我想要的是繁體中文版，自己看自己改自己講都不用轉一層。而且我做久了長出一套自己的流程：什麼時候用對話式開一個、什麼時候把現有內容轉成技能包、什麼時候先寫規格再動手。

所以就有了技能包大師。

Anthropic 的腳本整包吸收進來（Apache 2.0，附完整 NOTICE 跟 LICENSE），模式四五不用另外安裝。GPT 那邊的 agents/openai.yaml 也補上了，丟到 Codex 也能正確顯示。我自己的方法論放在最上面：五種模式分流、規格驅動、自由度設計、forward-testing 防汙染、跨 Agent 降級策略。

丟到 Claude Code、Codex、Cowork、OpenCode、反重力等等都能直接跑。

https://github.com/Jiang-Yude/skill-master
