# Candidate100 成果値と現在状態の境界設計

## 結論

Candidate100はCandidate98を直接親とし、`OUTCOME_SOURCE`を一規則だけ追加する。Candidate99は失敗経路を確認した観測証拠として参照し、prompt lineageには含めない。

制御対象は読取可能な証拠の広さではない。TaskSpecが固定した成果値、repository authorityが固定する未決値と制約、対象artifactが示す現在状態の役割を分ける。成果値と現在状態から変更predicateが一意になった時点で、変更前調査を終了する。

## Identityと状態

- candidate number: Candidate100
- prompt identity: `the-caption-3ce91a4-outcome-source-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-completion-sheet-r1`
- bundle SHA-256: `b4c260e5c18c8b5fdc3d005fe931f531c4328a222111f0522d33f0ba71683df3`
- changed target: root `AGENTS.md`
- changed predicate: `OUTCOME_SOURCE`の追加
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate98とする。
2. 基準状態の最短正常経路は、TaskSpecの成果値と対象artifactの現在状態を比較し、変更predicateを一意にして修正し、固定済み検証票で完了する経路である。
3. Candidate99 F07 N=5では、同じTaskSpecとfixtureに対して対象外を含む広い検索を4 / 5、履歴参照を1 / 5で観測した。
4. 成功したiteration 4はTaskSpecと対象artifactだけで変更predicateを確定した。他の4件は正規値をrepository authority、test、検証scriptまたは履歴で再確認した。
5. 5件とも同じ1行を変更し、required validationを満たしてscore `4`だった。追加検索は成果品質に必要ではなかった。
6. `EVIDENCE_SCOPE`はrepository authorityを許可入力として並列に置き、bind済み入力が十分かをexecutor自身へ委ねたため、成果値の再確認を止められなかった。
7. 追加するpredicateは、各情報源の役割と変更前調査の終了条件を定める`OUTCOME_SOURCE`一つとする。
8. 消す判断点は、TaskSpecで固定済みの成果値をrepository authorityから再決定または再確認するかという分岐である。
9. 新たに増える判断点は、成果値と現在状態だけでは変更predicateを一意にできない場合の`missing fact / consumer predicate`固定だけである。
10. 品質と狙った経路はF07 r2、Rating v14、Medium、CLI `0.146.0`、設定上の`M=24`、`N=5`で確認する。
11. 5 / 5 score `4`、required command evidence 5 / 5、root-only、履歴参照0件、対象外を含む広い検索0件を必須とする。一件でも未達なら停止する。

## 変更する規則

```text
OUTCOME_SOURCE: 明示user inputからTaskSpecへbind済みのrequested outcome valueを
repository authorityで再決定 / 再確認しない。repository authorityはTaskSpecが
authorityへ委ねた未固定value / constraintだけをbindし、target artifactはcurrent
stateだけを供給する。bind済みoutcome valueとcurrent stateから変更predicateが
一意なら変更前調査を終了する。判定不能な場合だけmissing factとconsumer
predicateを先にbindして追加入力する。
```

## 非目標

- TaskSpec、repository authority、required validationの変更
- tool、read、message、tokenの上限設定
- 特定case、path、commandのprompt本文への列挙
- executorまたはtool output配送の変更
- Candidate99の履歴artifactの書換え
- 採用、release、THE-CAPTION本体反映

## 評価境界

F07 targeted resultはStandard14の固定Layer 1 identityを維持したまま、実行前にF07とiteration 1〜5をcoverageとしてbindする。登録器はbound coverage外のslotを拒否し、Layer 4はbound coverage全件が揃った場合だけresultを登録する。

TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameter、設定上の`M=24`はCandidate99と同じ値を使う。Candidate81またはCandidate99を再実行しない。targeted gate通過前にStandard14またはB20へ進めない。
