# PRレビュー C02開発用固定ベンチマーク r1

- set identity: `pr-review-c02-development-benchmark-r1 / r1`
- target repository ref: `16f9637d33791abd839d5c7d57b6616e03930949`、tree `c6d21c0bba62f5065c9e685f021a90ae2f004290`
- case membership: `PRR-C02/r2`
- coverage: ターゲットインスタンス間のアーティファクト混在と、複数changed pathから成るfinding identity
- 状態: C02 Opus result確認後の開発用固定ベンチマーク

case、oracle、fixture、rating contractは変更せず、保存済み基準resultとの比較に再利用する。結果確認済みのケースなので、同じrevisionの新しい実行をheld-out evidenceとして扱わない。この1ケースだけから一般化、model ranking、採用、release、本体反映を判断しない。
