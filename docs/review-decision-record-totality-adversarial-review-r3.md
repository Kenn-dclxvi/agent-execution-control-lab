# review decision record全域性設計の実装前敵対的review r3

## review identityと入力封鎖

- producer identity: `review_decision_record_design_review_r3`
- 対象設計: `docs/review-decision-record-totality-design.md`
- 固定した対象SHA-256: `1753b9261fa49b95dad0b314551a1943a07118d5ba7acf4803d3041d5f044f3b`
- 開始時照合結果: 一致
- review種別: 情報封鎖された独立の実装前敵対的review

判定には、Candidate147原文、`docs/prompt-control-design-principles.md`、対象設計、および対象設計と作成先へ適用されるルートと`docs/`の`AGENTS.md`だけを使用した。後続Candidate本文、評価case、fixture、oracle、rating、raw trace、過去review artifactまたはfinding、期待terminal、修正案、会話履歴、その他のrepository artifactは入力にしていない。この判断を別producerへ再委譲していない。

## 結論

terminalは`counterexample_found`である。一般反例は1件であり、Candidate作成へは進めない。

## criterion別判定

1. **成立** — 一つの`review_subject`をCandidate147が`implementation_bound`へbindした一つの変更predicateとし、複数target等を理由に分割せず、複数predicateの場合だけsubjectを分けている。
2. **不成立** — 有限固定効果だけを選んだ場合のoccurrence graphでは重複数、identityと値、順序または依存、およびextra ruleを照合する。しかし、一つの変更predicateに有限固定効果とopen class効果が併存する場合、設計はgraphまたはbasisの二者択一しか要求せず、subjectの全効果が選択した表現へ収まったことを要求しない。finding F-01を参照する。
3. **成立** — occurrence graphへ入ったnodeについては、target、precondition、transformまたはend state、およびconstraintのidentityとbind済み値をともに比較し、一対一対応の意味差を一致として扱えない。
4. **成立** — 有限固定効果が全式を満たす場合は`matched / not_required`となり、manifest、packetまたはreviewerを要求しない。
5. **成立** — open classの`matched`には、現在のbasis、class predicate domain、決定的変換、全constraint binding、およびterminal successに一致するmachine-bound保持resultを要求し、sample、列挙済みinstance、部分集合、別versionを除外している。ただし、同じsubjectに併存する有限固定効果のcoverage欠落はcriterion 2のfindingで扱う。
6. **成立** — `missing / unreadable / terminal_failure`をterminal input stateとして許容し、allowed identity set、state map domain、classification map domainの完全一致と全identityの単一分類を要求している。
7. **成立** — `counterexample_found`にはwitness、subjectの出力または処遇、違反predicate identity、直接矛盾、および全`counterexample_support`入力のstate全体を持つsupport setを要求し、非value stateを値へ変換しない。
8. **成立** — 非value入力を不在だけで`irrelevant`にすることを禁じ、値により反例の成立・不成立が変わり得る場合は`outcome_sensitive`とし、`outcome_sensitive`が一件でもあれば`no_counterexample_found`を認めない。
9. **成立** — `unavailable`には、原因input identityと具体的反例predicate、terminalを変え得る不足identity、またはpermission denial／独立producer bind不能の原因identityのいずれかを要求し、一般的不確実性、未来instance未列挙、review回数または探索未完了だけでは成立させない。
10. **成立** — rootは機械的coverageだけを確認し、意味、分類、欠落fieldまたはterminalを補完しない。不完全recordをterminalへ変換せず、同じjudgementをrootまたは別producerへ再割当てしない。同一subjectで`not_required`とreviewも併存しない。
11. **成立** — 追加結果の効果は対応subjectの未発行変更へ限定され、別subject、read-only operation、別required outcomeまたはtask全体へ伝播しない。既存のoperation identity、permission、producer terminal resultおよびCandidate147の変更predicate単位を置換していない。
12. **成立** — 論理recordの必須関係は定めるが、実装するtool、file、機械schema、read順、review回数、worker数、runtimeまたは外部executorを解決条件として固定していない。

## finding record

### F-01: 混合effect subjectをgraphまたはbasisの一方だけで`matched`にできる

- 対応criterion: 2
- 再現可能な入力／状態: Candidate147が一つの`implementation_bound`変更predicateとして、有限固定target `config.mode`を値`strict`へ変更するatomic effectと、現在のclass predicate `generated_file`を満たす全instanceへ決定的変換`normalize_header`を適用するopen class effectを同時にbindしている。authorityも同じ一predicateで両effectと各constraintを固定している。implementationはopen class effectとそのconstraintを正しく実装する一方、有限固定effectでは`config.mode=permissive`を実装している。
- 設計が要求する処理: subjectは一predicateなので分割しない。固定順序3は、authorityと変更predicateからfinite effect occurrence graph **または** open class effect basisをbindする。open class経路を選ぶと、現在basisの全classを覆うmachine-bound保持resultがterminal successであり、式のbasis、domain、transform、constraintが一致すれば`matched`となる。
- 違反するpredicate／constraint: `matched`は一つのreview subjectにbindされた変更predicateの全change effectと保持constraintがauthorityに対応する場合だけ成立しなければならない。しかし再現状態では、有限固定effectの`config.mode=strict`というauthority bindingと`config.mode=permissive`というimplementation bindingが不一致である。それでもopen class式だけは全件成立し、subject全体を`matched / not_required`としてadmitできる。
- 既存条項で閉じない理由: subject分割禁止により有限部分を別subjectへ送れない。open class basisは一つのclass predicate、definition、version、deterministic transform、constraint集合だけを持ち、同一predicateに併存する有限occurrence graphまたはそのcoverageをfieldとして持たない。`extra_effect_rule_state`は有限effect経路にだけ定義され、open class経路の`open_class_matched`式には現れない。固定順序にも、選んだgraphまたはbasisがsubject内の全effectを漏れなくpartitionしたことを示すcoverage predicateがない。このため、後段のdomain一致、review record、root受入境界および失効規則は、review自体が不要とされた有限部分の不一致を検出できない。

## terminal record

- terminal: `counterexample_found`
- finding件数: 1
- witness input/state: 一つの`implementation_bound`変更predicateが、有限固定effectとopen class effectを同時に含み、open class部分だけがauthorityと一致する状態
- subject output/treatment: open class basisの式だけでsubject全体を`matched / not_required`として個別admitする
- violated predicate identity: criterion 2「finite fixed effectのoccurrence graphとextra rule stateが重複数および順序依存を含め全域的か」
- direct conflict: subject内の有限固定effectがauthorityと不一致であるのに、選択したopen class representationがそのeffectを表現・照合しないままsubject全体をreview不要にする
- counterexample support set: `{mixed_effect_subject_state}`。`mixed_effect_subject_state`はF-01の再現可能な入力／状態に記録したvalue state全体へbindする。

## Candidate作成gateへの効果

一般反例が一件成立したため、対象設計のままCandidateを作成してはならない。対象設計を修正し、別identityの情報封鎖された独立producerが全criterionを再reviewして`no_counterexample_found`を返すまで、Candidate作成gateは閉じたままとする。このreviewは設計、Candidate、評価、採用、releaseまたはprojectionの状態を変更しない。
