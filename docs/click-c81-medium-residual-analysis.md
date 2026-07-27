# Click C81 Medium残余経路分析

## 結論

F01のtoken中央値`+16.80%`は、反復内で安定した悪化ではない。iterationを対応させるとC81は5回中3回でtokenが減り、paired差の中央値は`-970 token`だった。独立中央値の組合せだけを根拠にF01向け制御を追加しない。

F04のelapsed増加は再現性がある。Mediumでは5回中4回で増え、paired差の中央値は`+6.809`秒、5回合計は`+16.24%`だった。Highでも5回合計`+17.94%`で同方向だった。C81全文はF04でedit前のgit history探索をHigh `3 / 5`、Medium `1 / 5`、合計`4 / 10`件発生させた。Control-freeはHigh / Medium合計`0 / 10`件だった。

この経路はrequired validation後の追加readではなく、変更方法を決める前の`git log` / `git show` / `git blame`である。C81の`VALIDATION_CLOSURE`はtarget探索・変更前へ適用しないと明記されているため、既存制御の失敗ではなく、pre-change evidence scopeという未制御領域である。

## F01: 独立中央値による見かけの増加

| iteration | Bundle A token | C81 token | C81 - A |
| ---: | ---: | ---: | ---: |
| 1 | 185,258 | 179,157 | -6,101 |
| 2 | 151,262 | 150,292 | -970 |
| 3 | 133,394 | 180,442 | +47,048 |
| 4 | 163,182 | 178,955 | +15,773 |
| 5 | 153,211 | 110,842 | -42,369 |

- 独立中央値: `153,211 → 178,955`（`+16.80%`）
- paired差中央値: `-970`
- 5回token合計: `786,307 → 799,688`（`+1.70%`）
- paired方向: 減少3 / 増加2

3つのC81成果variantはすべて同じCSI escape sequence grammarを実装し、focused / full gateを通過した。増加したiteration 3 / 4に共通する品質欠陥や追加operationはない。現時点では分布変動として保持し、新しいprompt predicateの根拠にしない。

## F04: reasoning増加とhistory探索

### Mediumのpaired結果

| iteration | A elapsed | C81 elapsed | 差 | A command | C81 command | history探索 |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 70.981 | 73.585 | +2.604 | 6 | 9 | なし |
| 2 | 90.607 | 97.416 | +6.809 | 10 | 8 | なし |
| 3 | 85.913 | 93.517 | +7.604 | 9 | 9 | なし |
| 4 | 72.470 | 70.377 | -2.093 | 10 | 10 | なし |
| 5 | 62.567 | 109.762 | +47.195 | 6 | 12 | `git log` / `git show` |

| 診断量 | Bundle A Medium | C81 Medium | 差 |
| --- | ---: | ---: | ---: |
| token合計 | 853,896 | 755,562 | `-11.51%` |
| elapsed合計 | 382.538秒 | 444.656秒 | `+16.24%` |
| reasoning output | 1,435 | 2,411 | `+68.01%` |
| model step | 47 | 36 | `-23.40%` |
| attempted command | 41 | 48 | `+17.07%` |

C81はmodel stepとtokenを減らしたが、各step内のreasoningとcommand密度が増えた。iteration 5はsourceを`1..940`行へ分割して広く読み、git historyからupstream修正を探索し、最終的に2箇所を変更した。他4件は現在sourceとfocused testだけから1箇所の修正へ到達した。全成果は品質上有効だが、history探索はdone conditionに不要だった。

### reasoning水準を跨いだ再現

| 条件 | history探索 | attempted command合計 | reasoning output合計 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: |
| High Control-free | 0 / 5 | 45 | 3,370 | 469.836秒 |
| High C81 | 3 / 5 | 59 | 5,078 | 554.112秒 |
| Medium Control-free | 0 / 5 | 41 | 1,435 | 382.538秒 |
| Medium C81 | 1 / 5 | 48 | 2,411 | 444.656秒 |

HighとMediumの両方でC81側のelapsed、reasoning、commandが増えたため、Mediumの一時的なhost contentionだけでは説明できない。一方、history探索はC81の全runではなく4 / 10件であり、C81全文のどのpredicateが直接発火させたかはこの観測から確定しない。

## 制御境界

C81の`VALIDATION_CLOSURE`は、artifact変更完了後にrequired validationを一括発行し、成功後の追加readを止める。F04の余分なhistory探索はartifact変更前なので、この制御を変更しても対象経路へ届かない。

新しい制御候補は次の一軸である。

> `PRECHANGE_EVIDENCE_SCOPE`: TaskSpecがrequired outcome、対象source、focused testを固定し、現在sourceとtestから変更箇所をbindできる場合、git history / blameを追加authorityとして読まない。現在sourceとtestだけではmethodをbindできない場合に限りhistoryへ進む。

これは提案であり、Candidate、採用、releaseではない。historyを常に禁止すると、regression originや互換意図がcurrent sourceから分からないtaskを壊すため、現在source / focused testでmethodをbindできる場合だけに限定する。

## 次の試験

新しい制御発見として、C81全文を親に上記一文だけを追加したClick Candidateを作る。まずF04 Medium `N=5`のtargeted gateで次を判定する。

1. 5 / 5件がvalid・score `4`である。
2. git history / blame探索が`0 / 5`である。
3. required focused / full gateを欠落させない。
4. C81 Medium F04に対しpairedまたは同一集約定義でcommand、reasoning、elapsedを記録する。

targeted gateを通過してもStd14効果、採用、release、runtime projectionは未確定である。F04で制御が実際に発火して経路を閉じた場合だけ、同じMedium Std14 70枠へ進む。Click向け単なる文言短縮は別系列とする。
