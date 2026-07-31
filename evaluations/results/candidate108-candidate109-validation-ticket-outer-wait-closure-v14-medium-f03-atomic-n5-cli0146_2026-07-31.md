# Candidate108 / Candidate109 F03 atomic N=5結果

## 結論

Candidate109のF03 r2 N=5は5 / 5件がvalid・rateable・score `4`で、required validationは全件一回、terminal前のmodel再入と途中messageは0件だった。

保存済みCandidate108 F03 N=5との互換比較では、Candidate109の中央値はquality `100.0`、token `118,151`、elapsed `64.330`秒だった。Candidate109 minus Candidate108はquality `0.0`、token `-22,448`（`-15.97%`）、elapsed `-12.650`秒（`-16.43%`）である。

ただしCandidate109は、prompt制御の判断境界ではなくouter yieldの最大値という実行方法を指定した。後続の設計原則再確認により、prompt-only Candidateの変更軸として不適切と判断した。数値結果は診断証拠として保持し、Standard14、採用、release、runtime projectionへ進めない。

## 固定条件

- candidate: `the-caption-3ce91a4-validation-ticket-outer-wait-closure-r1`
- bundle SHA-256: `fe39d4f66f981f0be35fe20dcf53562cf06dc00442dfc909895e3dcd10fc8c0d`
- direct reference: Candidate108の保存済みF03 N=5
- case: `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: 5
- profile上のM: 24
- comparison key: `6374fd3705e8f9afead12a3cea1ba8e0b2ccd0b2d62f6a4443381fbfc061083d`

## 結果

| 項目 | Candidate109 |
| --- | ---: |
| valid / rateable / score 4 | 5 / 5 / 5 |
| focused validation一回 | 5 / 5 |
| full validation一回 | 5 / 5 |
| terminal前model再入 | 0 / 5 |
| validation途中message | 0 / 5 |
| required validation再実行 | 0 / 5 |
| quality中央値 | 100.0 |
| token中央値 | 118,151 |
| elapsed中央値 | 64.330秒 |

owner-producer evidenceは5件ともproducer候補0で`failed`だった。Rating v14では`diagnostic_only`であり、提示済み成果条件、必須command evidence、許可pathの成立を確認して5件ともscore `4`とした。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate109-validation-ticket-outer-wait-closure-v14-medium-f03-atomic-n5-cli0146-20260731-r1`
- comparison preflight SHA-256: `8c20038bff81bc43c2f81cc732bbf1413597cc8a45e4b155811658e850b1c08d`
- quality audit SHA-256: `9e6280157212d3e8927f2cb117ac8ad2f791c30dd4aa8b008e25832f29ac2e32`
- mechanism audit SHA-256: `0da3d0d2da63fc9128070c94ccdb05ae0aba075bf53a4502b40cf8cdcfa6c943`
- analysis SHA-256: `3e25771c50f9c292fd07d4dcae01b7ef52b810391cf315cac7a625b029d6dcc0`
- comparison SHA-256: `57469303e4afa84dc2529a9f2e7615acceb1ffeb7bcc8f4a9a44c83d44770eb7`

## 状態

`targeted_f03_evaluated / quality_gate_passed / terminal_before_reentry_passed / cost_both_lower / prompt_design_boundary_failed / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。
