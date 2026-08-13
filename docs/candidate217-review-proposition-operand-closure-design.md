# Candidate217 review proposition operand closure 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `ADR9_r2_N5_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- direct base: `Candidate147`

この文書はCandidate bundle作成前の設計記録である。Candidate216を親にせず、Candidate147へreview命題の直接operand閉包を一つの軸として追加する。Candidate216は保存resultとtraceだけを反証入力にする。

## 結論

Candidate217で閉じるのは、rootがreview命題の判定に必要なcurrent valueを既にadmitしていても、その値をpacketへ含めずreviewerへ再取得させられる辺である。

```text
required review proposition
  -> terminal kindを分け得る直接operand集合
  -> 各operandを packet receipt または未取得observation targetへ一意にbind
  -> 全operandの供給経路が閉じた場合だけreviewerを起動
```

case名、field名、scope名、期待terminalまたは成功runのread順は使わない。命題を構成するpredicate dependencyと、TaskSpec-declared inputまたはadmission済みresultにそのcurrent valueがあるかだけを使う。

## 直接baseと保存trace

直接baseはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。

Candidate216 ADR9 r2 N=5では次を観測した。

- 45 / 45 valid、Score `4 / 1 = 44 / 1`。
- packet projectionと重なるread、whole-container read、誤ったpaired target read、root先読みは各0件だった。
- ADR03からADR06の期待terminalは19 / 20まで改善した。
- ADR07 / ADR09では、rootがadmit済みのinventory / contract current valueをpacketへ含めず、reviewerが同じcontainerから14回、7 run再取得した。
- 同一のmodel-visible条件でも、admit済みoperandをpacketへ渡してpaired targetだけを読むrouteと、operandをpacketから落としてreviewerに再取得させるrouteが併存した。
- ADR06の1 runでは必要なcurrent inventory operandがpacketにもdirect observationにもなく、期待`blocked`に対して`unavailable`となった。

Candidate216の成功時tool順、判断順またはpacketの文面は継承しない。追加readなしでもterminal resultが成立したことを、再取得が不要だった反証としてだけ使う。

## Promptが制御を置く正しい層である理由

rootはrequired review proposition、TaskSpec-declared fixed input、変更前evidence operationのadmission済みresultをreviewer起動前に観測できる。命題の真偽またはallowed terminal kindを変え得る直接operandと、そのcurrent valueが既取得か未取得かもpacket構築時に判定できる。

したがって、operandの供給先をpacketまたは許可済みobservationへ閉じる責務はprompt内のpacket construction境界に置ける。repository外executor、tool adapter、runtime hook、case oracleまたはrating変更は必要ない。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setはCandidate147とする。

最短正常経路は、rootが各required review propositionの直接operandを固定し、既にadmit済みのcurrent valueをpacketへliteralに含め、未取得operandだけをfinite manifest上のobservation targetへbindしてreviewerを起動する経路である。reviewerはpacketと必要な未取得operandだけでterminal resultを返す。

### 2. 保存traceへbindした具体的誤経路

Candidate216ではprojection conflictを避けながら、admission済みinventory / contract operandをpacketから省略するrouteが合法だった。そのrouteではreviewerが同じ値をrepositoryから14回、7 run再取得した。別の1 runでは必要operandがどちらの供給経路にも入らず期待terminalを失った。

### 3. 既存境界で防げない理由

Candidate147はpacketの必須入力閉包を定めない。Candidate216のregion conflictはpacketへ実際に入ったitemの再readを閉じるが、最初からpacketへ入れなかったadmission済みoperandにはreceiptもconflictも発生しない。TaskSpecのmanifest membershipとallowed readは候補集合を示すだけで、既取得operandをpacketへ供給する責務を固定しない。

### 4. 変更するpredicateと責務境界

```text
direct_review_operand(proposition, value_identity) :=
  propositionの他のbind済み入力を固定したまま
  value_identityの取り得る値だけが変われば
  propositionの真偽または残るallowed terminal kindが変わり得る

review_operand_binding(operand) :=
  admitted(current value) -> packet_construction_receipt
  not admitted and finite manifest result can bind it -> observation target
  otherwise -> unavailable

review_proposition_input_closed(proposition) :=
  全direct operandにexactly one review_operand_bindingがある
```

責務境界は次のとおりとする。

- operandはrequired review propositionとbind済み入力のdependencyから固定し、名前、case、field、scope、期待resultまたはvalue equalityから作らない。
- current valueがTaskSpec-declared fixed inputまたは変更前evidence operationでadmission済みなら、そのliteral valueとprovenanceをpacketへ含める。reviewer向け再readへ再分類しない。
- 未admit operandだけを、異なる値が残るallowed terminal kindを分け得る場合に限りfinite manifestのobservation targetへbindする。
- 同じoperandをpacketとobservationへ二重bindしない。
- 全required propositionのinput closureが成立しない限りreviewerを起動しない。供給不能な必須operandはreview operationを`unavailable`にする。
- packet constructionのための新規repository evidence、root先読みまたはmanifest存在確認を開かない。
- projection、read conflict、terminal support、producer result admission、対応変更effectは同じPRECHANGE_REVIEW境界内で維持する。

### 5. 消す判断点と到達可能辺

この置換は、admission済みcurrent valueをpacketへ入れるか、reviewerへ再取得させるか、どちらにも供給しないかをrunごとに選べる三分岐を消す。既取得ならpacket、未取得でterminalを分け得るならobservation、供給不能なら`unavailable`の一つへ固定する。

成功runの「先にinventoryを読む」「paired targetだけを後で読む」という順序は義務化しない。閉じるのは、既取得operandを未取得として再分類できるpermission辺と、必須operandをどの供給経路にもbindせずreviewerを起動できるadmission辺である。

### 6. 新たに増える判断点、参照、例外

追加する判断は、required propositionの真偽またはallowed terminal kindが一つのvalue identityだけの違いで変わり得るか、およびそのcurrent valueがadmission済みかだけである。case固有のoperand表、field対応、期待terminal、tool順、read順またはmodel step順は追加しない。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectを全件一致

### 8. 想定する実行routeの変化

- ADR03からADR06では必要な未取得非重複operandだけを観測し、期待terminalを20 / 20へ戻す。
- ADR07 / ADR09ではadmission済みdesign-container operandをpacketへ固定し、paired target以外のreviewer readを0件にする。
- packet projection重複read、whole-container read、誤paired read、mixed read、manifest外read、root prereadを各0件に維持する。
- tool順、判断順、具体的selectorまたはpacket表現を固定しない。

### 9. 停止条件

次のいずれか一件で停止する。

- validまたはScore 4が45 / 45でない。
- admission済みdirect operandをpacketへ含めずreviewerが再取得したrunが一件でもある。
- 必須operandにpacketまたは許可済みobservationのexactly one bindingがないままreviewerを起動したrunが一件でもある。
- ADR03からADR06の期待terminalが20 / 20でない。
- ADR07 / ADR09でpaired target以外のrepository regionを読むrunが一件でもある。
- packet projection重複read、whole-container read、誤paired read、mixed read、manifest外readまたはroot prereadが一件でもある。
- reviewer cardinality、result admissionまたはeffectが一件でも不一致になる。

必須operandの欠落と既取得値の再取得を同じ供給境界で閉じる目的なのでzero-toleranceとする。有効な低品質runを除外または自動再実行しない。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、field identity、scope identityまたは期待dispositionを記載しない。
- 成功runのtool順、read順または判断順を規定しない。
- direct operandはpropositionのpredicate dependencyからだけ固定する。
- admission済みcurrent operandをpacketへ含め、review evidence consumerへ戻さない。
- 未admit operandだけをfinite manifestの観測へbindする。
- 全required propositionのinput closure前にreviewerを起動しない。

## 評価後の判断

ADR9 r2 N=5は45 / 45 valid、Score `4 / 1 = 40 / 5`だった。ADR03からADR06のTaskSpecは`consumer_inventory`と`consumer_contracts`をmodel-visible fixed inputとする一方、reviewer packetをsemantic projection、境界、authority、適用時のboundary normative contract、必須scope、manifestだけに限定していた。C217はadmission済みdirect operandをpacketへ必須化し、reviewer-owned observationへの再分類も禁じたため、全20 runで固定入力と合法carrierの矛盾を作った。

5 runはその矛盾を検出してreviewer起動前に`unavailable`へ停止し、15 runは矛盾を残したままreviewerを起動した。したがって、operand dependencyを閉じるだけでは足りず、値をadmitする前に、その値をreviewerへ運ぶ合法なcarrierがpacketかdirect observationかを確定する必要がある。`model-visible`であることとpacketへ投影可能であることは同じではない。

C217は`quality_failed / mechanism_failed / stopped`とし、repair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate216 ADR9結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
- [Candidate216機序監査](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
