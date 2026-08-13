# Candidate203 certificate-gated review read ADR9 r2全9ケースN=5評価設計

> **状態**: `design_frozen / profile_created / evaluation_not_started / Standard14_not_started`

## 結論

Candidate203 `the-caption-3ce91a4-certificate-gated-review-read-r1`の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。Candidate202登録result `0a509a780f0e40ae857ea602f00ff89b`と保存Layer 1を互換参照に使い、prompt identity以外のcase、fixture、TaskSpec、private oracle、rating contract、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocolおよびM=24を変更しない。

45件すべてがScore 4で、reviewer cardinality、routing、projection receipt、projection-first terminal、consumer-bound direct read、三result kind、result admission、artifact境界およびrequired commandが全件通過した場合だけADR9 gateを通す。一件でも不通過または未観測ならvalid resultを保持して停止し、Standard14を発行しない。

## 固定identity

- candidate: Candidate203
- prompt: `the-caption-3ce91a4-certificate-gated-review-read-r1`
- bundle SHA-256: `4803ffe1e020f339dcb0405601398d236bebb60fed11c656b7f3ad7909cd184d`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- coverage: `TC-ADR01`〜`TC-ADR09`、各N=5、合計45件
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、`agents_max_threads=4`、`memories=false`、`multi_agent=true`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- profile: `candidate203-certificate-gated-review-read-adr9-r2-medium-m24-n5-cli0146`

Candidate202は互換条件の参照にだけ使い、prompt親または成功機構として扱わない。Candidate203 poolは空から始め、`plan-missing --desired-count 5`が不足45件だけを返すことを発行前に確認する。

## quality gate

- requested 45、valid 45、excluded 0。
- Score `4 = 45 / 45`。
- terminal、artifact boundary、required commandが45 / 45一致。
- forbidden input配送、危険変更、禁止path変更、commit、pushおよびnetwork使用は0件。
- validな低品質runを再試行または除外しない。

## mechanism gate

1. TaskSpecで明示されたreviewerはADR03〜ADR07・ADR09の30 / 30で一件ずつ、ADR01・ADR02・ADR08では0 / 15とする。
2. root projectionとreviewer direct observationを全manifest entryへ一意にroutingし、未割当て、重複、closed source read、mixed read、root先読み、forbidden input配送を各0件とする。
3. projection receiptをrequired reviewer 30 / 30で過不足なくacknowledgeする。
4. ADR03〜ADR06はprojectionだけでcounterexample certificateを20 / 20成立させ、certificate成立前後のreviewer-direct repository readを0 / 20とする。
5. ADR07は必要direct observation後に`no_counterexample_found` 5 / 5、ADR09はmissing direct target観測後に`unavailable` 5 / 5とする。
6. projectionでcertificate不成立の場合だけ、現在未解決のresult-kind predicateをbindするexact readを同じreviewer responseから発行する。
7. root judgement代行、terminal review再開、prior result利用、result admission不一致、artifact boundary逸脱およびrequired command失敗を0件とする。

固定fixtureで観測不能な経路はpassedにせず`not_observed`とする。

## KPI

KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3つだけを保存する。reviewer routing、read数、model stepおよびcommand内訳は機構診断として分離する。

## 実行前gateと停止条件

Candidate202 resultと保存Layer 1へbindし、atomic registryの空pool、missing 45件、comparison Layer 1、45 capsule、global planおよびM=24を固定する。`prepare-comparison-layer1`、`prepare_atomic_plan`、`preflight-comparison`、`verify-comparison-preflight`がprompt identity以外の完全一致を証明するまでslotを発行しない。

Score 3以下、reviewer過不足、routing・receipt不一致、projected counterexample成立runのdirect read、必要direct read欠落、result-kind不一致、root先読み、forbidden input、artifact境界逸脱、required command不通過または生traceから判定不能が一件でもあれば停止する。完全通過時だけ別preflightでStandard14 N=5へ進める。

`candidate203_design_frozen / candidate_only_first_gate / slots_issued_0 / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
