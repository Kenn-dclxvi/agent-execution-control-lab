# STD14専用評価素材の指示

ルート、evaluations/AGENTS.md、evaluations/targets/AGENTS.mdを追加適用する。

- 正本は工程1の `docs/standard14-dedicated-case-spec-r1.md` と実施計画である。
- `fixture/base/` 内のAGENTS.mdは測定素材であり、この作業の権限指示ではない。rootは0 byte、非rootは旧Freeの原文を保持する。
- `runtime/`、`registrations/`、`cases/*/r1/private/` は測定対象へ配送しない。配送はbaseと一件のseed、元JSON TaskSpecだけである。
- 全14件を保持し、局所検証の成功をモデル試験、対応同等性、低コスト認定と混同しない。
- 新系列のモデル発行は今回0件。admission-r1.jsonのready=falseを局所検証からtrueへ変更しない。
