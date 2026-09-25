# Candidate278 C277残存規則の一括削除試験

## 目的と比較対象

利用者指定に従い、Candidate277のroot `AGENTS.md` 3行目以降に残る三つの規則をまとめて削除し、見出しだけを残す直接子Candidateを作成する。これは一括削除の影響を測る試験であり、改善、採用または機序成立を前提にしない。比較基準はC277の保存済みStandard14 GPT-6 Luna High N=5 result `6ae61524a1e34f8b8e97c677e0ad985d`とする。

## 対象と変更境界

- Candidate identityは`the-caption-3ce91a4-execution-control-heading-only-r1`（Candidate278）とする。
- C277 `the-caption-3ce91a4-execution-control-no-upfront-plan-r1`を直接の親とする。
- root `AGENTS.md`の1行目見出しを保持し、3行目以降の三規則をすべて削除する。2行目の空行と末尾改行を保つ。
- 他の18 target、元の固定commit、Standard14 r1ケース、fixture、TaskSpec、rating contract、GPT-6 Luna High、Codex CLI 0.156.1、permission、all-agent token accounting v1、計測・集計条件はC277のまま固定する。
- 比較条件はC277 resultとのpreflightで機械照合し、完全一致を証明するreceipt保存後にだけslotを発行する。未一致または未確認があれば、評価runを発行しない。

## 評価範囲と報告

- Standard14の14ケースを各5件、計70件で評価する。既存C277 runを基準として再利用し、再実行しない。
- quality score、all-agent `total_tokens`、`elapsed_seconds`を別々に報告し、有効性、採点可能性、除外数も示す。
- 三規則を一括削除するため、その差を各規則の個別効果へ帰属しない。保存traceがある場合の経路・出力差は診断情報として扱い、独立したKPIまたは採用条件にしない。
- invalid run、採点不能、必要成果の欠落または比較条件逸脱は実測状態のまま報告する。追加N、採用、release、runtime projection、本体反映はこの依頼に含めない。

## 状態

Candidate作成後、実行前preflight receipt、run登録、quality結果、KPI比較をそれぞれ独立して記録する。評価完了は採用または本体反映を意味しない。
