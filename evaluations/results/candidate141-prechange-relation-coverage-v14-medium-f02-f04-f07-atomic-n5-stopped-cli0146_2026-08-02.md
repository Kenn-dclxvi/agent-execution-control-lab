# Candidate141 F02 / F04 / F07 N=5停止結果

## 結論

Candidate141のF02 / F04 / F07各N=5は、score `4 / 2 = 14 / 1`だった。F02がscore `4 / 2 = 4 / 1`、F04とF07は各5 / 5 score `4`である。score `2`が出たため停止し、追加24件とStandard14へ進めない。

F02ではrequired relationを含む限定範囲を選んだ4件が、変更前にengineとupdaterの両effectを未充足と認識して両sourceを変更し、score `4`だった。残る1件は4 target全体を終端まで取得し、updater effectを見落としてengineだけを変更した。focused gate失敗後もupdaterのcurrent contentをbindできないとして停止し、score `2`になった。

したがって、relation coverageを完全性の意味として追加した方向は成功4件の挙動と一致したが、全体取得を選ぶ既存分岐を閉じられなかった。quality gateとF02変更前の両effect認識5 / 5を満たさないため、Candidate141を停止する。

## 固定条件

- candidate: `the-caption-3ce91a4-prechange-relation-coverage-r1`
- bundle SHA-256: `72f7596b38e2ca2ef9c3b30aee9751787ccf9c1e21f5cd163ee168ab4bd79874`
- cases: F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / configured M: `5` / `24`
- newly issued: 15
- valid / rateable / excluded: `15 / 15 / 0`
- pool: `62eb3b3816a6a5c0a5d8f5a71024b5f401f042c85ac1c822146fd578723137d3`
- selection: `730464c27a3947979313b66f442f9c77`
- analysis: `aae9cea669d54774872b2e8cff614d7c`
- registered result: `59548939499d4fccb152ce0ce18681a2`
- selection comparison key: `008104d71d8980189b90ae60033bcfa118e1211b46be30dea8f7484eacfbcc7b`
- registered compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`
- median quality / tokens / elapsed: `100.0` / `397,627` / `232.801秒`
- execution archive SHA-256: `087082a5be7246e79dd7d2058ee5659c3e50dbb45cc1613719e916aa84b2b393`

中央値qualityは5つのselection iterationの中央であり、低Scoreがなかったことを意味しない。公式score分布と停止判断は15 run全件で判定する。

## F02挙動

### 限定取得の成功4件

次の4件は、4 target全体を終端まで取得せず、required relationを含む範囲を一waveで取得した。

- `7b187f86f00442d88ca0b40a963f8dc4`
- `a2b603c0117b42c780d16803283ab632`
- `d15d380b41a1484899cb2351142dbfef`
- `d552b668f88d4e6387826981827d0e60`

初回集約文字数は`46,322`が3件、`48,047`が1件だった。4件すべてが変更前に次を認識した。

1. primary refreshが日付を渡していない。
2. updaterが算出したend dateをmarket history取得へ接続していない。
3. selective retryとdate-bound test contractは既に保持されている。

4件ともengineとupdaterだけを変更し、focused gateとfull gateを成功させた。test変更と許可外driftはない。

### 全体取得の低Score1件

run `d51aa3bb9310444eb20f63890981ab16`は、開始identityと4 targetに対して`1,9999p`相当の全体取得を一つのcommandへまとめた。初回集約文字数は`55,360`だった。

初回判断ではprimary refreshだけを未充足とし、updaterの日付選択helperとdate-bound testの存在からupdater effectを変更対象へ入れなかった。engineだけを変更したため、focused gateは16件成功・8件失敗だった。full gateはfail-stopにより未実行である。

focused failure後は「再修正に必要なupdater current contentを変更前evidenceから確実にbindできない」として停止した。保存された初回outputにはupdater sourceが含まれていたが、relation coverageとして利用されなかった。

公式failureは次の三点である。

- `required_changed_path_missing:src/domain/collection_history_updater.py`
- focused pytest failure
- full gate未実行

## 仮説の判定

C139 / C140監査では、限定取得3 / 3件が変更前に両effectを認識し、全体・過大取得0 / 7件が認識しなかった。C141を加えた計15件では次になる。

- 限定取得: 変更前の両effect認識 `7 / 7`、最終score `4`は`7 / 7`
- 全体・過大取得: 変更前の両effect認識 `0 / 8`、最終score `4`は`1 / 8`

観測相関は一件増えても維持された。一方、Candidate141自身は限定取得を4 / 5件に増やしただけで、全体取得分岐を0 / 5へ閉じていない。

次に同じ意味を強い表現で重ねても、新しい判断根拠は増えない。次Candidateを作る前に、C122でone-waveとterminal closureを一つのpredicateへ結合したことにより、relation coverageをbindできない場合でも「一waveで終端判断する」方が優先される構造を監査する。one-waveを維持するか、relation coverage未成立時だけ`prechange_evidence_wave_ready=false`として既存通常経路へ戻すかを、一つの分岐として切り分ける。

executor、output delivery、行数またはbytes上限は次案にしない。

## 状態

`f02_f04_f07_n5_evaluated / score_2_1_of_15 / quality_gate_failed / relation_coverage_4_of_5 / whole_target_fallback_1_of_5 / result_registered / stopped`

## 結論表

| case / gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4 / 2` | `4 / 1` | fail |
| F04 score `4` | `5 / 5` | pass |
| F07 score `4` | `5 / 5` | pass |
| 全体score `3`以下 | 1件 | stop |
| F02変更前に両effect未充足認識 | 4 / 5 | fail |
| F02 relation限定取得 | 4 / 5 | insufficient |
| F02全体取得 | 1 / 5 | residual branch |
| F02一target部分成果 | 1 / 5 | fail |
| 追加24件 / Standard14 | 未発行 | stopped |
