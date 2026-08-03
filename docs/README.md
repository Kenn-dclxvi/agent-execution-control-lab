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
| [`candidate125-candidate147-control-findings-synthesis.md`](candidate125-candidate147-control-findings-synthesis.md) | C125のN=5成立とN拡張停止から、C126〜C142のeffect / evidence境界探索、C143の上流再構築、C147のN=100採用までの因果系列と現在解釈 |
| [`execution-control-research-paper.md`](execution-control-research-paper.md) | 研究成果の総説（論文形式、第3版・2026-07-31時点）。**下記の技術報告 第1版とは別の文書で、互いに置き換えない。** 実測値の要約と2026年7月ベンダ公式指針（GPT-5.6 Sol / Claude Opus 5）との対照。**正本ではない**。数値・状態の正本は同文書が示す一次artifact |
| [`execution-control-measurement-report.md`](execution-control-measurement-report.md) | 研究者向けの**技術報告 第1版**（2026-08-03、14節＋要旨＋付録A〜D）。BaselineをV1（汎用オーケストレーションプロンプト製品）の適用結果として位置づけ、本研究をV1が予定していたAI向け移行（V2）の実行として記述する。公開Baseline系譜（`orchestration-prompt`固定履歴）と外部文献・提供者指針を一次・補助資料として使う。**この版をもって記述を固定し、以降の測定は新しい版として追加する。** 数値と識別子は一次artifactを、主張と証拠の対応はevidence mapを正本とする。|
| [`execution-control-measurement-report-evidence-map.md`](execution-control-measurement-report-evidence-map.md) | 上記**第1版**のClaim IDごとの一次資料対応表（証拠水準・表現上限・再検証分類）、再検証候補20件、一次資料と要約文書の相違・留保30件（外部文献への誤帰属5件の撤回を含む） |
| [`branch-closure-retrospective-coding.md`](branch-closure-retrospective-coding.md) | 「分岐の開閉」軸の事後符号化（保存済みdiff 124件、新規測定なし）。判定入力をroot本文diffだけに限り、KPIを参照せずに符号化した手続きと全件の符号。**軸が実行経路と往復の2操作を含むこと、判定が符号化者に依存すること、経路を閉じることが十分条件でないことを確定する。** 技術報告§12.2はこれを引用する |
| [`why-prompt-writing-changes-your-bill.md`](why-prompt-writing-changes-your-bill.md) | **YouTube向けの3分説明資料**（引用なし）。Free比のAPI料金換算`-39.95%`を前面に出し、静的プロンプト`0 → 10,772 B`、実行トークン`-58.50%`、最高評価`65 / 70 → 70 / 70件`となった観測を一表と短い解説で説明する。 |
| [`how-to-write-prompts-that-cut-api-cost.md`](how-to-write-prompts-that-cut-api-cost.md) | **単独で読める「じゃあどう書くのか」3分説明資料**（引用なし）。そのまま使える4文を最初に示し、「仕様を決める・変更を始める・調べる・作業を終える」の各場面で何が変わるかを、具体例と作業への割り当てで説明する。 |
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

> **本体投影と評価状態は別軸**: Candidate147は公開版`the-caption`へ投影済みで、release status `projected` / approval `approved` / runtime projection `projected`である。Rating v14 Medium Standard14 N=100は1,400 / 1,400 score `4`、targeted F01 / F02 / F03のmechanismは15 / 15だった。Candidate125は移行前THE-CAPTIONへの投影履歴として保持する。Candidate125のStandard14 N=5は70 / 70 score `4`、A02 N=20はbind後再入0件だったが、2026-08-01のN=100追試はregistered poolを各case30件まで拡張した時点でF04 score `2`を5件確認し、`n100_execution_stopped / registered_pool_n30`で中断した（正式な`N=30`結果ではない）。過去のCandidate41・Candidate43・Candidate71・Candidate81・Candidate125の投影状態と、Candidate71の`standard14_b18_evaluated / stopped`を遡及変更しない。正本は[`prompts/releases/README.md`](../prompts/releases/README.md)と各release READMEとする。

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
| C78 | [`candidate78-project-index-navigation-design.md`](candidate78-project-index-navigation-design.md) | project index navigation |
| C79 | [`candidate79-ordered-validation-wave-design.md`](candidate79-ordered-validation-wave-design.md) | ordered validation wave |
| C80 | [`candidate80-root-validation-wrapper-design.md`](candidate80-root-validation-wrapper-design.md) | root validation wrapper |
| C81 | [`candidate81-validation-wrapper-precedence-design.md`](candidate81-validation-wrapper-precedence-design.md) | validation wrapper precedence |

### 3b. 比較・診断・段階記録

| 文書 | 役割 |
|---|---|
| [`prompt-control-graph-review.md`](prompt-control-graph-review.md) | 制御graph棚卸し。提案predicateはCandidate41として実装・評価済みで、B18後も追加規則を導かないと結論した根拠記録 |
| [`a02-rating-divergence.md`](a02-rating-divergence.md) | A02の「要求と採点のずれ」3件と、rating contract v10〜v13の変遷 |
| [`candidate5-candidate15-continuous-comparison.md`](candidate5-candidate15-continuous-comparison.md) | Candidate5 / Candidate15の連続試験比較 |
| [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md) | Review location誤差の原因診断 |
| [`task-spec-planner-phase1-plan.md`](task-spec-planner-phase1-plan.md) | TaskSpec確認 第1段階の実施記録（実施・評価・release・projection完了） |
| [`sa-routing-decision-table.md`](sa-routing-decision-table.md) | candidate2のSA routing decision table |
| [`candidate87-adoption-decision.md`](candidate87-adoption-decision.md) | C87の評価状態を保持した別stateの不採用・停止判断と、C82〜C89系列の完了境界 |
| [`candidate106-f03-b20-short-yield-route-analysis.md`](candidate106-f03-b20-short-yield-route-analysis.md) | C104 / C106 F03 B20の途中messageをouter early yieldとnonterminal再入の二段階へ分解した診断 |
| [`candidate107-validation-wrapper-reentry-closure-design.md`](candidate107-validation-wrapper-reentry-closure-design.md) | C106のF03 B20再発経路をouter deadline条件とcell ID wait-only遷移で閉じるCandidate107設計 |
| [`candidate108-validation-ticket-terminal-closure-design.md`](candidate108-validation-ticket-terminal-closure-design.md) | C107のdeadline大小比較を削除し、実行票全体のterminal wait-only遷移へ一本化するCandidate108設計 |
| [`candidate109-validation-ticket-outer-wait-closure-design.md`](candidate109-validation-ticket-outer-wait-closure-design.md) | C108のwait-only fallbackを維持し、validation ticketのouter yieldをruntime最大値へ固定するCandidate109設計 |
| [`candidate110-validation-ticket-decision-boundary-design.md`](candidate110-validation-ticket-decision-boundary-design.md) | C108の実行票途中状態を既存DECISION_BOUNDARYの外へ置くprompt-only Candidate110設計 |
| [`candidate111-validation-ticket-model-return-boundary-design.md`](candidate111-validation-ticket-model-return-boundary-design.md) | 判断価値のない途中状態をmodelへ返す必要性を発行時点で否定するprompt-only Candidate111設計 |
| [`candidate112-evidence-admission-scheduling-boundary-design.md`](candidate112-evidence-admission-scheduling-boundary-design.md) | evidence identityのadmissionと、許可済みで独立したinvocationの発行順序を分離するprompt-only Candidate112設計 |
| [`candidate113-explicit-authority-delegation-design.md`](candidate113-explicit-authority-delegation-design.md) | requested outcome valueのauthority探索をTaskSpecの明示委譲だけで開くprompt-only Candidate113設計 |
| [`candidate114-spec-ready-evidence-phase-boundary-design.md`](candidate114-spec-ready-evidence-phase-boundary-design.md) | `spec_ready`で仕様確定evidenceとtarget evidenceを分けるCandidate114設計 |
| [`candidate115-authority-location-discovery-design.md`](candidate115-authority-location-discovery-design.md) | authority path未記載による誤停止を対象にしたCandidate115設計 |
| [`candidate116-outcome-implementation-boundary-design.md`](candidate116-outcome-implementation-boundary-design.md) | required outcome確定とimplementation choice解決を分離するCandidate116設計 |
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
