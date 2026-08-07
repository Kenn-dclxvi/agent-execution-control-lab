# layer2 instructions

`layer2/`の指示は、KPIに含めないrun単位の診断用拡張を扱う。ルートの`AGENTS.md`の共通規則に加えて、この領域規則を適用する。

- `layer2/extensions/<run_id>/<feature>/`をrun単位の診断アーティファクトとして扱う。
- root／worker別token、session、command、routing情報をKPIへ入力しない。
- 拡張をLayer 3のquality score変更へ使用しない。
- feature（機能）ごとにschemaとsource identityを固定する。
- 元のrunとのbindingが確認できない拡張を比較根拠にしない。
- 拡張の欠落を推定値で補完しない。
- 拡張の追加をevaluation foundationのLayerまたはKPI拡張として扱わない。
- privateな生データを公開する拡張へ無条件に保存しない。
