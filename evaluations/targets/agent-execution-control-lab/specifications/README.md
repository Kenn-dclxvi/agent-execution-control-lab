# PRレビュー仕様索引

このディレクトリは、PRレビュー測定でcase、oracle、rating contract、Baselineを作る前提となる機能仕様と実行経路仕様を保持する。

- [`pr-review-function-r1.md`](pr-review-function-r1.md): PRレビュー機能のmodel-visibleな成果条件とfinding同一性
- [`core-baseline-r1.md`](core-baseline-r1.md): 現行Claude workflowとCore Review経路の入力対応、実行互換監査、Baseline admission gate
- [`workflow-free-r1.md`](workflow-free-r1.md): Core Baselineに対するFreeの境界、品質と測定成立の分離、review体制とmodel選択への校正順序
- [`relationship-reviewer-model-calibration-r1.md`](relationship-reviewer-model-calibration-r1.md): 関係レビュー役を1人に固定し、その役のSonnet／Opusだけを変える校正条件
- [`control-free-four-qualification-r1.md`](control-free-four-qualification-r1.md): 現行仕様へ適合した既存4ケースを使うcontrol-free baseline資格確認条件

仕様revisionが変わる場合は既存revisionを上書きせず、新しいrevisionを追加する。既存case、oracle、rating contract、profile、resultを新仕様へ遡及適合させない。
