# リポジトリ概要（初見の人向け）

このドキュメントは、THE-CAPTION-PROMPTリポジトリを初めて見る人が、全体像・作成済みプロンプト・評価の仕組み・A02採点の論点を一通り把握できるようにまとめたものです。詳細な正本は各節末尾のリンク先を参照してください。

## 1. このリポジトリは何をする場所か

THE-CAPTION（別リポジトリの本体システム）に与える**プロンプト（AIへの指示書）を設計・比較・評価し、反映可能な形へまとめる**ための専用リポジトリです。

- **やること**: 現行プロンプトの固定、候補プロンプトの構築、同一条件での評価、評価済み候補のrelease化。
- **やらないこと（スコープ外）**: THE-CAPTION本体のruntime（実行時の挙動）そのものの変更。本体への反映・PR・マージ・有効化は、**明示的に依頼されたときだけの別作業**として扱います。

重要な区別として、このリポジトリは **「artifactが存在すること」と「評価済み・採用済み・本体反映済みであること」を混同しません**。評価はあくまで観測で、採用や本体適用は人が別途下す判断です。

## 2. 基本用語

- **プロンプト（prompt）/ bundle**: AIへ渡す指示書一式。`AGENTS.md`等のファイル群をまとめた単位を bundle と呼びます。
- **baseline**: 比較の起点となる、現行プロンプトの固定スナップショット。
- **candidate（候補）**: baselineから派生させた改良案。`C1`〜`C77`のように番号で呼びます。
- **release**: 評価を経て、本体へ反映可能な単位として固定した候補。
- **token（トークン）**: AIが入出力を処理する量の単位。多いほど時間と費用が増えます。
- **all-agent `total_tokens`**: 統括役のroot agentと、そこから起動された全ての下位セッション（SA session＝worker）の使用量を合算した値。workerが増えると合計は大きく膨らみます。
- **case（評価case）**: プロンプトの挙動を測るための、症状・対象・成功条件を定めたテスト課題。`TC-F01`〜`TC-A06`など。
- **model-visible / private（model-invisible）**: 実行役のAIに提示する情報（model-visible）と、採点用の正解・期待diff・必須コマンド等の隠す情報（private）を厳密に分けます。

## 3. ディレクトリ構成

| Path | 役割 |
| --- | --- |
| `prompts/baselines/` | 比較元プロンプト（現行の固定スナップショット）。2件（`current-r1` / `current-r2`）。 |
| `prompts/candidates/` | 構築中の候補プロンプト。設計上はC77まで、bundleとして22件を保存。 |
| `prompts/routes/` | 共通の全文へ実行前に合成する小さな差分（route）。 |
| `prompts/releases/` | 本体へ反映可能な単位に固定したrelease。4件。 |
| `evaluations/cases/` | 評価case（20件）とmodel-visible / private境界。 |
| `evaluations/sets/` | caseを束ねた評価集合（例: `the-caption-standard14-r1`）。 |
| `evaluations/fixtures/` | caseが使う擬似リポジトリ状態。 |
| `evaluations/profiles/` | model・環境・反復条件・比較条件を固定したprofile。 |
| `evaluations/rating-contracts/` | 採点条件（rating contract）をrevision別に保存。14 revision。 |
| `evaluations/results/` | 公開済みの評価結果（append-only）。約105件の記録。 |
| `layer2/` | token内訳やsession情報など、KPIへ入れない補助データの保存先。 |
| `docs/` | リポジトリ契約、設計判断、反映手順。 |
| `scripts/` | 評価ループや証拠収集のスクリプト。 |

正本: [`docs/repository-contract.md`](repository-contract.md)、ルートの[`README.md`](../README.md)。

## 4. 評価の仕組み（evaluation foundation v3）

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

### candidate（C1〜C77、bundle 75件保存）

baselineから枝分かれした改良案です。番号順が単純な親子ではなく、いくつかの系譜に分かれています（例: compact構造を保つC1系、完了志向を保つC5系）。開発の主眼は一貫して「**品質を保ったままall-agentトークンを減らす制御**」の探索でした。トークンを大きく減らせた制御の分類と教訓は、[`docs/control-mechanisms.md`](control-mechanisms.md)にまとめています。

bundle 75件はすべてcandidate index（[`prompts/candidates/README.md`](../prompts/candidates/README.md)）の表に掲載しています。正本は責務ごとに分かれます。identityは各`manifest.json`（構築時provenanceとしてimmutable）、評価状態は独立したevaluation / diagnostic result、系譜と観測の整理は[`docs/candidate-history.md`](candidate-history.md)です。indexはこれらへの一覧と導線です。

掲載candidateには互換比較できないものが含まれます。C45〜C48はA06の広域監査を`N=1`で観測した`diagnostic_only / memory_off`の枝で、いずれも診断resultを`evaluations/results/`へ保存していますが、blind quality ratingを実施していないため`quality_score`は保存せず、状態は`draft`です。標準14項目やB18と互換な品質比較ではありません。C72/C73は対象4項目各`N=5`で`targeted_evaluated`ですが、いずれも`stopped`です。indexへの掲載は、評価済み・採用済みを意味しません。

### release（4件）と本体反映状況

正本`prompts/releases/README.md`はrelease status / approval / runtime projectionを別軸で保持する。ここでも同じ3軸に分けて示す。

| release（由来候補） | release status | approval | runtime projection | 本体反映 |
| --- | --- | --- | --- | --- |
| Candidate34 | `cancelled` | `cancelled` | `not_authorized` | なし（不採用・artifact削除ではない） |
| Candidate41 | `projected` | `approved` | `projected` | **反映済み**（THE-CAPTION [PR #334](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/334)、実変更8 path）。直前の投影履歴・C43の巻き戻し先として維持 |
| **Candidate43** | `projected` | `approved` | `projected` | **反映済み**（THE-CAPTION [PR #335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335)、直前投影からroot `AGENTS.md`一つ） |
| **Candidate71** | `projected` | `approved` | `projected` | **反映済み・承認済み**（THE-CAPTION [PR #340](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/340)、直前投影からroot `AGENTS.md`一つ） |

現在の本体投影は、Candidate41 → Candidate43 → Candidate71の順に積み上げたreleaseで、直近の投影は`VALIDATION_CLOSURE`一labelを足した **C71** です。C41・C43は過去の投影履歴かつ巻き戻し先として保持しており、`cancelled`にはしていません。C71は後述のとおり評価上は品質gateを通過していませんが、**トークン効率を優先する別の採用判断**として2026-07-23に本体適用されました。ここが「評価（stopped）と採用（本体適用）は別レイヤー」という原則の実例です。

正本: [`prompts/candidates/README.md`](../prompts/candidates/README.md)、[`prompts/releases/README.md`](../prompts/releases/README.md)、[`prompts/baselines/README.md`](../prompts/baselines/README.md)。

## 6. 評価caseとA02の採点

### 標準14項目セット

主要な評価集合 `the-caption-standard14-r1` は、機能系のF01〜F10（12件）に、曖昧性境界のA01・A02を加えた14 caseです。各caseを`N=5`（5回）など複数反復して測ります。

### A02はどんなcaseか

**TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING** は、「一見あいまいだが実はリポジトリ規則で一意に決まる正規の起動先を、**質問せずに正しく解決して実装できるか**」を測るcaseです。

- **提示する（model-visible）**: 症状・対象ファイル・成功条件の要点だけ。
- **隠す（private）**: 正規の起動先、期待するdiff、**必須試験の具体コマンド**。

この「提示する情報」と「隠す情報」の分離が、次のA02採点論点の核心です。

### A02採点で起きた「要求と採点のずれ」

C71のB18評価（18反復）で、A02に3件の低得点（score 3）が付き、当初は品質低下と解釈されました。しかし一次資料を確認すると:

- 実行役へ**提示された成果条件**は「**最終diffからrouting成立を確認する**」という抽象的な表現だけでした。
- 一方、採点側（private）には `git diff --check` という**特定コマンド**が置かれていました。
- 採点器はこの抽象条件を「`git diff --check` の実行必須」と読み替え、未実行を欠落として減点しました。
- ところが `git diff --check` は末尾空白や競合markerのlintであって、A02の主眼（routing成立の確認）とは別物です。

つまりこの3件は、**提示していない特定コマンドを採点側が必須化した「要求と採点のずれ」**であり、本物の品質低下とは言えません。提示条件に照らした実質的な低下は、A01の「未固定modeを確認せず実装・試験へ進んだ」1件にとどまります。

### 採点条件（rating contract）の進化

採点条件はrevision別に固定され、in-placeで書き換えません（結果を見た後の基準変更は必ず新revision）。A02の論点に関係する流れは次のとおりです。

| revision | 主眼 |
| --- | --- |
| v10 | 実行役に提示した成果境界だけを必須にする |
| v11 | F10数値lineの意味等価と位置診断を分離 |
| v12 | command evidenceのquote直列化を正規化 |
| **v13（現行）** | **提示した抽象成果条件を特定コマンドへ具体化して必須化することを禁止し、コマンド名までmodel-visibleに明示された必須試験だけを品質へ反映する** |

上記のA02のずれを塞いだのが第13版 [`outcome-abstract-condition-preserving-owner-diagnostic-v13`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json) です。既存のv12契約とB18結果はそのまま履歴として保持します。

正本: [`evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/`](../evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/)、[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)。

## 7. 現在の状態（まとめ）

- 評価基盤は `evaluation_foundation_v3`。3 KPIをappend-onlyで保存し、互換条件を満たす結果だけを比較します。
- baselineから多数の候補（C77まで）を派生させ、主眼は「品質維持でのall-agentトークン削減」。
- 本体へ反映済みなのは **C41・C43・C71**（この順に積み上げ投影、直近はC71）。C41・C43は過去の投影履歴として保持。C71は評価上`stopped`のまま、トークン効率優先の採用判断で適用済み。
- 採点条件は **v13が現行**。A02の「要求と採点のずれ」を塞いだ版です。
- **評価と採用は別レイヤー**。この基盤は数値を並べるだけで、優劣・採否は出しません。採否は人が判断します。

## 8. どこから読むとよいか

- 全体と経緯: ルート [`README.md`](../README.md)
- リポジトリ契約: [`docs/repository-contract.md`](repository-contract.md)
- 評価の手順: [`docs/prompt-comparison-workflow.md`](prompt-comparison-workflow.md) / [`docs/evaluation-loop-manual.md`](evaluation-loop-manual.md)
- 制御設計の原則: [`docs/prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 候補・release・baseline: `prompts/*/README.md`
- 採点条件: [`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)
