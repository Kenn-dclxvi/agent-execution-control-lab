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

週末から進めたSol・Astra比較と、9月8日のAstra推論設定5段階の評価をまとめました。**C274を使うTHE-CAPTIONの通常作業には、Astraのlow（軽）を推奨します。** 成果条件と必要な検証が明確な今回の試験では、品質点を保ちながら所要時間が最も短い設定でした。

観測されたAstraの特徴は次のとおりです。

- **未指定の成果を確認する傾向がある。** 共通制御を外した比較では、Solよりも確認して止まる例が多くありました。一方、編集前にファイル全文を広く読み、出力の省略で必要情報を読み直す例もあり、探索の効率まで自動的に良くなるわけではありません。
- **プロンプトの短さより、判断の往復を抑える制御が効く。** C147は推測して進む動作と不要な探索を抑え、SolとAstraの品質・トークン量を近づけました。検証中の判断往復を抑える境界まで削ったC273ではトークンが増え、その境界を保持したC274で回復しました。
- **推論設定を上げても、品質改善に直結しなかった。** highまではトークン総量が小さく、xhigh・maxでは待機、探索の分割、テスト選択のやり直しに伴う追加呼び出しと履歴入力が増えました。maxとlowの総トークン差の約88%は入力増で、直接の推論出力の増加は約9%でした。

C274・Astra・CLI 0.153.3を固定し、Standard14の14ケースを各5回、5設定で計350件実行した結果です。mediumは9月8日の再計測を使っています。

| 推論設定 | Score 4の件数 | トークン中央値 | 総所要時間中央値 | 選び方 |
| --- | ---: | ---: | ---: | --- |
| **low（軽）** | **70/70** | **1,474,356** | **631.48秒** | **通常用途の推奨** |
| medium | 70/70 | 1,494,822 | 659.69秒 | lowに近い次点 |
| high | 70/70 | 1,444,257 | 731.97秒 | トークン総量を優先する場合の代替 |
| xhigh | 70/70 | 1,670,312 | 1,295.22秒 | 今回は追加時間に見合う品質改善なし |
| max（最大） | 67/70 | 1,883,688 | 2,203.13秒 | 今回は追加時間・トークンに見合う品質改善なし |

トークンと時間は、各反復の14ケース合計から求めた5反復の中央値です。並列試験全体の待ち時間ではありません。maxの残り3件は確認質問に選択肢`daily`を明示しなかったためScore 2であり、確認せず実装を始めた失敗ではありません。

lowはmediumより時間が4.28%、トークンが1.37%少ないものの、時間のばらつきは重なります。highはlowよりトークンが2.04%少ない代わりに時間が15.91%長く、トークン総量の最小値を料金の最小値とは扱いません。highの削減は主に呼び出し減による履歴入力の減少で、直接の推論出力は増えていました。

推奨はこの固定評価の範囲に限ります。未知の設計・研究やAstra全般の優劣を判定したものではなく、総所要時間には開始・終了前後の待ちも含まれ、試験順も無作為化していません。詳しい根拠は[週末からの計測推移とSol・Astraの動作の特徴](docs/sol-astra-c147-c274-measurement-synthesis-r1.md)、[推論設定の推奨判定とトークン差の原因分析](docs/candidate274-astra-reasoning-recommendation-r1.md)を参照してください。

共通制御を外したFreeでも、9月8日にAstraのlow・medium・highを同じStandard14各N=5で計測しました。Score 4は順に70/70・68/70・66/70件で、トークン・総所要時間はlow、medium、highの順に増えました。数値と固定条件は[Freeの3設定比較](evaluations/results/control-free-astra-low-medium-high-standard14-n5_2026-09-08.md)を参照してください。

**Astraは仕様不足を認識しても、確認待ちで止まるとは限りません。** 変更先が未指定のA01では、lowは5件とも読み取り後に確認して止まりました。medium・highでは、確認前に現状テストを行う例と、既存の選択肢から変更先を推測して編集する例が増え、highには質問を表示した後も回答を待たず変更した例がありました。ただし、現状テストだけの実行もScore 0とする採点条件は、関連テストを許可する提示条件と差があります。推測による編集と同じ失敗にはまとめず、各5件の傾向をAstra全般へ一般化しません。詳しくは[A01の実行経路と採点上の限界](docs/astra-free-a01-reasoning-route-audit-r1.md)を参照してください。

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
