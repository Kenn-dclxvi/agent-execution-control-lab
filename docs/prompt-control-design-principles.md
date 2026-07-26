# Prompt制御の検討原則

## 位置付け

この文書は、THE-CAPTION向けpromptへ制御を追加、置換、削除する前に使う設計原則を定める。

評価基盤のLayer、KPI、schemaを変更しない。特定candidateの採用、release承認、THE-CAPTION本体への反映も判断しない。

以下は、ControlFreeRepository、Candidate11、Candidate23、Candidate35からCandidate40までの保存済み観測から得た現時点の設計原則である。少数反復の数値を範囲外へ一般化せず、今後の互換試験で更新する。

## 結論

制御は、規則を増やすためではなく、将来の不要な判断経路を先に消すために追加する。

良い制御は、制御自体の読解と確認に使うtokenより、回避できる探索、context継承、再読、再試行、手戻りのtokenを大きくする。同じ成果品質を維持したまま、実行を最短の有効経路へ収束させる。

追加条件が誤経路を減らす以上に、label間の関係、例外、確認点を増やす場合、その制御は追加しない。既存条件の置換、統合、削除を先に検討する。

## 基準とする基本挙動

最初の基準は、root `AGENTS.md`を0-byteとし、path-scoped repository instructionを保持した`the-caption-3ce91a4-control-free-repository-r1`とする。

この条件でも、実行は次の三層から制御される。

1. TaskSpecがrequired outcome、permission、allowed path、required validation、停止条件を定める。
2. path-scoped repository authorityが正規path、禁止されたlegacy path、配置規則を定める。
3. source、test、diff、repository stateが採用可能な事実と結果を限定する。

root制御を検討するときは、まずこの三層だけで成立する最短経路を記述する。その経路で再現する具体的な不足がない限り、rootへ同じ意味をlabel化して重ねない。

## 制御の価値

tokenへの正味の影響は、次の関係として扱う。

```text
正味token差
= 制御文の読解cost
 + 追加された判断・確認cost
 - 回避できた探索・context継承・再読・再試行・手戻りcost
```

token削減だけを成功としない。必要な確認や成果を省略してtokenが減った場合は、制御による収束ではない。

| 成果品質 | token | 設計上の読み方 |
| --- | --- | --- |
| 維持または向上 | 減少 | 誤経路または不要なcontextを減らした可能性がある |
| 向上 | 増加 | 品質または安全のためのcostとして妥当性を別途判断する |
| 同じ | 増加 | 制御処理だけを追加した可能性を先に疑う |
| 低下 | 増加 | 解釈負荷または最短経路の阻害を疑う |
| 低下 | 減少 | 必要な実行や成果を省略していないか確認する |

評価では中央値だけでなく、score分布、case別token、tool call、model step、worker数、context継承方法を確認する。token差をprompt文面の長短だけへ帰属させない。

## 制御追加の原則

### 1. 観測された誤経路だけを対象にする

新しい制御には、保存済みtraceで再現した誤経路を一つ対応させる。将来起こりそうという理由だけで条件を追加しない。

### 2. 最短の正常経路を先に固定する

誤経路だけでなく、制御追加後も残す正常経路を一つ明示する。正しいresultが既に存在する場合に、追加のowner探索、再取得、再検証を要求しない。

### 3. 実行前に分岐を減らす

正規path、permission、必要なcontext、明示された停止条件など、実行前に選択肢を減らせる条件を優先する。成果取得後のidentity照合や多段bindingは、それが防ぐ具体的な誤採用が確認されている場合だけ使う。

### 4. 一つのlabelに一つの不変条件を持たせる

labelは説明を圧縮するために使う。同じlabelへowner、producer、runtime identity、result、evidence、invalidationなど複数の独立条件を接続しない。

labelを読むたびに複数条件の展開が必要になる場合、そのlabelは圧縮ではなく間接参照になっている。条件の削除または直接記述を検討する。

### 5. 条件の追加数ではなく、消す判断点を数える

追加するpredicateごとに、どの探索分岐、再読、retry、context伝播を消すかを記録する。消す対象を示せないpredicateは追加しない。

### 6. 境界制御と方法制御を混同しない

境界制御は、誰が何を生成できるか、どのresultを受け取れるか、失効がどこまで伝播するかを定める。tool、読取り回数、実行順序は原則として固定しない。

ただし、境界を追加しても実行経路が減らない場合は、境界の文言を重ねない。必要なのがcontext流入の遮断、terminal stateの確定、または明示的な方法制約のどれかを分離して判断する。

### 7. 確定済みresultを再び問題にしない

有効なproducer terminal resultが既にrequired evidenceを含む場合、後続処理はそのresultを入力として扱う。projectionや表示形式の違いだけを理由にproducer operationを再開しない。

再開を許すのは、TaskSpecが追加のoperationを要求した場合、resultが明示条件で失効した場合、または必要なevidenceが欠けている場合に限る。

### 8. 新規追加より置換と削除を優先する

既存制御で同じ誤経路を扱っている場合は、条件を並置しない。既存predicateを狭く置換するか、不要になった記述を削除する。

candidateのroot promptが短くなったこと自体を効率化としない。意味上の判断点と参照関係が減ったことを確認する。

## 参照例

### 有効な方向: worker context sufficiency

Candidate11は、worker packetとallowed readで担当criterionを処理できる場合に`fork_turns=none`とし、不足時だけ必要最小限の履歴を継承した。

workerの起動要否、worker数、担当criterionは固定せず、不要な親contextの流入だけを実行前に遮断した。F07では必要な2 workerを各runで維持し、10 spawnすべてが`fork_turns=none`となった。保存済みN=5ではC10比のF07 token中央値が`-1,009,985`で、Candidate11全体は60 / 60がscore `4`だった。

この例では、短い境界の読解costより、回避した親contextの反復inputが大きかった。

### 注意する方向: result / owner条件の積み重ね

Candidate38からCandidate40では、result unit、producer terminal result、owner identity、evidence、invalidationの関係を追加または明確化した。

Candidate38はCandidate35と同じv9 targeted N=5で成果score `4`を10 / 10満たした一方、10 run token合計は`+255,767`だった。差の99.34%はinput tokenで、90.50%はF10に集中した。

Candidate40はoperationとresult projectionの境界を明確にしたが、F10のtool call、model step、token合計をCandidate38から減らさなかった。score分布は`4 / 1 = 9 / 1`だった。

この観測は、論理境界を詳しくするだけでは実行経路が減らず、label間の解釈と確認を増やす場合があることを示す。次のcandidateを追加する根拠ではなく、既存制御を圧縮する入力として扱う。

## Candidate作成前の検討gate

新しいcandidateを作る前に、次をすべて記録する。

1. 基準prompt setと、その状態での最短正常経路。
2. 保存済みtraceで確認した一つの誤経路。
3. 既存のTaskSpec、repository authority、repository stateで防げない理由。
4. 追加または置換する一つのpredicate。
5. そのpredicateが消す具体的な判断点またはcontext伝播。
6. 新たに増える判断点、label参照、例外条件。
7. 成果品質を維持したことを判定するcaseとscore分布。
8. 想定するtoken、tool call、model step、worker routingの変化。
9. 期待と逆の結果になった場合に、candidate追加を止める条件。

一項でも未定義なら、candidate bundleと評価profileを先に作らない。まず既存traceと制御graphを確認する。

## 現時点の検討方針

> [!IMPORTANT]
> **この節はCandidate35〜Candidate40時点の方針であり、以降の項目は当時の記述として保持する。** `C35からC40までのlabel / predicateの棚卸し`は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)で実施し、そこで合意した一つのpredicateはCandidate41として実装・評価済みである。「次candidateを作成しない」も当時の停止条件であり、その後系譜はCandidate78まで進んだ（系譜は[`candidate-history.md`](candidate-history.md)）。ただしcandidateごとの評価状態は個別であり、bundleの存在は評価済みを意味しない（`not_evaluated`が現在2件ある。評価状態の正本は各candidateの独立evaluation / diagnostic result、未実施分は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列）。現在の未完了項目は[`research-backlog.md`](research-backlog.md)を参照する。上記「制御追加の原則」1〜8とCandidate作成前gateは、時点に依存しない規範として引き続き正本である。

- ControlFreeRepositoryの自然な最短経路を比較基準に含める。
- C35からC40までに追加されたlabelとpredicateを、必要性、重複、参照関係で棚卸しする。
- 次の変更は条件追加を前提にせず、不要なresult unit制御の削除または既存terminal制御への統合を候補にする。
- 次candidateは、上記gateを満たす一つの変更predicateが定まるまで作成しない。
- expandedまたはcontinuous試験は、targeted試験で成果品質の維持と狙った実行経路の変化を確認してから行う。

## Evidence

- [Control-free repository N=5](../evaluations/results/control-free-generic-repository-expanded12-global-m24-n5_2026-07-16.md)
- [Candidate11 worker context sufficiency N=5](../evaluations/results/candidate11-sa-context-boundary-expanded12-global-m24-n5_2026-07-16.md)
- [ControlFreeRepository / Candidate23 operation boundary N=5](../evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)
- [Candidate35 / Candidate38 v9 targeted N=5](../evaluations/results/candidate35-candidate38-outcome-quality-owner-diagnostic-v9-targeted2-n5_2026-07-19.md)
- [Candidate35 / Candidate38 token trace analysis](../evaluations/results/candidate35-candidate38-v9-targeted2-n5-token-trace-analysis_2026-07-19.md)
- [Candidate40 targeted N=5](../evaluations/results/candidate40-operation-result-projection-boundary-v9-targeted2-n5_2026-07-19.md)
