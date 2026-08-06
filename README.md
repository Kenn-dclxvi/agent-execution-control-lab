# agent-execution-control-lab

AIエージェントの実行制御が成果品質・token・所要時間・実行経路へ与える影響を、再現可能に測る研究基盤です。

計測は評価対象repository（target）ごとのinstanceとして管理します。現在の登録instanceはTHE-CAPTION（`the-caption`）で、そのプロンプトを設計、比較、評価し、反映可能な形へまとめます。instance台帳は[`evaluations/targets/README.md`](evaluations/targets/README.md)を正本とします。

このリポジトリは2026-07-26に`THE-CAPTION-PROMPT`から改名しました。schema名prefix `the-caption-prompt.*`と既存bundle manifestの`construction_repository`は、保存済みresultへbindしたimmutableなidentityのため旧名のまま固定します（[`docs/repository-overview.md`](docs/repository-overview.md)）。

## 目的

- 現行プロンプトの参照元とidentityを固定する
- 候補プロンプトを本体から分離して構築する
- 同一条件で比較できる評価caseとprofileを管理する
- 評価済み候補をrelease単位でまとめる
- THE-CAPTION本体への反映を明示的な承認作業として扱う

## 現在の状態

`evaluation_foundation_v4`。1 case × 1 sampleのatomic runをappend-onlyで保存し、`N`をrun identityから分離しています。既存5 sampleから100 sampleへ増やす場合は95 sampleだけを追加し、分析時に使用run ID集合をwrite-onceで固定します。同じ`resource_class`のready runはanalysis conditionやdispatch件数が異なってもpair-awareな最大24 global queueへ投入できます。`total_tokens`はroot agentと全descendant SA sessionを合算するall-agent値です。v3 `prompt-set-result/v1` / `v2`とそれ以前のresultは履歴として保持し、元artifactを変更せずatomic runへ索引化できます。評価基盤はwinner、採用、本体反映、runtime有効化を判断しません。

## 主要な知見

観測された効率改善の要点は次のとおり。詳細と因果は[`docs/control-mechanisms.md`](docs/control-mechanisms.md)を参照。

- 不要なworker起動の抑制が最も効果が大きかった。
- 表面的なprompt短縮だけではall-agent tokenはほとんど動かなかった。
- 結論が変わらない場面の再判断（Decision Boundary）と、検証の一括化（Validation Closure）がstepとtokenを減らした（例: Validation ClosureのCandidate71はCandidate69比でtoken合計 -27.93%、top-level tool call -30.16%）。
- トークン削減の評価と、採用の判断は別レイヤーである。

## Candidate開発の経緯

BaselineからCandidate125までの系譜、固定した変更単位、保存evidence、評価状態は[`docs/candidate-history.md`](docs/candidate-history.md)にまとめる。candidate bundle 124件の系譜と現在状態の一覧は[`prompts/candidates/README.md`](prompts/candidates/README.md)にあり、identityの正本は各bundleの`manifest.json`（構築時provenanceとしてimmutable）とする。評価状態は、評価または診断を実施したcandidateでは独立したevaluation / diagnostic resultを正本とし、未実施の`not_evaluated`はresultが存在しないためindexの状態列を正本とする（manifestの`evaluation_status`は構築時の記録で、更新時にin-place変更しない）。本体へ投影済みなのはCandidate41・Candidate43・Candidate71・Candidate81・Candidate125（この順に積み上げた投影で直近はCandidate125）。release / approval / projection状態の正本は[`prompts/releases/README.md`](prompts/releases/README.md)。投影の実変更範囲は各release READMEを正本とし、[Candidate41は8 path](prompts/releases/the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1/README.md)、[Candidate43](prompts/releases/the-caption-3ce91a4-outcome-authority-boundary-release-r1/README.md)、[Candidate71](prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)、[Candidate81](prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md)、[Candidate125](prompts/releases/the-caption-3ce91a4-criterion-complete-single-target-continuation-release-r1/README.md)は各々直前投影からroot `AGENTS.md`一つである。

## 構成

| Path | 役割 |
| --- | --- |
| `docs/` | リポジトリ契約、設計判断、反映手順 |
| `prompts/baselines/` | 比較元プロンプトと取得元identity |
| `prompts/candidates/` | 構築中の候補プロンプト |
| `prompts/routes/` | 共通全文へ実行前合成する小さなroute差分 |
| `prompts/releases/` | 承認可能な単位へ固定したprompt bundle |
| `evaluations/cases/` | 評価caseとmodel-visible / private境界 |
| `evaluations/profiles/` | model、Agent、環境、反復条件、比較条件 |
| `evaluations/results/` | 公開済みの履歴評価結果。v3 runtime registryとは分離 |

運用境界は[`docs/repository-contract.md`](docs/repository-contract.md)を正本とします。
評価基盤のLayerと境界は[`docs/prompt-comparison-workflow.md`](docs/prompt-comparison-workflow.md)に定義します。実行方法は[`docs/evaluation-loop-manual.md`](docs/evaluation-loop-manual.md)、検証cloneの容量維持は[`docs/evaluation-storage-maintenance.md`](docs/evaluation-storage-maintenance.md)を参照します。
v3のall-agent token補正結果は[`evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md`](evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)に記録します。今後の制御追加、置換、削除は[`docs/prompt-control-design-principles.md`](docs/prompt-control-design-principles.md)を検討原則とします。Candidate5の評価整理と次candidateの設計方向は[`docs/candidate5-token-efficiency-direction.md`](docs/candidate5-token-efficiency-direction.md)、Candidate6からCandidate8までの効率化調査と設計結論は[`docs/candidate6-candidate8-efficiency-investigation.md`](docs/candidate6-candidate8-efficiency-investigation.md)に記録します。両設計文書のtoken由来の旧解釈はroot-only履歴であり、補正結果を現行値として扱います。

## 初期作業

1. THE-CAPTIONの対象commitと現行prompt identityを固定する
2. 現行promptを`prompts/baselines/`へ取り込む
3. 最初の候補が解く問題と非目標を定義する
4. 比較前にevaluation profileを固定する
5. 評価結果と承認を分けて記録する

## 今後の使い方と発展方針

このリポジトリは、AIエージェントの実行制御を設計・評価・改善する研究基盤として育てる。改善サイクル、評価setの育て方、model / runtime更新時の扱い、runtime制御への発展、採用判断の考え方は[`docs/future-roadmap.md`](docs/future-roadmap.md)にまとめる。

## ドキュメント

主要文書は次のとおり。`docs/`配下の研究文書は[`docs/README.md`](docs/README.md)で役割別（正本、現在の研究状態、完了済み研究記録、historical）に索引化しており、未完了の研究項目は[`docs/research-backlog.md`](docs/research-backlog.md)にまとめる。領域固有の作業規則は各`AGENTS.md`を正本とする。

研究内容を実務から読みたい場合は、[「AIへの指示は、短いほど安いのか？」](docs/01_why-prompt-writing-changes-your-bill.md)から始まる全8本のExecution Controlシリーズを参照してください。各記事は単体でも読め、ファイル名の`01`〜`08`が推奨順です。

| ドキュメント | 内容 |
| --- | --- |
| [`docs/repository-overview.md`](docs/repository-overview.md) | 初見向けの全体像・用語・評価基盤・現状 |
| [`docs/execution-control-measurement-report.md`](docs/execution-control-measurement-report.md) | 研究者向けの技術報告 第1版（2026-08-03）。品質制約下の指示書設計と実行経路の測定。数値と識別子は一次artifactを正本とする |
| [`docs/control-mechanisms.md`](docs/control-mechanisms.md) | トークンを大きく減らせた制御メカニズムの整理 |
| [`docs/candidate-history.md`](docs/candidate-history.md) | BaselineからCandidate147までの系譜と知見 |
| [`docs/candidate125-candidate147-control-findings-synthesis.md`](docs/candidate125-candidate147-control-findings-synthesis.md) | Candidate125のN拡張停止からCandidate147のN=100採用までの因果系列と統合知見 |
| [`docs/future-roadmap.md`](docs/future-roadmap.md) | 今後の運用・改善サイクル・runtime化の方針 |
| [`docs/repository-contract.md`](docs/repository-contract.md) | 運用境界の正本 |
| [`docs/prompt-comparison-workflow.md`](docs/prompt-comparison-workflow.md) | 評価基盤のLayerと境界 |
| [`docs/evaluation-loop-manual.md`](docs/evaluation-loop-manual.md) | 評価の実行手順 |
| [`docs/prompt-control-design-principles.md`](docs/prompt-control-design-principles.md) | 制御追加・置換・削除の検討原則 |

## 関連リポジトリ

「規約 → 計測 → 適用」の3層で運用している。本リポジトリは計測にあたる。

| リポジトリ | 役割 |
| :--- | :--- |
| [orchestration-prompt](https://github.com/Kenn-dclxvi/orchestration-prompt) | **規約**。エージェント実行制御の汎用プロンプトセット正本。ここで評価したCandidateを反映する |
| [agent-execution-control-lab](https://github.com/Kenn-dclxvi/agent-execution-control-lab) | **計測**。実行制御の効果を再現可能に測る研究基盤（本リポジトリ） |
| [the-caption](https://github.com/Kenn-dclxvi/the-caption) | **適用**。登録instance `the-caption` の実体。実運用しているポートフォリオ評価システム |

## License

[Apache License 2.0](LICENSE)。

ただし適用範囲には次の限定がある。case artifactの一部（`evaluations/cases/*/private/seed.patch`）は、評価対象instanceのrepository由来の小さなcode差分を含む。これらの権利は当該targetのrepositoryへ帰属し、このlicenseはそれを再許諾しない。
