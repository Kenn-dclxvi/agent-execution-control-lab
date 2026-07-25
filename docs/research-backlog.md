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

A01の現行2択caseを回帰基準として維持したまま、3択以上の未固定modeを持つvariationを診断用に追加できる。補集合選択か、mode名・候補順序・現在値・test期待値のauthority化かを切り分ける目的。

- 正本: [`future-roadmap.md`](future-roadmap.md)の「評価setの役割と育て方」節（設計条件を記載）
- 未実施。追加の根拠・対にするcase設計・反復条件は同節に従う

## 4. 投影済みCandidate71に残る未解決risk

Candidate71は評価上`stopped`（品質gate不通過）のまま、別の採用判断でTHE-CAPTION本体へ投影済みである。次の2件は取り消されていない。

| 未解決risk | 観測 |
| --- | --- |
| A02で`git diff --check`欠落 | 3 / 90件 |
| A01で未固定modeを確認せず実装・試験へ進んだ誤実行 | 1 / 90件 |

- 正本: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)
- A02の「要求と採点のずれ」自体はrating v13で整理済み。整理の経緯は[`repository-overview.md`](repository-overview.md)のA02採点節、rating契約は[`control-mechanisms.md`](control-mechanisms.md)の参照先を正本とする

## 5. F10 location mismatchの原因診断

Candidate41 B18などで観測したF10のfinding location誤差は、prompt境界へ直ちに変換せず、誤差の発生段階を識別する診断を先に置く方針。診断の最初の対象はprompt規則ではなく、model-visible入力を変えない記録`CLAIM_PROVENANCE`である。

- 正本: [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md)
- 制御graph側の判断（location mismatchを理由にroot規則を追加しない）は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)を参照

## 着手時の共通条件

- 一つのcandidateで一つのpredicateまたは一つの変更軸だけを扱う（[`prompts/AGENTS.md`](../prompts/AGENTS.md)のcandidate作成前gate9項目）
- 設計原則の正本は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 評価・採用・release・projectionは別gateとして記録する（[`repository-contract.md`](repository-contract.md)）
