# Candidate141 post-result change admission監査

## 結論

Candidate141の残存失敗は、C122のone-wave自体ではなく、**変更前requestの準備完了と、result受領後の変更開始準備完了が分離されていないこと**で発生した。

C141は発行前の`prechange_evidence_wave_ready`へ`required_relation_evidence_scope`を追加した。しかし、result受領後に全required effectのrelation coverageを再判定するpredicateは追加していない。低Score runではupdater effectが`unobserved`のまま残ったが、C136の「unobserved effectは別のunsatisfied effectの変更開始を拒否しない」が適用され、engineだけの初回変更を許した。

したがって次の一変更軸は、read方法、one-wave、terminal closure、effect witnessの再修正ではない。**TaskSpec上で複数editable targetが共同でrequired outcomeを所有する初回変更だけ、result受領後に全required effectが`satisfied`または`unsatisfied`へbind済みであることをchange admissionへ要求する軸**である。

単一editable target内の独立effectではC136のeffect-local変更を維持する。これによりF04の必要変更を止めず、F02やdependency pairの一target部分変更を防ぐ。

## 監査対象

- C122 `prechange_evidence_wave_ready`
- C125 `single_change_target_ready`とcontinuation
- C136 `effect_prechange_state`と`initial_change_effect_set`
- C138 / C139 continuation後の部分変更handoff
- C140 `effect_satisfaction_witness`
- C141 `required_relation_evidence_scope`
- C141 F02低Score run `d51aa3bb9310444eb20f63890981ab16`

## C141低Scoreの実際の遷移

低Score runは次の順で進んだ。

1. 発行前に、4 targetのrelation coverageを一waveへbindすると宣言した。
2. 実際には4 target全体を終端まで取得し、初回outputは`55,360`文字になった。
3. result受領後、engineのprimary refreshだけを`unsatisfied`と認識した。
4. updaterは日付選択helperとtestの存在を認識したが、helperからmarket history取得への未接続relationを変更対象へbindしなかった。
5. `initial_change_effect_set`へengine effectだけを入れた。
6. updater effectが`unobserved`でも、C136規則によりengine変更は拒否されなかった。
7. engineだけを変更してfocused gateを実行した。
8. focused gateは16件成功・8件失敗だった。
9. updater current contentを確実にbindできないとしてreworkせず停止した。

ここでC141のrelation coverageはrequest identityには現れた。しかし、受領したresultが本当にcoverage completeかを変更開始前に判定する分岐にはならなかった。

## 既存制御の役割と変化

### C122

C122はexact target setを一つの変更前waveで取得し、そのresultを`edit-ready`または`terminal stop`へ閉じるために導入された。C122本文には、変更predicateと保持constraintをbindできなければ具体的なterminal dispositionで停止する明示分岐があった。

目的はlocator-only result、複数waveへの分割、不要なmodel再入の削減である。全required effectの個別state管理はまだ存在しなかった。

### C125

C125は単一editable targetの取得不足によるF04 false stopを避けるため、同一target continuationを一度許可した。その際、初回resultでbind不能なら直ちに停止するC122の一文を、single-target continuation分岐へ展開した。

複数editable targetではcontinuationを開かずinitial waveを維持するとしたが、現在本文にはC122と同じ形の「multi-targetでbind不能なら停止」が独立predicateとして残っていない。

### C136

C136はF04で充足済みeffectを再変更してatomic patchを失敗させる問題を解くため、effectを`satisfied / unsatisfied / unobserved`へ分けた。`initial_change_effect_set`にはunsatisfiedだけを入れ、unobservedは推測変更せず、別のunsatisfied effectも止めないとした。

これは単一target内で、一方のeffectだけを安全に変更できる条件には必要だった。一方、複数targetが共同で一つのrequired outcomeを作るF02では、別ownerのunobserved effectを残した部分変更も同じ規則で許可した。

### C138 / C139

C138はsingle-target continuation後の観測済みeffect変更をvalidationへ渡すためのhandoffである。C139はそのhandoffへ`single_change_target_ready`を追加した。

ただしguardの適用先は`continuation_effect_change_ready`である。C141低Scoreはcontinuationを使わないinitial changeなので、C139 guardの対象外だった。

### C140 / C141

C140はeffectを`satisfied`へbindする証拠をrequired relationの全memberと接続へ厳密化した。C141は変更前requestのscopeをrequired relation coverageへ変えた。

両方ともstate判定の意味と入力scopeを改善したが、result受領後から`initial_change_effect_set`発行までのadmission条件は変更していない。

## 問題点の切り分け

今回の課題は三つに分かれる。

1. **発行前scope**: 何を証拠として要求するか。C141が担当する。
2. **受領後state**: 得られたcontentから各effectをどう分類するか。C140が担当する。
3. **変更開始admission**: unobserved effectが残る状態で別effectを変更してよいか。C136が担当する。

C141低Scoreは1を宣言したが、実resultでは2が一effect分成立せず、3が部分変更を許した。したがって次に変更すべきownerは3である。

one-waveとterminal closureを削除しても、同じresultから部分変更を許す3が残れば問題は解消しない。逆に、全taskでunobservedを変更開始拒否へ戻すと、C136が避けたF04 false stopを再導入する。

## 次Candidateの境界

次Candidateを作る場合はC141を直接親とし、`initial_change_effect_set`のadmissionだけを置換する。

候補predicateは次の意味に限定する。

```text
initial_joint_change_ready :=
  single_change_target_ready
  ∨ TaskSpec上でrequired outcomeを共同所有する全required effectが
    result受領後にsatisfiedまたはunsatisfiedへbind済み
```

```text
initial_change_effect_set :=
  initial_joint_change_ready=trueの場合の
  effect_prechange_state(effect)=unsatisfiedの全effect
```

`single_change_target_ready=true`ではC136のeffect-local変更を維持する。複数editable targetが共同所有する場合だけ、一effectでもunobservedならinitial partial changeを発行しない。

停止時に追加readを開く規則は追加しない。C122 / C125の既存evidence admissionとcontinuation境界を維持する。

## 汎用性

この境界はcase IDやfile名ではなく、required outcomeとeditable ownerの関係へ依存する。

- application producerとdomain consumer
- schema writerとreader
- config declarationとruntime consumer
- migrationと対応model
- dependency declarationとcompiled lock / provenance
- API implementationと別moduleのadapter

一つのtarget内で独立effectを順に直せる場合はeffect-local admissionを使う。複数ownerの成果がそろって初めて一つのoutcomeになる場合はjoint admissionを使う。

## 非目標

- 行数、bytes、command、read回数の固定
- 全file取得の禁止
- executorまたはoutput deliveryの変更
- unobserved effectの推測変更
- 追加evidence waveまたはrework回数の追加
- 全taskをcriterion完全観測gateへ戻すこと

## 判断

| 論点 | 判断 |
| --- | --- |
| C141の発行前scope | 4 / 5件で狙った限定取得へ対応したが、result coverageを保証しない |
| 低Score直前のowner | `initial_change_effect_set`のeffect-local admission |
| C122との関係 | one-wave目的は維持。元のbind不能停止は後続統合で独立分岐として残っていない |
| C125との関係 | single-target continuationを維持。F02 initial changeには適用されない |
| C136とのtradeoff | 単一targetでは必要。複数owner共同outcomeへ同じ許可を広げたことが残存漏れ |
| C139 guardとの重複 | 同じ`single_change_target_ready`を使うが、C139はcontinuation後だけ。次軸はinitial changeだけ |
| 次の一変更軸 | TaskSpec-bound joint ownerで全effect state bind後だけinitial changeを許可 |
| 現在状態 | `audited / post_result_initial_admission_gap_identified / candidate142_ready_not_created` |
