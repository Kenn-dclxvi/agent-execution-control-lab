# agent-execution-control-lab PRレビュー測定インスタンス

現行Claude Code Actionのagentic retrievalと、決定論的に入力を準備するCandidate Aを固定fixtureで調べる、`agent-execution-control-lab`向けnamespacedインスタンスである。ターゲットrefは測定環境導入前のcommit `8cd97283e60f13393fb1302c601c9a4fe0a5381f`へ固定する。

現在のインスタンス状態は登録済みであり、PRR-C01/r3のcase設計監査を終えている。Core Baseline repetition 1は3回とも`execution_failed`となった。三回目ではreviewerが入力を取得できたが、Action用git workspaceがなく、12ターンの明示上限にも達した。純正相当のレビュー条件と測定用の変更を分け直し、この二点を修正した四回目のprofileとpreflightを固定した。品質は観測できておらず、repetition 2は開始していない。既存`pr-review-finding-quality-v1`とPRR-C01 N=2は、PRレビュー機能仕様とBaseline admission gateより先に作成されたため、正式quality resultではなくdiagnostic evidenceとして保持する。正式な品質resultは0件である。

## アーティファクト

- [`target.json`](target.json): target identity、layout、artifact root
- [`specifications/`](specifications/README.md): PRレビュー機能仕様とCore Baseline admission gate
- [`cases/`](cases/README.md): r1 diagnostic fixture、PRR-C01/r2 development case、独立監査済みPRR-C01/r3 held-out fixture
- [`sets/`](sets/README.md): 6ケースの未qualification set
- [`profiles/`](profiles/README.md): 履歴profileと、fresh PRR-C01/r3 Core Baseline qualification profile
- [`prompts/`](prompts/README.md): 現行workflow source promptとCore Baseline prompt候補
- [`rating-contracts/`](rating-contracts/README.md): model-visible review contractとmodel-invisible quality rating contract
- [`results/`](results/README.md): 保存済みrunとdiagnostic再分類receipt。正式resultは0件
- [`contracts/`](contracts/README.md): 入力対応、測定境界、case設計監査、snapshot、qualification preflight
- [`contracts/baseline-input-mapping-r3.json`](contracts/baseline-input-mapping-r3.json): 現行workflowとCore入力の対応。`satisfied`
- [`contracts/baseline-measurement-boundary-r1.json`](contracts/baseline-measurement-boundary-r1.json): Claude Code純正相当のレビュー条件と測定用の変更との境界。`satisfied`
- [`schemas/`](schemas/README.md): fixture、review出力、診断run resultのschema
- [`tools/`](tools/README.md): このインスタンス固有の入力生成、収集、採点補助

## 境界

- profileへ固定したcase revisionの`input.json`だけをreviewerへ渡し、同revisionの`oracle.json`はgrader jobだけが読む。
- `.github/workflows/pr-review-measure-core.yml`はGitHubの配置制約によりリポジトリ共通領域へ置くが、このインスタンスのアーティファクトとtoolsだけを参照する。
- workflowは手動起動のみでGitHub commentを投稿しない。
- PRR-C01/r3のcase設計監査、入力対応、測定境界、四回目のfresh N=2 preflightは成立した。三回の失敗結果は測定環境を診断する証拠として保持する。四回目のrepetition 1が個別pass条件を満たすまで、repetition 2、Candidate A、残り5ケース、N=5、Integrationは発行しない。

## ローカル検証

```bash
.venv/bin/python evaluations/targets/agent-execution-control-lab/tools/pr_review_measurement.py validate-fixtures
.venv/bin/python -m pytest tests/test_pr_review_measurement.py -q
```

## Core Baseline qualification

GitHub Actionsの`PR Review Measurement Core`は、PRR-C01/r3を使って測定可能にしたClaude Code純正相当workflowを確認する。入力欄は過去のworkflowとの互換性のために残し、prepare jobがcase、variant、model、profile、repetitionを固定値へ照合する。

- reviewerは固定fixture toolからPR情報、規則、対象本文、読み取り専用snapshotを取得する。
- reviewer jobにはoracleと`.git`を渡さず、repository snapshotから書込権限を除く。
- GitHub comment、Candidate A、repetition 2はこの実行経路で開始しない。

旧workflowによる両variantのrunはdiagnostic evidenceとして履歴に残す。`pr-review-qualify-core-r1`は固定commitを取得できず、`pr-review-qualify-core-r2`は読取りコマンドの権限不足と結果回収用ファイル名の不一致により終了した。これらを修正した`pr-review-qualify-core-r3`ではreviewerが動作したが、12ターン以内に構造化結果を返せなかった。3件の一次resultは[`results/`](results/README.md)に保存している。

`pr-review-qualify-core-r4`は、downloadしたmodel-visible workspaceをAction用の最小git repositoryにし、target snapshotには`.git`を含めない。明示的な`--max-turns`は使用せず、Action stepを12分で停止する。profileとpreflightを新revisionとして固定し、過去三件の条件は変更しない。
