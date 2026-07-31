# Candidate110 validation実行票decision boundary F03 atomic N=5結果

## 結論

Candidate110のF03 r2 N=5は5 / 5件がvalid・rateable・score `4`で、required validationも全件一回だった。一方、実行票全体がterminalになる前にmodelへ戻らなかったrunは2 / 5件だけで、作成前mechanism gateを通過しなかった。

残る3件はouter yield `1000ms`を選び、3 / 3件がcell ID付きnonterminal resultを返した。うち2件は次のwaitより先に進捗messageを出した。既存`DECISION_BOUNDARY`へ実行票の途中状態を対応付ける抽象境界だけでは、途中状態を要求する発行選択を閉じられなかった。

当初はmechanismを主目的としてKPI比較前に停止したが、ユーザー訂正により3 KPIを主結果へ戻した。保存済みCandidate108との互換比較ではquality同値、token中央値`-1,844`（`-1.31%`）、elapsed中央値`-5.384`秒（`-6.99%`）だった。

ただし狙った制御は2 / 5件でしか成立せず、targeted KPI低下を制御効果へbindできない。ユーザー判断によりStandard14へ拡大せず停止する。残り65 slotのpreflight準備後、評価slotを一件も発行せず未実行profileとcampaignを撤回した。

## 固定条件

- candidate: `the-caption-3ce91a4-validation-ticket-decision-boundary-r1`
- bundle SHA-256: `b9e1140ebdfb79d66c04dd47f478f85ec985122de104f0b08eef25d03fa5cdbe`
- direct parent / reference: Candidate108
- case: `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: 5
- profile上のM: 24
- atomic pool key: `f37f35babce19d18a88a1c48b68b902a62d44fc026261c9d78e8a596da760fdc`
- comparison key: `6374fd3705e8f9afead12a3cea1ba8e0b2ccd0b2d62f6a4443381fbfc061083d`

## 結果

| 項目 | Candidate110 |
| --- | ---: |
| valid / rateable / score 4 | 5 / 5 / 5 |
| validation ticket wrapper一回 | 5 / 5 |
| focused validation一回 | 5 / 5 |
| full validation一回 | 5 / 5 |
| required validation成功 | 5 / 5 |
| terminal前model再入なし | 2 / 5 |
| cell ID付きnonterminal result | 3 / 5 |
| nonterminal後、messageなしでwait | 1 / 3 |
| nonterminal後の進捗message | 2件 / 2 run |
| required validation再実行 | 0 / 5 |
| quality中央値 | 100.0 |
| token中央値 | 138,755 |
| elapsed中央値 | 71.596秒 |

Candidate108の中央値はquality `100.0`、token `140,599`、elapsed `76.980`秒である。

owner-producer evidenceは5件ともproducer候補0で`failed`だった。Rating v14では`diagnostic_only`であり、提示済み成果条件、必須command evidence、許可pathの成立を確認して5件ともscore `4`とした。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate110-validation-ticket-decision-boundary-v14-medium-f03-atomic-n5-cli0146-20260731-r1`
- comparison preflight SHA-256: `b5803fea5611b4804cf80871aa46ca9f12833e36fe01fac8576b8fa740f7afc9`
- execution archive SHA-256: `f47502cb118ed5eab455672e2fa9f239430c4167798e740a8cdf37966da30e17`
- quality audit SHA-256: `0bd1e2cd0e69b5f2ab24a5929e4b8ee27f961e5ec57ef6402bae45ba77f84578`
- mechanism audit SHA-256: `13d0cff3d6e740d8a0e4d826f5b01dc307c5a5ef6acf16ea02997970ae3b440f`
- selection SHA-256: `39f7e4f490de41cb2e34b7b7e35c4af94d3d8e05d2c9e34da29b354a14621835`
- analysis SHA-256: `cd0d2a401342807afa8d02ad81d8592e722f2fb204155ea49cb5ed563e29d3ab`
- comparison SHA-256: `d59c7af8a0dde7511fd0b2aba37d6abbb4641765118124c9eb00cec97acde57d`

## 状態

`targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / control_not_demonstrated / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。
