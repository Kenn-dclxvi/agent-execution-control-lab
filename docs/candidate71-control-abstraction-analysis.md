# Candidate71 control abstraction分析

> [!IMPORTANT]
> **番号「Candidate74」の帰属に注意**: 本文が`P3`削除提案の作業名として繰り返す「Candidate74」は、本分析時点で作成前gateだけを定義しbundle・profile・評価が未着手の提案呼称である。その後、番号「Candidate74」は別軸の`the-caption-3ce91a4-typed-execution-state-machine-r1`（`standard14_evaluated`）へ実際に割り当てられた。Candidate番号とlineageの正本は[`prompts/candidates/README.md`](../prompts/candidates/README.md)、release・projectionの正本は[`prompts/releases/README.md`](../prompts/releases/README.md)とする。`P3`削除提案を「Candidate74」として新規作成せず、着手時は正本で現行の番号割当てを確認する。以下の各判定は当時の記述として保持する。

> [!NOTE]
> **この文書の読み方**（追補）: 本文は「現在の総括」「label別の監査台帳」「監査初期の履歴」が同居する。目的別の入口は次のとおり。
>
> - **現在の総括を知る**: [監査状況の分類](#監査状況の分類完了と再測定要の分離)（11 labelの最終判定と、再測定が必要な項目）。文書末尾にある。
> - **個別labelの根拠を読む**: 各`<label>監査結果`節（`OWNER_ROLE`、`SPEC`、`CONTEXT`、`PRODUCER`、`INDEPENDENCE`、`TERMINAL`、`ROOT`、`DECISION_BOUNDARY`、`METHOD`、`RECOVERY`の10節。`VALIDATION_CLOSURE`は凍結のため独立節を持たない）。
> - **未完了項目の着手判断**: [`research-backlog.md`](research-backlog.md)（`CONTEXT` X1、`INDEPENDENCE` I1、`RECOVERY` R1・R2、`P3`削除candidateを索引化）。
> - **履歴として読む**: 直下の`結論`に続く`五つの制御機能`から`現在の判定`までは監査初期（`OWNER_ROLE`→`SPEC`着手時点）の記述である。現在の判定として読まない。

## 結論

Candidate71のKPI差から確認できる因果は、11 label全体ではなく、Candidate69へ追加した`VALIDATION_CLOSURE`一行の効果に限定される。

その効果は「細かい試験手順」ではなく、変更後に行動集合が確定したら、全validationを一度に発行し、全result受領後の状態遷移を一度でterminalへ閉じる制御として抽象化できる。

ただしCandidate72とCandidate73は、抽象名だけを残すことと、tool実行だけを閉じることでは不十分だと示した。保持が必要なのは、入口の完全性、同時発行、result有効性、成功後のtool closure、成功後のresponse closureである。Candidate71の全単語が必要だとは確認していない。

その後、11 labelすべてを句単位で監査した(下記各`監査結果`節)。現時点の総括は[監査状況の分類](#監査状況の分類完了と再測定要の分離)にある。結果として、Candidate作成根拠が立つのは`PRODUCER`の`P3`一文削除だけで、他10 labelは根拠なし(完了6・暫定未完了3・凍結1)である。`P3`削除Candidate74はgate 9項目を定義済みだが、bundle / profile /評価は未着手であり、`PRODUCER`以外の不変更方針を維持する。

この冒頭以降の`五つの制御機能`〜`OWNER_ROLE監査結果`〜`現在の判定`は監査初期(OWNER_ROLE→SPEC着手時点)の記述で、履歴として保持する。最新の判定は各label `監査結果`節と`監査状況の分類`表を正とする。

## 事実

Candidate71のroot `AGENTS.md`は4,987 byte、11 labelである。

| label | byte | root全体比 | 主な内容 |
| --- | ---: | ---: | --- |
| `OWNER_ROLE` | 1,010 | 20.3% | owner解釈、worker起動条件、runtime identity、result binding、失敗伝播、補完禁止 |
| `SPEC` | 781 | 15.7% | outcome authority、実行開始gate、clarification、operation間の非伝播 |
| `VALIDATION_CLOSURE` | 695 | 13.9% | validation入口、同時発行、result判定、terminal closure、非適用域 |
| `PRODUCER` | 505 | 10.1% | producer一意性と変更時失効 |
| `CONTEXT` | 452 | 9.1% | workerへ渡す最小十分context |
| その他6 label | 1,544 | 31.0% | terminal、operation独立性、decision、method、recovery |

上位3 labelだけで2,486 byte、root全体の49.9%を占める。

Candidate69とCandidate71のroot差は`VALIDATION_CLOSURE`一行だけである。同一互換条件のB18ではCandidate71のall-agent token合計、elapsed合計、top-level tool call、model stepがCandidate69より小さかった。一方、意味確認ではCandidate71にA02のrequired validation欠落3件と、A01の未確認実装1件があり、Candidate71は停止済みである。

Candidate72は`VALIDATION_CLOSURE`を短いOPEN / CLOSED表現へ置換した。品質は維持したが、F06の編集後model再入中央値とtoken中央値が増えた。

Candidate73は入口、同時発行、成功後追加read禁止、失敗時nonterminalを残した。成功後の追加read / validationは0件だったが、F06の編集後model再入中央値は`2 -> 3`となった。tool closureだけでresponse closureを再現できなかった。

## 五つの制御機能

11 labelは、表現ではなく次の五機能へまとめて読める。

| 制御機能 | 対応label | 不変条件 |
| --- | --- | --- |
| Authority closure | `SPEC`、`INDEPENDENCE` | outcomeとoperation境界が確定するまで変更を始めない |
| Producer uniqueness | `PRODUCER`、`OWNER_ROLE`、`ROOT` | 一つのoperation resultを一つの実行identityだけが生成する |
| Context boundary | `CONTEXT` | producerへ必要十分なcontextだけを渡す |
| Decision / terminal closure | `DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`TERMINAL` | 独立resultをまとめ、欠落を補完せず、一度の状態遷移で閉じる |
| Failure semantics | `METHOD`、`RECOVERY` | method失敗、permission否定、environment recoveryを混同しない |

この五機能が構造であり、11個のlabel名や現在の文章量は実装表面である。

## どこが試験対策に見えるか

### 事実

`OWNER_ROLE`は`runtime_spawn_result.task_name`、`FINAL_ANSWER.Sender`、`wait`など、特定runtimeの観測fieldを直接参照する。

`SPEC`は一つのlabel内で、authority、開始gate、clarification、operation間伝播という複数の独立判断を扱う。

`VALIDATION_CLOSURE`はvalidation commandの発行model stepまで指定するため、境界制御だけでなく方法制約を含む。

### 推測

`OWNER_ROLE`は、一般的な「producer identityを一意にする」という不変条件より、評価traceでidentityを証明する方法までroot promptへ持ち込んでいる可能性が高い。これは11 label中で最も試験対策的に見える部分である。

`SPEC`も過積載だが、A01の未固定mode誤実装に直接関係するため、先に短縮するとStrict制御を弱める可能性がある。

`VALIDATION_CLOSURE`の方法制約は一般原則だけなら細かい。しかしCandidate72 / 73で、現在のruntimeではtool closureとresponse closureを自然には同時に保証できないことを観測した。現時点では単なる試験対策とは切り分ける。

## `OWNER_ROLE`の監査順序

1. `OWNER_ROLE`の各節を、保存済みtraceで実際に防いだ誤経路へ対応付ける。
2. 対応する誤経路がないruntime証跡手順を、構造的不変条件から分離する。
3. 一つの削除または置換predicateが定まった場合だけCandidate74の作成前gateを書く。
4. targeted試験でproducer誤帰属、worker欠落、root補完、tokenとmodel stepを確認する。
5. targetedで機能を保持した場合だけ、標準14項目またはB18を検討する。

`SPEC`と`VALIDATION_CLOSURE`はこの段階で変更しない。

## `OWNER_ROLE`監査結果

### 結論

`OWNER_ROLE`は試験case固有ではない。Codex runtimeの委譲protocolへ強く依存した条件である。

root-only taskへ常時読ませる配置は細かいが、句をそのまま削除できる証拠はない。既に同じ問題へ広い圧縮を行ったCandidate49は品質を維持した一方、20 run token合計を13.21%増やして停止している。Candidate74は作らない。

| `OWNER_ROLE`の機能 | 保存済み根拠 | 判定 |
| --- | --- | --- |
| criterion owner語列だけでworkerを起動しない | Candidate41はF05 / F10の不要workerを10 / 10で0にし、score `4`を維持した | 保持 |
| TaskSpecが独立producer executionを明示した場合だけ委譲する | Candidate41の変更predicate。Candidate67ではこのgateを`OWNER_ROLE`一か所へ残してD01の指定workerを5 / 5で維持した | 保持 |
| spawn `task_name`、`FINAL_ANSWER.Sender`、final result bindingでprovenanceを確認する | Candidate29はruntimeに存在しないfieldを要求した。Candidate30は実fieldへ直し、targeted 25、expanded 60、continuous 300 runでowner証跡不成立0だった | 明示委譲時だけ保持 |
| `wait`をidentity証跡にせず、result欠落をpassedへ補完しない | Candidate20 / 22ではchild sessionとfinal resultがないままrootが独立判定の受領を自己申告した | 明示委譲時だけ保持 |
| `false / failed`を同operationのterminal resultとして保持し、別operationを失効させない | Candidate33の必須response欠落に対しCandidate34が状態を分離し、targeted 10 / 10とexpanded 60 / 60を登録した | 意味は保持。ただし所属は`TERMINAL`側が自然 |
| root宣言、異Sender、root再構成でresultを補完しない | child resultなしの受領自己申告と、別producer resultのroot差替えを直接禁止する | 上記provenance / terminal条件の否定例として保持 |

### 推測の訂正

`runtime_spawn_result.task_name`や`FINAL_ANSWER.Sender`が書かれているため試験対策的に見える、という最初の推測は半分だけ正しい。

特定caseの正答を誘導する文ではない。実runtimeが返すfieldと、過去に実際に起きた偽のresult受領を対応付けたprotocolである。この意味では構造的である。

問題は、明示委譲がないroot-only taskでも1,010 byteの条件がroot promptに常在することである。ただしCandidate49の広い分離は実行tokenを減らさなかったため、「委譲時だけ別blockにする」と再提案するだけでは新しい検証仮説にならない。

### 次の対象

`OWNER_ROLE`は変更せず、次は`SPEC`を同じ方法で監査する。`SPEC`は781 byteの中にauthority、開始gate、clarification、operation間非伝播を持ち、`OWNER_ROLE`よりも一label一不変条件の原則へ明確に反している。

## 現在の判定

Candidate71のKPI改善は、制御全体が優れている証拠ではない。`VALIDATION_CLOSURE`によるmodel再入削減の証拠である。

同時に、Candidate72 / 73の結果は現在の詳細文を逐語的に正当化しない。抽象化で保持すべき機能境界を示しただけである。

したがって、全体を一括短縮するのではなく、KPI差に寄与していない大きなlabelから一つずつ、誤経路との対応を監査する。

（この節までが監査初期の判定。以降の各`監査結果`節で11 label全てを監査した。最終の総括は[監査状況の分類](#監査状況の分類完了と再測定要の分離)を正とする。）

## `SPEC`監査結果

### 結論

`SPEC`の六句はすべて保存済み誤経路へ対応し、削除または他labelへの置換で判断点を消せる句は一つもない。Candidate74は作らない。次は`CONTEXT`の9-field packet列挙を同じ方法で監査する。

### identity確認

- prompt identity `the-caption-3ce91a4-validation-closure-r1`、bundle SHA-256 `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`を`verify_bundle`で検証済み。
- 監査対象の`SPEC`一行はroot `AGENTS.md`の正本と一致。live HEADは`2113ed247a0060f4b68846ced2188a420ff17ea8`。
- 六句は[`Candidate43 control element分類`](candidate43-control-element-classification.md)の原子要素へ次のとおり対応する。`S1=F1`、`S2=A1`、`S3=A2`、`S4=A3`、`S5=A4`、`S6=F2`。`S2..S5`はauthority readiness(A系)、`S1 / S6`はfixed operation(F系)である。

### 六句の証拠対応表

事実列と判定列を分け、推測・提案は本表に混ぜない。

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 増やす判断点 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- | --- |
| `S1` operation identity分割 + predicate / criterion owner / permission / constraint固定 | C54でoutcome単位だけへ縮めるとF10の段階的再判断が増えた | TaskSpecはoutcome / read / permissionを固定するが、初回predicate前に一つのoperationへpredicate / permission / constraintをbindする原子開始単位を固定しない | operation identity分割、初回predicate前binding | C61で原子`SPEC`を復元しA01 / A02は10 / 10 score `4`。ただしF10短経路は復元せず(model step `48 -> 60`) | `retain`(意味)。効率効果は未確定 |
| `S2` `spec_ready`を明示input / outcome値を直接要求する一意authorityへbind済みで成立 | C42 A01 5 / 5でcurrent value `daily`と選択肢`daily / strict`から`strict`を推測し、質問前に編集・試験へ進んだ | TaskSpecはrequired outcomeを列挙するが、値をbindする根拠の適格性(authorityの一意性と直接要求)を限定せず、repository stateがbind候補として残る | authority適格性のbinding判定 | C43 A01 5 / 5で編集・試験前に質問、A02 5 / 5でcanonical routeを解決 | `retain` |
| `S3` current value / option set / complement / test expectation / implementation convenienceをbindしない | C42の補集合推測(`strict = not daily`)を直接閉じたnegative boundary | repository stateはauthorityに見えるため、positive規則(`S2`)だけでは補集合推測を排除しない | negative list照合 | C43でA01の補集合推測が5 / 5で消失 | `retain`(`S2`と一体) |
| `S4` `spec_ready=false`の間はproducer binding / predicate実行 / artifact変更 / testを開始しない | C41 A01 5 / 5で未固定policyを推測して実行。C42で開始禁止を追加。C71 B18 A01では1件が未固定modeを確認せず実装・testへ進行 | TaskSpec / authority / stateはreadinessの真偽を計算できても、falseでの実行開始を抑止する状態遷移を持たない | readiness gateによる実行抑止 | C43 A01 5 / 5で停止。C71に残存失敗1件があり、gateは強化対象で削除対象でない | `retain`(強化側) |
| `S5` authorityからbindできない未固定値だけをclarification resultにする | C42は質問せず推測(過小)、対称にrepository解決可能な値まで質問する過剰もありうる | TaskSpecは質問対象集合を定義せず、全部質問と全部推測の両誤りが起こりうる | clarification範囲の限定 | C43 A01 5 / 5で未固定値だけ質問、A02 5 / 5で解決可能routeを質問しなかった | `retain` |
| `S6` result / constraint / terminalを同一operation identity内だけへbindし別operation / task全体へ伝播させない | C33で別operationの成立済みresponse失効と必須response欠落。C34が状態を分離 | TaskSpec / stateは各resultを保持するが、あるoperationの`false / failed`を別operationへ伝播させない境界を定めない | operation間の失効非伝播 | C34 targeted 10 / 10、expanded 58 / 60がscore `4`、C31比token中央値`-12.57%` | `retain`。ただしOWNER_ROLE `F8`と非伝播方向で重複 |

### Strict制御と実行効率の分離

- `S2..S5`のStrict境界はA01 / A02で成立を確認済みだが、C71 B18で`S4`の残存失敗(A01の未固定mode誤実装1件)が観測された。これは`VALIDATION_CLOSURE`の非適用域である仕様確定前へ検証が流入した事例で、`S4`を弱めれば悪化する。A01の未確認実装をtoken削減と相殺せず、`S4`は削除・短縮対象にしない。
- `S1`の効率効果は未確定である。C61は原子`SPEC`をC55へ完全一致で戻したが、F10短経路は復元せず(`43 -> 55 tool call`、`848,388 -> 1,048,829 tokens`)。短経路はpredicate成立ではなくsampling変動に依存する。したがって`S1`の分割・統合でtoken削減を主張できず、C61 runtime不通過を`S1 / S6`の意味が不要という証拠へ読み替えない。

### 重複・移動候補の検討

handoffが挙げた四関係を確認した。いずれも判断点を消さない。

- `S1`と`PRODUCER`: `S1`はoperation identityとspec値の確定、`PRODUCER`はそのoperationへproducer execution identityを一つbind(`F3`)。`S1`は`PRODUCER`の前提条件であり、同一predicateの重複ではない。削除候補にならない。
- `S6`とTERMINAL / OWNER_ROLE: `S6`(`F2`)は一般の失効非伝播、OWNER_ROLEの`false / failed`保持(`F8`)は同じ非伝播を特定状態へ適用したものである。分類表でも`F2 / F8`統合が候補だが、OWNER_ROLE監査は既にOWNER_ROLEを変更しないと結論済みで、`S6`は一般形として常時読むcoreに必要である。統合は常時読むcore内の再配置で、判断点を消さない。
- `S2 + S3`統合: 分類は`A2`を`A1`へmergeと分類するが、これは一文への表面圧縮であり意味削減ではない。negative list(`S3`)はC42の補集合推測を排除する動作本体で、positive規則だけへ縮めると境界を失う。表面圧縮はC65 / C66で短経路を安定再現しなかったため、新しい検証仮説にならない。
- criterion ownerの`SPEC`常時固定: criterion ownerはOWNER_ROLE `D1`でも常時「担当情報でありworker指定でない」と記述され、常時読むcoreに既に存在する。`S1`から外してもcoreから消えず、明示委譲時だけ別blockにする再提案はCandidate49で実行tokenを減らさなかった。移動して同じ判断を別labelで読むだけであり、削減候補にしない。

### 構造と表現過積載の切り分け

- 構造: `S2 / S3`(authority適格性 + negative boundary)、`S4`(readiness gate)、`S5`(clarification範囲)、`S6`(失効非伝播)は、それぞれC42 / C43 / C34の異なる保存済み誤経路へ一対一で対応する独立不変条件である。
- 表現上の過積載に見える点: `SPEC`は一labelにA系(readiness)とF系(operation scope)を同居させ、一label一不変条件の原則へ反する。しかし句単位では重複predicateがなく、分割はlabel参照を一つ増やすだけで判断点を消さない。過積載はlabel名の粒度の問題であって、削除可能な句の存在を意味しない。

### Candidate74の判断

`作成根拠なし`。

削除または置換する一つのpredicateを導けない。六句すべてが保存済み誤経路へ対応し、既存の重複(`S6 / F8`、`S2 / S3`、criterion owner)はいずれも常時読むcore内の再配置または表面圧縮で、消す判断点・context伝播を示せない。handoffのCandidate74作成前gate九項目のうち、項目5(削除・置換predicate)と項目6(消す判断点)を定義できないため、bundle / profile / evaluation setを作らない。

### 次に監査するlabel

`CONTEXT`(452 byte)。分類`D6`で9-field packet列挙の単独効果が未分離で、field列挙の多くがTaskSpec / allowed read / required evidenceと重複するという具体的な縮小仮説がある。`SPEC`と`OWNER_ROLE`はこの段階で変更しない。

## SPEC監査 追加調査: S4再現(#1)と短経路(#2)

### 目的と方法

`SPEC`監査の`作成根拠なし`結論に対し、根拠を生成し得る二調査を、いずれも**新規eval runを起こさず既存archiveの再解析だけ**で実施した。route(top-level tool call)はdocと同一のmetric、すなわち各runのroot rollout(`~/.codex/sessions`の生rollout)の`custom_tool_call + function_call`件数で数えた。B18 archiveのrollout取得はmissing 0 / 180。

一次調査で採用した`command_execution`(adapter event)はshell command数に近く、tool callをbatchすると短経路を隠す。metricを生rolloutへ訂正した結果だけを以下の結論とする。

### #1 S4ゲート破れの再現性(既存B18 N=90再集計)

| 対象 | N | score分布 | 実質S4破れ |
| --- | ---: | --- | ---: |
| C71 A01(VALIDATION_CLOSURE有) | 90 | `4`×89 / `0`×1 | 1 / 90 |
| C69 A01(baseline, 無) | 90 | `4`×89 / `1`×1 | 0 / 90(1件は採点偽陰性で実挙動は正答) |

- C71の破れ1件(`6fa0bce4`)はtoken 228,095で90件中4位(中央値の2.46倍)。ゲート破れ時に実装+testへ進む高コスト末端事象。
- 1/90は単発でC69 0/90との差は統計的に区別不能。B18の特徴づけどおり`VALIDATION_CLOSURE`非適用域(仕様確定前)への検証流入であり、`SPEC` S4固有の弱さの証拠にならない。`S4`は破れ側で、削除・短縮の禁忌が補強された。
- 判定: `S4`置換predicateの根拠は生成されない。

### #2 F10-monthly短経路はprompt駆動かsamplingか

標準14項目v12、`TC-F10-MONTHLY-FORMAT-TEST-REVIEW`、固定prompt各N=90(rollout metric):

| 対象 | 短経路率(≤6 call) | median | 分布 |
| --- | ---: | ---: | --- |
| C71(VALIDATION_CLOSURE有) | 93%(84/90) | 3 | {3:62, 4:20, 5:2, 7:1, 8:3, 11:2} |
| C69(baseline, 無) | 54%(49/90) | 4 | {3:30, 4:16, 5:1, 6:2, 7:7, 8:2, 11:31, 14:1} |

- C69→C71の唯一の差である`VALIDATION_CLOSURE`が、短経路率を54%→93%へ上げる。N=90の明確なprompt効果でありsamplingではない。C69は短経路(3-4)と長経路(11)へ二分、C71はほぼ短経路へ収束。B18のtool call削減(9,075→6,338)とF10-monthly token`-23%`の実体である。
- catalog-fixed条件(`outcome-quality-owner-diagnostic-v9`, targeted2)でも、13 prompt×N=5=65 runの29%が短経路で、C56 `[3,3,3,3,3]`・C62 `[3,3,1,1,2]`は全run短経路、C51・C61は全run長経路。短経路はprompt依存とrun間sampling変動の両方が効く。
- **atomic SPEC(S1)は短経路を生まない**。C61(atomic `SPEC`完全復元)はcatalog-fixedで`[11,11,11,11,11]`＝全長経路。短経路のレバーは`SPEC`のS1ではなく`VALIDATION_CLOSURE`(別label・凍結済み)である。

### 追加調査の結論

- #1・#2とも、フルcampaign(実API約60 run・9M token規模)を起こさず既存archive再解析で決着した。
- どちらも`SPEC`の削除・置換predicateの根拠を生成しない。short-pathの効率レバーは`VALIDATION_CLOSURE`であって`SPEC` S1ではないと定量的に確認され、`SPEC`監査の`retain`結論とCandidate74`作成根拠なし`が補強された。
- 副次的に、C71のKPI改善が`VALIDATION_CLOSURE`によるmodel再入削減である(本書冒頭の主張)ことを、F10-monthlyのroute分布(短経路率54%→93%)としてcase単位で定量化した。

## `CONTEXT`監査結果

### 結論

`CONTEXT`の三句はすべて保存済み根拠に対応し、削除predicateは現時点で導けない。ただし`SPEC`と異なり、A06診断が名指した未実施のpaired diagnostic(packet resolved premise)が、根拠を生成し得る定義済みの投資先として残る。Candidate作成根拠は現時点なし。

### identity確認

- 監査対象はCandidate71 root `AGENTS.md`の`CONTEXT`一行(452 byte)。bundle identityは`SPEC`監査と同一(`995481...58695`、検証済み)。
- `CONTEXT`はD系(明示委譲時のworker packet制御)であり、root-only taskでは発火しない。B18 / standard14は全runがroot-onlyのため、`CONTEXT`の実行効果はF07 multi-workerやA06のような委譲caseでのみ現れる。
- 三句は分類`D6 / D7`へ対応する。

### 三句の証拠対応表

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 増やす判断点 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- | --- |
| `X1` worker packetへ9 field(`criterion / owner / pass condition / TaskSpec該当範囲 / target identity / scoped diffまたはresult / required evidence / allowed read / forbidden input`)を固定 | C11は明示packet + sufficiencyで不要な全履歴継承を防いだが、9 field個々の単独効果は未確認。特定fieldの欠落による誤経路の保存traceはない | packetが無ければworkerはroot履歴やTaskSpecを自分で辿る。ただしfieldの一部(owner / pass condition / TaskSpec該当範囲)はTaskSpec参照と重複する | packet field固定 | C11でF07が必要2 workerを維持しつつ全spawn `fork_turns=none` | `review`(全体はretain、TaskSpec重複fieldの単独効果は未分離) |
| `X2` packet + allowed readで判定可能なら`fork_turns=none`、不足時だけ意味保持に必要な最小turn継承 | C10まではSA起動時に全会話履歴を継承し、不要なcontext反復inputが発生 | TaskSpec / allowed readは判定材料を定義するが、十分な場合に履歴継承を止める境界を持たない | 十分性判定 | C11: F07でC10比token中央値`-1,009,985`、60 / 60 score `4`。C33で境界を押し込みchild token`-48.53%`、C34が同境界維持で品質回復 | `retain`(token lever) |
| `X3` 利便性 / 念のため / 無関係tool outputの参照可能性を全履歴継承の理由にしない | 全履歴継承の常態化 | `X2`の否定境界。TaskSpec / stateは「念のための継承」を禁止しない | 継承理由の限定 | C11 / C33で`fork_turns=none`が成立 | `retain`(`X2`と一体) |

### Strict制御と実行効率の分離

- 効率leverは`X2 / X3`(sufficiency境界)である。C11のF07 `-1,009,985` tokenはこの境界の効果で、`X1`のfield列挙内容ではない。
- C33はこの境界をさらに押し込みchild token`-48.53%`を得たが品質が下がった。ただしC34のtrace確認で、F05 out-of-scopeとF10 inventoryの低scoreはresult-state(terminal response欠落)起因であり、context境界自体はC34で維持したまま品質を回復した。したがってcontext sufficiency境界の削減は品質低下の原因と切り分けられ、`X2 / X3`は削除・緩和対象にしない。

### 重複・移動候補と未実施investigation

`X1`の9 fieldには相反する二方向があり、いずれも保存traceで未決着である。

- 縮小方向: `owner / pass condition / TaskSpec該当範囲`はTaskSpec参照と重複する。分類`D6`は`未解決predicate / target identity / required evidence / allowed read / forbidden input`への縮小を候補にする。ただし特定fieldの欠落誤経路が保存traceにないため、これは`SPEC`のcriterion owner再配置と同型で、消す判断点を示せない。期待値は低い。
- 拡張方向: A06診断は、authority専任workerがauthorityを確定した後も各監査workerが担当findingに必要なauthority条項を直接再読し、rootもworker result採用前にsourceを再取得する現象を観測した。しかしA06はresolved premise(target identity / 適用authority集合と関連条項 / production surface / 確定済みcommand receipt)をmodel-visible入力として渡していないため、この再読が削減可能な情報境界欠陥か、独立判断とfinding admissionに必要な読取りかを判定できない。A06結果は、片方だけにresolved premiseを渡すpaired diagnosticを名指しで要求している。

拡張方向は、`SPEC`監査には無かった「保存観測に裏付けられた具体的investigation設計」である。ただし現時点では、観測された再読が必要な独立検証(`確定済みresultを再び問題にしない`原則の反対側)かもしれず、削減可能と確認されていない。

### 構造と表現過積載の切り分け

- 構造: `X2 / X3`(sufficiency境界と全履歴継承禁止)はC10→C11の実誤経路(不要な履歴反復input)へ対応する独立不変条件で、token leverでもある。
- 過積載に見える点: `X1`の9 field列挙。うちboundary制御field(`required evidence / allowed read / forbidden input`)と作業handle field(`criterion / target identity / scoped diff or result`)はworkerが担当判断に要するが、`owner / pass condition / TaskSpec該当範囲`はTaskSpec重複で、常時packetへ固定する単独根拠が弱い。ただし削除可能の証明ではない。

### Candidate判断

`作成根拠なし`(現時点)。

削除・置換する一つのpredicateを保存誤経路から導けない。縮小方向は消す判断点を示せず、拡張方向は再読が削減可能と未確認である。handoffのCandidate作成前gate九項目のうち、項目3(TaskSpec等で防げない理由)と項目5(削除・置換predicate)を今のtraceでは満たせない。

### 次の投資

`CONTEXT`をさらに進める場合の唯一の定義済み経路は、A06結果が要求したpaired diagnosticである。required outcomeを固定し、片方だけにresolved premise(target identity / 適用authority集合と関連条項 / production surface / 確定済みcommand receipt)を渡し、worker数・担当file・tool・読取り順は固定せず、成果品質とsource再取得だけを分離して観測する。これは新規A06 case variant + bundle + gate定義を要する別タスクであり、既存archiveでは答えられない。実施しない限り`X1`の判定は`review`のまま保持する。

補足: このpaired diagnosticは既存データで事前sizingもできない。multi-worker runのper-session rollout archive(candidate45 A06、candidate41 F07)はいずれもprune済みで、standard14 / B18は全runがsession_count=1(root-only)で`CONTEXT`が発火しない。A06診断はN=1・非登録で再読の除去可能率を単一条件からは判定できない、という元結果の制約もそのまま残る。

## `PRODUCER`監査結果

### 結論

single producerを作る`P1 / P2`は構造として保持する。明示委譲gateの短い再記述`P3`だけは`OWNER_ROLE`へ同じpredicateの正本があり、Candidate67で削除後の意味保持も確認済みである。Candidate74の作成前gateは、`P3`一文だけを`PRODUCER`から削除する変更として定義できる。bundle、profile、evaluationはまだ作らない。

### 五句の証拠対応表

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 重複または未分離 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- | --- |
| `P1` 初回predicate前に各operationへproducer execution identityを一つbind | C28が対象にしたroot / worker重複実行とworker不成立後のroot差替え | TaskSpecはoperationとownerを持てるが、実行runtimeのproducer identityを一意にbindしない | `SPEC`のoperation bindingをruntime executionへ接続する役割で、同じpredicateではない | C28 expanded 60 runは58件score `4`、2件score `3`。残存2件は独立owner operation不成立であり、single producerの重複実行ではない | `retain` |
| `P2` 同一operationのpredicate / resultを別producerへ順次・並行に割り当てない | C28以前のroot / worker重複実行とroot差替え | producer候補が複数存在してもTaskSpecは再割当て可否を定めない | `INDEPENDENCE`の同一predicate再割当て禁止と重複していたが、Candidate67は正本を`PRODUCER`へ残した | Candidate67は対象30 runでCandidate43と同じscore分布、D01 5 / 5で指定worker一つ、標準14は70 / 70 score `4` | `retain`(正本) |
| `P3` TaskSpecが独立producer executionを明示した場合だけ指定identityをbind | C41以前はcriterion owner語列をworker指定へ読み替え、F05 / F10で不要workerを起動 | owner語列とproducer execution指定はTaskSpec内でも別意味であり、変換可否をTaskSpecだけでは決めない | `OWNER_ROLE`にowner否定境界、TaskSpec明示gate、task identity binding、predicate前spawnを含む完全な正本がある | Candidate67は`PRODUCER`側の短い再記述を削除し、D01 5 / 5で指定worker境界を維持。標準14 70 / 70もscore `4` | `merge` into `OWNER_ROLE`。`PRODUCER`から削除可能 |
| `P4` criterion owner語列だけでproducerを選ばない | C35ではF05 / F10各5件で不要workerを起動し、C41で0件になった | ownerはnon-machine risk担当であり、producer execution指定ではない | `OWNER_ROLE`冒頭にも同じnegative boundaryがあるが、Candidate67は`P4`を残しており、この一文だけの削除は未確認 | C41は10 / 10 score `4`、worker 10件から0件、token合計`-51.97%`。ただし変更は`PRODUCER`と`OWNER_ROLE`を同時に整合させた | `review`。重要な意味は保持し、重複位置の削除は別predicate |
| `P5` producer変更は旧bindingを失効し、新identityのTaskSpecで行う | producer不成立後に同じoperationをroot resultへ差し替える経路 | TaskSpecは新identityを記述できるが、旧bindingをいつ失効させるかを自動では定めない | C28由来だが、この文だけのablationとproducer変更の正のcaseがない。`P1 / P2`へ統合できる可能性は未確認 | 現評価は通常経路か委譲開始時のproducer固定であり、正当なproducer変更を含まない | `review`。正のcase前に削除しない |

### 構造と試験対策的な重複

- 構造は`P1 / P2`である。一つのoperationが一つのproducerに属し、そのproducerだけがpredicateとresultを生成する。これはcase固有の正答ではなく、root / worker間の二重実行とresult差替えを防ぐ実行所有権である。
- `P3`の意味も必要だが、`PRODUCER`と`OWNER_ROLE`の二か所へ置く必要はない。Candidate67は正本を`OWNER_ROLE`へ残すだけでD01の指定worker境界を維持した。現在のCandidate71が同じ短文を再び`PRODUCER`にも持つ状態は、保存済み証拠上の構造ではなく重複表現である。
- `P4`も表面上は重複する。ただしC41は二labelを同時変更し、Candidate67も`P4`を残した。このため`P3`と一緒に削除せず、別の未分離predicateとして残す。
- `P5`は「失敗時もproducerを替えない」という`P2`のnegative pathと、「正当に替えるなら新operationにする」というpositive pathを一文で扱う。後者を試すcaseがないため、細かく見えることだけを理由に削除しない。

### Candidate74の作成根拠

`作成根拠あり`。ただし対象は`P3`一文だけである。

1. 基準prompt identityはCandidate71 `the-caption-3ce91a4-validation-closure-r1`とする。
2. 最短正常経路は、root-only operationではrootを一度bindし、明示委譲operationではTaskSpec指定workerだけをpredicate前に一度spawnする経路である。
3. 保存誤経路は、criterion owner語列をproducer指定へ読み替えたC35の不要worker起動である。
4. TaskSpecだけではowner metadataとproducer execution指定の変換可否を定めないため、明示委譲gate自体は必要である。
5. 削除predicateは、`PRODUCER`内の「TaskSpecが独立したproducer executionを明示した場合だけ、その指定identityをproducer role identityへbindする。」一文だけとする。
6. 消す判断点は、`PRODUCER`の短いgateと`OWNER_ROLE`の完全なgateの語差を照合する判断である。委譲可否の判断自体は消さない。
7. 新しい判断、参照、例外、labelは増やさない。`OWNER_ROLE`の正本と`P1 / P2 / P4 / P5`は逐語維持する。
8. quality、routing、required validationを維持し、root-only caseとD01のtool call、model step、all-agent tokenを記録する。runtime削減は事前に保証しない。
9. 不要worker、D01のworker欠落、root再読 / result再生成、required validation欠落、実質的品質後退が一件でもあれば停止する。意味を補う文は追加しない。

Candidate67は`P3`削除と`INDEPENDENCE`側の別重複削除を同時に行ったため、Candidate74にはそのbundleを継承しない。Candidate71から`P3`だけを削除し、`VALIDATION_CLOSURE`を含む現在の制御topologyで単独効果を確認する。

### 次の作業

Candidate74を作る場合は、上記九項目を独立した設計記録へ固定し、bundleの静的差分が`P3`一文だけであることを構造testで先に確認する。新しいEvaluation setやrating revisionは作らず、既存の互換D01正例とroot-only対象を使う。評価runはbundleとprofileのidentity確認後の別段階とする。

## `INDEPENDENCE`監査結果

### 結論

`INDEPENDENCE`の二句は`I1`(=`F9`)と`I2`(=`F4`)で、いずれも保存済み測定がある。`I2`はPRODUCER `P2`の重複でC67検証済み、`I1`はC68でF10-only削除を実測し品質中立だがruntime非改善でgate不通過。Candidate作成根拠なし。ただし`I1`のA / D scopeでの削除は未測定で、この点で監査は未完了。

### identity確認

- 監査対象はCandidate71 root `AGENTS.md`の`INDEPENDENCE`一行(193 byte)。bundle identityは既監査と同一。
- 現行句: 「先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する。同一predicateを別producerへ再割当てしない。」
- 第一文`I1`はC68が削除した`F9`一文と逐語一致。第二文`I2`はPRODUCER `P2`(=`F4`)と同一不変条件。

### 二句の証拠対応表

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- |
| `I1` 先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定(`F9`) | 先行result / artifactの独立確認を別operationとして事前bindせず、既存operationへ混ぜる | TaskSpec / stateは「先行成果を対象とする独立operationの事前binding」trigger自体を持たない | C68でF10-only削除→5 / 5 score `4`・root-only・zero drift維持、top-level tool call `40 -> 40`。ただしtoken中央値`+1.16%`・elapsed中央値`+26.04%`・token合計`+426`でgate不通過。**A / F追加scope / Dは未実行** | `review`(F10で保持、A / D未測定) |
| `I2` 同一predicateを別producerへ再割当てしない(`F4`) | 同一predicateの別producer再割当て | PRODUCER `P2`と重複。INDEPENDENCE内の再記述 | C67でcross-label dedupを検証(品質・runtime中立)。C68でも本文は保持 | `merge`(PRODUCER側で保持) |

### Candidate判断

`作成根拠なし`。

`I2`はPRODUCER `P2`の重複でC67検証済み(中立)。`I1`はC68がF10で削除を実測し、品質は中立だがtool cycleを短縮せずruntimeを改善しなかったため、削除の効率根拠がない。C68自身が「F9を一般に削除可能とは判断しない」とし、次はF9でなく`F5`を対象にと記録している。したがって現時点で削除・置換predicateを導けない。

### 監査状態: 未完了(I1のA / D未測定)

`I1`削除はF10-onlyでしか測っておらず、A系・D系での品質と経路は未測定である。分類の`F9`判定「常時制御からの削除可能性はF10内に限定して保持する」と一致する。この未測定を埋めるにはA / D caseでのF9削除評価(fresh run)が要る。ただしF10で既にruntime非改善が出ており、C68も次対象をF5へ移しているため、flip見込みは低い。

## `TERMINAL`監査結果

### 結論

`TERMINAL`の二句(`T1=F6`、`T2=F7`)は、C30で観測した「terminal resultを待たず最終応答で完了宣言する」実失敗へ直接対応し、C31 targetedで再発しなかった。単一目的labelで削除・置換predicateはなく、Candidate作成根拠なし。未実施の再測定もなく監査完了。

### identity確認

- 監査対象はCandidate71 root `AGENTS.md`の`TERMINAL`一行(287 byte)。bundle identityは既監査と同一。
- 分類でも`TERMINAL`は`F`単一目的(287 byte)とされ、`T1=F6`、`T2=F7`に対応する。

### 二句の証拠対応表

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- |
| `T1` 全predicateにbind済みproducer terminal resultがある場合だけterminal(`F6`) | C30 continuousで、非同期処理が「受付済み」を返した後にterminal resultを待たず最終応答で完了を宣言する実失敗2件 | TaskSpecはstop conditionを定めるが、全predicateのterminal result充足を完了の必要条件として強制する状態機械を持たない | C31 targeted(F06 empty snapshot / F07 canonical / F07 dependency)15 / 15 score `4`、premature completion再発せず | `retain` |
| `T2` nonterminal / result欠落ならnonterminalに保ち、進行報告 / 集約結果 / final responseで補完しない(`F7`) | 同じ実失敗の否定側。欠落したpredicate resultを応答で補完 | 同上 | C31 15 / 15で応答による補完を観測せず | `retain`(`T1`と一体) |

### Candidate判断と監査状態

`作成根拠なし`、監査`完了`。

- 両句とも単一目的で、C31の実失敗へ一対一対応する。case固有・command固有の条件は本文にない。
- cross-label重複は「`OWNER_ROLE`が応答補完禁止(`F7`)と`false / failed`保持(`F8`)を再記述」だが、正本の所属は`TERMINAL`側が自然で、`OWNER_ROLE`監査で不変更確定済み。`TERMINAL`側から消す判断点はない。
- 留意: C31はprompt変更とcollector v2を同一campaignで評価したため両者の寄与率は未分離だが、防いだ誤経路(premature completion 2件)は明確で、audit判定(誤経路対応の有無)には影響しない。KPI寄与の分離はaudit要件ではない。
- 未実施の再測定はなく、`OWNER_ROLE` / `SPEC`と同じ完了扱いとする。

## `ROOT`監査結果

### 結論

`ROOT`の一句(`D5`)はC28の誤経路(非producer rootによるresult再生成 / predicate再実行)に対応し保持。`F3`への統合候補だが中立relocationで消す判断点はない。Candidate作成根拠なし、監査完了。

### 証拠対応表

- 監査対象: `ROOT`一行(160 byte)。分類`D5`対応、D系(明示委譲時のみ発火、root-only taskでは不使用)。

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- |
| `D5` rootがproducerでないoperationではpacket構築 / result binding / terminal集約だけを行い、predicate実行 / result再生成をしない | C28: root / worker重複実行と、worker不成立後にrootがresultを差し替える経路 | TaskSpecは非producer rootの役割境界(集約のみか再生成可か)を定めない | C28で対象化。C38 / C40ではroot / child重複readを単独では止めなかった(別挙動) | `retain`(`F3`統合候補、中立relocation) |

`D5`削除・置換predicateは導けない。`F3`へのmergeはC67型の中立relocationで、消す判断点を示せない。C28誤経路対応は明確で、未実施の再測定もなく完了。

## `DECISION_BOUNDARY`監査結果

### 結論

`DECISION_BOUNDARY`は単一句のmodel再入削減制御で、C69がtool call`-26.60%`・token`-22.59%`・品質中立(F10 location score `3` 1件はC43でも出る共有事象)を実測した。削除predicateはなく(効率lever本体)、Candidate作成根拠なし、監査完了。

### 証拠対応表

- 監査対象: `DECISION_BOUNDARY`一行。C43分類には無い後発label(C69 `model-reentry-decision-boundary`由来)。

| 句 | 消す判断点 / 防ぐ経路(保存trace) | TaskSpec等で防げない理由 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- |
| `decision_boundary`を持たない既知の相互非依存invocationを同一model stepで発行し、全result受領後に一度だけ判断 | C43 baselineは独立invocationごとにmodelへ戻り、top-level tool callが多い(639) | TaskSpecはinvocationのbatch境界(どこでmodelへ戻るか)を定めない | C69標準14 70 / 70: top-level tool call `639 -> 469`(`-26.60%`)、token`-22.59%`、shell commandは`-2.27%`のみ(必要作業は維持)、品質中立 | `retain` |

削除・置換predicateなし。効率lever本体で、削除すればmodel再入が増える。`VALIDATION_CLOSURE`(凍結)はvalidation phaseへの特化で、`decision_boundary`が成立しない検証集合を`validation_set_ready`で扱う相補関係であり重複ではない。未実施の再測定なし、完了。

## `METHOD`監査結果

### 結論

`METHOD`の四句(`M1..M4`)は手段選択とpermission境界で、C23の早期停止誤経路に対応する。単一目的でcross-label重複なし。Candidate作成根拠なし、監査完了。

### 証拠対応表

- 監査対象: `METHOD`一行。分類`M1..M4`対応、単一目的(method selection)。

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 判定 |
| --- | --- | --- | --- |
| `M1`+`M2` TaskSpec明示手段だけ固定し、未固定手段はpermission内でexecutorが選ぶ | 未指定手段を「禁止」と誤読して手を止める | TaskSpecは「未指定 = 禁止ではない」を明示せず、F04 cleanupの代替手段を閉じ得る | `retain`(`M1`は`M2`へmerge) |
| `M3` invocationのfailed / unavailableをpermission否定 / terminalにせず、未固定手段があれば継続 | C23: 手段失敗をterminal扱いして早期停止 | TaskSpecは手段失敗と停止条件を分離しない | `retain` |
| `M4` 明示禁止 / permission否定は停止し、回避しない | permission境界の逸脱(禁止手段への迂回) | permission境界の逸脱防止 | `retain` |

削除・置換predicateなし。`M1`は`M2`への統合候補だが中立。未実施の再測定なし、完了。

## `RECOVERY`監査結果

### 結論

`RECOVERY`の二句(`R1 / R2`)はcounter誤消費を防ぐが、現Evaluation setは`environment_recovery_max=0`または`not_applicable`で、正のrecovery cycleを一度も観測していない。効果が未測定のため監査は未完了。Candidate作成根拠なし。

### 証拠対応表

- 監査対象: `RECOVERY`一行。分類`R1 / R2`対応。

| 句 | 意図する制御 | 現状の観測 | 判定 |
| --- | --- | --- | --- |
| `R1` `environment recovery := environment-only repair + same required command rerun` | environment障害の同一command再試行を一組として扱う | C10 / C23由来。F05 / F10では`not_applicable` | `review`(recovery適用caseで別判定) |
| `R2` 組の開始時だけ`environment_recovery_max`を消費し、未固定手段の選択は数えない | method choiceによるcounter誤消費を防ぐ | 現対象caseでの効果は未測定 | `review`(`R1`と同時判定) |

### 監査状態: 未完了(効果未測定)

`R1 / R2`は削除も保持も現データでは確定できない。「証拠不足」は不要の証明ではなく、常時coreへ残す根拠も外す根拠も無い状態である。埋めるには`environment_recovery_max>0`の正のrecovery scenario caseを含むfresh evalが要る。flip見込みは不明(未測定)。

## 監査状況の分類(完了と再測定要の分離)

`作成根拠なし`と`再測定が必要`は別状態である。後者は監査未完了であり、完了に数えない。現時点の分類は次のとおり。

| label | Candidate根拠 | 監査状態 | 未完了なら必要な再測定 | 再測定が結論をflipし得るか |
| --- | --- | --- | --- | --- |
| `OWNER_ROLE` | なし | 完了 | — | — (relocationはC49で測定済み) |
| `SPEC` | なし | 完了 | — | — (#1 S4・#2 短経路を既存データで解決。criterion ownerは論証でrelocation判定) |
| `TERMINAL` | なし | 完了 | — | — (T1 / T2ともC31 targeted 15 / 15で誤経路対応済み。単一目的) |
| `ROOT` | なし | 完了 | — | — (D5はC28誤経路対応。F3統合は中立relocation) |
| `DECISION_BOUNDARY` | なし | 完了 | — | — (C69で効率lever実測、品質中立。削除は再入増) |
| `METHOD` | なし | 完了 | — | — (M1..M4はC23早期停止誤経路対応。単一目的) |
| `CONTEXT` | なし(暫定) | **未完了** | `X1`: A06 paired diagnostic。新規A06 case variant + bundle + gate + fresh run。既存archiveでは事前sizingも不可 | **あり**。拡張方向(packet resolved premiseで再読削減)は未検証で、削減可能なら根拠になり得る |
| `PRODUCER` | **あり(P3のみ)** | 作成前gate定義済み・bundle未作成 | Candidate74で`P3`一文だけをC71から削除し、D01正例 + root-onlyでtargeted評価(未実施)。詳細は上記`PRODUCER`監査結果節 | — (P5は別途`review`保留、正のproducer変更case前に削除しない) |
| `INDEPENDENCE` | なし | **未完了(I1のみ)** | `I1`(=`F9`): A / D scopeでの削除評価。C68はF10-onlyのみ実測でun-run | 低い。F10で既にruntime非改善、C68も次対象をF5へ移した |
| `RECOVERY` | なし | **未完了** | `R1 / R2`: `environment_recovery_max>0`の正のrecovery scenario caseでの評価。現Evaluation setは`not_applicable`でun-run | 不明(効果未測定) |
| `VALIDATION_CLOSURE` | — | 凍結 | — | — |

- 完了(根拠なし・再測定不要): `OWNER_ROLE`、`SPEC`、`TERMINAL`、`ROOT`、`DECISION_BOUNDARY`、`METHOD`(6)。
- 作成根拠あり: `PRODUCER`(`P3`一文削除のCandidate74作成前gate定義済み、bundle未作成)(1)。
- 未完了(根拠なし判定は暫定、再測定が残る): `CONTEXT`(結論をflipし得る)、`INDEPENDENCE`(I1句のみ、flip低)、`RECOVERY`(効果未測定、flip不明)(3)。
- 凍結: `VALIDATION_CLOSURE`(1)。11 labelすべてを分類した。
- 11 label中、Candidate作成根拠があるのは`PRODUCER`の`P3`一文削除だけである。他10 labelは根拠なし(完了6・暫定未完了3・凍結1)。未完了3 labelの再測定はいずれもfresh runを要し既存データでは決着しない。`PRODUCER`以外の不変更方針を維持し、`P3`削除Candidate74はbundle・profile・評価を別段階とする。
