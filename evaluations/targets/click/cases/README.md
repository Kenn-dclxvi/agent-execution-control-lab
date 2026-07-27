# click cases

target instance `click`のcase artifactを置く。1 case revisionごとに`README.md`、`trial-prompt-input.json`、`private/`（`seed.patch`と`case-data.json`）を持つ。

カバーすべき判断点と元caseの対応は[`docs/public-target-selection-phase0.md`](../../../../docs/public-target-selection-phase0.md)の「14項目のcoverage対応」を正本とする。case追加手順は[`evaluations/cases/README.md`](../../../cases/README.md)の追加順序に従う。

## 現在のcase

| case | 元case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| [`CLICK-F01-ANSI-SEQUENCE-STRIP/r1`](CLICK-F01-ANSI-SEQUENCE-STRIP/r1/README.md) | F01 | 単一fileのsource実装、不変条件の復元 | fixture qualified / P1-c evaluated（3 batch、15 / 15 score 4） |
| [`CLICK-F02-STREAM-DEPRECATION-CONTRACT/r1`](CLICK-F02-STREAM-DEPRECATION-CONTRACT/r1/README.md) | F02 | 複数source file、公開・非公開APIの層間contract | fixture qualified / N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP/r1`](CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP/r1/README.md) | F03 | filesystem cleanupとcwd復元 | fixture qualified / N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F04-NESTED-GROUP-COMPLETION/r1`](CLICK-F04-NESTED-GROUP-COMPLETION/r1/README.md) | F04 | nested contextのshell completion | fixture qualified / N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F05-CLARIFY-COMMAND-ORDER/r1`](CLICK-F05-CLARIFY-COMMAND-ORDER/r1/README.md) | F05 | 未固定policyの確認とzero drift | N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY/r1`](CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY/r1/README.md) | F05-OS | publish authorization境界 | N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION/r1`](CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION/r1/README.md) | F06 | test-only regression contract | fixture qualified / N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F07-CANONICAL-TOX-RUNNER/r2`](CLICK-F07-CANONICAL-TOX-RUNNER/r2/README.md) | F07 | repository設定からのcanonical command復元 | r1は未rating、r2 N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F07-P-DEPENDENCY-LOCK-PAIR/r3`](CLICK-F07-P-DEPENDENCY-LOCK-PAIR/r3/README.md) | F07-P | dependency provenance pairとoffline lock | r1 / r2は各3 / 3 score 3、r3は3 / 3 score 4 |
| [`CLICK-F08-SHELL-COMPLETION-DOC-SYNC/r1`](CLICK-F08-SHELL-COMPLETION-DOC-SYNC/r1/README.md) | F08 | implementationとdocsの同期 | fixture qualified / N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F10-COMMAND-API-INVENTORY/r1`](CLICK-F10-COMMAND-API-INVENTORY/r1/README.md) | F10 | read-only API inventory | N=3 evaluated（3 / 3 score 4） |
| [`CLICK-F10-COMMAND-API-INVENTORY/r2`](CLICK-F10-COMMAND-API-INVENTORY/r2/README.md) | F10 | `src/AGENTS.md` authority availability | N=5 × 4条件評価完了（authorityなし2条件はscore 1 × 5、あり2条件はscore 4 × 5） |
| [`CLICK-F10-R-NESTED-COMPLETION-REVIEW/r1`](CLICK-F10-R-NESTED-COMPLETION-REVIEW/r1/README.md) | F10-R | fixed commitのzero-drift review | N=3 evaluated（3 / 3 score 4） |
| [`CLICK-A01-LATENT-CONTEXT-POLICY/r1`](CLICK-A01-LATENT-CONTEXT-POLICY/r1/README.md) | A01 | latent ambiguityの確認停止 | N=3 evaluated（3 / 3 score 4） |
| [`CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING/r1`](CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING/r1/README.md) | A02 | repository根拠による無質問解決 | N=3 evaluated（3 / 3 score 4） |

14項目のcaseを固定し、Bundle Aの標準setは70 / 70件がscore `4`で完了した（[一次結果](../results/click-control-free-standard14-n5_2026-07-26.md)）。F07 r1とF07-P r1 / r2は失敗revisionの履歴として保持し、標準setへは含めない。

## 実測で確定した共通条件

- gate commandは**repository rootをcwdとして実行する**。cwd外実行では`tests/test_utils/test__expand_args.py::test_expand_args`がseedと無関係に失敗する。
- seedは2026-05-01以降のcommitから選び、`src/`部分だけの逆patchとして固定する。逆patchが現在のtarget commitへ当たること（後続commitで同じ箇所が変更されていないこと）を`git apply --check`で確認する。
- seed patchは純粋なdiffだけを保存する。`git show`のheaderはcommit messageを含み、修正内容がoracleとして漏れるため除去する。
