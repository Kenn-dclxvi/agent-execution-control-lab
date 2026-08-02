# Candidate139 F02 / F04 / F07 N=5停止結果

## 結論

Candidate139のF02 / F04 / F07各N=5は、score `4 / 2 = 11 / 4`だった。F02がscore `4 / 2 = 1 / 4`、F04とF07は各5 / 5 score `4`である。score `2`が出たため停止し、追加NとStandard14へ進めない。

Candidate138で欠けていた`single_change_target_ready`をANDしても、F02の部分変更を防げなかった。低Score四件のうち三件は`src/app/v4_engine.py`だけを変更し、focused testが8件失敗した。一件は二target分を含む変更を試みたが、patchのpreimage不一致で変更なしのまま停止した。

原因は、guardが数えるtarget集合をTaskSpecから事前固定していないことである。三件の部分変更runは、未観測の`collection_history_updater.py`側effectを「既に実装済み」と動的に再分類した。その結果、未解決target集合が`v4_engine.py`一件へ縮み、`single_change_target_ready=true`としてhandoffが開いた。既存guardを追加しただけでは、誤った充足判定からtarget数を独立させられなかった。

## 固定条件

- candidate: `the-caption-3ce91a4-single-target-continuation-handoff-r1`
- bundle SHA-256: `2e51c8461cf6e5445e46ddb8d885bc56271861fede905e7c886c99b67378a7bb`
- cases: F02 r2、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 15
- pool: `b3121d7c9ddeb82bf21096780f13345bd6a82ce00fadd40f04e6252a5ccdd632`
- selection: `2b503773e0054d46b4ae96f7bd2b9d73`
- analysis: `84ae0dabc2b54cc6a1d15d3bca58cbf5`
- registered result: `4b74e68ea45b46e49dce786256d7e8fe`
- compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`
- median quality / tokens / elapsed: `83.3333` / `426,487` / `235.041秒`

## 低Score挙動

対象runは次の四件である。

- `5029265d2b894c6598dd7bbf0d75b6e8`
- `8752a348f10c4b3a8a40f7caf5327e6c`
- `e01e22e7117e4da0afc1a92b0695eab7`
- `e521d4a599634e74bade46e6dd52eafd`

`5029265d2b894c6598dd7bbf0d75b6e8`、`e01e22e7117e4da0afc1a92b0695eab7`、`e521d4a599634e74bade46e6dd52eafd`は、updater側の日付境界を既に満たすと判断し、engine側だけを未解決targetとして扱った。三件とも`v4_engine.py`だけを変更し、focused testは16件成功、8件失敗だった。失敗8件はupdater側に必要なyfinance `end`境界、対象日、市場日、Alpha Vantage fallbackのeffectが未実装であることを示した。full validationは実行しなかった。

`8752a348f10c4b3a8a40f7caf5327e6c`はengineのprimary / selective refreshとupdater側effectを含むpatchを試みた。しかし`v4_engine.py`のpreimageが一致せず、変更を適用できなかった。その後は追加変更やvalidationを行わず停止した。

## 原因の切り分け

Candidate139が追加したのは、次のAND条件だけだった。

```text
single_change_target_ready
∧ continuation result受領済み
∧ initial_change_effect_setが非空
∧ 変更単位が観測済みcurrent contentへbind済み
```

この形はtarget数を独立に固定していない。実行中に「どのeffectが未充足か」を判定し、その判定後に残ったtargetを数える。したがって未観測effectを充足済みと誤判定すると、複数target taskでも一targetへ縮退する。

F04で成立し、F02で崩れた差はcase名ではない。F04ではTaskSpec上のrequired effectを一つのsource targetが所有する。F02では二つのsource targetが共同所有する。C139はこのTaskSpec上の構造ではなく、観測後の未解決集合をguardの入力にしたため、F02の誤分類に追従してしまった。

次の候補軸は、`task_change_target_set`をTaskSpecから変更前に固定し、effectの充足判定で縮めないことである。部分変更handoffは、その固定集合が一件の場合だけ開く。複数targetでは、あるtargetを充足済みと判断してもcardinality gateを解除しない。この軸は新しいread、validation、rework、executor制御を追加しない。

ただし、単に「変更可能pathを全部数える」とtest fileなどの任意targetを混ぜる。次案では、TaskSpecがrequired outcomeの実装ownerとして要求するresult target集合を何から機械的にbindできるかを、Candidate作成前に監査する必要がある。

## 状態

`f02_f04_f07_n5_evaluated / score_2_4_of_15 / quality_gate_failed / single_target_guard_ineffective / dynamic_target_shrink_identified / result_registered / stopped`

## 結論表

| case / gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4 / 2` | `1 / 4` | fail |
| F04 score `4` | `5 / 5` | pass |
| F07 score `4` | `5 / 5` | pass |
| 全体score `3`以下 | 4件 | stop |
| F02の一target部分変更 | 3 / 5 | fail |
| F02の二target patch試行後停止 | 1 / 5 | observed |
| focused validation | 部分変更3件とも8 failure | fail |
| full validation | 低Score4件とも未実行 | expected stop |
| 追加N / Standard14 | 未発行 | stopped |
