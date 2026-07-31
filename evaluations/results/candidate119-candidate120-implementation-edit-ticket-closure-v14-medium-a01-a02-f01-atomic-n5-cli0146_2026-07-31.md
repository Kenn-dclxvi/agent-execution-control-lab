# Candidate119 / Candidate120 implementation edit ticket closure結果

## 結論

Candidate120は15 / 15件がscore `4`だったが、狙ったimplementation bind後のterminal closureを成立させなかった。A02の確定表明後・最初のartifact変更前のcommand再入はCandidate119の1 / 5件から2 / 5件へ増えた。変更後・最初のvalidation前method探索は0 / 5件を維持した。

A02 token中央値は`149,154`から`220,592`へ`71,438`（`47.90%`）増え、Candidate107目標`125,559`を`95,033`（`75.69%`）上回った。quality gateだけが通過し、mechanism gateとcost gateは不通過である。N=20、Standard14、採用、release、runtime projection、本体反映へ進めず、Candidate120を`stopped`とする。

## Identityと結果

- candidate: `the-caption-3ce91a4-implementation-edit-ticket-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`
- bundle SHA-256: `c171d3c12fcd81158b72fa234975c252fa06bae6917909efef2ad6ff41f0a8c1`
- cases: A01 r2 / A02 r2 / F01 r3、各`N=5`
- Rating / model / reasoning: v14 / `gpt-5.6-sol` / Medium
- CLI / Python / profile M: `0.146.0` / `3.14.5` / 24
- execution: 15 / 15 valid、excluded 0、external failure 0
- quality: score `4` × 15
- pool key: `baf02bb8668ab67f82bb2e1db58a5f274744cc78f88c40daa6a8086fbbf57380`
- selection ID: `8e35a26de73e481abfe1d2536278e0fc`
- analysis ID: `68a64da53d6d48a0ad5ae47e7489507d`
- result ID: `0139d66832684d39a6f2b34ec1781d1f`

## Gate判定

| 判定項目 | Candidate119 | Candidate120 | gate |
| --- | ---: | ---: | --- |
| score `4` | `15 / 15` | `15 / 15` | pass |
| A01変更・testなし | `5 / 5` | `5 / 5` | pass |
| A02 canonical成果 | `5 / 5` | `5 / 5` | pass |
| A02 bind表明後・変更前再入 | `1 / 5` | `2 / 5` | fail |
| A02変更後method探索 | `0 / 5` | `0 / 5` | pass |
| F01 required command evidence | `5 / 5` | `5 / 5` | pass |
| A02 token中央値 | `149,154` | `220,592` | fail |

再入したrunは`155217731fd145e78221912ce5d77843`と`f275dcab9bbc4ecdaf5bdc9bcb0067bc`である。前者は正規entrypointと旧参照の不一致を確定した後に、関連instructionとrouting testを追加確認した。後者は原因と変更箇所を確定した後に、test fileを追加で読んだ。どちらもその後の成果とvalidationは成功したため、quality失敗ではなく狙ったevent sequenceの不成立である。

Candidate120の「確定表明をedit ticketのcommit pointにする」という新labelは、追加evidenceを止めなかった。むしろagentが確定表明を遅らせる余地を増やし、変更前探索そのものを減らさなかった。したがってこのlabelを微修正して続けない。

3 case集約中央値もtoken `325,773 → 409,426`（`+25.68%`）、elapsed `159.656 → 172.511`秒（`+8.05%`）で両方増えた。これはtargeted 3 caseの結果であり、Standard14へ一般化しない。

## 状態

`targeted_a01_a02_f01_evaluated / quality_gate_passed / postchange_method_boundary_preserved / edit_ticket_closure_failed / aggregate_cost_both_higher / a02_cost_target_failed / result_registered / stopped`

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate120-implementation-edit-ticket-closure-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- execution archive SHA-256: `1afd477006aeabe53548294ea0345a98ce775a37c5e44eaaf6737a44d48a26f7`
- final archive SHA-256: `b77dd789c3dbce7bb3b977051740a2a6c22b69cb5d1e05a03324e15aa54c36f8`
- quality audit: `batch-001/quality-audit.json`
- selection: `candidate-selection.json`
- analysis: `candidate-analysis.json`
