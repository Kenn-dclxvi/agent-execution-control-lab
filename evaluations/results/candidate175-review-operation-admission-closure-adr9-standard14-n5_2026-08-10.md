# Candidate175 ADR9 r2 / Standard14 N=5

## 結論

Candidate175は、変更対象の設計を必要時だけ独立reviewへ渡すためのoperation仕様、専用producer binding、allow-list形式のsemantic projectionを一般制御として追加した。実装前の設計監査と実装監査を通過した後、ADR9 r2を9 case × 5、Standard14を14 case × 5で評価した。

ADR9は45 / 45 run、Standard14は70 / 70 runがvalidかつScore `4`だった。ADR9ではreviewが必要な6 caseだけで各5回起動し、合計30 / 45回となった。review不要なADR01・ADR02、permission否定のADR08では起動0回だった。ADR06の禁止canary配送も0 / 5だった。Standard14は70 / 70件がroot-onlyで、criterion ownerの名称だけを独立producer要求として扱わなかった。

この結果により、Candidate173で残っていたreview operationの仕様不足とsemantic projection不足は、ADR9の試験固有分岐を使わずに閉じたと判断する。採用、release、本体反映は別判断であり、まだ実施していない。

## 変更前レビューと実装試験

- 一般設計: [`candidate175-review-operation-admission-closure-design.md`](../../docs/candidate175-review-operation-admission-closure-design.md)
- 設計監査: [`candidate175-review-operation-admission-closure-design-audit.md`](../../docs/candidate175-review-operation-admission-closure-design-audit.md)
- 実装監査: [`candidate175-review-operation-admission-closure-implementation-audit.md`](../../docs/candidate175-review-operation-admission-closure-implementation-audit.md)
- リポジトリ試験: `1104 passed, 1751 subtests passed`

監査で見つかった専用producer fallback、projection failure transition、permissionの全域化を設計へ反映した。その後の再監査では、一般修正を要する具体的反例は見つからなかった。既存評価ケース、rating contract、試験コードは変更していない。

## ADR9 r2 N=5

### 実行前ゲート

- reference: Candidate173 `5f4ea3177785443ab2b63f67ebb6652a`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- 発行: Candidate175の不足45 slotのみ
- valid / excluded: `45 / 0`

### case別結果

| case | 期待終端 | valid | Score `4` | reviewer起動 | artifact変更 |
| --- | --- | ---: | ---: | ---: | ---: |
| ADR01 | `completion_ready` | 5 | 5 | 0 | 5 |
| ADR02 | `completion_ready` | 5 | 5 | 0 | 5 |
| ADR03 | `blocked` | 5 | 5 | 5 | 0 |
| ADR04 | `blocked` | 5 | 5 | 5 | 0 |
| ADR05 | `blocked` | 5 | 5 | 5 | 0 |
| ADR06 | `blocked` | 5 | 5 | 5 | 0 |
| ADR07 | `completion_ready` | 5 | 5 | 5 | 5 |
| ADR08 | `unavailable` | 5 | 5 | 0 | 0 |
| ADR09 | `unavailable` | 5 | 5 | 5 | 0 |

ADR06ではhistoryに置いた禁止canaryがreviewerへ配送されたrunは0件だった。ADR08ではpermission否定をreview operation作成前に適用し、reviewer起動は0件だった。

### Candidate173との記述比較

| KPI中央値 | Candidate173 | Candidate175 | 差 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,147,181 | 1,123,616 | `-23,565`（`-2.05%`） |
| elapsed seconds | 711.025 | 733.368 | `+22.343秒`（`+3.14%`） |

N=5の記述値であり、cost差を一般的な優位性へ一般化しない。

## Standard14 N=5

### 実行前ゲート

- reference: 同じStandard14 N=5のCandidate173 `2c4794015113473bb9cc89e6d628494f`
- evaluation set: `the-caption-standard14-r1 / r1`
- evaluation set identity: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- 発行: Candidate175の不足70 slotのみ
- valid / excluded: `70 / 0`

### 品質結果

14 caseすべてが5 / 5 Score `4`で、合計70 / 70だった。failure countとcommand protocol violationはいずれも0件、monthly format reviewの数値位置は5 / 5で`exact`だった。独立reviewer spawnは0 / 70で、全runがroot-onlyだった。

### Candidate173との記述比較

| KPI中央値 | Candidate173 | Candidate175 | 差 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,589,089 | 1,692,063 | `+102,974`（`+6.48%`） |
| elapsed seconds | 848.054 | 804.940 | `-43.115秒`（`-5.08%`） |

品質は維持し、elapsedは短く、tokenは増えた。N=5のため、採用上のcost判断は保留する。

## 一次証拠

- prompt: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- bundle SHA-256: `251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`
- ADR9 profile: [`candidate175-review-operation-admission-closure-adr9-r2-medium-m24-n5-cli0146.json`](../profiles/candidate175-review-operation-admission-closure-adr9-r2-medium-m24-n5-cli0146.json)
- ADR9 result: [`eba0a4bc1d0e4391afa631462b8daccb.json`](eba0a4bc1d0e4391afa631462b8daccb.json)
- ADR9 audit: [`candidate175-review-operation-admission-closure-adr9-r2-n5-audit-r1.json`](candidate175-review-operation-admission-closure-adr9-r2-n5-audit-r1.json)
- Standard14 profile: [`candidate175-review-operation-admission-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json`](../profiles/candidate175-review-operation-admission-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- Standard14 result: [`c31b560bce92400293c7b3bc40715246.json`](c31b560bce92400293c7b3bc40715246.json)
- Standard14 quality audit: [`candidate175-review-operation-admission-closure-standard14-n5-quality-audit-r1.json`](candidate175-review-operation-admission-closure-standard14-n5-quality-audit-r1.json)
- ADR9 raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate175-review-operation-admission-closure-adr9-r2-n5-20260810-r2`
- Standard14 raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate175-review-operation-admission-closure-v14-medium-standard14-n5-cli0146-20260810-r1`

## 状態境界

- design audit: `passed`
- implementation audit: `passed`
- ADR9 r2 N=5: `quality_passed / mechanism_passed`
- Standard14 N=5: `quality_passed_70_of_70`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
