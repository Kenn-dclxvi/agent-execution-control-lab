# 次期review terminal proof設計のための原因分析

> 状態: `analysis_complete / design_not_started / candidate_not_created`

## 結論

Candidate186の主因は、reviewへ渡した全入力の存在と、terminalを成立させる証明依存関係を同一視したことである。全入力identityと各入力stateをpacketへ保存することは必要だが、全入力について同じ強さの反実仮想証明を要求してはならない。

`counterexample_found`は具体的な一反例が成立すれば閉じる存在証明である。`no_counterexample_found`は対象domain全体の閉包を必要とする全域証明である。Candidate186は前者にも後者と同じ全域性を要求したため、成立済み反例と無関係なmissingを`outcome_sensitive`として過剰停止した。逆にCandidate185は後者の閉包を弱く扱い、judgement-relevantなmissingがあるまま反例なしを受け入れた。

次の設計ではCandidate186を継承しない。Candidate147を直接基盤とし、後続Candidateからは観測事実だけを使う。追加候補は、全入力分類ではなくterminalごとに異なる`proof obligation`と、その結論を成立させる最小dependency certificateである。

## 証拠範囲

- Candidate147: operation、producer、terminal、`implementation_bound`、`result_effect_scope`の直接基盤
- Candidate173 ADR9 r2: 45 / 45 Score 4。具体的反例を先に判定し、成立後の無関係なmissingで失効させない順序が成立した診断証拠
- Candidate185 ADR9 r2: Score `38 / 7`。missingをpacket stateとして配送できたが、反例なしの閉包が不足した診断証拠
- Candidate186 ADR9 r2: Score `27 / 18`。反例なしの危険な変更は止めたが、全域record要求が過剰停止へ転じた直接原因証拠

Candidate173、Candidate185、Candidate186の条項本文、schema、state名またはproducer構成は次設計へ継承しない。

## 18件の失敗分解

| 原因クラス | 件数 | 対象 | 観測 |
|---|---:|---|---|
| 有限固定効果への不要review | 5 | ADR01、ADR02 | authorityが閉じた変更なのにreviewを起動。ADR02の1件は後続recordのbasis表現不一致で`unavailable` |
| missingをpacket未完成とした起動前停止 | 3 | ADR03、ADR04、ADR09 | `missing`をterminal input stateとして配送せずreviewを作らなかった |
| 成立済み反例を無関係なmissingで失効 | 6 | ADR04、ADR06 | 具体的witnessと直接矛盾が揃っているのにpaired-scope missingを`outcome_sensitive`とした |
| readable入力の過剰な`outcome_sensitive`化 | 3 | ADR07 | 閉包証拠を含む全入力を判定不能要因として`unavailable`にした |
| 閉包証拠を無視した偽反例 | 1 | ADR07 | readableなpaired-scope証拠が閉じる範囲を無視してopen membership自体を反例にした |

失敗は別々の例外ではない。Candidate186の次の二条件が、存在証明を全域証明へ変えたことが中心原因である。

1. supportでない全入力へ、全許可値domainでterminal不変となる`irrelevant`証明を要求した。
2. `counterexample_found`にも、全入力が`counterexample_support | irrelevant`であり`outcome_sensitive=0`であることを要求した。

この組合せでは、既に一つの反例が立証済みでも、別入力のmissingについて全domain不変を証明できなければ`counterexample_found`を返せない。ADR04とADR06の6件はこの誤りで説明できる。

## 原因帰属の確度

原因は二層に分ける。

### 条件自体にある論理上の原因

ADR04とADR06の6件は、実行側が成立済みwitnessを認識しながら、別のmissingを`outcome_sensitive`として`counterexample_found`を形成不能にしたと明示している。これはCandidate186の`counterexample_found`形成条件が全入力の`outcome_sensitive=0`を要求したことと直接対応する。ここはpromptの長さだけでは説明せず、terminal proof obligationの仕様誤りとして扱える。

### 制御密度による追従不安定

missingをpacket未完成とした3件は、Candidate186自身が「non-value stateはpacketを未完成にしない」と明示した制御に反している。有限固定効果への不要review 5件も、`matched`とreviewの併存禁止に反する。したがって、この8件を上記の論理式だけへ帰属させない。

Candidate186は6条項でeffect partition、finite graph、open class、relation result、独立admission producer、4 domain一致、全input分類、terminal recordおよびresult再validationを同時に要求した。観測は、状態数、role数、前後関係および類似した完全性条件の密度が、明示済み禁止を安定して保持できない水準だった可能性と整合する。評価はprompt長だけを独立操作していないため、長さ単独の因果効果までは主張しない。

次設計はpredicateを修正するだけでなく、roleと中間stateを減らす必要がある。独立producerはTaskSpecが要求するreview judgementへ限定し、review admissionのための別worker、推論したcomponent graph、全入力の排他的分類mapは新設しない。

## 保持する成功と捨てる機構

### 保持する成功

- 許可された全input identityと`value | missing | unreadable | terminal_failure`のstateをpacketへ保存する。
- missing自体はpacket不完成を意味しない。
- `no_counterexample_found`は、対象domainと必須scopeの閉包証拠が揃わない限り受け入れない。
- permission denialではreview operationを作らず、対応subjectの変更だけを止める。
- admissibleなreview terminalの効果を対応する未発行変更へ限定する。
- rootはreviewerの意味判断を補完しない。

### 捨てる機構

- 全入力へ同じ三分類と同じ全domain不変証明を要求する方式
- `counterexample_found`へ`outcome_sensitive=0`を要求する方式
- terminal certificateの外にある入力まで意味上の`irrelevant`と証明する方式
- review admissionだけのために別の独立producerを必須化する方式
- authorityが明示列挙した有限入力domainへ追加のmachine enumerator成功を必須化する方式
- Candidate147がbindした一変更predicateを、推論したoccurrence graphやopen class componentへ再分解してreview要否を決める方式

## terminal別の正しい証明責務

| terminal | 証明形 | 必須certificate | certificate外入力の扱い |
|---|---|---|---|
| `not_required` | 閉じた有限対応 | authorityの直接閉包identity、変更predicate、全effect entryと保持relationの一対一対応 | 対応に必要な値が欠ければreview required。review後の入力は使わない |
| `counterexample_found` | 存在証明 | 具体的witness、適用する規範predicate、固定設計上の処遇、直接矛盾、一般設計を変えるeffect | witness certificateを無効化しない入力は結論へ不要。追加反例の有無は要求しない |
| `no_counterexample_found` | 全域証明 | review対象domain、必須scope、各観測のsuccess、反例predicateを閉じるclosure receipt | closure frontier上のmissing、unreadable、terminal failureは許可しない |
| `unavailable` | 未解決frontier証明 | 形成できない先行terminal、欠けたdependency identity、そのstate、値または成功でどのpredicateが閉じるか | 一般的不確実性やopen domainというlabelだけでは成立しない |

重要なのは、packet domainの全域性とterminal certificateのdependency集合を分けることである。

`packet_domain = 許可された全入力identity`

`terminal_dependency_set = 選択したterminalの証明に実際に必要なpacket atomの部分集合`

全packet atomは保存するが、terminal dependencyへ入っていないatomについて全値domainでの不変証明は要求しない。ただし、そのatomが選択済みcertificateのwitness適用性、direct conflictまたはclosureを無効化し得ると固定根拠から示される場合はdependencyへ入れる。

## 次設計の判定順序

一つのreview subjectについて、次の順序だけを許す。

1. Candidate147の`implementation_bound=true`へbind済みの一変更predicateをsubjectとする。
2. TaskSpecまたは適用中authorityが全effectと保持relationを直接閉じた有限集合として固定している場合だけ、同じbind済み値との一対一対応を確認する。
3. 直接対応が完全なら`not_required`とし、review admissionまたはreview operationを作らない。
4. 直接対応が完全でない、open boundaryへ依存する、または対応値が未固定ならreview requiredとする。未固定値を`not_required`へ補完しない。
5. permissionと独立review producerをbindし、明示manifestから全input identityと各stateを一つのpacketへ保存する。non-value stateだけを理由にpacketを未完成にしない。
6. reviewerはまず具体的counterexample certificateの形成可否を判定する。成立したcertificateは、そのcertificateのdependencyを変えない別入力のmissingで失効させない。
7. counterexample certificateが成立しない場合だけ、no-counterexample closure certificateを判定する。
8. closure certificateが成立せず、その原因dependencyと未解決predicateを固定できる場合だけ`unavailable`とする。
9. terminal certificateと現在basisが一致することだけをrootが機械的に確認し、対応subjectの未発行変更へ効果を適用する。

この順序は`counterexample_found > no_counterexample_found > unavailable`という結果の優先順位ではない。先に成立した存在証明は後続の全域探索を不要にする、という証明責務の包含関係である。具体的反例certificateが不成立なら、反例なしまたは利用不能を続けて判定する。

## 有限固定効果の扱い

ADR01とADR02の修復に、Candidate186のeffect partition、occurrence multiset、open class basisまたはrelation resultを使わない。

有限対応を許すのは、TaskSpecまたは一意なrepository authorityが次を直接固定している場合だけとする。

- subject identity
- effect entryの閉じたidentity集合
- 各entryのtargetとend stateまたはtransform
- entry間の必須relationまたは保持constraint
- 集合が全件であることを示すclosure source

Candidate147の`implementation_bound`へbind済み変更predicateが同じidentityと値を全件保持し、追加effectがない場合だけ対応成立とする。対象が複数でも一変更predicateなら一subjectのまま扱う。直接閉包がない場合に、executorがgraph、未来classまたはfallbackを推論して`matched`を作らない。

## 次設計前に追加する反証条件

既存ADR9 r2は回帰確認に使えるが、Candidate173が同条件で45 / 45を満たしているため、新設計の必要性を単独では示せない。設計前に、次の一般条件をcontractとして固定し、情報封鎖した例へmaterializeする必要がある。

1. 具体的witnessは成立しているが、別入力がmissingである。missingは追加witness数だけを変え、既存witnessを無効化しない。期待は`counterexample_found`。
2. 具体的witnessの規範predicateへの適用性を決める入力自体がmissingである。期待は`unavailable`。
3. witnessはなく、domain closureを決める入力がmissingである。期待は`unavailable`。
4. witnessはなく、readableなclosure receiptが対象domainを閉じる。期待は`no_counterexample_found`。
5. authorityが空のreview scopeを含む複数target effectを直接閉じる。期待はreviewなしの`completion_ready`。
6. permission denialと、未信頼の先行review resultが同時に存在する。期待はreview未起動の`unavailable`。

特に条件2を追加しないと、「反例が一つ見えたらmissingをすべて無視する」という逆方向の誤修復を検出できない。

## 設計開始ゲート

次のすべてが揃うまでCandidate番号、bundle、profileまたは評価runを作らない。

- 上記6条件のcontract、情報境界、private oracleが固定されている。
- C147へ追加する制御が一つの`terminal proof obligation`軸へ縮約されている。
- packet全域性とterminal dependency集合が別のidentityとして定義されている。
- counterexample certificateを無効化するdependencyと、単にcertificate外にある入力を区別できる。
- 有限固定効果の対応がauthorityの直接閉包だけから判定され、推論したgraphを要求しない。
- 情報封鎖した敵対的reviewで、既存ADR9の期待結果や過去Candidateを渡さず反例を探索する。

## 現時点の判断

次設計の中心は`review_decision_record_totality`ではなく、terminalごとの`proof obligation`と`dependency certificate`に置く。Candidate186の6条項を修正して再利用せず、C147へ小さい条項群として新設する。

ただしCandidate173がADR9 r2を既に45 / 45で通過しているため、既存ADR9だけを再実行する新Candidateは結論を変えない。まず上記の反証条件2を含む新しいqualification contractで、Candidate173型の単純な優先順と次設計のdependency certificateの差を観測可能にする必要がある。
