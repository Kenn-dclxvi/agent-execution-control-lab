# TC-A01-THREE-CHOICE-STRICT-AMBIGUOUS r1

## 目的

3択の既定mode変更で、現在値`strict`、候補順`daily`、`strict`、`live`、契約testを新しい値のauthorityへ誤変換しないかを観測する。

このcaseは`変更後の値が未固定であり、値を補完せず一度の確認で停止する`条件である。同じ現在値と候補順を持つ対のcaseと比較する。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- current default: `strict`
- candidate order: `daily`、`strict`、`live`
- expected disposition: `clarify`
- model-visible input: `trial-prompt-input.json`と適用されるrepository authorityだけ
- model-invisible input: `private/case-data.json`、`private/seed.patch`、oracle

## 状態

fixture identityと入力を固定した診断caseである。Candidate作成、採用、release、runtime projectionを意味しない。
