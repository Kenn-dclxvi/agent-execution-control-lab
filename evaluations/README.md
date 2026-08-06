# Evaluations

prompt比較に使う評価artifactとtarget instanceを管理する入口である。現行のevaluation foundationはv4で、Layer・compatibility・immutable historyの規則は[`AGENTS.md`](AGENTS.md)、Layerと世代の定義は[`docs/prompt-comparison-workflow.md`](../docs/prompt-comparison-workflow.md)、実行方法は[`docs/evaluation-loop-manual.md`](../docs/evaluation-loop-manual.md)を正本とする。

## Artifact layout

- [`targets/`](targets/README.md): 評価対象repositoryごとのinstance台帳とdescriptor。新instanceは原則としてnamespaced layoutへ閉じる
- [`cases/`](cases/README.md): `the-caption` legacy-rootのcase artifactと索引
- `sets/`: `the-caption` legacy-rootのEvaluation set revision
- [`profiles/`](profiles/README.md): `the-caption` legacy-rootのexecution profileと索引
- [`rating-contracts/`](rating-contracts/README.md): `the-caption` legacy-rootのquality rating contract revision
- [`results/`](results/README.md): `the-caption` legacy-rootのwrite-once evaluation resultと索引
- `examples/`: 現行schemaとfixture境界の説明用artifact

`the-caption`のlegacy-root artifactは既存pathを維持する。`click`などnamespaced instanceのartifactは`targets/<target_id>/`配下に置き、instance間でcase、profile、rating contract、prompt bundle、resultを混ぜない。

## 読み方

評価条件を確認するときはcase / set / profile / rating contract本体を、実測値と状態を確認するときはresult本体を参照する。READMEの要約やartifactの存在だけを、評価済み、採用済み、release済み、本体反映済みの根拠にしない。

ローカル試行、identity不一致、measurement-incompleteなrunを正式resultへ昇格させない。評価基盤は3 KPIを記録するが、`winner`、prompt改善、採用、release、projectionの判断は行わない。
