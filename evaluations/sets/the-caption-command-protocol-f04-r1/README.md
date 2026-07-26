# THE-CAPTION command protocol F04診断 第1版

## 結論

Candidate71を変更せず、現行command evidence protocol v1とroot ordered wrapperを明示するv2をF04 r2で各10回確認する。

protocol revisionはcomparison conditionであるため、両resultを互換Layer 4 comparisonへ混ぜない。closure率と3 KPIの記述差をprotocol診断として扱う。

## 構成

| 評価項目 | 版 | 観測対象 |
| --- | --- | --- |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | `r2` | 3 required commandの1-step closure、個別exit、fail-stop |

## 固定条件

- promptは両条件ともCandidate71へ固定する。
- modelは`gpt-5.6-sol`、reasoning effortは`medium`とする。
- target commit / tree、case revision、model-visible TaskSpec、permission、rating v13、fixture、token accountingは同一にする。
- 各条件はF04を10回、実効`M=10`で実行する。
- v1は既存の個別command証跡指示を維持する。
- v2はroot producerへ、一つのcustom exec wrapper内から列挙順の個別`tools.exec_command`を発行し、nonzeroまたはunavailableで後続を止め、完了済み全resultを一度だけmodelへ返すよう明示する。
- v2でもshell compound commandを許可しない。

## 判定範囲

両条件とも10 / 10 valid・rateable・score `4`、required command欠落0、protocol違反0、zero driftを必要条件とする。

v2の1-step closure率がv1より高くならない場合は、model-visible protocolだけではexecutor primitiveを代替できないと判定する。品質、token、elapsedは必ず記録するが、compatibility keyが異なるため公式Layer 4差にはしない。

この診断はprompt candidateの評価、標準14項目完了、採用、release、runtime projectionを判断しない。

## 実行結果

[v1 / v2各N=10結果](../../results/candidate71-command-protocol-v1-v2-v13-medium-f04-n10_2026-07-26.md)を別compatibility keyのappend-only resultとして登録した。v2は1-step closureを`5 / 10 -> 10 / 10`へ増やしたが、token合計`+6.63%`、elapsed合計`+2.69%`だったため`behavior_gate_passed / efficiency_gate_not_passed`である。
