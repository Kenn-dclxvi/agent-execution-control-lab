# Candidate266 F01・F02・F03・F10 entrypoint N=5

> **現在系列での位置づけ訂正（2026-08-16）**: このN=5は、C147上の局所機序を観測した履歴としては有効だが、利用者が求めたCandidate254系の有効制御保持とCandidate264の弱化修復を判定できない。目的に直接対応しないprobeを別のrequired outcomeへ置き換えて発行したため、本来は評価slotを発行すべきではなかった。以下の実測値は変更せず、現在系列では`off_target_diagnostic_evidence`に限定し、改善根拠、親、必須gate、Standard14移行または採用判断へ使わない。

## 結論

Candidate266の機械的なinstruction依存は、対象四ケース各N=5で品質と正常経路を維持し、F10の誤経路を5 / 5件で閉じた。`src/AGENTS.md`の内容が必要か、適用されるか、後続readへ影響するかをモデルへ自己判定させていない。TaskSpecに明示されたexact path、配下pathのprefix関係、exact readのterminal success content resultだけをpermission開放条件にした。

ただし、これはC147上で一つのpermission edgeだけを切り出した機序probeである。Candidate254を直接の基盤とするCandidate264系の有効制御を保持した改善Candidateではない。したがってCandidate266の通過をCandidate264の置換、採用、Standard14移行またはrelease判断には使わない。

## 結果

| ケースと観測 | C147 N=5 | Candidate264 N=5（診断） | Candidate266 N=5 |
|---|---:|---:|---:|
| F01 開始identityと許可済みreadを同一model stepから発行 | 5 / 5 | 5 / 5 | 5 / 5 |
| F02 同上 | 5 / 5 | 5 / 5 | 5 / 5 |
| F03 同上 | 5 / 5 | 5 / 5 | 5 / 5 |
| F10 `src/AGENTS.md` success result後にだけ配下readを発行 | 2 / 5 | 2 / 5 | 5 / 5 |
| F10 result後に必要な配下readを完遂 | 5 / 5 | 5 / 5 | 5 / 5 |

F10の5件では、raw rollout上のexact instruction call、対応するtool output、最初の`src/app/entrypoints`配下callのevent indexがすべて`11 -> 12 -> 15`だった。instruction result前の配下listing・本文readは0件である。

品質は20 / 20件がScore `4`、必須commandのnonzeroは0件、許可外変更は0件だった。validation wrapperのcell ID waitは全ケース0件であり、追加model再入は発生しなかった。このwait頻度は対象permission機序の判定条件には含めていない。

## KPI

| 比較 | quality | total_tokens | elapsed_seconds |
|---|---:|---:|---:|
| C147 | 100.0 | 494,706 | 302.929 |
| Candidate264（診断） | 100.0 | 484,121 | 307.710 |
| Candidate266 | 100.0 | 476,908 | 291.481 |
| Candidate266 − C147 | 0.0 | -17,798（-3.60%） | -11.447（-3.78%） |
| Candidate266 − Candidate264 | 0.0 | -7,213（-1.49%） | -16.229（-5.27%） |

N=5では10%を超えるcost退行はなく、tokenと時間はいずれも減少した。これを機序の一般的なcost効果へ外挿せず、今回の四ケースN=5の観測として保持する。

## 証拠と状態

- Candidate266 selection: `0cbcb3a897aa402397d91b43aa49ecac`
- Candidate266 analysis: `111fd55bcc0741d3a85c32f307b1a48e`
- 登録result: `5ca7e3a68e444ccbad70ecf50a82236a`
- C147基準result: `29cf98307448409f820a739b2d008f7b`
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`
- quality audit: [`candidate266-declared-instruction-descendant-read-dependency-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json`](candidate266-declared-instruction-descendant-read-dependency-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json)
- mechanism audit: [`candidate266-declared-instruction-descendant-read-dependency-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json`](candidate266-declared-instruction-descendant-read-dependency-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)
- 実行準備監査: [`candidate266-f01-f02-f03-f10-entrypoint-n5-execution-preparation-audit.md`](../../docs/candidate266-f01-f02-f03-f10-entrypoint-n5-execution-preparation-audit.md)

slot発行前の容量guardを完了直後に回した手順逸脱は、再実行で隠さず実行準備監査へ固定した。

当時の観測状態は`mechanism_probe_passed / targeted_n5_quality_passed / normal_routes_passed / no_cost_regression`として保持する。現在系列での状態は`objective_mismatch_confirmed / off_target_diagnostic_evidence / historical_observation_only / not_candidate264_replacement / not_parent / not_required_gate / adoption_not_approved / standard14_not_started / release_not_created / projection_not_performed`とする。
