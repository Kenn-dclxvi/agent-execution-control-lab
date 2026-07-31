# Candidate108 / Candidate114 spec-ready evidence phase boundary targeted結果

## 結論

Candidate114のA01 r2 / A02 r2 / F01 r3各N=5は15 / 15件がvalid・rateableで、score分布は`4: 14件 / 1: 1件`だった。A01は5 / 5件がtarget、test、history、authorityを追加探索せず、開始状態確認後のclarificationへ到達した。狙ったA01のphase分離は成立した。

一方、A02の1 / 5件がrepository authorityのpath未記載を理由にclarificationへ誤停止し、成果を作らなかった。事前quality gateの15 / 15 score `4`を満たさないため、Candidate114はStandard14へ進めず停止する。

## 固定条件

- candidate: `the-caption-3ce91a4-spec-ready-evidence-phase-boundary-r1`
- bundle SHA-256: `c6cd2756a8a1a5b192ed6eb5f17dc380bd884873c23c3f190d9974fc09c757dd`
- direct parent / reference: Candidate108
- cases: A01 r2 / A02 r2 / F01 r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: case別に5
- profile上のM: 24
- ready slot: 15件
- candidate pool key: `ef6b5f782a977a6f5de2d4c57d379285c2f32bec733b6e90e416b8b43ecbae5f`
- reference result ID: `bf0e18fedb054cd2a558fbb3d89ec0b9`
- candidate result ID: `c67f35690bd34cb38a504285500cc0bf`

Candidate108の同じ15 atomic runは保存済みpoolから再利用し、再実行は0件だった。Candidate114の15 slotは一つのglobal queueへ入れ、設定`M=24`で実行した。attempt 15、excluded 0、実時間は`95.316`秒だった。

## 3 KPI

| 項目 | Candidate108 | Candidate114 | C114 - C108 |
| --- | ---: | ---: | ---: |
| quality中央値 | `100.0` | `100.0` | `0.0` |
| token中央値 | `420,683` | `337,689` | `-82,994`（`-19.73%`） |
| elapsed中央値 | `218.560`秒 | `194.812`秒 | `-23.748`秒（`-10.87%`） |

中央値では両KPIが低下したが、A02にscore `1`があるため改善判定には使わない。15 runのtoken合計は`2,185,593 -> 1,680,369`で`-505,224`（`-23.12%`）だった。

| case | score 4 | token中央値 C108 | token中央値 C114 | 差 | elapsed中央値 C108 | elapsed中央値 C114 | 差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | `5 / 5` | `78,687` | `33,409` | `-45,278`（`-57.54%`） | `40.516`秒 | `27.100`秒 | `-13.416`秒（`-33.11%`） |
| A02 | `4 / 5` | `200,556` | `182,116` | `-18,440`（`-9.19%`） | `99.226`秒 | `85.968`秒 | `-13.258`秒（`-13.36%`） |
| F01 | `5 / 5` | `152,145` | `143,865` | `-8,280`（`-5.44%`） | `77.992`秒 | `82.091`秒 | `+4.099`秒（`+5.26%`） |

## 挙動分析

A01は5件とも開始状態だけを確認して一度のclarificationで停止した。target source、関連test、git history、repository authorityの探索、変更、試験は0件だった。Candidate108の狙ったroute 1 / 5から5 / 5へ増え、phase境界は観測routeへ作用した。

A02の成功4件は、TaskSpecの「canonical targetはrepository authorityと現行entrypoint実体を根拠に決める」をauthority探索のadmissionとして扱った。失敗run `daf49b9bd6534ee1affcff06d04e7902`は開始状態だけを確認し、authorityのファイルまたは定義箇所がTaskSpecに未記載として利用者へ質問した。

残余差はauthorityを使うかどうかではない。TaskSpecがauthority利用を明示した後、そのauthority location自体をallowed read内で解決してよいかという一つの解釈差である。Candidate114のphase分離を維持し、この解釈だけを次candidateで検証する。

## 状態

`targeted_a01_a02_f01_evaluated / a01_mechanism_passed / quality_gate_failed / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate114-spec-ready-evidence-phase-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- execution archive SHA-256: `c6d52514d0b223a6a4db3830d349774157d776095ae4113e9bdd7427b3d21092`
- registered result: `c67f35690bd34cb38a504285500cc0bf`
