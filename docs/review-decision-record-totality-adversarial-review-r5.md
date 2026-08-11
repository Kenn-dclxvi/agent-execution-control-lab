# review decision record全域性設計 実装前敵対的review r5

> terminal: `counterexample_found`

## review identityと入力封鎖

- producer identity: `review_decision_record_design_review_r5`
- 対象設計: `docs/review-decision-record-totality-design.md`
- 固定対象SHA-256: `267e345f90b1c56c2401e91ba84c7073b3e0e41784140151056502715df989c3`
- 開始時SHA-256: `267e345f90b1c56c2401e91ba84c7073b3e0e41784140151056502715df989c3`
- SHA照合: 一致

このreviewは、Candidate147原文、`docs/prompt-control-design-principles.md`、対象設計、および対象設計と本成果物へ適用されるrootと`docs/`の`AGENTS.md`だけを入力とした。後続Candidate本文、評価case、fixture、oracle、rating、raw trace、過去review artifactまたはfinding、期待terminal、修正案、会話履歴、その他のrepository artifactは参照していない。判断は上記producerが単独で行い、他producerへ再委譲していない。

## criterion別判定

| # | 判定 | 根拠 |
| --- | --- | --- |
| 1 | `no_counterexample_found` | `review_subject`はCandidate147が`implementation_bound=true`としてbindした一つの変更predicateと同一identityであり、複数targetやartifact間relationを理由に分割せず、複数predicateの場合だけ別subjectにする。一般反例は成立しなかった。 |
| 2 | `no_counterexample_found` | authority側とimplementation側の全change effect identityをfinite graphと0個以上のopen class componentへ非重複和として割り当て、component内外のedge、共有constraint、open classを含む共有constraintの全instance組合せresultまで一つの合成式で要求する。finiteのみ、open classのみ、混合、複数open classのいずれにも同じ式が適用され、一般反例は成立しなかった。 |
| 3 | `no_counterexample_found` | occurrenceの多重度とidentityを保持し、target、precondition、transformまたはend state、constraintの各bindingをidentityとbound valueの双方で比較し、必要なorderまたはdependency edgeも全件比較する。一般反例は成立しなかった。 |
| 4 | `no_counterexample_found` | finite graphが完全一致し、他の合成条件も成立する場合は`matched / not_required`となり、manifest、packet、reviewerを要求しない。一般反例は成立しなかった。 |
| 5 | `no_counterexample_found` | open classのfast pathは、現在のbasis、現在のclass predicate domain、決定的変換、component-local constraintにbindされたmachine-bound resultのterminal successを要求し、sampleや列挙済み部分集合を許さない。一般反例は成立しなかった。 |
| 6 | `no_counterexample_found` | `missing / unreadable / terminal_failure`を入力stateとして保持し、state mapとclassification mapのdomainを許可入力identity全集合へ一致させ、欠落または余剰があるpacketやterminalをadmitしない。一般反例は成立しなかった。 |
| 7 | `counterexample_found` | `counterexample_record`のwitnessとその根拠を許可入力およびsupport setへ閉じる等式がなく、`outcome_sensitive`が残るrecordも`counterexample_found`の形成条件から排除されていない。finding `R5-F01`を参照。 |
| 8 | `no_counterexample_found` | `no_counterexample_found`は全非value入力が`irrelevant`であり、`outcome_sensitive`が0件であることを要求する。`irrelevant`も許可値の変化でterminal judgementが変わらないことを受領済みpredicateから直接bindできる場合に限られる。一般反例は成立しなかった。 |
| 9 | `no_counterexample_found` | `unavailable`は、原因input identityと具体的反例predicate、terminalを変え得る不足identity、または明示permission denial／独立producer bind不能の原因identityのいずれかを要求し、open domainや一般的不確実性だけでは形成できない。一般反例は成立しなかった。 |
| 10 | `counterexample_found` | permission denial時の`unavailable`形成規則が、producer自身によるterminal形成およびroot補完禁止と同時に成立しない。finding `R5-F02`を参照。 |
| 11 | `counterexample_found` | finding `R5-F02`の状態では、Candidate147のproducer terminal result境界を保てば設計上要求されたterminalを形成できず、設計上のterminalを形成すればproducer境界を変更する。 |
| 12 | `no_counterexample_found` | 抽象的なbindingとrecord形成条件は定めるが、具体的tool、file、外部schema、read順、review回数、worker数または外部runtimeを解決条件として固定していない。一般反例は成立しなかった。 |

## finding records

### R5-F01: packet外witnessと未解決inputを持つ`counterexample_found`を形成できる

- 対応criterion: 7
- 再現可能な入力／状態:
  - `allowed_review_input_identity_set(subject) = {i}`
  - `review_input_state(i) = missing(i)`
  - `input_effect_class(i) = outcome_sensitive`
  - packetに含まれない具体的状態`w`について、subject treatment`t`、violated predicate`p`、direct conflict`t conflicts with p`をrecordへbindする。
  - `counterexample_support`へ分類された許可入力は0件なので、`counterexample_support_set = {}`とする。
- 設計が要求する処理: `counterexample_found`節は、witness、treatment、violated predicate、direct conflict、および全`counterexample_support`入力を含むsupport setがbind済みならrecordを形成する。この状態では列挙された全fieldが形式上bind済みである。`counterexample_found`の形成条件には、witnessが許可入力のstateであること、recordの意味fieldがsupport setだけに依存すること、support setが非空であること、または`outcome_sensitive=0`であることが含まれない。
- 違反するpredicate／constraint: review判断はpacketへ固定された許可入力だけから形成され、`counterexample_found`はwitnessとその直接矛盾を成立させる全supportをbindする、という入力封鎖およびcriterion 7の全件binding。
- 直接矛盾: packet外の`w`で反例terminalを形成でき、同時に許可入力`i`はterminalを変え得る未解決状態のまま残る。したがってsupport setはrecordの実質的dependencyを全件表現していない。
- 既存条項で閉じない理由: state mapとclassification mapのdomain一致は`i`の分類漏れを防ぐだけであり、terminal recordのfield dependencyを許可入力集合またはsupport setへ一致させない。rootの確認項目もfield identityとresult dependencyの確認に留まり、packet外dependencyを拒否する集合等式を定めない。`outcome_sensitive`を禁じる条件は`no_counterexample_found`にだけあり、`counterexample_found`にはない。

### R5-F02: permission denial時の`unavailable`に正当なproducerが存在しない

- 対応criterion: 10、11
- 再現可能な入力／状態:
  - `subject_correspondence(subject) = unmatched`
  - review permissionは明示的にdeniedである。
  - permission denialの原因identity`d`はbind済みである。
- 設計が要求する処理: `review要否とpacket形成`および正常経路は、producerを起動せず、原因identity`d`を持つ対応subjectの`unavailable`として変更を止める。一方、rootの受入境界は、`unavailable`を含むterminalをrootが補完・変換することを禁じ、`unavailable`はbind済みproducer自身が形成条件を満たすrecordとして返した場合だけterminalになるとする。
- 違反するpredicate／constraint: operationごとにproducerを一つbindし、そのproducerのterminal resultだけでoperationをterminalにするCandidate147の`PRODUCER`と`TERMINAL`、およびrootがproducerでないoperationのresultを再生成しない`ROOT`。
- 直接矛盾: permission denialに従ってproducerを起動しなければ、`unavailable`を返せるbind済みproducerが存在せずreview operationはnonterminalのままである。rootが`unavailable`を生成すれば、設計自身のroot補完禁止とCandidate147のproducer境界に違反する。
- 既存条項で閉じない理由: permission denialを`unavailable`の形成理由に含めても、そのrecordを生成するproducer identityは供給されない。独立producer bind不能を原因にできる条項も同じ自己欠落を持つ。packet発行前なので、root受入境界が要求するpacketの許可入力集合、state map、classification mapも形成されない。起動失敗をpermission denialへ読み替えない条項は、このproducer不在を解消しない。

## terminalとCandidate作成gateへの効果

- finding件数: 2
- terminal: `counterexample_found`
- Candidate作成gate: 閉鎖。対象設計を修正し、別identityの情報封鎖された独立producerが全criterionを再reviewして`no_counterexample_found`を返すまでCandidateを作成しない。

この成果物は設計reviewのterminal recordであり、Candidate、評価結果、採用、releaseまたはprojectionではない。
