# Candidate127 F02 / F04 / F07逐次N=100追試停止結果

## 結論

Candidate127をF02、F04、F07 dependencyの順に、既存N=5へ24件ずつ追加して各case N=100まで延長する追試は、最初のF02 batchで停止した。

F02の追加24件は24 / 24 valid、controller error 0、excluded 0だった。score分布は`4 / 2 = 22 / 2`である。score `2`が2件発生したため、ユーザー指定の「score 3以下で停止」に従い、F02の次batch、F04、F07は一件も発行していない。

既存F02 N=5と追加24件を固定した正式なN=29 resultは、score `4 / 2 = 27 / 2`である。現在状態を`f02_n29_evaluated / quality_gate_failed / stopped_before_f04_f07 / result_registered`とする。

## 実行条件と順序

- candidate: `the-caption-3ce91a4-failed-change-salvage-r1`
- bundle SHA-256: `75d37043e6efbcb91bf4e097e80f38f88e73ca7e05d42273b71c172832d2eba9`
- evaluation set: `the-caption-standard14-r1` revision `r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured max workers: `M=24`
- requested case order: F02 → F04 → F07 dependency
- requested targets per case: N=`29` → `53` → `77` → `100`
- planned new slots: `24` → `24` → `24` → `23`
- stop condition: 新規batchにscore `3`以下が一件以上

`N`、coverage、iteration集合はatomic runの実行互換条件へ入れず、dispatchと集計provenanceとして固定した。prompt、case、fixture、TaskSpec、rating、model、reasoning、runtime、CLI、permission、executor挙動、token accountingは既存N=5と機械照合した。

## F02追加24件

- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` revision `r1`
- existing run: 5件
- new run: 24件
- target count: N=29
- valid / excluded / controller error: `24 / 0 / 0`
- controller elapsed: `155.430秒`
- batch score分布: score `4` 22件、score `2` 2件
- archive SHA-256: `a197f70d5b0a3b86be0540dfd261ed79756955806cf8ddf51264a000da7d9ddd`
- seal SHA-256: `790cc8e453f3617df4423d1d996835c263a217af60f122ef56c3dc8b7059ff7d`

score `2`は次の2件だった。

| run ID | batch iteration | score | 観測された未達 |
|---|---:|---:|---|
| `352352e56b7b4bdaa0565cf048c2e445` | 13 | 2 | updater path未変更、focused pytest失敗、full gate未実施 |
| `e88c0aad89aa4167bbc97fb49505de39` | 4 | 2 | updater path未変更、focused pytest失敗、full gate未実施 |

2件は同じ最終状態だった。`src/app/v4_engine.py`では`refresh()`へ`target_date`と`us_market_date`を渡す変更を適用した。一方、`src/domain/collection_history_updater.py`の変更はcurrent contentとの不一致で適用できず、最終diffに含まれなかった。

focused gateは2件とも`8 failed, 16 passed`だった。失敗はupdaterがyfinanceへend dateを渡さず、関連するAlpha Vantage fallbackも作動しないことを示した。focused gate失敗後はTaskSpecどおり`bash scripts/dev/main_verify.sh`を実行せず停止した。

これはF04で通過した「失敗した不要変更を捨て、独立した必要変更だけを救う」経路とは異なる。F02では二つのfile変更が同じ成果条件を共同で満たす。片方だけを救済しても成果が成立しないため、最終状態は部分成果になった。

## N=29登録結果

- Candidate127 F02 pool: `1d47dc0f208f0d51143361d05c50c8627ad2be1201bcbb7b0818b64bfba54792`
- selection: `7b5777ebbabe4d0ca7da78e0a41f1594`
- analysis: `42261fead6cc4167aff9e76a88b60874`
- result: `14b34e112ad74ab4a5f21b448c9352e8`
- compatibility key: `26034960b99f5a2eaf724a99b3ea313e3fec9df74336c4b7db2f25c4afe06049`
- score分布: score `4` 27件、score `2` 2件
- quality中央値: `100`
- all-agent token中央値: `122,569`
- elapsed中央値: `77.557秒`

中央値がquality `100`でも、score `2`が2件存在するため品質gate通過を意味しない。

## 発行しなかった試験

- F02 N=53、N=77、N=100: 未発行
- F04追加試験: 未発行
- F07 dependency追加試験: 未発行

F04とF07の既存N=5 resultは変更していない。今回の停止結果はCandidate127の既存Standard14 N=5 70 / 70 score `4`を履歴上書きせず、追加stability evidenceとして別状態で保持する。

## 実行前停止したcampaign

最初の準備campaign `...20260801-r1`はevaluation slotを0件も発行せず停止した。F02単独reference resultがF02 fixtureだけを持つ一方、comparison source Layer 1がStandard14全14caseのfixture集合を持ち、実行前gateが不一致を検出したためである。

このLayer 1は上書きしなかった。Standard14 referenceから全fixture identityを継承したF02 / F07単独reference resultを新規登録し、別campaign identity `...20260801-r2`でpreflightをやり直した。r2だけが評価slotを発行した。
