# Candidate140 evidence completeness granularity監査

## 結論

Candidate140のF02低Scoreを分けた主要な観測差は、`effect_satisfaction_witness`の定義ではなく、変更前evidenceの粒度である。

C139 / C140のF02計10件では、必要な関係を含む範囲へ限定した3件は3 / 3件とも変更前にengineとupdaterの両effectを未充足として認識し、最終score `4`だった。4 targetの全体または終端を一括取得した7件は、変更前に両effectを認識した例が0 / 7件だった。最終的にscore `4`へ回復したのは、focused validation失敗後にupdaterを一回reworkしたC140の1件だけである。

したがって次に検証する価値がある軸は、read回数、行数、bytes上限、追加のeffect分類ではない。**evidenceの完全性を「artifact全体を広く取得したこと」ではなく、「各required effectを決めるmemberと接続関係を直接覆ったこと」で判定する軸**である。

これはexecutorの出力制御ではない。promptが変更前判断に使う証拠の選択単位を、file単位からrequired relation単位へ変更する案である。

## 監査対象

- Candidate139 F02 `N=5`
- Candidate140 F02 `N=5`
- Rating v14、`gpt-5.6-sol`、reasoning `medium`、Codex CLI `0.146.0`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND`

C139とC140の比較条件はprompt identityを除いて一致する。C140はC139の`effect_prechange_state(effect)=satisfied`証拠条件だけを置換した。

ここでいう「変更前認識」は、最初のartifact変更を発行する前に、engineとupdaterの両方へ必要変更があると判断した状態を指す。「限定取得」は固定行数を意味しない。required relationを含む一部範囲を取得し、4 target全体を終端まで集約していない形を指す。

## 保存traceの観測事実

| Candidate | run | 変更前evidenceの形 | 集約文字数 | 変更前の両effect認識 | 最終挙動 | score |
| --- | --- | --- | ---: | --- | --- | ---: |
| C139 | `4223252e508240f1a65643043d1e5887` | 4 targetの限定範囲 | 46,329 | あり | engine / updaterを変更し全gate通過 | 4 |
| C139 | `5029265d2b894c6598dd7bbf0d75b6e8` | 4 target全体 | 55,367 | なし | updaterを充足済みとしengineだけ変更 | 2 |
| C139 | `8752a348f10c4b3a8a40f7caf5327e6c` | instructionと4 targetの過大範囲 | 65,476 | なし | patch不一致後に変更なしで停止 | 2 |
| C139 | `e01e22e7117e4da0afc1a92b0695eab7` | 4 targetの過大範囲 | 55,524 | なし | focused validationでupdaterを閉じられると判断しengineだけ変更 | 2 |
| C139 | `e521d4a599634e74bade46e6dd52eafd` | 4 target全体 | 64,645 | なし | updaterの必要contentがoutput capで欠けたと判断しengineだけ変更 | 2 |
| C140 | `1aec3ae3d13a46f2aaa36b17bdbdce6a` | 4 target全体を複数rangeで集約 | 55,360 | なし | engineだけ変更後、focused failureからupdaterを一回rework | 4 |
| C140 | `1fd57ebbdf1a424591e79d0a1a61f081` | 4 targetの限定範囲 | 47,278 | あり | engine / updaterを変更し全gate通過 | 4 |
| C140 | `7d05c57220fe43fe9feec6e6d97db66e` | 4 targetの過大範囲 | 55,533 | なし | focused failure後も証拠を安全にbindできないとして停止 | 2 |
| C140 | `7d9de314f617497a94744ba437b61f27` | 4 target全体 | 55,360 | なし | focused failure後に追加調査せず停止 | 2 |
| C140 | `d0f2caca99554e4a9bda10cc33106549` | 4 targetの限定範囲 | 48,322 | あり | engine / updaterを変更し全gate通過 | 4 |

集計すると次になる。

- 限定取得: 変更前の両effect認識 `3 / 3`、最終score `4`は`3 / 3`
- 全体または過大取得: 変更前の両effect認識 `0 / 7`、最終score `4`は`1 / 7`
- 全体または過大取得で唯一回復した1件も、変更前判断ではなくfocused validation失敗後のreworkで回復した

C140の5件では、保存された初回`aggregated_output`のすべてに、`_resolve_market_end_date`、未接続の`self._fetch_market_history(asset)`、`yf.download`、updater側の日付境界testが含まれる。つまりarchive上は、低Score二件だけrequired memberの文字列が欠落していたわけではない。

ただし、保存archiveの`aggregated_output`がmodelへ同じ形で全量提示されたことまでは、このartifactだけでは証明できない。よって「executorが切り詰めた」または「modelが全量を見た」とは確定しない。確定できるのは、広い集約と変更前のrelation bind失敗が強く対応したことまでである。

## なぜ以前は細かい制御なしでも成功したか

成功時は、model自身が自然に必要箇所を含む限定範囲を選んでいた。その結果、helperの存在だけでなく、helperから実際の取得callまでの接続が同じ判断材料の中で目立つ形になった。

一方、失敗時は4 target全体を一つのterminal waveへ集約した。必要な文字列自体は保存outputに残っていても、required effectを決める接続関係が大量の周辺contentへ埋もれた。その状態で、helperの存在、後続validation予定、出力不足の自己判断が、未接続関係より先に採用された。

これは「正しく進む時だけ制御が効いた」という差ではない。同じpromptの裁量の中で、先に選ばれたevidenceの形が違い、その後のeffect判定が分岐したと解釈する方が保存traceに合う。

## 既存の完全性gateとのトレードオフ

C122の`prechange_evidence_wave_ready`は、TaskSpecが同じpredicateを共同で決めるexact target setを列挙した場合、全targetのcontent evidenceを一つのwaveへまとめ、次を`edit-ready`または`terminal stop`へ閉じるために導入された。目的は、locator-only result、複数waveへの分割、変更前の不要なmodel再入を防ぐことである。C122のF02ではこの制御が成立し、tokenも削減した。

C125の`continuation_scope_complete`は別の問題を扱う。単一editable targetで初回範囲が不足した場合に、未観測criterionへbindするsymbol context、または同一targetの未取得content全体を一度だけ取得し、取得不足によるfalse stopを防ぐ。これはF04のsingle-target continuation用であり、F02のmulti-target initial waveでは発火しない。

したがってF02の直接の境界はC122のone-wave terminal closureである。C125の全未取得content fallbackがF02を直接発生させたとはいえない。ただし両者は、完全性を「対象contentを広く覆うこと」で代替できる同じ設計傾向を持つ。

この設計には実測上のトレードオフがある。

- target集合を欠落させず、一waveで判断を閉じると、under-readと不要な再入を減らせる。
- 完全性をartifact contentの広さで満たそうとすると、multi-targetでは証拠が大きくなり、required relationの実効的な識別が弱くなる可能性がある。
- effect判定だけを厳密にしても、その判定へ入るrelationが使える形で選ばれていなければ低Scoreは残る。C140がその例である。

よって両立点はone-waveを撤回することではない。**一waveの完了条件をtarget content coverageからrequired relation coverageへ変えること**である。

## Std14を越える汎用性

次軸はF02のpath、symbol、file数へ依存させない。required relationは、TaskSpecが成果として要求する二つ以上の要素と、その接続を意味する。

適用例は次のとおりである。

- 関数定義とcall site: helperがあるだけでなく、要求された経路から呼ばれること
- producerとconsumer: 値が生成されるだけでなく、要求されたconsumerへ渡ること
- branchとeffect: 条件分岐があるだけでなく、指定条件で要求effectへ到達すること
- configとreader: keyが宣言されるだけでなく、実行経路で読み取られること
- schemaとwriter / reader: fieldが片側にあるだけでなく、生成と消費の両側が対応すること
- dependency pair: 一方のfile変更だけでなく、TaskSpecが要求する組が対応していること
- commandとdocument: command名が存在するだけでなく、説明対象と実行方法の対応が示されること

一方、required relationがTaskSpecで固定されていない探索型課題、repository全体のreview、単なるprose校正へ同じfast pathを強制しない。これはすべてのreadを小さくする一般規則ではない。

## 次Candidateへ進む前の境界

Candidate141を作るなら、C140を直接親とし、変更軸を変更前evidence waveの完了単位だけに限定する。

候補predicateは次の意味にする。

```text
prechange_relation_coverage_ready :=
  TaskSpecが列挙した各required effectについて、
  satisfied / unsatisfiedを決めるmemberと接続の直接evidenceが
  同じ変更前waveに一度ずつ含まれる
```

`prechange_relation_coverage_ready=true`なら、artifact全体の未取得contentを完了条件にしない。falseならeffectを推測で充足済みにせず、既存のadmission境界に従う。

次は変更しない。

- 一waveでexact target setを扱うC122の目的
- C125のsingle-target continuation回数とterminal closure
- C128のrequired-effect closure
- C140のeffect satisfaction witness
- validation failure後のrework回数
- executor、CLI、tool adapter、runtime hook、外部wrapper

行数、bytes、`sed`、`awk`、出力capはpredicateへ含めない。これらを固定すると、file構造や言語へ依存し、以前の細粒度な実行制御へ戻るためである。

## 判断

| 論点 | 判断 |
| --- | --- |
| C140低Scoreの直前分岐 | 変更前evidenceの粒度。限定取得は両effect認識3 / 3、全体・過大取得は0 / 7 |
| C140 predicateの評価 | relation定義は必要だが単独では不十分。入力evidenceの形を安定させなかった |
| C122との関係 | one-wave terminal closureの目的は維持する。content全体ではなくrelation coverageで完了させる余地がある |
| C125との関係 | F02の直接原因ではない。F04専用fallbackだが、content量で完全性を代替する同型のtradeoffを持つ |
| executor報告制御か | いいえ。保存archiveだけではdeliveryを確定できず、解決軸にも使わない |
| 汎用化単位 | required effectのmemberと接続。関数、data flow、branch、config、schema、pair、文書関係へ適用可能 |
| 次の一変更軸 | prechange waveの完了単位をtarget content coverageからrequired relation coverageへ置換 |
| 現在状態 | `audited / evidence_granularity_split_identified / candidate141_ready_not_created` |
