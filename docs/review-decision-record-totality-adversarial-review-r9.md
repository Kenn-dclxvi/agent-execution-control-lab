# review decision record全域性設計の実装前敵対的review r9

## review identityと入力封鎖

- producer identity: `review_decision_record_design_review_r9`
- 対象設計: `docs/review-decision-record-totality-design.md`
- 固定対象SHA-256: `484b4834e3e32b1ac3977e103f090f26e94e8a890d98bfcf37794e975790bff6`
- 開始時照合結果: 一致
- 許可入力: Candidate147原文、`docs/prompt-control-design-principles.md`、対象設計、および対象設計と本成果物へ適用されるroot `AGENTS.md`と`docs/AGENTS.md`だけを使用した。
- 禁止入力: 後続Candidate本文、評価case、fixture、oracle、rating、raw trace、過去review artifactまたはfinding、期待terminal、修正案、会話履歴、その他repository artifactを使用していない。
- 判断境界: 各criterionについて、再現可能な入力または状態を持つ一般反例だけをfindingとした。表現上の好み、一般的不確実性、特定caseの期待値はfindingにしていない。

## 結論

terminalは`counterexample_found`である。一般反例は2件成立したため、この設計は現状のままCandidate作成へ進めない。

## criterion別判定

| # | 判定 | 根拠 |
| --- | --- | --- |
| 1 | 一般反例なし | `implementation_bound=true`で一つの実行可能な変更predicateとしてbindされたidentityを一つのsubjectとし、複数predicateの場合だけsubjectを分ける。複数target、field、artifactまたはartifact間relationを含む一predicateを分割しないため、Candidate147の変更predicate単位を保持している。 |
| 2 | 一般反例なし | authority側とimplementation側の全change effect identityを、finite occurrenceと複数個を許すopen class componentの非重複和へpartitionする。component間edge、共有constraintのdependency set、合成後の保持resultおよび単一の合成式を要求するため、finiteだけ、open classだけ、混合、複数open classのいずれも一部一致を全体一致へ昇格できない。 |
| 3 | 一般反例なし | occurrence identityによる一対一対応に加え、各nodeのtarget、precondition、transformまたはend state、constraint参照をidentityとbind済み値で比較する。constraint本体はsubject relation basisでidentity、bound value、dependency set、evaluation stageを比較するため、参照だけの一致で意味差を消せない。 |
| 4 | 一般反例なし | 有限固定効果はoccurrence graph、relation basis、extra ruleの一回の照合だけで`matched / not_required`となり、manifest、packetまたはreviewerを要求しないことが正常経路にも明記されている。 |
| 5 | 一般反例なし | 各open class componentについて、現在のclass predicate全域、現在の決定的変換、component-local constraintへbindされたmachine predicateとterminal successを要求する。複数component共有constraintには、現在の全dependent component basisと全instance組合せを覆う別のsubject relation resultを要求する。 |
| 6 | 一般反例あり | Finding F-01。state mapとclassification mapはpacketが自己申告した集合とのdomain一致しか検査されず、permission内で渡せる入力identity全集合そのもののcoverageを機械的に確定するbasisがない。 |
| 7 | 一般反例あり | Finding F-02。`counterexample_found`の構造的field、非空support set、packet内dependency、表面上の`outcome_sensitive=0`は要求されるが、全許可入力の分類根拠はrecordへbindされない。そのため、実際にはoutcome-sensitiveな非value入力を`irrelevant`と誤記したrecordを排除できない。許可入力0件、packet内witness、subject treatment、violated predicate、direct conflict、非value stateの表現自体については一般反例を得なかった。 |
| 8 | 一般反例あり | Finding F-01およびF-02。許可入力の集合外脱落と、集合内非value入力の根拠なし`irrelevant`分類の双方により、outcome-sensitiveな非value入力を含む`no_counterexample_found`がrootの機械的受入条件を通り得る。 |
| 9 | 一般反例なし | `unavailable`は、原因input identityと具体的反例predicate、またはterminalを変え得る不足identityのいずれかを要求する。open domain、未来instance未列挙、一般的不確実性、review回数、探索未完了だけでの形成を明示的に禁止している。 |
| 10 | 一般反例なし | review admissionとreview judgementは別operationで別producerへbindされる。`not_admitted`ではreview operation自体を作らず、admitted producerの変更、同一judgementの再割当て、rootによる意味再判定・補完・terminal変換を禁止している。 |
| 11 | 一般反例なし | 開始条件をCandidate147の`implementation_bound=true`に限定し、追加境界は対応subjectの未発行変更だけへ効果を及ぼす。別subject、read-only operation、別required outcomeまたはtask全体へ停止効果を伝播させず、permission、producer、terminal resultもCandidate147から置換していない。 |
| 12 | 一般反例なし | 設計はtool、file、schema、read順、review回数、worker数、runtimeおよび外部executorを固定しないと明記し、これらを解決条件にする変換も禁止している。 |

## finding record

### F-01: 許可入力全集合の外部coverageを証明せず、自己申告集合だけでdomain一致が閉じる

- 関連criterion: 6、8
- 再現可能な入力または状態: あるsubjectについてpermission内でreviewへ渡せる入力identityが`A`と`B`であり、`B`のstateが別の許可値なら具体的反例の成立が変わるとする。packet形成側が`allowed_review_input_identity_set={A}`だけを固定し、state mapとclassification mapのdomainも`{A}`にする。`A`には反例がなく、分類を`irrelevant`にする。
- 設計が要求する処理: packet発行前にはstate mapのdomainをpacketへbindされた`allowed_review_input_identity_set`と一致させ、terminalではstate map、classification map、同集合の三者一致をrootが機械的に確認する。提示状態では三者とも`{A}`で一致し、`B`はどのdomainにも現れないため、構造上は`no_counterexample_found`の受入条件を満たす。
- 違反するpredicateまたはconstraint: 「permission内で当該subjectの判断へ渡せる入力identity全集合」を固定すること、および`review_input_state_map.domain == input_effect_class_map.domain == allowed_review_input_identity_set`が許可入力全集合を覆ること。`B`がoutcome-sensitiveである以上、`B`を原因identityとして`unavailable`へ閉じなければならない。
- 直接矛盾: 設計が全許可入力の判断効果をterminal recordへ閉じるとする一方、受入判定はpacket形成側が選んだ集合の内部整合しか確認せず、許可された`B`の脱落を許したまま`no_counterexample_found`をadmitできる。
- なぜ既存条項で閉じないか: 「全集合を固定する」という規範文はあるが、permissionから導かれる許可入力identity domain、集合のcoverage result、またはそのdependencyをpacket identityとroot受入条件へbindしていない。rootはpacketへbind済みの集合だけを確認し、packet外の意味や入力を再判定しないため、`B`の欠落を検出する既存fieldがない。

### F-02: `irrelevant`分類の成立根拠がterminal recordに残らず、outcome-sensitiveな非value入力を誤分類できる

- 関連criterion: 7、8
- 再現可能な入力または状態: 完全な許可入力集合を`{A,B}`とし、`A=value(a)`が具体的反例を直接成立させ、`B=missing(B)`とする。`B`の許可値によって同じsubjectの処遇または直接矛盾が変わり得るので、本来の分類は`outcome_sensitive`である。review producerが`A=counterexample_support`、`B=irrelevant`と記録する場合と、両方を`irrelevant`と記録して`no_counterexample_found`を返す場合を考える。
- 設計が要求する処理: `irrelevant`は、当該inputの許可値が変わってもterminal judgementが変わらないことを受領済みpredicateから直接bindできる場合だけ成立する。正しい処理では`B`を`outcome_sensitive`とし、原因identityと具体的反例predicateを持つ`unavailable`へ閉じる。
- 違反するpredicateまたはconstraint: `missing / unreadable / terminal_failure`を値がないことだけで`irrelevant`にしないこと、値により反例成立が変わるinputを`outcome_sensitive`にすること、`counterexample_found`と`no_counterexample_found`で`outcome_sensitive=0`を要求すること。
- 直接矛盾: `B`は実質的にはoutcome-sensitiveなのに、分類map上のlabelだけを`irrelevant`にすれば、`counterexample_found`では非空support setと表面上の`outcome_sensitive=0`を、`no_counterexample_found`では全非value入力が表面上`irrelevant`であることを満たせる。
- なぜ既存条項で閉じないか: terminal recordとreview record basisはinput classification自体を保持するが、`irrelevant`を直接成立させたpredicate identity、そのpredicateの受領済みresult、またはinput値変化に対するterminal不変性のmachine-bound resultを必須fieldにしていない。rootは分類の正しさやmissingの関連性を再判定しないと明記されているため、誤分類を構造的に拒否できない。禁止変換7と8は規範を再記述するだけで、この欠落したdependencyを受入条件へ追加しない。

## terminalとCandidate作成gateへの効果

- terminal: `counterexample_found`
- finding件数: 2件
- Candidate作成gate: 不通過。設計本文の規則に従い、一般反例を解消した別identityの設計を、別identityの独立producerが全criterionについて`no_counterexample_found`と判定するまでCandidateを作成しない。
- 効果範囲: この判定は対象設計からCandidateを作成する未発行operationだけを停止する。Candidate147、別subject、read-only operation、採用、releaseまたはprojectionの状態を変更しない。
