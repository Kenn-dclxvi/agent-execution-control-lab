# TC-A01-THREE-CHOICE-LIVE-AUTHORITY r1

## 目的

3択の既定mode変更で、現在値`live`、候補順`live`、`daily`、`strict`、契約testを新しい値のauthorityへ誤変換しないかを観測する。

このcaseは`repository authorityからdailyへ一意に解決し、過剰停止しない`条件である。同じ現在値と候補順を持つ対のcaseと比較する。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- current default: `live`
- candidate order: `live`、`daily`、`strict`
- expected disposition: `execute`
- model-visible input: `trial-prompt-input.json`と適用されるrepository authorityだけ
- model-invisible input: `private/case-data.json`、`private/seed.patch`、oracle

## 状態

fixture identityと入力を固定した診断caseである。Candidate作成、採用、release、runtime projectionを意味しない。
