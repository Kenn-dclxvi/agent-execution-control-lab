# review制御再構成の方向レビュー

> **現在解釈**: 初回10責務の方向レビュー完了後、Candidate192の発行遷移失敗に限定した再開M3を追記済み

> **位置づけ**: M3固定成果物／M2修正反映済み／M4への入力

## 結論

M2責務設計の初稿に対し、target、permission、methodまたはstop conditionを変える具体的反例が5件成立した。M2へ戻り、既存10責務を増やさず次を修正した。

1. review契約の適用可否をreview要否より前に固定する。
2. aggregate failure下の個別observation resultは、result contractが有効性を明示する場合だけadmitする。
3. terminal review resultのdependency変更後は同operationを再開せず、新operation identityを要求する。
4. finite direct matchは既存machine-bound resultだけで全effectとrelationを照合できる場合に限定する。
5. 保存済みreview resultのadmissionと、新規review execution permissionを分離する。

修正版を同じ8条件で再確認し、未解決のblocking counterexampleは0件となった。残る不確実性はprompt実行時の安定性であり、M5〜M7のmechanism predicateとして検証できる。新しいschema、registry、locator、review workerまたは比較系列を追加する必要はない。

M3を`complete`とし、次に許可されるのはM4のCandidate実装である。ただし本reviewはCandidate作成、評価実施、採用、releaseまたはprojectionを許可するものではない。

## Candidate189 M5後の再開注記

ADR07 iteration 5で、真正なcurrent `no_counterexample_found`へsaved prior result専用`result_use_permission`を要求する具体的反例が成立した。初回M3-F05は「saved prior resultを新規review execution permission否定で棄却しない」ことを狙ったが、result admission共通predicateへ利用permissionを置いたためcurrent resultまで巻き込んだ。

修正は責務を増やさず、`RESULT_ADMISSION`内を`current_review_result_admissible`と`prior_review_result_admissible`へ分ける。current resultはbind済みexecution permissionと真正性証拠で閉じ、prior resultだけへ`result_use_permission`と`result_still_valid`を要求する。これによりM3-F05のsaved result経路を保持しつつ、Candidate189失敗経路を閉じる。

修正版を次の具体的状態で再確認した。

| 状態 | 修正版の導出 | 判定 |
|---|---|---|
| current reviewが許可され、真正な`no_counterexample_found`を返す | execution permission、current operation identity、producer、sender、observation、certificateでadmitし、別利用permissionを要求しない | Candidate189失敗経路を閉じる |
| 新規reviewは禁止だがadmissibleなsaved prior resultがある | prior predicateだけが`result_use_permission`と`result_still_valid`を確認し、新規execution permissionを要求しない | 初回M3-F05を保持 |
| 新規reviewは禁止でsaved prior resultもない | current resultは存在せず、外側admissionを`unavailable`へ閉じる | ADR08経路を保持 |
| current result terminal後にobservation dependencyが変わる | current predicateの`authenticかつcurrent`がfalseになり、`RESULT_EFFECT`が旧resultを失効する | stale replayを許さない |

4状態で未解決blocking counterexampleは0件だった。責務、schema、registry、producer roleまたは比較系列は増やしていない。再開M3を`complete`とする。このreviewは次Candidateの実装一致または試験成功を証明せず、新identity実装は未実施である。

## review operation

- operation identity: `review-control-reconstruction-m3-direction-review`
- producer: root
- criterion: M2責務設計を一般入力で成立不能にし、target、permission、methodまたはstop conditionの変更を必要とする具体的反例があるか
- pass condition: 全確認条件で、反例が不成立または同じ10責務内の修正によって解消し、未解決blocking findingが0件
- allowed input: M1因果分析、M2責務設計、C147原文、prompt制御原則、ADR9 r2設計r11、保存済みCandidate resultの原因分析
- forbidden input: 新Candidate本文、評価後に作る修正案、新規oracle、未保存の期待run
- artifact変更permission: M2責務設計、マイルストーン計画、本reviewおよび索引だけ

M3計画は独立execution identityを必須条件にしていないため、別producerは起動していない。完全性はこのreviewで主張せず、試験へ委譲する。

## 初回finding

### M3-F01: review契約のない通常変更へのspillover

- 具体的状態: Standard14の通常実装でC147の`implementation_bound=true`は成立するが、authorityが全effectを有限列挙していない。TaskSpecは独立review criterionまたはreview resultをrequired outcomeにしていない。
- 初稿の処理: `finite_direct_match=false`だけで`review_requirement=required`となり、独立reviewを新設する。
- 破る境界: criterion owner文字列だけでproducerを起動しないC147の最短正常経路と、Standard14のroot-only経路。
- 判定: `counterexample_found`。
- 修正: `review_control_applicable`を追加し、TaskSpecまたは適用中authorityがcriterion、allowed result kind、consumer、independenceを直接固定したsubjectだけへ本設計を適用する。非適用は`not_applicable`としてC147へ委譲する。

### M3-F02: aggregate failure下の部分result

- 具体的状態: 一つのstructured invocationがatom Aの`value`とatom Bの`missing`を個別表示し、同時にinvocation-level non-successを返す。表示されたAがaggregate failure後もauthoritativeかはtool contractにない。
- 初稿の処理: 個別stateが見えることからAをadmitする読み方と、aggregate failureから全atomを`terminal_failure`にする読み方が両立する。
- 破る境界: observation result真正性。
- 判定: `counterexample_found`。
- 修正: `invocation result contract identity`をatomへ加え、aggregate non-success下でもper-item successを保持すると適用中contractが固定する場合だけ統合を許す。未固定なら別invocationを要求する。

### M3-F03: terminal resultのdependency変更

- 具体的状態: reviewerが`counterexample_found`を返してreview operationがterminalになった後、certificate内のapplicability入力だけが新しい許可resultで変わる。
- 初稿の処理: result失効は定義されていたが、terminal review operationを再開するか、同identityでresultを置換するか、新identityへ移るかが未固定だった。
- 破る境界: 一operation一producer terminal resultと不変履歴。
- 判定: `counterexample_found`。
- 修正: terminal operationを再開しない。同じcriterionを再判定する場合は新しいreview operation、packet、producer、result identityを形成する。TaskSpecが再reviewを禁じる場合は外側operationを固定stopへ閉じる。

### M3-F04: finite relationの非機械的照合

- 具体的状態: authorityは二targetと各end stateを閉じるが、両者の保持relationは自然言語だけで、bind済み変更predicateとの一致に一般設計判断が必要である。
- 初稿の処理: authorityがrelationを「直接固定」したという記述だけで`finite_direct_match=true`にできる。
- 破る境界: finite closureとopen reviewの分離。
- 判定: `counterexample_found`。
- 修正: 既存machine-bound resultだけで全effect、constraint、relationの同一性を確認できる場合だけfinite direct matchとする。non-machine照合が必要ならreview contract適用下では`required`とする。

### M3-F05: 保存済みresultと新規review permission

- 具体的状態: current subject、criterion、packet basis、producer、dependencyへ完全一致し、利用permissionも許可されたadmissibleな保存済み`no_counterexample_found`がある一方、TaskSpecは新しいreview executionだけを禁止する。
- 初稿の処理: `review_execution_permission=denied`により保存済みresultも使わず外側operationを`unavailable`にする。
- 破る境界: 確定済みresultを明示失効なしに再び問題にしない境界。
- 判定: `counterexample_found`。
- 修正: 保存result admissionと`result_use_permission`を新規review execution permissionより前に判定する。activeなadmitted resultがあれば新reviewを作らず利用し、新規実行permission否定はそれを失効させない。

## 修正版の8条件再確認

| 条件 | 修正版での導出 | 再review result |
|---|---|---|
| 一atomがwitness applicabilityとclosureの両方へ依存 | `counterexample_found`は実際のcertificate dependency、`no_counterexample_found`は全scopeを持つため、同じatomでもresult別に効果が分かれる | `no_counterexample_found` |
| per-item stateとaggregate failureが併存 | result contractがper-item validityを固定する場合だけ統合し、なければ別invocation | `no_counterexample_found` |
| certificate dependencyがterminal後に変化 | 旧resultを失効し、必要なら新review operation identityへ移る。同operationを再開しない | `no_counterexample_found` |
| finite effectのrelationだけ非機械的 | `finite_direct_match=false`となり、review contract適用下では`required` | `no_counterexample_found` |
| 新規review禁止とadmissible prior resultが併存 | prior resultを先にadmitし、新規reviewを作らずresult effectへ進む | `no_counterexample_found` |
| coupled subjectsの一つが`counterexample_found` | 全subject allowとrelation保持が揃わないためinvocationを発行せず、分離不能ならimplementation choiceを失効 | `no_counterexample_found` |
| target identity未固定と、固定targetの`missing` | 前者はpacket unavailable、後者はpacket readyかつobservation `missing`としてreviewerへ渡る | `no_counterexample_found` |
| review契約のない通常変更でdirect match不成立 | `review_requirement=not_applicable`としてC147既存経路へ委譲し、reviewを新設しない | `no_counterexample_found` |

## terminal導出の再確認

### 有限閉包

review contractが適用され、既存machine-bound resultで全effectとrelationが一致する場合だけ`not_required`となる。permission、packet、review producerを作らず、C147の変更・validation経路へ進む。

### 具体的反例

reviewerがwitness、applicability、規範predicate、直接矛盾、一般設計変更効果を実observation resultへbindする。certificate外missingはresultを失効せず、artifact変更は対応subjectだけで禁止される。

### 反例なし

発行時に固定したreview scopeとmanifest全atomのauthenticな`value`を必要とする。未来全域の不存在は要求せず、activeな保存済みresultも同じdependency照合で利用できる。

### 判断依存入力不足

identity固定済みtargetの`missing`はpacketを不成立にせずreviewerへ渡す。そのatomがclosureまたはwitness applicability dependencyならreviewerが`unavailable`を形成する。

### permission否定

activeかつ利用許可済みのadmitted prior resultがない場合だけ、新規review execution permission否定によりreview一式を作らず外側admissionが`unavailable`となる。rootはreviewer resultを代行しない。

## 残余リスクと試験対応

| 残余リスク | 後続で確認するpredicate |
|---|---|
| finite direct matchが不安定で不要reviewを起動する | ADR01、ADR02のreviewer 0件 |
| review contract適用済みなのにrequired reviewを省略する | ADR03〜ADR07、ADR09のbound reviewer各1件 |
| concrete witnessと無関係missingを再びaggregateする | ADR05のobservation atom、certificate dependency、`blocked` |
| semantic inputへ禁止履歴を混ぜる | ADR06のcanary配送0件 |
| fixed manifest未完了で反例なしをadmitする | ADR09の`no_counterexample_found`受入0件、変更0件 |
| review契約のない通常変更へreviewがspilloverする | Standard14全14ケースのproducer route |
| result失効を別subjectまたはtask全体へ広げる | ADR9全ケースのsubject-local effect監査 |
| method failure、target missing、permission denialを混同する | ADR08、ADR09と高リスク拡張のstate監査 |

これらは設計方向を未確定にする反例ではなく、固定設計を実行時に安定して選べるかという試験predicateである。

## M3完了判定

- 初回blocking counterexample 5件をM2へ返し、同じ10責務内で修正した。
- 修正版を8条件で再確認し、未解決blocking counterexampleは0件となった。
- review target、permission、method、stop conditionは修正版へ固定した。
- 残余リスクをADR9およびStandard14のmechanism predicateへ対応させた。
- review反復でschema、registry、locator、producer roleまたは比較系列を増やしていない。

この成果物の初回固定時点は`M1_complete / M2_complete / M3_complete / M4_not_started`とする。後続の現在位置は[`review制御再構成マイルストーン計画`](review-control-reconstruction-milestone-plan.md)を正とする。

## Candidate192後の発行遷移限定レビュー

### 対象と境界

Candidate192の保存traceで否定されたのはreview terminal設計ではなく、発行集合の論理判定を実際のmodel responseへ拘束する仮定である。再開M3は、改訂した[`責務設計`](review-control-reconstruction-responsibility-design.md)の`DISPATCH_TRANSITION`が一般入力で成立不能となり、target、permission、methodまたはstop conditionの変更を必要とする具体的反例だけを確認した。

直接基盤はCandidate191とし、C192の`DISPATCH_ADMISSION`本文は設計入力にしない。C192からはconsumer、dependency、個別result contract、真正dependency非越境および次の保存反例だけを使った。

- A01のconsumerなし開始identity 2 / 5
- 共同発行対象8ケースのidentity/read同一step 1 / 40
- 退行9ケースの追加変更前roundなし 4 / 45
- 共同発行3件中1件のcompound result

### 方向を変える反例の確認

| 状態 | 改訂設計の導出 | 判定 |
|---|---|---|
| required outcome未固定でclarificationだけがterminal。TaskSpecに開始identityはあるが、そのresultを消費するoperationがない | `dispatch_candidate=false`となりfrontierは空。現在responseのtool callを0件にして`no_dispatch`とする | 反例不成立 |
| identity drift時にartifact変更は禁止されるが、固定済みreadのtarget、permission、methodおよびresult contractは変わらない | identity確認とreadに相互predecessorがないため同じfrontierへ入り、現在responseから個別tool callで全件発行する | 反例不成立 |
| identity drift時にread自体が禁止される、またはread targetが変わる | identity resultをreadの`dispatch_predecessor`へ固定し、identityだけを先行cycleへ置く。安全性のための別stepを退行扱いにしない | 反例不成立 |
| ready invocation数が明示された同時発行上限を超える | 上限とoperation specificationの固定順序で現在frontierを一意に切り、frontier全件を同一responseから発行する。result受領後の便宜的選び直しを許さない | 反例不成立 |
| 同じfrontierの一commandがfailed、他commandがsuccess | 個別tool callとmachine-bound resultを保持し、failed resultはそのconsumerだけへ効く。success済みresultをaggregate failureで失効しない | 反例不成立 |
| 一tool callがcell ID付きnonterminal resultを返す | dispatch cycleを未収集のまま保持し、同じcell IDへのwait以外を発行しない。別invocationの完了だけでcycle terminalにしない | 反例不成立 |
| producerがfrontierの一部だけを発行し、残りを次responseへ送ろうとする | 現在responseのtool-call identity集合がfrontierと一致しないため`dispatch_transition_terminal=false`。部分発行resultを正しいdispatch completionへ昇格できない | 反例不成立 |
| producerが同時発行を一つのshell compound commandで代用する | frontier identityとtool-call identityが一対一一致せず、個別result contractも欠くため遷移不成立 | 反例不成立 |

### 結論

未解決blocking counterexampleは0件である。C192の判定軸だけを残し、次の3段階を一つの`dispatch_transition_terminal`へ閉じたことで、C192の「判定は成立するが挙動が変わらない」という経路を設計上は閉じた。

1. consumerを持つ候補と未解決predecessorからfrontierを固定する。
2. 現在model responseの個別tool-call集合をfrontierへ一対一bindする。
3. 全result受領まで判断を再開せず、各resultを元consumerへbindする。

review適用、`OWNER_ROLE`、current/prior result admission、terminal kind、artifact変更permissionおよびvalidationは変更していない。新しいschema、registry、producer role、result kindまたは比較系列も追加していない。完全性と選択安定性は試験で確認し、本reviewの成功をCandidate実装または評価成功へ一般化しない。

再開M3の状態は`dispatch_transition_direction_review_complete / blocking_counterexample_zero / next_candidate_not_created`とする。

## Candidate193評価後の訂正

Candidate193 ADR9 r2 N=5は、上記レビューが見落とした具体的反例を実測した。全9ケースで開始identity不一致時には後続read自体を停止するため、identity resultはreadの発行可否を変える。それにもかかわらず28 / 45件でidentityとreadが同じmodel stepから発行され、正しい初回frontierは17 / 45件だけだった。

同じ新基準でCandidate191の保存45件を再集計すると越境36件、正しい分離9件だった。Candidate193は直接親に対して正しい分離を8件増やしているため、発行遷移が無作用だったとはいえない。一方、ケース内で挙動が変動し、ADR05・ADR06では計3件悪化した。したがって、論理判定と実挙動を同じterminal名へ入れれば分離不能になるという上記の十分性結論だけを撤回する。各primitiveの有効性まで一括棄却しない。

consumer、真正dependency、個別result contract、compound command禁止は方向を変えない安全境界として残す。`dispatch_candidate`、`dispatch_predecessor`、`dispatch_frontier`、独立条項化およびCandidate193を次の親にするかは保留する。捨てるのは、`dispatch_transition_terminal`という自己宣言だけで現在responseのtool-call選択を一意に強制できるという仮定である。現在状態は`candidate193_counterexample_found / dispatch_transition_sufficiency_rejected / primitives_pending / M1_reopened`とする。
