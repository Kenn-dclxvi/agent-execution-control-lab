# 専用展開・採点・局所検証

- `fixture.py`: baseと一件のseedを独立Gitへ展開し、JSON TaskSpecの配送バイトを返す。
- `inspect_artifact.py`: 最終treeから実検査の証拠を作り、独立した応答・test差分判定の証拠と結ぶ。
- `grader.py`: 操作、最終tree、criterion、コマンド終了から0〜4点を判定する。
- `qualification.py`、`supplemental_checks.py`: 設計側の正常・誤成果を検査する。
- `freeze.py`: hash、環境、対応、配送境界、未確認条件を保存する。

これらはモデル試験を発行しない。保存応答の意味判定は、実行役の自己申告を使わず、証拠hashと独立判定者のcriterion評価を `assess` へ渡す。実行器・収集器の実運用への接続確認が済むまでは、admissionのready=falseを維持する。
