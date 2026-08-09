# PRレビュー held-out 3ケース r1

- set identity: `pr-review-held-out-three-r1 / r1`
- target repository ref: `16f9637d33791abd839d5c7d57b6616e03930949`、tree `c6d21c0bba62f5065c9e685f021a90ae2f004290`
- case membership: `PRR-C02/r2`、`PRR-C03/r2`、`PRR-C06/r2`
- coverage: ターゲット間の混在、保存済みresultの上書き、clean control
- 状態: 固定済み・[独立case設計監査](../../contracts/pr-review-held-out-three-case-design-audit-r1.json)済み・未実行
- 使用禁止: Control-Free品質確認用のprofileとpreflightが成立するまで資格確認スロットを発行せず、その品質確認が全件で成立するまで比較スロットを発行しない

3ケースは同じschema、review contract、target repository refへ固定する。control-free条件で全件quality score `4`を確認できた場合だけ、Claude Code純正相当CoreとOpus関係レビュー役の比較へ進める。比較結果からcase、oracle、rating contractを変更しない。
