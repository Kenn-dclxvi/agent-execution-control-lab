# Portable semantic C147 reference先行資格確認r1結果

> [!IMPORTANT]
> **結果**: `valid_14_of_14 / schema_valid_14 / c147_score4_6 / c147_mechanism_passed_6 / semantic_set_reference_not_qualified / portable_r1_equivalence_unresolved / Standard14_remains_end_to_end_authority / semantic_r2_not_created`

## 結論

新しいsemantic held-out r1をportable同等性の品質gateへ使う前に、直接の親C147 reference一枚を同じ14 Case N=1で資格確認した。14件すべてでschema適合応答、all-agent一次tokenおよびelapsedを取得したが、Score 4は6 / 14、機序通過も6 / 14だった。事前に固定した14 / 14のreference gateを通過しなかったため、semantic held-out r1をC147同等性テストとして資格なしと判定する。

portable r1は同じheld-outで7 / 14だったが、この値をC147機能再現率、portable完成率またはC147より一件優れる証拠へ使わない。両promptのqualityは、C147自身が通過しない未資格のoracleに対する記述値に限る。portable r1の正式resultと当時の`quality_failed`は履歴として保持するが、現在のportable同等性判断は`unresolved`へ戻す。

## 固定条件

- prompt: `portable-semantic-c147-full-agent-reference-r1`
- source: `the-caption-3ce91a4-result-effect-scope-r1`
- bundle SHA-256: `d330421521b231d6029e69e8cd6d4e175fb46b06254e80b3d2f4d8f8f3a55d9f`
- Profile: `portable-semantic-c147-full-agent-reference-codex-cli0146-sol-medium-heldout-r1-n1-r1`
- evaluation set: `portable-instruction-semantic-heldout-r1` / `r1`
- rating: `portable-instruction-semantic-exact-v1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime: Codex CLI `0.146.0`
- token accounting: all-agent `v2`
- permission: read-only / approval `never`
- N / M: `N=1` / `M=24`
- raw root: `/Users/kenn/repos/_verification/portable-semantic-c147-full-agent-reference-heldout-r1-n1-20260818-r1`

Profile、planおよびpreflightはprompt identityと系列identity以外をportable r1条件へ一致させた。preflightはPIC-H01〜PIC-H14の14 slotだけを`dispatch_allowed=true / issued_slot_count=0`で許可し、14件を同一model stepから発行した。external failure、再試行およびexcluded resultは0件である。

## 測定値

| 指標 | C147 reference | portable r1 | 備考 |
| --- | ---: | ---: | --- |
| valid | 14 / 14 | 14 / 14 | 両条件で測定成立 |
| Score 4 | 6 / 14 | 7 / 14 | 未資格set上の記述値 |
| 機序通過 | 6 / 14 | 7 / 14 | 未資格set上の診断値 |
| token中央値 | 15,749.0 | 15,337.5 | 品質非同等のため効率判定に使わない |
| elapsed中央値 | 11.037秒 | 11.173秒 | 品質非同等のため効率判定に使わない |

C147のScore分布はScore 1が2件、Score 2が6件、Score 4が6件だった。portable r1との差をcost改善、品質改善またはportable効果へ帰属しない。

## Case別結果

| Case | C147 | portable r1 | C147の主な差 |
| --- | ---: | ---: | --- |
| H01 | 2 | 4 | deniedな2 operationを`unavailable`へ再掲 |
| H02 | 4 | 4 | exact |
| H03 | 2 | 2 | deniedなreadを`unavailable`へ再掲 |
| H04 | 2 | 2 | 既存terminalとdenied operationを再掲 |
| H05 | 2 | 2 | 既存terminal operationを再掲 |
| H06 | 4 | 4 | exact |
| H07 | 4 | 4 | exact |
| H08 | 4 | 4 | exact |
| H09 | 4 | 4 | exact |
| H10 | 1 | 1 | failed個別resultに加え集約validationをterminal化 |
| H11 | 1 | 1 | 個別terminal／後続unavailableを再掲し、未知のcontinuation IDを追加 |
| H12 | 4 | 4 | exact |
| H13 | 2 | 2 | 既存terminal executionを再掲 |
| H14 | 2 | 2 | 既存terminalとdenied代替methodを再掲 |

H03、H04、H05、H10、H13、H14では、portable r1とC147が同じCaseで同型の余分な状態出力を行った。H11も両方がexact oracleを外し、個別resultと集約状態のprojectionを一意にできなかった。この一致は、少なくとも当該差をportable再表現固有の退行へ帰属できないことを示す。

## 判定

semantic held-out r1の状態を次で固定する。

- measurement transport: `qualified`
- control-free quality: `descriptive_only`
- C147 reference quality: `6 / 14 / reference_not_qualified`
- portable r1 quality: `7 / 14 / equivalence_unresolved`
- C147との効率比較: `not_performed`
- Standard14代替: `not_authorized`
- N=5 / N=20: `not_authorized`

既存held-out r1、oracle、TaskSpec、response schema、ratingおよび両resultを変更しない。低Scoreを再試行しない。

## 次の境界

semantic setを維持する場合は、別revisionで次を先に固定する。

1. model-visible共通contractへ、response fieldが入力時点の状態一覧ではなく今回の合法な遷移を表すかどうかを明示する。
2. 個別result、個別operation、後続発行permissionおよび集約completionの対応をCase固有正解なしで定義する。
3. 新revisionをportableより先にC147で資格確認する。
4. C147が全件通過した場合だけportable局所診断へ使う。

このrevisionを作らない場合はsemantic setをportable完成gateから外し、Standard14の互換end-to-end比較へ一本化する。どちらの場合も、現在のheld-out r1へportable promptを合わせない。

## 参照

- [`正式result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-full-agent-reference-heldout-r1-n1-qualification-r1.json)
- [`reference先行資格確認設計`](portable-semantic-c147-reference-qualification-design.md)
- [`portable r1正式result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json)
- [`Candidate147 Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
