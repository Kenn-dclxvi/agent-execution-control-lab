# agent-execution-control-lab

## 研究目的

本研究の中心は、AIエージェントへソフトウェア開発を委ねる際、**導入のために人間組織から借りたオーケストレーションの枠組みがどれだけの実行コストを要求し、そのどこを残せば守ろうとしていた品質責務を保てるのかを測定すること**です。

指示書がAIエージェントの進行・停止・完了をどう決めるかを実行制御と呼びます。このリポジトリは、品質を最適化対象ではなく維持すべき制約として固定したうえで、実行制御を変えたときの成果品質・all-agent token・所要時間・実行経路を、比較可能な条件のもとで観測する研究基盤です。

- 人間中心の開発プロセスをAIエージェントへ再現したときの実行コストを測る
- 品質責務を保ちながら削除・置換できる枠組みと、残す必要がある実行制御を対象instance内で識別する
- 静的なprompt量と動的な実行量を分け、実行経路の効率を評価する
- 成立しなかった条件と測定上の限界も、再現可能な研究結果として残す

計測は評価対象repository（target）ごとのinstanceとして管理します。prompt設計、比較、評価、反映可能な形へのまとめを実行している現行instanceはTHE-CAPTION（`the-caption`）です。instance台帳は[`evaluations/targets/README.md`](evaluations/targets/README.md)を正本とします。

## いま進めていること

Candidate147を本体へ投影した後は、次の2軸を進めています。進行中の設計・診断文書は[`docs/README.md`](docs/README.md)の「現行frontier」を正本とします。

| 軸 | 現在地 |
| --- | --- |
| 機能見直し・review admission | Candidate147を基準に、過去機能の維持・休眠・欠落・prompt強制不能を一件ずつ判定しています。Candidate164から166でreview admissionの過不足を詰め、review挙動のcaseを再分類して次gateを7 case × N=5へ固定した段階です |
| 公開target拡張 | 公開target `click`（`pallets/click`）を第三者再現可能なinstanceとして登録し、Bundle Aのbaselineを確立しました。Bundle比較・採用・release・本体反映は未実施です |

計測に使う評価基盤は`evaluation_foundation_v4`です（1 case × 1 sampleのatomic runをappend-only保存し、比較時に使用run ID集合を固定。`total_tokens`はroot agentと全descendant SA sessionを合算するall-agent値。詳細は[`docs/repository-overview.md`](docs/repository-overview.md)）。基盤はwinner、採用、本体反映、runtime有効化を判断しません。

## 実行制御で何が変わったか

観測された効率改善の要点は次のとおり。詳細と因果は[`docs/control-mechanisms.md`](docs/control-mechanisms.md)を参照。

- 不要なworker起動の抑制が最も効果が大きかった。
- 表面的なprompt短縮だけではall-agent tokenはほとんど動かなかった。
- 結論が変わらない場面の再判断（Decision Boundary）と、検証の一括化（Validation Closure）がstepとtokenを減らした（例: Validation ClosureのCandidate71はCandidate69比でtoken合計 -27.93%、top-level tool call -30.16%）。
- トークン削減の評価と、採用の判断は別レイヤーである。

代表的な同一環境比較は次のとおり。

| Prompt | score分布 | token中央値 | Baseline比 | elapsed中央値 | Baseline比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 0 = 65 / 1 / 4` | 13,624,982 | — | 3,333.567秒 | — |
| Free | `4 / 0 = 65 / 5` | 3,488,611 | -74.40% | 1,166.296秒 | -65.01% |
| Candidate43 | `4 = 70` | 3,151,442 | -76.87% | 1,091.549秒 | -67.26% |
| Candidate71 | `4 = 70` | 2,030,116 | -85.10% | 988.187秒 | -70.36% |
| **Candidate147** | **`4 = 70`** | **1,447,626** | **-89.38%** | **852.543秒** | **-74.43%** |

Rating v14 Medium / Standard14 / atomic N=5。同一環境内だけの互換比較で、tokenはall-agent `total_tokens`。詳細と比較境界は[`evaluations/results/baseline-free-c43-c71-c147-cross-environment-trend_2026-08-03.md`](evaluations/results/baseline-free-c43-c71-c147-cross-environment-trend_2026-08-03.md)を参照。

この表に出るCandidateは、構築した162件のbundleの一部です。本体へ投影済みなのはCandidate41・43・71・81・125・147の6件（この順に積み上げ）で、Candidate125までは移行前のTHE-CAPTIONを対象とし、直近は2026-08-03にCandidate147を公開版`the-caption`（[PR #13](https://github.com/Kenn-dclxvi/the-caption/pull/13)）へ投影しました。

| 知りたいこと | 正本 |
| --- | --- |
| 系譜、固定した変更単位、保存evidence、知見 | [`docs/candidate-history.md`](docs/candidate-history.md) |
| 全bundleの現在状態とidentity | [`prompts/candidates/README.md`](prompts/candidates/README.md) |
| release / approval / projection状態と投影の実変更範囲 | [`prompts/releases/README.md`](prompts/releases/README.md) |

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

運用境界の正本は[`docs/repository-contract.md`](docs/repository-contract.md)です。その他の文書は[ドキュメント](#ドキュメント)を参照してください。

## ドキュメント

全文書の索引は[`docs/README.md`](docs/README.md)を正本とし、役割別（正本、現在の研究状態、完了済み研究記録、historical）に分類しています。未完了の研究項目は[`docs/research-backlog.md`](docs/research-backlog.md)、領域固有の作業規則は各`AGENTS.md`を正本とします。

読み始める場所は目的別に次の3つです。

| 目的 | 入口 |
| --- | --- |
| 全体像・用語・評価基盤・現状を知る | [`docs/repository-overview.md`](docs/repository-overview.md) |
| 研究の問い・測定方法・結果・限界を読む | [`docs/execution-control-measurement-report.md`](docs/execution-control-measurement-report.md) |
| 実務の観点から読む | [「AIへの指示は、短いほど安いのか？」](docs/01_why-prompt-writing-changes-your-bill.md)（全8本のExecution Controlシリーズ。単体でも読め、ファイル名の`01`〜`08`が推奨順） |
| 今後の方針を知る（改善サイクル、評価setの育て方、model / runtime更新時の扱い、runtime制御への発展、採用判断） | [`docs/future-roadmap.md`](docs/future-roadmap.md) |

作業を始める場所は次のとおりです。

| 作業 | 正本 |
| --- | --- |
| baseline / candidate / releaseのbundle構築（形式・manifest・格納） | [`docs/prompt-file-bundle.md`](docs/prompt-file-bundle.md) |
| 比較条件の固定（評価基盤のLayerと境界） | [`docs/prompt-comparison-workflow.md`](docs/prompt-comparison-workflow.md) |
| 評価の実行 | [`docs/evaluation-loop-manual.md`](docs/evaluation-loop-manual.md) |
| 新しいtarget instanceの追加 | [`evaluations/targets/AGENTS.md`](evaluations/targets/AGENTS.md) |

## 関連リポジトリ

「出発点 → 計測 → 適用」の3層で運用している。本リポジトリは計測にあたる。

| リポジトリ | 役割 |
| :--- | :--- |
| [orchestration-prompt](https://github.com/Kenn-dclxvi/orchestration-prompt) | **出発点（V1）**。任意のリポジトリへ展開する前提で書かれた汎用プロンプトセット。本研究のBaselineは、これを`the-caption`へ適用した結果である |
| [agent-execution-control-lab](https://github.com/Kenn-dclxvi/agent-execution-control-lab) | **計測**。V1を出発点として候補を作り、実行制御の効果を再現可能に測る研究基盤（本リポジトリ） |
| [the-caption](https://github.com/Kenn-dclxvi/the-caption) | **適用**。登録instance `the-caption` の実体。実運用しているポートフォリオ評価システムであり、採用したCandidateのreleaseはこのリポジトリへのプルリクエストとして記録する |

V1と本研究の系列を別リポジトリで育てている理由、および適用の実体は[`docs/execution-control-measurement-report.md`](docs/execution-control-measurement-report.md)の3節を参照。

## リポジトリ名の変更

このリポジトリは2026-07-26に`THE-CAPTION-PROMPT`から改名した。schema名prefix `the-caption-prompt.*`と既存bundle manifestの`construction_repository`は、保存済みresultへbindしたimmutableなidentityのため旧名のまま固定する（[`docs/repository-overview.md`](docs/repository-overview.md)）。

## License

[Apache License 2.0](LICENSE)。

ただし適用範囲には次の限定がある。case artifactの一部（`evaluations/cases/*/private/seed.patch`）は、評価対象instanceのrepository由来の小さなcode差分を含む。これらの権利は当該targetのrepositoryへ帰属し、このlicenseはそれを再許諾しない。