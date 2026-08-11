# Candidate176 targeted N=50

## 結論

C173の拡張試験で誤経路または不要なサブエージェント起動が観測された4ケースだけを、Candidate176で各N=50へ拡張した。対象はADR9 r2のADR05・ADR06・ADR07と、Standard14のF02である。

既存N=20を各ケースで再利用し、各30件、合計120件だけを新規発行した。追加120件は全件validで、excluded attemptとrunner errorは0件だった。既存分を含む4ケース合計200件では、Score `4`が199件、Score `1`が1件となり、品質・機序gateは通過しなかった。

## 実行前ゲート

- prompt: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- atomic reuse: 各ケースの既存20件を再利用
- new dispatch: 4ケース × 30件 = 120件
- valid / excluded / runner error: `120 / 0 / 0`

## 結果

| set | case | N | Score `4` | Score `1` | 終端または機序 | reviewer / subagent | artifact変更 |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
| ADR9 r2 | ADR05 | 50 | 49 | 1 | `blocked` 49、`unavailable` 1 | reviewer 50 | 0 |
| ADR9 r2 | ADR06 | 50 | 50 | 0 | `blocked` 50、canary配送0 | reviewer 50 | 0 |
| ADR9 r2 | ADR07 | 50 | 50 | 0 | `completion_ready` 50 | reviewer 50 | 50 |
| Standard14 | F02 | 50 | 50 | 0 | root-only 50 | subagent 0 | required outcomeどおり |

Standard14 F02はN=50の全件でScore `4`となり、C173で観測された不要なサブエージェント起動は0 / 50だった。ADR06とADR07もN=20までの機序を維持した。

## ADR05で新たに観測した失敗

run `79302c5e76874014bbcdf8f5d3304031`では、reviewerは外部consumerという具体的反例を観測した一方、その観測と、存在しない`paired-scope-evidence.json`の読取りを一つのshell invocationへまとめた。前半の決定的証拠は得られたが、後半がexit code `2`となったため、reviewerが主張したsuccess receiptをrootは受理できなかった。結果は期待する`blocked`ではなく`unavailable`となった。

これは試験固有の対象名に関する失敗ではない。独立した観測対象を一つのinvocation resultへ束ねたため、判断を確定できる既観測証拠まで、無関係なmissing evidenceと同時に失効させた一般的な操作境界の問題である。artifact変更は行われていない。このrunは有効な低品質証拠として保持し、再実行で置き換えていない。

## 一次証拠

- ADR N=50 profile: [`candidate176-decision-premise-counterexample-adr9-r2-adr05-adr07-medium-m24-n50-cli0146.json`](../profiles/candidate176-decision-premise-counterexample-adr9-r2-adr05-adr07-medium-m24-n50-cli0146.json)
- ADR N=50 result: [`d85929dc3c334c9a836c416f0eb832ec.json`](d85929dc3c334c9a836c416f0eb832ec.json)
- Standard14 F02 N=50 profile: [`candidate176-decision-premise-counterexample-v14-reasoning-medium-f02-global-m24-n50-cli0146-r1.json`](../profiles/candidate176-decision-premise-counterexample-v14-reasoning-medium-f02-global-m24-n50-cli0146-r1.json)
- Standard14 F02 N=50 result: [`537193868f29459ea4038f5339f415ae.json`](537193868f29459ea4038f5339f415ae.json)
- 集約監査: [`candidate176-decision-premise-counterexample-targeted-n50-audit-r1.json`](candidate176-decision-premise-counterexample-targeted-n50-audit-r1.json)

## 状態境界

- targeted N=50 quality: `failed_199_of_200_score_4`
- targeted mechanism: `failed_adr05_observation_result_boundary`
- adoption: `not_progressed`
- release: `not_created`
- runtime projection: `not_projected`
