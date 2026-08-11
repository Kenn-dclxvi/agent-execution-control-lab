# review decision record全域性設計の実装前敵対的review r2

> terminal: `counterexample_found`
>
> Candidate作成gate: `blocked`

## 入力封鎖と実行identity

- producer identity: `review_decision_record_design_review_r2`
- 対象設計: `docs/review-decision-record-totality-design.md`
- 固定対象SHA-256: `f1c659d5ad28ddfd81565b516b691df263a5da815589d2174e0033ee9775ea11`
- 開始時SHA-256照合: 一致
- 判断に使用した入力: Candidate147原文、`docs/prompt-control-design-principles.md`、対象設計、ならびに対象と作成先へ適用されるrootと`docs/`の`AGENTS.md`
- 封鎖した入力: 後続Candidate本文、評価case、fixture、oracle、rating、raw trace、過去review artifactとfinding、期待terminal、修正案、会話履歴、その他のrepository artifact
- 再委譲: なし

このreviewは設計本文の一般反例だけを判定した。特定caseの期待値、過去の実行結果、禁止入力からの推測はfindingに使用していない。

## criterion別判定

| # | criterion | 判定 | 根拠 |
| --- | --- | --- | --- |
| 1 | 一つのreview subjectがCandidate147の一つの`implementation_bound`変更predicateと一致するか | `no_counterexample_found` | `implementation_bound=true`でbindされた一つの変更predicateを一subjectとし、複数predicateの場合だけsubjectを分ける。read-only operation、validation、別required outcome、未来候補を加えず、既存predicateの分割もしない。 |
| 2 | finite fixed effectのentry集合とextra rule stateが全域的か | `counterexample_found` | Finding F-01。entryを数学的な集合として定義したため、同一tupleが複数回現れる効果の多重度が消える。`extra_effect_rule_state`も、集合外の規則が実装側にない場合はこの差を回収しない。 |
| 3 | target identityによる一対一対応がprecondition、transformまたはend state、constraintのidentityとbind済み値の意味差を取りこぼさないか | `counterexample_found` | Finding F-01。同一target identity、同一precondition、同一transform、同一constraintを複数回適用するauthorityと、一回だけ適用する実装が、集合化後には同じ一entryになる。各entry内のidentityと値の比較では適用回数の意味差を観測できない。 |
| 4 | fixed effect fast pathがmanifestやreviewerを要求しないか | `no_counterexample_found` | `matched`ではreviewを作らず個別admit可能とし、正常経路もmanifest、packet、reviewerを読まずに変更へ進むと明記している。 |
| 5 | open class fast pathが現在basisの全classを覆うmachine-bound保持resultを要求するか | `no_counterexample_found` | 現在の`open_class_basis`と同一identity・値をdependencyに持ち、現在class predicateの全instance、現在transform、全constraintを覆うterminal successだけを`matched`にする。sample、列挙済み部分集合、別versionは除外している。 |
| 6 | 非value stateを含む許可入力全集合と二つのmapのdomain一致を強制するか | `no_counterexample_found` | packet発行前にstate mapの完全一致を要求し、terminal前にclassification mapの完全一致と一identity一分類を要求する。root受入でも三domainの一致を確認し、不一致recordをadmitしない。 |
| 7 | `counterexample_found`が必須五要素を全件bindするか | `counterexample_found` | Finding F-02。五要素の存在自体は要求するが、`counterexample_support`は「input stateまたはvalue」を許す一方、support setは全support inputの「identityと値」だけを要求する。この型差により非value state自体が反例を直接成立させる入力をrecordへ閉じられない。 |
| 8 | `no_counterexample_found`がoutcome-sensitiveな非value inputを誤って`irrelevant`にできないか | `no_counterexample_found` | 非value inputを値の不存在だけで`irrelevant`にすることを禁じ、許可値が変わってもterminal judgementが変わらないことを受領済みpredicateから直接bindする必要がある。全非value inputの`irrelevant`と`outcome_sensitive=0`もterminal条件である。 |
| 9 | `unavailable`が具体的な反例predicateまたは欠落dependencyを要求し、一般的不確実性を許さないか | `no_counterexample_found` | outcome-sensitive入力には原因identityと具体的反例predicateを要求し、counterexample record不足にはterminalを変え得る不足identityを要求する。open domain、未来instance未列挙、一般的不確実性、探索未完了だけの`unavailable`を禁じている。 |
| 10 | root補完、重複review、別producerへの再割当てを導入していないか | `no_counterexample_found` | rootの意味再判定と欠落補完を禁じ、不完全recordをnonterminalのまま保持する。同じjudgementのrootまたは別producerへの再割当ても禁じる。 |
| 11 | Candidate147のoperation identity、permission、producer、terminal、result effect boundaryを変更していないか | `no_counterexample_found` | Candidate147の一変更predicateをsubject単位として保ち、reviewを独立producerの別operationとして形成する。result効果は対応subjectを含む未発行変更だけに限定し、別subject、read-only operation、別required outcome、task全体へ伝播させない。 |
| 12 | tool、file、schema、read順、review回数、worker数、外部runtimeを固定していないか | `no_counterexample_found` | 設計は境界上のidentity、state、record field、単一producer operationを定めるが、実行手段としてのtool、file、schema、read順、試行回数、worker数、runtimeまたは外部executorを解決条件にしていない。 |

## finding records

### F-01: entry集合が同一効果の多重度を消し、異なる変更predicateを`matched`にできる

- 対応criterion: 2、3
- 再現可能な入力・状態:
  - authorityは、一つのsubjectで同じtarget `T`へ、同じprecondition `P`の下、同じtransform `increment`を二回適用する有限固定効果を直接bindしている。
  - 各回のconstraint binding集合は同じ`C`である。
  - Candidate147のimplementation choiceは、同じtarget `T`へ同じ`P`、同じ`increment`、同じ`C`を一回だけ適用する変更predicateとしてbindされている。
  - 実装にはentry集合の外へ届くselection、fallback、normalizationまたは追加変換がないため、`extra_effect_rule_state=absent`である。
- 設計が要求する処理:
  - authorityとimplementationをそれぞれ`{(target_binding, precondition_binding, transform_or_end_state_binding, constraint_binding_set)}`という集合へ変換する。
  - authority側の同一tuple二個は集合では一要素へ縮約される。implementation側も同じ一要素である。
  - entry数、target identityによる対応、各bindingのidentityと値、constraint集合、`extra_effect_rule_state=absent`がすべて一致するため、`finite_effect_matched=true`となり、review不要でadmit可能になる。
- 違反するpredicate・constraint:
  - 一つのreview subjectがCandidate147の一つの変更predicateの意味全体を保持すること。
  - finite fixed effectのentry対応がauthorityとimplementationの全change effectを全域的に比較すること。
  - transformのbind済み値の意味差を取りこぼさないこと。
- 直接矛盾:
  - authorityの効果は二回適用、implementationの効果は一回適用であり、変更predicateの効果は一致しない。それにもかかわらず集合化により多重度が消え、`matched / not_required`になる。
- 既存条項で閉じない理由:
  - entryにはoccurrence identity、順序、または多重度がない。
  - target identityによる一対一対応は、集合化後に残った一entry同士しか比較しない。
  - `extra_effect_rule_state`はimplementationのentry集合外の規則を分類するが、このimplementationには追加規則がないため`absent`であり、authority側で失われた二回目を復元しない。

### F-02: 非value state自体が反例supportの場合に必須support setを形成できない

- 対応criterion: 7
- 再現可能な入力・状態:
  - packetの許可入力identity `I`は`review_input_state(I)=missing(I)`である。
  - authorityのbind済みpredicateは`I`が必須であることを要求し、subjectは`missing(I)`を成功として処遇する。
  - したがって現在の`missing(I)`というinput state自体が、subject treatmentとauthority predicateの具体的な直接矛盾を成立させる。`input_effect_class(I)=counterexample_support`である。
- 設計が要求する処理:
  - `counterexample_found`にはwitness、subject treatment、violated predicate、direct conflict、support setの五要素を要求する。
  - `counterexample_support`の定義はinput stateまたはvalueが反例を直接成立させる場合を含む。
  - 一方、`counterexample_support_set`は全support inputの「identityと値」でなければならない。
- 違反するpredicate・constraint:
  - `missing / unreadable / terminal_failure`を含む許可入力全集合の判断効果を排他的terminal recordへ閉じること。
  - 具体的反例が成立した場合に、五要素をbindした`counterexample_found`を形成できること。
- 直接矛盾:
  - `missing(I)`にはbind可能なvalueがないため、反例を直接支えるstateは存在しても、必須support setの`identityと値`を形成できない。具体的反例が成立しているのに`counterexample_found`を返せない。
- 既存条項で閉じない理由:
  - state mapに`missing(I)`を記録しても、support setの必須fieldはstateではなくvalueを要求する。
  - `unavailable`のcounterexample record不足条項は、受領済みinputだけで不足要素を対応づけられない場合を扱うが、この例ではdependencyが欠けているのではなく、許可された非value stateをsupport setの要求型が表現できない。
  - rootによる補完は禁止されており、不完全recordはnonterminalのままになるため、別terminalもこの反例を閉じない。

同じ反例は、`unreadable(identity)`または`terminal_failure(identity,result)`というstate自体がauthorityまたは保持constraintとの直接矛盾を成立させる場合にも再現する。

## terminalとCandidate作成gateへの効果

- finding件数: 2
- terminal: `counterexample_found`
- Candidate作成gateへの効果: 一件以上の一般反例が成立したため`blocked`。このreview resultのままCandidateを作成できない。
- result effect scope: 対象設計に基づく未発行のCandidate作成だけを停止する。対象設計以外のartifact、別required outcome、評価、採用、releaseまたはprojectionの状態を変更しない。
