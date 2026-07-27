# Click Control-free Medium baseline分析

## 結論

ClickのControl-free baselineがTHE-CAPTIONより軽い主因は、reasoning effortだけではなく、repositoryとcaseがモデルへ返すcontext量の差である。Medium同士の記述的対照では、ClickはTHE-CAPTION ControlFreeRepositoryより公式token中央値が`889,082`（`25.42%`）、elapsed中央値が`177.033`秒（`14.16%`）小さかった。70 trace合計ではtool出力文字数が`50.46%`少ない一方、model stepは`10.26%`、tool wrapperは`11.21%`少ないだけだった。

したがって、「Clickでは推論stepそのものが一律に少ない」とは言えない。小さいsource tree、root以外のrepository instructionがないこと、短いread / test出力が各model再入時のcached contextを小さくしている、というrepository固有特性が強い。ただしClick A02はTHE-CAPTION対応caseより重く、Click固有のrouting / validation探索は別の最適化余地として残る。

## 比較境界

次の3系列を使った。

| 系列 | reasoning | prompt | run |
| --- | --- | --- | ---: |
| Click High | `high` | root `AGENTS.md` 0 byte | 70 |
| Click Medium | `medium` | root `AGENTS.md` 0 byte | 70 |
| THE-CAPTION ControlFreeRepository Medium | `medium` | root制御prompt 0 byte、階層別repository instructionは維持 | 70 |

Click High / Mediumは同じset、case、rating、runtime、prompt identityでreasoningだけが異なる。reasoningはcompatibility conditionなので、差は水準間の診断であり同一Layer 4 comparisonではない。

Click / THE-CAPTION Mediumはmodelとreasoning、各14 case・N=5・M=24を揃えたが、target repository、case内容、rating contractが異なる。この対照はrepository特性の記述に限り、prompt効果や因果効果の推定には使わない。

## 公式KPI

| 条件 | score分布 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Click High | `4 = 70` | 100.000 | 2,860,702 | 1,235.719秒 |
| Click Medium | `4 = 70` | 100.000 | 2,607,894 | 1,073.024秒 |
| THE-CAPTION ControlFreeRepository Medium | `4 / 0 = 65 / 5` | 92.857 | 3,496,976 | 1,250.057秒 |

Click内でMediumはHighよりtoken中央値`-252,808`（`-8.84%`）、elapsed中央値`-162.695`秒（`-13.17%`）だった。品質は70 / 70件でscore `4`を維持した。

Medium同士ではClickがTHE-CAPTIONよりtoken中央値`-889,082`（`-25.42%`）、elapsed中央値`-177.033`秒（`-14.16%`）だった。品質差はA01のcase内容とrepository cueが異なるため、repository規模の効果として解釈しない。

## trace分解

全70 runのroot sessionを同じ抽出方法で集計した。公式KPIはiteration単位の中央値であり、以下の70 trace合計とは集約方法が異なる。

### Click HighからMedium

| 診断量 | High | Medium | 差 |
| --- | ---: | ---: | ---: |
| all-agent token | 14,232,713 | 13,307,331 | `-6.50%` |
| cached input token | 12,199,936 | 11,365,888 | `-6.84%` |
| output token | 195,266 | 167,581 | `-14.18%` |
| reasoning output token | 46,575 | 28,788 | `-38.19%` |
| model step | 688 | 656 | `-4.65%` |
| tool wrapper | 618 | 586 | `-5.18%` |
| tool出力文字 | 1,723,987 | 1,693,783 | `-1.75%` |

Medium化で最も大きく減ったのはreasoning outputである。model stepとtool出力量の減少は小さいため、Click内のHigh→Medium短縮は主に各model stepの推論量低下と、一部の再入・tool call減少で説明できる。

### Click MediumとTHE-CAPTION Medium

| 診断量 | THE-CAPTION | Click | Click差 |
| --- | ---: | ---: | ---: |
| all-agent token | 17,173,925 | 13,307,331 | `-22.51%` |
| cached input token | 14,567,424 | 11,365,888 | `-21.98%` |
| output token | 193,598 | 167,581 | `-13.44%` |
| reasoning output token | 31,015 | 28,788 | `-7.18%` |
| model step | 731 | 656 | `-10.26%` |
| tool wrapper | 660 | 586 | `-11.21%` |
| tool出力文字 | 3,418,845 | 1,693,783 | `-50.46%` |

token差`22.51%`に対してreasoning output差は`7.18%`に留まり、tool出力文字は半減した。これは「Clickのモデルが深く考えない」よりも、「各stepへ戻るrepository contextが小さい」ことを支持する。

## repository固有特性

固定fixtureのtracked artifact量は次のとおりだった。

| target | tracked file | tracked byte | source file | docs file | `AGENTS.md` |
| --- | ---: | ---: | ---: | ---: | ---: |
| Click | 165 | 1,580,629 | 18 | 41 | 0 |
| THE-CAPTION | 259 | 14,870,276 | 76 | 70 | 5 |

THE-CAPTIONはtracked byteがClickの約`9.41倍`、source fileが約`4.22倍`である。ControlFreeRepositoryはroot制御promptを空にするが、4つの階層別repository instructionを維持する。Click Bundle Aはroot `AGENTS.md`が0 byteで、階層別instructionもない。この差は、read結果、検索結果、適用規則がmodel再入時のcached inputへ積み上がる量と整合する。

これは相関であり、repository size単体の因果効果ではない。両targetのcase実装量、test出力、言語、rating contractも異なる。

## 軽さの例外

case番号は役割を揃えた対応であり、task本文は同一ではない。

| 対応case | Click Medium | THE-CAPTION Medium | 観測 |
| --- | --- | --- | --- |
| A02 | 429,730 token、16 step、132.782秒 | 298,180 token、9 step、96.740秒 | Clickがtoken `+44.12%`。tox routingと検証経路がClick固有の重い経路 |
| F02 | 223,548 token、11 step、104.139秒 | 306,699 token、9 step、94.403秒 | Clickはcontextが小さいが再入とelapsedは多い |
| F06 | 249,282 token、13 step、88.006秒 | 282,521 token、11 step、84.881秒 | tokenは小さいがstepとelapsedは小さくない |
| F07 | 176,685 token、9 step、67.251秒 | 386,894 token、17 step、108.867秒 | Clickのcanonical runner経路は大幅に軽い |
| F08 | 186,562 token、10 step、68.654秒 | 405,931 token、19 step、132.737秒 | docs同期でrepository規模差が強く現れる |
| F10 | 143,234 token、8 step、74.588秒 | 226,361 token、13 step、114.831秒 | read-only inventoryもClickが軽い |

Click全体のbaselineが軽くても、A02、F02、F06には多い再入が残る。新しい制御を探す場合は、全caseへ一律に指示を足すより、この3経路のtraceで繰り返すnavigation、routing判断、validation再入を起点にする方が、既存の軽いcaseへcostを加えにくい。

## 次の判断

事実として、MediumはClickの新しい通常比較基準線を70 / 70 score `4`で確立した。事前には、C81全文の主作用であるmodel再入削減は、Medium化で既にstepが`4.65%`減ったため限界効果が小さくなる可能性を置いた。追試では逆に、C81全文はtoken中央値`-28.79%`、elapsed中央値`-12.62%`となり、Highのtoken `-23.96%`を上回る削減率とHighで得られなかったelapsed短縮を示した。

C81全文 Medium Std14は同じcompatibility keyで70 / 70 score `4`を維持した。A02とF06のtoken中央値はそれぞれ`-54.88%`、`-41.32%`となり、Baselineで重かった経路にもC81が効いた。一方、F01はtoken `+16.80%`、F04はelapsed `+29.04%`だった。次の新しいClick固有制御またはprompt最適化は、この2つの残余経路のtraceを先に分析してから設計する。
