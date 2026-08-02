# Candidate145 F01 / F02 / F03 cost原因分析

## 結論

Candidate145のCandidate125比cost増加を「同じconsumerの既知観測が個別resultへ分断され、各command後にmodelへ戻ったため」とする先行分析は誤りだった。`command_execution`件数とmodel step数を混同していた。

保存traceを`agent_message`境界で再集計すると、F01 / F02 / F03のsource / test初回観測はCandidate125、Candidate145とも15 / 15件で同じmodel stepから共同発行されていた。

主な構造差は開始identityである。Candidate125は13 / 15件でidentityとcontentを同じmodel stepから発行した。Candidate145は15 / 15件でidentity resultを受領してからcontentを別stepで発行した。この一step追加が、同程度のcontent outputでもcached inputが増えた事実と整合する。

TaskSpecはidentity確認を最初のeditまたはrequired command前に要求するが、read前には要求しない。したがって、identity resultの停止効果を許可済みreadまで広げた境界は不可避な安全性tradeoffではない。次の分析軸はconsumer closureではなく、resultが失効できる後続operation classを限定する`result_effect_scope`である。

詳細な再監査は[`Candidate146 model step boundary監査`](candidate146-model-step-boundary-audit.md)を正本とする。

## 対象と訂正方法

比較対象は、同じStandard14、Rating v14、`gpt-5.6-sol / medium`、CLI `0.146.0`で登録されたCandidate125とCandidate145のF01 / F02 / F03各5件である。

先行集計で用いた変更前command件数、output文字数、token、elapsedの数値は保存eventから正しく取得されている。ただし、複数commandが連続し、その間に`agent_message`がない場合も個別model往復と解釈した因果推論が誤っていた。

訂正後は次を分ける。

- shell command件数
- tool call件数
- `agent_message`で区切ったmodel step数
- 同じmodel stepから共同発行された観測集合
- 初回content result後のfocused continuation

## 保存済みKPI

| case | Candidate | total token中央値 | elapsed中央値 | cached input中央値 | 変更前command中央値 |
| --- | --- | ---: | ---: | ---: | ---: |
| F01 | C125 | 104,663 | 63.337秒 | 62,464 | 1 |
| F01 | C145 | 154,553 | 88.154秒 | 119,296 | 3 |
| F02 | C125 | 124,094 | 78.648秒 | 83,968 | 1 |
| F02 | C145 | 196,118 | 114.228秒 | 166,144 | 8 |
| F03 | C125 | 99,202 | 68.374秒 | 70,656 | 1 |
| F03 | C145 | 166,152 | 93.882秒 | 115,968 | 3 |

この表のcommand件数差はtool callの構成差を示す。しかしmodel往復数は示さない。

## model step再集計

| case | C125変更前model step中央値 | C145変更前model step中央値 | source / test共同発行 C125 | source / test共同発行 C145 |
| --- | ---: | ---: | ---: | ---: |
| F01 | 1 | 2 | 5 / 5 | 5 / 5 |
| F02 | 1 | 2 | 5 / 5 | 5 / 5 |
| F03 | 1 | 2 | 5 / 5 | 5 / 5 |

C145のF02では4 fileを4つの`sed`へ分けたrunがある。しかし4 command間に`agent_message`はなく、同じmodel stepから発行され、全result後に一度だけmodelへ戻っていた。

初回content result後のfocused continuationはCandidate145 F02の2 / 5件で発生した。この追加stepはF02の一部costを説明できるが、F01 / F03の共通増加は説明しない。

## 開始identity境界

| 挙動 | C125 | C145 |
| --- | ---: | ---: |
| identityとcontentを同じmodel stepから発行 | 13 / 15 | 0 / 15 |
| identity result後にcontentを別model stepから発行 | 2 / 15 | 15 / 15 |

C125は共同resultを受領してからartifact変更へ進んでいる。identityとcontentを同時に発行しても、identity result受領前にeditまたはrequired commandを発行したことにはならない。

TaskSpecの停止条件は、drift時に「変更せず停止」することである。許可済みcontentを読まず停止することは要求していない。Candidate145側の分離は、identity resultがread permissionも変えると広く解釈した結果である。

## 因果解釈

事実として、Candidate145はCandidate125より変更前model stepが各case中央値で一つ多い。各追加stepでは、それまでのprompt、TaskSpec、message、tool resultが再びmodel inputへ入る。F01 / F03でcontent output量がほぼ同じでもcached inputが増えたことと整合する。

F02にはさらに初回content不足後のfocused continuationが2件ある。ただし、command件数`1 → 8`の差全体を8回のmodel往復として扱ってはならない。

したがって、Candidate145 cost増加の支持された原因は次である。

1. C125の大半にあったidentity + content共同stepを外した。
2. F02の一部でcontent不足後のcontinuationが追加された。
3. command構成差は存在するが、単独ではmodel往復増加を示さない。

## 次に検討する境界

次案では、resultが変え得る後続operationを種類別にbindする。

```text
result_effect_scope :=
  resultがtarget / permission / method / stop conditionを
  実際に変え得る未発行operation classの集合
```

開始identity resultはartifact changeとrequired validationを止め得る。一方、TaskSpecで既に許可されたreadは止めない。そのためidentityと許可済みreadは同じmodel stepから発行し、共同resultを受領してidentityが正常と判定されるまでartifact変更とrequired commandだけを閉じる。

この境界はexact target set、single-target continuation、file数、span、command形式を固定しない。

## 結論表

| 論点 | 訂正後の判定 | 根拠 |
| --- | --- | --- |
| C145のsource / testが個別model往復か | いいえ | 15 / 15で同じmodel stepから共同発行 |
| command数増加がそのまま往復増加か | いいえ | command間に`agent_message`なし |
| 共通cost差 | identity / content分離が主候補 | C125共同13 / 15、C145共同0 / 15 |
| F02固有差 | focused continuationを含む | C145 2 / 5 |
| C125の挙動はTaskSpec違反か | 違反ではない | read前identityは要求されていない |
| consumer closureを次軸にするか | しない | C145ですでに共同発行成立 |
| 次軸 | `result_effect_scope` | 停止効果をoperation classへ限定 |
