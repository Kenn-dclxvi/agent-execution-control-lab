# agent-execution-control-lab

AIエージェントの実行制御を再現可能に測る研究基盤です。

これまでに分かった最も重要なことは、指示の効き目は短さや詳しさでは決まらないということです。必要な結果と実行の境界を正確に書けば、品質を保ったまま、エージェントの実行経路を改善できます。

## 研究目的

AIエージェントにソフトウェア開発を任せるにあたり、人間の組織で使われてきた役割分担や仕事の進め方を取り入れてきました。この研究で確かめたいのは、**その枠組みを動かすためにどれだけのコストがかかり、どの部分を残せば、もともと守ろうとしていた品質を維持できるのか**ということです。

指示書がAIエージェントの進行・停止・完了をどう決めるかを実行制御と呼びます。このリポジトリは、品質を最適化対象ではなく維持すべき制約として固定したうえで、実行制御を変えたときの成果品質・費用（全エージェントの使用量を単価表で換算した値）・所要時間・実行経路を、比較可能な条件のもとで観測する研究基盤です。2026-10-09より前の計測は、費用の代わりに全エージェント合算トークンをKPIとしていました。

- 人間中心の開発プロセスをAIエージェントへ再現したときの実行コストを測る
- 品質責務を保ちながら削除・置換できる枠組みと、残す必要がある実行制御を対象インスタンス内で識別する
- 静的なプロンプト量と動的な実行量を分け、実行経路の効率を評価する
- 成立しなかった条件と測定上の限界も、再現可能な研究結果として残す

計測は評価対象リポジトリ（ターゲット）ごとのインスタンスとして管理します。プロンプト設計、比較、評価、反映可能な形へのまとめを実行している現行インスタンスはTHE-CAPTION（`the-caption`）です。インスタンス台帳は[`evaluations/targets/README.md`](evaluations/targets/README.md)を正本とします。

## 直近の計測（2026-10-09〜12、新しい基準）

THE-CAPTIONを対象にしたStandard14（STD14、全14ケース）を各5回（N=5、各条件70件）計測した結果です。2026-10-09から、次の条件で測る系列に切り替えました。それ以前の計測とは比較条件が違うため、数値を直接比べません。

- **実行環境：** エージェントを個人のシェル設定から切り離し、作業ツリーの`.venv`を明示的に有効にする（[記録](docs/agent-runtime-venv-isolation-record-r1.md)）。
- **KPI：** 品質、費用、経過時間の3つ。費用は全エージェントの使用量（キャッシュを使わない入力、キャッシュ読み取り、キャッシュ書き込み、出力）を単価表で米ドルに換算した値で、比べる両方を同じ単価表（`api-standard-2026-10-10-r2`）で数え直しています。全エージェント合算トークンは参考として記録します（[計測と記録の基準r2](docs/shared-instruction-evaluation-criteria-r2.md)）。
- **発行：** 同時実行の上限24本の内側で、実行中のCPU使用率が70%以下のときだけ次のrunを始める（[試行の記録](evaluations/results/c301-sonnet55-low-load-admission-trials_2026-10-09.md)）。

比べたプロンプトは次の2つです。中央値は各反復の14ケース合算値を5反復分から算出し、括弧内は5反復の最小〜最大です。

- **Free：** rootの指示（`AGENTS.md`、Claude Codeでは`CLAUDE.md`）だけを空にしたもの。THE-CAPTIONのほかの指示や文書（`src/`・`tests/`などの局所の`AGENTS.md`、`docs/`、`prompts/`）は、C316を含むどの条件でも同じものを置いています。C316との違いは、rootに置いた6行だけです。
- **C316：** 現在の汎用指示。結果が決まるまで作業を始めない規則、事前調査を絞る規則、完了条件の確認を最後の確認と同じ応答で行いその後は戻らない規則、既定値より短い待機時間を指定しない規則、確認のコマンドを終了コードと判断に必要な出力だけを受け取る形で実行する規則、ファイルの本文を判断に必要な範囲だけ受け取る形で読む規則の6項目です（[設計記録](docs/candidate315-candidate316-c313-file-read-receive-form-design.md)、[本文](prompts/candidates/the-caption-3ce91a4-receive-form-file-read-range-r1/files/AGENTS.md.txt)）。

| モデル | 点数分布（Free → C316） | 費用 Free（USD） | 費用 C316（USD） | 費用の差 | 経過時間 Free（秒） | 経過時間 C316（秒） | 経過時間の差 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GPT-6.1 Sol Low | 4点69件・0点1件 → 4点70件 | 0.9344（0.8397〜0.9810） | 0.6421（0.5709〜0.6803） | −31.28%（幅より下） | 636.90 | 505.65 | −20.61%（幅より下） |
| GPT-6 Astra Low | 4点68件・0点2件 → 4点70件 | 6.1484（5.6532〜6.4405） | 4.1229（3.8843〜4.8369） | −32.94%（幅より下） | 634.75 | 497.36 | −21.65%（幅より下） |
| Claude Code Sonnet 5.5 low | 4点65件・0点5件 → 4点70件 | 0.6997（0.6776〜0.7323） | 0.6216（0.6097〜0.6469） | −11.17%（幅より下） | 249.24 | 232.75 | −6.62%（幅より下） |
| Claude Code Opus 5.5 low | 4点69件・0点1件 → 4点70件 | 1.2731（1.2379〜1.3126） | 1.1249（1.1058〜1.1410） | −11.64%（幅より下） | 269.41 | 247.12 | −8.27%（幅より下） |

差はFreeを基準にしたC316の差で、括弧内はFreeの5反復の幅に対する位置です。

### 分かったこと

- Freeの0点は、どのモデルでもA01（求める結果が決まっていないケース）で、結果が決まる前に編集や試験へ進んだものです。C316ではどのモデルでも起きませんでした。
- C316は4つのモデルすべてで、Freeより費用と経過時間が下がりました。下がり方はCodexの2モデル（Sol Low、Astra Low）で大きく、Claude Codeの2モデルでは小さくなっています。
- Sol LowのC316（70件）では、既定値より短い待機時間の指定と、300行を超えるファイルの本文を一度に全部読むことが0回、確認の後にもう一度戻って出す呼び出しが1回でした。完了条件の確認（作業ツリーの状態の確認）は、35件すべてで最後の確認と同じ呼び出しで行っていました（[記録](evaluations/results/c316-sol61-low-standard14-n5_2026-10-12.md)）。Sol LowとSonnet lowでは、C316を累積N=20まで測り、各セル280件がすべて4点で、費用の中央値もN=5と同じ程度でした（[記録](evaluations/results/c316-sonnet55-sol61-low-standard14-n20_2026-10-12.md)）。

### 読み方の注意

- Codexの2モデルでは、共通の先頭部分のキャッシュが別のrunの間でも共有されるため、計測の始めのrunで最初のリクエストがキャッシュに乗らないことがあります。乗らなかったrunは、Astra LowでFree 36件・C316 34件（どちらも単独で最初に流した計測）、Sol LowでFree 7件・C316 2件でした。費用は実測のままです（[診断の記録](evaluations/results/codex-first-request-cache-order-diagnostics_2026-10-10.json)）。
- 費用はモデルごとに単価が違うため、モデル間の金額の大小はモデルの優劣を示しません。
- 経過時間のうちモデルの応答時間は計測の時間帯で揺れるため、時間差をプロンプトだけの効果とは断定しません。
- 固定STD14内の観測です。C316は2026-10-12にリリースし、承認しました。THE-CAPTION本体へは反映していません（[リリース記録](prompts/releases/the-caption-3ce91a4-receive-form-file-read-range-release-r1/README.md)）。

記録：[4モデルの比較](evaluations/results/free-c316-four-models-standard14-n5_2026-10-12.md)。C316に至る経過（C301〜C316）は[results索引](evaluations/results/README.md)と[docs索引](docs/README.md)にあります。

## 実行制御で何が変わったか

新しい基準（2026-10-09以降）で、項目を一つずつ足したり外したりして測り直した結果、分かったことは次のとおりです。

- **固定したSTD14の品質を満たすうえで、人間の組織を模した役割分担（複数のエージェントによる分業やレビュー）は必須ではありませんでした。** 根拠は、組織を模した出発点（Baseline）と、rootの指示を空にしたFreeを、同じ条件のSTD14で並べた比較です。BaselineはrootのAGENTS.mdで、親エージェントは管理だけを行い、実装・監査・レビューをサブエージェントへ任せるよう定めています。Freeはこのroot指示だけを空にしており、ほかの文書は同じです（[2026-07-26](evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)、[2026-08-03](evaluations/results/baseline-control-free-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md)、どちらも旧系列のCodex）。
  - STD14は、この問いを確かめられるように組んだ14課題です（[課題集合](evaluations/sets/the-caption-standard14-r1/README.md)）。F01〜F10の12課題は、THE-CAPTIONの実際のリポジトリで、組織の役割が守ろうとしていた仕事（実装と必要な検証、レビュー、確認して止まる判断、範囲外の操作を断る判断、正しい手順の選択）を一つずつ課します。ただしF課題は、どう振る舞えばよいかを作業指示に書いてあるため、エージェント自身が不足に気づけるかは測れません。そこで、求める結果がリポジトリから決まらず確認して止まるべきA01と、リポジトリの規則から一意に決まり質問せずに進むべきA02を対にして加えました。止まりすぎても進みすぎても減点されるため、常に止まる指示や常に進む指示では満点になりません。
  - 採点は、最終的な成果物と、成果を確かめた証拠だけを0〜4点で見ます。どの役割が作業したか、レビューを経たかは点数に入りません。このため、役割分担のある指示とない指示を、同じ物差しで比べられます。
  - 組織の枠組みを置いても、品質は上がっていませんでした。70件中4点だった件数は、2026-07-26がBaseline 62件・Free 65件、2026-08-03がどちらも65件です。
  - Freeが失敗したのは、どちらの計測でもA01（求める結果が決まっていないケース）だけでした。結果が決まる前に編集や試験へ進んだものです。
  - Baselineも、A01では5件中3件で同じ失敗をしていました。さらに、Freeが一度も落とさなかったA02（リポジトリ内で経路を決めるケース）やF07（依存関係の出どころを確かめるケース）でも失敗しています。組織の枠組みは、Freeの失敗を確実には防がず、Freeにはなかった失敗を増やしていました。
  - A01の失敗は、分業ではなく、結果が決まるまで作業を始めないという一つの判断の誤りです。この判断を指示に書いたCandidate147と、現在のC316では、70件すべてが4点になりました。新しい基準でも、Freeの0点は4つのモデルすべてでA01だけで、C316では起きていません。
  - つまり、品質を守るのに残す必要があったのは、組織の役割分担ではなく、この一つの判断でした。ただし、これは固定したSTD14（THE-CAPTION）の範囲での観測です。今回の課題ではサブエージェントが起動しないため、分業が必要になる課題があるかどうかは確かめていません。
- **料金を決めるのは、指示の長さではなく、作業中の一手の数と受け取る量です。** 6行（1,687バイト）の指示（C316）で、4つのモデルすべての費用がFreeより11〜33%下がりました。Sol Lowでは、1セットあたりのツールの呼び出しが80回から58回に、受け取ったファイルの中身や出力が約526KBから約287KBに減っています。
- **結果が決まるまで作業を始めない規則が、品質を守っています。** Freeで満点にならなかった実行は、どのモデルでも、求める結果が決まる前に編集や試験へ進んだものでした。C316ではどのモデルでも起きていません。
- **作業の流れの中で決まる事実で書くと、無駄な一手が止まりました。** 「最後の変更の後、最後の確認と同じ応答で状態を確認する」「既定値より短い待機時間を指定しない」と書いた後、Sol Lowでは、確認の後にもう一度戻って出す呼び出し（C301は5反復で19回）と、短い待機時間の指定（同52回）が、ほぼなくなりました。
- **禁止より、させたい受け取り方を書くほうが効きました。** 「1回で300行を超えて受け取らない」と上限で禁止すると、小さいファイルまで分けて読むようになりました。「判断に必要な範囲だけを受け取る形で読む」と書くと、Sol Lowで300行を超えるファイルの全文取得が16回から0回になり、受け取る量が27%減りました。
- **効果の見えない項目は外しました。** 方針を一つにまとめる項目は、外しても費用・品質が変わりませんでした。担当を分ける項目は、今回の課題ではサブエージェントが起動せず測れないため外しました。

実務向けの説明は[実務ガイド](docs/practical-guide/README.md)、各Candidateの設計記録と計測記録は[docs索引](docs/README.md)と[results索引](evaluations/results/README.md)にあります。

2026-10-08までの旧系列（全エージェント合算トークンを指標とした計測）では、人間の組織を模した出発点（Baseline）からCandidate147までに、不要なワーカー起動の抑制、結論が変わらない場面の再判断の停止、検証の一括化によってトークンを約9割減らしました。その要点は[`docs/control-mechanisms.md`](docs/control-mechanisms.md)にあります。

構築したCandidateのバンドルは300件を超えます。本体への投影はCandidate41・43・71・81・125・147・274の7件で、公開版のTHE-CAPTIONには2026-08-03にCandidate147（[PR #13](https://github.com/Kenn-dclxvi/the-caption/pull/13)）、2026-09-08にCandidate274（[PR #27](https://github.com/Kenn-dclxvi/the-caption/pull/27)）を反映しました。新しい基準のC316は、2026-10-12にリリースして承認しました。THE-CAPTION本体へは反映しておらず、利用者の個人の共通指示（`~/.claude/CLAUDE.md`、`~/.codex/AGENTS.md`）に置いています（[リリース記録](prompts/releases/the-caption-3ce91a4-receive-form-file-read-range-release-r1/README.md)）。

| 知りたいこと | 正本 |
| --- | --- |
| 系譜、固定した変更単位、保存エビデンス、知見 | [`docs/candidate-history.md`](docs/candidate-history.md) |
| 全バンドルの現在状態と識別子 | [`prompts/candidates/README.md`](prompts/candidates/README.md) |
| release / approval / projection状態と投影の実変更範囲 | [`prompts/releases/README.md`](prompts/releases/README.md) |

## モデルが更新されたときの評価

STD14は、課題、作業の材料、採点の考え方を固定したまま、モデルごとの実行条件（CLIの版、実行環境、証跡の集め方、採点契約の版）を記録して測り直せます。CodexとClaude Codeでは実行環境と証跡の集め方が違うため、エージェント間で数値を直接比べることはしません。新しいモデルが出たときにこの試験を流すと、次の三つを確かめられます。

- **既知の弱点が新しいモデルでも出るか。** 結果が決まる前に作業へ進むA01の失敗は、Freeを測ったほとんどの条件で出ています。出なかったのは2026-09のGPT-6 Astra lowだけで、そのlowも10月の測り直しでは失点が出ました。出る件数はモデルと推論設定で変わります。
- **新しい弱点が出ていないか。** GPT-6 Luna mediumでは実装と検証を完了しない失点、Claude Code Opus 5.5 mediumでは確認すべき論点を確認しない失点が、A01以外で現れました。
- **今の指示がそのモデルでも効くか。** C147はGPT系のモデルでは品質を満点まで戻しましたが、Opus 5.5では戻りませんでした。これが、特定のモデルの流れに合わせない汎用指示（C316）へ進むきっかけになりました。

これまでのモデル別の結果は次のとおりです。数字は各条件70件のうち4点だった件数です。CLIの版、採点契約の版、計測の基準は時期によって違うため、比べるのは、同じモデル・同じ推論設定・同じ評価条件で測ったFreeと指示ありの間だけにしてください。複数のモデルや推論設定をまとめた行もあります。

| 時期 | モデル（推論設定） | Free | 指示あり | 分かったこと |
| --- | --- | --- | --- | --- |
| 2026-07〜08 | GPT-5.6 Sol（high・medium） | 65（A01で0点5件） | Baseline 62〜65、C147 70 | 組織を模したBaselineは品質を上げず、C147で満点になった。mediumのN=100でもFree 1,300 / 1,400件、C147 1,400 / 1,400件（[記録](evaluations/results/control-free-candidate147-v14-medium-standard14-atomic-n100-cli0146_2026-08-03.md)） |
| 2026-09-05〜08 | GPT-6 Astra（low・medium・high） | low 70、medium 68、high 66（失点はすべてA01） | C147・C274 70（medium） | 推論を強くするほどA01で先へ進んでしまう件数が増えた（[Free](evaluations/results/control-free-astra-low-medium-high-standard14-n5_2026-09-08.md)、[指示あり](evaluations/results/candidate274-c147-astra-medium-standard14-n5_2026-09-05.md)） |
| 2026-09-24 | GPT-6 Sol（low・medium・high） | 各65（A01で0点5件） | — | 推論設定によらず、A01だけで失点した（[記録](evaluations/results/control-free-sol6-low-medium-high-standard14-n5-cli0156_2026-09-24.md)） |
| 2026-09-24 | GPT-6 Luna（medium・high・xhigh） | medium 62、high・xhigh 65 | C147・C274 70（high） | mediumでは、A01に加えてF02・F07で実装や検証を完了しない失点が出た（[Free](evaluations/results/control-free-luna6-medium-high-xhigh-standard14-n5-cli0156_2026-09-24.md)、[指示あり](evaluations/results/candidate147-candidate274-luna6-high-standard14-n5-cli0156_2026-09-24.md)） |
| 2026-09-30 | GPT-6.1 Sol（low・medium） | 各65（A01で0点5件） | C147 low 70・medium 69 | GPT系では、C147がモデルの更新後も効き続けた（[記録](evaluations/results/sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30.md)） |
| 2026-10-01 | Claude Code Opus 5.5（medium） | 67 | C147 67、C276 67 | C147を入れても品質が上がらず、確認すべき論点を確認しない失点（F05）はむしろ増えた（[記録](evaluations/results/claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01.md)） |
| 2026-10-06 | GPT-6 Astra（low） | 65 | C276 70 | 9月には満点だったlowのFreeでも失点が出た（[記録](evaluations/results/astra6-c276-free-low-standard14-new-n5_2026-10-06.md)） |
| 2026-10-08〜10 | Claude Code Sonnet 5.5（low） | 65（A01で0点5件） | C280 70、C301・C309 70 | Freeで、A01の失点が測ったモデルの中で最も多かった。結果が決まるまで作業を始めない規則を入れると満点になった（[C280](evaluations/results/claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08.md)、[Free](evaluations/results/free-c301-c309-sol61-low-sonnet55-low-standard14-n5_2026-10-10.md)） |
| 2026-10-08 | Claude Code Haiku 5.5（low） | 未計測 | C280 69、C291 69 | 同じ規則を入れても、A01で0点が1件ずつ残った。同じ指示のOpus 5.5とSonnet 5.5では起きていない（[記録](evaluations/results/claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08.md)） |
| 2026-10-10〜12 | GPT-6.1 Sol、GPT-6 Astra、Claude Code Sonnet 5.5、Opus 5.5（いずれもlow） | 65〜69 | C316 すべて70 | 新しい基準で、汎用指示C316が4つのモデルすべてで満点になった。FreeのA01の失点はSonnet 5.5で最も多かった（[記録](evaluations/results/free-c316-four-models-standard14-n5_2026-10-12.md)） |

モデルが変わっても、Freeの失点の中心はA01でした。そのため、結果が決まるまで作業を始めないという判断は、モデルの更新を越えて残す必要がある制御だと言えます。一方、ほかの失点はモデルごとに現れ方が違います。新しいモデルでは、まずこの試験で、Freeと今の指示の両方を測り直すのがよいと考えています。

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
| 実務の観点から読む | [実務ガイド](docs/practical-guide/README.md)（全3本。指示で料金が変わる理由、書き方、人間の開発工程の移し方）。前に書いた[Execution Controlシリーズ](docs/01_why-prompt-writing-changes-your-bill.md)（全8本）も残しています |
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
