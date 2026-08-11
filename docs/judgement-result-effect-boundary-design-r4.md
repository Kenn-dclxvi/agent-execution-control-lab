# 判断結果の効果境界設計 第4版

> 状態: `pre_candidate_design_revision_4 / adversarial_review_not_started / candidate_not_created`

## 結論

この設計はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接の基準とし、変更predicateについて独立reviewが必要かを決める発行境界と、review resultが未発行のartifact変更へ及ぼせる効果境界を一つの制御として追加する。

追加する制御は`judgement_result_effect_boundary`の一改訂だけである。Candidate147がbindしたoperation、producer、terminal result、evidence consumer、`implementation_bound`、変更predicateおよび`result_effect_scope`の単位を変更しない。reviewのtool、read順、回数、file、schema、record形式または実行方法は固定しない。

本設計はCandidate bundleではない。情報封鎖した実装前敵対的reviewが`no_counterexample_found`で終端するまでCandidate番号、prompt bundle、profile、Target評価、採用、releaseまたはprojectionを作成しない。

## 基準と非継承

直接の基準はCandidate147だけとする。Candidate184を含む後続Candidateの本文、構造、identity体系、registry、canonical locator、完全coverage条件、未来集合の閉包条件およびresult schemaは継承しない。

Candidate147の`implementation_bound=true`を開始条件とする。TaskSpecが要求する全change effect、artifact間relation、実行可能な変更predicateおよび保持constraintが一つのimplementation choiceへbindされていなければ、本境界を開始せずCandidate147の変更前gateで停止する。本境界は不完全な`implementation_bound`を補完、再探索または独立に証明しない。

## 判断subjectの単位

`judgement_subject`は、Candidate147のterminal resultが一つの実行可能な変更predicateとしてbindしたidentityとする。

- 一つのpredicateが複数target、複数field、複数artifactまたは一つのartifact間relationを含んでも、一subjectのままとする。
- target数、変更field数、artifact数またはrelationの存在からrootやreview producerがsubjectを分割しない。
- Candidate147が複数predicateを個別にbindした場合だけ、複数subjectとする。
- read-only operation、validation operationおよび別required outcomeはsubjectにしない。

artifact変更invocationを発行する前に、そのpayloadが同時生成し得る全subject identity、適用順および保持constraintを一つの`coemission_set(invocation)`へ過不足なくbindする。payload、subject identity、適用順または保持constraintが変われば新しいcoemission identityとする。予定していないsubject集合や未来の全組合せは列挙しない。

## review admissionの固定順序

各subjectは、次の順序を飛ばさず一度だけ進む。

1. Candidate147の`implementation_bound=true`を確認する。
2. Candidate147がbindした変更predicateを一subjectとして固定する。
3. `fixed_effect_correspondence_state`を一つbindする。
4. `review_requirement`を一つbindする。
5. `review_requirement=not_required`ならreview permission、manifestまたはpacket readinessを評価せず個別admissionへ進む。
6. `review_requirement=required`ならreview permissionと情報封鎖producerのbind可否を評価する。
7. permissionが許可されproducerをbindできる場合、全許可入力をterminal stateへbindしてpacketを発行する。
8. review producerのterminal judgementを受領し、そのresultに対応する局所効果だけを適用する。

後段の値を前段の判定へ逆流させない。`design_relies_on_boundary`、review permission、manifest、expected readable state、現在のtarget数、具体的反例、予定validationまたはpacket内入力の可読性は、`fixed_effect_correspondence_state`を変更できない。

## 固定対応の三状態

`fixed_effect_correspondence_state(subject) := matched | unmatched | unbound`

三状態は排他的であり、必ず一つへbindする。

### 有限固定対応

有限固定対応の比較入力は次に限定する。

- TaskSpecまたは適用中authorityが直接固定した有限な全target identity
- 各targetへ適用する決定的変換または終状態
- TaskSpecまたは適用中authorityが直接固定した保持constraint
- Candidate147の`implementation_bound`へbind済み変更predicateのtarget、変換または終状態、保持constraint
- 変更predicateに選択規則、fallback、正規化または固定範囲外へ届く規則が含まれるか

`finite_fixed_effect_matched(subject) := authorityの全target identity集合 == 変更predicateの全target identity集合 ∧ authorityの変換または終状態 == 変更predicateの変換または終状態 ∧ authorityの全保持constraint == 変更predicateの全保持constraint ∧ 追加の選択規則、fallback、正規化または固定範囲外規則がない`

targetが一件か複数かはこの式を変えない。複数targetへ一つのrelationを保持する変更も、Candidate147が一predicateとしてbindした場合はtarget集合、各変換およびrelation constraintを同じ一回の照合へ入れる。複数targetであることやrelationを持つことだけではreview対象にしない。

### open class固定対応

open classへ届く変更は、class predicate identityと決定的変換が固定されているだけでは`matched`にしない。

`class_fixed_effect_matched(subject) := TaskSpecまたは適用中authorityが定義・version付きclass predicate identityと決定的変換を固定済み ∧ 既存の許可済みmachine-bound resultが同じclass predicate identity・変換identity・全保持constraint identityへbindされ、その変換がclassの任意入力で全保持constraintを維持するresultを直接持つ ∧ Candidate147の変更predicateがその全identityと一致 ∧ 追加の選択規則、fallbackまたは正規化がない`

### 三状態へのbind

- 有限固定対応またはopen class固定対応の式が全項目で成立した場合は`matched`。
- 比較入力が全件bind済みで、一項目以上の具体的不一致または固定範囲外規則を観測した場合は`unmatched`。
- 比較に必要なidentityまたは値が`missing / unreadable / terminal failure`で、一致も具体的不一致もbindできない場合は`unbound`。

`unbound`をclarification、task全体の停止、追加証明または未来列挙へ変換しない。固定対応として省略できないことだけを意味する。

## review要否の二状態

`review_requirement(subject) := not_required if fixed_effect_correspondence_state=matched else required`

二状態は排他的である。

- `not_required`では`individual_admission_ready=true`とし、個別review operationを作らない。
- `required`では、permissionが許可され情報封鎖producerをbind可能なら個別review operationを必ず発行する。
- `design_relies_on_boundary=true`は`matched`を`required`へ変更しない。
- 現在targetが少数、現在値でconstraint成立、producer説明、反例の未発見または予定validationは`unmatched / unbound`を`not_required`へ変更しない。
- review permissionはreviewの発行可否であり、review要否を決めない。

rootは同じsubjectへ`not_required`とreview operationの両方をbindできない。固定対応を後からreview resultで再確認しない。固定対応のdependencyが変わった場合だけ旧`matched`を失効し、新しいbasisで三状態からやり直す。

## review発行前のpermission

`review_requirement=required`のsubjectだけについてpermissionを評価する。

- 明示的なpermission denialは、原因identityを`unavailable_dependency`へbindした当該subjectの`unavailable` terminalにする。
- permission内で情報封鎖producerをbind不能な場合も、原因identityをbindした当該subjectの`unavailable` terminalにする。
- 起動方法のfailedまたはunavailableをpermission denialへ読み替えず、Candidate147の`METHOD`と`RECOVERY`で同じreview predicateへ継続する。

permission denial、producer bind不能または起動方法失敗を、固定対応の照合結果、別subject、read-only operationまたはtask全体へ伝播させない。

## review入力の四状態

reviewへ渡す各許可入力identityを、次の排他的な一状態へbindする。

`review_input_state(input) := value(identity,value) | missing(identity) | unreadable(identity) | terminal_failure(identity,result)`

値が得られないことと、入力identity自体が未固定であることを分ける。TaskSpec、authority、manifestまたはCandidate147の許可済みresultから入力identityが固定されていれば、値が`missing / unreadable / terminal failure`でも入力はbind済みである。

`review_packet_bound := subject identity、保持constraint、review criterion、許可入力identityが全件固定済み ∧ 各許可入力identityにreview_input_stateが一つだけbind済み ∧ 禁止入力がpacketにない`

`review_launch_ready := review_requirement=required ∧ permission=allowed ∧ 情報封鎖producerがbind済み ∧ review_packet_bound=true`

`missing / unreadable / terminal failure`は`review_packet_bound=false`にしない。manifestの`expected_readable_state`と`success_condition`はreviewerがterminal judgementを作る入力であり、review発行前のpass conditionではない。

このreview operationについて、Candidate147の`CONTEXT`が要求する`required evidence`は、値の成功取得ではなく、許可入力identityに対する一つの`review_input_state`のbindで満たす。可読性の成功を要求するTaskSpec validation predicate、review後のadmission predicateまたはartifact変更predicateを、packet formation predicateへ流入させない。

repository evidenceの完全性、input domainの開閉、具体的反例の有無、反例探索の完了度またはmanifest項目の成功数をreview発行判断へ入れない。

## review producerの情報境界

review producerはimplementation choiceを生成したproducerと異なるexecution identityへbindする。渡せる入力は次に限定する。

- TaskSpec
- 適用中authority
- Candidate147が許可したrepository evidence
- bind済みimplementation choice
- subjectまたはcoemission set
- 保持constraint
- review criterion
- 各許可入力の`review_input_state`

評価case、fixture、oracle、rating、過去finding、旧Candidate、期待terminal、修正案および会話履歴は渡さない。禁止入力を観測したproducer由来resultは、別producerへ要約または転送してもreview basisへadmitしない。

## 個別reviewの三つのterminal judgement

個別review producerは各subjectへ、次の排他的terminal judgementを一つ返す。

- `counterexample_found`
- `no_counterexample_found`
- `unavailable`

rootはproducer identity、terminal性、subject identity、result identityおよびdependency bindingだけを確認する。反例の意味、missingの関連性または反例なしの十分性を再判定、補完、比較または再採点しない。

### `counterexample_found`

具体的入力または状態、subjectの出力または処遇、TaskSpec・authority・保持constraintとの直接矛盾をbindした場合だけ成立する。反例の成立条件を変え得る受領入力identityと値だけを`counterexample_support`へbindする。support外のmissing、unreadable、terminal failure、別subject resultまたは将来入力は成立済み反例を失効できない。

### `no_counterexample_found`

未来全域の不存在証明ではない。発行時に受領したTaskSpec、authority、subject、保持constraintおよび全`review_input_state`に対して具体的反例を見つけず、かつ値が得られれば同じ判断を変え得るmissing等がない場合だけ成立する。判断を変え得る入力だけを`no_counterexample_dependency`へbindする。

### `unavailable`

値次第で同じsubjectの具体的反例を成立させ得る`missing / unreadable / terminal failure`、または必要なsubject・authority・保持constraint・dependency identityの対応不能へbindする。原因identityと変わり得る反例predicateを`unavailable_dependency`へbindする。open domain、未来instance未列挙または一般的不確実性だけでは成立させない。

## 同時発行集合のreview境界

`coemission_set`が一subjectだけなら組合せreviewは不要である。複数subjectではartifact変更前に、`joint_effect_independent | combination_no_counterexample_found | combination_counterexample_found | combination_unavailable`の排他的stateを一つbindする。

`joint_effect_independent`は、Candidate147へbind済みのartifact間relation、変更predicate、適用順および保持constraintから、各subjectの出力・適用条件・保持constraintが他subjectの有無またはresultで変わらず、全joint constraintが個別constraintへ分解済みであることを既存machine-bound resultから直接確認できる場合だけ成立する。

直接bindできなければ、実際の`coemission_set`全体を一つのcombination subjectとして情報封鎖producerへ必ずreviewを発行する。全subsetを事前列挙せず、反例時だけ最小subject集合をsupportへbindする。combination reviewにも同じpermission、四状態入力、packet formation、情報封鎖、三状態judgementおよびdependency規則を適用する。

## judgement resultの効果範囲

review operation発行前に次をbindする。

`judgement_result_effect_scope(result) := resultがadmission、停止、失効または再reviewの要否を変え得る未発行subject、coemission identityおよびartifact変更invocationの具体的集合`

各resultの効果を次へ限定する。

- 個別`counterexample_found`: 対応subjectを含む未発行artifact変更だけを停止する。
- 個別`no_counterexample_found`: 対応subjectだけを個別にadmit可能にする。
- 個別`unavailable`: 対応subjectを含む未発行artifact変更だけを停止する。
- `combination_counterexample_found`: 同じcoemission identityの未発行artifact変更だけを停止する。
- `combination_no_counterexample_found`: 同じcoemission identityだけをadmit可能にする。
- `combination_unavailable`: 同じcoemission identityの未発行artifact変更だけを停止する。

停止subjectまたはcoemission identityを除くとrequired outcome、artifact間relation、実行可能性または保持constraintを満たせない場合、Candidate147の当該implementation choiceだけを失効する。別subject、別coemission、read-only operation、別required outcomeまたはtask全体へ停止を伝播させない。

## artifact変更のadmission

`individual_admission_ready(subject) := review_requirement=not_required ∨ admissibleなno_counterexample_foundがsubjectへbind済み`

`joint_admission_ready(invocation) := coemission_setが一subject ∨ joint_effect_independentがcoemission identityへbind済み ∨ admissibleなcombination_no_counterexample_foundが同じcoemission identityへbind済み`

artifact変更invocationは、全subjectが同じpayloadへ過不足なく対応し、全個別admission、joint admission、scope内reviewのterminalおよびpayload identity一致が揃い、有効な停止resultがない場合だけ発行する。

停止subjectをpayloadから除外するとCandidate147の保持constraintまたは実行可能性を壊す場合は、一部だけを発行せずimplementation choiceを失効する。

## dependencyと局所失効

各固定対応、個別judgement、joint independenceおよびcombination judgementへ、terminal時の全dependency identityと値を`judgement_basis_identity`としてbindする。

`judgement_result_valid(result) := 現在の全bind済みdependency identityと値がjudgement_basis_identityと完全一致`

次の未発行operation前に一致を確認し、不一致なら旧resultを失効する。失効resultをadmission、停止、待機解除、別result失効またはterminal集約へ使用しない。変更後basisへ同じpredicateの新producerを一つbindする。一致するdependencyを、support外のmissing解消、同値再取得、full packet変化または無関係resultだけで失効させない。

固定対応のbasisはtarget集合、変換または終状態、保持constraint、固定範囲外規則の不存在とする。個別judgementは各support、judgement dependencyまたはunavailable dependencyだけ、joint resultはcoemission identity、適用順、subject predicate、artifact間relation、全保持constraintおよびbind済み判断dependencyだけへbindする。

## 最短経路

TaskSpecまたは適用中authorityが有限な全target identity、各targetの終状態および保持constraintを直接固定し、Candidate147の一つの変更predicateが同じtarget集合、終状態およびconstraintだけへ一致する場合、`fixed_effect_correspondence_state=matched`、`review_requirement=not_required`となる。targetが一件でも複数でも、review permission、manifestおよびpacket readinessを評価せずCandidate147のartifact変更経路へ進む。

open classへ届き、class全域のconstraint保持resultがない場合は`unmatched`または`unbound`、`review_requirement=required`となる。permissionが許可されproducerをbindできれば、全manifest入力を`value / missing / unreadable / terminal_failure`のいずれかへbindし、そのままreviewを発行する。

## Candidate作成前gate

情報封鎖した独立producerへ、次の三文書だけを渡して敵対的reviewを行う。

- Candidate147の制御原文
- `docs/prompt-control-design-principles.md`
- この設計

Candidate実装、評価設計、評価case、fixture、oracle、rating、保存済みresult、旧Candidate、先行review findingおよび会話履歴は渡さない。

review producerは一般入力で次の反例を探す。

1. finiteなauthority固定変更に`design_relies_on_boundary`、target数、relationまたはpermissionを理由として不要reviewを要求できる。
2. 必要な比較identityが欠けた固定対応をreview不要にできる。
3. open classへ届く変更を、class全域のconstraint保持resultなしでreview不要にできる。
4. 一つのCandidate147変更predicateをtarget、field、artifactまたはrelationの数から複数subjectへ分割できる。
5. `missing / unreadable / terminal failure`をpacket readiness不足としてreview発行前に停止できる。
6. manifestのexpected readable stateまたはsuccess conditionをreview発行前のpass conditionへ変換できる。
7. permission denial、producer bind不能または起動失敗を互いに読み替えられる。
8. support外のmissingで成立済み反例を失効できる。
9. 判断を変え得るmissingがあるまま`no_counterexample_found`をadmitできる。
10. open domainまたは未来instance未列挙だけで`unavailable`にできる。
11. 複数subjectを同時発行するとき、machine-boundなjoint independenceも同じcoemission identityのcombination judgementもないまま変更をadmitできる。
12. 一subjectまたは一coemission identityの失敗を別subject、別coemission、read-only operationまたはtask全体へ伝播できる。
13. dependency変更後の旧resultを維持できる、またはdependency不変なのに旧resultを失効できる。
14. rootがreview resultの意味、missing関連性、反例または反例なしを再判定できる。
15. 固定tool、file、schema、locator、read順またはreview回数がなければ実行不能になる。

一件でも具体的反例が成立した場合は`counterexample_found`としてこのdesign identityを停止し、修正版を新しいdesign revisionとして再reviewする。全観点で具体的反例が成立しない場合だけ`no_counterexample_found`とし、Candidate147を直接親とする一つのCandidate bundleを作成できる。

## 後続境界

設計reviewの通過は、実装一致、Target評価、採用、releaseまたはprojectionを意味しない。

Candidate作成後は、Candidate147とprompt identity以外が完全一致する固定Target評価をpreflightし、保存済み基準runを再実行せず新Candidateの不足runだけを発行する。品質とmechanismを別gateにし、正しいterminalだけでなく固定対応、review起動、四状態packet、情報封鎖、support、dependency、coemission set、result効果scopeおよびartifact変更有無を個別に監査する。
