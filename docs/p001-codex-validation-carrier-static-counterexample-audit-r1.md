# P001後続 Codex validation carrier静的反例監査 r1

> [!IMPORTANT]
> **状態**: `management_draft_audited / static_cases_9 / initial_blocking_edges_3 / repaired_in_same_draft / remaining_blocking_counterexample_0 / candidate_not_created / evaluation_not_started`
>
> 本書は管理用composition draftのpermissionとdependencyを静的に監査した記録である。model実行、評価result、効率改善、Candidate、採用、releaseまたはprojectionではない。

## 結論

初回r2 draftには三つのblocking edgeがあった。

1. required validationが0件でも空planをcarrierへbindできた。
2. nested executionとcontinuationだけが利用可能なsurfaceを、7 capabilityが揃ったcarrierとして開始できた。
3. required terminal evidenceの観測元がcarrierから見えなくても開始でき、evidenceの補完または追加readへ進めた。

`validation-carrier-codex-r2`のadmissionだけを修正し、required validation非空、7 capability全件の同一identity binding、必要evidenceとdocumented result fieldの事前bindingを要求した。修正後の静的Case 9件にblocking counterexampleはない。

この修正は成功runのtool順を追加していない。carrierへ入れる前のpermissionを狭め、能力または観測fieldが欠ける場合を`unavailable`へ閉じただけである。

## 監査対象

対象は次の三componentを一枚へrenderする管理用manifestである。

- `validation-plan-semantics-r2`
- `validation-result-closure-r2`
- `validation-carrier-codex-r2`

共通semantic component二件、validation以外の共有component、既存P001、Candidate bundleおよび評価artifactは変更しない。

## Case別結果

| Case | 固定状態 | 必要なroute | 閉じる誤route | 初回 | 修正後 |
| --- | --- | --- | --- | --- | --- |
| VCR-S01 validationなし | required validation 0件 | carrierを開始しない | 空planの発行と不要なterminal projection | `counterexample_found` | `no_counterexample_found` |
| VCR-S02 全件success | 二件、個別method・pass condition・evidence field bind済み | 一carrier内の個別resultをterminalで一度投影 | 各result後のmodel再入、追加validation | なし | `no_counterexample_found` |
| VCR-S03 途中non-success | 第二resultがnon-success、第三は第二へ依存 | 第二resultを保持し第三を未発行にする | 第三発行、全件success補完、第二再実行 | なし | `no_counterexample_found` |
| VCR-S04 nonterminal継続 | nested resultがcontinuation identityを返す | 同じidentityだけをterminalまで継続 | 別operation、別identity、途中報告 | なし | `no_counterexample_found` |
| VCR-S05 continuation identity欠落 | nested resultはnonterminalだがidentityを観測不能 | 個別resultを`unavailable`にする | identity推測、別execution、terminal補完 | なし | `no_counterexample_found` |
| VCR-S06 capability部分集合 | executionとcontinuationはあるがintermediate ingress denialがない | validation operationを`unavailable`にする | 部分能力でcarrier開始、model loopへのfallback | `counterexample_found` | `no_counterexample_found` |
| VCR-S07 evidence field欠落 | required evidenceはあるがdocumented result fieldへbind不能 | 開始前に`unavailable`にする | evidence捏造、carrier外の追加read、raw outputから事後選択 | `counterexample_found` | `no_counterexample_found` |
| VCR-S08 raw output過剰投影 | terminal statusと必要evidence以外のraw outputが存在 | 固定schemaの必要fieldだけを一度投影 | issued output全件のcompletion result化 | なし | `no_counterexample_found` |
| VCR-S09 carrier後fallback | carrier terminalまたは途中failureを受領 | 同じplanを一度だけ結果消費へ渡す | modelへ戻る個別validation routeで再開 | なし | `no_counterexample_found` |

## 5つの誤経路の閉鎖

| 誤経路 | 閉じるboundary |
| --- | --- |
| 途中result漏出 | `intermediate_ingress_denial`をcarrier admissionの必須能力にし、plan nonterminal中のmodel-visible outputを禁止する |
| 失敗後発行 | 固定済みstop dependencyに従い、non-successまたは`unavailable`に依存する後続nested invocationを発行しない |
| identity消失 | nonterminalは同じcontinuation identityだけを許可し、観測または指定不能なら補完せず`unavailable`にする |
| 過剰投影 | 開始前にterminal schemaと必要evidence fieldをbindし、それ以外のraw outputをterminal resultへ昇格させない |
| model loopへのfallback | capability集合欠落時とcarrier terminal後の双方で、個別model発行routeへの切替を禁止する |

## 保持した正常route

- required validationがなければcarrierを読まずに既存completionへ進む。
- required validationがあり全capabilityをbindできれば、個別identity、固定順、個別pass conditionおよびfailure診断を保持する。
- non-successは隠さずterminal statusとして投影し、依存しない既存operationへ停止効果を広げない。
- nonterminalは同じidentityで継続し、identityを観測できない場合だけ当該validationを`unavailable`にする。
- terminal outputは一度だけ結果消費側へ渡す。

## 修正範囲と意味保持

修正したのは`validation-carrier-codex-r2`の先頭二statementだけである。共通semantic primitive 15件の対応は変えず、platform capability文を新しいC147 primitiveとして数えない。validation以外66 primitiveのcomponent bytesも変更しない。

修正後のrender結果は12,922 bytes、SHA-256 `999d409cd90b83408739d0140ddb5dc4e052f5af40bc603834553df5a6a0ad0b`である。bytes増加は効率改善を示さない。今回の判定対象は誤routeの静的到達可能性だけである。

## 次のgate

静的反例0件だけではCandidateを作らない。次はCandidate作成前設計として、次を固定する。

1. 直接の基準、P001の診断証拠としての役割、C147から保持する意味、r2だけの差分。
2. 上記9 Caseのうち本文作成に使ったCaseと、本文固定後に作る新しい未見Caseの分離。
3. 品質、途中model ingress、model response数、token、elapsedを別々に判定するtargeted gate。
4. capability receiptが比較Profileの互換条件へ入ることと、欠落時に評価slotを発行しないpreflight。
5. 一件でも意味欠落、正常route後退、途中ingress、過剰投影またはfallbackがあれば停止する条件。

このgateを固定するまで、P002、prompt identity、Profile、dispatch planまたは評価slotを作成しない。
