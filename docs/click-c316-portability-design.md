# Click C316水平適用の設計記録

## 結論

THE-CAPTIONでリリースしたC316（root `AGENTS.md`の「# 実行制御」6項目と、それを指すroot `CLAUDE.md`のリンク）を、改変せずにClickのrootへ置く。Click Standard14 r4で、Claude Code（Sonnet 5.5 low）を各ケース5回ずつ測り、保存済みの[制御なしの基準](../evaluations/targets/click/results/click-free-sonnet55-low-standard14-r4-n5_2026-10-14.md)と、同じ単価表で品質・費用・経過時間を比べる。

新しい制御を設計するのではなく、THE-CAPTIONで効果を確かめたC316が別の公開リポジトリでも成り立つかを確かめる試験である。

## Candidate作成前の確認

1. 比較の基準は、Click Standard14 r4の制御なし（`click-00e592c-control-free-r1`、result `b67fae7501c94c63a1d21b420aebc0ef`）とする。品質はA01の5件が0点、ほかの65件が4点、費用の中央値は`$0.4489`（`0.4188`〜`0.4854`）だった。
2. 閉じたい誤経路は、THE-CAPTIONと同じく、結果が依頼と正本から決まらないまま調査・変更・試験を始める経路（A01）と、念のための追加探索、変更後の確認の分割、短い待機の指定、出力やファイル本文の全量取得による費用の増加である。
3. C316の本文はTHE-CAPTIONでの評価のまま使い、Click向けに語句を足したり削ったりしない。Click固有の指示やrepository authorityも加えない。
4. 変更軸は、制御なしのroot `AGENTS.md`（空）をC316の本文へ置き換え、root `CLAUDE.md`を`AGENTS.md`へのリンクとして加えることだけである。THE-CAPTIONのC316と同じ2対象・同じ構造で、ほかの17対象はTHE-CAPTION固有の内容なので含めない。
5. 期待は、A01が確認して停止して4点になること、ほかの13ケースの品質を保つこと、費用が基準の幅より下がることである。期待どおりでなくても、追加のNやケースの変更で結果を引き上げない。

## 固定条件

- 評価セット：`click-standard14-r4` / `r4`
- プロンプト：`click-00e592c-receive-form-file-read-range-r1`
- モデル / 推論 / Agent：`claude-sonnet-5-5` / `low` / Claude Code `2.1.288`（計測の道具のセル`click-r4-sonnet`）
- 採点：`click-outcome-abstract-condition-preserving-claude-collector-v3`
- 単価表：`api-standard-2026-10-10-r2`
- 発行：基準と同じく、全セルで一つの待ち行列、合計24本まで、負荷を見て発行する

プロンプト以外の条件は基準と同じにし、比較は保存後に`compare`で行う。

## 非目標

- C316の個別項目への因果の帰属
- Clickのケース、TaskSpec、採点、実行環境、モデル、推論の変更
- 採用、リリース、`pallets/click`本体への反映
