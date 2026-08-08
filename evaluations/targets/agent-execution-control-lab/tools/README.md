# target固有ツール

- `pr_review_fixture_tool.py`: model-visible fixtureのread-only取得
- `pr_review_measurement.py`: fixture検証、入力準備、許可field収集、診断採点

両ツールは`agent-execution-control-lab`固有のcase IDとruleを解釈するため、ターゲット非依存kernelの`scripts/`へ置かない。
