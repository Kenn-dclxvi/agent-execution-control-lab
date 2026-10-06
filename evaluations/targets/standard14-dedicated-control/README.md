# STD14専用評価素材

工程1の仕様に基づく全14件の専用素材。[旧新各84件の保存結果](../../../docs/standard14-dedicated-stage5-final-report-r1.md)を保持する。[工程7最終判定](../../../docs/standard14-dedicated-stage7-final-verdict-r1.md)では開始履歴の修正が必要と判断した。難しさの同等性と低コストな代替は未認定。

- [全14件](sets/dedicated14-r1.json)
- [専用コード](fixture/base/)
- [採点](rating-contracts/outcome-r1.json)
- [局所検証](registrations/local-qualification-r1.json)
- [旧criterionとの双方向対応](registrations/criterion-map-r1.json)
- [配送境界検査](registrations/delivery-audit-r1.json)
- [固定hash](registrations/source-freeze-r1.json)
- [環境](registrations/environment-r1.json)
- [コード量と保存量](registrations/storage-r1.json)
- [発行不可条件](registrations/admission-r1.json)
- [工程3への引き継ぎ](../../../docs/standard14-dedicated-stage2-r1.md)

局所検証は `runtime/qualification.py`、固定記録は `runtime/freeze.py`。どちらもモデル試験を発行しない。

- [開始状態の設計契約 第2版](registrations/stage7-start-state-contract-r2.json)
- [最終判定と証拠の索引](registrations/README.md)
- [履歴素材別版の実装方針](../../../docs/standard14-dedicated-stage8-material-revision-plan-r1.md)

現在の開発方針は[全体計画第2版](../../../docs/standard14-dedicated-evaluation-plan-r2.md)。利用者の最新指示により、`/Users/kenn/repos/standard14-evaluation-dev` は何も引き継がない空のリポジトリとして作成した。この場所のコード・計画・ルール・結果はコピーせず、そのまま保持する。
