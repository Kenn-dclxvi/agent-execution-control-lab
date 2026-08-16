# Candidate264 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate254の保存済みStandard14 N=5からF01、F02、F03、F10 entrypointを各5件選び、基準result `4208b6ca016d485684f8df9fadc5b38e`へ固定した。Candidate264のprompt identity以外の比較条件は一致し、比較前receiptは`ready`、Candidate264の不足20件だけを許可した。Candidate254その他のCandidateは新しく実行しない。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate264 bundle SHA-256: `9b33e94432ede3ee0c278d876e743ec07f123ba5478c8c8df84dcf4d159ab930`。
- 直接比較基準: Candidate254。
- 基準result: `4208b6ca016d485684f8df9fadc5b38e`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- Candidate254 pool: `e71ba5db8f3766df39c9c9af10970888e820ff04761b4f709cd543faa01e8b38`。
- Candidate264 pool: `2492f6513ec56a00e80104de1ff63f1252448b273cede8d6d2d1c56e04c18d8c`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- 比較前receipt: `ready`、許可20件、発行前0件。

## 評価境界

- F01、F02、F03では開始確認と許可済みreadの分離を診断する。
- F10ではinstruction resultがread対象または許可を変え得る場合の必要な分離を診断する。
- 品質、問題経路、正常経路、token、時間を別々に記録する。
- 完了待ち、本文圧縮、command、wrapper、待ち時間、read範囲および他Candidateは対象にしない。

許可した20件だけを発行し、20 / 20件がvalidかつ採点可能、Score `4`となった。Candidate254の再実行は0件だった。評価後の判断は[`evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md`](../evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)へ分離する。

現在状態は`preflight_ready / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed`とする。
