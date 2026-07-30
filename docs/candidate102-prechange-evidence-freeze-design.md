# Candidate102 変更前証拠集合の固定設計

## 結論

Candidate102はCandidate98を直接親とし、`SPEC`一規則だけを置換する。Candidate99からCandidate101までは失敗経路の観測証拠であり、prompt lineageには含めない。

制御対象は検索の禁止でもTaskSpecの非目標でもない。`spec_ready=true`になった時点で、変更前に未解決のpredicateと必要証拠のidentityを固定する。permission、allowed read、利用可能なtool、repository authorityの存在は、この集合へ新しい確認を追加しない。

## Identityと状態

- candidate number: Candidate102
- prompt identity: `the-caption-3ce91a4-prechange-evidence-freeze-r1`
- direct parent: `the-caption-3ce91a4-validation-completion-sheet-r1`
- bundle SHA-256: `bea40b133f2a97a1f0972aa30d858edadb8c5338be050dbb4e85771ec497634f`
- changed target: root `AGENTS.md`
- changed predicate: `SPEC`の置換
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate98とする。
2. Candidate99の`EVIDENCE_SCOPE`はrepository authorityを正当な入力として列挙し、command発行前のconsumer bindingを証跡化しなかった。
3. Candidate99の広い検索4件は、検索後に検証script、`src/AGENTS.md`、entrypoint、fixtureをrepository authorityとして説明した。未取得証拠と利用先を検索前には示していない。
4. Candidate100は情報源を分離したが、周辺gateを別の確認対象にできた。
5. Candidate101は追加調査の発火条件を置いたが、その条件が成立するかを調べる新しい責務を作り、広い検索が5 / 5へ増えた。
6. 共通する穴は、`spec_ready=true`の後もexecutorが変更前required evidence集合を増やせることである。
7. 置換するpredicateは、`spec_ready=true`時に未解決predicateとrequired evidence identityを固定する`SPEC`一つとする。
8. command名、検索path、F07の非目標はprompt本文へ入れない。
9. 品質と狙った経路はF07 r2、Rating v14、Medium、CLI `0.146.0`、設定上の`M=24`、`N=5`で確認する。
10. 5 / 5 score `4`、required command evidence 5 / 5、root-only、履歴参照0件、対象外を含む広い検索0件を必須とする。一件でも未達なら停止する。

## 変更する規則

```text
SPEC: 実行前にrequired outcomeをoperation identityへ分け、predicate / criterion owner /
permission / constraintをTaskSpecへ固定する。spec_readyの既存条件を維持する。
spec_ready=true時に変更前のunresolved predicate / required evidence identityを固定し、
permission / allowed read / available tool / repository authorityの存在だけでは追加しない。
変更前invocationは、そのresultを固定済みの未固定valueまたはunresolved predicateへ
consumerとして先にbindできる場合だけ発行する。target artifactのrequired readが
bind済みvalueまたはconstraintとの矛盾を観測した場合だけspec_ready=falseへ戻し、
追加evidence identityを再bindする。
```

## 非目標

- TaskSpecまたはF07 case文面の変更
- 読取path、command、tool回数の固定
- repository authorityの利用禁止
- executorまたはtool output配送の変更
- Candidate99からCandidate101の履歴artifactの書換え
- 採用、release、THE-CAPTION本体反映

## 評価境界

F07 targeted resultはStandard14の固定Layer 1 identityを維持し、model slot発行前にF07 iteration 1〜5をcoverageへbindする。TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameter、設定上の`M=24`はCandidate101と同じ値を使う。既存prompt setは再実行しない。targeted gate通過前にStandard14またはB20へ進めない。
