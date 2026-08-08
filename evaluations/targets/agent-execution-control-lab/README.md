# agent-execution-control-lab PRレビュー測定インスタンス

現行Claude Code Actionのagentic retrievalと、決定論的に入力を準備するCandidate Aを固定fixtureで調べる、`agent-execution-control-lab`向けnamespacedインスタンスである。ターゲットrefは測定環境導入前のcommit `8cd97283e60f13393fb1302c601c9a4fe0a5381f`へ固定する。

現在のインスタンス状態は登録済みであり、PRR-C01/r3のcase設計監査を終えている。Core Baseline repetition 1は最初の3回が`execution_failed`となった。Action用git workspaceとturn条件を修正した四回目では、review、構造化出力、採点が完了したがscore `0`で`quality_failed`となった。reviewerはrequired findingの内容を捉えたものの、model-visible規則にgrader必須のrule identityがなく、finding identityを一致させられなかった。これはBaseline性能へbindせず、fixtureと入力契約の不整合としてrepetition 2を停止している。既存`pr-review-finding-quality-v1`とPRR-C01 N=2は、PRレビュー機能仕様とBaseline admission gateより先に作成されたため、正式quality resultではなくdiagnostic evidenceとして保持する。

## アーティファクト

- [`target.json`](target.json): target identity、layout、artifact root
- [`specifications/`](specifications/README.md): PRレビュー機能仕様とCore Baseline admission gate
- [`cases/`](cases/README.md): r1 diagnostic fixture、PRR-C01/r2 development case、独立監査済みPRR-C01/r3 held-out fixture
- [`sets/`](sets/README.md): 6ケースの未qualification set
- [`profiles/`](profiles/README.md): 履歴profileと、fresh PRR-C01/r3 Core Baseline qualification profile
- [`prompts/`](prompts/README.md): 履歴prompt候補と、Anthropic `code-review` sourceへbindした新Core Baseline prompt候補
- [`rating-contracts/`](rating-contracts/README.md): model-visible review contractとmodel-invisible quality rating contract
- [`results/`](results/README.md): 保存済みrunとdiagnostic再分類receipt。正式resultは0件
- [`contracts/`](contracts/README.md): 入力対応、測定境界、case設計監査、snapshot、qualification preflight
- [`contracts/baseline-input-mapping-r4.json`](contracts/baseline-input-mapping-r4.json): 規則identity修正後の純正workflow対応監査。旧Coreは`unsatisfied`
- [`contracts/baseline-code-review-workflow-mapping-r1.json`](contracts/baseline-code-review-workflow-mapping-r1.json): 新Baseline promptのproducer構成対応。`satisfied_not_executed`
- [`contracts/baseline-measurement-boundary-r2.json`](contracts/baseline-measurement-boundary-r2.json): 固定`code-review` sourceのproducer構成と測定用変更の境界。`satisfied`
- [`schemas/`](schemas/README.md): fixture、review出力、診断run resultのschema
- [`tools/`](tools/README.md): このインスタンス固有の入力生成、収集、採点補助

## 境界

- profileへ固定したcase revisionの`input.json`だけをreviewerへ渡し、同revisionの`oracle.json`はgrader jobだけが読む。
- `.github/workflows/pr-review-measure-core.yml`はGitHubの配置制約によりリポジトリ共通領域へ置くが、このインスタンスのアーティファクトとtoolsだけを参照する。
- workflowは手動起動のみでGitHub commentを投稿しない。
- PRR-C01/r3のcase設計監査、入力対応、測定境界、四回目のfresh N=2 preflightは成立した。四回目で実行経路はterminalになったが、fixtureのmodel-visible rule identityがgraderと一致しないため個別pass条件は未成立である。repetition 2、Candidate A、残り5ケース、N=5、Integrationは発行しない。

## ローカル検証

```bash
.venv/bin/python evaluations/targets/agent-execution-control-lab/tools/pr_review_measurement.py validate-fixtures
.venv/bin/python -m pytest tests/test_pr_review_measurement.py -q
```

## Core Baseline qualification

GitHub Actionsの既存`PR Review Measurement Core`は、PRR-C01/r3で単一Actionの測定経路を確認した履歴workflowであり、Anthropic純正`code-review`のproducer構成を移植していない。純正相当Baselineの外部実行には使わない。

- reviewerは固定fixture toolからPR情報、規則、対象本文、読み取り専用snapshotを取得する。
- reviewer jobにはoracleと`.git`を渡さず、repository snapshotから書込権限を除く。
- GitHub comment、Candidate A、repetition 2はこの実行経路で開始しない。

旧workflowによる両variantのrunはdiagnostic evidenceとして履歴に残す。`pr-review-qualify-core-r1`は固定commitを取得できず、`pr-review-qualify-core-r2`は読取りコマンドの権限不足と結果回収用ファイル名の不一致により終了した。これらを修正した`pr-review-qualify-core-r3`ではreviewerが動作したが、12ターン以内に構造化結果を返せなかった。3件の一次resultは[`results/`](results/README.md)に保存している。

`pr-review-qualify-core-r4`は、downloadしたmodel-visible workspaceをAction用の最小git repositoryにし、target snapshotには`.git`を含めない。明示的な`--max-turns`は使用せず、Action stepを12分で停止する。profileとpreflightを新revisionとして固定し、過去三件の条件は変更しない。

新しい[`claude-code-review-core-r1`](prompts/baselines/claude-code-review-core-r1/README.md)は、Anthropicの固定`code-review`原文をsourceにし、haiku事前判定、authority path収集、sonnet要約、4並列reviewer、issue別validation、未確認issueの除外を保持する。現時点ではprompt-level mappingまでで、Action接続、PRR-C01/r4独立監査、profile、preflightは未完了である。
