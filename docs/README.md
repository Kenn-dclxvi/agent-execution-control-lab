# docs 索引

`docs/`配下の研究文書を、読む前に**役割で選べる**ようにするための索引。文書は次の8分類で位置づける。

| 分類 | 意味 | 扱い |
|---|---|---|
| **正本（canonical）** | 他文書が参照authorityとして引く契約・原則 | 統合・要約せず維持。正本指定は各領域の`AGENTS.md`（下表参照） |
| **現在地・研究全体像** | 研究の目的、系譜、横断知見、未完了項目、長期方向 | 現在地点を把握する最初の起点 |
| **現行frontier** | 現在進行中の研究軸と、その直近の設計・診断 | 因果系列ごとに追い、完了済み成果と混ぜない |
| **研究成果・統合知見** | 固定版の技術報告、総説、横断分析、統合知見 | 現在有効な研究成果として読む。数値・状態は各文書が示す一次アーティファクトを正本とする |
| **実務者向け解説** | 研究成果を実務へ翻訳した読み物 | 研究アーティファクトの代替ではなく、実務から理解する入口として扱う |
| **評価・運用基盤** | 評価インフラ、実行環境、運用仕様 | 研究内容そのものではなく、測定・運用を成立させる基盤として扱う |
| **完了済み研究記録** | 特定Candidate・比較・診断の成果アーティファクト | 当時のresult・scoreを保持（遡及書換なし） |
| **historical／superseded** | root-only履歴、完了済みの引き継ぎ文書、旧設計入力 | 現行設計として読まない。冒頭バナーで位置づけ |

分類間の原則は[`AGENTS.md`](AGENTS.md)を正とする（現在状態・当時の評価・後続の再解釈を混ぜない／過去result・scoreを削除しない／現在解釈は注記か別文書として追加）。

---

## 1. 正本（canonical）

参照先として維持する。統合・要約・全文複製の対象にしない。「正本指定元」列は、その正本性を明示するinstructionを示す。

| 文書 | 役割 | 正本指定元 |
|---|---|---|
| [`repository-contract.md`](repository-contract.md) | リポジトリ契約の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md) | 評価基盤のレイヤーと境界の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`evaluation-loop-manual.md`](evaluation-loop-manual.md) | 評価実行方法の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-control-design-principles.md`](prompt-control-design-principles.md) | プロンプト制御の設計原則の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-file-bundle.md`](prompt-file-bundle.md) | prompt file bundle形式・manifest・格納の正本 | [`scripts/AGENTS.md`](../scripts/AGENTS.md) |

## 2. 現在地・研究全体像

「何を研究しているか → どこまで来たか → 何が分かったか → 何が残っているか → どこへ進むか」の順に読むための入口。

| 文書 | 役割 |
|---|---|
| [`repository-overview.md`](repository-overview.md) | 初見向けの全体像（入口） |
| [`candidate-history.md`](candidate-history.md) | Candidate系譜と知見の索引。系譜と現在状態の一覧は[`prompts/candidates/README.md`](../prompts/candidates/README.md) |
| [`control-mechanisms.md`](control-mechanisms.md) | 横断的な制御メカニズムの知見 |
| [`research-backlog.md`](research-backlog.md) | 未完了研究項目の索引（label監査の再測定、`P3`削除candidate、A01 variation、未解決リスク）。判定の正本は各リンク先 |
| [`future-roadmap.md`](future-roadmap.md) | 長期方針と発展方向（恒久的な方針のみ） |

## 3. 現行frontier

現在進行中の研究軸を、別軸の作業を混ぜず因果系列ごとに並べる。

### 3a. 機能見直し・review admission

| 文書 | 役割 |
|---|---|
| [`feature-review-phase1-plan.md`](feature-review-phase1-plan.md) | Candidate147を基準に、過去機能の維持・休眠・欠落・プロンプト強制不能を一件ずつ判定する機能見直しフェーズ。最初の対象は独立SA reviewと情報封鎖の必要性 |
| [`candidate164-autonomous-review-admission-design.md`](candidate164-autonomous-review-admission-design.md) | FR-01自律routingで観測したHR03失敗に対し、C147へreview admission / producer選択predicate一つだけを追加した設計。targeted試験はreviewer起動5 / 5まで改善したがterminal再生成1件で停止 |
| [`candidate165-review-result-admission-design.md`](candidate165-review-result-admission-design.md) | C164の1件をprior評価のauthority誤分類として分解し、current TaskSpecへbind済みのresultだけをquality criterionへadmitする設計。Review4は20 / 20、Standard14は70 / 70 Score `4`。C147比のコスト増を残す |
| [`candidate165-standard14-review-route-analysis.md`](candidate165-standard14-review-route-analysis.md) | C165 Standard14 70 traceから、独立SAの実質修正0 / 41、通常ケースへの系統起動40件、clean-context root review成功5 / 5を分離し、result admission成立とreview admission過大を切り分けた現在解釈 |
| [`candidate166-prior-evaluation-review-admission-design.md`](candidate166-prior-evaluation-review-admission-design.md) | C165の過大発動に対し、アーティファクト実装・調査を独立SA切替条件から外した一変更。Review4はroute / closure 20 / 20、oracle一致18 / 20。HR03のケース設計不備によりquality未判定、Standard14未実施 |
| [`candidate166-review4-case-validity-analysis.md`](candidate166-review4-case-validity-analysis.md) | C166 Review4のHR03を再監査し、raw response不在のまま観測表現を強めたため期待terminalが一意でないと判定。18 / 20をquality failureへ使わず、r2 case revisionの事前条件を固定 |
| [`candidate166-review-behavior-case-reassessment.md`](candidate166-review-behavior-case-reassessment.md) | プロンプト内部条件の直積を廃止し、review不要、正常、欠陥、判定不能と外乱対照pairで既存ケースを再分類。次gateを7ケース × N=5へ固定するケース設計 |
| [`preimplementation-information-sealed-adversarial-design-review-spec.md`](preimplementation-information-sealed-adversarial-design-review-spec.md) | 固定済み契約を満たす一般設計をC147の`implementation_bound`へ渡す前に、探索で閉じた境界、固定試験の見落とし可能性、反例による設計変更を共同判定し、必要な場合だけ情報封鎖した独立敵対的レビューを行う新規仕様。Candidate、評価設計、評価は未着手 |

### 3b. 公開ターゲット拡張

| 文書 | 役割 |
|---|---|
| [`public-target-selection-phase0.md`](public-target-selection-phase0.md) | 公開ターゲット選定Phase 0の実測記録と判定（`pallets/click`をPhase 1候補とした根拠） |

## 4. 研究成果・統合知見

固定版の研究成果、総説、横断分析、現在有効な統合知見をまとめる。進行中のCandidate系列とは分けて読む。

| 文書 | 役割 |
|---|---|
| [`execution-control-measurement-report.md`](execution-control-measurement-report.md) | 研究者向けの**技術報告 第1版**（2026-08-03、14節＋要旨＋付録A〜D）。BaselineをV1（汎用オーケストレーションプロンプト製品）の適用結果として位置づけ、本研究をV1が予定していたAI向け移行（V2）の実行として記述する。公開Baseline系譜（`orchestration-prompt`固定履歴）と外部文献・提供者指針を一次・補助資料として使う。**この版をもって記述を固定し、以降の測定は新しい版として追加する。** 数値と識別子は一次アーティファクトを、主張と証拠の対応はevidence mapを正本とする。|
| [`execution-control-measurement-report-evidence-map.md`](execution-control-measurement-report-evidence-map.md) | 上記**第1版**のClaim IDごとの一次資料対応表（証拠水準・表現上限・再検証分類）、再検証候補20件、一次資料と要約文書の相違・留保30件（外部文献への誤帰属5件の撤回を含む） |
| [`execution-control-research-paper.md`](execution-control-research-paper.md) | 研究成果の総説（論文形式、第3版・2026-07-31時点）。**上記の技術報告 第1版とは別の文書で、互いに置き換えない。** 実測値の要約と2026年7月ベンダ公式指針（GPT-5.6 Sol / Claude Opus 5）との対照。**正本ではない**。数値・状態の正本は同文書が示す一次アーティファクト |
| [`candidate125-candidate147-control-findings-synthesis.md`](candidate125-candidate147-control-findings-synthesis.md) | C125のN=5成立とN拡張停止から、C126〜C142のeffect / evidence境界探索、C143の上流再構築、C147のN=100採用までの因果系列と現在解釈 |
| [`branch-closure-retrospective-coding.md`](branch-closure-retrospective-coding.md) | 「分岐の開閉」軸の事後符号化（保存済みdiff 124件、新規測定なし）。判定入力をroot本文diffだけに限り、KPIを参照せずに符号化した手続きと全件の符号。**軸が実行経路と往復の2操作を含むこと、判定が符号化者に依存すること、経路を閉じることが十分条件でないことを確定する。** 技術報告§12.2はこれを引用する |
| [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md) | C71 control abstraction分析（11 label監査台帳＋現在の結論）。現在の総括は同文書の「監査状況の分類」表を正とする |

## 5. 実務者向け解説

研究成果を実務から読むためのExecution Controlシリーズ。研究アーティファクトや一次資料の代替ではない。

| 文書 | 役割 |
|---|---|
| [`01_why-prompt-writing-changes-your-bill.md`](01_why-prompt-writing-changes-your-bill.md) | **実務者向けExecution Controlシリーズ 1 / 8**。Free比のAPI料金換算`-39.95%`を入口に、削るべきものは文字数ではなく迷う余地だと説明する。 |
| [`02_how-to-write-prompts-that-cut-api-cost.md`](02_how-to-write-prompts-that-cut-api-cost.md) | **シリーズ 2 / 8**。成果、変更開始、担当と結果、調査、完了という5つの判断条件を、推測・手戻り・過剰な探索や検証と対応づける。 |
| [`03_what-not-to-write-in-ai-prompts.md`](03_what-not-to-write-in-ai-prompts.md) | **シリーズ 3 / 8**。索引追加、表面的な短文化、抽象的なmeta判断など、無条件に足さない7項目と代替を書く。 |
| [`04_what-prompts-can-and-cannot-control.md`](04_what-prompts-can-and-cannot-control.md) | **シリーズ 4 / 8**。AIが観測後に選ぶ行動と、executorやtool adapterが担う配送・原子性などの境界を説明する。 |
| [`05_review-roles-vs-decision-conditions.md`](05_review-roles-vs-decision-conditions.md) | **シリーズ 5 / 8**。レビュー工程と品質責務を分離し、別担当を増やす前に固定する判定対象と結果を示す。 |
| [`06_execution-paths-drive-ai-cost.md`](06_execution-paths-drive-ai-cost.md) | **シリーズ 6 / 8**。静的な文章量ではなく、モデル往復、再読、再検証を含む実行経路を設計対象として説明する。 |
| [`07_do-not-copy-human-development-processes.md`](07_do-not-copy-human-development-processes.md) | **シリーズ 7 / 8**。人間組織の工程を導入経路として認めつつ、AI向けには失敗様式と観測可能な条件へ変換する。 |
| [`08_what-is-execution-control.md`](08_what-is-execution-control.md) | **シリーズ 8 / 8**。AIへの依頼とExecution Controlを分け、進行・停止・完了を制御する全体像をまとめる。 |

## 6. 評価・運用基盤

| 文書 | 役割 |
|---|---|
| [`THE-CAPTION_execution-control_revision-instructions.md`](THE-CAPTION_execution-control_revision-instructions.md) | execution control修正指示（invocation_status等の定義） |
| [`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md) | 評価ストレージの維持・GC |
| [`desktop-evaluation-slot.md`](desktop-evaluation-slot.md) | desktop評価スロットの前提条件 |
| [`shared-python-runtime.md`](shared-python-runtime.md) | 共有Pythonランタイム |
| [`typed-boundary-evidence.md`](typed-boundary-evidence.md) | typed boundary evidenceの仕様 |
| [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md) | Layer 2 executorをClaude Code CLIへ置き換える試験方法の設計検討（未実装。未確定事項を含む） |
| [`pr-review-measurement-environment-design.md`](pr-review-measurement-environment-design.md) | `agent-execution-control-lab` namespacedインスタンスでClaude Code Actionの実行経路を比較するPRレビュー測定設計。仕様監査で既存PRR-C01 runをdiagnosticへ再分類し、Core Baselineは未qualification |

## 7. 完了済み研究記録

### 7a. Candidate設計記録

各Candidateの制御軸を記録した成果アーティファクト。当時のresult・scoreは遡及変更しない。

正本はlifecycle軸ごとに分かれる。**identityは各バンドルの`manifest.json`**、**評価状態は評価・診断を実施済みなら独立したevaluation / diagnostic result、未実施の`not_evaluated`は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列**、**release・approval・runtime projectionは[`prompts/releases/README.md`](../prompts/releases/README.md)**を正本とする。系譜と現在状態の一覧はcandidate索引にある。この索引は制御軸だけを示し、状態は複製しない（`docs/AGENTS.md`「同じ説明を複数文書へ全文複製せず正本へリンク」）。評価と採用、releaseとprojectionは別状態である（[`repository-contract.md`](repository-contract.md)、[`AGENTS.md`](AGENTS.md)）。

> **本体投影と評価状態は別軸**: Candidate147は公開版`the-caption`へ投影済みで、release status `projected` / approval `approved` / runtime projection `projected`である。Rating v14 Medium Standard14 N=100は1,400 / 1,400 score `4`、targeted F01 / F02 / F03のmechanismは15 / 15だった。Candidate125は移行前THE-CAPTIONへの投影履歴として保持する。Candidate125のStandard14 N=5は70 / 70 score `4`、A02 N=20はbind後再入0件だったが、2026-08-01のN=100追試はregistered poolを各ケース30件まで拡張した時点でF04 score `2`を5件確認し、`n100_execution_stopped / registered_pool_n30`で中断した（正式な`N=30`結果ではない）。過去のCandidate41・Candidate43・Candidate71・Candidate81・Candidate125の投影状態と、Candidate71の`standard14_b18_evaluated / stopped`を遡及変更しない。正本は[`prompts/releases/README.md`](../prompts/releases/README.md)と各release READMEとする。

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

C107〜C116の設計記録は「7b. 比較・診断・段階記録」へ掲載している。C164〜C166は現行frontierのため「3a」へ掲載している。

| Candidate | 文書 | 制御軸 |
|---|---|---|
| C82 | [`candidate82-producer-gate-deduplication-design.md`](candidate82-producer-gate-deduplication-design.md) | producer gate deduplication |
| C83 | [`candidate83-delegation-value-boundary-design.md`](candidate83-delegation-value-boundary-design.md) | delegation value boundary |
| C84 | [`candidate84-delegation-marginal-value-boundary-design.md`](candidate84-delegation-marginal-value-boundary-design.md) | delegation marginal value boundary |
| C85 | [`candidate85-planning-first-producer-selection-design.md`](candidate85-planning-first-producer-selection-design.md) | planning first producer selection |
| C86 | [`candidate86-producer-plan-fast-path-design.md`](candidate86-producer-plan-fast-path-design.md) | producer plan fast path |
| C87 | [`candidate87-producer-local-invocation-wave-design.md`](candidate87-producer-local-invocation-wave-design.md) | producer local invocation wave |
| C88 | [`candidate88-parallel-worker-admission-design.md`](candidate88-parallel-worker-admission-design.md) | parallel worker admission |
| C89 | [`candidate89-dispatch-time-worker-admission-design.md`](candidate89-dispatch-time-worker-admission-design.md) | dispatch time worker admission |
| C90 | [`candidate90-tool-output-ingress-boundary-design.md`](candidate90-tool-output-ingress-boundary-design.md) | tool output ingress boundary |
| C91 | [`candidate91-concise-output-ingress-design.md`](candidate91-concise-output-ingress-design.md) | concise output ingress |
| C92 | [`candidate92-bound-output-route-design.md`](candidate92-bound-output-route-design.md) | bound output route |
| C93 | [`candidate93-result-classification-design.md`](candidate93-result-classification-design.md) | result classification |
| C94 | [`candidate94-operation-criterion-totality-design.md`](candidate94-operation-criterion-totality-design.md) | operation criterion totality |
| C95 | [`candidate95-required-judgment-owner-boundary-design.md`](candidate95-required-judgment-owner-boundary-design.md) | required judgment owner boundary |
| C96 | [`candidate96-successful-validation-result-projection-design.md`](candidate96-successful-validation-result-projection-design.md) | successful validation result projection |
| C97 | [`candidate97-decision-round-closure-design.md`](candidate97-decision-round-closure-design.md) | decision round closure |
| C97 | [`candidate97-minimal-decision-round-closure-r2-design.md`](candidate97-minimal-decision-round-closure-r2-design.md) | minimal decision round closure r2 |
| C98 | [`candidate98-validation-completion-sheet-design.md`](candidate98-validation-completion-sheet-design.md) | validation completion sheet |
| C99 | [`candidate99-decision-evidence-boundary-design.md`](candidate99-decision-evidence-boundary-design.md) | decision evidence boundary |
| C100 | [`candidate100-outcome-source-closure-design.md`](candidate100-outcome-source-closure-design.md) | outcome source closure |
| C101 | [`candidate101-additional-investigation-trigger-design.md`](candidate101-additional-investigation-trigger-design.md) | additional investigation trigger |
| C102 | [`candidate102-prechange-evidence-freeze-design.md`](candidate102-prechange-evidence-freeze-design.md) | prechange evidence freeze |
| C103 | [`candidate103-prechange-evidence-receipt-design.md`](candidate103-prechange-evidence-receipt-design.md) | prechange evidence receipt |
| C104 | [`candidate104-staged-evidence-admission-design.md`](candidate104-staged-evidence-admission-design.md) | staged evidence admission |
| C105 | [`candidate105-validation-terminal-return-design.md`](candidate105-validation-terminal-return-design.md) | validation terminal return |
| C106 | [`candidate106-compact-validation-terminal-wait-design.md`](candidate106-compact-validation-terminal-wait-design.md) | compact validation terminal wait |
| C117 | [`candidate117-implementation-authority-delegation-design.md`](candidate117-implementation-authority-delegation-design.md) | implementation authority delegation |
| C118 | [`candidate118-implementation-bind-terminal-closure-design.md`](candidate118-implementation-bind-terminal-closure-design.md) | implementation bind terminal closure |
| C119 | [`candidate119-validation-predicate-method-boundary-design.md`](candidate119-validation-predicate-method-boundary-design.md) | validation predicate method boundary |
| C120 | [`candidate120-implementation-edit-ticket-closure-design.md`](candidate120-implementation-edit-ticket-closure-design.md) | implementation edit ticket closure |
| C121 | [`candidate121-evidence-request-scope-closure-design.md`](candidate121-evidence-request-scope-closure-design.md) | evidence request scope closure |
| C122 | [`candidate122-prechange-evidence-wave-closure-design.md`](candidate122-prechange-evidence-wave-closure-design.md) | prechange evidence wave closure |
| C123 | [`candidate123-preterminal-result-round-closure-design.md`](candidate123-preterminal-result-round-closure-design.md) | preterminal result round closure |
| C124 | [`candidate124-incomplete-content-continuation-design.md`](candidate124-incomplete-content-continuation-design.md) | incomplete content continuation |
| C125 | [`candidate125-criterion-complete-single-target-continuation-design.md`](candidate125-criterion-complete-single-target-continuation-design.md) | criterion complete single target continuation |
| C126 | [`candidate126-criterion-bound-change-input-design.md`](candidate126-criterion-bound-change-input-design.md) | criterion bound change input |
| C127 | [`candidate127-failed-change-salvage-design.md`](candidate127-failed-change-salvage-design.md) | failed change salvage |
| C128 | [`candidate128-required-effect-closure-design.md`](candidate128-required-effect-closure-design.md) | required effect closure |
| C129 | [`candidate129-unsatisfied-effect-change-admission-design.md`](candidate129-unsatisfied-effect-change-admission-design.md) | unsatisfied effect change admission |
| C130 | [`candidate130-focused-criterion-continuation-design.md`](candidate130-focused-criterion-continuation-design.md) | focused criterion continuation |
| C131 | [`candidate131-criterion-anchor-continuation-design.md`](candidate131-criterion-anchor-continuation-design.md) | criterion anchor continuation |
| C132 | [`candidate132-observed-preimage-change-construction-design.md`](candidate132-observed-preimage-change-construction-design.md) | observed preimage change construction |
| C133 | [`candidate133-anchor-first-continuation-order-design.md`](candidate133-anchor-first-continuation-order-design.md) | anchor first continuation order |
| C134 | [`candidate134-syntactic-lexeme-continuation-design.md`](candidate134-syntactic-lexeme-continuation-design.md) | syntactic lexeme continuation |
| C135 | [`candidate135-criterion-span-request-authority-design.md`](candidate135-criterion-span-request-authority-design.md) | criterion span request authority |
| C136 | [`candidate136-effect-local-change-admission-design.md`](candidate136-effect-local-change-admission-design.md) | effect local change admission |
| C137 | [`candidate137-pending-effect-validation-admission-design.md`](candidate137-pending-effect-validation-admission-design.md) | pending effect validation admission |
| C138 | [`candidate138-continuation-effect-change-handoff-design.md`](candidate138-continuation-effect-change-handoff-design.md) | continuation effect change handoff |
| C139 | [`candidate139-single-target-continuation-handoff-design.md`](candidate139-single-target-continuation-handoff-design.md) | single target continuation handoff |
| C140 | [`candidate140-effect-satisfaction-witness-design.md`](candidate140-effect-satisfaction-witness-design.md) | effect satisfaction witness |
| C141 | [`candidate141-prechange-relation-coverage-design.md`](candidate141-prechange-relation-coverage-design.md) | prechange relation coverage |
| C142 | [`candidate142-initial-joint-effect-admission-design.md`](candidate142-initial-joint-effect-admission-design.md) | initial joint effect admission |
| C143 | [`candidate143-required-outcome-implementation-bind-design.md`](candidate143-required-outcome-implementation-bind-design.md) | required outcome implementation bind |
| C144 | [`candidate144-required-outcome-validation-method-boundary-design.md`](candidate144-required-outcome-validation-method-boundary-design.md) | required outcome validation method boundary |
| C145 | [`candidate145-lifecycle-consumer-evidence-admission-design.md`](candidate145-lifecycle-consumer-evidence-admission-design.md) | lifecycle consumer evidence admission |
| C146 | [`candidate146-consumer-closure-evidence-operation-design.md`](candidate146-consumer-closure-evidence-operation-design.md) | consumer closure evidence operation |
| C147 | [`candidate147-result-effect-scope-design.md`](candidate147-result-effect-scope-design.md) | result effect scope |
| C148 | [`candidate148-five-point-execution-control-design.md`](candidate148-five-point-execution-control-design.md) | five point execution control |
| C149 | [`candidate149-specification-start-boundary-design.md`](candidate149-specification-start-boundary-design.md) | specification start boundary |
| C150 | [`candidate150-required-outcome-bind-readable-design.md`](candidate150-required-outcome-bind-readable-design.md) | required outcome bind readable |
| C151 | [`candidate151-evidence-consumer-boundary-readable-design.md`](candidate151-evidence-consumer-boundary-readable-design.md) | evidence consumer boundary readable |
| C152 | [`candidate152-four-decision-rules-readable-design.md`](candidate152-four-decision-rules-readable-design.md) | four decision rules readable |
| C156 | [`candidate156-five-prompt-conditions-readable-design.md`](candidate156-five-prompt-conditions-readable-design.md) | five prompt conditions readable |
| C157 | [`candidate157-focused-prechange-research-readable-design.md`](candidate157-focused-prechange-research-readable-design.md) | focused prechange research readable |
| C158 | [`candidate158-outcome-method-readable-design.md`](candidate158-outcome-method-readable-design.md) | outcome method readable |
| C159 | [`candidate159-change-start-readable-design.md`](candidate159-change-start-readable-design.md) | change start readable |
| C160 | [`candidate160-assignment-result-readable-design.md`](candidate160-assignment-result-readable-design.md) | assignment result readable |
| C161 | [`candidate161-assignment-result-closure-readable-design.md`](candidate161-assignment-result-closure-readable-design.md) | assignment result closure readable |
| C162 | [`candidate162-completion-ticket-readable-design.md`](candidate162-completion-ticket-readable-design.md) | completion ticket readable |
| C163 | [`candidate163-five-verified-lines-integrated-design.md`](candidate163-five-verified-lines-integrated-design.md) | five verified lines integrated |

### 7b. 比較・診断・段階記録

| 文書 | 役割 |
|---|---|
| [`prompt-control-graph-review.md`](prompt-control-graph-review.md) | 制御グラフ棚卸し。提案predicateはCandidate41として実装・評価済みで、B18後も追加規則を導かないと結論した根拠記録 |
| [`a02-rating-divergence.md`](a02-rating-divergence.md) | A02の「要求と採点のずれ」3件と、rating contract v10〜v13の変遷 |
| [`candidate5-candidate15-continuous-comparison.md`](candidate5-candidate15-continuous-comparison.md) | Candidate5 / Candidate15の連続試験比較 |
| [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md) | Review location誤差の原因診断 |
| [`task-spec-planner-phase1-plan.md`](task-spec-planner-phase1-plan.md) | TaskSpec確認 第1段階の実施記録（実施・評価・release・projection完了） |
| [`sa-routing-decision-table.md`](sa-routing-decision-table.md) | candidate2のSA routing decision table |
| [`candidate87-adoption-decision.md`](candidate87-adoption-decision.md) | C87の評価状態を保持した別stateの不採用・停止判断と、C82〜C89系列の完了境界 |
| [`candidate106-f03-b20-short-yield-route-analysis.md`](candidate106-f03-b20-short-yield-route-analysis.md) | C104 / C106 F03 B20の途中のメッセージをouter early yieldとnonterminal再入の二段階へ分解した診断 |
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
| [`candidate118-residual-validation-reentry-analysis.md`](candidate118-residual-validation-reentry-analysis.md) | C118の残存トークン増加を、追加したbind closureではなく変更後validationのnonterminal返却とmodel再入で説明した診断 |
| [`candidate121-f02-evidence-route-analysis.md`](candidate121-f02-evidence-route-analysis.md) | C121のF02のコスト未達をevidence bytesだけでは説明できないと示し、locator→content spanの二段階routeを共通差として分離した診断 |
| [`candidate122-preterminal-result-round-analysis.md`](candidate122-preterminal-result-round-analysis.md) | トークンの高低を分けた共通差がinvocation数ではなく、変更・停止までにtool resultをmodelへ返したround数だと特定した診断 |
| [`candidate125-adoption-decision.md`](candidate125-adoption-decision.md) | C125の採用判断。評価状態、release、approval、projectionを分離して記録 |
| [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md) | C125 Standard14 N=5を通常input / cached input / cache write / outputへ分解し、公開API単価で課金換算した比較 |
| [`candidate125-candidate132-six-point-control-synthesis.md`](candidate125-candidate132-six-point-control-synthesis.md) | C125〜C132の六点の制御を統合し、六点を同時に解くglobal predicateは作らないと結論した記録 |
| [`candidate131-point4-dependency-audit.md`](candidate131-point4-dependency-audit.md) | Point 4 dependencyを独立predicateへ固定しないと判断した監査 |
| [`candidate131-point6-closure-recovery-audit.md`](candidate131-point6-closure-recovery-audit.md) | Point 6 closure / recoveryに新Candidateを作らないと判断した監査 |
| [`candidate133-task-spec-lexeme-authority-audit.md`](candidate133-task-spec-lexeme-authority-audit.md) | anchorを意味判断で選ばず、TaskSpec原文のcode-shaped lexemeを構文規則で全件抽出する次軸を固定した監査 |
| [`candidate134-reference-symbol-coverage-ownership-audit.md`](candidate134-reference-symbol-coverage-ownership-audit.md) | C134の低ScoreをPoint 2 evidence coverage不足へ帰属させ、request identity失敗とcoverage closure失敗の同時修正を禁じた監査 |
| [`candidate135-effect-local-change-admission-audit.md`](candidate135-effect-local-change-admission-audit.md) | 充足済み`colSpan` effectを再び変更対象へ入れ必要変更と同一のパッチへ結合したことをScore 2の直接原因とした監査 |
| [`candidate136-criterion-lexeme-member-totality-audit.md`](candidate136-criterion-lexeme-member-totality-audit.md) | C136 Score 3の原因を入力範囲ではなくlexeme member抽出規則の退行と特定した監査 |
| [`candidate137-existing-case-observer-coverage-audit.md`](candidate137-existing-case-observer-coverage-audit.md) | `pending_effect_validation_admitted`を既存ケースで確実に発生させる方法はないと判定し、F04維持と停止条件を固定した監査 |
| [`candidate139-effect-satisfaction-witness-audit.md`](candidate139-effect-satisfaction-witness-audit.md) | F02部分変更の一次原因を`satisfied`の誤bindとし、次軸`effect_satisfaction_witness`を導出した監査 |
| [`candidate140-evidence-completeness-granularity-audit.md`](candidate140-evidence-completeness-granularity-audit.md) | F02低Scoreを分けた差がwitness定義ではなく変更前evidenceの粒度だと示した監査 |
| [`candidate141-post-result-change-admission-audit.md`](candidate141-post-result-change-admission-audit.md) | 残存失敗を、変更前request準備完了とresult受領後の変更開始準備完了が未分離であることへ帰属させた監査 |
| [`candidate145-f01-f02-f03-cost-causal-analysis.md`](candidate145-f01-f02-f03-cost-causal-analysis.md) | C145のコスト増加の先行分析を誤りと訂正し、`command_execution`件数とmodel step数の混同を明示した再集計 |
| [`candidate146-model-step-boundary-audit.md`](candidate146-model-step-boundary-audit.md) | `agent_message`をmodel step境界としてC125 / C145 / C146を再集計し、C146の増分機構なしと判定した監査 |
| [`candidate147-adoption-decision.md`](candidate147-adoption-decision.md) | C147の採用判断。品質・安定性・機構・コスト回収を別々に確認し、公開版`the-caption`へ投影した記録 |
| [`candidate81-candidate125-control-findings-synthesis.md`](candidate81-candidate125-control-findings-synthesis.md) | C81〜C125で有効だった制御の統合知見。抽象的注意ではなく実行時に観測できる条件へ閉じることが要点 |
| [`click-runtime-reproducibility.md`](click-runtime-reproducibility.md) | Click評価用known-goodランタイムを空環境から再構築し、offline full gateまで一致を確認した記録 |
| [`click-control-free-medium-baseline-analysis.md`](click-control-free-medium-baseline-analysis.md) | Click Control-free baselineがTHE-CAPTIONより軽い主因をリポジトリ / ケースのcontext量差として分離した分析 |
| [`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md) | Click C81 Mediumの残余経路をpaired差で再評価し、F01の悪化は非再現、F04 elapsed増加は再現性ありと判定した分析 |
| [`click-c81-full-portability-design.md`](click-c81-full-portability-design.md) | THE-CAPTION C81全文をClick root 1 targetへ改変なく水平適用する比較設計（外部妥当性の検証） |
| [`click-c125-full-portability-design.md`](click-c125-full-portability-design.md) | 同様にC125全文をClickへ水平適用し、Click Standard14 r2を各case`N=5`で実施する設計 |
| [`click-c81-repository-authority-standard14-r2-design.md`](click-c81-repository-authority-standard14-r2-design.md) | C81全文のみと、C81全文＋Click repository authorityを`click-standard14-r2`で比較する設計 |
| [`click-repository-authority-availability-design.md`](click-repository-authority-availability-design.md) | repository authorityの可用性差を、THE-CAPTIONで差が出たF10と同じ観点でClickへ移す比較設計 |
| [`click-repository-subagents-comparison-design.md`](click-repository-subagents-comparison-design.md) | Clickの階層別repository instructionの影響を、root制御プロンプトと分離して確認する比較設計 |
| [`delegation-cost-control-redesign.md`](delegation-cost-control-redesign.md) | ワーカー起動自体を失敗条件にせず、実行全体を3 KPIで判定するコスト判定・制御の再設計 |
| [`planning-first-route-diagnostic.md`](planning-first-route-diagnostic.md) | planning-first経路のrun別補助記録。ワーカー数の採点ではなくKPI差の説明に使う |
| [`sealed-execution-wave-design.md`](sealed-execution-wave-design.md) | 中間resultをmodelへ配送しないexecutor境界の第1版設計（`sealed_execution_wave.py`） |
| [`success-silent-delivery-design.md`](success-silent-delivery-design.md) | deterministicな成功resultだけをmodelへ配送しない`success-delivery/v1`第1版設計 |
| [`pytest-allowlist-success-delivery-design.md`](pytest-allowlist-success-delivery-design.md) | 成功出力の大半を占めるpytest系だけをexact argv boundなwrapper対象とする`success-delivery/v2`設計 |

## 8. historical handoff／superseded interpretation

内容は当時の記録として保持する。現行設計・現行値として読まない。各文書の冒頭バナーが位置づけを示す。

| 文書 | 位置づけ |
|---|---|
| [`candidate5-token-efficiency-direction.md`](candidate5-token-efficiency-direction.md) | root-only token由来の旧解釈。現行値はall-agent再集計へ置換済み |
| [`candidate6-candidate8-efficiency-investigation.md`](candidate6-candidate8-efficiency-investigation.md) | root-only token由来の調査履歴。現行値はall-agent再集計を参照 |
| [`candidate71-spec-audit-handoff.md`](candidate71-spec-audit-handoff.md) | C71 `SPEC`監査の完了済みhandoff。監査結果は`candidate71-control-abstraction-analysis.md`へ統合済み |
| [`prompt-control-review-handoff.md`](prompt-control-review-handoff.md) | C35〜C40時点の制御見直しの引き継ぎ記録。当時のbranch・HEAD・未commit差分を含む |
| [`sa-routing-condition-extraction.md`](sa-routing-condition-extraction.md) | candidate2設計の出発点となった`design_input`。その後の系譜は大きく進行 |
| [`prechange-information-sealed-repair-contract-spec.md`](prechange-information-sealed-repair-contract-spec.md) | 修正の要否と修正後条件を変更前レビューで決める旧仕様。C167〜C169の不通過を経て破棄し、現行設計へ継承しない |
| [`prechange-information-sealed-repair-contract-design-audit.md`](prechange-information-sealed-repair-contract-design-audit.md) | 破棄済み旧修正契約仕様に対する当時の設計監査 |
| [`prechange-information-sealed-repair-contract-targeted-evaluation-design.md`](prechange-information-sealed-repair-contract-targeted-evaluation-design.md) | 破棄済み旧修正契約系列のtargeted評価設計。現行設計の試験へ流用しない |
| [`candidate167-prechange-repair-contract-admission-design.md`](candidate167-prechange-repair-contract-admission-design.md) | 旧修正契約系列の履歴Candidate。targetedはScore `4 / 1 = 21 / 14`で停止 |
| [`candidate168-repair-evidence-burden-design.md`](candidate168-repair-evidence-burden-design.md) | 旧修正契約系列の履歴Candidate。targetedはScore `4 / 1 = 29 / 6`で停止 |
| [`candidate169-repair-decision-evidence-closure-design.md`](candidate169-repair-decision-evidence-closure-design.md) | 旧修正契約系列の履歴Candidate。targetedはScore `4 / 1 = 30 / 5`で停止 |
