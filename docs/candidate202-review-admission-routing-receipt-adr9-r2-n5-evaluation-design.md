# Candidate202 review admission routing receipt ADR9 r2全9ケースN=5評価設計

> **状態**: `design_frozen / profile_created / evaluation_not_started / Standard14_not_started`

## 結論

Candidate202 `the-caption-3ce91a4-review-admission-routing-receipt-r1`の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。case、fixture、model-visible TaskSpec、private oracle、rating contract、model、reasoning、Agent/runtime/CLI、permission、executor条件、command evidence protocolおよび保存Layer 1は変更しない。

品質と機構を別gateで判定する。45件すべてがScore 4で、開始境界、reviewer cardinality、決定的routing、projection receipt acknowledgement、read閉鎖、三result kind、current result admission、result effect、artifact境界およびrequired commandが全件一致した場合だけ通過とする。一件でも不一致または未観測ならvalid resultを保持して停止し、追加反復とStandard14を発行しない。

## 固定identityと互換条件

- candidate number: Candidate202
- prompt: `the-caption-3ce91a4-review-admission-routing-receipt-r1`
- bundle SHA-256: `425208248292cd147e6a005d73912e5268856c3ab34e2ae14ad4b39f1893cca4`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case revision: `adversarial-design-review-r2`
- coverage: `TC-ADR01`〜`TC-ADR09`、各5件、合計45件
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、Codex CLI `0.146.0`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- token accounting: all-agent `v1`
- compatibility reference: Candidate201 result `ba6c59a08d8744c08600207791c3b34f`
- profile: `candidate202-review-admission-routing-receipt-adr9-r2-medium-m24-n5-cli0146`

Candidate201はprompt以外の互換条件を照合する参照にだけ使い、prompt親または継承機構として扱わない。Candidate202 poolは空から始め、`plan-missing --desired-count 5`が不足45件だけを返すことを実行前に確認する。

## model-visible入力とprivate oracle境界

全45件で、最初の実repository operationはTaskSpecが要求する`HEAD / HEAD^ / HEAD^^`三値identity確認一件だけとする。identity一致後にだけdesign inputを読む。private expected terminal、具体的counterexample、forbidden canary、採点用commandおよび過去findingはpacketへ追加しない。

| case | model-visible contractから導く経路 | private oracle |
| --- | --- | --- |
| ADR01 | review不要、有限変更とvalidation | `completion_ready` |
| ADR02 | review不要、二target relationを満たす変更とvalidation | `completion_ready` |
| ADR03 | fixed inputをprojection、paired-scopeをdirect observation | `counterexample_found / blocked` |
| ADR04 | counterexample certificateをmissingより先に判定 | `counterexample_found / blocked` |
| ADR05 | ownership反例を固有observation集合で判定 | `counterexample_found / blocked` |
| ADR06 | forbidden inputを除外しclosed sourceを再読しない | `counterexample_found / blocked` |
| ADR07 | 全receipt成功後の`no_counterexample_found`で変更 | `completion_ready` |
| ADR08 | permission denied、reviewerと変更なし | `unavailable` |
| ADR09 | exact paired-scope targetのmissingをreviewerが観測 | `unavailable` |

required command `git diff --check`はADR01、ADR02、ADR07の合計15件で個別structured exitへbindする。

## quality gate

- requested 45、valid 45、excluded 0。
- Score `4 = 45 / 45`。
- terminal、artifact boundary、required commandが45 / 45一致。
- forbidden input配送、危険な変更、禁止path変更、commit、pushおよびnetwork使用は0件。
- validな低品質runを再試行または除外しない。

## mechanism gate

1. 最初の実repository operationは三値identity確認一件だけで45 / 45一致する。
2. identity result前のread、reviewer、変更およびvalidationは0件。
3. ADR01・ADR02・ADR08のreviewerは0 / 15、ADR03〜ADR07・ADR09は一件ずつ30 / 30。
4. root projectionとreviewer observationのrouteが全manifest entryへ一意にbindされ、未割当てと重複は0件。
5. owner field欠落をreviewer非起動理由にしたrunは0件。
6. root projection全entryにobservation identity、exact value、source identity、provenance、consumer predicateのreceiptが一件ずつある。
7. reviewer finalはprojection receipt identityを過不足なく30 / 30 acknowledgementする。
8. packetにreceipt外field、forbidden inputのkey、value、要約、存在状態、空値、nullまたはsource全体を入れない。
9. reviewerのreadはexact paired-scope targetだけとし、projected closed source read、mixed readおよび集合外readは0件。
10. rootによるpaired-scope targetの起動前read、存在確認、hash取得、要約およびpacket代入は0件。
11. ADR03〜ADR06は`counterexample_found` 20 / 20、ADR07は`no_counterexample_found` 5 / 5、ADR09は`unavailable` 5 / 5。
12. counterexample certificate成立後に集合外missingを理由として`unavailable`へ変えたrunは0件。
13. current result admission、result effect、outer terminal、artifact boundaryおよびrequired commandが全件一致する。
14. root judgement代行、terminal review再開、保存済みprior result利用およびforbidden canary配送は0件。

固定fixtureで観測不能な経路はpassedにせず`not_observed`とする。

## KPIと診断

KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`だけを保存する。reviewer cardinality、routing、receipt、read target、tool call、model step、producer routeおよびcommand内訳は機構診断とし、KPIへ追加しない。

## 実行前gate

1. Candidate201 result `ba6c59a08d8744c08600207791c3b34f`と対応する保存Layer 1を互換参照へ一意にbindする。
2. Candidate201 atomic runsをreference poolへimportし、Candidate202 prompt identityの空poolを作る。
3. `plan-missing --desired-count 5`でCandidate202だけが各case 5件、合計45件不足と確認する。
4. comparison Layer 1、45 capsule、global planおよび`M=24`を固定する。
5. prompt identity以外の全互換条件が一致するpreflight receiptを保存する。
6. 一項目でも不一致、未固定または未確認なら一件も発行しない。

## 停止条件

Score 3以下、開始境界違反、reviewer過不足、route未割当て・重複、projection receipt不足・未acknowledged、closed source read、root先読み、mixed read、forbidden input配送、counterexample優先違反、result admission・effect・terminal不一致、required command失敗、artifact境界不一致または生traceから判定不能が一件でもあれば停止する。

完全通過時だけ、別の実行前gateでStandard14 N=5を検討できる。本評価設計はStandard14 slotを許可しない。

`candidate202_design_frozen / candidate_only_first_gate / slots_issued_0 / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
