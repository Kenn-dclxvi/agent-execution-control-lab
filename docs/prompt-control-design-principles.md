# Prompt制御の検討原則

## 位置付け

この文書は、THE-CAPTION向けpromptへ制御を追加、置換、削除する前に使う設計原則を定める。

評価基盤のLayer、KPI、schemaを変更しない。特定candidateの採用、release承認、THE-CAPTION本体への反映も判断しない。

以下は、ControlFreeRepository、Candidate11、Candidate23、Candidate35からCandidate40まで、およびCandidate69からCandidate95までの保存済み観測から得た現時点の設計原則である。少数反復の数値を範囲外へ一般化せず、今後の互換試験で更新する。

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

### Worker選択とコスト判定

Workerの起動要否は、TaskSpecが別execution identityをrequired outcomeにする場合を除き、executor methodとする。promptはWorkerの期待価値を完全なboolean predicateとして列挙しない。

producer選択はoperation分解後へ後付けしない。ただし、単一operationをrootが完了できる場合まで完全なoperation graphや明示planを要求しない。この場合は実行前にrootへ直接bindする。複数operation、別execution identityのresult、またはworker固有capabilityが必要な場合だけ、scope、dependency、result consumer、producer、execution waveを展開してから実行する。

producer関連入力は、required outcomeが別execution identityのresultを必要とするhard constraint、実行手段への希望、owner / risk / roleなどのmetadataへ分ける。hard constraintだけがAIのproducer選択を制約する。Worker利用の指示を含む希望とmetadataはproducer非決定情報として扱い、未制約operationはAIがroot／Workerを選ぶ。

readyなroot operationとWorker operationは同じwaveで開始する。未受領Worker resultが次operationのdependencyで、ほかにreadyなroot operationがない場合だけ待つ。実行開始後は、plan前提の失効なしにproducerを再選択しない。

Worker数、child token、並列／逐次実行、再割当て、rootによる再確認はdiagnosticである。これらを単独の品質またはコスト失敗条件へ昇格しない。Workerを含む実行全体を、互換条件を満たす`quality_score`、all-agent `total_tokens`、`elapsed_seconds`で判定する。

candidateのコストgateは、直接baseline、compatibility key、token / elapsed tolerance、比較単位をcandidate result確認前に固定した場合だけ有効とする。未固定なら、実測値とroute診断を記録してもコスト通過または失敗を確定しない。詳細は[`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)を正本とする。

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

### 9. semantic auditをCandidate作成根拠にしない

prompt本文だけを読んで見つけた未定義、複数解釈、論理上の非対称性は、説明上のriskとして記録できる。ただし、互換なbaselineの保存済み実行結果で対応する誤経路を観測していない限り、それだけを制御追加またはCandidate作成の根拠にしない。

LLM promptは形式仕様ではない。本文上の余白、重複、既定値の未記載が、実行時には正常経路を選ぶための注意配分または裁量として働く場合がある。論理的な完全化によって新しいstate、分類、clarification条件を導入すると、未観測だった判断経路を新たに発火させる可能性がある。

低頻度または確率的な誤経路を一般制御へ昇格する場合は、単発traceの事後説明だけで原因を確定しない。同じbaseline identityとcompatibility条件で再現性を確認するか、別の観測証拠によって変更対象predicateとの因果境界を固定する。

### 10. 実行結果から必要な制御を逆算する

制御設計では、prompt本文の完全性ではなく、baselineの実行結果を出発点にする。最初に、正常経路、誤経路、余分なmodel再入、不要なtool call、欠落したresult、誤った停止を保存済みtraceへbindする。その後で、観測した差を消す最小の制御を選ぶ。

追加する制御は、モデルへ新しい意味判定を要求するのではなく、既存の選択肢またはmodel再入を一つ以上減らすものとする。例えば「non-machine judgmentが必要かを判断する」のようなmeta-predicateは、それ自体が新しい非機械的判断になる。明示input、repository authority、machine-bound resultなど、実行時に直接観測できる値へ変換できない場合はprompt predicateにしない。

局所caseで得たroute改善を共通promptへ昇格する前に、非対象caseへ同じ制御の読解、探索、確認costが流入しないことを確認する。対象caseだけの改善と標準集合全体の改善を分けて評価する。

### 11. 制御を強制可能な層へ置く

観測した問題ごとに、制御を置く層を先に決める。

- requested outcome value、permission、required operationの未固定はTaskSpecまたはschemaで明示する。
- repositoryから一意に解決できるpath、command、配置規則はrepository authorityへ置く。
- モデルが観測可能な条件に基づく判断、停止、具体的なtool発行順はpromptで制御する。
- tool result配送、output cap、atomicity、dispatch順、modelへ戻る前の処理はexecutorで強制する。
- 正しい成果を誤って低得点にする問題はrating contractで修正する。

モデルが発行時点で観測できないruntime stateや、tool adapterがresultを返す前にしか変更できない挙動をpromptへ記述しない。prompt文面で希望するだけでは強制できない制御は、Candidateではなくexecutor capabilityの不足として扱う。

### 12. 意味上の重複を行動上の冗長性と区別する

同じpredicateが別labelにも書かれていることだけを理由に削除しない。LLM promptでは、実行判断を行う位置の近くにある再記述が、注意喚起または誤変換を防ぐ局所的な制約として働く場合がある。

重複を削除、統合、移動する場合は、文字列または論理式の一致ではなく、削除前後の実行routeで同じ判断が維持されることを確認する。意味上の正規化は、単独ではprompt改善ではない。

### 13. mechanism gateの前にbaselineを再実行しない

candidate固有の狙った経路変化は、candidateの保存traceだけで先に確認する。qualityまたはmechanism gateが不通過なら、KPI比較用baselineを新規実行しない。

gate通過後にbaselineが必要になった場合も、同じimmutable identityとcompatibility keyを持つ保存済みresultを先に再利用する。必要なresultが欠ける場合だけ新規slotを作る。複数prompt setの不足slotは別cycleのまま一つのglobal queueへ入れ、推定所要時間の長い順に最大24 workerまで使用する。baseline完了後にcandidateを開始する直列化は、先行resultが後続の発行条件を変える場合だけ許す。

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
2. 保存済みtraceで確認した一つの誤経路。semantic auditの指摘だけではこの項目を満たさない。
3. 既存のTaskSpec、repository authority、repository stateで防げない理由と、promptが制御を置く正しい層である理由。
4. 追加または置換する一つのpredicate。その発火条件は、明示input、repository authority、machine-bound resultのいずれかから直接判定できること。
5. そのpredicateが消す具体的な判断点またはcontext伝播。
6. 新たに増える判断点、label参照、例外条件。
7. 成果品質を維持したことを判定するcaseとscore分布。
8. 想定するtoken、tool call、model step、worker routingの変化。
9. 期待と逆の結果になった場合に、candidate追加を止める条件。

一項でも未定義なら、candidate bundleと評価profileを先に作らない。まず既存traceと制御graphを確認する。

## 現時点の検討方針

> [!IMPORTANT]
> **この節はCandidate35〜Candidate40時点の方針であり、以降の項目は当時の記述として保持する。** `C35からC40までのlabel / predicateの棚卸し`は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)で実施し、そこで合意した一つのpredicateはCandidate41として実装・評価済みである。「次candidateを作成しない」も当時の停止条件であり、その後系譜はCandidate95まで進んだ（系譜は[`candidate-history.md`](candidate-history.md)）。ただしcandidateごとの評価状態は個別であり、bundleの存在は評価済みを意味しない（Candidate36は`not_evaluated`である。評価状態の正本は各candidateの独立evaluation / diagnostic result、未実施分は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列）。現在の未完了項目は[`research-backlog.md`](research-backlog.md)を参照する。上記「制御追加の原則」1〜12とCandidate作成前gateは、時点に依存しない規範として引き続き正本である。

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
- [Candidate69 / Candidate71 validation closure Standard14 B18](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)
- [Candidate71 / Candidate74 typed execution state machine Standard14 N=5](../evaluations/results/candidate71-candidate74-typed-execution-state-machine-v12-standard14-n5_2026-07-23.md)
- [Candidate71 / Candidate79 ordered validation wave F04 N=5](../evaluations/results/candidate71-candidate79-ordered-validation-wave-v13-medium-f04-n5_2026-07-26.md)
- [Candidate71 / Candidate81 validation wrapper precedence Standard14 N=5](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- [Candidate81 / Candidate95 required judgment owner boundary Standard14 B20](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md)
