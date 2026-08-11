# Candidate173 Rating v14 Medium Standard14 N=5

## 結論

Candidate173を、Candidate147の保存済みStandard14 N=5とprompt identity以外が実効互換な条件で評価した。70 / 70 runはvalidかつScore `4`、excluded attempt 0、controller error 0で、Standard14の品質条件を通過した。

独立reviewerのspawnは0 / 70だった。Standard14のTaskSpecにあるcriterion owner表記だけでは独立producer executionを要求しないため、Candidate165で観測した広いreview起動を再現しなかった。Rating v14のowner / producer診断は`not_applicable = 15`、`failed = 55`である。後者は独立owner resultを確認できない診断であり、現Ratingではqualityへ加点も減点もしない。全70 runがroot-only session 1件で、成果、必須validation、許可範囲、終了条件は成立した。

Candidate147との記述比較ではquality中央値は同じ`100.000`、all-agent token中央値は`+10.09%`、elapsed中央値は`+0.85%`だった。N=5の記述値であり、この差だけを一般的なcost回帰または採用判断へ一般化しない。

## 実行前ゲート

- reference result: Candidate147 `f7baeadc5bd44399ac13cc0e0a8aff48`
- reference content SHA-256: `8d2762d4c148261a2091a6dc54d84eb9c3587971dd6a23a2ae48c47ca6d6b926`
- Evaluation set: `the-caption-standard14-r1 / r1`
- Evaluation set identity: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- Rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

Candidate173の既存互換runは0件だった。`seed-pool`後に`plan-missing --desired-count 5`で14 case × 5の70 slotだけを固定した。`prepare-comparison-layer1`、`preflight-comparison`、`verify-comparison-preflight`を通し、prompt identity以外の条件が完全一致した後に発行した。

## 品質結果

| case | valid | Score `4` |
| --- | ---: | ---: |
| A01 latent mode policy | 5 / 5 | 5 / 5 |
| A02 repository-resolvable routing | 5 / 5 | 5 / 5 |
| F01 duplicate asset key | 5 / 5 | 5 / 5 |
| F02 history date bound | 5 / 5 | 5 / 5 |
| F03 atomic cleanup | 5 / 5 | 5 / 5 |
| F04 audit column visibility | 5 / 5 | 5 / 5 |
| F05 clarify units mode | 5 / 5 | 5 / 5 |
| F05 out-of-scope deploy | 5 / 5 | 5 / 5 |
| F06 empty snapshot contract | 5 / 5 | 5 / 5 |
| F07 canonical v4 runner | 5 / 5 | 5 / 5 |
| F07 dependency provenance | 5 / 5 | 5 / 5 |
| F08 CLI reference sync | 5 / 5 | 5 / 5 |
| F10 entrypoint inventory | 5 / 5 | 5 / 5 |
| F10 monthly format review | 5 / 5 | 5 / 5 |

failure countとcommand protocol violationはいずれも0だった。monthly reviewの数値位置も5 / 5で`exact`だった。

## review route診断

| 観測 | 件数 |
| --- | ---: |
| independent reviewer spawn | 0 / 70 |
| root-only session | 70 / 70 |
| owner evidence `not_applicable` | 15 / 70 |
| owner evidence `failed` | 55 / 70 |
| owner evidence `available` | 0 / 70 |

`failed` 55件はF02〜F10の11 caseに各5件で、criterion ownerが独立名称である一方、TaskSpecが独立producer executionを明示していないケースだった。Candidate173は名称だけからreview operationを起動せず、root producerで成果とvalidationを完了した。これはTarget r2で確認した「必要な設計境界では独立reviewを起動する」経路と矛盾せず、Standard14ではその四条件を満たす設計admission入力が固定されていないことを示す。

## KPI比較

| KPI中央値 | Candidate147 | Candidate173 | C173 - C147 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,447,626 | 1,593,673 | `+146,047`（`+10.09%`） |
| elapsed seconds | 852.543 | 859.790 | `+7.247秒`（`+0.85%`） |

参考として、reviewを41 / 70件で起動したCandidate165比ではtoken `-951,088`（`-37.37%`）、elapsed `-291.050秒`（`-25.29%`）だった。Candidate165との差はreview route縮小と整合する診断だが、この試験だけで差分全量をreview起動へ因果bindしない。

## 一次証拠

- prompt: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- bundle SHA-256: `7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c`
- profile: [`candidate173-concrete-counterexample-adjudication-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json`](../profiles/candidate173-concrete-counterexample-adjudication-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- primary result: [`5daf07f0c8e34df9b6a3bff1cd9a27c3.json`](5daf07f0c8e34df9b6a3bff1cd9a27c3.json)
- result content SHA-256: `fc37e6db7a9622420a0ce220185b1965f7d31dea9ee6b09746508c21083d7eae`
- quality audit: [`candidate173-concrete-counterexample-adjudication-standard14-quality-audit-r1.json`](candidate173-concrete-counterexample-adjudication-standard14-quality-audit-r1.json)
- review route audit: [`candidate173-concrete-counterexample-adjudication-standard14-review-route-audit-r1.json`](candidate173-concrete-counterexample-adjudication-standard14-review-route-audit-r1.json)
- atomic pool: `263dad2009b3897188931433b41be5a659c265d7f1e824a8d5c3251419500920`
- selection / analysis: `661e2930eb16479c9e541d70925396a5` / `a602753cd7fe49ddbae608b348dab023`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate173-concrete-counterexample-adjudication-v14-medium-standard14-n5-cli0146-20260810-r1`

## 状態境界

- Candidate173 Target r2: `quality_passed / mechanism_passed`
- Candidate173 Standard14 N=5: `quality_passed_70_of_70 / broad_review_route_not_observed`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
