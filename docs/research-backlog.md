# 研究バックログ（未完了項目の索引）

現在**未完了**の研究項目を、着手判断のために一箇所へ集める索引。長期方針は[`future-roadmap.md`](future-roadmap.md)、系譜と観測は[`candidate-history.md`](candidate-history.md)を参照する。

この文書は索引であり、判定の正本ではない。各項目の状態・数値・停止理由は「正本」列のartifactを正とする。ここに載っていることは、着手済み・評価済み・採用予定のいずれでもない。

## 1. label監査の未完了（再測定にfresh runが必要）

`Candidate71`の11 label監査で「根拠なし」判定が**暫定**のまま残る3件。いずれも既存の保存データでは決着しない。正本は[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)の「監査状況の分類」表。

| 項目 | 必要な再測定 | 結論をflipし得るか |
| --- | --- | --- |
| `CONTEXT`（`X1`） | A06 paired diagnostic。新規A06 case variant、bundle、gate、fresh runが必要。既存archiveでは事前sizingも不可 | **あり**。拡張方向（packet resolved premiseによる再読削減）が未検証 |
| `INDEPENDENCE`（`I1` = `F9`） | A / D scopeでの削除評価。Candidate68はF10-onlyのみ実測でun-run | 低い。F10ではruntime非改善 |
| `RECOVERY`（`R1 / R2`） | `environment_recovery_max>0`の正のrecovery scenario caseでの評価。現Evaluation setは`not_applicable`でun-run | 不明（効果未測定） |

## 2. `PRODUCER`の`P3`一文削除candidate（作成前gate定義済み・bundle未作成）

11 label監査で唯一「Candidate作成根拠あり」となった項目。`P3`の正本は`OWNER_ROLE`側にあり、`PRODUCER`側の短い再記述だけを削除する。gate 9項目は定義済みで、bundle・profile・評価は未着手。

- 正本: [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)（`PRODUCER`監査結果節と作成根拠節）
- 評価計画: Candidate71から`P3`一文だけを削除し、D01正例＋root-onlyでtargeted評価。新しいEvaluation setやrating revisionは作らない
- **番号に注意**: 同分析が作業呼称として使う「Candidate74」は、実際には別軸の`the-caption-3ce91a4-typed-execution-state-machine-r1`へ割り当て済みである。着手時は[`prompts/candidates/README.md`](../prompts/candidates/README.md)で現行の番号割当てを確認し、新しい番号で作成する

## 3. A01の3択variation診断

**未実施。** A01の現行2択caseを回帰基準として維持したまま、3択以上の未固定modeを持つvariationを診断用に追加する。設計条件は次のとおり。

- 2択で非現行値を選び、3択では確認して停止するなら、補集合選択の可能性が高い。
- 3択でも特定値を選ぶなら、mode名の意味、候補順序、現在値、test期待値などをauthorityへ変換している可能性を調べる。
- 現在値と候補順序を回転し、曖昧なら停止するcaseとrepository authorityから一意に解決できるcaseを対にして、過剰停止と未指定値補完の両方を観測する。

case追加の一般規則（追加根拠の限定、既存revisionを上書きしないこと、反復数の固定）は[`future-roadmap.md`](future-roadmap.md)の「評価setの役割と育て方」節を正本とする。

## 4. 投影済みCandidate71のrisk（当時の記録と現在解釈を分離）

Candidate71は評価上`stopped`（v12の品質gate不通過）のまま、別の採用判断でTHE-CAPTION本体へ投影済みである。当時のrelease artifactに保存された未解決riskは2件で、これはimmutableな記録として取り消さない。一方、rating v13による現在解釈では、この2件の位置づけが分かれる。

| 当時のrelease risk（v12時点） | 観測 | rating v13後の現在解釈 |
| --- | --- | --- |
| A02で`git diff --check`欠落 | 3 / 90件 | **現在の未完了研究項目ではない。** 実行役へ提示していない特定コマンドを採点側が必須化した「要求と採点のずれ」であり、本物の品質低下と区別される。v13でこのずれを塞いだ |
| A01で未固定modeを確認せず実装・試験へ進んだ誤実行 | 1 / 90件 | **現在も残る品質上のrisk。** v13でも品質上の問題として扱う |

- 当時の未解決riskの正本: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)（v12結果は履歴として保持）
- 現在解釈の正本: [`control-mechanisms.md`](control-mechanisms.md)のrating v13節と[`a02-rating-divergence.md`](a02-rating-divergence.md)
- したがって研究項目として残るのはA01側の挙動である。A01の未固定mode確認は上記「3. A01の3択variation診断」と同じ論点に接続する

## 5. F10 location mismatch: exact coordinateのevidence interface（別軸）

**原因診断そのものは実施済みで、prompt側の変更は停止している。** `CLAIM_PROVENANCE` collectorと90件backfillの後、30件checkpoint診断（`max_30_diagnostic_valid_without_location_mismatch`で停止）、追加105件、coordinate representation診断、delayed reconstruction診断、implicit coordinate passive case-control、real-Agent representation recency診断、recorded-state collision受動監査まで到達した。

正本の現在判断は、repository-wideに削除できるprompt判断点を確認できないため、**prompt変更と追加model runをここで止める**ことである。残る未完了項目は次の一点。

- exact coordinateがhard requirementである場合に限り、modelが選んだexact line textをdeterministicなsource indexでone-based coordinateへ変換する**evidence interface要件を別軸で検討**する。prompt制御の変更軸としては扱わない。
- 正本: [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md)（「対策判断への接続」節と各診断結果節）
- 制御graph側の判断（location mismatchを理由にroot規則を追加しない）は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)を参照

## 6. 現行rating contract identityの確定（解決済み・2026-07-25）

新規runへ適用する現行rating contractの指定が、評価基盤の正本（`owner-producer-quality-v8`）と後続文書（最新revision v13）で一致していなかった。**2026-07-25に現行をv13へ確定した。** 正本[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)の指定、評価実行手順[`evaluation-loop-manual.md`](evaluation-loop-manual.md)のLayer 3、契約台帳[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)、および`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`をv13へ追従させ、v13 capsuleが受理されることをunit testで確認済みである。この項目は未完了ではない。

派生して残る作業は次の一点である。

- **v13での最初の評価run**は未実施である。互換比較できる最新のresult集合はv12（Candidate71 / Candidate74 / Candidate77の標準14項目・B18）であり、v13 runを実施した後もv12以前のresultを同一comparisonへ混ぜない。

## 7. `QUALITY_RATING`という汎用名がv8を指している（保守上の誤認risk）

`scripts/evaluation_loop.py`では現行契約が`QUALITY_RATING_V13`として登録されている一方、revision名を持たない汎用定数`QUALITY_RATING`は`owner-producer-quality-v8`を指し続けている。integration testの既定`quality_rating`もこの定数を使う。

- **実行上の不具合ではない**。run capsuleは`quality_rating`の明示指定を必須とし、v13は`SUPPORTED_QUALITY_RATINGS`へ登録済みで、v13の実挙動はunit testで検証している。
- 残るのは保守上のriskで、汎用名が現行契約を表すように見えるため、将来の変更時にv8を現行と誤認し得る。
- 解消するにはv8定数の改名（例: `QUALITY_RATING_V8`）とtest既定値の見直しが必要で、複数testの既定経路へ波及する。現行identityの確定（項目6）とは別の判断単位として扱う。

## 着手時の共通条件

- 一つのcandidateで一つのpredicateまたは一つの変更軸だけを扱う（[`prompts/AGENTS.md`](../prompts/AGENTS.md)のcandidate作成前gate9項目）
- 設計原則の正本は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 評価・採用・release・projectionは別gateとして記録する（[`repository-contract.md`](repository-contract.md)）
