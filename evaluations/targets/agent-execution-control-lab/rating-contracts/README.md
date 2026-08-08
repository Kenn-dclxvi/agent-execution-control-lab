# agent-execution-control-lab PRレビューrating contract索引

- [`pr-review-finding-quality-v1`](pr-review-finding-quality-v1.json): r1 diagnostic runで使用した履歴contract
- [`pr-review-finding-quality-v2`](pr-review-finding-quality-v2.json): 機能仕様r1から導出したPRR-C01/r2用のcontract候補。独立qualification未実施
- [`pr-review-finding-quality-v3`](pr-review-finding-quality-v3.json): 新しいheld-out候補PRR-C01/r3用のcontract候補。[独立case設計監査](../contracts/prr-c01-r3-case-design-audit-r1.json)済み・未実行・Baseline未qualification
- [r1 diagnostic review contract](review-contract-r1.md): r1 runでClaudeへ提示したfinding構造
- [r2 review contract](review-contract-r2.md): `related_paths`を含む機能仕様r1準拠のmodel-visible契約

review contractはmodel-visible、quality rating contractとoracleはmodel-invisibleである。2026-08-08のr1 runを新contractで事後採点しない。v2はcase設計監査を通過するまでprofileへbindしない。v3の独立監査はcase設計だけを満たし、Baseline qualification、実行許可、quality claimを意味しない。
