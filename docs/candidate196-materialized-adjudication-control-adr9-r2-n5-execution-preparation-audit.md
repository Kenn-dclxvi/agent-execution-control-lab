# Candidate196 materialized adjudication control ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate196のADR9 r2全9ケース各5件は、Candidate195の登録済み45 atomic runsと保存Layer 1を参照へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、Candidate196の不足45件だけを許可した。監査時点の発行数は0件である。

Candidate195 runはCandidate196 runとして流用していない。Candidate195は互換参照でありprompt親ではない。直接親はCandidate147である。

## 固定identity

- profile: `candidate196-materialized-adjudication-control-adr9-r2-medium-m24-n5-cli0146`
- profile SHA-256: `688c302f01bc3954f5ad4eaf337436ba74eacba06966ad52929cc62324306fbc`
- reference result: `457400a8506d404f8b564074d0b28802`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate195 reference pool: `5643489ca90215addca33c43a4de5bce88a5b6a7d9363784671dba7fd4fe7428`
- Candidate196 pool: `1352703cc5b95bdc539ff16a2206423c786f4bb4a8b7144c336baab712b04407`
- plan ID: `1b1ca945dcc04105838c9442674d9020`
- dispatch plan SHA-256: `5b109a33e2309fc9189af4c977fb04cde12e8a06b22d190506598f59ebd8701a`
- global plan SHA-256: `73afad47af66b974fa9a2e7e34a2507fa61887d5a3e6a18a1eb7e17b317984be`
- comparison generation SHA-256: `42252dd4c217008c25684c7261014b5faf4651841b28f0c77d67f14d4fa55d7c`
- comparison preflight SHA-256: `1159a4c9d2addfdebb663392a885f0d42069a766bdcd076a2d31872c5fdc8409`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate196-materialized-adjudication-control-adr9-r2-n5-20260812-r1`

## 不足計画と互換性

`seed-pool`は架空runを作らずCandidate196の空poolを作成した。`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件とした。45 capsuleは独立sample IDを持つ。

Evaluation set、9 case revision、fixture identity、TaskSpec、rating、command evidence protocol、model、reasoning、Agent/runtime/CLI、permission、executor、token accounting、target commit/treeおよびM=24はCandidate195登録resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

最初のatomic plan生成は、コピーしたCandidate195 templateのprompt identity不一致を検出してcapsule生成前に停止した。slot発行、adapter起動およびrunは0件だった。9 templateのprompt名、bundle hash、bundle pathだけをCandidate196へ機械置換し、再実行で45 capsuleを生成した。fixture、TaskSpec、oracleおよびcomparison conditionは変更していない。

## 発行境界

comparison receiptは`status=ready`、authorized slots 45、issued slots 0、M=24を固定した。preparation rootに`parallel-run`は存在しない。`ready`は互換条件と発行集合が揃ったことだけを意味し、品質、機構、採用、releaseまたはprojectionを意味しない。

`execution_preparation_passed / reference_candidate195_45_bound / candidate196_existing_0 / candidate196_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate196_not_evaluated`
