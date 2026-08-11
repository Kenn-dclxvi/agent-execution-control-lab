# review terminal proof obligation direction r1

terminal別proof obligationの方向性だけを確認するdevelopment probe。LLM実行、quality rating、KPI比較、Candidate gateまたはheld-out evidenceではない。

- 公開入力: [`cases.json`](cases.json)
- model-invisible oracle: [`private/oracle.json`](private/oracle.json)
- 判定: [`../../../scripts/review_terminal_direction_probe.py`](../../../scripts/review_terminal_direction_probe.py)
- 設計: [`../../../docs/review-terminal-proof-obligation-minimal-direction-design.md`](../../../docs/review-terminal-proof-obligation-minimal-direction-design.md)

6条件の差分は事前固定する。probe結果に合わせて入力またはoracleを変更する場合は新しいrevisionとする。
