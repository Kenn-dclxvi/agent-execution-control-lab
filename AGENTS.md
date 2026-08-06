# Repository instructions

このrootには、全pathへ共通して適用する不変条件だけを残す。領域固有の配置、更新、検証、履歴保持規則は、対象領域の局所`AGENTS.md`を正本とする。対象pathに局所`AGENTS.md`がある場合は、その領域固有規則を追加適用する。

## Repository scope

- このリポジトリは、target instanceごとのprompt構築、比較、評価、release準備を扱う。登録instanceは`the-caption`（THE-CAPTION）と`click`（`pallets/click`）である。`the-caption`はrelease準備と本体投影まで進める現行instance、`click`はBundle A baselineを確立した公開targetで、Bundle比較、採用、release、本体反映は未実施である。instanceの登録と境界は`evaluations/targets/README.md`を正本とする。
- instance間でartifactを混ぜない。case、profile、set、rating contract、prompt bundle、resultはinstance固有artifactとして扱い、あるinstanceで成立した結果を他instanceの一般的効果として扱わない。target非依存のkernelとinstance固有artifactの帰属も`evaluations/targets/README.md`を正本とする。
- prompt制御上の問題を解く方法は、このリポジトリ内のprompt、TaskSpec、repository authority、評価artifactの境界へ限定する。repository外のexecutor、Codex CLI、tool adapter、runtime hook、外部wrapper、target runtimeの変更を、prompt Candidateの解決策、次案、backlog、再開条件として提案または実装しない。
- repository外の挙動や過去のexecutor試験は、保存済みresultの原因を分類するread-only診断証拠としてだけ参照できる。問題がrepository外の層でしか強制できない場合は、このリポジトリでは未解決として停止する。外部対応へ作業を広げない。評価基盤自体の保守は、ユーザーが明示的に依頼した別作業に限る。
- target本体のruntime変更は通常作業範囲に含めない。
- target本体への変更、push、PR、merge、runtime有効化は、明示的に依頼された別作業とする。

## 共通のartifact境界

- artifactが存在することと、評価済み、採用済み、release済み、本体反映済みであることを混同しない。
- baseline、candidate、release、evaluation result、approval、projectionを別の状態とgateとして扱う。
- secret、credential、非公開のraw run log、一時worktreeをcommitしない。
- 文書は原則として日本語で記述する。
- schema名、path、status、commandは再現性のため英語表記を許容する。

## Agent execution discipline

このリポジトリで作業するagentは、次の制御をそのまま適用する。本文はCandidate147（`the-caption-3ce91a4-result-effect-scope-r1`）で本体へ採用された制御原文`prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt`からの逐語転記であり、要約、緩和、repository向けの調整を加えていない。転記元のreleaseが変わる場合は、release identityを更新して全文を差し替える。

この適用はrepository保守のagent execution disciplineであり、Candidate147の評価結果を別target instanceへ一般化すること、prompt candidateとして採用すること、releaseまたはtarget本体へprojectionすることを意味しない。

repository固有の不都合が観測されるまで、条項へ差分を加えない。差分が必要になった場合は、根拠となる観測事象と原文からの差分をこの節へ明示する。

- SPEC: 実行前にrequired outcomeをoperation identityへ分け、`predicate / criterion owner / permission / constraint`をTaskSpecへ固定する。`spec_ready := required outcome valueが、明示user inputまたはそのvalueを直接要求する一意なrepository authorityへbind済み`。required outcome valueはTaskSpecが利用者に観測可能な成果として選択を要求する値とする。target artifact / canonical path / module / command / implementation methodは、TaskSpecがそれ自体を成果として要求しない限りimplementation choiceであり、未固定でも`spec_ready`をfalseにしない。current value / option set / complement / test expectation / implementation convenienceはrequired outcome valueをbindしない。`spec_ready=false`の間はproducer binding / predicate実行 / artifact変更 / testを開始せず、未固定のrequired outcome valueだけをclarification resultにする。`result / constraint / terminal`は同一operation identity内だけへbindし、別operation / task全体へ伝播させない。
- PRODUCER: 初回predicate前に各operationへrootまたはworkerのproducer execution identityを一つbindする。同一operationのpredicate実行 / result生成を他producerへ順次・並行に割り当てない。TaskSpecが独立したproducer executionを明示した場合だけ、その指定identityをproducer role identityへbindする。criterion owner語列だけでproducerを選ばない。producer変更は理由を問わず旧bindingを失効し、新identityのTaskSpecで行う。
- TERMINAL: 全predicateにbind済みproducerのterminal resultがある場合だけoperationをterminalにする。invocation / worker / sessionがnonterminal、またはresult欠落ならoperationもnonterminalとし、進行報告 / 集約結果 / final responseで補完しない。
- CONTEXT: worker packetへ`criterion / owner / pass condition / TaskSpec該当範囲 / target identity / scoped diffまたはresult / required evidence / allowed read / forbidden input`を固定する。packetとallowed readで判定可能なら`fork_turns=none`とし、不足時だけ意味保持に必要な最小turn数を継承する。利便性、念のため、無関係なtool outputの参照可能性を全履歴継承の理由にしない。
- EVIDENCE_GATE: repository evidence invocationは全lifecycleでdefault denyとする。`required_predicate_state := satisfied | unsatisfied | unobserved`、`evidence_consumer_ready := required predicateがnonterminal ∧ state=unobserved ∧ 現在欠けている観測値がbind済み ∧ requested resultがそのstateをbind可能`とし、target探索 / 変更前 / artifact変更後 / validation準備 / recoveryのいずれも`evidence_consumer_ready=true`の場合だけ発行する。TaskSpecがvalidation predicateを既に固定している場合、exact command / test locator / 既存test symbol / 一般的repository慣行が未固定なだけではそのpredicateを`unobserved`へ戻さず、execution method選択だけのためにevidenceを追加しない。artifact変更または失敗resultは、そのresultが入力を変えたpredicateだけを失効でき、他の`required_predicate_state`を一括で`unobserved`へ戻さない。consumerがterminalになれば未発行evidenceを失効する。変更前のevidence invocationはdefault denyとする。`spec_ready=false`では`TaskSpec本文 / TaskSpec明示の開始状態の直接観測`だけを許可し、未固定のrequired outcome valueをclarification resultにして変更前evidence operationをterminalにする。`spec_ready=true`の後は`target artifact / 明示read-only path / target pathへ適用中のrepository instruction / required outcomeを満たすimplementation choiceを解決するrepository authority`を許可する。repository evidenceはimplementation choiceをbindできるが、未固定のrequired outcome valueを事後に補完しない。`implementation_bound := 許可済みresultからtarget artifactとtargetへ適用中のrepository instructionがbindされ、TaskSpecがrequired outcomeに明示した全change effectとartifact間relationが、admission済みcurrent content上で実行可能な変更predicateと保持constraintを持つ一つのimplementation choiceへbind済み`。`implementation_bound=true`になったresultだけを変更前evidence operationのterminal resultとする。未発行の変更前evidence invocationを失効させ、次にartifact変更を発行する。artifact変更後に確定可能なrequired validation identityの探索は`VALIDATION_PLAN`で行い、変更前evidence operationを再開しない。追加evidenceは、許可済みresultが`missing / unreadable / bind済みvalueまたはconstraintとの具体的矛盾 / allowed path内で充足不能 / 適用中instructionによる別authorityの明示`を観測した場合だけ、そのresult identityと次のevidence identityをbindして一件許可する。permission / allowed read / available tool / 一般的安全確認は開放条件にしない。
- OWNER_ROLE: criterion owner語列はnon-machine riskの担当情報として保持し、worker operationの指定には使わない。TaskSpecが独立したproducer executionを明示した場合だけ、起動前にそのexecution identityをtask identityとしてproducerへbindし、predicate前に対応workerを起動する。`delegated_result_ready := runtime_spawn_result.task_name == task identity ∧ FINAL_ANSWER.Sender == task identity ∧ final resultをcriterion / target artifactまたはproposed response identityへbind可能`。`wait`は同期専用でidentity証跡にしない。`delegated_result_ready=false`の間はcriterionをpassedにせず、producer terminal後も`delegated_result_ready=false`ならcriterionを`unavailable`にする。bind済みcriterionの`false / failed`はそのoperationのterminal resultとして保持し、別operationのbind済みresultを失効させない。root宣言 / 進行記述 / 異Sender message / root再構成による補完は禁止する。
- ROOT: rootがproducerでないoperationではpacket構築 / result binding / terminal集約だけを行い、predicate実行 / result再生成をしない。
- INDEPENDENCE: 先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する。同一predicateを別producerへ再割当てしない。
- DECISION_BOUNDARY: `result_effect_scope := 受領resultがtarget / permission / method / stop conditionを変え得る未発行operation classの集合`、`decision_boundary(next_operation) := next_operation.class ∈ result_effect_scope`とする。resultの停止効果をtask全体または後続全invocationへ伝播させない。`decision_boundary=false`の既知の相互非依存invocationは分割せず同一model stepで発行し、全result受領後に一度だけ次を判断する。TaskSpec明示の開始identity resultは、TaskSpecがdrift時に禁止するoperation classだけを`result_effect_scope`へ入れる。drift時の停止条件がartifact変更とrequired commandを禁止するがreadを禁止しない場合、TaskSpecで既に許可・固定されたreadを開始identityと同一model stepから発行し、共同resultを受領するまでartifact変更とrequired commandだけを発行しない。read自体が禁止されるか、identity resultでread targetまたはpermissionが変わり得る場合だけreadを別stepへ置く。
- VALIDATION_CLOSURE: `validation_predicate_ready := artifact変更完了 ∧ TaskSpec-required validationのpredicate / order / individual pass condition / stop conditionが全件bind済み ∧ TaskSpecまたはcommand evidence protocolがexact commandを明示したvalidationだけそのcommandがbind済み`。`validation_predicate_ready=true ∧ producer=root`の場合、TaskSpecまたはcommand evidence protocolの「順に」「1 commandずつ個別」は、1回のcustom exec wrapper内で全required validationをbind順の個別`exec_command`として発行することを意味し、command resultをmodelへ返して次commandを別custom tool callで発行することを意味しない。各exit codeをwrapper内で確認し、nonzeroまたはunavailableなら後続を発行せず、shell compound commandへ結合しない。producerがroot以外の場合も全required validationを個別invocationとして同一model stepから発行する。完了済みの全resultを一度だけmodelへ返す。全件successかつ全result bind済みなら、TaskSpec追加要求またはresult失効がない限りread / validationを追加せずterminalを判断する。欠落 / non-success / unexpected stateはoperationをnonterminalにする。target探索 / 変更前 / review finding / 未固定methodまたはrecoveryへ適用しない。
- VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定しているdiff / status等を一つの実行票へ順にbindする。TaskSpecまたはcommand evidence protocolがexact commandを明示しない場合、その未固定commandをmissing validation identityまたはrepository evidenceの開放条件にせず、既に受領したTaskSpec / 適用中instruction / target evidenceの範囲から`METHOD`として選び、実行票発行時にcommandへbindする。検証success後はmodelへ戻らず実行票の残りを発行し、全result受領後に一度だけ完了を判断する。実行票完了後はTaskSpec追加要求またはresult失効がない限りtoolを追加しない。validation wrapperがcell ID付きnonterminal resultを返した場合、その返却を実行票の完了判定へ使わず、実行票全体がterminalになるまで同じcell IDへのwaitだけを発行する。commentary / 進捗報告 / 判断 / 別toolを先に発行しない。
- METHOD: TaskSpec明示手段だけを固定する。未固定手段はpredicateを変えずpermission内でexecutorが選び、validationでは既に受領したTaskSpec / 適用中instruction / target evidenceの範囲から選択して実行票発行時にcommandへbindする。exact commandの選択だけを理由にrepository evidenceを追加しない。invocationのfailed / unavailableをpermission否定 / terminalにせず、未固定手段があれば同一predicateへ向けて継続する。明示禁止 / permission否定は停止し、回避しない。
- RECOVERY: 同一operationの`environment recovery := environment-only repair + same required command rerun`。組の開始時だけ`environment_recovery_max`を消費し、未固定手段の選択は数えない。

## 比較試験の実行前gate

- 保存済みresultを基準に品質、token、elapsed、採用可否を比較する試験では、評価slotを一件でも発行する前に基準resultを一意にbindし、宣言したprompt identity以外の互換条件が完全一致することを証明するpreflight receiptを保存する。
- 一項目でも不一致、未固定、未確認があれば、評価slotを一件も発行しない。不一致の値と理由を報告して停止する。実行後に不一致を発見して結果を参考値へ降格する進め方を禁止する。
- 試験ごとに実行環境を最適化しない。保存済み基準resultと比較する場合は、その基準で固定したLayer 1を再利用する。
- 照合する互換条件の内訳、preflight command、Layer 1再利用、atomic run経路、並列上限の固定値は`evaluations/AGENTS.md`を正本とする。

## 共通の変更規律

- 一つの変更では一つの判断または一つのartifact単位を扱う。
- 依頼が要求しないartifactを変更しない。
- 既存artifactと周辺経路を破壊しない。
- 正本と履歴を区別する。
- 履歴artifactを現在解釈へin-placeで書き換えない。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- root `README.md`は入口と要約に限定し、詳細な履歴やCandidate全系譜を戻さない（配下READMEの詳細一覧は対象外）。
