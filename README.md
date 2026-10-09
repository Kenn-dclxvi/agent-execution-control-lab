# agent-execution-control-lab

AIエージェントの実行制御を再現可能に測る研究基盤です。

## 研究目的

AIエージェントにソフトウェア開発を任せるにあたり、人間の組織で使われてきた役割分担や仕事の進め方を取り入れてきました。この研究で確かめたいのは、**その枠組みを動かすためにどれだけのコストがかかり、どの部分を残せば、もともと守ろうとしていた品質を維持できるのか**ということです。

指示書がAIエージェントの進行・停止・完了をどう決めるかを実行制御と呼びます。このリポジトリは、品質を最適化対象ではなく維持すべき制約として固定したうえで、実行制御を変えたときの成果品質・費用（全エージェントの使用量を単価表で換算した値）・所要時間・実行経路を、比較可能な条件のもとで観測する研究基盤です。2026-10-09より前の計測は、費用の代わりに全エージェント合算トークンをKPIとしていました。

- 人間中心の開発プロセスをAIエージェントへ再現したときの実行コストを測る
- 品質責務を保ちながら削除・置換できる枠組みと、残す必要がある実行制御を対象インスタンス内で識別する
- 静的なプロンプト量と動的な実行量を分け、実行経路の効率を評価する
- 成立しなかった条件と測定上の限界も、再現可能な研究結果として残す

計測は評価対象リポジトリ（ターゲット）ごとのインスタンスとして管理します。プロンプト設計、比較、評価、反映可能な形へのまとめを実行している現行インスタンスはTHE-CAPTION（`the-caption`）です。インスタンス台帳は[`evaluations/targets/README.md`](evaluations/targets/README.md)を正本とします。

## 直近の計測（2026-10-09〜10、新しい基準）

THE-CAPTIONを対象にしたStandard14（STD14、全14ケース）を各5回（N=5、各条件70件）計測した結果です。2026-10-09から、次の条件で測る系列に切り替えました。それ以前の計測とは比較条件が違うため、数値を直接比べません。

- **実行環境：** エージェントを個人のシェル設定から切り離し、作業ツリーの`.venv`を明示的に有効にする（[記録](docs/agent-runtime-venv-isolation-record-r1.md)）。
- **KPI：** 品質、費用、経過時間の3つ。費用は全エージェントの使用量（キャッシュを使わない入力、キャッシュ読み取り、キャッシュ書き込み、出力）を単価表`api-standard-2026-10-09`で米ドルに換算した値です。全エージェント合算トークンは参考として記録します（[計測と記録の基準r2](docs/shared-instruction-evaluation-criteria-r2.md)）。
- **発行：** 同時実行の上限24本の内側で、実行中のCPU使用率が70%以下のときだけ次のrunを始める（[試行の記録](evaluations/results/c301-sonnet55-low-load-admission-trials_2026-10-09.md)）。

比べたプロンプトは次の3つです。中央値は各反復の14ケース合算値を5反復分から算出し、括弧内は5反復の最小〜最大です。

- **Free：** rootの`AGENTS.md`を空にしたもの。
- **C301：** C280（結果が決まるまで作業を始めない規則など）のMarkdownの書式を揃えたもの。新しい系列の基準です。
- **C309：** C301に、完了条件の確認を最後の確認と同じ応答で行い、その後は戻らない一文、既定値より短い待機時間を指定しない一文、確認コマンドの出力を絞ってよいとする一文を加えたもの（[設計記録](docs/candidate309-c307-final-check-unit-design.md)）。

### GPT-6.1 Sol Low

| プロンプト | 点数分布 | 品質中央値 | 費用中央値（USD） | 経過時間中央値（秒） | 生のトークン中央値（参考） |
| --- | --- | ---: | ---: | ---: | ---: |
| Free | 4点69件・0点1件 | 100.00 | 0.9344（0.8397〜0.9810） | 636.90（619.65〜667.13） | 2,218,847 |
| C301 | 4点70件 | 100.00 | 0.9260（0.8460〜1.0041） | 571.17（555.47〜585.48） | 1,871,588 |
| C309 | 4点70件 | 100.00 | 0.7809（0.7273〜0.8551） | 511.82（498.05〜527.98） | 1,439,210 |

C309はC301に対し、費用が−15.67%、経過時間が−10.39%で、どちらもC301の5反復の幅より下でした。C301は最初のリクエストがキャッシュに乗らなかったrunが多く（70件中31件、C309は12件）、費用が高めに出ています。この揺れを差し引いた見積もりでは、費用の差は約−8.3%です。

### Claude Code Sonnet 5.5 low

| プロンプト | 点数分布 | 品質中央値 | 費用中央値（USD） | 経過時間中央値（秒） | 生のトークン中央値（参考） |
| --- | --- | ---: | ---: | ---: | ---: |
| Free | 4点65件・0点5件 | 92.86 | 0.6997（0.6776〜0.7323） | 249.24（241.46〜261.62） | 859,525 |
| C301 | 4点70件 | 100.00 | 0.6811（0.6634〜0.6938） | 286.68（269.85〜343.71） | 822,676 |
| C309 | 4点70件 | 100.00 | 0.6637（0.6443〜0.6918） | 290.06（273.76〜308.29） | 777,420 |

C309はC301に対し、費用が−2.56%、経過時間が+1.18%で、どちらもC301の5反復の幅の中でした。Freeの経過時間が短いのは、A01で方針を確認せずに編集や試験へ進んだ分を含むためです。

### 分かったこと

- Freeの0点は、両セルともA01（求める結果が決まっていないケース）で、結果が決まる前に編集や試験へ進んだものです（Sonnet lowは5件中5件、Sol Lowは5件中1件）。C301とC309ではどちらも起きませんでした。
- C309は、Sol Lowで、確認の後にもう一度戻って出す呼び出し（C301は5反復で19回）、既定値より短い待機時間の指定（52回）、待機だけの呼び出し（23回）を、いずれも0回にしました。完了条件の確認（作業ツリーの状態の確認）は省かず、35件すべてで最後の確認と同じ呼び出しで行っていました。
- C309に至るまでに、成功後のコマンドを止める一文が、TaskSpecの求める確認や完了条件の確認まで止める弱点を、Sonnet lowで順に潰しました（[C305〜C307](evaluations/results/c305-c307-claude-sonnet55-low-standard14-n5_2026-10-10.md)、[C308](evaluations/results/c308-claude-sonnet55-low-standard14-n5_2026-10-10.md)、[C309](evaluations/results/c309-claude-sonnet55-low-standard14-n5_2026-10-10.md)）。

[3つの比較の記録](evaluations/results/free-c301-c309-sol61-low-sonnet55-low-standard14-n5_2026-10-10.md)、[Sol LowのC309とC301](evaluations/results/c309-sol61-low-standard14-n5_2026-10-10.md)。経過時間のうちモデルの応答時間は計測の時間帯で20〜30%揺れるため、時間差をプロンプトだけの効果とは断定しません。固定STD14内の観測であり、採用・本体反映は実施していません。

## 2026-10-06〜08の計測（旧系列）

以下は、実行環境を切り離す前の系列で、全エージェント合算トークンをKPIとしていた当時の記録です。上の新しい基準の計測とは比較条件が違うため、数値を直接比べません。

THE-CAPTIONを対象にしたStandard14（STD14）の結果です。まず全14ケースを各5回計測したN=5を示し、追加試験の累積N=20は別表に示します。N=5の各条件は70件の有効な実行からなります。品質中央値は各反復の14ケースを100点満点へ換算した値、トークンと時間の中央値は各反復の14ケース合算値を、それぞれ5反復分から算出しています。品質中央値100でも全件4点とは限らないため、点数分布を併記します。

### GPT-6.1 Sol Low

| プロンプト | 点数分布 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値（秒） | 記録 |
| --- | --- | ---: | ---: | ---: | --- |
| Free（10/6） | 4点64件・2点1件・0点5件 | 92.86 | 2,097,651 | 560.16 | [登録結果](evaluations/results/ecf6ece4009149e384fb29ab8ea40d35.json) |
| C276（10/6） | 4点70件 | 100.00 | 1,958,203 | 519.62 | [登録結果](evaluations/results/e8614a2ea0f74cdbaf9fd9084c0ceeff.json) |
| C280（10/7） | 4点70件 | 100.00 | 2,071,746 | 537.75 | [計測記録](evaluations/results/c280-sol61-low-standard14-n5_2026-10-07.md) |
| C281（10/7） | 4点70件 | 100.00 | 1,963,036 | 571.86 | [計測記録](evaluations/results/c281-sol61-low-standard14-n5_2026-10-07.md) |
| C282（10/7） | 4点70件 | 100.00 | 2,144,337 | 562.12 | [計測記録](evaluations/results/c282-sol61-low-standard14-n5_2026-10-07.md) |
| C283（10/7） | 4点70件 | 100.00 | 1,983,664 | 572.39 | [計測記録](evaluations/results/c283-sol61-low-standard14-n5_2026-10-07.md) |
| C284（10/7） | 4点70件 | 100.00 | 1,537,374 | 580.38 | [計測記録](evaluations/results/c284-sol61-low-standard14-n5_2026-10-07.md) |
| C285（10/7） | 4点70件 | 100.00 | 1,415,661 | 614.00 | [計測記録](evaluations/results/c285-sol61-low-standard14-n5_2026-10-07.md) |
| C286（10/7） | 4点70件 | 100.00 | 1,313,998 | 558.17 | [計測記録](evaluations/results/c286-sol61-low-standard14-n5_2026-10-07.md) |
| C287（10/7） | 4点70件 | 100.00 | 1,371,299 | 575.66 | [計測記録](evaluations/results/c287-sol61-low-standard14-n5_2026-10-07.md) |
| C288（10/7） | 4点70件 | 100.00 | 1,304,022 | 626.11 | [計測記録](evaluations/results/c288-sol61-low-standard14-n5_2026-10-07.md) |
| C289（10/8） | 4点70件 | 100.00 | 1,263,739 | 582.11 | [計測記録](evaluations/results/c289-sol61-low-standard14-n5_2026-10-08.md) |

C276はFreeに対し品質中央値が7.14ポイント高く、トークンは-6.65%、時間は-7.24%でした。C280〜C289は各70件すべて4点でした。C289のトークン中央値はC288より3.09%少なく、経過時間中央値は7.03%短い観測値でした。

[C276・Freeの計測記録](evaluations/results/sol61-c276-free-low-medium-standard14-new-n5_2026-10-06.md)、[C276とC280のケース別・個別KPI比較](evaluations/results/c280-c276-sol61-low-standard14-n5-per-run-comparison_2026-10-07.md)。各候補の変更内容と比較関係は[Candidate索引](prompts/candidates/README.md)を参照してください。

各ケース20回まで追加した結果は、上のN=5とは分けて示します。トークンと時間は各反復の14ケース合算値20件の中央値です。

| プロンプト | 点数分布 | 全エージェントトークン中央値 | 経過時間中央値（秒） | 記録 |
| --- | --- | ---: | ---: | --- |
| C283 | 4点280件 | 2,096,732 | 573.70 | [累積N=20](evaluations/results/c283-sol61-low-standard14-n20_2026-10-07.md) |
| C286 | 4点280件 | 1,314,863.5 | 537.53 | [累積N=20](evaluations/results/c286-sol61-low-standard14-n20_2026-10-07.md) |
| C288 | 4点280件 | 1,303,006.5 | 594.89 | [累積N=20](evaluations/results/c288-sol61-low-standard14-n20_2026-10-08.md) |
| C289 | 4点280件 | 1,262,119 | 571.33 | [累積N=20](evaluations/results/c289-sol61-low-standard14-n20_2026-10-08.md) |

C289はC288の累積N=20に対してトークン中央値が3.14%少なく、経過時間中央値は3.96%短い観測値でした。時間差には実行時刻や応答待ちの変動が含まれます。

### GPT-6.1 Sol Medium

| プロンプト | 点数分布 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値（秒） | 記録 |
| --- | --- | ---: | ---: | ---: | --- |
| Free | 4点65件・0点5件 | 92.86 | 2,708,904 | 662.60 | [登録結果](evaluations/results/3dd2e8bded274b5599ce72efaecd4a6a.json) |
| C276 | 4点70件 | 100.00 | 2,333,617 | 622.17 | [登録結果](evaluations/results/ad917ff0063f4ae2a099242b3f0cea9a.json) |

C276はFreeに対し品質中央値が7.14ポイント高く、トークンは-13.85%、時間は-6.10%でした。[条件と個別実行の記録](evaluations/results/sol61-c276-free-low-medium-standard14-new-n5_2026-10-06.md)を参照してください。

### GPT-6 Astra Low

| プロンプト | 点数分布 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値（秒） | 記録 |
| --- | --- | ---: | ---: | ---: | --- |
| Free | 4点65件・2点3件・0点2件 | 96.43 | 2,134,746 | 652.02 | [登録結果](evaluations/results/71163a1a328641f2ae1d447370253b7f.json) |
| C276 | 4点70件 | 100.00 | 1,944,598 | 616.53 | [登録結果](evaluations/results/09113d732579439cb3d84ade1c91fe4f.json) |

C276はFreeに対し品質中央値が3.57ポイント高く、トークンは-8.91%、時間は-5.44%でした。[計測記録](evaluations/results/astra6-c276-free-low-standard14-new-n5_2026-10-06.md)を参照してください。

### Claude Code Opus 5.5 Medium

| プロンプト | 点数分布 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値（秒） | 記録 |
| --- | --- | ---: | ---: | ---: | --- |
| Free | 4点68件・0点2件 | 100.00 | 1,196,005 | 501.72 | [登録結果](evaluations/results/aff3ca28282a452bb75b004506dfa1e1.json) |
| C276 | 4点70件 | 100.00 | 1,057,346 | 431.57 | [登録結果](evaluations/results/b3a245079bb94501a58c1fa5e08ec8c6.json) |
| C280 | 4点70件 | 100.00 | 1,058,318 | 448.52 | [登録結果](evaluations/results/10a2d444d80f4987a6a4d74e22fb8937.json) |
| C281 | 4点70件 | 100.00 | 1,068,110 | 371.40 | [計測記録](evaluations/results/claude-opus55-c281-standard14-n5-cli2288_2026-10-07.md) |
| C286 | 4点70件 | 100.00 | 1,328,871 | 436.94 | [計測記録](evaluations/results/claude-opus55-c286-standard14-n5-cli2288_2026-10-07.md) |

C276はFreeに対し4点が68件から70件へ増え、トークンは-11.59%、時間は-13.98%でした。C280、C281、C286も全70件が4点です。C286のトークン中央値はC280比25.56%増でした。Claude Code 2.1.288、Claude採点契約v2による独立系列です。最初のFree・C276・C280の計測では利用上限による除外が3条件合計285件あり、同じ枠を再実行しました。除外は品質失敗へ含めていません。[初回3条件の計測記録](evaluations/results/claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06.md)を参照してください。

C287は[各ケース2回の計測](evaluations/results/claude-opus55-c287-standard14-n2-cli2288_2026-10-07.md)で28件すべて4点でした。反復数を揃えたC280比ではトークン中央値が43.57%増でした。N=5の表とは混ぜていません。

### 比較の範囲と現在の状態

同じモデル・推論設定内では、固定したケース、TaskSpec、採点契約、実行環境を維持してプロンプトを比較しています。異なるモデルや実行環境の数値を、モデル単独の効果や総合順位として扱いません。実行日時と待ち行列の違いがあるため、時間差をプロンプトだけの因果効果とは断定しません。表の比較には除外・再試行を品質失敗として含めていません。

以上は固定STD14内の観測であり、別の課題への一般化や採用を示すものではありません。C280以降の表に挙げた計測に基づく採用・本体反映は実施していません。A01だけの試験や別の評価系列は、この集約表へ含めていません。

### 以前の計測

9月24〜25日のFree・C274・C276の数値とAPI費用の参考値は、[Free/C274統合比較](evaluations/results/free-c274-selected-model-summary_2026-09-24.md)、[Freeモデル比較](evaluations/results/control-free-model-reasoning-comparison_2026-09-24.md)、[C276 Luna Medium](evaluations/results/candidate276-execution-control-luna6-medium-standard14-n5-cli0156_2026-09-25.md)に残しています。9月末〜10月初旬を含む計測履歴は[結果索引](evaluations/results/README.md)から参照できます。

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
