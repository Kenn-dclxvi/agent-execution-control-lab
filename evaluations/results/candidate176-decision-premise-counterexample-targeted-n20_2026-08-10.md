# Candidate176 targeted N=20

## 結論

C173の拡張試験で誤経路が観測されたケースだけを、Candidate176で各N=20へ拡張した。対象はADR9 r2のADR05・ADR06・ADR07と、Standard14でサブエージェント起動が観測されたF02である。

既存のCandidate176 N=5を各ケースで再利用し、各15件、合計60件だけを新規発行した。追加60件は全件validで、既存分を含む4ケース合計80件はすべてScore `4`だった。ADR側の期待経路、ADR06の情報封鎖、Standard14 F02のroot-only実行も全件で成立した。

## 対象を選んだ根拠

- C173 ADR9 r2 N=50：ADR05で誤経路2件、ADR06で禁止canary配送1件、ADR07で過剰停止1件を観測した。
- C173 Standard14 N=50：F02の1件でcriterion owner文字列を独立producer指定と誤認し、サブエージェントを起動した。品質Scoreは4だったが機序違反として保持された。
- 上記以外のケースは今回の追加対象にしていない。

## 実行前ゲート

- prompt: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- atomic reuse: 各ケースの既存5件を再利用
- new dispatch: 4ケース × 15件 = 60件
- valid / excluded: `60 / 0`

## 結果

| set | case | N | Score `4` | 終端または機序 | reviewer / subagent | artifact変更 |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| ADR9 r2 | ADR05 | 20 | 20 | `blocked` 20 / 20 | reviewer 20 | 0 |
| ADR9 r2 | ADR06 | 20 | 20 | `blocked` 20 / 20、canary配送0 | reviewer 20 | 0 |
| ADR9 r2 | ADR07 | 20 | 20 | `completion_ready` 20 / 20 | reviewer 20 | 20 |
| Standard14 | F02 | 20 | 20 | root-only 20 / 20 | subagent 0 | required outcomeどおり |

F02はC173 N=50で観測した独立producer過剰起動を0 / 20に抑えた。ADR05は判断前提の直接反証を20 / 20で具体的反例として受け入れ、artifactを変更せず停止した。ADR06とADR07も既存N=5の機序を維持した。

## 一次証拠

- ADR N=20 profile: [`candidate176-decision-premise-counterexample-adr9-r2-adr05-adr07-medium-m24-n20-cli0146.json`](../profiles/candidate176-decision-premise-counterexample-adr9-r2-adr05-adr07-medium-m24-n20-cli0146.json)
- ADR N=20 result: [`c5f3eb7b655941a3ac077566a735363e.json`](c5f3eb7b655941a3ac077566a735363e.json)
- Standard14 F02 N=20 profile: [`candidate176-decision-premise-counterexample-v14-reasoning-medium-f02-global-m24-n20-cli0146-r1.json`](../profiles/candidate176-decision-premise-counterexample-v14-reasoning-medium-f02-global-m24-n20-cli0146-r1.json)
- Standard14 F02 N=20 result: [`5e14b9628a1a4586832cc4f67edc2c1c.json`](5e14b9628a1a4586832cc4f67edc2c1c.json)
- 集約監査: [`candidate176-decision-premise-counterexample-targeted-n20-audit-r1.json`](candidate176-decision-premise-counterexample-targeted-n20-audit-r1.json)

## 状態境界

- targeted N=20 quality: `passed_80_of_80`
- targeted mechanism: `passed`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 後続のcommand evidence再判定

2026-08-12の[訂正機構監査r2](candidate176-decision-premise-counterexample-mechanism-reassessment-r2.json)では、ADR追加45 runに対するcollector報告19件のうち17件を誤検出、ADR05 run `159b3cf3ab6f4b48962e0946a8c2faa8`とADR07 run `07264470f1114e9dba541604616aa536`の2件を真正なmachine-bound exit code欠落と判定した。

80 / 80 Score 4と各terminalは保持するが、targeted N=20の現在の機序解釈は`mechanism_failed`である。今後は登録resultと訂正機構監査r2を一組としてbindし、旧`targeted mechanism: passed`を比較基準にしない。
