# Candidate146 model step boundary監査

## 結論

Candidate146の作成根拠だった「Candidate145は同じconsumerの既知観測間でmodelへ戻っている」という分析は誤りだった。保存eventの`command_execution`件数をmodel往復数として数えたことが原因である。

`agent_message`をmodel step境界としてC125 / C145 / C146のF01 / F02 / F03各5件を再集計すると、source / testの初回既知観測は3 Candidateとも15 / 15件で一つのmodel stepから共同発行されていた。C146はC145になかったconsumer closureを新たに成立させていない。

実際の差は開始identityとcontent readの間にある。C125は13 / 15件で両者を同じmodel stepから発行した。C145は15 / 15件で別stepにした。C146も14 / 15件で別stepを維持し、1件だけ同じstepへ戻った。

TaskSpecが開始identityの確認を要求するのは「最初のeditまたはrequired command前」であり、content read前ではない。したがって、C143以降で保持した「identity result受領前はcontentを読まない」という境界はTaskSpecより強い。drift resultが変えるのはartifact変更とrequired commandのadmissionであり、既に許可されたreadのadmissionではない。

次に検討する価値がある軸はconsumer closureの強化ではない。resultが後続operationのどの種類を失効できるかを限定する`result_effect_scope`である。開始identityと許可済みreadは共同発行可能にし、その共同resultを受領するまでartifact変更とrequired commandだけを閉じる。

## 訂正対象

次の先行解釈を訂正する。

- `command_execution`一件をmodel往復一件として数えた。
- shell commandが複数なら、前command resultを受領してから次を発行したと推定した。
- C145のF01 / F02 / F03 cost増加を、同一consumer観測間のmodel再入へ帰属した。
- C146のclosure成立を、一つのshell commandへ結合した5 / 15件だけと判定した。

Codex eventでは、複数の`command_execution`が連続し、その間に`agent_message`がなければ、同じmodel stepから発行されたtool call群である。shell command数、tool call数、model step数は別の測定値として扱う必要がある。

## 対象

- Candidate125 F01 / F02 / F03各N=5
- Candidate145 F01 / F02 / F03各N=5
- Candidate146 F01 / F02 / F03各N=5
- Rating v14、`gpt-5.6-sol / medium`、CLI `0.146.0`
- 同じcase、fixture、TaskSpec、runtime、permission、token accounting

各runについて最初のartifact変更より前のeventを取り出し、`agent_message`の後から次の`agent_message`までに発行された`command_execution`を一つのmodel step groupとした。

## 再集計

### 変更前model step中央値

| case | C125 | C145 | C146 |
| --- | ---: | ---: | ---: |
| F01 | 1 | 2 | 3 |
| F02 | 1 | 2 | 3 |
| F03 | 1 | 2 | 2 |

C146はC145より変更前model stepを減らしていない。F01とF02では中央値が一つ増えた。

### 初回既知観測の共同発行

| 観測 | C125 | C145 | C146 |
| --- | ---: | ---: | ---: |
| source / testが同じmodel step | 15 / 15 | 15 / 15 | 15 / 15 |
| identityとcontentが同じmodel step | 13 / 15 | 0 / 15 | 1 / 15 |
| identity result後にcontentを別stepで発行 | 2 / 15 | 15 / 15 | 14 / 15 |

C145でsource / testを複数shell commandへ分けたrunも、command間に`agent_message`はなかった。たとえばF02では4 fileを4つの`sed`へ分けたrunがあるが、4 commandは同じmodel stepから発行され、全result後に一度だけmodelへ戻っていた。

### 初回content result後の追加step

C145はF02の2 / 5件だけが、初回content resultの不足を具体化してfocused continuationへ進んだ。C146ではF01の2 / 5件とF02の5 / 5件がcontent continuationを行い、F01の別1件は適用中`AGENTS.md`を次stepで取得した。

したがって、C146の3 case集約token `-4.50%`、elapsed `-5.61%`をmodel step削減へ帰属できない。F01 / F02のstep数はむしろ増えている。F03はC145と同じ2 stepでもtokenが大きく下がった。N=5のKPI差は記述値として保持するが、C146の追加軸によるcost改善とは判定しない。

## TaskSpecとの照合

F01 / F02 / F03の開始条件は共通して、最初のeditまたはrequired command前に`pwd / branch / HEAD / git status --short`を確認し、予期しないdriftがあれば変更せず停止するよう要求している。

この条件は次を要求する。

- identity result受領前にartifact変更しない。
- identity result受領前にrequired commandを実行しない。
- driftがあればartifact変更とrequired commandへ進まない。

一方、許可済みtarget contentのreadをidentity result受領後まで待つことは要求していない。C125の13 / 15件はidentityとcontentを共同発行したが、そのresult後に初めてartifact変更へ進んでいた。これはTaskSpecの開始条件と両立する。

C146 F01 iteration 1はidentityとcontentを同じmodel stepへ入れた。C146設計自身が追加した「driftならtarget contentを読まず停止する」条件には反するが、評価TaskSpecの「変更せず停止」には反しない。よってquality score `4`は正しく、問題はCandidate設計がTaskSpecより強い境界を独自に追加したことにある。

## C143以降の因果関係の訂正

C143はC125のone-waveを継承せず、required outcome全体のimplementation bindを優先した。その結果、開始identityとimplementation contentを別model stepへ置く挙動がC145まで固定された。

C145のconsumer gateは不要evidenceを閉じたが、F01 / F02 / F03のsource / test共同発行はC145時点ですでに成立していた。したがってC145のcost残差を「consumerのあるevidenceが個別resultへ分断された」と説明することはできない。

C146は、その誤った原因仮説を直接対象にしたため、C145との差分軸が実効挙動として空になった。共同発行はC145と同じ15 / 15である。追加された文面は、開始identityとcontentを同じstepへ入れた1件を逆に設計違反と評価する境界も含んでいた。

## 次の設計可能性

次軸は、resultの停止効果を後続operation全体へ広げず、operation classごとに限定する。

```text
result_effect_scope :=
  そのresultが未発行operationの
  target / permission / method / stop conditionを
  実際に変え得るoperation classの集合
```

開始identityについては次になる。

```text
identity_result_effect_scope = {artifact_change, required_validation}
authorized_read ∉ identity_result_effect_scope
```

そのため、identity観測とTaskSpecで既に許可・固定されたreadは同じmodel stepから発行できる。ただし共同resultを受領してidentityが正常と判定されるまで、artifact変更とrequired commandは発行できない。

これはC125のexact target set、single-target continuation、固定spanを戻す設計ではない。resultが何を止めるかをTaskSpecの権限効果へ一致させる一般境界である。

## 状態

`audited / prior_command_reentry_analysis_corrected / c145_joint_issue_already_15_of_15 / c146_incremental_closure_not_demonstrated / start_gate_effect_scope_overextended / next_axis_bounded / candidate_not_created`

## 結論表

| 論点 | 実測・根拠 | 判定 |
| --- | --- | --- |
| C145の同一consumer観測間model再入 | source / test共同発行15 / 15 | 先行分析を棄却 |
| C146の共同発行 | 15 / 15だがC145も15 / 15 | 増分機構なし |
| C125の低cost側の挙動 | identity + content共同発行13 / 15 | 実在 |
| C145の開始境界 | identityとcontent分離15 / 15 | 追加model stepの主差 |
| C146の開始境界 | 分離14 / 15、共同1 / 15 | 設計自身の過剰境界が不安定 |
| TaskSpecがread前identityを要求するか | 要求しない | 不可避なtradeoffではない |
| C146 KPI改善の帰属 | step数は減っていない | 帰属不能 |
| 次軸 | `result_effect_scope` | Candidate作成前の設計候補 |
