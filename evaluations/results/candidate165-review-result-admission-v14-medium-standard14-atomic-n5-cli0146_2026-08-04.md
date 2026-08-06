# Candidate165 Rating v14 Medium Standard14 N=5

## 結論

Candidate165を、Review4とは分離した既存Standard14の14 case × N=5で評価した。70 / 70 runはvalidかつScore `4`で、事前に固定した「Score `3`以下が一件でもあれば停止」のquality gateを通過した。

一方、互換なCandidate147 N=5に対し、集約中央値はall-agent token `+75.79%`、elapsed `+34.99%`だった。qualityは同じ100.000である。C165では独立criterion owner resultが41 / 70件で観測され、review operationの広い発生が実行量増加の主要な診断候補である。ただしこの試験だけで増加量の全てをreview起動へ因果bindしない。

状態は`standard14_evaluated / quality_gate_passed_70_of_70 / aggregate_cost_both_higher / review_route_expansion_observed / adoption_not_decided`とする。quality通過だけを採用判断へ読み替えない。

## 評価構成

- Standard14: 既存の14 case × N=5
- Review4: このrunへ混ぜず、先行targeted result 20 / 20を独立gateとして保持
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- Rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- `M=24`

Candidate147 Standard14 N=5の保存済みLayer 1から、fixture、TaskSpec、case revision、rating、model、reasoning、runtime、permission、executor挙動、token accountingを複製した。prompt identityだけをCandidate165へ変更した。互換キーは`cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`で一致した。

## 期待値と結果

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid | 70 / 70 | 70 / 70 | 通過 |
| Score `4` | 70 / 70 | 70 / 70 | 通過 |
| Score `3`以下 | 0 / 70 | 0 / 70 | 通過 |
| excluded attempt | 0 | 0 | 通過 |
| controller error | 0 | 0 | 通過 |

全14 caseが各5 / 5でScore `4`だった。

## Candidate147との互換比較

| KPI中央値 | Candidate147 | Candidate165 | C165 - C147 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | `0.000` |
| all-agent tokens | 1,447,626 | 2,544,761 | `+1,097,135`（`+75.79%`） |
| elapsed seconds | 852.543 | 1,150.840 | `+298.297`（`+34.99%`） |

両analysisはcomparison keyとexecution stratumが一致し、各N=5である。N=5の記述比較であり、統計的な一般化はしない。

## review route diagnostic

owner / producer evidenceは次の分布だった。この項目はRating v14ではdiagnosticでありKPIではない。

| status | 件数 | 意味 |
| --- | ---: | --- |
| `available` | 41 | 独立criterion ownerのadmissible resultを確認 |
| `not_applicable` | 15 | 独立owner resultを要求しない |
| `failed` | 14 | 独立owner resultを確認できないが、現行ratingではdiagnostic-only |

`available`はF02、F03、F04、F06、F07 2種、F08、F10 entrypointで各5件、F05 out-of-scopeで1件だった。Candidate165のStandard14でreview operationが一部の例外ではなく広い経路になったことを示す。

また、descendant commandをmachine-bound exit codeへ結び付けられない`command_protocol_violations`を52件観測した。影響runは19 / 70で、A02、F02、F03、F04、F06、F07 canonical、F10 entrypointに分布した。required outcomeとmachine validationは成立したためScoreは全件4だが、Candidate147の同じN=5 resultではこのdiagnosticは0件だった。採用判断では無視しない。

## 実行identity

- prompt: Candidate165 `the-caption-3ce91a4-review-result-admission-r1`
- bundle SHA-256: `dc434293678fbc1623f395ff21f5c146d41361b08148584db1b999c62215b452`
- Evaluation set identity: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- atomic pool: `b55ac304a89536eda715c318d869bc9e76c805902fb3584f113d825681994595`
- selection / analysis: `fb8cea9497ec4827a05c8daa0c6c58c5` / `529736be8c0d44c78f5d7e5596abeda3`
- registered result: `6b95098cb4544e86bb23c9a74aed69ad`
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate165-review-result-admission-v14-medium-standard14-n5-cli0146-20260804-r1`

実行前に二つのcycleがslot 0件で停止した。一つ目は参照Layer 1に旧comparison receiptを含めたため新receiptを書けず、二つ目はsnapshot作成時にsymlinkを実体化してF01 fixture identityが変化したためである。symlinkとmodeを保持し、旧receiptだけを除外した`cycle-r2`でpreflightを通し、70件を一度だけ発行した。停止cycleをquality結果へ算入していない。

## Review4と合わせた現在位置

| gate | 状態 |
| --- | --- |
| Review4 | 20 / 20、quality / mechanism通過 |
| Standard14 | 70 / 70 Score `4`、quality通過 |
| efficiency | C147比token `+75.79%`、elapsed `+34.99%` |
| adoption | 未決定 |
| release / projection | 未実施 |

したがって「review result authority境界は成立し、既存成果品質も維持した」までは確認済みである。一方、「必要なときだけreviewして実行量を抑える」状態にはまだ達していない。次の判断対象はresult admissionの正しさではなく、review admissionがStandard14で41件まで広がることを許容するか、route条件を狭める新Candidateが必要かである。
