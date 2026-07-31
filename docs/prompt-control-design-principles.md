# Prompt制御の検討原則

## 位置付け

この文書は、THE-CAPTION向けpromptへ制御を追加、置換、削除する前に使う設計原則を定める。

評価基盤のLayer、KPI、schemaを変更しない。特定candidateの採用、release承認、THE-CAPTION本体への反映も判断しない。

試験の試行回数は`N`で表す。新規の試験、設計、結果では`B`を試行回数の表記に使わない。`N=20`は同一互換条件で選択した20 atomic runを意味する。過去artifactのpathや題名に残る`B20`は履歴identityとして保持するが、新規文書ではその意味を`N`へ読み替えず、実際のrun数を確認して`N=<run数>`と記録する。batch数を示す必要がある場合は`batch count`と明記する。

以下は、ControlFreeRepository、Candidate11、Candidate23、Candidate35からCandidate40まで、およびCandidate43からCandidate125までの保存済み観測から得た現時点の設計原則である。Candidate81以降の横断整理は[`Candidate81からCandidate125までのprompt制御知見`](candidate81-candidate125-control-findings-synthesis.md)を参照する。少数反復の数値を範囲外へ一般化せず、今後の互換試験で更新する。

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

## 制御経路の分類と評価単位

共通promptの一つの効率制御を全taskへ水平適用すると、対象経路の判断を減らす一方で、非対象経路へ新しい分類、確認、再入を追加することがある。制御設計と評価では、少なくともambiguity系（A系）とfulfillment系（F系）を分ける。さらに、正常経路が異なる下位区分を分離する。

この分類は、保存traceを分析し、targeted gateと非対象経路へのspilloverを判定するための設計上の分類である。prompt本文へ`A_MODE`、`F_MODE`、case ID、固定path、固定commandの分岐を追加する根拠にはしない。promptが分岐に使えるのは、TaskSpec、repository authority、repository state、bind済みresultから直接観測できる状態だけである。

### A系: required outcomeとimplementation choiceの解決

A系は、変更開始前に何が未解決かによって二つへ分ける。

| 経路 | 開始状態 | 最短の正常経路 | 閉じるべき誤経路 |
| --- | --- | --- | --- |
| outcome unresolved型（A01型） | 利用者に観測可能なrequired outcome valueが未固定 | TaskSpec明示の開始状態をbindし、変更・試験前に一度のclarificationへ停止 | target、test、history、authorityを読んで未固定outcomeを推測する経路 |
| implementation resolvable型（A02型） | required outcomeは固定済みだがimplementation choiceが未解決 | repository authorityからchoiceを解決し、choiceがbindされた時点で変更前evidence operationをterminalにして変更へ進む | authority path未記載だけによる誤停止と、choice確定後の追加探索・再入 |

outcomeの確定とimplementation choiceの解決を同じauthority判定へまとめない。一般的なallowed readをoutcome決定委譲へ読み替えず、repository evidenceで未固定outcomeを事後補完しない。一方、outcomeが固定済みでrepositoryからimplementationを一意に解決できる場合は、必要なauthority探索をclarificationへ置換しない。

### F系: 成果生成、review、terminal disposition

F系は、成果の性質によって少なくとも三つへ分ける。

| 経路 | 主なoperation | 最短の正常経路 | 主な制御対象 |
| --- | --- | --- | --- |
| 実装・validation型 | artifact変更とrequired validation | 独立した変更前evidenceを必要十分なwaveで取得し、変更後はrequired validation全体を一度発行してterminal resultを集約 | evidence間の不要なmodel再入、validation途中return、再取得、再実行 |
| read-only review型 | 固定diff、source、inventoryの判定 | 判定に必要なevidenceを取得し、findingまたは根拠あるno-findingを一度返す | 固定済みevidenceの再読、対象外探索、finding確定後の追加確認 |
| 変更なしterminal型 | clarification、refusal、scope外停止 | TaskSpecだけでterminal dispositionを決められる場合はrepository evidenceを開かず停止 | 不要なrepository探索、変更・試験の開始、停止後の再入 |

F系の効率制御をA系のauthority解決へ流入させず、A系のauthority admission条件をF系の通常実装へ流入させない。例えば、read batchが固定evidence reviewを短縮しても探索型A02のread集合を広げるなら、共通制御として採用しない。逆に、A01 / A02のauthority分類を追加してF系の全caseへ分類costと再入を増やすなら、そのA系改善をStandard14集約値だけで採用しない。

### 共通promptへ残す不変条件

A系とF系を分けても、次の品質・安全境界は共通promptの不変条件として維持する。

- required outcome、permission、constraintを推測で補完しない。
- operationごとにproducerをbindし、producerのterminal resultを待つ。
- bind済みresultを、明示的な失効またはevidence不足なしに再び問題にしない。
- artifact変更後はrequired validation全体を確定し、全result受領後に一度だけ成否を判断する。
- 未検証の成果を成功、完了、採用可能として報告しない。

共通部分は不変条件に限定する。経路固有の効率制御、探索範囲、review方法、validation配送方法を、別経路にも常時解釈させるglobal proseとして重ねない。

### 経路別gateとspillover判定

新しいcandidateは、変更対象経路のtargeted gateだけでなく、非対象経路へ追加costを移していないことを確認する。

1. outcome unresolved型のqualityと停止挙動を判定する。
2. implementation resolvable型のquality、canonical成果、choice確定前後の探索を判定する。
3. F実装・validation型のquality、required validation、validation再入を判定する。
4. F read-only review型と変更なしterminal型のquality、不要read、停止後再入を判定する。
5. 変更対象外の区分でmodel step、tool call、探索範囲、再読、再試行が増えていないかspilloverを判定する。
6. 各区分のgate通過後にだけStandard14の3 KPIを集約する。

Standard14集約値は最終的な横断KPIであり、経路間のcost移動を相殺してよいという意味ではない。結果報告ではA系subtotal、F系subtotal、下位区分のcase別値を併記する。

token増加は次のように扱う。

- qualityが維持され、保存trace上の経路、model step、探索範囲が変わらない増加は、反復変動の可能性を残して記述する。
- 品質回復または必要なcanonical成果の復元に伴う増加は、必要costとして理由と対象経路を分離する。
- 新しい探索、分類、再入、再読、retryを伴う増加は、全体tokenが減っていてもspillover失敗とする。
- 対象経路の削減を非対象経路の増加で相殺した値だけをcandidate成功の根拠にしない。

### 保存済み結果から得た境界

過去の主な観測は次のとおりである。比率は各resultで固定した比較単位に従い、互換条件の異なる行同士を直接比較しない。

| 比較 | 観測 | 設計上の読み方 |
| --- | --- | --- |
| Candidate43 → Candidate50 targeted | F05 / F10 token合計`-40.08%`、A01 / A02`+15.70%`、20 run全体`-2.49%` | Fのread batchは成立したが、A02のcommand `38 → 84`、model step `48 → 54`を伴う探索拡大のため停止。全体削減はspilloverを打ち消さない |
| Candidate43 → Candidate69 Standard14 | A系token合計`-12.39%`、F系`-24.07%`。A01中央値は増加 | model再入削減は横断効果を示したがcase別方向は一様でない。Candidate69自体はF10 quality gateで停止 |
| Candidate69 → Candidate71 Standard14 | A01 token合計`+1.12%`だがtool call / model stepは不変。A02とF 12 caseはtoken減少 | A01増加を新しい誤経路とせず、validation closureの経路削減を採用判断材料にした |
| Candidate98 → Candidate104 Standard14 | A01中央値`+23.63%`、A02`-25.02%`、A系token合計`-22.12%` | 一つのA caseの増加だけでA系全体を失敗としない。targeted A02 / F07 mechanismと非対象経路を分けて判定 |
| Candidate108 → Candidate116 Standard14 | A02中央値`+19.72%`だがA系token合計`-8.47%`、F系`-9.68%` | A02増加は誤停止せずcanonical implementationを解決する必要costを含む。outcome / implementation境界は成立 |
| Candidate116 → Candidate117 Standard14 | A系token合計`-23.16%`、F系`+19.91%`、全体`+12.80%`。A01 / A02の再入13件減に対し他caseで26件増 | A向けauthority admission分類がFへ判断costを移した。Aの局所改善をglobal predicateとして採用せず停止 |
| Candidate116 → Candidate118 | A02 `N=20`のbind後・変更前再入は5件から0件。Standard14はtoken中央値`+7.44%`、elapsed`-14.37%`で、tokenは11 / 14 caseで増加。completed commandは11件減ったがinput token合計は`+9.67%` | terminal遷移のmechanism成立と全体cost改善を分離する。機構通過だけでは採用せず、command数へ帰属できないinput context costとKPI優先順位を別判断へ残す |

この履歴から、許容されてきたのは「A系ならtoken増加してよい」という規則ではない。正しい挙動を維持し、新しい探索・再入へbindできない局所増加、または品質回復に必要なcostだけを理由付きで許容してきた。経路拡大へbindできる増加は、F側の削減やStandard14全体の削減があっても停止条件とする。

数値と当時の判断の一次記録は、[`Candidate43 / Candidate50 targeted`](../evaluations/results/candidate43-candidate50-root-read-batch-targeted-n5_2026-07-21.md)、[`Candidate43 / Candidate69 Standard14`](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-n5_2026-07-22.md)、[`Candidate69 / Candidate71 Standard14`](../evaluations/results/candidate69-candidate71-validation-closure-v10-standard14-n5_2026-07-22.md)、[`Candidate98 / Candidate104 Standard14`](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md)、[`Candidate108 / Candidate116 Standard14`](../evaluations/results/candidate108-candidate116-outcome-implementation-boundary-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)、[`Candidate116 / Candidate117 Standard14`](../evaluations/results/candidate116-candidate117-implementation-authority-delegation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)、[`Candidate116 / Candidate118`](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)に置く。

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

モデルが発行時点で観測できないruntime stateや、tool adapterがresultを返す前にしか変更できない挙動をpromptへ記述しない。prompt文面で希望するだけでは強制できない制御は、このリポジトリではscope外の制約として記録して停止する。

### 11.1 repository外対応を解決方法にしない

このリポジトリのprompt制御研究では、repository外のexecutor、Codex CLI、tool adapter、runtime hook、外部wrapper、target runtimeの変更を、Candidateの解決策、次案、backlog、または再開条件にしない。正しい強制層がexecutorであるという分類は、外部変更を提案する権限や理由へ変換しない。

repository外の挙動や過去のexecutor試験は、保存済みresultの原因を分類するread-only診断証拠としてだけ利用する。例えば、同じpromptでresult配送方法だけを変えた過去試験は、token増加がprompt判断とoutput配送のどちらに対応するかを切り分ける証拠にはできる。しかし、その観測から外部hook、wrapper、CLI改修をこのrepositoryの次候補として導かない。

promptだけで強制できない問題は、無理に方法指定をpromptへ書かず、かつ外部対応へ作業を広げず、`prompt_control_not_demonstrated / candidate_not_created`として停止する。再開できるのは、保存済み互換traceからmodel-visibleな新しいprompt判断点が確認された場合、またはユーザーが評価基盤保守を別作業として明示した場合だけである。後者をprompt Candidateの系譜、採用判断、releaseへ混ぜない。

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
