# Candidate159 / Free 変更開始一文 Rating v14 Medium F02 N=5比較

## 結論

Candidate159は、Freeの0-byte root `AGENTS.md`へ次の一文だけを追加した。

> 変更前に、必要な成果、変更箇所、直し方、維持する動作を一つの方針にまとめ、どれか決まらない間は変更しない。

F02 N=5は両条件とも5 / 5件がscore `4`で、部分変更と無変更停止はなかった。最初のcommand前に具体的な成果、変更対象・方法、維持する動作を同時に示した実行はFreeの`0 / 5件`からCandidate159の`4 / 5件`へ増えた。この一文が、変更方針を早い段階で明示する選択へ影響したと判定する。

一方、最初のfile changeまでには両条件とも`5 / 5件`が方針を形成していた。tokenとelapsedも増えたため、変更の完全性またはcost改善の証拠にはしない。

## 比較条件

| 項目 | Free | Candidate159 |
| --- | --- | --- |
| root prompt | 0 byte | 1文 |
| case | F02 r1 | 同左 |
| N | 5 | 5 |
| Rating | v14 | 同左 |
| model / reasoning | `gpt-5.6-sol / medium` | 同左 |
| runtime / CLI | Python 3.14.5 / Codex CLI 0.146.0 | 同左 |
| permission | `workspace-write / never` | 同左 |
| token accounting | all-agent v1 | 同左 |
| `max_workers` | 24 | 24 |

prompt identity以外の実効条件は実行前preflightで一致した。Candidate159の不足5 runだけを新規発行し、Freeの保存済みF02 5件は再実行していない。

## 結果

| 指標 | Free | Candidate159 | 差 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 0 |
| 最初のcommand前の具体的方針 | 0 / 5 | 4 / 5 | +4件 |
| 最初のfile change前の方針 | 5 / 5 | 5 / 5 | 0 |
| all-agent total token中央値 | 315,507 | 327,309 | `+3.74%` |
| elapsed中央値 | 91.418秒 | 104.688秒 | `+14.51%` |

## 状態境界

- 評価: `targeted_f02_n5_completed`
- 品質gate: `passed`
- 行動条件: `passed`。最初のcommand前の具体的方針`0 / 5 → 4 / 5`
- cost低下: `not_observed`
- 掲載判断: `included_in_supplementary_article`
- Standard14: `not_started`
- 採用: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

Layer 4 result IDは`c24bd641e44c4a89bce9fc7c4a08b393`、execution archive SHA-256は`3d3e056ad495758bf34e6b9682d08e3a6f58967476f9eb82a6b0a39337eb1b66`、final archive SHA-256は`84d06d37539f40cb5ec220d3081c028d1f5acedc39f340c8966c41854b7afd39`である。

