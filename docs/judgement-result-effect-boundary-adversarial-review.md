# 判断結果の効果境界設計 第1版 情報封鎖敵対的review

> review result: `counterexample_found`
>
> producer identity: `judgement_effect_design_review_r1`

## review境界

独立producerは次の三文書だけを読んだ。ファイルは変更していない。

- Candidate147制御原文 `prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt`
- 一般設計原則 `docs/prompt-control-design-principles.md`
- 設計第1版 `docs/judgement-result-effect-boundary-design.md`

評価case、fixture、oracle、rating、保存済みresult、Candidate147以外の旧Candidate、先行finding、会話履歴、期待terminal、修正案、インターネット、画面履歴およびmemoryは入力にしていない。

## 結論

Candidate作成前gateの11観点を確認し、一般入力だけから独立した具体的反例が2件成立した。設計第1版は`counterexample_found / stopped`とし、Candidate bundle、profileおよびTarget評価を作成しない。

## 11観点の結果

1. authorityが対象identityと終状態を固定した単純な設定変更では、`authority_fixed_effect=true`からreviewなしで変更へ進むため、不要reviewを要求する反例は成立しなかった。
2. `authority_fixed_effect`がversion付きclass predicateと決定的変換を許すため、固定されていない将来入力へ届く変更をreviewなしでadmitできる反例`CE-JREB-02`が成立した。
3. `missing / unreadable / terminal failure`をterminal review入力として渡す規定があり、packet readiness不足としてreview発行前に停止する反例は成立しなかった。
4. `counterexample_support`外のmissing等は成立済み反例を失効できないため、この反例は成立しなかった。
5. 判断を変え得るmissingがあれば`unavailable`を返すため、そのまま`no_counterexample_found`をadmitする反例は成立しなかった。
6. open domain、未来instance未列挙、一般的不確実性だけでは`unavailable`にしないため、この反例は成立しなかった。
7. judgementの停止効果は対応subjectを含む未発行artifact変更へ限定され、read-only operationと別required outcomeはsubjectから除外されているため、失敗を無関係なsubjectまたはtask全体へ直接伝播する反例は成立しなかった。
8. rootの確認対象はproducer identity、terminal性、subject identity、result identity、dependency bindingに限定され、意味再判定を禁止しているため、この反例は成立しなかった。
9. combination resultを無関係な個別subjectへ複製することは禁止されている。一方、必要な`combination_subject`の形成が義務ではなく「できる」に留まるため、組合せ違反を表すsubjectを形成しないまま変更をadmitできる反例`CE-JREB-09`が成立した。
10. tool、file、schema、locator、read順、review回数を固定せず、起動方法の失敗も`METHOD`と`RECOVERY`で扱うため、この反例は成立しなかった。
11. 列挙済みdependencyが実際に変わった場合だけ失効し、同値再取得や無関係な変更では失効しないため、dependencyが正しくbindされた入力では反例は成立しなかった。

## CE-JREB-02

### 入力

- TaskSpecは、今後受け取る設定キーをすべて小文字化する変更と、設定キーの一意性を保持するconstraintを要求する。
- 適用中authority `key-normalization/v1`は、対象classを「すべての入力設定キー」、決定的変換を`lowercase(key)`として固定する。
- admission済みcurrent contentは`Foo`と`Bar`だけであり、小文字化後も`foo`と`bar`で一意である。
- implementation choiceは、入力設定キーすべてへ`lowercase`を適用する規則を追加する。対象class、変換、version、一意性constraintをbindし、current content上では実行可能なので`implementation_bound=true`となる。
- artifact変更後のterminal inputとして、二つの設定キー`A`と`a`を与える。
- resultは両方とも`a`となり、一意性constraintに直接矛盾する。
- next operationは、この規則を含むartifact変更invocationである。

### 設計上の遷移

`implementation_bound=true`
→ version付きclass predicateと決定的変換がauthorityに固定され、implementation choiceも機械的に一致する
→ `authority_fixed_effect=true`
→ 独立reviewを発行せず`review_admission_ready=true`
→ artifact変更invocationを発行
→ 将来入力`A`と`a`で一意性constraintを破る。

### 誤ったartifact変更

固定されていない個々の入力値へ届く一般規則を、全入力に対するconstraint成立をreviewせずに変更可能と判定する。

### 破る設計predicate

- `authority_fixed_effect`が、version付きclass predicateと決定的変換の機械的一致だけでreview省略を許す部分。
- Candidate作成前gate第2観点の、固定されていない入力へ届く変更をreviewなしでadmitできない境界。
- artifact変更を許すには全対応subjectが安全にadmitされているという`review_admission_ready`の意図。

### 入力境界

TaskSpec、version付きauthority、current content、implementation choice、保持constraint、terminal input、result、next operationだけで構成され、禁止入力を使用していない。

## CE-JREB-09

### 入力

- TaskSpecは、将来の数値入力`x`に対し、subject `S1`として条件`A=true`なら`x := x + 1`、subject `S2`として条件`B=true`なら`x := x * 2`を追加し、結果を`10`以下に保つconstraintを要求する。
- current contentでは`A=false`かつ`B=false`であり、implementation choiceは現在状態上で実行可能としてbindされる。
- `S1`単独についてはterminal input `x=5, A=true, B=false`のresultが`6`でconstraintを満たす。
- `S2`単独についてはterminal input `x=5, A=false, B=true`のresultが`10`でconstraintを満たす。
- 各subjectの独立reviewは`no_counterexample_found`となる。
- `combination_subject={S1,S2}`は形成されない。
- next operationは`S1`と`S2`を同時に含むartifact変更invocationである。
- artifact変更後のterminal input `x=5, A=true, B=true`では、`S1`の後に`S2`が作用してresultが`12`となり、constraintに直接矛盾する。

### 設計上の遷移

`S1 no_counterexample_found`かつ`S2 no_counterexample_found`
→ combinationだけで違反が成立する場合にも`combination_subject`は作成可能であるだけで、形成を必須にするpredicateがない
→ 有効なcombination subjectが存在しない
→ invocation内の全個別subjectが`review_admission_ready=true`
→ `S1`と`S2`を同時に含むartifact変更を発行
→ joint inputでconstraintを破る。

### 誤ったartifact変更

個別subjectでは成立しないが最小subject集合で成立する反例について、その集合identityを形成しないまま各個別judgementだけで同時変更をadmitする。

### 破る設計predicate

- artifact変更admissionが「有効なcombination subject」の禁止集合だけを確認し、そのcombination subjectの必要十分な形成を要求していない部分。
- 一つのinvocationが生成する全変更predicateを安全にadmitするというartifact変更admissionの意図。

### 入力境界

TaskSpec、current content、二つのimplementation predicate、保持constraint、各subjectのterminal judgement、joint terminal input、result、next operationだけで成立し、禁止入力を使用していない。
