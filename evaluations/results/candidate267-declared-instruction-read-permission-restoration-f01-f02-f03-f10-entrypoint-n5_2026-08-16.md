# Candidate267 F01・F02・F03・F10 entrypoint N=5

## 結論

Candidate267は、Candidate264を直接の基盤としてF01・F02・F03の正常経路を各5 / 5件で保持し、F10のinstruction result前配下readを0 / 5件へ閉じた。F10ではexact `src/AGENTS.md`のterminal success content result後にだけ配下readを発行し、その後の必要readも5 / 5件で完遂した。

品質は20 / 20件がScore `4`だった。一方、Candidate264比でtokenは`+31.44%`、経過時間は`+10.98%`となった。変更対象のF10はtoken中央値`+1.88%`、経過時間`-4.08%`だが、変更対象外のF01とF02でtoken中央値が`+30.81%`と`+67.61%`増えた。増加分を必要なinstruction dependencyまたは正常経路へ対応づけられないため、固定済み停止条件どおり`unjustified_cost_regression`として停止する。

## 結果

| ケースと観測 | Candidate264 N=5 | Candidate267 N=5 |
|---|---:|---:|
| F01 開始identityと影響を受けない必要readを同一model stepから発行 | 5 / 5 | 5 / 5 |
| F02 同上 | 5 / 5 | 5 / 5 |
| F03 同上 | 5 / 5 | 5 / 5 |
| F10 `src/AGENTS.md` success result後にだけ配下readを発行 | 2 / 5 | 5 / 5 |
| F10 result後に必要な配下readを完遂 | 5 / 5 | 5 / 5 |

F10のraw rolloutでは、4件がinstruction call・result・最初の配下callの順に`7 -> 8 -> 11`、1件が`11 -> 12 -> 15`だった。instruction result前の配下listing・本文readは0件である。

nonterminal tool result後にmodelが発行した外部`wait`は、Candidate267ではF01 15回、F02 7回、F03 7回、F10 0回であり、該当runは10 / 20件だった。Candidate147は6回・4 / 20件、Candidate264は6回・6 / 20件である。custom exec wrapper内部のpollは数えていない。F10では三候補とも外部`wait`が0回であるため、Candidate267の追加再入を必要なF10 permission dependencyの費用として正当化しない。

## KPI

| 比較 | quality | total_tokens | elapsed_seconds |
|---|---:|---:|---:|
| Candidate147 | 100.0 | 494,706 | 302.929 |
| Candidate264 | 100.0 | 484,121 | 307.710 |
| Candidate267 | 100.0 | 636,348 | 341.495 |
| Candidate267 − Candidate147 | 0.0 | +141,642（+28.63%） | +38.567（+12.73%） |
| Candidate267 − Candidate264 | 0.0 | +152,227（+31.44%） | +33.785（+10.98%） |

## 証拠と状態

- Candidate267 selection: `3f1973df77be40f8ae7eb7e9a9cce825`
- Candidate267 analysis: `848088e5d58c4aad84f07e12f1cf9da8`
- 登録result: `e4dee1e302a2468ba055500a0c3610d7`
- Candidate264基準result: `1a64c1b2429c4e89aff3aedd6836944e`
- Candidate147診断比較result: `29cf98307448409f820a739b2d008f7b`
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`
- quality audit: [`candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json`](candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json)
- mechanism audit: [`candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json`](candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)
- 実行準備監査: [`candidate267-f01-f02-f03-f10-entrypoint-n5-execution-preparation-audit.md`](../../docs/candidate267-f01-f02-f03-f10-entrypoint-n5-execution-preparation-audit.md)
- cost原因監査: [`candidate267-candidate264-candidate147-cost-reentry-causal-audit.md`](../../docs/candidate267-candidate264-candidate147-cost-reentry-causal-audit.md)
- Candidate254からCandidate267までの自然語feedback優先監査: [`candidate254-candidate263-candidate267-natural-language-feedback-priority-audit.md`](../../docs/candidate254-candidate263-candidate267-natural-language-feedback-priority-audit.md)

状態は`targeted_n5_quality_passed / target_mechanism_passed / preserved_routes_passed / unjustified_cost_regression / stopped / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
