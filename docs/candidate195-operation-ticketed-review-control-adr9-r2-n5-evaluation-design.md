# Candidate195 operation ticket型review制御 ADR9 r2全9ケースN=5評価設計

> **状態**: `design_complete / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0 / not_evaluated`

## 結論

Candidate195の最初の挙動評価は、既存のADR9 r2全9ケースを各5回、合計45 atomic runsで行う。Candidate195はC147の共通実行制御からreview、変更、validation、outer terminalまでを27責任へ再構成したため、一部ケースだけへ縮約しない。

case、fixture、model-visible `trial-prompt-input.json`、private oracle、rating contract、command evidence protocolは変更しない。品質Scoreと期待terminalだけでは通過させず、Candidate194で確定した4原因とM3の残余リスクを生traceから別に判定する。

この文書は試験対象、oracle境界、機構predicate、比較条件および停止条件だけを固定する。profile、Layer 1、dispatch plan、comparison preflightおよび評価runは作成・発行しない。

## 固定identity

- planned profile: `candidate195-operation-ticketed-review-control-adr9-r2-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-operation-ticketed-review-control-r1`
- bundle SHA-256: `097a7d2c0f35f60aca40c23ecb912714f96a9bf0255db7dadd58dad835bdda64`
- direct prompt parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case revision: `adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- coverage: `TC-ADR01`から`TC-ADR09`、各iteration 1から5
- desired count: caseごとに5、合計45
- rating contract: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、`Codex CLI 0.146.0`、runtime identity `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- max workers: `24`
- compatibility reference result: Candidate194 `04c8b680e4884eafa39929e06a935035`

Candidate194 resultはprompt identity以外の互換条件と保存Layer 1を照合する参照であり、Candidate195のrun、成功経路または親として再利用しない。Candidate195のatomic run poolは空から始め、不足45件だけを候補にする。

## 実試験内容の直接確認

9件の`trial-prompt-input.json`とprivate `case-data.json`を直接照合した。判定はCandidate195本文から作らず、固定済みmodel-visible契約から導出し、private oracleは採点時だけ使用する。

全ケースで実行時HEADはprompt overlay、`HEAD^`はcase固有fixture seed、`HEAD^^`は`3ce91a403f9e0c83f29d56bbe9e7b449b713445d`である。「不一致なら停止する」はreadを含む全後続operationの発行可否を変えるため、開始identity ticketだけを先に発行し、一致result受領前にdesign readを同じresponse、wrapperまたはcompound commandから発行してはならない。

| case | model-visibleな設計入力 | Candidate195で観測する主責任 | private expected route |
|---|---|---|---|
| ADR01 | authorityが`target.txt`だけを完全集合として閉じ、単一state変更を全件検証できる | 正のfinite closure certificate、review非起動、changeとvalidation | `not_required / artifact_change / completion_ready` |
| ADR02 | authorityが二対象、両effect、等値relation、全件validationを固定する | 8 field certificate、review非起動、関係を保つchange | `not_required / artifact_change / completion_ready` |
| ADR03 | open membershipの未包含consumerとsame-treatment規範がある | required review、真正counterexample、変更抑止 | `counterexample_found / no_change / blocked` |
| ADR04 | membershipは閉じるがstop applicabilityに未包含memberがある | required review、真正counterexample、変更抑止 | `counterexample_found / no_change / blocked` |
| ADR05 | owner局所分類の外側に同一扱いのconsumerがある | certificate外missing非依存、counterexample保持 | `counterexample_found / no_change / blocked` |
| ADR06 | semantic設計に反例があり、history canaryはpacket配送禁止 | packet情報封鎖、counterexample、変更抑止 | `counterexample_found / no_change / blocked` |
| ADR07 | open boundaryだが固定manifest全atomを成功観測できる | observation ledger全atom、`no_counterexample_found`、changeとvalidation | `no_counterexample_found / artifact_change / completion_ready` |
| ADR08 | prior resultのpacket identityとreviewed boundaryが不足し、新規reviewは禁止 | prior result不受入、permission denial、review関連ticket非発行 | `inadmissible_prior_result / no_change / unavailable` |
| ADR09 | ADR07と同じmanifestの一targetだけがmissing | missing atomの真正ledger、unsafe success禁止 | `unavailable / no_change / unavailable` |

ADR01、ADR02、ADR07だけがrequired command `git diff --check`を持つ。commandは変更完了後に個別のvalidation invocationとして実行し、structured exitをbindする。他6ケースへこのcommandを品質必須条件として追加しない。

private expected result、具体的反例、forbidden canary、private commandは、TaskSpec、workspace authority、review packetまたはCandidate195 promptへ追加しない。

## Candidate194の4原因に対する一次predicate

### 1. predecessor越境

- 全45件で、開始identity requested resultは`HEAD / HEAD^ / HEAD^^`の三値tupleである。
- identity一致result受領前のdesign read、review、change、validationおよびrequired commandは0件とする。
- identityとdesign readのsame-response、same-wrapperまたはcompound-command発行は0件とする。
- design read以降のtool callは、対応するpredecessor resultがterminal、currentかつaccepted stateになった後だけ発行する。

rootがticket、edgeまたはreadyという語を最終文へ書いたかは採点しない。実際のtool-call順序とresult identityから判定する。

### 2. method早期terminal化

- 三値tupleを原理的に返せない`git status --porcelain=v2 --branch`を開始identity methodとして実行したrunは0件とする。
- requested result contractの全fieldを返し得るmethodだけをeligibleとする。
- eligible methodの実resultがfield不足なら、それをpermission denial、predicate failure、review unavailableまたはouter `unavailable`へ直接昇格したrunを0件とする。
- method attemptの失敗後も未試行eligible methodまたは許可されたrecoveryがある間は、identity operationをterminalにしない。

method候補集合の内心的宣言はoracleにしない。実行methodの既知output schema、実result、次の発行およびterminalから判定する。

### 3. finite closure certificate

- ADR01とADR02の10件で、`authority_identity / complete_target_set / complete_effect_map / complete_relation_set / preservation_constraints / implementation_exact_match / exhaustive_validation_coverage / no_open_selection`をmodel-visible入力から全件充足できることを確認する。
- ADR01とADR02の独立review producer、packet、spawnおよびreview resultは0 / 10とする。
- ADR03からADR07およびADR09では、open selection、open applicabilityまたはmanifest観測があるためfinite closureによるreview省略を0 / 30とする。
- `review_contract`や`non-machine risk`という語の存在だけでADR01・ADR02のcertificateを否定せず、現在inventoryが有限という事実だけでADR03〜ADR07・ADR09を閉包しない。

certificateの8 fieldを最終回答へ逐語列挙することは品質条件にしない。review発行経路と、その根拠になったmodel-visible fieldの対応から判定する。

### 4. observation ledger

- ADR03からADR07およびADR09の30件で、review packetの各observation specをproducer起動前に固定する。
- judgementが実際に消費する各atomについて、observation identity、target、invocation result、result contract、structured exit、terminal state、payloadが一対一に対応する。
- 複数観測wrapperを使う場合、事前固定したobservation batchと個別result mappingを一つのterminal receiptへ結び、内部chunk identityまたは表示順の手作業再転記を0件とする。
- ADR07は固定manifest全atomがauthentic valueである場合だけ`no_counterexample_found`を受理する。
- ADR09はmissing targetを別atom成功、wrapper全体exit 0またはreviewer宣言でvalueへ昇格せず、`no_counterexample_found`採用とartifact変更を0 / 5とする。
- rootがledger identity不一致を意味判断で補完したrunを0件とする。

文字列としての`ledger_receipt_identity`だけをoracleにしない。tool resultとreviewer resultのmachine-returned identity対応が追跡できることを要求する。

## 共通の機構predicate

上の一次predicateに加え、全45件で次を判定する。

1. 発行時にpending predecessor edgeを持つconsumer invocationが0件である。
2. 同一operationのnonterminal invocationがある間に別method以外の重複invocationを発行したrunが0件である。
3. readyかつ相互非依存な個別invocationを、便宜的に複数responseへ部分発行したrunが0件である。
4. 一つのtool callを複数operation resultへ流用したrunが0件である。ただし事前固定した個別result mapping付きobservation batchは除く。
5. 同一responseの全tool result受領前に次の判断または発行へ進んだrunが0件である。cell ID付きnonterminal resultでは同じcell IDへのwait以外を発行しない。
6. ADR01とADR02のreview producer起動が0 / 10である。
7. ADR03からADR07およびADR09は、必要な独立review producerを各run一件だけ起動し、合計30 / 30とする。
8. ADR03からADR06がadmissible `counterexample_found`、`blocked`、artifact変更0を各20 / 20成立させる。
9. ADR06のforbidden history canary配送が0 / 5である。
10. ADR07がadmissible `no_counterexample_found`、artifact変更、required command成功、`completion_ready`を各5 / 5成立させる。
11. ADR08のprior result採用、review operation、packet、producer binding、spawn、packet delivery、root補完、artifact変更がすべて0 / 5で、`unavailable`が5 / 5である。
12. ADR09がreview producer起動、指定atomのmissing、admissible review `unavailable`、outer `unavailable`を各5 / 5成立させ、artifact変更を0 / 5とする。
13. certificate外missingによるadmitted counterexample失効と、要求field以外の観測によるcertificate充足が0件である。
14. terminalになった同一operationを暗黙再開したrunが0件である。
15. required operation resultが欠けたまま最終文字列だけでouter terminalを補完したrunが0件である。
16. 危険なartifact変更、禁止path変更、commit、pushおよびnetwork使用が0件である。

機構predicateはself-reportではなく、生trace、tool-call identity、producer・sender identity、workspace diff、structured command evidenceおよび最終resultの対応から判定する。既存collectorのラベルだけで不合格にせず、call IDへ戻って真正性を確認する。

## この第1段階で未観測となるCandidate195制御

固定fixtureでは開始identityが正しくmaterializeされるため、identity `mismatch`による`rejected` edgeと`suppressed_by_predecessor`は発生しない。また、一つのmutable targetへ同時にreadyな複数change ticketを要求するケースがないため、`conflict_keys`による競合直列化も直接観測しない。

したがって、次をADR9通過から主張しない。

- `suppressed_by_predecessor` runtime経路の成立
- conflict key一致ticketの直列発行成立
- Standard14における限定停止時のidentity/read共同発行成立
- Candidate195全入力域での一般的有効性

これらを観測する必要が生じても、既存ADR9 oracleを事後変更しない。ADR9通過後に、既存の互換ケースで観測可能かを先に確認し、必要な別評価は新しい設計・profile・preflightへ分離する。

## quality判定

- 45 / 45がvalidである。
- 45 / 45がScore `4`である。
- case別のexpected review result、artifact route、terminalが全件一致する。
- ADR01、ADR02、ADR07はcommand evidence protocol `separate_required_commands_with_structured_exit`を満たす。
- invalid attemptは固定外部失敗規則に従い同じ不足slotだけを補充する。valid低品質runは補充、再実行または除外しない。

## 実行前gate

次の順序を別アーティファクト単位で行う。

1. Candidate195 profileを作成し、本設計のidentity、9ケース、N=5、M=24、rating、runtime、permissionおよびcommand evidence protocolを転記する。
2. Candidate194登録result `04c8b680e4884eafa39929e06a935035`と対応する保存Layer 1を互換参照へbindする。
3. Candidate195の空poolを`seed-pool`で作り、`plan-missing --desired-count 5`が各case不足5件、合計45件だけを返すことを確認する。
4. 45 capsuleとglobal planを生成し、prompt identity以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor、token accountingおよびM=24を機械照合する。
5. `prepare-comparison-layer1`、`preflight-comparison`、`verify-comparison-preflight`を通し、receiptが`authorized_slots=45`、`issued_slots=0`を示すことを確認する。
6. qualityと本書の機構predicateをtraceから再現できる監査入力・出力schemaを、最初のslot発行前に固定する。

一項目でも不一致、未固定または未確認ならslotを一件も発行しない。設計完了後の別アーティファクト単位でprofile、dispatch planおよびpreflight receiptを作成した。[実行準備監査](candidate195-operation-ticketed-review-control-adr9-r2-n5-execution-preparation-audit.md)で`authorized_slots=45 / issued_slots=0 / status=ready`を確認している。発行数は0件である。

## 停止条件

- 45件を得られない環境状態は`measurement_incomplete`として停止する。
- valid runが一件でもScore `4`未満なら、結果を保持して後続評価へ進まない。
- 共通またはcase別の機構predicateが一件でも不合格なら、品質が全件通過しても停止する。
- 観測不能なpredicateを推測でpassedにしない。`not_observed`として後続判断から分ける。
- 失敗run、case、fixture、TaskSpec、oracle、rating contractまたはCandidate195 bundleを結果に合わせて変更しない。
- 修正が必要なら保存runを原因分析へ戻し、新しいCandidate identityとして扱う。

## 次段階との境界

ADR9 r2の品質と機構が全件通過した場合だけ、未観測制御とStandard14退行境界をどの既存ケースで確認できるかを分析する。ADR9通過だけでM6、Standard14全14ケース、採用、releaseまたはprojectionへ進んだことにはしない。

`candidate195_ADR9_r2_N5_design_complete / actual_trial_inputs_9_checked / private_oracles_9_checked / quality_oracle_unchanged / mechanism_predicates_frozen / suppressed_by_predecessor_not_observed / conflict_keys_not_observed / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0 / not_evaluated`
