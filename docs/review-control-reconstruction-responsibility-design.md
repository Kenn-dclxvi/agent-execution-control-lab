# review制御再構成の責務設計

> **位置づけ**: M3具体的反例、Candidate189・190・191の後続反例およびCandidate192発行遷移失敗を反映したM2設計記録。Candidate193後の現在解釈は末尾注記を参照する

## 結論

review制御とそれを支える共通execution coreを、次の11責務へ再構成する。

1. operation specification
2. producer binding
3. review requirement
4. review execution permission
5. packet formation
6. dispatch transition
7. observation result
8. review judgement
9. result admission
10. result effect and invalidation
11. artifact change and outer terminal

各状態遷移は一つの責務だけが所有する。review要否、permission、packet、発行集合、観測、judgement、result受入、失効、artifact変更許可および外側terminalを一つの`admission`、`record`または`proof`へ縮約しない。発行資格の論理判定と実際のtool-call発行も別責務にせず、`DISPATCH_TRANSITION`の一つのterminal遷移として扱う。

C147の不変条件は責務へ再配置するが、13条項の本文、条項数、順序または語列は保持条件にしない。新しい汎用schema、registry、canonical locator、全入力分類mapまたはreview admission専用workerは作らない。実装時の条項数とprompt量はM8で測る結果であり、本設計の入力制約にしない。

この設計はCandidate本文ではない。Candidate192後の限定M3では方向を変える具体的反例が0件となったが、Candidate bundleは未作成であり、ADR9またはStandard14のrunも発行していない。

## Candidate実装topology

Candidate bundleは親promptをruntimeで暗黙継承しないfull bundleである。したがってCandidate本文は、歴史的Candidate identityまたは「既存経路」という外部参照なしに、review非適用の通常operationも実行できる自己完結した制御でなければならない。

実装は次の二層を同じ本文内に持つ。

1. 共通execution core: operation specification、producer binding、producer result、operation terminal、全worker context、evidence admission、dispatch transition、result effect、validation、methodおよびrecovery
2. review責務: review requirement、review execution permission、review packet、observation result、review judgement、review result admissionおよびchange admission

この二層は別promptを参照する継承関係ではない。review責務は共通coreの`implementation_bound`、producer、terminal、worker packetおよびresult effectを入力として使うが、それらを再定義しない。共通coreもreview固有terminalを推測しない。review非適用では共通coreだけが作動する。

一つの条項へ全lifecycle evidence admission、review observation stateおよびimplementation bindingを同居させない。全worker packetとreview固有packetも分ける。各C147不変条件は新本文内の一つの正本へ移し、Candidate本文に`C147`その他の歴史的Candidate identityを書かない。

## 適用範囲

本設計が追加で扱うのは、C147の`implementation_bound=true`へbindされた変更predicateについて、独立reviewが必要か、そのresultがartifact変更を許可または禁止できるかを決める範囲である。

ただし、TaskSpecまたは適用中repository authorityが、現在subjectへ独立review criterion、許可result kindおよびresult consumerを直接固定している場合だけ本設計を適用する。review契約のない通常の変更へ、open boundary、non-machine risk、owner語列または`finite_direct_match=false`だけを理由にreviewを新設しない。その場合は`review_requirement=not_applicable`として自己完結した共通execution coreだけを適用する。

次は本設計の外に置き、C147から保持する。

- required outcomeが未固定な場合のclarification
- implementation choiceをrepository authorityから解決する変更前evidence
- artifact変更後のvalidation plan、個別result、順序およびclosure
- method failureとpermission denialの区別
- environment-only recovery
- review以外のread-only operationおよび別required outcome

review制御のためにこれらを再定義せず、review resultを別operationまたはtask全体へ伝播させない。

## 制御対象

### operation

一つの変更predicateに対して、必要な場合だけ次のoperationを形成する。

| operation | identity | producer | terminal result |
|---|---|---|---|
| 外側admission | `admission(subject)` | root | `change_path_ready | blocked | unavailable` |
| 独立review | `review(subject)` | bind済み独立reviewer | `counterexample_found | no_counterexample_found | unavailable` |
| 観測 | `observe(atom)` | review producer。tool invocationは観測源でありproducerではない | `value | missing | unreadable | terminal_failure` |
| artifact変更 | C147へbind済み変更operation | C147でbindしたproducer | scoped change result |
| validation | C147へbind済みvalidation operation | C147でbindしたproducer | 個別validation result |

`review(subject)`は`review_requirement=required`かつ`review_execution_permission=allowed`の場合だけ形成する。permission否定時にはreview operation、packet、producer binding、spawnまたはdeliveryを作らない。この場合の`unavailable`は、存在しないreviewerの代行resultではなく、rootがproducerである外側`admission(subject)`のterminal resultである。

現在subjectへadmissibleかつactiveな保存済みreview resultがbind済みの場合は、新しい`review(subject)`を形成せずそのresultを使う。`review_execution_permission`は新しいreview executionの作成・起動permissionであり、保存済みresultの`result_use_permission`を兼ねない。

### subject

`subject`は、C147の`implementation_bound=true`が一つの実行可能な変更predicateとしてbindしたidentityとする。

- 一predicateが複数target、複数effectまたはartifact間relationを含んでも一subjectのままとする。
- C147が複数predicateを別々にbindした場合だけ複数subjectとする。
- target数、field数、artifact数、open classまたはreview都合からsubjectを再分解しない。
- 複数subjectを同じartifact変更invocationへ含める場合、全subjectの変更許可と全relation保持を必要とする。

### observation atom

`observation_atom`は、review判断が参照できる最小の観測result単位であり、次を持つ。

```text
observation_atom :=
  observation identity
  + target identity
  + 値を使うpredicate identity
  + producer identity
  + invocation result identity
  + invocation result contract identity
  + terminal state
```

terminal stateは`value | missing | unreadable | terminal_failure`のいずれか一つである。

- 対象を正常に観測して不存在だった場合は`missing`とする。
- invocation自体が結果を返せなかった場合は`terminal_failure`とする。
- permission否定はobservation stateにしない。
- rootの推測、reviewerの宣言だけ、別observationの成功またはaggregate exit codeからatomの`value`を生成しない。

## 責務と状態遷移の所有者

| 責務 | 所有する状態遷移 | owner／producer | 所有しないもの |
|---|---|---|---|
| `OPERATION_SPEC` | operation identityとdependencyの`unbound -> ready` | root | producer result、review judgement、artifact変更 |
| `PRODUCER_BINDING` | operation producerの`unbound -> bound`とproducer変更時の旧binding失効 | root | owner語列の意味、result内容、terminal補完 |
| `REVIEW_REQUIREMENT` | subjectの`unbound -> not_applicable | not_required | required` | root | permission、packet、review terminal |
| `REVIEW_EXECUTION_PERMISSION` | required subjectの新規review実行permissionの`unbound -> allowed | denied` | rootがTaskSpec／authority resultをbind | 保存result利用permission、method failure、reviewer不在result |
| `PACKET_FORMATION` | packetの`unbound -> ready | unavailable` | root | observation値、review judgement |
| `DISPATCH_TRANSITION` | consumerを持つ発行可能invocation集合の`unbound -> frontier_bound -> issued -> collected`、空集合の`unbound -> no_dispatch` | invocationを発行する現在producer | evidence資格、result意味、別invocationへのresult統合 |
| `OBSERVATION_RESULT` | atomの`unobserved -> value | missing | unreadable | terminal_failure` | atomへbind済みproducerの実result | 別atomのstate、review terminal |
| `REVIEW_JUDGEMENT` | review operationの`nonterminal -> counterexample_found | no_counterexample_found | unavailable` | bind済み独立reviewer | outer terminal、artifact変更 |
| `RESULT_ADMISSION` | review resultの`unchecked -> admitted | inadmissible` | rootの機械照合 | reviewerの意味判断の再実施 |
| `RESULT_EFFECT` | admitted resultの`active -> invalidated`と未発行operationへの効果投影 | root | 新しい意味resultの生成 |
| `CHANGE_TERMINAL` | `change_permission=unbound -> allowed | denied`と外側operationのterminal | rootおよびC147へbind済み変更・validation producer | review resultの再採点 |

一つの状態遷移を複数責務が所有しない。とくに`missing`は`PACKET_FORMATION`、`OBSERVATION_RESULT`、`REVIEW_JUDGEMENT`で別の意味に読み替えない。packetはidentityが揃っていれば値の`missing`を含んだままreadyとなり、reviewerだけがそのmissingがどのterminal dependencyへ効くかを判断する。

## 状態遷移

### 1. operation specification

```text
operation_spec_ready(o) :=
  predicate identityが固定済み
  ∧ permission sourceが固定済み
  ∧ required result kindが固定済み
  ∧ result consumerが固定済み
  ∧ 先行operationとのdependencyが固定済み
```

独立reviewを候補にする場合は、TaskSpecまたは適用中authorityが固定するreview criterion、allowed result kind、result consumerおよびexecution independence requirementもoperation specificationへbindする。これらがないことを一般的risk判断で補完しない。

外側admission、独立review、観測、artifact変更、validationは別operation identityを持つ。別operationのresultを同一operationの進行報告やroot宣言で補完しない。

### 2. producer binding

各operationは初回predicate実行前に一producerへbindする。TaskSpecが独立reviewをrequired outcomeとして要求した場合だけ、一般設計producerと異なるexecution identityを`review(subject)`へbindする。criterion owner、risk、role、artifact作成者またはreviewの有用性はproducerを決めない。

review permissionが否定されている場合は`review(subject)`自体を形成しないため、review producerもbindしない。外側`admission(subject)`はroot producerのまま`unavailable`を形成できる。

### 3. review requirement

review適用可否、review要否、新規review execution permissionおよび保存result利用permissionを一状態へ統合しない。

```text
review_control_applicable(subject) :=
  TaskSpecまたは適用中repository authorityが
  現在subjectへ独立review criterion、allowed result kind、
  result consumerおよび必要なexecution independenceを直接固定済み
```

```text
finite_direct_match(subject) :=
  現在設計より前に固定された一意なTaskSpecまたは適用中authorityが
  subjectの全target identity、全effect、各end stateまたはtransform、
  全保持constraint、全artifact間relationおよび集合の全件性を直接固定
  ∧ 既存のmachine-bound resultだけから、C147へbind済み変更predicateが
    同じidentityと値へ過不足なく一致すると判定可能
  ∧ 追加の選択、除外、探索、fallback、normalizationまたは完全性判断がない
```

```text
review_requirement(subject) :=
  not_applicable  if review_control_applicable(subject)=false
  not_required    if review_control_applicable(subject)=true
                    and finite_direct_match(subject)
  required        otherwise
```

review contractが適用済みで、authorityがない、closure identityがない、値が未固定、open boundaryへ依存する、relationの一致にnon-machine判断が必要、または対応を推論しなければならない場合は`required`とする。推論したgraph、現在target数、検証成功、witness不在、形成可能なreview resultまたはimplementation convenienceから`not_required`を作らない。

`not_applicable`ではreview permission、packetまたはreviewerを作らず、同じCandidate本文内の共通execution coreを維持する。`not_required`でもreview permission、packetまたはreviewerを評価せず、artifact変更許可判定へ進む。

### 4. review permissionとoperation形成

`review_requirement=required`の場合、最初に現在subjectへbind済みの保存済みreview resultが`RESULT_ADMISSION`と`RESULT_EFFECT`を満たすか確認する。admissibleかつactiveなら、新しいreview executionを作らずそのresultをartifact変更許可へ渡す。

admissible、activeかつ`result_use_permission=allowed`の保存済みresultがない場合だけ、現在subjectの新規review execution permissionをbindする。

```text
review_operation_ready(subject) :=
  review_requirement=required
  ∧ activeなadmitted prior review resultがない
  ∧ review_execution_permission=allowed
  ∧ review operation identityが固定済み
  ∧ 独立producerがbind済み
  ∧ packet_ready
```

新規review permission否定かつactiveな保存済みresultがない場合はreview一式を作らず、外側admissionだけを`unavailable`にする。新規review permission否定は、同じsubject、criterion、packet basis、producer identityおよびdependencyへbind済みのactive resultを失効させない。tool起動失敗、producer method失敗、観測targetのmissingまたはreviewerの`unavailable`をpermission否定へ読み替えない。

### 5. packet formation

```text
packet_ready(subject) :=
  TaskSpec該当範囲が固定済み
  ∧ subjectと保持constraintが固定済み
  ∧ semantic design inputが固定済み
  ∧ 適用authorityと規範predicateが固定済み
  ∧ review scope identity集合が固定済み
  ∧ observation identity、target、allowed read、success conditionが固定済み
  ∧ forbidden inputが固定済み
  ∧ allowed result kindが固定済み
```

packetは評価case、private oracle、期待terminal、過去finding、旧Candidate、修正案、実装後diffまたは禁止履歴を含めない。許可artifactの一部だけがsemantic inputなら、そのprojectionだけを入れる。

observation targetが存在すること、readが成功すること、全atomが`value`になることは`packet_ready`の条件ではない。identity自体が未固定、semantic projectionを作れない、permission内のallowed readを固定できない、または禁止情報を分離できない場合だけpacketを`unavailable`にする。この`unavailable`はroot producerの外側admission resultであり、reviewer resultではない。

### 6. dispatch transition

evidence資格を得たことだけではinvocationを発行しない。各発行cycleのtool callより前に、現在producerは候補invocationごとにconsumerと未解決dependencyを固定する。

```text
dispatch_candidate(i) :=
  iが未発行
  ∧ iのevidenceまたはrequired command資格が成立
  ∧ i.requested_resultを消費するbind済みoperationがnonterminal
  ∧ requested_resultがそのconsumerの未確定predicate、target、permission、method、
    stop conditionまたはterminal stateの少なくとも一つをbind可能
```

開始identityまたは開始状態がTaskSpecに明示されていること、drift可能性、一般的安全確認、許可済みreadの存在または進捗報告上の有用性はconsumerを作らない。

```text
dispatch_predecessor(i, j) :=
  j.resultが未受領
  ∧ j.resultがiのtarget、permission、method、stop condition、
    requested result contractまたは発行可否を変え得る

dispatch_frontier :=
  現在producerが同一model responseから個別tool callとして発行可能な
  全dispatch_candidate iのうち、未解決dispatch_predecessor(i, j)がない集合
```

operation identity、lifecycle、predicate、consumerまたはresult格納先が異なることだけでは`dispatch_predecessor`を作らない。先行identityのdriftがartifact変更だけを禁止し、固定済みreadのtarget、permission、method、result contractまたは発行可否を変えない場合、そのidentity確認とreadは同じfrontierへ入る。drift時にread自体が禁止されるかread target等が変わり得る場合だけ、readは次cycleへ置く。

```text
dispatch_transition_terminal(frontier) :=
  frontierが空なら、現在responseからtool callを一件も発行せずno_dispatch
  otherwise、現在responseのtool-call集合がfrontierの全identityと一対一一致
  ∧ frontier外のinvocationを含まない
  ∧ 各invocationを個別result contractを持つ別tool callとして発行
  ∧ 全invocationがterminal resultを返すまでmodel判断を再開しない
  ∧ 各resultを元のinvocation identityとconsumerへbind
```

frontierの一部だけを発行してresultをmodelへ返し、残りを次responseから発行してはならない。共同発行をshell compound command、wrapper内の一aggregate resultまたは一tool callへ統合してはならない。明示された同時発行上限または利用可能toolのため同じresponseから発行不能なinvocationはfrontierへ入れず、上限未固定を理由に任意の一部集合を選ばない。上限内で複数のfrontier候補がある場合は、TaskSpecで固定された順序、なければoperation specificationで固定した順序から決定し、result受領後に都合よく選び直さない。

tool callがcell ID付きnonterminal resultを返した場合、そのinvocationは未収集のままである。同じcell IDへのwait以外のtool、判断、commentaryまたは別cycleを先に発行しない。一invocationのfailed resultは同cycleの他invocationから受領済みの個別resultを失効させず、各consumerのdependencyに従って次cycleまたはterminalを決める。

### 7. observation issuance and atomicity

evidenceは、未確定review predicateと現在欠けている観測値へ直接bindできる場合だけ発行する。

```text
observation_consumer_ready(atom) :=
  review operationがnonterminal
  ∧ atom.state=unobserved
  ∧ atomが閉じ得るpredicate identityが固定済み
  ∧ requested resultがそのpredicateをbind可能
```

相互非依存のready atomは`DISPATCH_TRANSITION`が同じmodel responseから発行する。ただし、実行方法の自由はresult統合の自由を意味しない。

```text
observation_integration_allowed(atom_a, atom_b) :=
  一つのinvocation resultが各atomへ個別terminal stateを直接返す
  ∧ 一atomのnon-valueまたはinvocation failureが他atomの取得済みstateを消さない
  ∧ 適用中のinvocation result contractが、aggregate statusがnon-successでも
    個別success stateをauthoritative resultとして保持すると固定する
```

この条件を満たさないatomは別invocationとして発行する。per-item stateが見えても、aggregate failure時の有効性をresult contractが固定していなければ個別successへ昇格しない。tool、command、read数または順序は固定しないが、一つのaggregate exit codeしか返さないcompound invocationへ独立atomを束ねない。これにより、C176で観測した「具体的反例の成功観測と無関係なmissingを一resultへ束ね、両方を失敗扱いする」経路を閉じる。

一方、実invocationなしにsuccess receiptを昇格しない。これによりC177型の未観測receipt昇格を閉じる。

### 8. review judgement

reviewerはpacketと許可されたobservation resultだけから一terminal resultを形成する。

#### `counterexample_found`

```text
counterexample_certificate_ready :=
  concrete witnessがvalueとして観測済み
  ∧ witness applicabilityを決める規範predicateと全入力がvalue
  ∧ witnessがpositive applicabilityを満たす
  ∧ 固定設計上の処遇との直接矛盾が成立
  ∧ 解消に一般設計のtarget、rule、permission、methodまたはstop condition変更が必要
```

certificateは、上記成立に実際に使ったobservation resultだけをdependencyに持つ。certificate外のatomが追加witness数だけを変える場合、そのatomの`missing`、`unreadable`または`terminal_failure`は成立済みcertificateを失効しない。witness applicability自体を変え得るatomがnon-valueならcertificateは成立せず、`unavailable`を判定する。

#### `no_counterexample_found`

```text
no_counterexample_certificate_ready :=
  発行時に固定した全review scope identityがreview済み
  ∧ 固定manifestの全observation atomがauthenticなvalue
  ∧ 全規範predicateを適用して具体的counterexample certificateが成立しない
```

未来の全instance不存在、open classの永続閉包または一般設計の普遍的真理は要求しない。一方、固定manifestの一atomでも`missing | unreadable | terminal_failure`なら`no_counterexample_found`へ進まない。

#### `unavailable`

```text
review_unavailable_ready :=
  counterexample_certificate_ready=false
  ∧ no_counterexample_certificate_ready=false
  ∧ 未解決predicate identityが固定済み
  ∧ そのpredicateを閉じ得るdependency atomとnon-value stateが固定済み
```

open boundaryというlabel、一般的不確実性、reviewerの慎重さ、packet外の未知または追加反例の可能性だけでは`unavailable`にしない。

reviewerは`counterexample_found`を形成できた時点で、certificate dependencyを変えない未発行observationを失効する。counterexampleが成立しない場合だけ、固定scope全体の`no_counterexample_found`を判定する。これはterminal値の一般的優先順位ではなく、存在証明が成立した後に全域証明を続けないという証明責務の順序である。

### 9. result admission

rootはreviewerの意味判断を再実施しない。current review resultとsaved prior review resultを別predicateで機械照合する。

```text
current_review_result_admissible(result) :=
  result.operation_identity == current bound review operation identity
  ∧ review_execution_permission=allowed
  ∧ result.producer_identity == 対応operationへbind済みのreview producer
  ∧ sender identityがproducer bindingと一致
  ∧ result kindがallowed result kindに含まれる
  ∧ 参照するobservation resultが実在しauthenticかつcurrent
  ∧ terminal kindに必要なcertificateが揃う
  ∧ forbidden inputを根拠に含まない
```

```text
prior_review_result_admissible(result) :=
  TaskSpecがresult.operation_identityをprior review resultとしてadmit可能
  ∧ result_use_permission=allowed
  ∧ 現在subject、review criterion、allowed result kind、packet basis、
    producer identityおよびdependencyが保存resultと一致
  ∧ result_still_valid=true
  ∧ producer、sender、observation、certificateおよびforbidden input条件が成立
```

current review resultへ別の`result_use_permission`を追加要求しない。新しいreview execution permissionはsaved prior result admissionの条件にしない。

rootはcanonical locator、再構成した集合順、文字列表現または独自のsemantic projectionを作ってreviewer resultと完全一致させない。意味真正性は、bind済みproducer、許可入力、実observation result、certificate dependencyおよびterminal kindの対応で確認する。

inadmissible resultを別producerへ再割当てせず、同じresultをrootが補完しない。methodまたはenvironment failureで同じreview predicateを継続できる場合だけ、C147の`METHOD`と`RECOVERY`に従う。

### 10. result effect and invalidation

```text
result_dependency_set(result) :=
  resultが参照するsubject identity
  + review criterion identity
  + review scope identity
  + certificate形成に使ったobservation result identity集合
  + saved prior resultの場合だけresult use permission identity
```

新規reviewの作成・起動だけを制御する`review_execution_permission`は、保存済みresultのdependencyへ入れない。保存resultの利用可否を変える`result_use_permission`、subject、criterion、scopeまたはcertificate dependencyが変わった場合だけ、そのresultを失効またはinadmissibleにする。

```text
result_still_valid(result) :=
  result_dependency_set内のidentityまたはvalueを変えた新resultがない
```

resultはdependency set内の値が変わった場合だけ失効する。

- `counterexample_found`はwitness certificateのdependencyだけを持つ。
- `no_counterexample_found`は固定review scopeとmanifest全atomをdependencyに持つ。
- `unavailable`は未解決predicateとそれを閉じ得るnon-value atomをdependencyに持つ。
- certificate外の新result、別subject、別required outcome、read-only operationまたはtask全体の状態は失効理由にしない。

resultの効果は対応subjectを含む未発行artifact変更と外側admission terminalだけへ投影する。reviewer起動、既にterminalな別review、無関係なread、別subjectまたはtask全体へ停止効果を伝播させない。

terminalになったreview operationを、dependency変更後に再開しない。admitted resultが失効し、同じreview criterionを再び判定する必要がある場合は、変更後dependencyを持つ新しいreview operation identity、packet identity、producer bindingおよびresult identityを形成する。TaskSpecが現在design identity内の再reviewまたは改訂を禁止する場合は新operationを作らず、外側admissionを`unavailable`または固定済みstop conditionへ閉じる。

### 11. artifact change permission

```text
subject_change_allowed(subject) :=
  review_requirement=not_applicable
  ∨ finite_direct_match(subject)
  ∨ (
      review_requirement=required
      ∧ admitted no_counterexample_foundがactive
    )
```

`review_requirement=not_applicable`はreview責務が新しい変更permissionを生成するという意味ではなく、同じ本文の共通coreが固定する`implementation_bound`、permission、change predicateおよびvalidation gateだけへ委譲することを意味する。

```text
subject_change_denied(subject) :=
  admitted counterexample_foundがactive
  ∨ admitted review unavailableがactive
  ∨ (review_execution_permission=denied ∧ activeなadmitted prior review resultがない)
  ∨ packet unavailable
```

`counterexample_found`は現在design identityをrejectし、対応subjectを含むartifact変更を禁止する。`unavailable`は欠陥を確定せず、判断に必要なresultがないため対応subjectの変更だけを禁止する。

一つのartifact変更invocationが複数subjectを含む場合は、全subjectで`subject_change_allowed=true`かつ全artifact間relationと保持constraintが成立する場合だけ発行する。禁止subjectをpayloadから除くとrequired outcome、relationまたは実行可能性を壊す場合は、一部変更せずC147のimplementation choiceを失効する。別implementation choiceを作る場合は新identityで変更前gateからやり直す。

### 12. outer terminal

| 条件 | 外側admission result | artifact変更 | outer terminal |
|---|---|---:|---|
| finite direct match、変更・validation全success | `change_path_ready` | 必須 | `completion_ready` |
| review contract非適用、共通core gateと変更・validation全success | 共通core result | TaskSpecどおり | 共通core terminal |
| activeな保存済み`no_counterexample_found`、変更・validation全success | `change_path_ready` | 必須 | `completion_ready` |
| activeな保存済み`counterexample_found` | `blocked` | 0 | `blocked` |
| activeな保存済みreview `unavailable` | `unavailable` | 0 | `unavailable` |
| admitted `no_counterexample_found`、変更・validation全success | `change_path_ready` | 必須 | `completion_ready` |
| admitted `counterexample_found` | `blocked` | 0 | `blocked` |
| activeな保存済みresultがなくreview execution permission denied | `unavailable` | 0 | `unavailable` |
| packet unavailable | `unavailable` | 0 | `unavailable` |
| admitted review `unavailable` | `unavailable` | 0 | `unavailable` |
| required result、変更resultまたはvalidation resultが未terminal | nonterminal | 0または未完了 | nonterminal |

外側operationは、必要な全operationについてbind済みproducerのterminal resultが揃うまでterminalにしない。invocation終了、reviewer session終了、進行報告、集約文またはfinal responseで欠けたresultを補完しない。

## ADR terminalの導出

Candidate名、case IDまたは期待terminalを参照せず、入力状態から次の5経路を導出できる。

| 入力状態 | 導出 |
|---|---|
| review contractが現在subjectへ非適用 | `not_applicable -> common execution core` |
| authorityが全effectとrelationを直接閉じ、変更predicateが完全一致 | `finite_direct_match -> not_required -> change -> validation -> completion_ready` |
| direct matchなし、activeなadmitted prior resultあり | `required -> prior result effect -> corresponding outer path` |
| direct matchなし、permission許可、具体的witness certificate成立 | `required -> review -> counterexample_found -> change denied -> blocked` |
| direct matchなし、permission許可、固定scope全観測success、反例なし | `required -> review -> no_counterexample_found -> change -> validation -> completion_ready` |
| direct matchなし、permission許可、terminal dependencyがnon-value | `required -> review -> unavailable -> change denied -> unavailable` |
| direct matchなし、permission否定 | `required -> no review operation -> change denied -> outer unavailable` |

この導出はADR9の5種類の証明責務を覆うが、prompt本文へcase IDまたは上表をそのまま分岐として埋め込むことを意味しない。

## C147条項の再配置

| C147条項 | 新しい正本責務 | 処置 |
|---|---|---|
| `SPEC` | `OPERATION_SPEC` | operationとouter terminalを分けて改訂 |
| `PRODUCER` | `PRODUCER_BINDING`、`RESULT_ADMISSION` | producer選択とresult真正性へ分割 |
| `TERMINAL` | `REVIEW_JUDGEMENT`、`CHANGE_TERMINAL` | inner／outer terminalへ分割 |
| `CONTEXT` | `PACKET_FORMATION`、terminal certificate | packet membershipとdependencyを分割 |
| `EVIDENCE_GATE` | `OBSERVATION_RESULT`、`RESULT_EFFECT`、`CHANGE_TERMINAL` | evidence発行、失効、変更許可へ分割 |
| `OWNER_ROLE` | `OPERATION_SPEC`、`PRODUCER_BINDING`、`RESULT_ADMISSION` | invariantを移し独立条項を削除 |
| `ROOT` | `RESULT_ADMISSION`、`CHANGE_TERMINAL` | root非代行を直接組み込み独立条項を削除 |
| `INDEPENDENCE` | operation dependency、observation atomicity | dependency形成へ改訂 |
| `DECISION_BOUNDARY` | `RESULT_EFFECT`、`DISPATCH_TRANSITION` | resultの局所効果とfrontierの挙動遷移へ分割して改訂 |
| `VALIDATION_CLOSURE` | validation責務 | reviewから隔離して保持 |
| `VALIDATION_PLAN` | validation責務 | reviewから隔離して保持 |
| `METHOD` | observation state、method continuation | state区別を加えて改訂 |
| `RECOVERY` | environment recovery | review再判断を含めず保持 |

責務の再配置後、一つの状態遷移を複数条項が競合して所有しない。局所注意喚起のための再記述で正本を増やさず、共通coreとreview責務の接続は定義済みstate名だけで行う。

## M3で確認したblocking counterexample

M3は次の具体的状態で、設計のtarget、permission、methodまたはstop conditionを変えなければ解けない反例だけを確認する。網羅性追加、表現改善、schema追加または試験で観測可能な不確実性だけではM2へ戻さない。

1. 一つのobservation valueが、同一subjectのwitness applicabilityとclosureの両方へ依存し、一方だけを失効させる必要がある場合。
2. 一つのtool invocationが複数atomの個別stateを返すが、invocation-level failureも同時に返す場合に、atomicity規則で真正性を一意に判定できない状態。
3. `counterexample_found`形成後に、certificate dependency内のapplicability入力だけが変わり、review operationを再開せず新identityへ移る必要がある状態。
4. authorityが複数effectを有限閉包するが、保持relationの一部だけがmachine-boundで、残部が一般設計判断を必要とする状態。
5. permission否定とadmissibleな先行review resultが同時に存在し、先行resultの利用可否が外側terminalを変える状態。
6. 複数subjectを一invocationでしか実装できず、一subjectだけが`counterexample_found`となった状態。
7. observation target identity自体が未固定な状態と、identityは固定済みだがtargetが`missing`の状態を同じpacket規則が誤って同一視する場合。
8. review契約がない通常変更で`finite_direct_match=false`となり、本設計が独立reviewを新設してStandard14の既存root-only経路を退行させる場合。

初回reviewでは条件2、3、4、5、8に具体的反例が成立したためM2へ戻り、本設計へ修正を反映した。修正版の再確認は[`review制御再構成の方向レビュー`](review-control-reconstruction-direction-review.md)を正とし、8条件すべてで未解決blocking counterexampleは0件となった。残余リスクはM5〜M7のmechanism predicateへ対応させてM4へ渡す。

## M2完了判定

- operation、predicate、evidence、producer、result、dependency、invalidation、terminalおよびartifact変更許可を、review責務を保持した10責務と共通coreの`DISPATCH_TRANSITION`へ再配置した。
- 各状態遷移のownerを一つに限定した。
- 5種類のterminalをCandidate名、case IDまたは期待terminalなしに導出した。
- evidence発行、観測result真正性、terminal dependency、result admission、局所失効およびouter terminalを分離した。
- method自由と独立observation atomの統合許可を分離した。
- C147の13条項を新しい正本責務へ全件対応させた。

## Candidate192発行責務の再判定

Candidate191のStandard14保存traceでは、evidence資格を持つinvocationが別operation identityへ属することを理由に別model stepへ送られ、9ケース、45 run中44件で変更前stepが一つ増えた。A01では下流terminalを変えない開始identity観測も発行された。これはreviewの10責務を変える反例ではなく、共通execution core内で発行可否と共同発行を所有する責務が欠けていた反例である。

Candidate192は共通coreへ`DISPATCH_ADMISSION`を追加し、次を一つの変更軸として所有させた。

```text
invocation_consumer_ready(i) :=
  evidence_consumer_ready(i)
  ∧ requested resultを消費するbind済みoperationがnonterminal
  ∧ resultがconsumerのtarget / permission / method / stop conditionを変え得る

dispatch_dependency(i, j) :=
  i.resultがjのtarget / permission / method / stop conditionを変え得る

coissuance_ready(S) :=
  Sの全invocationがinvocation_consumer_ready
  ∧ S内の任意の異なるi, jでdispatch_dependency(i, j)=false
```

- TaskSpecが開始状態を明示していても、結果consumerがなければ開始観測を発行しない。
- 現在readyで相互非依存な最大集合を同じmodel stepから発行し、一部result受領後に残りを発行しない。
- operation identity、lifecycle、predicate、consumerまたはresult格納先が別であることだけではdecision boundaryを作らない。
- 同一model stepからの共同発行と、一つのinvocation resultへの統合を分ける。個別result contractが必要なら別tool callのまま共同発行する。
- 開始identity resultがreadを禁止する、またはread target・permissionを変える場合は真正なdependencyとして別stepを維持する。

`EVIDENCE_ADMISSION`は証拠資格、`RESULT_EFFECT`はresultの局所効果と失効、`DISPATCH_ADMISSION`は発行可否と共同発行だけを所有するとした。`OWNER_ROLE`、review適用、result admission、terminal、validationおよびrecoveryは変更しなかった。

### 評価後の反例

対象Standard14 N=5では、A01以外の退行8ケース40件中39件が、`coissuance_ready(S)`を実際の同一model step発行へ変換しなかった。A01でも2 / 5件がconsumerなし開始identityを発行した。したがって、上記補遺は発行集合の妥当性を定義しているが、その集合を現在のmodel responseで必ず発行する遷移ownerを持たず、挙動を拘束できない。

本改訂ではCandidate192を直接基盤にせず、Candidate191の成立経路へ第6節`DISPATCH_TRANSITION`だけを接続する。`coissuance_ready(S)`という判定結果を残さず、`dispatch_frontier`を現在responseの全tool-call identityへ一対一bindし、全result収集までを一つのterminal遷移にした。consumerなしならfrontierに入らず、frontierが空ならtool callは0件となる。consumerがある相互非依存invocationは、一件でも現在responseから欠ければ遷移自体がnonterminalであり、その部分発行resultを正しいdispatch completionへ昇格しない。単一shell commandへのresult集約は解決に使わない。
Candidate192後の限定M3は、空frontier、真正dependency、同時発行上限、個別result、nonterminal tool、部分発行およびcompound代用を確認し、当時の設計入力上はblocking counterexample 0件で完了した。

その後のCandidate193 ADR9 r2 N=5では、全9ケースで開始identity不一致が後続readを禁止する真正dependencyだったにもかかわらず、28 / 45件で両者を同じmodel stepから発行した。正しい初回frontierは17 / 45件に留まり、同一ケース内でも挙動が変動した。ただし同じ基準のCandidate191は越境36 / 45、正しい分離9 / 45であり、Candidate193は直接親から8件改善した。したがって第6節は成立済み設計ではないが、無作用として全削除できる仮説でもない。

残すのはconsumer・真正dependency・個別result contract・compound command禁止である。`dispatch_candidate`、`dispatch_predecessor`、`dispatch_frontier`、独立条項化および次Candidateの直接基盤はM1で保留する。捨てるのは、自己terminal宣言だけで現在responseのtool-call選択を一意に強制できるという十分性仮定である。ADR05・ADR06のterminal不一致は、発行遷移との直接因果を推定せず、certificate dependencyとobservation target bindingの問題として別に分析する。

Candidate188のM4静的再監査では、削除済み親経路への委譲、汎用worker context欠落および`OBSERVATION_RESULT`過密化が具体的反例として成立した。このため自己完結した実装identityをCandidate189へ分離した。Candidate189 M5でcurrent resultへprior用permissionを誤適用した反例を受け、第8節と第9節のpermission scopeをCandidate190へ実装した。Candidate193評価後はM1へ戻っており、本書の第6節を修正して次Candidateを作る段階にはない。後続の現在位置は[`review制御再構成マイルストーン計画`](review-control-reconstruction-milestone-plan.md)を正とする。
