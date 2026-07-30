# Candidate101 追加調査の発火条件設計

## 結論

Candidate101はCandidate98を直接親とし、`METHOD`一規則だけを置換する。Candidate99とCandidate100は失敗経路の観測証拠であり、prompt lineageには含めない。

制御対象は検索回数や読取pathではない。TaskSpecと適用済みrepository authorityから変更対象、期待値、許可artifactが一意で、対象内の単一最小変更で成果条件を満たせる間は変更へ進む。追加調査は、実際に曖昧さ、複数artifactへの波及、固定済み制約との矛盾、変更起因の検証失敗を観測した場合だけ開始する。

## Identityと状態

- candidate number: Candidate101
- prompt identity: `the-caption-3ce91a4-additional-investigation-trigger-r1`
- direct parent: `the-caption-3ce91a4-validation-completion-sheet-r1`
- bundle SHA-256: `b31f2156e599319bd243ad5487453b83297d149654f15e58c6a0b5c84d3056e9`
- changed target: root `AGENTS.md`
- changed predicate: `METHOD`の置換
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate98とする。
2. 基準状態の最短正常経路は、開始identity、適用規則、対象artifactを確認し、TaskSpecで固定済みの一行を修正してrequired validationへ進む経路である。
3. Candidate99とCandidate100のF07 N=5は、いずれも対象外を含む広い検索を4 / 5で観測した。
4. Candidate100は成果値の情報源を分離したが、runner gate、fixture、検証script、局所authorityを別の確認対象とする分岐を閉じなかった。
5. 独立サブエージェント診断ではrepository全体、tests、scripts本文、Git履歴を検索せず、root `AGENTS.md`と`run.sh`だけで一行修正へ進んだ。
6. 同診断の事後聞き取りでは、「既存routing全体の新規監査は要求しない」「誤ったmappingだけを最小修正」「正しい値がTaskSpecで固定済み」の順で追加調査を止める判断へ強く作用した。
7. 同診断は`.venv`欠落でrequired validationを完了しておらず、C81またはCandidate100 bundleによる正式評価でもない。機構の設計根拠に限定し、効果の証明には使わない。
8. 置換するpredicateは、追加調査を具体的な観測へbindする`METHOD`一つとする。
9. 新たに増える判断点は、四つの発火条件のどれを実際に観測したかだけである。
10. 品質と狙った経路はF07 r2、Rating v14、Medium、CLI `0.146.0`、設定上の`M=24`、`N=5`で確認する。
11. 5 / 5 score `4`、required command evidence 5 / 5、root-only、履歴参照0件、対象外を含む広い検索0件を必須とする。一件でも未達なら停止する。

## 変更する規則

```text
METHOD: TaskSpec明示手段だけを固定する。未固定手段はpredicateを変えずpermission内で
executorが選ぶ。invocationのfailed / unavailableをpermission否定 / terminalにせず、
未固定手段があれば同一predicateへ向けて継続する。明示禁止 / permission否定は停止し、
回避しない。変更前はstart gateと適用repository authorityの確認後、TaskSpecがtarget /
requested value / allowed artifactを一意にbindし、target内の単一最小変更でpredicateを
満たせるなら変更へ進む。追加調査は曖昧さ / 複数artifactへの波及 / bind済みconstraint
との矛盾 / 変更起因のvalidation failureを観測した場合だけ、その観測と未決predicateへ
scopeをbindして発行する。一般的安全確認 / 念のため / 既存経路全体の再監査だけでscopeを
広げない。
```

## 非目標

- TaskSpec、repository authority、required validationの変更
- tool、read、message、tokenの上限設定
- 特定case、path、commandのprompt本文への列挙
- executorまたはtool output配送の変更
- Candidate99またはCandidate100の履歴artifactの書換え
- 採用、release、THE-CAPTION本体反映

## 評価境界

F07 targeted resultはStandard14の固定Layer 1 identityを維持したまま、実行前にF07とiteration 1〜5をcoverageとしてbindする。登録器はcoverage外のslotを拒否し、Layer 4はbind済み5 slotが揃った場合だけresultを登録する。

TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameter、設定上の`M=24`はCandidate100と同じ値を使う。Candidate81、Candidate98、Candidate99、Candidate100を再実行しない。targeted gate通過前にStandard14またはB20へ進めない。
