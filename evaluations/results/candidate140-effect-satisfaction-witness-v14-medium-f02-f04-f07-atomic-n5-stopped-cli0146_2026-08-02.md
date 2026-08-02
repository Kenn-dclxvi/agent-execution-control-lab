# Candidate140 F02 / F04 / F07 N=5停止結果

## 結論

Candidate140のF02 / F04 / F07各N=5は、score `4 / 2 = 13 / 2`だった。F02がscore `4 / 2 = 3 / 2`、F04とF07は各5 / 5 score `4`である。score `2`が出たため停止し、追加NとStandard14へ進めない。

`effect_satisfaction_witness`はF02五件中二件で変更前に未接続helperを未充足と認識させた。別の一件はengineだけを初回変更した後、focused failureを受けて一回のreworkでupdater接続を修復した。しかし二件は、required relationの全memberと未接続callがmodel-visible resultに存在しても、primary refreshだけを変更した。したがって証拠定義は一部挙動を改善したが、変更開始判断を安定して拘束できなかった。

## 固定条件

- candidate: `the-caption-3ce91a4-effect-satisfaction-witness-r1`
- bundle SHA-256: `789ff42087140df1012a058bd532a2550195bd62b3a7211fb0392e8e80150002`
- cases: F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 15
- valid / rateable / excluded: `15 / 15 / 0`
- pool: `bfcec836cd435c16f8ed52fe3a403991ddea71ea6b421001648cebbc93e730ca`
- selection: `bbe8051b71824f2d8bd0da43a568f68e`
- analysis: `63c8956e19db4dfbba6ea63eebfa71a4`
- registered result: `9e77596292d248a5bd776a811fba19b4`
- selection comparison key: `008104d71d8980189b90ae60033bcfa118e1211b46be30dea8f7484eacfbcc7b`
- registered targeted compatibility key: `f3f74b392a22e54828608943f3f29c4e1200cf626d34e0ee0487d758112dedeb`
- median quality / tokens / elapsed: `100.0` / `466,278` / `235.449秒`
- execution archive SHA-256: `6471bac91b567341c35b34cc403e24c5b62025c3a951a35e1dae3bc8af75b022`

## F02挙動

### 変更前に両effectを認識した成功

run `1fd57ebbdf1a424591e79d0a1a61f081`と`d0f2caca99554e4a9bda10cc33106549`は、変更前に次の二点を未充足と認識した。

1. primary refreshが日付引数を渡していない。
2. updaterの日付解決resultがmarket history取得へ接続されていない。

両sourceを初回変更し、focused 24件、full 326件成功・3件skipで完了した。

### reworkで回復した成功

run `1aec3ae3d13a46f2aaa36b17bdbdce6a`は、初回にengineだけを変更した。focused gateは16件成功・8件失敗だった。そのresultでupdaterの未接続を明示し、変更前resultに存在したcurrent contentを使って一回のreworkを行った。二回目のfocused gateとfull gateは成功した。

### 低Score

低Score runは次の二件である。

- `7d05c57220fe43fe9feec6e6d97db66e`
- `7d9de314f617497a94744ba437b61f27`

両runはengineだけを変更した。focused gateは16件成功・8件失敗で、updaterの日付境界とfallback effectが未充足だった。full gateは停止条件に従い実行しなかった。

初回resultには次がすべて存在した。

- `def _resolve_market_end_date`
- `self._fetch_market_history(asset)`という未接続call
- `yf.download`
- updaterの日付境界test

したがって、required relationを判定するcontentがなかったわけではない。一件は最終報告でresult切断を理由にしたが、保存されたmodel-visible resultには未接続を直接示すmemberが存在する。C140のpredicateを変更判断へ適用しなかったことが低Score二件に共通する。

## C139からの変化

C139 F02はscore `4 / 2 = 1 / 4`で、engineだけの部分変更が3 / 5だった。C140 F02はscore `4 / 2 = 3 / 2`で、最終的なengineだけの部分成果は2 / 5へ減った。

ただし、この差はN=5の記述値であり、改善率または安定性を主張しない。Candidate140は要求した5 / 5 score `4`と部分変更0 / 5を満たしていない。

## 原因と次の調査境界

未接続helperを充足済みにする意味上の空白はC140で閉じた。それでも二件は、全memberが観測済みの状態で局所的な「primary refreshだけが未充足」という判断を維持した。

次に必要なのは、同じpredicateを別名で追加することではない。成功二件、rework成功一件、低Score二件で、`effect_satisfaction_witness`が変更開始判断へ適用されたか、validation failureまで延期されたか、無視されたかを分けた判断順序の比較である。新Candidateはこの比較前に作らない。

## 状態

`f02_f04_f07_n5_evaluated / score_2_2_of_15 / quality_gate_failed / partial_effect_witness_response / f02_partial_change_2_of_5 / result_registered / stopped`

## 結論表

| case / gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4 / 2` | `3 / 2` | fail |
| F04 score `4` | `5 / 5` | pass |
| F07 score `4` | `5 / 5` | pass |
| 全体score `3`以下 | 2件 | stop |
| F02変更前に両effect未充足認識 | 2 / 5 | insufficient |
| F02一回reworkで両effect完了 | 1 / 5 | observed |
| F02最終一target部分成果 | 2 / 5 | fail |
| 追加N / Standard14 | 未発行 | stopped |
