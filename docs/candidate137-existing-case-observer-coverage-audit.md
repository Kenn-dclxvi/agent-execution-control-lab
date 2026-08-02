# Candidate137既存case observer coverage監査

## 結論

Candidate137の`pending_effect_validation_admitted`を、既存caseで確実に発生させる方法はない。Standard14のimplementation caseには構造上適用可能なものが複数あるが、保存traceで「変更前に未観測のまま残った充足済みeffect」を実際に観測したのはF04だけである。

新しいcase revisionやfixture変更で未観測状態を作ると、promptだけを変える比較ではなくなる。したがって既存F04 r2を維持し、Candidate137の同一atomic poolを24件単位で追加する。追加runでscore `3`以下が一件でも出たら停止する。pending effect状態が出た場合は、required validationへのadmission、direct source observer、validation result後closureを個別に判定する。

## 監査対象

- Standard14 r1のimplementation caseのTaskSpec、seed intent、oracle、grader evidence source
- Candidate125 N=30 batchの保存command trace
- Candidate128 F02 / F04 / F07 N=5 result
- Candidate132、Candidate136のF04低Score trace
- Candidate137 F04 N=5 result

## 適用条件

Candidate137固有経路には次の四条件が必要である。

1. 複数required effectの一部だけが変更を必要とする。
2. 変更不要なeffectが変更前evidenceで未観測になる。
3. artifact変更はそのeffectを所有するcontentを変更しない。
4. TaskSpec-required validationが変更後artifact上でそのeffectを直接判定する。

一般的なtest、lint、build、diff、statusの成功だけでは4を満たさない。TaskSpecがeffect固有のsource check、routing check、mocked behavior、test contractをrequired validationへ明示している場合だけ候補になる。

## 既存caseの分類

| case | 構造上のpending候補 | required direct observer | 保存traceの変更前観測 | 判定 |
| --- | --- | --- | --- | --- |
| F01 duplicate asset key | 既存normalization保持 | focused / full test | 抽出した5 runはsourceとfocused testを全量取得 | 適用可能だが未観測経路なし |
| F03 atomic cleanup | successful save保持 | deterministic focused test | C125 5 / 5がsourceとfocused testを全量取得 | 適用可能だが未観測経路なし |
| F04 audit column | 既存`colSpan`保持 | TaskSpec明示の静的source確認 | C132とC136で各1件の`colSpan`未観測。C137 N=5は0件 | 唯一の保存済み発生case |
| F06 empty snapshot test | production挙動保持 | focused / full testとdrift | 抽出した5 runは対象testを全量取得 | preservationはあるがpending source effectではない |
| F07 canonical runner | surrounding routing保持 | 静的routing確認 | 抽出した5 runは`run.sh`全量取得 | 適用可能だが未観測経路なし |
| F07 dependency pair | なし | pair static validation | seedで両effectが未充足 | pending保持caseではない |
| F08 CLI reference | legacy statement保持 | document / entrypoint照合 | 抽出した5 runは対象文書とentrypointを全量取得 | 適用可能だが未観測経路なし |
| F02 cross-layer date | なし | focused test | seedで両source effectが未充足 | pending保持caseではない |

F01、F03、F07 canonical、F08は言語とartifact種別が異なるため、predicateの汎用domainを確認する材料にはなる。しかし現在のfixtureと通常readでは必要contentが小さく、開始状態のeffectが未観測にならない。これらを実行してもCandidate137固有経路を測る可能性はF04より低い。

## F04を維持する理由

F04では同じfixtureとTaskSpecで、保存済みC132とC136に変更前`colSpan`未観測が各1件ある。どちらも必要な`hasAuditKey`変更後、Candidate128由来closureがrequired static source observerへ進まず停止した。

Candidate137 N=5は全件が変更前に`colSpan`を観測したため通常経路だけを通った。これは追加predicateの失敗ではなく、発生条件がなかったことを示す。

F04 r2を変えず同一poolへ追加すれば、次を維持できる。

- Evaluation set、case、fixture、TaskSpec、ratingのidentity
- model、reasoning、CLI/runtime、permission、executor挙動
- C136低Scoreと同じ自然発生経路
- atomic runの再利用と不足slotだけの発行

## 採らない方法

- fixtureを短縮、並べ替え、分割して`colSpan`を見えにくくする
- TaskSpecからcriterion lexemeを削除する
- model-visible outputをexecutorで切り詰める
- read commandや行範囲をpromptへ固定する
- F03等へcase固有の未観測effectを人工的に追加する

これらは比較条件またはexecutor挙動を変え、Candidate137のprompt-only効果と混ざる。

## 次の実測gate

- case: F04 r2のみ
- existing pool: Candidate137 F04 N=5の5 atomic runを再利用
- extension: 24 run単位で追加する
- configured M: 24
- score `3`以下が一件でもあれば停止
- pending effect経路が発生した場合、未観測effect変更0、direct observer admission、required validation完備、validation result後closureを要求
- pending effect状態が0件なら、同じpoolへ次の24件を追加する
- pending effect状態が発生するか、score `3`以下が出たwaveで追加発行を停止する

## 実測更新

N=29ではpending effect状態が0件だったため、ユーザー指示により同じpoolへ24件を追加した。N=53でC2を変更前に確定できないrunが一件発生した。同じrunがscore `2`だったため停止した。

このrunはartifact変更前の`EVIDENCE_GATE`で停止し、Candidate137の変更後validation admissionへ到達しなかった。詳細は[`N=53追試停止結果`](../evaluations/results/candidate137-pending-effect-validation-admission-v14-medium-f04-atomic-reuse-n53-stopped-cli0146_2026-08-02.md)へ保存する。
