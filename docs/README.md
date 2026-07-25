# docs 索引

`docs/`配下の研究文書を、読む前に**役割で選べる**ようにするための索引。文書は次の4分類で位置づける。

| 分類 | 意味 | 扱い |
|---|---|---|
| **正本（canonical）** | 他文書が参照authorityとして引く契約・原則 | 統合・要約せず維持。正本指定は各領域の`AGENTS.md`（下表参照） |
| **現在の研究状態** | 入口・全体像・横断知見・現行frontier・運用spec | 現在地点を把握する起点 |
| **完了済み研究記録** | 特定Candidate・比較・診断の成果artifact | 当時のresult・scoreを保持（遡及書換なし） |
| **historical／superseded** | root-only履歴、完了済みhandoff、旧design input | 現行設計として読まない。冒頭バナーで位置づけ |

分類間の原則は[`AGENTS.md`](AGENTS.md)を正とする（現在状態・当時の評価・後続の再解釈を混ぜない／過去result・scoreを削除しない／現在解釈は注記か別文書として追加）。

---

## 1. 正本（canonical）

参照先として維持する。統合・要約・全文複製の対象にしない。「正本指定元」列は、その正本性を明示するinstructionを示す。

| 文書 | 役割 | 正本指定元 |
|---|---|---|
| [`repository-contract.md`](repository-contract.md) | リポジトリ契約の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md) | 評価基盤のLayerと境界の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`evaluation-loop-manual.md`](evaluation-loop-manual.md) | 評価実行方法の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-control-design-principles.md`](prompt-control-design-principles.md) | prompt制御の設計原則の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-file-bundle.md`](prompt-file-bundle.md) | prompt file bundle形式・manifest・格納の正本 | [`scripts/AGENTS.md`](../scripts/AGENTS.md) |

## 2. 現在の研究状態

### 2a. 入口・全体像

| 文書 | 役割 |
|---|---|
| [`repository-overview.md`](repository-overview.md) | 初見向けの全体像（入口） |
| [`future-roadmap.md`](future-roadmap.md) | 長期方針と発展方向（恒久的な方針のみ） |
| [`research-backlog.md`](research-backlog.md) | 未完了研究項目の索引（label監査の再測定、`P3`削除candidate、A01 variation、未解決risk）。判定の正本は各リンク先 |
| [`candidate-history.md`](candidate-history.md) | Candidate系譜と知見の索引。系譜と現在状態の一覧は[`prompts/candidates/README.md`](../prompts/candidates/README.md) |
| [`public-target-selection-phase0.md`](public-target-selection-phase0.md) | 公開target選定Phase 0の実測記録と判定（`pallets/click`をPhase 1候補とした根拠） |

### 2b. 横断知見・現行frontier

| 文書 | 役割 |
|---|---|
| [`control-mechanisms.md`](control-mechanisms.md) | 横断的な制御メカニズムの知見 |
| [`execution-control-research-paper.md`](execution-control-research-paper.md) | 研究成果の総説（論文形式）。実測値の要約と2026年7月ベンダ公式指針（GPT-5.6 Sol / Claude Opus 5）との対照。**正本ではない**。数値・状態の正本は同文書が示す一次artifact |
| [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md) | C71 control abstraction分析（11 label監査台帳＋現在の結論）。現在の総括は同文書の「監査状況の分類」表を正とする |

### 2c. 運用・評価infra spec

| 文書 | 役割 |
|---|---|
| [`THE-CAPTION_execution-control_revision-instructions.md`](THE-CAPTION_execution-control_revision-instructions.md) | execution control修正指示（invocation_status等の定義） |
| [`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md) | 評価storageの維持・GC |
| [`desktop-evaluation-slot.md`](desktop-evaluation-slot.md) | desktop評価slotの前提条件 |
| [`shared-python-runtime.md`](shared-python-runtime.md) | 共有Python runtime |
| [`typed-boundary-evidence.md`](typed-boundary-evidence.md) | typed boundary evidenceのspec |
| [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md) | Layer 2 executorをClaude Code CLIへ置き換える試験方法の設計検討（未実装。未確定事項を含む） |

## 3. 完了済み研究記録

### 3a. Candidate設計記録

各Candidateの制御軸を記録した成果artifact。当時のresult・scoreは遡及変更しない。

正本はlifecycle軸ごとに分かれる。**identityは各bundleの`manifest.json`**、**評価状態は評価・診断を実施済みなら独立したevaluation / diagnostic result、未実施の`not_evaluated`は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列**、**release・approval・runtime projectionは[`prompts/releases/README.md`](../prompts/releases/README.md)**を正本とする。系譜と現在状態の一覧はcandidate indexにある。この索引は制御軸だけを示し、状態は複製しない（`docs/AGENTS.md`「同じ説明を複数文書へ全文複製せず正本へリンク」）。評価と採用、releaseとprojectionは別状態である（[`repository-contract.md`](repository-contract.md)、[`AGENTS.md`](AGENTS.md)）。

> **本体投影と評価状態は別軸**: 本体へ投影済みなのはCandidate41・Candidate43・Candidate71で、この順に積み上げた投影の直近はCandidate71である（3件いずれもrelease status `projected` / approval `approved` / runtime projection `projected`。実変更範囲はCandidate41が8 path、Candidate43とCandidate71は各々直前投影からroot `AGENTS.md`一つ。正本は[`prompts/releases/README.md`](../prompts/releases/README.md)と各release README）。ただしこれは採用判断側の状態であり、candidate評価状態とは一致しない。特にCandidate71のcandidate評価状態は`standard14_b18_evaluated / stopped`（[`candidate71-validation-closure-design.md`](candidate71-validation-closure-design.md)）であり、効率削減を根拠とする別の採用判断でreleaseがprojectedになった。評価停止は取り消されていない。

| Candidate | 文書 | 制御軸 |
|---|---|---|
| C43 | [`candidate43-control-element-classification.md`](candidate43-control-element-classification.md) | 制御要素の目的別分別（F/A系分類） |
| C45 | [`candidate45-judgment-authority-boundary-design.md`](candidate45-judgment-authority-boundary-design.md) | 判断成立責任境界 |
| C46 | [`candidate46-resolved-premise-input-boundary-design.md`](candidate46-resolved-premise-input-boundary-design.md) | 解決済み前提入力境界 |
| C47 | [`candidate47-applicability-domain-boundary-design.md`](candidate47-applicability-domain-boundary-design.md) | 適用域境界 |
| C48 | [`candidate48-premise-dependency-boundary-design.md`](candidate48-premise-dependency-boundary-design.md) | 前提依存境界 |
| C49 | [`candidate49-explicit-delegation-control-boundary-design.md`](candidate49-explicit-delegation-control-boundary-design.md) | 明示委譲制御境界 |
| C50 | [`candidate50-root-read-batch-design.md`](candidate50-root-read-batch-design.md) | root read batch |
| C51 | [`candidate51-root-operation-completion-boundary-design.md`](candidate51-root-operation-completion-boundary-design.md) | root operation completion境界 |
| C52 | [`candidate52-root-independence-boundary-design.md`](candidate52-root-independence-boundary-design.md) | root independence境界 |
| C53 | [`candidate53-purpose-separated-operation-graph-design.md`](candidate53-purpose-separated-operation-graph-design.md) | 目的分離operation graph |
| C54 | [`candidate54-evidence-backed-control-core-design.md`](candidate54-evidence-backed-control-core-design.md) | evidence-backed control core |
| C55 | [`candidate55-prebound-operation-graph-design.md`](candidate55-prebound-operation-graph-design.md) | prebound operation graph |
| C55 | [`candidate55-route-efficiency-gate-r2.md`](candidate55-route-efficiency-gate-r2.md) | route efficiency gate（r2追試） |
| C56 | [`candidate56-resolved-fixed-read-boundary-design.md`](candidate56-resolved-fixed-read-boundary-design.md) | resolved fixed read boundary |
| C57 | [`candidate57-task-enumerated-read-boundary-design.md`](candidate57-task-enumerated-read-boundary-design.md) | task-enumerated read boundary |
| C58 | [`candidate58-purpose-bound-read-route-design.md`](candidate58-purpose-bound-read-route-design.md) | purpose-bound read route |
| C59 | [`candidate59-read-only-operation-batch-design.md`](candidate59-read-only-operation-batch-design.md) | read-only operation batch |
| C60 | [`candidate60-operation-method-capsule-design.md`](candidate60-operation-method-capsule-design.md) | operation method capsule |
| C61 | [`candidate61-atomic-spec-operation-gate-design.md`](candidate61-atomic-spec-operation-gate-design.md) | atomic SPEC operation gate |
| C62 | [`candidate62-task-closed-read-route-design.md`](candidate62-task-closed-read-route-design.md) | task-closed read route |
| C63 | [`candidate63-fixed-evidence-route-projection-design.md`](candidate63-fixed-evidence-route-projection-design.md) | fixed evidence route projection |
| C64 | [`candidate64-self-contained-execution-paths-design.md`](candidate64-self-contained-execution-paths-design.md) | self-contained execution paths |
| C65 | [`candidate65-shared-operation-core-design.md`](candidate65-shared-operation-core-design.md) | shared operation core |
| C66 | [`candidate66-topology-preserving-compression-design.md`](candidate66-topology-preserving-compression-design.md) | topology-preserving compression |
| C67 | [`candidate67-cross-label-predicate-deduplication-design.md`](candidate67-cross-label-predicate-deduplication-design.md) | cross-label predicate deduplication |
| C68 | [`candidate68-independent-review-operation-removal-design.md`](candidate68-independent-review-operation-removal-design.md) | independent review operation removal |
| C69 | [`candidate69-model-reentry-decision-boundary-design.md`](candidate69-model-reentry-decision-boundary-design.md) | model reentry decision boundary |
| C70 | [`candidate70-machine-decision-boundary-design.md`](candidate70-machine-decision-boundary-design.md) | machine decision boundary |
| C71 | [`candidate71-validation-closure-design.md`](candidate71-validation-closure-design.md) | validation closure |
| C72 | [`candidate72-closed-validation-state-design.md`](candidate72-closed-validation-state-design.md) | closed validation state |
| C73 | [`candidate73-terminal-closure-preserving-compression-design.md`](candidate73-terminal-closure-preserving-compression-design.md) | terminal closure preserving compression |
| C74 | [`candidate74-typed-execution-state-machine-design.md`](candidate74-typed-execution-state-machine-design.md) | typed execution state machine |
| C75 | [`candidate75-authority-bound-validation-fast-path-design.md`](candidate75-authority-bound-validation-fast-path-design.md) | authority-bound validation fast path |
| C76 | [`candidate76-final-state-validation-wave-design.md`](candidate76-final-state-validation-wave-design.md) | final-state validation wave |
| C77 | [`candidate77-triggered-exception-transition-design.md`](candidate77-triggered-exception-transition-design.md) | triggered exception transition |

### 3b. 比較・診断・段階記録

| 文書 | 役割 |
|---|---|
| [`prompt-control-graph-review.md`](prompt-control-graph-review.md) | 制御graph棚卸し。提案predicateはCandidate41として実装・評価済みで、B18後も追加規則を導かないと結論した根拠記録 |
| [`a02-rating-divergence.md`](a02-rating-divergence.md) | A02の「要求と採点のずれ」3件と、rating contract v10〜v13の変遷 |
| [`candidate5-candidate15-continuous-comparison.md`](candidate5-candidate15-continuous-comparison.md) | Candidate5 / Candidate15の連続試験比較 |
| [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md) | Review location誤差の原因診断 |
| [`task-spec-planner-phase1-plan.md`](task-spec-planner-phase1-plan.md) | TaskSpec確認 第1段階の実施記録（実施・評価・release・projection完了） |
| [`sa-routing-decision-table.md`](sa-routing-decision-table.md) | candidate2のSA routing decision table |
| [`prompt-set-result-registry-additional-requirements.md`](prompt-set-result-registry-additional-requirements.md) | result台帳の追加要件記録。status `implemented_as_evaluation_foundation_v3`。具体設計の正本は`prompt-comparison-workflow.md`と`evaluation-loop-manual.md` |

## 4. historical handoff／superseded interpretation

内容は当時の記録として保持する。現行設計・現行値として読まない。各文書の冒頭バナーが位置づけを示す。

| 文書 | 位置づけ |
|---|---|
| [`candidate5-token-efficiency-direction.md`](candidate5-token-efficiency-direction.md) | root-only token由来の旧解釈。現行値はall-agent再集計へ置換済み |
| [`candidate6-candidate8-efficiency-investigation.md`](candidate6-candidate8-efficiency-investigation.md) | root-only token由来の調査履歴。現行値はall-agent再集計を参照 |
| [`candidate71-spec-audit-handoff.md`](candidate71-spec-audit-handoff.md) | C71 `SPEC`監査の完了済みhandoff。監査結果は`candidate71-control-abstraction-analysis.md`へ統合済み |
| [`prompt-control-review-handoff.md`](prompt-control-review-handoff.md) | C35〜C40時点の制御見直しhandoff。当時のbranch・HEAD・未commit差分を含む |
| [`sa-routing-condition-extraction.md`](sa-routing-condition-extraction.md) | candidate2設計の出発点となった`design_input`。その後の系譜は大きく進行 |
