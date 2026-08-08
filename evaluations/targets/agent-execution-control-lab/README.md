# agent-execution-control-lab PRレビュー測定インスタンス

現行Claude Code Actionのagentic retrievalと、決定論的に入力を準備するCandidate Aを固定fixtureで調べる、`agent-execution-control-lab`向けnamespacedインスタンスである。ターゲットrefは測定環境導入前のcommit `8cd97283e60f13393fb1302c601c9a4fe0a5381f`へ固定する。

現在のインスタンス状態は登録済み・機能仕様監査後のBaseline未qualificationである。既存`pr-review-finding-quality-v1`とPRR-C01 N=2は、PRレビュー機能仕様とBaseline admission gateより先に作成されたため、正式quality resultではなくdiagnostic evidenceとして保持する。正式resultは0件である。

## アーティファクト

- [`target.json`](target.json): target identity、layout、artifact root
- [`specifications/`](specifications/README.md): PRレビュー機能仕様とCore Baseline admission gate
- [`cases/`](cases/README.md): r1 diagnostic fixtureと、機能仕様から導出したPRR-C01/r2 development case
- [`sets/`](sets/README.md): 6ケースの未qualification set
- [`profiles/`](profiles/README.md): PRR-C01 baseline qualification profile
- [`rating-contracts/`](rating-contracts/README.md): model-visible review contractとmodel-invisible quality rating contract
- [`results/`](results/README.md): 保存済みrunとdiagnostic再分類receipt。正式resultは0件
- [`contracts/`](contracts/README.md): GitHub Actions診断経路の比較条件
- [`schemas/`](schemas/README.md): fixture、review出力、診断run resultのschema
- [`tools/`](tools/README.md): このインスタンス固有の入力生成、収集、採点補助

## 境界

- `cases/*/r1/input.json`だけをreviewerへ渡し、`oracle.json`はgrader jobだけが読む。
- `.github/workflows/pr-review-measure-core.yml`はGitHubの配置制約によりリポジトリ共通領域へ置くが、このインスタンスのアーティファクトとtoolsだけを参照する。
- workflowは手動起動のみでGitHub commentを投稿しない。
- PRレビュー機能仕様に適合するcase、rating contract、Baseline identityが未qualificationのため、Candidate A、残り5ケース、N=5、Integrationを発行しない。

## ローカル検証

```bash
.venv/bin/python evaluations/targets/agent-execution-control-lab/tools/pr_review_measurement.py validate-fixtures
.venv/bin/python -m pytest tests/test_pr_review_measurement.py -q
```

## Diagnostic Core Review

GitHub Actionsの`PR Review Measurement Core`は`case_id`、`variant`、`repetition`、`model`を受ける。

- `agentic-retrieval`: reviewerがfixture toolを使って入力を取得するCore Baseline診断prototype
- `deterministic-input`: Actions側で完成した`review-input.json`をreviewerが読むCandidate A

両variantとも同じfixture、review contract、出力schema、Claude Code Action revisionを使う。これは接続診断の実装であり、現行Claude workflowとの対応receiptと機能適合gateを満たしていない。新しい正式evaluation slotは発行しない。
