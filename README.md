# agent-execution-control-lab

AIエージェントの実行制御を再現可能に測る研究基盤です。

## 研究目的

本研究の中心は、AIエージェントへソフトウェア開発を委ねる際、**導入のために人間組織から借りたオーケストレーションの枠組みがどれだけの実行コストを要求し、そのどこを残せば守ろうとしていた品質責務を保てるのかを測定すること**です。

指示書がAIエージェントの進行・停止・完了をどう決めるかを実行制御と呼びます。このリポジトリは、品質を最適化対象ではなく維持すべき制約として固定したうえで、実行制御を変えたときの成果品質・全エージェント合算トークン・所要時間・実行経路を、比較可能な条件のもとで観測する研究基盤です。

- 人間中心の開発プロセスをAIエージェントへ再現したときの実行コストを測る
- 品質責務を保ちながら削除・置換できる枠組みと、残す必要がある実行制御を対象インスタンス内で識別する
- 静的なプロンプト量と動的な実行量を分け、実行経路の効率を評価する
- 成立しなかった条件と測定上の限界も、再現可能な研究結果として残す

計測は評価対象リポジトリ（ターゲット）ごとのインスタンスとして管理します。プロンプト設計、比較、評価、反映可能な形へのまとめを実行している現行インスタンスはTHE-CAPTION（`the-caption`）です。インスタンス台帳は[`evaluations/targets/README.md`](evaluations/targets/README.md)を正本とします。

## いま進めていること

9月24日時点の主要結果を、FreeとC274に分けて掲載します。各条件はStandard14の14ケースを5反復した70件で、全件有効、除外0件です。token中央値は各反復の14ケース合計を5反復で個別に中央値化した値です。

### Free

| モデル / 推論 | Score 4 / 0 | 入力 / 出力token中央値 | 全agent token中央値 | 総所要時間中央値 | API費用目安（70件） |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Astra / low | 70 / 0 | 2,020,189 / 13,567 | 2,033,901 | 777.51秒 | $107.54 |
| GPT-6 Sol / medium | 65 / 5 | 2,870,088 / 24,297 | 2,894,385 | 813.13秒 | $29.86 |
| GPT-6 Luna / high | 65 / 5 | 3,104,244 / 37,160 | 3,141,404 | 1,043.65秒 | $1.71 |
| GPT-5.6 Sol / medium（9/4） | 65 / 5 | 3,695,723 / 40,514 | 3,734,191 | 1,777.42秒 | $77.96 |

### C274

| モデル / 推論 | Score 4 / 0 | 入力 / 出力token中央値 | 全agent token中央値 | 総所要時間中央値 | API費用目安（70件） |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Astra / low | 70 / 0 | 未記録 | 1,474,356 | 631.48秒 | 算出不可 |
| GPT-6 Sol / medium | 70 / 0 | 1,789,594 / 20,281 | 1,809,875 | 681.90秒 | $18.60 |
| GPT-6 Luna / high | 70 / 0 | 1,768,213 / 40,173 | 1,808,386 | 975.93秒 | $0.98 |

各組内でのFree比は、C274でAstraが総token−27.51%・所要時間−18.78%、Solが−37.47%・−16.14%、Lunaが−42.43%・−6.49%でした。SolとLunaではScore 4が各65件から70件へ増え、AstraはFreeもC274も70件でした。GPT-5.6 Sol Mediumは9月4日のFree結果のみで、対になるC274 resultは登録資料で確認できません。

API費用はキャッシュ割引なしで、各70件全体の入力・出力token合計へ通常単価を当てた参考値です。実際のCodex Free請求額ではありません。Astra C274は入出力内訳が保存されていないため算出していません。9月24日のGPT-6 Sol/LunaはCLI 0.156.1、AstraとGPT-5.6 SolはCLI 0.153.3で実施日も異なります。モデル間の差をモデル単独の効果とはみなしません。また、固定された70件の観測をモデル全般や異なる課題へ一般化しません。

費用対品質点の順位とAPI単価、C274 LunaとFreeの追加比較は[Free/C274統合比較](evaluations/results/free-c274-selected-model-summary_2026-09-24.md)にまとめています。

### Candidate276・GPT-6 Luna Medium（2026-09-25）

Standard14を5反復した70件はすべて有効で、全件の採点分布はScore 4が68件、Score 1が1件、Score 0が1件でした。保存済みControl-Free Luna MediumとのN=5比較では、品質中央値は100.00点、全エージェントトークン中央値は2,330,083、経過時間中央値は681.60秒で、Control-Free比はそれぞれ品質+7.14ポイント、トークン-7.15%、経過時間-4.47%でした。これは固定Standard14・Luna Medium条件内の観測です。条件と採点分布を含む[Candidate276の試験記録](evaluations/results/candidate276-execution-control-luna6-medium-standard14-n5-cli0156_2026-09-25.md)を参照してください。

以前のAstra Low推奨は当時の固定条件に関する記録として[推論設定の推奨判定とトークン差の分析](docs/candidate274-astra-reasoning-recommendation-r1.md)に残しています。今日の横断表は[Free/C274統合比較](evaluations/results/free-c274-selected-model-summary_2026-09-24.md)、Free各条件の詳細は[Freeモデル比較表](evaluations/results/control-free-model-reasoning-comparison_2026-09-24.md)、各Candidateの詳細は[Sol C274](evaluations/results/candidate274-sol6-medium-standard14-n5-cli0156_2026-09-24.md)と[Luna High C147/C274](evaluations/results/candidate147-candidate274-luna6-high-standard14-n5-cli0156_2026-09-24.md)を参照してください。

## 実行制御で何が変わったか

観測された効率改善の要点は次のとおり。詳細と因果は[`docs/control-mechanisms.md`](docs/control-mechanisms.md)を参照。

- 不要なワーカー起動の抑制が最も効果が大きかった。
- 表面的なプロンプト短縮だけでは全エージェント合算トークンはほとんど動かなかった。
- 結論が変わらない場面の再判断（Decision Boundary）と、検証の一括化（Validation Closure）が手順数とトークンを減らした（例: Validation ClosureのCandidate71はCandidate69比でトークン合計 -27.93%、top-level tool call -30.16%）。
- トークン削減の評価と、採用の判断は別レイヤーである。

代表的な同一環境比較は次のとおり。

| プロンプト | スコア分布 | トークン中央値 | Baseline比 | 経過時間中央値 | Baseline比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 0 = 65 / 1 / 4` | 13,624,982 | — | 3,333.567秒 | — |
| Free | `4 / 0 = 65 / 5` | 3,488,611 | -74.40% | 1,166.296秒 | -65.01% |
| Candidate43 | `4 = 70` | 3,151,442 | -76.87% | 1,091.549秒 | -67.26% |
| Candidate71 | `4 = 70` | 2,030,116 | -85.10% | 988.187秒 | -70.36% |
| **Candidate147** | **`4 = 70`** | **1,447,626** | **-89.38%** | **852.543秒** | **-74.43%** |

Rating v14 Medium / Standard14 / atomic N=5。同一環境内だけの互換比較で、トークンは全エージェント合算の`total_tokens`。詳細と比較境界は[`evaluations/results/baseline-free-c43-c71-c147-cross-environment-trend_2026-08-03.md`](evaluations/results/baseline-free-c43-c71-c147-cross-environment-trend_2026-08-03.md)を参照。

この表に出るCandidateは、構築した162件のバンドルの一部です。本体への投影履歴はCandidate41・43・71・81・125・147・274の7件です。Candidate125までは移行前のTHE-CAPTIONを対象とし、公開版では2026-08-03にCandidate147（[PR #13](https://github.com/Kenn-dclxvi/the-caption/pull/13)）、2026-09-08にCandidate274（[PR #27](https://github.com/Kenn-dclxvi/the-caption/pull/27)）を反映しました。現在の共通制御と評価範囲は[Candidate274のrelease記録](prompts/releases/the-caption-3ce91a4-execution-boundary-core-release-r1/README.md)を参照してください。

| 知りたいこと | 正本 |
| --- | --- |
| 系譜、固定した変更単位、保存エビデンス、知見 | [`docs/candidate-history.md`](docs/candidate-history.md) |
| 全バンドルの現在状態と識別子 | [`prompts/candidates/README.md`](prompts/candidates/README.md) |
| release / approval / projection状態と投影の実変更範囲 | [`prompts/releases/README.md`](prompts/releases/README.md) |

## 構成

| パス | 役割 |
| --- | --- |
| `docs/` | リポジトリ契約、設計判断、反映手順 |
| `prompts/baselines/` | 比較元プロンプトと取得元の識別子 |
| `prompts/candidates/` | 構築中の候補プロンプト |
| `prompts/routes/` | 共通全文へ実行前合成する小さなルート差分 |
| `prompts/releases/` | 承認可能な単位へ固定したプロンプトバンドル |
| `evaluations/cases/` | 評価ケースとmodel-visible / private境界 |
| `evaluations/profiles/` | モデル、エージェント、環境、反復条件、比較条件 |
| `evaluations/results/` | 公開済みの履歴評価結果。v3のランタイムレジストリとは分離 |
| `evaluations/targets/agent-execution-control-lab/` | このリポジトリを対象とするAI PRレビュー測定のnamespacedインスタンス |

運用境界の正本は[`docs/repository-contract.md`](docs/repository-contract.md)です。その他の文書は[ドキュメント](#ドキュメント)を参照してください。

## ドキュメント

全文書の索引は[`docs/README.md`](docs/README.md)を正本とし、役割別（正本、現在の研究状態、完了済み研究記録、historical）に分類しています。未完了の研究項目は[`docs/research-backlog.md`](docs/research-backlog.md)、領域固有の作業規則は各`AGENTS.md`を正本とします。

読み始める場所は目的別に次のとおりです。

| 目的 | 入口 |
| --- | --- |
| 全体像・用語・評価基盤・現状を知る | [`docs/repository-overview.md`](docs/repository-overview.md) |
| 研究の問い・測定方法・結果・限界を読む | [`docs/execution-control-measurement-report.md`](docs/execution-control-measurement-report.md) |
| 実務の観点から読む | [「AIへの指示は、短いほど安いのか？」](docs/01_why-prompt-writing-changes-your-bill.md)（全8本のExecution Controlシリーズ。単体でも読め、ファイル名の`01`〜`08`が推奨順） |
| 今後の方針を知る（改善サイクル、評価セットの育て方、モデル / ランタイム更新時の扱い、ランタイム制御への発展、採用判断） | [`docs/future-roadmap.md`](docs/future-roadmap.md) |

作業を始める場所は次のとおりです。

| 作業 | 正本 |
| --- | --- |
| baseline / candidate / releaseのバンドル構築（形式・マニフェスト・格納） | [`docs/prompt-file-bundle.md`](docs/prompt-file-bundle.md) |
| 比較条件の固定（評価基盤のレイヤーと境界） | [`docs/prompt-comparison-workflow.md`](docs/prompt-comparison-workflow.md) |
| 評価の実行 | [`docs/evaluation-loop-manual.md`](docs/evaluation-loop-manual.md) |
| PRレビュー測定環境の検証・手動実行 | [`evaluations/targets/agent-execution-control-lab/README.md`](evaluations/targets/agent-execution-control-lab/README.md) |
| 新しいターゲットインスタンスの追加 | [`evaluations/targets/AGENTS.md`](evaluations/targets/AGENTS.md) |

## 関連リポジトリ

「出発点 → 計測 → 適用」の3層で運用している。本リポジトリは計測にあたる。

| リポジトリ | 役割 |
| :--- | :--- |
| [orchestration-prompt](https://github.com/Kenn-dclxvi/orchestration-prompt) | **出発点（V1）**。任意のリポジトリへ展開する前提で書かれた汎用プロンプトセット。本研究のBaselineは、これを`the-caption`へ適用した結果である |
| [agent-execution-control-lab](https://github.com/Kenn-dclxvi/agent-execution-control-lab) | **計測**。V1を出発点として候補を作り、実行制御の効果を再現可能に測る研究基盤（本リポジトリ） |
| [the-caption](https://github.com/Kenn-dclxvi/the-caption) | **適用**。登録インスタンス `the-caption` の実体。実運用しているポートフォリオ評価システムであり、採用したCandidateのreleaseはこのリポジトリへのプルリクエストとして記録する |

V1と本研究の系列を別リポジトリで育てている理由、および適用の実体は[`docs/execution-control-measurement-report.md`](docs/execution-control-measurement-report.md)の3節を参照。

## リポジトリ名の変更

このリポジトリは2026-07-26に`THE-CAPTION-PROMPT`から改名した。schema名の接頭辞 `the-caption-prompt.*`と既存バンドルのマニフェストにある`construction_repository`は、保存済みresultへbindした不変の識別子のため旧名のまま固定する（[`docs/repository-overview.md`](docs/repository-overview.md)）。

## ライセンス

[Apache License 2.0](LICENSE)。

ただし適用範囲には次の限定がある。ケースアーティファクトの一部（`evaluations/cases/*/private/seed.patch`）は、評価対象インスタンスのリポジトリ由来の小さなコード差分を含む。これらの権利は当該ターゲットのリポジトリへ帰属し、このライセンスはそれを再許諾しない。
