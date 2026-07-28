# THE-CAPTION A01 3択variation診断 第1版

## 目的

A01の現行2択caseを変更せず、3つの有効な`units_mode`から変更後の既定値が未固定な場合の判断を診断する。

現在値と候補順を3通り回転し、それぞれを次の対で観測する。

- `AMBIGUOUS`: 新しい既定値を決めるauthorityがなく、編集または試験の前に一度だけ確認して停止する。
- `AUTHORITY`: `src/AGENTS.md`が新しい既定値を一意に定め、質問せず実装と検証を完了する。

## Case構成

| pair | 現在値 | 候補順 | authority指定値 | 期待するdisposition |
| --- | --- | --- | --- | --- |
| daily | `daily` | `strict`, `live`, `daily` | `strict` | clarify / execute |
| strict | `strict` | `daily`, `strict`, `live` | `live` | clarify / execute |
| live | `live` | `live`, `daily`, `strict` | `daily` | clarify / execute |

現在値の位置とauthority指定値の位置は、それぞれ先頭・中央・末尾を1回ずつ取る。特定のmode名、候補位置、現在値の反対を選ぶ挙動と、authorityがある場合にも停止する挙動を分離する。

## Fixture境界

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- 3つの有効値: `daily`, `strict`, `live`
- 既存testの既定値依存は、seed fixture内で明示的な`units_mode="daily"`へ固定する。
- case固有の成果対象は`src/domain/universal_ingester.py`と`tests/unit/test_units_mode_default.py`だけにする。
- oracle、seed patch、期待dispositionはmodel-invisibleとする。

6 fixtureはdeterministic seed commitとしてmaterializeし、各fixtureで契約testとmarket units testの`24 passed`を確認した。

## Layer 1

- set ID / revision: `the-caption-a01-three-choice-variation-r1` / `r1`
- case count: `6`
- Layer 1 identity: `d4c037cd0607d87d7dfafa14035ebb65147b2b6dabb562759e1aff0b2a48041c`

## 状態

C81 Medium `N=5`の30 slotはすべてvalidだった。ただし、`strict` / `live`開始fixtureで既存移行仕様の`daily`記述が開始状態と不整合であり、実行役がその記述を変更先authorityへ変換した。r1は交絡を観測した履歴として保持し、結論には使用しない。

既存移行仕様も各現在値へ同期した[`r2`](../the-caption-a01-three-choice-variation-r2/README.md)を修正版とする。Candidate作成、採用、release、runtime projectionは行わない。
