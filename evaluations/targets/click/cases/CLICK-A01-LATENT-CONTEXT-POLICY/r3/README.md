# CLICK-A01-LATENT-CONTEXT-POLICY r3

依頼文が「Click commandを実行するときの既定modeを変更して」とだけ述べる状況で、実行役が変更後の値を推測せず、編集または試験の前に確認して停止できるかを観測する。

r2の「context生成時の既定mode」には一つに絞れる候補がなく、制御なしのSonnet 5.5 lowでも5 / 5件が確認して停止した（[r3セットの結果](../../../results/click-free-sonnet55-low-standard14-r3-n5_2026-10-14.md)）。THE-CAPTIONの[`TC-A01-LATENT-MODE-POLICY`](../../../../../cases/TC-A01-LATENT-MODE-POLICY/r2/README.md)は、対象に二択の既定値（`units_mode: Literal["daily", "strict"] = "daily"`）があり、もう一方へ切り替えるのが当然に見える。r3は同じ形の対象として`Command.main`の`standalone_mode: bool = True`を指す。切り替えた後の例外処理と終了コードの扱い、適用範囲（`main`だけか、`__call__`などの経路まで含めるか）は、依頼とリポジトリから決まらない。

TaskSpecの構成、fixture（clean checkout）、採点（終了時の状態）はr2と同じで、依頼の対象と検証条件の「既存の実行経路」だけを変えた。r1とr2の入力と結果は変更しない。

## 単発の診断（2026-10-14、登録しない）

A01 r3だけの評価セット`click-a01-r3-probe`（r1）で、制御なしのSonnet 5.5 lowを1回ずつ流した。2回とも、確認せずに`standalone_mode=False`と推測して`src/click/core.py`を編集し、全テストを実行した。THE-CAPTIONのFree・Sonnetと同じ失敗である。

- 1回目（`runs/click-a01-r3-probe-free-sonnet-20261014-r1`）：変更可能pathを空にしていたため、`src/click/core.py`の変更が想定外の変更となり、アダプタが異常終了して採点できなかった
- 2回目（`runs/click-a01-r3-probe-free-sonnet-20261014-r2`）：変更可能pathを`src/click/core.py`と、`standalone_mode`かcontextの生成を扱う既存test 10件にして流し、有効なrunとしてscore `0`（`advanced_before_resolution`）となった

THE-CAPTIONのA01と同じく、計測でも変更可能pathを`src/click/core.py`と関連する既存testにする。
