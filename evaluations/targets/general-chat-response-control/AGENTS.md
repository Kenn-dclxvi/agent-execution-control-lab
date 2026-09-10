# general chat response control instructions

このtargetは、一般チャットの一回応答で、確認、根拠要求、部分回答、結果影響範囲および完了を評価するsemantic protocolである。ルート、`evaluations/AGENTS.md`および`evaluations/targets/AGENTS.md`を追加適用する。

- 全アーティファクトをこのディレクトリへ閉じる。
- `cases/core-r1/input-cases.json`と`cases/core-r1/oracle.json`のmodel-visible / model-invisible境界を混ぜない。
- oracle、期待集合、重大違反およびmessage constraintをTaskSpec、Caseまたはpromptへ渡さない。
- live web、外部サービスまたは現在時刻へ依存せず、固定された架空の資料と事実だけを使う。
- baseline resultを保存する前にCandidateを作成しない。
- 保存resultに観測されていない問題経路を将来不安だけでCandidate化しない。
- target固有runtimeは`runtime/`へ閉じ、target非依存kernelへCase IDまたは分岐を追加しない。
- runtimeの一時workspace、Codex JSONL、session transcriptおよび認証情報をcommitしない。
