# Candidate138 F02 / F04 / F07 N=5汎用性停止結果

## 結論

Candidate138のF02 / F04 / F07各N=5は、score `4 / 2 = 13 / 2`だった。F02がscore `4 / 2 = 3 / 2`、F04とF07は各5 / 5 score `4`である。score `2`が出たため停止し、追加NとStandard14へ進めない。

二件の失敗は同じ原因だった。Candidate138の設計domainは単一targetだったが、prompt内の`continuation_effect_change_ready`へ`single_change_target_ready`を含めなかった。そのため複数editable targetのF02でも、観測できた`v4_engine.py`だけを先に変更し、未観測の`collection_history_updater.py`をvalidationへ回した。focused testは8件失敗し、full gateは未実行となった。

## 固定条件

- candidate: `the-caption-3ce91a4-continuation-effect-change-handoff-r1`
- bundle SHA-256: `b542f78becf313fbcc8226c904a2aa324fa4194983c4fc8ec14bcee57cbae7a5`
- cases: F02 r2、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: F02 5、F07 5
- reused: F04 5
- pool: `07e817fd939e74fbe60613c4da935da2757e0e073642c9c9c77d8d4c716f3ef8`
- selection: `e9ad877c58ea428284f76d5c02db8fa1`
- analysis: `9a88971d986c4bdea34809d22b348aa5`
- registered result: `bc519da8b78848c59f1d7c07cbcdb9e7`
- compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`

## 低Score挙動

対象runは`a8738c6a810f4e538c210c11c1363089`と`c17f6943b9f54e2dadd3460f2104742b`である。

両runは、primary refreshが日付引数なしであることを観測した。一方、updater内部のcurrent contentは出力切り詰めにより十分にbindできなかった。そこで`src/app/v4_engine.py`だけを変更し、`src/domain/collection_history_updater.py`は変更しなかった。

focused testではengine側effectは成功したが、updaterがyfinanceの`end`やAlpha Vantage fallbackの日付境界を実装していないため8件失敗した。既存stop conditionに従い、追加read、推測変更、full gateは行わず停止した。

## 原因

Candidate138の設計文書は適用対象を単一targetへ限定している。しかし実装predicateは次だった。

```text
continuation result受領済み
∧ initial_change_effect_setが非空
∧ 変更単位が観測済みcurrent contentへbind済み
```

ここに`single_change_target_ready`がない。F04では全effectを一つのtargetが所有するため安全だった。F02では二つのeditable targetが共同でrequired outcomeを所有するため、部分変更をvalidationへ渡してはいけなかった。

次の修正軸は新しい回復機構ではない。Candidate138のhandoff admissionへ既存の`single_change_target_ready`をANDし、複数targetでは従来の完全content waveと停止境界を維持することである。

## 状態

`f02_f04_f07_n5_evaluated / score_2_2_of_15 / quality_gate_failed / f04_mechanism_pass_preserved / multi_target_admission_leak_identified / result_registered / stopped`

## 結論表

| case / gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4 / 2` | `3 / 2` | fail |
| F04 score `4` | `5 / 5` | pass |
| F07 score `4` | `5 / 5` | pass |
| 全体score `3`以下 | 2件 | stop |
| F02両target変更 | 低Score2件とも1 / 2 target | fail |
| focused validation | 低Score2件とも8 failure | fail |
| full validation | 低Score2件とも未実行 | expected stop |
| 追加N / Standard14 | 未発行 | stopped |
