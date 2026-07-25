# Candidate43制御要素の目的別分別

> [!NOTE]
> **正本の範囲**: 本書はCandidate43時点の**目的別分別**（A / F / D / M / R系の区分と記号体系、labelから目的領域への対応）を正本とする。その後Candidate71では11 labelを句単位で監査し、labelごとの**Candidate作成根拠と監査状態**を別軸で判定した。各labelを変更してよいかの現在判定は[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)の「監査状況の分類」表を正とし、本書の分類と混同しない。未完了の再測定項目は[`research-backlog.md`](research-backlog.md)にある。

## 結論

Candidate43の9 labelは、九つの独立した規則ではない。A系、F系、明示委譲、手段選択、回復上限という五つの目的が、`SPEC`、`PRODUCER`、`OWNER_ROLE`を介して相互参照している。

最初に直す対象は文の長さではなく、適用域である。

- A系は、requested outcome valueを確定できるかだけを扱う。
- F系は、確定済みoperationのproducer、result state、terminalだけを扱う。
- 明示委譲系は、TaskSpecが独立producer executionを明示した場合だけ適用する。
- `METHOD`は個別手段とoperation terminalを分離する。
- `RECOVERY`はcounter対象caseだけで独立して判断する。

本書は要素の分別を正本とする。後続candidateと評価runは別artifactで実施し、得た証拠による分類更新だけを本書へ反映する。

## 分類記号

| 記号 | 意味 |
| --- | --- |
| `A` | TaskSpec readiness。実行を開始できるか |
| `F` | fixed operation。開始済みoperationをどう完了するか |
| `D` | explicit delegation。root以外のproducerを明示した場合だけ |
| `M` | method selection。手段失敗とpermission / terminalの分離 |
| `R` | environment recovery counter |

処置は次の四つに分ける。

| 処置 | 意味 |
| --- | --- |
| `retain` | 観測済み誤経路に対応し、目的領域へ残す |
| `conditional` | 常時制御から外し、適用条件が成立した場合だけ使う |
| `merge` | 意味は残すが、重複する別要素へ統合する |
| `review` | TaskSpecとの重複または証拠不足があり、削除前に別確認する |

## 静的構成

以下はUTF-8 byte数であり、token数ではない。tokenizerを固定していないためtokenへ読み替えない。

| label | bytes | 主な目的 | 現在の混在 |
| --- | ---: | --- | --- |
| `SPEC` | 782 | A / F | readinessとoperation scopeが同居 |
| `PRODUCER` | 506 | F / D | single producerと委譲gateが同居 |
| `TERMINAL` | 287 | F | 単一目的 |
| `CONTEXT` | 453 | D | 明示委譲時だけ必要 |
| `OWNER_ROLE` | 1,011 | D / F / evidence | 委譲gate、runtime照合、result stateが同居 |
| `ROOT` | 160 | D | 明示委譲時だけ必要 |
| `INDEPENDENCE` | 193 | F / D | producer exclusivityと一部重複 |
| `METHOD` | 338 | M | 単一目的 |
| `RECOVERY` | 217 | R | 単一目的 |

`SPEC / CONTEXT / OWNER_ROLE`だけで`2,246 bytes`、root本文全体の`56.43%`を占める。`CONTEXT / OWNER_ROLE / ROOT`の`1,624 bytes`、`40.80%`は主として明示委譲時だけ使う制御である。

## 現行labelから目的領域への対応

```text
SPEC --------- A readiness
  |
  +----------- F operation scope

PRODUCER ----- F single producer
  |
  +----------- D explicit producer selection

TERMINAL ----- F completion

CONTEXT ------ D worker input boundary

OWNER_ROLE --- D owner / launch / result provenance
  |
  +----------- F false / failed result state

ROOT --------- D non-producer root boundary

INDEPENDENCE - F separate operation
  |
  +----------- F producer exclusivityと重複

METHOD ------- M invocation persistence
RECOVERY ----- R counter consumption
```

## 原子的要素の分別

### A系: 実行開始の可否

| ID | C43の要素 | 由来と観測 | 処置 | 依存先 |
| --- | --- | --- | --- | --- |
| `A1` | required outcome valueは、明示user inputまたはその値を直接要求する一意なrepository authorityだけから固定する | C42はA01 5 / 5で補集合を正解と推測した。C43は5 / 5で編集・試験前に質問した | `retain` | TaskSpec、repository authority |
| `A2` | current value、option set、complement、test expectation、implementation convenienceを変更後値の根拠にしない | C42の誤経路を直接閉じたnegative boundary | `merge` into `A1` | `A1` |
| `A3` | `spec_ready=false`の間はproducer binding、predicate実行、artifact変更、testを開始しない | C41はA01 5 / 5で未固定policyを推測して実行した。C42で開始禁止を追加した | `retain` | `A1` |
| `A4` | repository authorityから固定できない未固定値だけをclarification resultにする | C43はA01 5 / 5で質問し、A02 5 / 5で不要な質問をしなかった | `retain` | `A1`、TaskSpec |

A系はF系のoperation identity、producer、terminalを参照する必要がない。`spec_ready=false`ならclarificationで終了し、trueの場合だけF系へ渡す。

### F系: 確定済みoperationの完了

| ID | C43の要素 | 由来と観測 | 処置 | 依存先 |
| --- | --- | --- | --- | --- |
| `F1` | required outcomeをoperation identityへ分け、predicate / permission / constraintを固定する | C54はこの関係をoutcome単位だけへ縮めた。C55で初回predicate前bindingを復元した初回F10はstep / tool / tokenを減らしたが、route gate r2では`52 / 47 / 909,468`となり短経路は安定しなかった | 意味関係は`retain`、効率効果は未確定。criterion owner列挙はD系へ分離 | TaskSpec |
| `F2` | result / constraint / terminalを同一operationへ閉じ、別operation / task全体へ伝播させない | C34は別operationの成立済みresponse失効を止め、C33の必須response欠落をtargeted 10 / 10で再現しなかった | `retain` | `F1` |
| `F3` | 初回predicate前に各operationへproducer execution identityを一つbindする | C28はroot / worker重複実行とworker不成立後のroot差替えを対象にした | `retain` | `F1` |
| `F4` | 同一operationのpredicate実行 / result生成を他producerへ再割当てしない | `PRODUCER`と`INDEPENDENCE`の「同一predicateを別producerへ再割当てしない」が重複する | `merge` into `F3` | `F3` |
| `F5` | producer変更は旧bindingを失効し、新operation identityのTaskSpecで行う | C28由来だが、この文だけのablationはない | `review` | `F1`、`F3` |
| `F6` | 全predicateのbind済みproducer terminal resultが揃った場合だけoperationをterminalにする | C31 targetedは15 / 15 score `4`。完了結果を待たずfinal responseで完了宣言する実失敗を対象にした | `retain` | `F1`、`F3` |
| `F7` | invocation / worker / sessionがnonterminal、またはresult欠落ならoperationをnonterminalに保ち、応答で補完しない | C31の実失敗へ直接対応する | `retain` | `F6` |
| `F8` | bind済みcriterionの`false / failed`をterminal resultとして保持し、`unavailable`や別operation失効へ変換しない | C34がC33のfalse対象の曖昧さを修正し、品質中央値を回復した | `retain`、`OWNER_ROLE`からFへ移す | `F2`、`F6` |
| `F9` | 先行result / artifactの独立確認は固有predicateを持つ別operationにする | C68でこの一文だけを削除したF10は5 / 5 score `4`、root-onlyだったが、token中央値`+1.16%`、elapsed中央値`+26.04%`でruntime gateを通過しなかった。A / Dは未確認 | `review`、standalone候補は停止 | TaskSpec、`F1`、`F3` |

F系の中核は`F1 / F2 / F3 / F6 / F7 / F8`である。`F1`はTaskSpec fieldの説明ではなく、確定済みpredicate、permission、constraintを初回predicate前に一つのoperationへbindする関係として残す。`F5 / F9`は既存要素へ統合または常時coreから除く。

Candidate56〜59で、固定readの取得方法をglobal `AGENTS.md`へ置くcostも分離した。Candidate56はF10を5 / 5で3 tool callへ収束させたがA02へ波及した。TaskSpec列挙条件へ狭めたCandidate57とoperation全体のno-edit条件へ狭めたCandidate59もA02 batchを止めなかった。A routeを明示したCandidate58は品質を戻したがA02 tokenを`29.30%`増やした。したがって、Fのmethod controlはF系意味coreへ常置しない。次に検討する場合はF TaskSpecだけへ局所提示し、A TaskSpecから不可視にする別軸とする。

Candidate60では、methodをTaskSpecの局所operation capsuleへ移し、同一A02 task内で次operationへ失効するかを確認した。Candidate55とCandidate60の両方が非伝播を満たしたため、局所化はTaskSpecだけで成立した。一方、共通`AGENTS.md`へexport境界を追加したCandidate60固有の効果は観測できず、A02 tokenは`+88.29%`だった。よって、operation methodのカプセル化はTaskSpec側へ置き、F1の共通意味coreへ追加しない。

### D系: 明示委譲時だけ

| ID | C43の要素 | 由来と観測 | 処置 | 依存先 |
| --- | --- | --- | --- | --- |
| `D1` | criterion owner語列は担当情報でありworker指定ではない | C41はF05 / F10の不要workerを10 / 10で0にし、score `4`を維持した | `retain` | TaskSpec |
| `D2` | TaskSpecが独立producer executionを明示した場合だけ指定identityへ委譲し、predicate前にworkerを起動する | C41の変更predicate。`PRODUCER`と`OWNER_ROLE`に同じgateが重複している | `conditional`、一か所へ`merge` | `D1` |
| `D3` | spawn `task_name`、`FINAL_ANSWER.Sender`、final result bindingのANDでdelegated result provenanceを確認する | C24はchildなし受領自己申告、C30は存在しないruntime field要求を修正した。現行runtime固有である | `conditional`、exact fieldは`review` | `D2`、runtime interface |
| `D4` | `wait`は同期専用とし、result未取得をpassedにせず、producer terminal後も未取得なら`unavailable`にする | child result欠落をroot宣言で補う経路を閉じる | `conditional` | `D2`、`D3`、`F7` |
| `D5` | rootがproducerでない場合はpacket、result binding、terminal集約だけを行い、predicate / resultを再生成しない | C28由来。C38 / C40ではroot / child重複readを単独では止めなかった | `conditional`、`F3`へ`merge` | `D2`、`F3` |
| `D6` | worker packetへ9 fieldを列挙する | fieldの多くはTaskSpec、allowed read、required evidenceと重複する。完全なfield列挙の単独効果は未分離 | `review` | `D2`、TaskSpec |
| `D7` | packetとallowed readで十分なら`fork_turns=none`、不足時も必要最小turnだけ継承する | C33はC32比token中央値`-24.63%`だが品質低下。C34は同境界を維持して品質を回復した | `conditional`、sufficiency境界を`retain` | `D2`、`D6` |

`D3 / D4 / D6 / D7`はroot-onlyのA系・F系では読解対象にしない。D系の正の適用例、すなわちTaskSpecが独立producer executionを明示するcaseで、result provenanceとcontext sufficiencyの必要最小形を再確認する必要がある。

### M系: 手段選択

| ID | C43の要素 | 由来と観測 | 処置 | 依存先 |
| --- | --- | --- | --- | --- |
| `M1` | TaskSpecが明示した手段だけを固定する | C23由来。TaskSpecと重複するが、未指定手段を禁止へ読み替えない前提になる | `merge` with `M2` | TaskSpec |
| `M2` | 未固定手段は同じpredicate / permission内でexecutorが選ぶ | F04 cleanupの代替手段を残す | `retain` | `M1` |
| `M3` | 個別invocationのfailed / unavailableをpermission否定 / terminalにせず、未固定手段があれば継続する | C23の観測済み早期停止へ直接対応する | `retain` | `M2`、`F6` |
| `M4` | 明示禁止 / permission否定は停止し、手段変更で回避しない | permission境界の逸脱を防ぐ | `retain` | TaskSpec permission |

M系はF系のproducerやdelegationを参照せず、`M1 + M2`と`M3 + M4`の二条件へ整理できる可能性がある。

### R系: environment recovery

| ID | C43の要素 | 由来と観測 | 処置 | 依存先 |
| --- | --- | --- | --- | --- |
| `R1` | environment recoveryをenvironment-only repairとsame required command rerunの一組とする | C10 / C23由来。F05 / F10では`not_applicable`だった | `review` in recovery-applicable cases | TaskSpec counter |
| `R2` | 組の開始時だけ上限を消費し、未固定手段の選択は数えない | method choiceによるcounter誤消費を防ぐが、現対象caseでの効果は未測定 | `review` together with `R1` | `R1`、`M2` |

R系は削除候補と決めない。A / F / Dの圧縮へ混ぜず、recovery counterが実際に適用されるcaseで別に判断する。

## 重複と混在の確定一覧

| 現在の重複・混在 | 整理後の所属 |
| --- | --- |
| `SPEC`内のreadinessとoperation scope | `A1..A4`と`F1 / F2`へ分離 |
| `PRODUCER`と`OWNER_ROLE`の明示委譲gate | `D2`一か所へ統合 |
| `PRODUCER`と`INDEPENDENCE`の再割当て禁止 | `F3 / F4`へ統合 |
| `TERMINAL`と`OWNER_ROLE`の応答による補完禁止 | `F7`へ統合 |
| `SPEC`と`OWNER_ROLE`の別operation失効禁止 | `F2 / F8`へ統合 |
| `OWNER_ROLE`内のfalse / failed状態 | D系ではなく`F8`へ移動 |
| `ROOT`のresult再生成禁止 | 明示委譲時の`D5`として`F3`へ接続 |
| `CONTEXT`のpacket fieldとhistory境界 | `D6`と`D7`へ分離 |

## 現時点の保持層

次の形までは事実と保存済み観測から支持できる。これはcandidate文面ではない。

```text
A: readiness
  A1 authority -> A3 stop or A4 clarification

F: fixed operation
  F2 scope -> F3 producer -> F6/F7 completion
                         -> F8 result state

D: explicit delegation only
  D1/D2 gate -> D3/D4 provenance -> D5 root boundary
              -> D7 context boundary

M: method
  M1/M2 selection -> M3 continue or M4 stop

R: recovery
  R1/R2 separate review
```

## 次に確認する要素

candidateを作る前に、次を確認する。

1. `F1 / F5 / F9`のうち、TaskSpecだけでは防げない実誤経路が現在も残るか。
2. 明示委譲の正のcaseで、`D3`のruntime三重照合と`D6`の9-field packetがどこまで必要か。
3. recovery対象caseで`R1 / R2`を外すとcounter誤消費が再現するか。

この三点を後続の「保留要素の判定」で処置できるまでは、削除対象を確定せず、新candidateの作成gateを閉じる。

## 保留要素の判定

2026-07-21に保存済みresult、現行TaskSpec、Candidate43からの差分を再照合した。

| 保留群 | 判定 | 次candidateでの処置 |
| --- | --- | --- |
| `F1` | C54でoutcome単位だけへ縮めるとF10の段階的再判断が増えた。C55初回resultは事前binding復元後に短縮したが、同じpromptのr2では短経路を安定再現しなかった | operationへの事前bindingは意味保持のため残す。効率効果は主張せず、criterion ownerはD系へ分離する |
| `F5` | producer変更を新TaskSpecにする文の単独効果は未確認 | `F3`の再割当て禁止へ統合 |
| `F9` | C52での復元はF10 routingを改善せず、C68での単独削除もF10の成果品質を落とさなかった。一方、C68はtoken合計が事前上限を426超え、A / Dを実行していない | 常時制御からの削除可能性はF10内に限定して保持する。単独candidateは停止し、一般削除へ読み替えない |
| `D3` | C30は実runtime fieldへ合わせた後、targeted 25、expanded 60、continuous 300 runでowner証跡不成立0件 | 明示委譲時だけ保持 |
| `D6` | C11は明示packetとcontext sufficiencyの効果を支持するが、後の9項目すべての単独効果は未確認 | 未解決predicate、target、required evidence、allowed read、forbidden inputへ縮小 |
| `R1 / R2` | 現Evaluation setは`environment_recovery_max=0`または`not_applicable`で、正のcycleを観測していない | 常時coreから外し、正のrecovery caseへ分離 |

ここで「証拠不足」は不要の証明ではない。常時読むcoreへ残す根拠がないという判定である。

保留群は、保持、統合、別検証への分離まで決まった。F1の「outcome入口だけ残す」という初回判定はCandidate54 traceで不十分と分かり、Candidate55で事前bindingを復元した。ただし[`route gate r2`](../evaluations/results/candidate43-candidate55-route-efficiency-gate-r2-catalog-fixed-targeted-n5_2026-07-21.md)では短経路が安定しなかったため、F1は意味保持とruntime効率を分けて扱う。Candidate55は停止し、A01 / A02へ進めていない。

Candidate61ではC55の`READINESS + OPERATION`をC43のatomic `SPEC`一文へ完全一致で戻した。A01 / A02は10 / 10 score `4`だったが、F10は5 / 5が11 tool callとなった。したがって、atomic開始gateはA系境界の意味保持には使えるが、C43短経路を説明する十分条件ではない。結果は[`Candidate43 / Candidate55 / Candidate61対象試験`](../evaluations/results/candidate43-candidate55-candidate61-atomic-spec-operation-gate-catalog-fixed-targeted-n5_2026-07-21.md)へ固定した。

Candidate62ではC43を共通coreとし、C56方法をtask全体がclosed read-onlyの場合だけへ限定した。F10はCandidate56より短縮したが、A02 4 / 5へmethodが流入した。operation-levelだけでなくtask-levelの条件も、同じ常時可視prompt内で方法表現の非適用を保証しなかった。今後この軸を検討する場合は条件文を追加せず、task開始前のprompt set選択として分離する。

Candidate63では、この分離を二つの全文sourceではなく、C43 full bundleと一行route deltaの実行前materializationで実装した。新しいF10-only `N=5`では両promptが5 / 5 score `4`、shell command 55件を維持した。Candidate63は5 / 5で3 tool call、4 model stepへ収束し、token合計はC43比`-52.90%`だった。非対象factsはCandidate43 identityを選ぶ機械契約でdelta bytes自体を不可視にした。F10一事例のため、次は別の固定証拠reviewで再現性と外部selector境界を確認する。

Candidate64では、32 clauseを削らず4 blockへ移し、root / delegated両pathへF coreを全文重複した。A01 / A02、F05 / F10、明示producer D01の25 / 25はscore `4`だったため、意味分別による成果欠落は観測しなかった。一方、root-only F10はtool call `43 -> 54`、model step `48 -> 59`、token合計`+28.90%`となり、A / F / D各scopeのtoken合計も12〜14%増えた。全文重複による自己完結化は停止し、次はCandidate43から共通operation coreとdelegation固有extensionを重複なしで短文化する。

Candidate65ではCandidate43の32 clauseを重複なしの11 labelへ対応させ、root bytesを`7.01%`縮小した。F05 / F10は10 / 10 score `4`、root-onlyだった。一方、F10はtool call `43 -> 49`、model step `48 -> 54`、token合計`+14.25%`となり事前上限を超えた。shell commandは`50 -> 51`に留まり、増加の中心は同じ開始identity確認とsource readを分割したtop-level tool cycleだった。目的領域への再配置を含む圧縮は停止し、次に検討する場合はCandidate43の一層9 label、label順、clause所属を保持した表面圧縮へ限定する。

Candidate66ではCandidate43の一層9 label、label順、32 clause所属を維持し、同一label内の文法表現だけを`57 bytes`、`1.43%`短くした。F10-only、A01 / A02、F05 / F10、D01の30 / 30はscore `4`で、D01の指定producer境界も5 / 5で維持した。最初のF10-onlyではtool call `40 -> 39`、model step `29 -> 28`、token合計`-2.04%`だったが、追加F set内のF10では`43 -> 57`、`48 -> 62`、token合計`+31.36%`となった。表面圧縮だけでも短経路を安定再現しなかったため、この軸を停止する。次は`merge / review / conditional`へ分類済みの重複predicateと常時core外へ分離可能な要素を、表面圧縮と混ぜず意味単位で扱う。

Candidate67では、`D2`の明示委譲gateを`OWNER_ROLE`へ、`F4`のproducer再割当て禁止を`PRODUCER`へ残し、別labelの短い再記述だけを削除した。root bytesは`188 bytes`、`4.72%`減った。対象試験ではCandidate43と同じscore分布とD01境界を維持したが、追加F10とD01のtokenが増えたため一度停止した。その後の標準14項目各`N=5`ではCandidate43とCandidate67の両方が70 / 70 score `4`となり、3 KPI中央値差はquality `0.000`、token `-2.33%`、elapsed `-0.69%`だった。一方、70件token合計はCandidate67が`+0.28%`多い。この観測範囲では`D2 / F4`を各正本一か所へ`merge`できるが、runtime削減の再現性は確定しない。

Candidate68ではCandidate43の`INDEPENDENCE`から`F9`一文だけを削除し、root bytesを`120 bytes`、`3.02%`減らした。F10-onlyは5 / 5 score `4`、root-only、zero driftで、tool call `40 -> 40`、shell command `50 -> 50`だった。3 KPI中央値はquality同値、all-agent token `+1.16%`、elapsed `+26.04%`で、token合計も`811,578 -> 812,004`となった。事前gateに従いCandidate68を停止し、A / F追加scope / Dへ進めない。F9削除によるF10の意味欠落は観測しなかったが、一般削除可能性とruntime改善は確認しない。次はCandidate43から`F5`一文だけを対象にし、producer変更の正の境界を持つcaseを先に選ぶ。

## Evidence

- [`Prompt制御graph棚卸し`](prompt-control-graph-review.md)
- [`Candidate31 terminal closure targeted`](../evaluations/results/candidate31-operation-terminal-closure-owner-producer-v4-targeted3-global-m15-n5_2026-07-17.md)
- [`Candidate32 compact execution control`](../evaluations/results/candidate32-compact-execution-control-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)
- [`Candidate33 worker context sufficiency`](../evaluations/results/candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)
- [`Candidate34 owner result state separation`](../evaluations/results/candidate34-owner-result-state-separation-owner-producer-v5-targeted2-expanded12-n5_2026-07-18.md)
- [`Candidate41 owner metadata / delegation boundary`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)
- [`Candidate42 spec readiness`](../evaluations/results/candidate42-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)
- [`Candidate43 outcome authority`](../evaluations/results/candidate43-outcome-authority-boundary-ambiguity-targeted2-n5_2026-07-20.md)
- [`Candidate43 / Candidate53 purpose separation`](../evaluations/results/candidate43-candidate53-purpose-separated-operation-graph-catalog-fixed-targeted-n5_2026-07-21.md)
- [`Candidate43 / Candidate54 evidence-backed core`](../evaluations/results/candidate43-candidate54-evidence-backed-control-core-catalog-fixed-targeted-n5_2026-07-21.md)
- [`Candidate43 / Candidate55 prebound operation graph`](../evaluations/results/candidate43-candidate55-prebound-operation-graph-catalog-fixed-targeted-n5_2026-07-21.md)
- [`Candidate43 / Candidate55 route efficiency gate r2`](../evaluations/results/candidate43-candidate55-route-efficiency-gate-r2-catalog-fixed-targeted-n5_2026-07-21.md)
- [`Candidate43 / Candidate55 / Candidate61 atomic SPEC`](../evaluations/results/candidate43-candidate55-candidate61-atomic-spec-operation-gate-catalog-fixed-targeted-n5_2026-07-21.md)
- [`Candidate43 / Candidate56 / Candidate62 task-closed read route`](../evaluations/results/candidate43-candidate56-candidate62-task-closed-read-route-catalog-fixed_2026-07-22.md)
- [`Candidate43 / Candidate63 fixed evidence route projection`](../evaluations/results/candidate43-candidate63-fixed-evidence-route-projection-f10-n5_2026-07-22.md)
- [`Candidate43 / Candidate64 self-contained execution paths`](../evaluations/results/candidate43-candidate64-self-contained-execution-paths-catalog-fixed-n5_2026-07-22.md)
- [`Candidate43 / Candidate65 shared operation core`](../evaluations/results/candidate43-candidate65-shared-operation-core-catalog-fixed-f-n5_2026-07-22.md)
- [`Candidate43 / Candidate66 topology-preserving compression`](../evaluations/results/candidate43-candidate66-topology-preserving-compression-catalog-fixed-n5_2026-07-22.md)
- [`Candidate43 / Candidate67 cross-label predicate deduplication`](../evaluations/results/candidate43-candidate67-cross-label-predicate-deduplication-catalog-fixed-n5_2026-07-22.md)
- [`Candidate43 / Candidate67 standard14 N=5`](../evaluations/results/candidate43-candidate67-cross-label-predicate-deduplication-v10-standard14-n5_2026-07-22.md)
- [`Candidate43 / Candidate68 independent review operation removal`](../evaluations/results/candidate43-candidate68-independent-review-operation-removal-f10-n5_2026-07-22.md)
