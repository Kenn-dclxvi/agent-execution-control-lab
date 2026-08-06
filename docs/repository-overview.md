# リポジトリ概要（初見の人向け）

このドキュメントは、`agent-execution-control-lab`リポジトリを初めて見る人が、全体像・作成済みプロンプト・評価の仕組み・採点条件の考え方を一通り把握できるようにまとめたものです。詳細な正本は各節末尾のリンク先を参照してください。個別の研究事例は別文書へ分離しています（例: A02の採点ずれは[`a02-rating-divergence.md`](a02-rating-divergence.md)）。

## 1. このリポジトリは何をする場所か

AIエージェントの実行制御を与える**プロンプト（AIへの指示書）を設計・比較・評価し、反映可能な形へまとめる**ための計測基盤です。計測は評価対象repository（target）ごとのinstanceとして管理し、現在の登録instanceはTHE-CAPTION（`the-caption`、別リポジトリの本体システム）だけです。instance台帳と境界は[`evaluations/targets/README.md`](../evaluations/targets/README.md)を正本とします。

- **やること**: 現行プロンプトの固定、候補プロンプトの構築、同一条件での評価、評価済み候補のrelease化。
- **やらないこと（スコープ外）**: target本体のruntime（実行時の挙動）そのものの変更。本体への反映・PR・マージ・有効化は、**明示的に依頼されたときだけの別作業**として扱います。

重要な区別として、このリポジトリは **「artifactが存在すること」と「評価済み・採用済み・本体反映済みであること」を混同しません**。評価はあくまで観測で、採用や本体適用は人が別途下す判断です。

### 1.1 リポジトリ名と識別子の名前空間

このリポジトリは2026-07-26に`THE-CAPTION-PROMPT`から`agent-execution-control-lab`へ改名しました。計測対象を単一targetから複数instanceへ広げる方針に合わせた変更で、評価基盤の境界、KPI、compatibility条件は変えていません。

次の識別子は保存済みresultへbindしたimmutableなidentityであり、**改名しても旧名のまま固定します**。

| 識別子 | 状態 | 理由 |
| --- | --- | --- |
| schema名prefix `the-caption-prompt.*` | 旧名で固定 | 20種類以上のschemaで使用し、保存済みresultとprofileへbind済み。[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)のImmutable historyが上書きを禁じる |
| 既存bundle manifestの`construction_repository` | 旧名で固定 | 構築時provenanceであり、in-place変更しない。GitHubのrename redirectで解決できる |
| prompt set identity（`the-caption-*`） | 旧名で固定 | target instance `the-caption`の名前空間であり、改名の対象ではない |

新しく生成するbundleの`construction_repository`は新しいURLを記録します。過去の記述を当時のまま残す文書（historical／superseded分類）は旧pathのまま保持します。

## 2. 基本用語

- **プロンプト（prompt）/ bundle**: AIへ渡す指示書一式。`AGENTS.md`等のファイル群をまとめた単位を bundle と呼びます。
- **baseline**: 比較の起点となる、現行プロンプトの固定スナップショット。
- **candidate（候補）**: baselineから派生させた改良案。`C1`〜`C78`のように番号で呼びます。
- **release**: 評価を経て、本体へ反映可能な単位として固定した候補。
- **token（トークン）**: AIが入出力を処理する量の単位。多いほど時間と費用が増えます。
- **all-agent `total_tokens`**: 統括役のroot agentと、そこから起動された全ての下位セッション（SA session＝worker）の使用量を合算した値。workerが増えると合計は大きく膨らみます。
- **case（評価case）**: プロンプトの挙動を測るための、症状・対象・成功条件を定めたテスト課題。`TC-F01`〜`TC-A06`など。
- **model-visible / private（model-invisible）**: 実行役のAIに提示する情報（model-visible）と、採点用の正解・期待diff・oracleが参照する確認コマンド等の隠す情報（private）を厳密に分けます。privateに確認コマンドがあっても、それは実行役へ課された必須試験ではありません（必須試験はTaskSpecまたは適用されるリポジトリ規則が要求するものだけ）。

## 3. ディレクトリ構成

| Path | 役割 |
| --- | --- |
| `prompts/baselines/` | 比較元プロンプト（現行の固定スナップショット）。2件（`current-r1` / `current-r2`）。 |
| `prompts/candidates/` | 構築中の候補プロンプト。設計上はC81まで、bundleとして79件を保存。 |
| `prompts/routes/` | 共通の全文へ実行前に合成する小さな差分（route）。 |
| `prompts/releases/` | 本体へ反映可能な単位に固定したrelease。7件。 |
| `evaluations/cases/` | 評価case（63件、revision別directory）とmodel-visible / private境界。 |
| `evaluations/sets/` | caseを束ねた評価集合（例: `the-caption-standard14-r1`）。 |
| `evaluations/fixtures/` | caseが使う擬似リポジトリ状態。 |
| `evaluations/profiles/` | model・環境・反復条件・比較条件を固定したprofile。354件。 |
| `evaluations/rating-contracts/` | 採点条件（rating contract）をrevision別に保存。14 revision（v1〜v14）。 |
| `evaluations/results/` | 公開済みの評価結果（append-only）。runを重ねるごとに増えるため、現況は同ディレクトリを参照（2026-08-07時点で278件、READMEを除く）。 |
| `layer2/` | token内訳やsession情報など、KPIへ入れない補助データの保存先。 |
| `docs/` | リポジトリ契約、設計判断、反映手順。 |
| `scripts/` | 評価ループや証拠収集のスクリプト。 |

正本: [`docs/repository-contract.md`](repository-contract.md)、ルートの[`README.md`](../README.md)。

## 4. 評価の仕組み（evaluation foundation v4）

### 4つのLayerと3つのKPI

評価は4つのLayerに限定されます。各Layerは自分の出力だけを作り、前段のartifactを変えません。

1. **Evaluation set** — どのcaseで測るかを固定する。
2. **Execution** — 固定条件でプロンプトを実行し、一次結果を保存する。
3. **Quality rating** — case成果を0〜4で採点する（`quality_score`）。
4. **KPI comparison** — 保存済み結果から比較viewを作る。

扱うKPIは次の**3つだけ**です。

- **`quality_score`**: caseごとの成果を0〜4点で採点した値。
- **`total_tokens`**: all-agent（root＋全worker）の合算トークン。
- **`elapsed_seconds`**: 所要時間。

### 互換条件（compatibility key）

2つの結果を比較してよいのは、**評価集合・対象リポジトリ版・model・環境・権限・fixture・case・反復条件などが全て一致するとき**だけです。この一致を1つのハッシュ（compatibility key）で表し、キーが違う結果を暗黙に混ぜません。

### この基盤が「出さない」もの

- `winner`（勝ち負け）、改善・悪化の断定、KPIの優先順位。
- 採用・release・本体反映の判断。

つまり評価基盤は**判断材料（数値）を並べるだけ**で、優劣や採否は決めません。採否は人が別に判断します。

正本: [`docs/prompt-comparison-workflow.md`](prompt-comparison-workflow.md)、[`docs/evaluation-loop-manual.md`](evaluation-loop-manual.md)。

## 5. 作成済みプロンプト

### baseline（2件）

現行プロンプトの固定スナップショット。`the-caption-3ce91a4-current-r1` と `-r2`。すべての候補はここから派生します。

### candidate（C1〜C166、bundle 162件保存）

baselineから枝分かれした改良案です。番号順が単純な親子ではなく、いくつかの系譜に分かれています（例: compact構造を保つC1系、完了志向を保つC5系）。開発の主眼は一貫して「**品質を保ったままall-agentトークンを減らす制御**」の探索でした。トークンを大きく減らせた制御の分類と教訓は、[`docs/control-mechanisms.md`](control-mechanisms.md)にまとめています。

bundle 162件はすべてcandidate index（[`prompts/candidates/README.md`](../prompts/candidates/README.md)）の表に掲載しています。正本は責務ごとに分かれます。identityは各`manifest.json`（構築時provenanceとしてimmutable）、系譜と観測の整理は[`docs/candidate-history.md`](candidate-history.md)です。評価状態は、評価または診断を実施したcandidateでは独立したevaluation / diagnostic resultが正本で、未実施の`not_evaluated`はresultが存在しないためindexの状態列が正本です。manifestの`evaluation_status`は構築時の記録で、状態更新時にin-place変更しません。indexは実施済みcandidateについては一覧と導線です。

掲載candidateには互換比較できないものが含まれます。C45〜C48はA06の広域監査を`N=1`で観測した`diagnostic_only / memory_off`の枝で、いずれも診断resultを`evaluations/results/`へ保存していますが、blind quality ratingを実施していないため`quality_score`は保存せず、状態は`draft`です。標準14項目やB18と互換な品質比較ではありません。C72/C73は対象4項目各`N=5`で`targeted_evaluated`ですが、いずれも`stopped`です。indexへの掲載は、評価済み・採用済みを意味しません。

### release（7件）と本体反映状況

正本`prompts/releases/README.md`はrelease status / approval / runtime projectionを別軸で保持する。ここでも同じ3軸に分けて示す。

| release（由来候補） | release status | approval | runtime projection | 本体反映 |
| --- | --- | --- | --- | --- |
| **Candidate147** | `projected` | `approved` | `projected` | **反映済み・承認済み**（公開版`the-caption` [PR #13](https://github.com/Kenn-dclxvi/the-caption/pull/13)、直前投影からroot `AGENTS.md`一つ） |
| **Candidate125** | `projected` | `approved` | `projected` | **反映済み・承認済み**（THE-CAPTION [PR #345](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/345)、直前投影からroot `AGENTS.md`一つ） |
| Candidate34 | `cancelled` | `cancelled` | `not_authorized` | なし（不採用・artifact削除ではない） |
| Candidate41 | `projected` | `approved` | `projected` | **反映済み**（THE-CAPTION [PR #334](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/334)、実変更8 path）。直前の投影履歴・C43の巻き戻し先として維持 |
| **Candidate43** | `projected` | `approved` | `projected` | **反映済み**（THE-CAPTION [PR #335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335)、直前投影からroot `AGENTS.md`一つ） |
| **Candidate71** | `projected` | `approved` | `projected` | **反映済み・承認済み**（THE-CAPTION [PR #340](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/340)、直前投影からroot `AGENTS.md`一つ） |
| **Candidate81** | `projected` | `approved` | `projected` | **反映済み・承認済み**（THE-CAPTION [PR #343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343)、直前投影からroot `AGENTS.md`一つ） |

現在の本体投影は、Candidate41 → Candidate43 → Candidate71 → Candidate81 → Candidate125 → Candidate147の順に積み上げたreleaseです。直近のCandidate147は、resultの停止効果をtask全体へ広げず、実際に影響を受けるoperation classだけへ限定します。Standard14 N=100で1,400 / 1,400件がscore `4`、targeted F01 / F02 / F03で狙った機構が15 / 15件成立し、Candidate145で生じたcost増加をCandidate125付近へ戻したという判断で2026-08-03に採用しました（正本: [`candidate147-adoption-decision.md`](candidate147-adoption-decision.md)）。F06のauthority追加readは21 / 100件残っており、quality failureではないが除去済みとは扱いません。

Candidate125までの投影は移行前のTHE-CAPTIONを対象とし、Candidate147は公開版`the-caption`を対象とします（公開移行の時間境界は本節末の「対象リポジトリの公開移行」を参照）。Candidate125は、一つのeditable targetが全未解決変更criterionを所有する場合に限定して、同じtargetへのcriterion-complete continuationを一度許可した版です。Candidate125 N=100追試は投影状態と分離して実施し、registered poolを各case30件まで拡張した時点でF04 score `2`を5件確認して停止しました。N=30 selection resultは未作成です。C41・C43・C71・C81・C125は投影履歴かつ巻き戻し先として保持し、`cancelled`にはしません。

正本: [`prompts/candidates/README.md`](../prompts/candidates/README.md)、[`prompts/releases/README.md`](../prompts/releases/README.md)、[`prompts/baselines/README.md`](../prompts/baselines/README.md)。

## 6. 評価caseと採点条件

### 標準14項目セット

主要な評価集合 `the-caption-standard14-r1` は、機能系のF01〜F10（12件）に、曖昧性境界のA01・A02を加えた14 caseです。各caseを`N=5`（5回）など複数反復して測ります。

caseは「提示する情報（model-visible）」と「隠す情報（private: 正規の起動先、期待するdiff、oracleが参照する確認コマンドなど）」を分けて設計します。ここで、privateに確認コマンドが存在することと、それが実行役へ課された必須試験であることは別です。必須試験はTaskSpecまたは適用されるリポジトリ規則が要求するものに限られます。この区別を崩すと、品質低下と採点のずれを混同しかねません。

### 採点条件（rating contract）

採点条件はrevision別に固定し、in-placeで書き換えません（結果を見た後の基準変更は必ず新revision）。最新revisionは**v14**で、v13の条件（提示した抽象成果条件を特定コマンドへ具体化して必須化しない。コマンド名までmodel-visibleに明示された必須試験だけを品質へ反映する）をすべて維持したうえで、A01だけを応答文面の分類からversioned terminal-state evidenceへ切り替えます。疑問符や質問語といった文面特徴はこの状態の導出とscoreに使いません。既存のv13以前の契約と結果は履歴として保持します。

新規runへ適用する「現行」契約も**v14**です（指定の正本は[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)、revision別要求の正本は[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)）。2026-07-26に[`6条件の標準14項目各N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録しました。v14はv13とは別のcompatibility conditionであり、v13以前のresultと同一comparisonへ混ぜません。

この論点の具体例（A02で実際に起きた「要求と採点のずれ」3件、v10〜v13の変遷）は、個別事例として[`a02-rating-divergence.md`](a02-rating-divergence.md)へ分離しています。

正本: [`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)。

### 対象リポジトリの公開移行（2026-08-01〜08-03）

登録instance `the-caption` の実体は公開のための移行を行った。3リポジトリの関係は[root `README.md`](../README.md)を正本とする。

本リポジトリの記録には**公開日という時間の境界**がある。

- **2026-08-01より前の記録は、移行前のリポジトリを対象としている。** manifest、profile、release、resultが記録する対象repository、commit、tree、PR番号はすべてこの時点のものである。write-onceの記録として変更しない。
- **公開版は履歴を切り出し直しているため、移行前のcommit・tree・PR番号は公開版では解決しない。**
- 公開日以降の投影・反映を記録する場合は、公開版を対象として書く。

## 7. 現在の状態（まとめ）

- 評価基盤は `evaluation_foundation_v4`。3 KPIをatomic run単位でappend-only保存し、計画上の`N`をrun identityへ含めません。実効互換なrunだけをpoolから選択し、使用run ID集合を固定して比較します。v3 prompt-set resultは履歴として保持します。
- baselineから多数の候補（C166まで、bundle 162件）を派生させ、主眼は「品質維持でのall-agentトークン削減」。
- 本体へ反映済みなのは **C41・C43・C71・C81・C125・C147**（この順に積み上げ投影、直近はC147）。C41〜C125は過去の投影履歴かつ巻き戻し先として保持。C125までは移行前のTHE-CAPTION、C147は公開版`the-caption`を対象とする。
- 採点条件は **v14が現行**（v13でA02の「要求と採点のずれ」を塞ぎ、v14でA01をterminal-state evidenceへ切り替えた版。指定の正本は[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)）。v13とv14は別のcompatibility conditionで、最初のv13互換resultは6条件・計420件です。
- **評価と採用は別レイヤー**。この基盤は数値を並べるだけで、優劣・採否は出しません。採否は人が判断します。

## 8. どこから読むとよいか

- 全体と経緯: ルート [`README.md`](../README.md)
- リポジトリ契約: [`docs/repository-contract.md`](repository-contract.md)
- 評価の手順: [`docs/prompt-comparison-workflow.md`](prompt-comparison-workflow.md) / [`docs/evaluation-loop-manual.md`](evaluation-loop-manual.md)
- 制御設計の原則: [`docs/prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 候補・release・baseline: `prompts/*/README.md`
- 採点条件: [`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)
