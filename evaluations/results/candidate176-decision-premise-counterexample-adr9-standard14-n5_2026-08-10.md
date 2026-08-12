# Candidate176 ADR9 r2 / Standard14 N=5

## 結論

Candidate176は、固定一般設計が境界判断に使う明示前提を、許可済みの具体的事実が直接反証する経路をCandidate175へ追加した。評価ケースと採点契約を変更せず、ADR9 r2を9 case × 5、Standard14を14 case × 5で評価した。

ADR9は45 / 45 run、Standard14は70 / 70 runがvalidかつScore `4`だった。修正対象のADR05は5 / 5で`blocked`となり、独立reviewerを各回1件起動し、artifact変更は0件だった。ADR9の他8ケースも既存の期待経路を保持し、Standard14では独立reviewer起動が0 / 70だった。

品質と機序の初回gateは通過した。N=5の記述値では、Candidate175比でADR9のtokenとelapsedが増え、Standard14はtokenが減りelapsedが増えた。採用、release、本体反映は別判断であり、まだ実施していない。

## 変更前レビューと実装試験

- 一般設計: [`candidate176-decision-premise-counterexample-design-r13.md`](../../docs/candidate176-decision-premise-counterexample-design-r13.md)
- 情報封鎖した最終review packet: [`candidate176-decision-premise-counterexample-review-packet-r13.md`](../../docs/candidate176-decision-premise-counterexample-review-packet-r13.md)
- 設計監査: [`candidate176-decision-premise-counterexample-design-audit.md`](../../docs/candidate176-decision-premise-counterexample-design-audit.md)
- 実装監査: [`candidate176-decision-premise-counterexample-implementation-audit.md`](../../docs/candidate176-decision-premise-counterexample-implementation-audit.md)
- リポジトリ試験: `1104 passed, 1752 subtests passed`

最終設計と実装の独立再監査はいずれも`no_counterexample_found`だった。既存評価ケース、fixture、oracle、rating contract、試験コードは変更していない。

## ADR9 r2 N=5

### 実行前ゲート

- reference: Candidate175 `eba0a4bc1d0e4391afa631462b8daccb`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- 発行: Candidate176の不足45 slotのみ
- valid / excluded: `45 / 0`

### case別結果

| case | 終端 | valid | Score `4` | reviewer起動 | artifact変更 |
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

ADR06で禁止canaryをreviewerへ配送したrunは0件だった。ADR08はpermission否定をreview operation作成前に適用し、reviewer起動は0件だった。

### Candidate175との記述比較

| KPI中央値 | Candidate175 | Candidate176 | 差 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,123,616 | 1,233,829 | `+110,213`（`+9.81%`） |
| elapsed seconds | 733.368 | 865.427 | `+132.059秒`（`+18.01%`） |

N=5の記述値であり、cost差を一般的な効果へ一般化しない。

## Standard14 N=5

### 実行前ゲート

- reference: Candidate175 `c31b560bce92400293c7b3bc40715246`
- evaluation set: `the-caption-standard14-r1 / r1`
- evaluation set identity: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- 発行: Candidate176の不足70 slotのみ
- valid / excluded: `70 / 0`

### 品質結果

14 caseすべてが5 / 5 Score `4`で、合計70 / 70だった。failure countとcommand protocol violationはいずれも0件、monthly format reviewの数値位置は5 / 5で`exact`だった。独立reviewer spawnは0 / 70で、全runがroot-onlyだった。

### Candidate175との記述比較

| KPI中央値 | Candidate175 | Candidate176 | 差 |
| --- | ---: | ---: | ---: |
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,692,063 | 1,649,559 | `-42,504`（`-2.51%`） |
| elapsed seconds | 804.940 | 958.386 | `+153.447秒`（`+19.06%`） |

品質は維持し、tokenは減り、elapsedは増えた。N=5のため、採用上のcost判断は保留する。

## 一次証拠

- prompt: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- bundle SHA-256: `45c8162191e4c844f33188f492bf56768021a26be5f790d8bb9cf825716d56be`
- ADR9 profile: [`candidate176-decision-premise-counterexample-adr9-r2-medium-m24-n5-cli0146.json`](../profiles/candidate176-decision-premise-counterexample-adr9-r2-medium-m24-n5-cli0146.json)
- ADR9 result: [`d3e91302f0d14350906075676c5a2791.json`](d3e91302f0d14350906075676c5a2791.json)
- ADR9 audit: [`candidate176-decision-premise-counterexample-adr9-r2-n5-audit-r1.json`](candidate176-decision-premise-counterexample-adr9-r2-n5-audit-r1.json)
- ADR9 comparison: [`candidate176-decision-premise-counterexample-adr9-r2-n5-comparison-c175-r1.json`](candidate176-decision-premise-counterexample-adr9-r2-n5-comparison-c175-r1.json)
- Standard14 profile: [`candidate176-decision-premise-counterexample-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json`](../profiles/candidate176-decision-premise-counterexample-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- Standard14 result: [`a0702207f03a4cb18c8b501329b74023.json`](a0702207f03a4cb18c8b501329b74023.json)
- Standard14 quality audit: [`candidate176-decision-premise-counterexample-standard14-n5-quality-audit-r1.json`](candidate176-decision-premise-counterexample-standard14-n5-quality-audit-r1.json)
- Standard14 comparison: [`candidate176-decision-premise-counterexample-standard14-n5-comparison-c175-r1.json`](candidate176-decision-premise-counterexample-standard14-n5-comparison-c175-r1.json)
- ADR9 raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate176-decision-premise-counterexample-adr9-r2-n5-20260810-r3`
- Standard14 raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate176-decision-premise-counterexample-v14-medium-standard14-n5-cli0146-20260810-r1`

## 状態境界

- design audit: `passed`
- implementation audit: `passed`
- ADR9 r2 N=5: `quality_passed / mechanism_passed`
- Standard14 N=5: `quality_passed_70_of_70`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 後続のcommand evidence再判定

2026-08-12にADR9の生traceを統一基準で再監査した。[訂正機構監査r2](candidate176-decision-premise-counterexample-mechanism-reassessment-r2.json)では、collector報告17件のうち16件は誤検出だったが、ADR09 run `30c3e517fba84368b4f9af759847cc44`のwrapperが`text(r.output)`だけを返し、machine-bound exit codeを失った真正違反1件を確認した。

45 / 45 Score 4、terminal、reviewer cardinality、artifact境界およびStandard14結果は保持する。一方、ADR9 N=5の現在の機序解釈は`mechanism_failed`であり、上記の旧`mechanism_passed`を今後の比較基準にしない。登録result `d3e91302f0d14350906075676c5a2791`と訂正機構監査r2を一組としてbindする。
