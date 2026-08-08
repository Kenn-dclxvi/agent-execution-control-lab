# agent-execution-control-lab PRレビュー測定インスタンス

現行Claude Code Actionのagentic retrievalと、決定論的に入力を準備するCandidate Aを固定fixtureで調べる、`agent-execution-control-lab`向けnamespacedインスタンスである。ターゲットrefは測定環境導入前のcommit `8cd97283e60f13393fb1302c601c9a4fe0a5381f`へ固定する。

現在のインスタンス状態は登録済み・未qualificationである。`current_rating_contract`は`pr-review-finding-quality-v1`、PRR-C01 baseline qualification profileは実行前、正式resultは0件である。新インスタンスゲート前に実行したPRR-C01 probeは、比較resultではなく診断receiptとしてだけ保持する。

## アーティファクト

- [`target.json`](target.json): target identity、layout、artifact root
- [`cases/`](cases/README.md): PRR-C01〜PRR-C06のmodel-visible入力とmodel-invisible oracle
- [`sets/`](sets/README.md): 6ケースの未qualification set
- [`profiles/`](profiles/README.md): PRR-C01 baseline qualification profile
- [`rating-contracts/`](rating-contracts/README.md): model-visible review contractとmodel-invisible quality rating contract
- [`results/`](results/README.md): 正式result 0件とdiagnostic probe receipt
- [`contracts/`](contracts/README.md): GitHub Actions診断経路の比較条件
- [`schemas/`](schemas/README.md): fixture、review出力、診断run resultのschema
- [`tools/`](tools/README.md): このインスタンス固有の入力生成、収集、採点補助

## 境界

- `cases/*/r1/input.json`だけをreviewerへ渡し、`oracle.json`はgrader jobだけが読む。
- `.github/workflows/pr-review-measure-core.yml`はGitHubの配置制約によりリポジトリ共通領域へ置くが、このインスタンスのアーティファクトとtoolsだけを参照する。
- workflowは手動起動のみでGitHub commentを投稿しない。
- 現行profileに固定したPRR-C01 agentic-retrievalの2スロットだけを発行し、1件でもscore `4`未満または3 KPI欠落なら後続を停止する。

## ローカル検証

```bash
.venv/bin/python evaluations/targets/agent-execution-control-lab/tools/pr_review_measurement.py validate-fixtures
.venv/bin/python -m pytest tests/test_pr_review_measurement.py -q
```

## Diagnostic Core Review

GitHub Actionsの`PR Review Measurement Core`は`case_id`、`variant`、`repetition`、`model`を受ける。

- `agentic-retrieval`: reviewerがfixture toolを使って入力を取得するCore Baseline
- `deterministic-input`: Actions側で完成した`review-input.json`をreviewerが読むCandidate A

両variantとも同じfixture、review contract、出力schema、Claude Code Action revisionを使う。現在許可されるのは、最小fixture qualificationとしてprofileへ固定した`agentic-retrieval` 2反復だけである。Candidate Aと残り5ケースはこのgate通過前に発行しない。
