# claude-pr-review-core-r1

固定target refの`.github/workflows/claude-pr-review.yml`から、レビュー観点をCore Reviewへ移したBaseline候補である。

- [`source-prompt.md`](source-prompt.md): target commit `8cd97283e60f13393fb1302c601c9a4fe0a5381f`の現行workflow prompt
- [`core-prompt.md`](core-prompt.md): fixture toolと構造化出力へ接続するCore用prompt候補
- [`manifest.json`](manifest.json): source、Action、file hash、状態
- 入力対応: [`baseline-input-mapping-r1`](../../../contracts/baseline-input-mapping-r1.json)

現在状態は`admission_blocked`である。局所規則の選択・優先順位とrepository read範囲の意味同一性が未証明であり、workflow、profile、resultへbindしない。
