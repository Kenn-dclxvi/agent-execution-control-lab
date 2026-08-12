# Candidate192 consumer-bound co-issuance Standard14対象9ケース・F04対照 N=5

> **結果**: `50 / 50 valid / Score 4 = 50 / quality_passed / mechanism_failed / stopped`

## 結論

Candidate191で共同発行退行を観測した9ケースとF04対照だけを各5件、Candidate191の同じ50 atomic runへ互換bindして評価した。Candidate192の新規50件はすべてvalidで、Score `4 = 50`、command protocol violation 0件、unexpected changed path 0件だった。Candidate191で成立した成果品質、review非適用、terminalおよびartifact変更境界は退行していない。

しかし、Candidate192の一変更軸である`DISPATCH_ADMISSION`は機序条件を満たさなかった。A01ではconsumerのない開始identity commandが2 / 5件に残った。A01以外の退行8ケースでは、開始identityと、そのresultに依存しない許可済みreadを同じmodel stepから発行したrunは1 / 40件だけだった。退行9ケース全体では、追加の変更前result roundを作らなかったrunは4 / 45件に留まった。

したがって、consumerとdependencyを定義しただけでは、ready invocationの発行集合を実際のmodel stepへ拘束できていない。品質成功やtoken低下を機序成立の代用にせず、事前停止条件に従って残り4ケース、ADR9、採用、releaseおよびprojectionへ進まない。

## 互換性と登録

- prompt: `the-caption-3ce91a4-consumer-bound-coissuance-r1`
- bundle SHA-256: `1d5770dec7f508c2c6999ed8bff934779efb94f82fb17358da0a63e2098d0f81`
- reference result ID: `4b3fcabe4a004d9a945f6d1bcbdecfdc`
- compatibility key: `58c8563e60f397402b8b6d07f6636273f1836ddc88e0e51ad9df900b8f2719b3`
- Candidate192 pool key: `889fc29433dc0c13a64aef3f724b5ec76ee04ba9de6a4e0dba46784ef58b5a0d`
- selection ID: `a01c24a51e074ee785965a47f7837dfc`
- analysis ID: `f0c878809aab4d7bb9152a3c55255fa9`
- registered result ID: `f53d1494b2ec45d083fdd199ec04a14d`
- result content SHA-256: `4e4b579215441e729a4a25d55b008bf31a741d41704b9e9abd3857927c3d5098`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate192-consumer-bound-coissuance-standard14-affected9-f04-n5-20260812-r1`
- max workers: `24`

comparison preflightは50件発行前に`ready`となった。基準はCandidate191の登録済みatomic runから同じ10ケース各5件だけを選び、Candidate側だけに不足50件を発行した。TPOや別比較系列は追加していない。

## 品質と機序

| 判定 | 結果 |
|---|---:|
| valid | 50 / 50 |
| Score 4 | 50 / 50 |
| command protocol violation | 0 |
| 単一session | 50 / 50 |
| 子agent使用 | 0 / 50 |
| A01 consumerなし開始identityなし | 3 / 5 |
| 退行8ケース identity/read同一step | 1 / 40 |
| 退行9ケース 追加変更前roundなし | 4 / 45 |
| F04 dependency越境なし | 5 / 5 |

F04は「共同発行すべき」と固定したケースではなく対照である。5件中2件はidentityとreadを共同発行し、3件は分離したが、真正dependencyを越えた発行は0件だった。共同発行3件のうち1件は複数identity観測を一つのshell invocationへ集約しており、個別result contractを保持するgateも不通過だった。

owner-producer evidenceは15件が`not_applicable`として適格、35件が独立producer不在で不適格だった。この10ケースは独立review operationを指定していないため、producerを起動しないことが期待経路であり、Rating v14でも同診断は品質点へ影響しない。

## 互換KPI

10ケースN=5の集約中央値は、Candidate191が`1,503,319 tokens`、Candidate192が`1,555,212 tokens`で、Candidate192は`+3.45%`だった。Candidate192のelapsed中央値は`753.759秒`である。ケース別token中央値ではA01 `-49.65%`、F01 `-16.75%`、F02 `-26.27%`だった一方、A02 `+28.28%`、F04 `+29.91%`、F07 canonical `+17.20%`だった。方向が混在し、狙った共同発行も1 / 40しか成立していないため、token差を制御効果へbindしない。

## 一次証拠

- [登録result](f53d1494b2ec45d083fdd199ec04a14d.json)
- [品質監査](candidate192-consumer-bound-coissuance-standard14-targeted-n5-audit-r1.json)
- [機序監査](candidate192-consumer-bound-coissuance-standard14-targeted-n5-mechanism-audit-r1.json)
- [評価profile](../profiles/candidate192-consumer-bound-coissuance-standard14-affected9-f04-control-n5-cli0146.json)
- [評価設計](../../docs/candidate192-consumer-bound-coissuance-standard14-targeted-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate192-consumer-bound-coissuance-standard14-targeted-n5-execution-preparation-audit.md)

## 状態

`candidate192_targeted_standard14_evaluated / fifty_valid / fifty_score4 / quality_passed / mechanism_failed / dispatch_admission_not_behaviorally_binding / remaining_standard14_not_issued / adr9_not_issued / stopped / adoption_not_decided / release_not_created / projection_not_performed`
