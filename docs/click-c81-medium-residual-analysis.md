# Click C81 Medium残余経路分析

## 結論

F01のtoken中央値`+16.80%`は、反復内で安定した悪化ではない。iterationを対応させるとC81は5回中3回でtokenが減り、paired差の中央値は`-970 token`だった。独立中央値の組合せだけを根拠にF01向け制御を追加しない。

F04のelapsed増加は再現性がある。Mediumでは5回中4回で増え、paired差の中央値は`+6.809`秒、5回合計は`+16.24%`だった。Highでも5回合計`+17.94%`で同方向だった。C81全文はF04でedit前のgit history探索をHigh `3 / 5`、Medium `1 / 5`、合計`4 / 10`件発生させた。Control-freeはHigh / Medium合計`0 / 10`件だった。

この経路はrequired validation後の追加readではなく、変更方法を決める前の`git log` / `git show` / `git blame`である。C81の`VALIDATION_CLOSURE`はtarget探索・変更前へ適用しないと明記されているため、同predicateの失敗ではない。ただし、2026-07-28に4件のraw traceを再解析した結果、history探索後に初めてmethodまたは変更scopeが確定していた。保存traceに「method bind後の代替探索」は`0 / 4`件であり、新しいprompt制御または既存`METHOD`置換の根拠にはしない。

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

## method bind時点の再解析（2026-07-28）

C81の`VALIDATION_CLOSURE`は、artifact変更完了後にrequired validationを一括発行し、成功後の追加readを止める。F04の余分なhistory探索はartifact変更前なので、この制御を変更しても対象経路へ届かない。

当初は次の新規labelを候補にした。

> `PRECHANGE_EVIDENCE_SCOPE`: TaskSpecがrequired outcome、対象source、focused testを固定し、現在sourceとtestから変更箇所をbindできる場合、git history / blameを追加authorityとして読まない。現在sourceとtestだけではmethodをbindできない場合に限りhistoryへ進む。

この文は`git history / blame`という具体的手段を固定し、repository evidenceをauthorityとして扱い、既存`METHOD`へ新しい判断点を並置するため、[`prompt-control-design-principles.md`](prompt-control-design-principles.md)の「境界制御と方法制御を混同しない」「新規追加より置換と削除を優先する」に合わない。そこでCandidateを作らず、history探索4件について「history取得前にmethodがbind済みだったか」をraw traceで確認した。

| reasoning / iteration | run ID | history取得前 | history resultが確定した内容 | 分類 |
| --- | --- | --- | --- | --- |
| High / 2 | `87f3dfcd98e94f33a8004a863e3d4486` | 親`ctx`から残り引数を取る1行を原因候補としたが、repository意図の確認を未解決条件として明示 | 同じ不具合の既存修正と、子contextへ切り替えてから残り引数を取る2行の順序 | bind前。methodと変更単位の確定に使用 |
| High / 3 | `d0576447b0354220ac26fb6e5054f024` | non-chain Groupの原因を特定 | 同じfixture commitが壊した2箇所を確認し、chain Groupを変更scopeへ追加 | bind前。target scopeを変更 |
| High / 5 | `0f0bda9475c54b9681c628fd00da6f60` | sourceとfocused testを読む範囲だけを固定 | 既存修正から2行の順序復元をmethodとして確定 | bind前。method確定に使用 |
| Medium / 5 | `29fac65be1504fb5929f3622448e6b8f` | source前半とfocused testを読み、関連履歴を調査対象に含めた | fixture seedと既存修正を確認した後、非-chain / chain両経路の順序復元を確定 | bind前。methodと変更scopeの確定に使用 |

4件とも、最終成果から遡ればcurrent sourceとfocused testだけでも解けた可能性はある。しかし、それは事後的なoracle判断であり、各trace内でhistory取得前にmethodがbind済みだった証拠ではない。historyがdone conditionに不要だったことと、取得時点でmethod bindに不要だったことは分ける。

## 停止判断

Candidate作成前gateのうち、次を満たせない。

- 保存済みtraceで、method bind後にも続いた具体的な誤経路を示せない。
- TaskSpec、repository authority、repository stateだけでは防げない理由を示せない。
- 新しいpredicateが消す判断点を、必要なevidence取得と分離できない。

したがって`PRECHANGE_EVIDENCE_SCOPE`の新規追加、`METHOD`置換Candidate、F04 Medium `N=5` targeted runは実施せず、この軸を`stopped_before_candidate`とする。F04のelapsed差とhistory探索`4 / 10`は診断事実として保持するが、追加prompt制御の根拠へ読み替えない。将来、method bind済みを明示した後にも代替evidence探索が続く保存traceを別に観測した場合だけ、新しい作成前gateとして再検討する。
