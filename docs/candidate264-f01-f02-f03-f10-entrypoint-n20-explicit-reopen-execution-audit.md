# Candidate264 F01・F02・F03・F10 entrypoint N=20明示的再開実行監査

## 結論

Candidate264はN=5で`normal_route_regressed / unjustified_cost_regression / stopped`となっていた。2026-08-16の利用者による明示的な判断に限り、同じ四ケースを各N=20まで観測する作業を再開した。以前の停止判断は履歴として保持し、Standard14、採用、releaseおよびprojectionへ作業を広げていない。

既存atomic poolには各ケース5件があったため、不足15件ずつ、計60件だけを許可した。Candidate254基準result `4208b6ca016d485684f8df9fadc5b38e`へprompt identity以外の互換条件を固定したpreflight receiptは`ready`で、許可60件、発行前0件だった。receipt content SHA-256は`8ccadd9173d2061cf3845bd61a62f57f1024934cbeb74cd1ba922f1cfe521971`である。

## 発行前固定

- Candidate264 pool: `2492f6513ec56a00e80104de1ff63f1252448b273cede8d6d2d1c56e04c18d8c`。
- 既存run: 4ケース各5件、計20件。
- desired count: 各20件。
- authorized missing slots: 4ケース各15件、計60件。
- dispatch: atomic、global queue、同時実行上限24。
- workspace copy mode: `clonefile`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- token accounting: all-agent v1。
- baselineの新規実行: 0件。

preflightは既存N=5 resultの互換条件を検証するため、Candidate264のN=5 profileを用いた。追加枠のN=20 identityはdispatch planとN=20 profileへ別に固定し、最終selectionの登録時に20 iterationsを検証した。profileの試行回数を実行後に書き換えていない。

## 実行結果

追加60件は60 / 60 valid、excluded 0、execution error 0、再試行0で完了した。v14品質監査は60件すべてScore `4`だった。既存N=5の20件と合わせたatomic poolは各ケース20件、計80件になった。

Candidate147はN=100登録resultのatomic poolから同じ四ケース各20件を固定し直し、再実行せず比較基準result `a1910bf71a474153947dabfc4582991a`として登録した。Candidate264のN=20 selectionは`142850aac9e748019f7a8e7a88338c9d`、登録resultは`92467093897544f98eb526e018757abb`である。

評価と判断は[`Candidate264 F01・F02・F03・F10 entrypoint N=20`](../evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n20_2026-08-16.md)へ分離する。

現在状態は`explicit_reopen_authorized / preflight_ready / existing_20_reused / authorized_60 / issued_60 / valid_60 / reference_rerun_0 / n20_registration_completed / standard14_not_started`とする。
