# PRレビュー測定環境

現行Claude Code Actionと、決定論的に入力を準備するCandidate Aを、固定fixtureと同一review contractで比較するための測定環境。

現在状態は`implemented_unexecuted`である。fixture、schema、collector、grader、Core Review workflowは実装済みだが、Claudeを使うpilotおよびN=5比較は未実行・未評価である。

## 境界

- `evaluations/`のプロンプト比較resultとは別系列として扱う。
- `fixtures/*/input.json`はmodel-visibleである。
- `fixtures/*/oracle.json`はmodel-invisibleであり、reviewer jobへ渡さない。
- `.github/workflows/pr-review-measure-core.yml`は手動起動だけを許可し、GitHub commentを投稿しない。
- 正式resultはworkflow artifactから検証後に別変更で登録する。生のAction出力は登録しない。

## ローカル検証

```bash
.venv/bin/python scripts/pr_review_measurement.py validate-fixtures
.venv/bin/python -m pytest tests/test_pr_review_measurement.py -q
```

## Core Review実行

GitHub Actionsの`PR Review Measurement Core`を手動起動し、`case_id`、`variant`、`repetition`、`model`を指定する。`attempt`には一意なGitHub run IDを使用する。

- `agentic-retrieval`: reviewerがfixture toolを使って入力を取得するCore Baseline
- `deterministic-input`: Actions側で完成した`review-input.json`をreviewerが読むCandidate A

両variantとも同じfixture、review contract、出力schema、Claude Code Action revisionを使う。出力はartifactへ保存され、GitHub commentは作成しない。
