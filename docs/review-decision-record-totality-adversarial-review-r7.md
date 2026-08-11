# review decision record全域性設計の実装前敵対的review r7

## 判定

- producer identity: `review_decision_record_design_review_r7`
- 対象設計: `docs/review-decision-record-totality-design.md`
- 固定した対象SHA-256: `fe81b56ffc73363c363038bbe6bd6b47d5ad8fe3f52c304a786a776ee23e1ed1`
- 開始時の照合結果: 一致
- terminal: `counterexample_found`
- finding件数: 1件
- Candidate作成gateへの効果: 不通過。設計を修正し、別identityの独立producerによる全criterionの再reviewが`no_counterexample_found`で終端するまでCandidateを作成しない。

## 入力封鎖

このreviewは、固定されたproducer identityにより、次の入力だけを用いて実施した。

1. Candidate147原文 `prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt`
2. `docs/prompt-control-design-principles.md`
3. `docs/review-decision-record-totality-design.md`
4. 上記入力と本成果物へ適用されるrepository rootの`AGENTS.md`および`docs/AGENTS.md`

Candidate185を含む後続Candidate本文、評価case、fixture、oracle、rating、raw trace、過去review artifactまたはfinding、期待terminal、修正案、会話履歴、その他のrepository artifactは入力にしていない。この判断を他producerへ再委譲していない。

## criterion別判定

1. **一般反例なし。** `implementation_bound=true`を開始条件とし、Candidate147が一つの実行可能な変更predicateとしてbindしたidentityを一つの`review_subject`にしている。複数targetやartifact間relationを含んでもpredicateを分割せず、複数predicateが個別bindされた場合だけsubjectを分けるため、operation identityを横断したsubject合成は要求していない。
2. **一般反例なし。** authority側とimplementation側の全change effect identityについて非重複和集合によるcoverageを個別に要求し、finite、0個以上のopen class component、両者の混合および複数open classを同じ合成式へ閉じている。component間edge、共有constraintのdependency set、evaluation stageおよびopen classを含む共有constraintの全組合せ保持resultも合成条件に含まれる。
3. **一般反例なし。** finite occurrenceは重複数とoccurrence identityを保持し、対応nodeのtarget、precondition、transformまたはend state、constraintをidentityとbound valueの双方で照合する。必要なorderまたはdependency edgeも照合対象であり、自然言語上の類似や現在値だけによる一致を許していない。
4. **一般反例なし。** finite-onlyの全対応、relation、constraint、coverageおよびextra effect rule不在が成立すれば`matched / not_required`となり、manifest、packetまたはreviewerを要求せず変更predicateを個別にadmit可能としている。
5. **一般反例なし。** open class componentを`matched`にするには、現在の`open_class_basis`、現在class predicateの全domain、決定的変換、component-local constraintおよびterminal successへbindされたmachine-bound resultを要求する。sample、列挙済みinstance、部分集合、別versionを代用できない。
6. **一般反例なし。** 許可入力identity全集合と`review_input_state_map`のdomainが一致しないpacketを発行せず、`missing / unreadable / terminal_failure`をterminal input stateとして保持する。全terminalの受入時にもstate mapとclassification mapのdomain完全一致を共通条件としている。
7. **一般反例あり。** finding `F-R7-01`のとおり、packetへ固定されるTaskSpec、subject、authority、保持constraintと`allowed_review_input_identity_set`の包含関係が要求されていない。許可入力集合が空で、packet basisだけから直接矛盾が成立する状態では、packet内の反例であってもwitnessと非空support setを形成できず、`counterexample_found`へ閉じない。
8. **一般反例なし。** `irrelevant`は入力の許可値が変わってもterminal judgementが変わらないことを受領済みpredicateから直接bindできる場合に限定される。非valueであることだけによる`irrelevant`化を禁止し、`no_counterexample_found`は全非value入力の`irrelevant`と`outcome_sensitive=0`を要求する。
9. **一般反例なし。** `unavailable`は、原因input identityと成立可否が変わり得る具体的反例predicate、またはterminalを変え得る不足identityのいずれかを要求する。open domain、未来instance未列挙、一般的不確実性、review回数または探索未完了だけでは形成できない。
10. **一般反例なし。** review admissionとreview judgementは別operation、別producer terminalとして形成される。`not_admitted`ではreview operation自体を作らず、admitted producer以外へのjudgement再割当て、rootによる意味再判定、不完全recordのterminal化を禁止している。
11. **一般反例なし。** 追加resultの効果は対応subjectを含む未発行変更だけへ限定される。別subject、read-only operation、別required outcomeまたはtask全体へ伝播させず、Candidate147のpermission、producer terminalおよび`result_effect_scope`を置換していない。
12. **一般反例なし。** 設計はtool、file、schema、read順、review回数、worker数または外部runtimeを解決条件として固定せず、それらの固定を明示的に禁止している。

## finding record

### F-R7-01: packet basisだけで成立する反例を非空support setへ写せない

- 対応criterion: 7
- 再現可能な入力と状態:
  1. Candidate147の一つの変更predicate `P`について`implementation_bound=true`である。
  2. authorityはtarget `A`をend state `S`にすることを要求するが、implementation choiceのsubject treatmentはtarget `B`をend state `S`にし、`A`を変更しない。authorityとimplementationのeffect graphは具体的に`unmatched`となり、reviewが必要である。
  3. review admissionは独立producer `R`をbindして`admitted(R)`で終端する。
  4. packet identityにはTaskSpec、authority、implementation choice、subject、保持constraintおよびreview criterionが固定される。一方、これらpacket basis identityを`allowed_review_input_identity_set`へ含める条項はない。permission内で追加して渡せるrepository evidenceがない状態として、`allowed_review_input_identity_set = {}`、`review_input_state_map = {}`をbindする。両domainは完全一致するためpacket発行条件を満たす。
- 設計が要求する処理: reviewerは許可入力全集合を分類して排他的terminalを一つ返す。上記subject treatmentは、packet内authorityの「target `A`をend state `S`にする」というpredicateと直接矛盾するため、具体的反例として扱われなければならない。
- 違反するpredicateまたはconstraint: `counterexample_found`はwitnessを`allowed_review_input_identity_set`所属identityに限定し、`counterexample_support_set`を非空かつwitness dependency全件包含にする。しかし許可入力集合が空なので、packet内のsubject、authorityおよび直接矛盾をrecord dependencyに使えても、witnessもsupportも一件も形成できない。これにより、packet内witness、subject treatment、violated predicate、direct conflictおよび非空support setを全件bindして具体的反例をterminalへ閉じるというcriterion 7を満たさない。
- terminal全域が失われる理由: `counterexample_found`は空集合から非空support setを形成できない。`no_counterexample_found`はpacket basis上ですでに具体的反例が成立しているため返せない。`unavailable`も、`outcome_sensitive`なinput、値によって成立可否が変わる具体的反例predicate、または受領済みinputに対応づけられないterminal-changingな不足identityが存在しないため返せない。したがってreview operationは三terminalのどれにも閉じずnonterminalのまま残る。
- 既存条項で閉じない理由: state mapとclassification mapのdomain一致は空集合同士でも成立する。packet basisを`allowed_review_input_identity_set`へ必ず含める条件、またはpacket basisだけで成立する反例をsupportへ写す条件はない。`record_dependency_identity_set`がTaskSpec、subject、authorityおよび保持constraintを含められることは、witnessとsupport setが許可入力identityに限定される別条件を満たさない。rootは欠落要素を補完できず、不完全recordを`unavailable`へ変換することも禁止されているため、後段でも閉じない。

## terminal

`counterexample_found`

一般反例は1件である。criterion 7が不通過であるため、現在の設計からCandidate作成へ進めない。
