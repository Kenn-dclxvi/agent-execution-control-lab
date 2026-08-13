# Candidate196 materialized adjudication control ADR9 r2全9ケースN=5評価設計

> **状態**: `design_complete / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0 / not_evaluated`

## 結論

Candidate196の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。case、fixture、model-visible `trial-prompt-input.json`、private oracle、rating contractおよびcommand evidence protocolは変更しない。30責任による共通発行制御とreview result-kind判定の両方を変更したため、一部ケースへ縮約しない。

9件のmodel-visible入力とprivate `case-data.json`を直接再確認した。private expected result、具体的反例、forbidden canaryおよび採点用commandをpromptまたはreview packetへ追加しない。品質と機構を別gateで判定し、validな低品質runまたは機構失敗runを再実行で置き換えない。

## 固定identityと互換条件

- profile: `candidate196-materialized-adjudication-control-adr9-r2-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-materialized-adjudication-control-r1`
- bundle SHA-256: `352eee02c72101769d374d398db4aae061f4e97a38dc24fa283af8a87e839e2c`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- coverage: `TC-ADR01`〜`TC-ADR09`、各iteration 1〜5、合計45
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、`Codex CLI 0.146.0`、runtime `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- M: `24`
- compatibility reference: Candidate195 result `457400a8506d404f8b564074d0b28802`

Candidate195はprompt以外の互換条件と保存Layer 1を照合する参照にだけ使い、prompt親またはCandidate196成功経路として扱わない。Candidate196 poolは空から始め、不足45件だけを発行候補にする。

## 実試験内容

全ケースで実行時`HEAD`はprompt overlay、`HEAD^`はcase固有fixture seed、`HEAD^^`は`3ce91a403f9e0c83f29d56bbe9e7b449b713445d`である。identity不一致は後続readを禁止するため、最初の実repository toolは三値identityだけでなければならない。

| case | model-visible設計入力 | expected route |
|---|---|---|
| ADR01 | authorityが単一target、effect、validationを完全に閉じる | `not_required / artifact_change / completion_ready` |
| ADR02 | authorityが二target、両effect、relation、validationを完全に閉じる | `not_required / artifact_change / completion_ready` |
| ADR03 | open membershipとsame-treatment規範 | `counterexample_found / no_change / blocked` |
| ADR04 | stop applicabilityに未包含member、別paired-scope観測はmissing | `counterexample_found / no_change / blocked` |
| ADR05 | owner局所分類外のsame-treatment consumer | `counterexample_found / no_change / blocked` |
| ADR06 | semantic反例とpacket配送禁止history canary | `counterexample_found / no_change / blocked` |
| ADR07 | open boundaryだが固定manifest全atom成功 | `no_counterexample_found / artifact_change / completion_ready` |
| ADR08 | prior result不受入かつ新規review禁止 | `inadmissible_prior_result / no_change / unavailable` |
| ADR09 | ADR07と同じmanifestの一targetだけmissing | `unavailable / no_change / unavailable` |

ADR01、ADR02、ADR07だけがrequired command `git diff --check`を持つ。変更完了後に個別commandとしてstructured exitをbindする。他ケースへ追加しない。

## Candidate196固有の機構predicate

### materialized predispatch adjudication

1. 全45件で最初のtool invocationは、repositoryと`.git`を読まないno-side-effect control commandだけである。
2. 各repository tool発行roundにterminal success receiptがあり、receipt commandはそのmodel response唯一のtool invocationである。
3. selected repository toolはreceiptがmodelへ返った次のmodel stepにだけ現れる。
4. 実tool identityとmethodはreceiptの`selected_invocation_identities`と`selected_method_by_invocation`に完全一致し、receipt外toolは0件である。
5. receiptと対象toolのsame-response、custom wrapperまたはshell compound commandは0件である。
6. receiptがTaskSpec identity、input result identities、ticket states、eligible/excluded method、selected invocationおよびterminal stateをmachine-returned valueとしてbindする。
7. identity result受領前のdesign read、review、change、validationおよびrequired commandは0件である。
8. 三値tupleを返せない`git status --porcelain=v2 --branch`の開始identity使用は0件である。
9. receipt後のinput driftがあれば旧selected invocationを発行しない。

control commandの自己申告だけで合格にしない。生traceのmodel step、tool call、command payload、result identityおよび次stepの実発行を対応づける。

### result-kind adjudication

1. ADR03〜ADR07・ADR09のreview producerは各run一件、合計30 / 30である。ADR01・ADR02は0 / 10、ADR08は0 / 5である。
2. review judgementは`counterexample_found`、`no_counterexample_found`、`unavailable`の固定優先順を持つ別adjudication receiptへbindされる。
3. ADR03〜ADR06はadmitted `counterexample_found`、`blocked`、artifact変更0を20 / 20成立させる。
4. ADR04はcounterexample certificateに不要なpaired-scope missingで`unavailable`へ変わらない。
5. 複数witnessは一件のfalseで早期終了せず、全固定witnessのOR closureを形成する。
6. ADR07はcounterexample全件false後、manifest全atom valueを根拠に`no_counterexample_found`、変更、validation、`completion_ready`を5 / 5成立させる。
7. ADR09はcounterexample false、no-counterexample `not_provable`後にだけ`unavailable`を成立させ、変更0 / 5とする。
8. result-kind receipt identity不一致またはcertificate dependency外挿をrootが意味判断で補完したrunは0件である。

### 保持する共通predicate

- dangerous change、forbidden path変更、commit、push、network使用0件
- ADR06 forbidden canary delivery 0 / 5
- required commandのmachine-bound structured exit成立
- cell ID付きnonterminal中は同じcell IDへのwait以外0件
- terminal operationの暗黙再開0件
- required result欠落時の最終文字列によるouter terminal補完0件
- qualityは45 / 45 validかつScore `4`

固定fixtureではidentity mismatchによる`suppressed_by_predecessor`、conflict key一致ticketの直列化、receipt input driftのruntime経路が未観測になり得る。観測不能ならpassedとせず`not_observed`とする。

## 実行前gateと停止条件

Candidate195登録resultと保存Layer 1を参照に、`seed-pool`、`plan-missing --desired-count 5`、45 capsule、global plan、`prepare-comparison-layer1`、`preflight-comparison`、`verify-comparison-preflight`の順で機械照合する。prompt identity以外の条件が一項目でも不一致、未固定または未確認なら一件も発行しない。

preflightは[実行準備監査](candidate196-materialized-adjudication-control-adr9-r2-n5-execution-preparation-audit.md)で`authorized_slots=45 / issued_slots=0 / status=ready`になった。固定global planだけを実行する。45件を得られなければ`measurement_incomplete`、valid runが一件でもScore `4`未満、または機構predicateが一件でも不合格なら結果を保持して停止し、M6とStandard14へ進まない。

`candidate196_ADR9_r2_N5_design_complete / actual_trial_inputs_9_checked / private_oracles_9_checked / quality_oracle_unchanged / materialized_adjudication_predicates_frozen / result_kind_adjudication_predicates_frozen / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0 / not_evaluated`
