# Evaluations

プロンプト比較に使う評価アーティファクトとターゲットインスタンスを管理する入口である。現行のevaluation foundationはv4で、レイヤー・互換条件・不変の履歴の規則は[`AGENTS.md`](AGENTS.md)、レイヤーと世代の定義は[`docs/prompt-comparison-workflow.md`](../docs/prompt-comparison-workflow.md)、実行方法は[`docs/evaluation-loop-manual.md`](../docs/evaluation-loop-manual.md)を正本とする。

## アーティファクト配置

- [`targets/`](targets/README.md): 評価対象リポジトリごとのインスタンス台帳とディスクリプタ。新インスタンスは原則として`namespaced` layoutへ閉じる
- [`cases/`](cases/README.md): `the-caption` legacy-rootのケースアーティファクトと索引
- `sets/`: `the-caption` legacy-rootのEvaluation set revision
- [`profiles/`](profiles/README.md): `the-caption` legacy-rootのexecution profileと索引
- [`rating-contracts/`](rating-contracts/README.md): `the-caption` legacy-rootのquality rating contract revision
- [`results/`](results/README.md): `the-caption` legacy-rootのwrite-once evaluation resultと索引
- `examples/`: 現行のschemaとfixture境界の説明用アーティファクト

`the-caption`のlegacy-rootアーティファクトは既存のパスを維持する。`click`など`namespaced`インスタンスのアーティファクトは`targets/<target_id>/`配下に置き、インスタンス間でケース、プロファイル、rating contract、プロンプトバンドル、resultを混ぜない。

## 読み方

評価条件を確認するときはケース / セット / プロファイル / rating contract本体を、実測値と状態を確認するときはresult本体を参照する。READMEの要約やアーティファクトの存在だけを、評価済み、採用済み、release済み、本体反映済みの根拠にしない。

ローカル試行、identity不一致、measurement-incompleteなrunを正式resultへ昇格させない。評価基盤は3 KPIを記録するが、`winner`、プロンプト改善、採用、release、projectionの判断は行わない。
