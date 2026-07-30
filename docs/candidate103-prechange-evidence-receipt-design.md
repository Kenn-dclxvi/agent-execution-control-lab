# Candidate103 変更前実行票の可視化設計

## 結論

Candidate103はCandidate98を直接親とし、`SPEC`一規則だけを置換する。Candidate99からCandidate102までは失敗経路の観測証拠であり、prompt lineageには含めない。

制御対象は検索pathや回数ではない。最初のinvocation前に、変更前invocation、そのresultを利用するTaskSpec固定済みの未解決判断、resultによって変わる後続判断をmodel-visibleな`PRECHANGE_RECEIPT`へ固定する。結果で判断が変わらない呼出しは発行対象にしない。

## Identityと状態

- candidate number: Candidate103
- prompt identity: `the-caption-3ce91a4-prechange-evidence-receipt-r1`
- direct parent: `the-caption-3ce91a4-validation-completion-sheet-r1`
- bundle SHA-256: `e3acc82d0712db6c2834dc69d154a50f470cc119db2db0bb2ed1ceb6cbfede8f`
- changed target: root `AGENTS.md`
- changed predicate: `SPEC`の置換
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate98とする。
2. 基準状態の最短正常経路は、開始identityと変更対象を確定し、変更、required validation、完了証拠の順に進む経路である。
3. Candidate102は品質5 / 5、履歴参照なし5 / 5を維持したが、対象外を含む広い検索なしは2 / 5だった。
4. Candidate102の3件は`spec_ready=true`と説明した後も周辺pathを検索した。内部的な証拠集合はcommand発行前の証跡にならず、検索後にconsumerを説明し直せた。
5. 既存TaskSpec、repository authority、repository stateは必要な成果を固定するが、内部bindingを観測可能にはしない。
6. 置換するpredicateは、変更前invocationとconsumerを最初のinvocation前に出力する`SPEC`一つとする。
7. 新たな判断点は、各receipt itemのresultが後続判断を変えるかという一つである。receipt自体を外部executor artifactにはしない。
8. command名、検索path、特定caseの非目標はprompt本文へ入れない。
9. 品質と狙った経路はF07 r2、Rating v14、Medium、CLI `0.146.0`、設定上の`M=24`、`N=5`で確認する。
10. 5 / 5 score `4`、required command evidence 5 / 5、root-only、履歴参照なし5 / 5、対象外を含む広い検索なし5 / 5を必須とする。一件でも未達なら停止する。

## 変更する規則

```text
SPEC: 既存のTaskSpec固定とspec_ready条件を維持する。
spec_ready=true後の最初のinvocation前に、変更前invocationごとのidentity、
TaskSpec固定済みの未固定valueまたはunresolved predicateであるconsumer、
resultにより変わる後続判断をPRECHANGE_RECEIPTとしてmodel-visible responseへ一度出力する。
固定済みconsumerへbindできないinvocation、先行result受領後も後続判断を変えないinvocation、
receiptにない変更前invocationは発行しない。receipt済みresultがbind済みvalueまたはconstraintを
失効させた場合だけ、失効resultと追加consumerを示してreceiptを改訂する。
permission、allowed read、available tool、repository authorityの存在だけでは追加しない。
```

## 非目標

- TaskSpecまたは評価case文面の変更
- 読取path、command、tool回数の固定
- repository authorityの利用禁止
- executor、開発環境、tool output配送による外部receiptの追加
- Candidate99からCandidate102の履歴artifactの書換え
- 採用、release、THE-CAPTION本体反映

## 評価境界

F07 targeted resultはStandard14の固定Layer 1 identityを維持し、model slot発行前にF07 iteration 1〜5をcoverageへbindする。TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameter、設定上の`M=24`はCandidate102と同じ値を使う。既存prompt setは再実行しない。targeted gate通過前にStandard14またはB20へ進めない。
