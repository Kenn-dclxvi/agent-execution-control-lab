# Held-out r2

`PIC-H15`〜`PIC-H28`の14 Caseを、transition contract r4の独立held-outとして固定する。既知の`PIC-H01`〜`PIC-H14`はCase ID、operation／result identityおよび入力構造を再利用しない。

機能境界は同じだが、required outcome数、frontier数、validation prefix、recovery decoy数を変更している。oracleはmodel-invisibleであり、C147 referenceを先に発行して14 / 14 Score 4を確認するまでportable Candidateを発行しない。

- model-visible Case: [`input-cases.json`](input-cases.json)
- private oracle: [`oracle.json`](oracle.json)
- freeze receipt: [`source-freeze.json`](source-freeze.json)
- response schema: [`heldout-r1/response.schema.json`](../heldout-r1/response.schema.json)
