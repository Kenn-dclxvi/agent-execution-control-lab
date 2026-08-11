# review decision record全域性設計 実装前敵対的review r6

> 状態: `completed / counterexample_found / candidate_creation_blocked`

## review identityと入力封鎖

- producer identity: `review_decision_record_design_review_r6`
- 対象設計: `docs/review-decision-record-totality-design.md`
- 固定対象SHA-256: `2ee882d3d207da937521525d9fb0b428ce0cecf8270fa02f45a893076c69b19b`
- 開始時SHA-256照合: 一致
- 判断方法: 各criterionについて、許可入力だけから具体的な一般反例を探索した。

判断に使用したrepository入力は、Candidate147制御原文、`docs/prompt-control-design-principles.md`、対象設計、および対象設計と本成果物へ適用されるルートと`docs/`の`AGENTS.md`だけである。Candidate185を含む後続Candidate本文、評価case、fixture、oracle、rating、raw trace、過去review artifactまたはfinding、期待terminal、修正案、会話履歴、その他のrepository artifactは読まず、判断へ使用していない。

## 結論

terminalは`counterexample_found`である。一般反例は2件あるため、設計はこのidentityのままCandidate作成へ進めない。

## criterion別判定

| # | 判定 | 根拠 |
| --- | --- | --- |
| 1 | `no_counterexample_found` | `implementation_bound=true`でbind済みの一つの変更predicate identityを一つの`review_subject`とし、複数predicateの場合だけsubjectを分ける。複数targetやartifact間relationを理由に分割する経路はない。 |
| 2 | `no_counterexample_found` | authority側とimplementation側の全effect identityについて非重複和集合によるcoverageを要求し、finite、open class、混合、複数open classの全componentとcomponent間relation、共有constraint、必要な合成resultを一つの合成式で閉じる。部分componentの一致をsubject全体へ昇格できない。 |
| 3 | `no_counterexample_found` | occurrence数とidentityによる一対一対応に加え、target、precondition、transformまたはend state、constraintのidentityとbind済み値、edgeの一致を全件要求する。重複の集合縮約や自然言語上の類似一致は許されない。 |
| 4 | `no_counterexample_found` | finite graphとrelation basisを含むcorrespondenceが`matched`なら`not_required`となり、packet、manifest、review admissionまたはreviewerを作らない。 |
| 5 | `no_counterexample_found` | open class componentは現在のbasis、現在class predicateの全domain、現在の決定的変換、component-local constraintを持つmachine-bound resultのterminal successを要求する。sample、部分集合、別versionでは代用できない。 |
| 6 | `no_counterexample_found` | `missing / unreadable / terminal_failure`をterminal input stateとして認めつつ、許可入力identity全集合、state map、classification mapのdomain完全一致と一identity一分類を要求する。 |
| 7 | `counterexample_found` | Finding F-01。`violated_predicate_identity`にはTaskSpec predicateを許す一方、`record_dependency_identity_set`の許可basisからTaskSpec identityを除外しているため、TaskSpecだけが所有するpredicateへの具体的反例を依存関係ごとrecordへbindできない。 |
| 8 | `no_counterexample_found` | 非value入力を値がないことだけで`irrelevant`にすることを禁止し、別の許可値で反例成立が変わり得る場合は`outcome_sensitive`を要求する。`no_counterexample_found`は全非value入力が`irrelevant`かつ`outcome_sensitive=0`の場合に限定される。 |
| 9 | `no_counterexample_found` | `unavailable`は原因input identityと成立可否が変わり得る具体的反例predicate、またはterminalを変え得る不足identityを要求する。open domain、未来instance未列挙、一般的不確実性、探索未完了だけでは形成できない。 |
| 10 | `counterexample_found` | Finding F-02。producer自身がterminal別形成条件を満たしても、rootの受入境界が非空support setと`outcome_sensitive=0`をterminal種別で分岐せず要求するため、`no_counterexample_found`と`outcome_sensitive`型`unavailable`をnonterminalへ戻す。producer judgementをrootがterminal共通条件で上書きする一般経路が残る。 |
| 11 | `no_counterexample_found` | 追加resultの効果は対応subjectの未発行artifact変更だけへ限定される。別subject、read-only operation、別required outcomeまたはtask全体へ伝播せず、Candidate147のoperation identity、permission、producer、terminal、result effect boundaryを置換しない。 |
| 12 | `no_counterexample_found` | 固定しているのは意味上のbinding順と境界であり、tool、file、schema、read順、review回数、worker数または外部runtimeを解決条件にしていない。 |

## finding record

### F-01: TaskSpec predicateを反例dependencyへ収容できない

- 対応criterion: 7
- 再現可能な入力・状態: packet内の許可入力`input_A`が`value(input_A, v)`であり、subjectの処遇`treatment_T`が、適用中authorityや保持constraintには複製されていないTaskSpec predicate `P_task`へ直接違反する。`input_A`だけで反例成立が確定し、他の全許可入力は成立可否を変えない。
- 設計が要求する処理: `counterexample_record`の`violated_predicate_identity`へ`P_task`をbindし、`input_A`のstateを非空の`counterexample_support_set`へbindする。同時に、recordの全dependencyを`record_dependency_identity_set`へbindし、その集合をpacket identity basisの許可部分集合にする。
- 違反するpredicateまたはconstraint: `counterexample_found`はTaskSpec predicateを正規の違反predicateとして表現し、その必須fieldとdependencyをpacket内だけで全件bindできなければならない。
- 直接矛盾: `violated_predicate_identity`の選択肢はTaskSpec、authority、保持constraintを含むが、`record_dependency_identity_set`へ入れてよいidentityはsubject、authority、保持constraint、`counterexample_support_set`だけであり、TaskSpec identityがない。`P_task`を入れると許可basis外となり、入れないと必須fieldのdependencyが欠落する。
- 既存条項で閉じない理由: packet自体にはTaskSpecを含める条項があるが、後段のdependency subsetをTaskSpecまで拡張する条項はない。rootは不足fieldやdependencyを補完できず、不完全recordをterminalへ変換できない。そのため、packet内の具体的反例であっても適法な`counterexample_found`を形成できない。

### F-02: rootの共通受入条件がterminal別形成条件と両立しない

- 対応criterion: 10
- 再現可能な入力・状態A: 許可入力全集合の全value入力に具体的反例がなく、全inputが`irrelevant`で、`outcome_sensitive=0`である。producerは定義どおり`no_counterexample_found`を形成する。このterminalには`counterexample_support`がなく、非空support setは形成されない。
- 再現可能な入力・状態B: 非value入力`input_M`が`missing(input_M)`であり、その別の許可値によって具体的反例predicate `P_M`の成立可否が変わる。producerは`input_M`と`P_M`をbindし、`outcome_sensitive`を1件以上持つ`unavailable`を形成する。
- 設計が要求する処理: producer terminalを受け取ったrootは、terminalごとに定義済みの形成条件を機械的に確認し、意味判断を再実行せず、適合するterminal resultを保持する。
- 違反するpredicateまたはconstraint: review judgementはbind済み独立producerだけが形成し、rootはその意味や十分性を再判定せず、不完全recordだけをnonterminalとして保持しなければならない。
- 直接矛盾: rootの受入境界はterminal種別による限定なしに「非空support set」と`outcome_sensitive=0`の確認を列挙する。状態Aは非空support setを持てず、状態Bは`outcome_sensitive=0`を満たせないため、どちらも各terminal固有の形成条件を満たしながらroot受入条件を満たせない。
- 既存条項で閉じない理由: 非空support setは`counterexample_found`だけの必須条件であり、`no_counterexample_found`へ空support setを明示的に許すroot分岐がない。`outcome_sensitive`を原因とする`unavailable`をrootだけ例外扱いする分岐もない。rootはterminalを補完または変換できないため、正しく形成されたproducer resultをnonterminalへ戻す一般経路が残る。

## terminalとCandidate作成gateへの効果

- terminal: `counterexample_found`
- finding件数: 2
- gate効果: Candidate作成を停止する。対象設計を修正し、別identityの独立producerが全criterionを再reviewして`no_counterexample_found`となるまで、Candidate番号、prompt bundle、profile、Target評価、採用、releaseまたはprojectionへ進めない。
