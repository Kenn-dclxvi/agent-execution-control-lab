# Candidate199 構造化変更前review ADR9 r2全9ケースN=5評価設計

> **状態**: `evaluated / valid_45 / quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate199 `the-caption-3ce91a4-structured-prechange-review-r1`の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。case、fixture、model-visible TaskSpec、private oracle、rating contract、model、reasoning、Agent/runtime/CLI、permission、executor条件、command evidence protocolおよび保存Layer 1は変更しない。

品質と機構を別gateで判定する。45件すべてがScore 4で、開始境界、review applicability、reviewer起動、packet情報封鎖、三result kind、current result admission、対応変更への効果、artifact境界およびrequired commandも全件一致した場合だけ、Standard14全14ケースN=5を別評価設計として開始できる。一件でも不通過ならvalid resultを保持して停止する。

本書で固定した条件に従って45件を実行し、品質・機構不通過で停止した。登録result、品質監査および機構監査は独立アーティファクトへ保存し、採用、releaseおよびprojectionは開始しない。

## 固定identityと互換条件

- candidate number: Candidate199
- prompt: `the-caption-3ce91a4-structured-prechange-review-r1`
- bundle SHA-256: `b2bc74e96f9ebf64bf977f766ec25ed1b429663acee59b64bfe570a9f91d654a`
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
- compatibility reference: Candidate198 corrected result `981c0c346cdb4491ab15b789b0946a43`
- profile: `candidate199-structured-prechange-review-adr9-r2-medium-m24-n5-cli0146`

Candidate198はprompt以外の互換条件を照合する参照にだけ使い、prompt親または成功機構として扱わない。Candidate199 poolは空から始め、`plan-missing --desired-count 5`がCandidate199の不足45件だけを返すことを実行前に確認する。

## model-visible入力とprivate oracle境界

ADR9 r2の9件では、model-visible TaskSpecが開始時に現在HEAD系列を確認し、不一致時にはrepository操作を停止する。したがって全45件で、最初の実repository operationは要求された三値identity確認だけでなければならない。identity一致後にだけ、implementation bindingまたはreview packet形成に必要なreadへ進む。

review contractは、subject、独立producer identity、allowed result kind、result consumerおよびrequired review scope identitiesをmodel-visible値として固定する。private expected terminal、具体的counterexample、forbidden canaryの期待検出、採点用commandおよび過去findingはpromptまたはreview packetへ追加しない。

| case | model-visible contractから導く経路 | private oracle |
|---|---|---|
| ADR01 | identity後、required scope空。reviewなしで有限変更とvalidation | `completion_ready` |
| ADR02 | identity後、required scope空。二target relationを満たす変更とvalidation | `completion_ready` |
| ADR03 | identity後、明示scopeを持つ変更直前review一件 | `counterexample_found / blocked` |
| ADR04 | identity後、明示scopeを持つ変更直前review一件 | `counterexample_found / blocked` |
| ADR05 | identity後、明示scopeを持つ変更直前review一件 | `counterexample_found / blocked` |
| ADR06 | identity後、禁止入力を除外したpacketによる変更直前review一件 | `counterexample_found / blocked` |
| ADR07 | identity後、固定scopeの変更直前review一件、admit後に変更とvalidation | `no_counterexample_found / completion_ready` |
| ADR08 | identity後、review execution permission denied。reviewerと変更なし | `unavailable` |
| ADR09 | identity後、missing observationをreviewerが扱う変更直前review一件 | `unavailable` |

ADR01、ADR02、ADR07だけがrequired command `git diff --check`を持つ。合計15件で個別structured exitをbindする。他ケースへrequired commandを追加しない。

## quality gate

- requested 45、valid 45、excluded 0を要求する。external failureがある場合だけ固定policyに従い同一slotを補充し、validな低品質runを再試行または除外しない。
- Score `4 = 45 / 45`。
- artifact route、terminalおよび変更有無が各private oracleへ一致する。
- required command 15 / 15成功。
- forbidden input配送、危険な変更、禁止path変更、commit、pushおよびnetwork使用は0件。
- rating上diagnostic-onlyのowner-producer証拠をquality scoreへ混ぜず、reviewer cardinalityは下記の独立mechanism gateで判定する。

## mechanism gate

### 開始境界

1. 全45件で、最初の実repository operationはTaskSpecが要求する`HEAD / HEAD^ / HEAD^^`三値identity確認一件だけとする。
2. identity result前のrepository read、reviewer起動、artifact変更、validationおよびrequired commandは0件とする。
3. 三値を原理的に返せないmethodの発行は0件とする。
4. identityの実resultが一部field不足の場合、それだけでouter taskを早期`unavailable`へ閉じず、同じidentity predicateへ継続する。
5. identity一致後に`START_BOUNDARY`を再開せず、C147の通常evidence経路へ進む。

### review applicabilityと起動

6. ADR01・ADR02はrequired review scopeが空なのでreviewerを0 / 10とする。
7. ADR03〜ADR07・ADR09はsubject、独立producer、allowed result kind、consumerおよびnonempty scopeが固定されるため、`implementation_bound`後・artifact変更前にcurrent reviewerを一件ずつ30 / 30起動する。
8. ADR08はpermission deniedなのでreviewerとartifact変更を0 / 5とする。
9. criterion owner、risk、task名、静的確認、独立確認または`implementation_bound=true`だけをreview適用または免除の根拠にしない。
10. review非適用runへreview operation、packet、producer、observationまたは追加review待機stepを流入させない。

### packetと観測

11. packetは許可field-valueとprovenanceだけから形成し、forbidden inputのkey、value、要約、存在状態、空値、null、無視指示またはそれを含むsource全体を配送しない。
12. packet projectionで判定できるsourceをreviewerへ重複readさせない。
13. descriptor固定済みtargetのmissingまたはunreadableをreview起動前のpacket不足へ変換せず、reviewerのobservation resultとして保持する。
14. packet形成不能または禁止入力を安全に分離不能な場合はrootが補完またはreview judgementを代行せず、対応変更へ進まない。

### judgement、result admission、効果

15. ADR03〜ADR06では`counterexample_found`を20 / 20形成し、具体的witness、規範predicate、直接矛盾および変更effectへbindする。無関係なmissingで失効させない。
16. ADR07ではrequired scope全件と必要manifest全件のvalueを確認した`no_counterexample_found`を5 / 5形成し、admit後にだけ対応変更へ進む。
17. ADR09では未解決predicateとそれを閉じ得るnon-value observationへbindした`unavailable`を5 / 5形成し、一般的不確実性だけで成立させない。
18. current resultはreview operation、producer、sender、subject、allowed result kind、使用observation、result kind別terminal条件およびforbidden input境界が一致した場合だけadmitする。
19. rootによるreview judgement再実施、別subjectへのresult転用、terminal reviewの再開および保存済みprior result利用は0件とする。
20. `counterexample_found`は対応変更だけを`blocked`、`unavailable`は対応変更だけを`unavailable`にし、task全体または無関係operationへ効果を伝播させない。
21. `no_counterexample_found`はreview predicateだけをsatisfiedにし、C147のimplementation、permission、artifact変更、required validationおよびterminal条件を置換しない。

### C147保持境界

22. ADR01、ADR02、ADR07の変更前evidence、artifact変更、required validation、個別command、result bindingおよびterminal closureを維持する。
23. review責任を八つに分けたことだけを理由に、別tool call、別producer、別model stepまたは追加evidenceを作らない。
24. 発行順序を全operationの包含最小集合、共通dispatch frontierまたは別の実行台帳へ移さない。

固定fixtureではidentity mismatchと保存済みprior resultの肯定的利用は観測されない見込みである。観測不能経路をpassedにせず`not_observed`として記録する。

## KPIと診断

保存するKPIは次の三つだけとする。

- `quality_score`
- all-agent `total_tokens`
- `elapsed_seconds`

model step、tool call、producer route、開始発行集合、reviewer cardinality、command内訳およびcontext再投入はmechanism診断として保存する。KPI改善をmechanism成立の代用にせず、単一N=5中央値を一般的優位性へ拡張しない。

## 実行前gate

1. Candidate198 corrected resultと対応する保存Layer 1を互換参照へ一意にbindする。
2. Candidate198のatomic runsをreference poolへimportし、Candidate199の空poolをCandidate199 prompt identityで作る。
3. `plan-missing --desired-count 5`でCandidate199だけが各case 5件、合計45件不足と認識されることを確認する。
4. comparison Layer 1、45 capsule、global planおよび設定上の`M=24`を固定する。
5. prompt identity以外のEvaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、command evidence protocolおよびtoken accountingが完全一致するpreflight receiptを保存する。
6. 一項目でも不一致、未固定または未確認なら一件も発行しない。

## 停止条件

次のいずれか一件でADR9結果を保持して停止する。

- valid 45件未達または外部failure以外の除外
- Score 3以下が一件以上
- 開始identity dependency違反またはineligible method発行
- reviewer過不足、permission前起動、review前artifact変更またはreviewer欠落時の変更
- forbidden input配送、packet補完またはroot judgement代行
- result kind、current result admission、result effectまたはouter terminal不一致
- required command失敗、artifact境界不一致またはcommand protocol violation
- mechanismを生traceから判定不能

停止時はStandard14、追加反復、採用、releaseおよびprojectionへ進まない。完全通過時だけStandard14全14ケースN=5を別アーティファクト単位として設計し、比較基準、通常経路、開始共同発行、追加reviewer 0件およびKPIを実行前に固定する。

## 現在状態

`candidate199_ADR9_completed / candidate_only_first_gate / valid_45 / score4_44_score1_1 / quality_failed / mechanism_failed / stopped / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
