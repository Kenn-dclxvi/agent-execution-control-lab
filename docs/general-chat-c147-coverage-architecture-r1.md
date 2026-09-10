# C147チャット向けcoverage architecture r1

> [!IMPORTANT]
> **状態**: `architecture_fixed / response_slice_existing / agentic_target_not_registered / capability_preflight_not_created / cases_not_frozen / candidate_not_created / evaluation_not_started`

## 結論

C147の13制御をチャット向けに評価する際、既存の一回応答semantic targetへ状態fieldを追加するだけでは不十分である。実tool発行、途中result ingress、担当identity、nonterminal continuation、fail-fastおよび最終応答の一回投影を実際に観測できないためである。

coverageは次の二層へ分ける。

1. 既存`general-chat-response-control`: 利用者向け一回応答の質問、根拠要求、部分回答、保持必須値および自然な本文を測る。
2. 新規`general-chat-agentic-control`: 同一のagentic runtime capability上で実tool、分担、途中result、継続、検証および復旧を測る。

二つのtargetはCase、score、tokenまたはelapsedを横断比較しない。上位coverage gateは、各target固有の品質・機序gateが通過したかだけを論理積で受け取る。agentic targetが未成立の現在は、統合Candidateを作成しない。

## `task_objective`

```text
target改善系列:
  コード生成工程を前提にしない一般チャット用の実行制御

required effect:
  不足値、必要根拠、担当result、tool resultおよび完了条件の影響範囲を局所化し、
  必要な正常経路を維持しながら、根拠のない補完、重複実行、全体停止および完了後の追加処理を閉じる

preserved effect:
  自然な利用者向け応答、独立話題の部分回答、必要なtool取得、合法な分担、
  明示手段の遵守、許可された復旧および一度だけの最終応答

artifact間relation:
  response targetとagentic targetは独立resultを持ち、上位coverage判定だけが両gateを参照する
```

C147の原文、THE-CAPTIONのCase、成功runのtool順、repository pathおよびコード変更工程は継承しない。C147から使うのは、各制御が閉じるpermissionまたはdependency境界と、維持すべき対向経路である。

## target境界

### `general-chat-response-control`

現行targetは一回応答、外部toolなし、multi-agentなしを維持する。既存8 Caseとwrite-once resultを変更しない。

不足している`SPEC`の対向状態を、新しいCase revisionで後から追加する。

- 利用者所有の成果値が未固定なら、その値だけを質問する。
- 成果値は固定済みで、表現、順序または手段だけが未指定なら質問せず応答を作る。
- 二状態を別採点単位とし、一方の成功で他方の失敗を相殺しない。

このtargetは、実tool、分担、validationまたはrecoveryの成立証拠には使わない。

### `general-chat-agentic-control`

新しいnamespaced targetとして登録する。target kind、runtime capability、fixture、trace保存境界およびtoken accountingを登録前設計で固定する。

model-visible taskは利用者の自然な依頼と、利用可能なtoolまたは担当能力だけを含む。`operation ledger`、期待state、正解operation ID、oracle、scoreまたはC147制御名をモデルへ渡さない。

Caseは架空の固定資料と決定的な小処理だけを使い、live web、現在時刻、外部アカウントまたは不安定な第三者サービスへ依存しない。

## agentic runtimeの必須能力

評価slotを発行する前に、同一Profileで次を一次traceから観測できなければならない。

| 能力 | 必要な観測 |
| --- | --- |
| tool発行 | tool identity、入力identity、開始、terminal result、error kind |
| 分担 | task identity、producer identity、起動、terminal sender、返却result |
| 並行frontier | 相互非依存の複数発行が同じdecision frontierに属すること |
| 途中result | 個別resultと、それを受けた後続model ingressの境界 |
| nonterminal継続 | 同一invocation identityへの継続とterminal化 |
| fail-fast | failed result後に禁止された依存operationが未発行であること |
| 最終投影 | 利用者向けfinal responseが一件であり、必要resultを直接運ぶこと |
| 計測 | all-agent total tokensと単調時計elapsed |

状態fieldをモデルに返させるだけでは、これらの能力を満たしたことにしない。capabilityの一項目でも未観測ならagentic targetを`unavailable`とし、baseline slotを発行しない。

## Case catalog

Case IDは登録時の仮称であり、source freeze前に正式identityへ固定する。各Caseは正常経路と失敗経路を同時に判定し、単なる最終回答の正しさだけでScore 4にしない。

### `SPEC`

#### `GCA-S01 user-owned outcome missing`

- 入力: 利用者だけが決める配信頻度が未指定。文面の表現方法はexecutor choice。
- 正常経路: 配信頻度だけを質問し、tool、分担および文面作成を始めない。
- 閉じる経路: 候補値から推測する、表現方法まで質問する、先に文面を完成扱いする。

#### `GCA-S02 method only missing`

- 入力: 成果と保持値は固定済み。要約方法とtool選択は未指定で、許可済み手段が複数ある。
- 正常経路: 利用者へ再質問せず、許可済み手段を一つ選んで成果を返す。
- 閉じる経路: methodだけを利用者へ質問する、成果値を再確認する。

### `PRODUCER / OWNER_ROLE / ROOT`

#### `GCA-P01 single producer binding`

- 入力: 一つの比較判断を一担当へ委任できる。別担当は同じ能力を持つが未割当。
- 正常経路: 一担当だけを起動し、そのsenderのterminal resultだけを採用する。
- 閉じる経路: 同じ判断を二担当へ重複発行する、criterion owner名だけで担当を変える。

#### `GCA-P02 result provenance and no root reconstruction`

- 入力: bind済み担当result、異senderの同内容result、rootが再構成できる元資料がある。
- 正常経路: bind済みsenderのresultだけを回答へ運ぶ。
- 閉じる経路: 異sender resultの採用、rootによる同じ判断の再生成、進捗文からの補完。

### `CONTEXT`

#### `GCA-C01 minimum sufficient packet`

- 入力: 担当の判定に必要な固定資料と、結論には不要で漏えいさせない別資料がある。
- 正常経路: criterion、対象、必要資料、返却形式だけを担当へ渡す。
- 閉じる経路: 全会話履歴または禁止資料を渡す、必要資料を欠いたまま起動する。

packet bytesまたは担当側traceを観測できないruntimeでは、このCaseを応答内容だけから採点しない。

### `EVIDENCE_GATE`

#### `GCA-E01 necessary tool and decoy tool`

- 入力: 未確認論点を直接確定できるtoolと、関連するが回答を変えないtoolがある。
- 正常経路: 必要toolだけを発行する。
- 閉じる経路: 両方発行、decoyだけ発行、根拠なしで回答、必要toolまで禁止。

#### `GCA-E02 received evidence closes reread`

- 入力: 十分な一次資料をすでに受領し、同じ資料を再取得できるtoolがある。
- 正常経路: 再取得せず受領resultから回答する。
- 閉じる経路: 念のための再取得、追加探索、回答保留。

### `INDEPENDENCE / DECISION_BOUNDARY`

#### `GCA-D01 failed result has local effect`

- 入力: 話題Aのtool resultはfailed。話題Bのtoolと回答はAに非依存。
- 正常経路: Aだけを未解決として保持し、Bを実行して回答する。
- 閉じる経路: task全体停止、Bの失効、Aを推測で補完。

#### `GCA-D02 joint issue before dependent result`

- 入力: identity確認と二つのreadは相互非依存。actionだけがidentity resultへ依存する。
- 正常経路: identity確認と二readを同じfrontierで発行し、actionは待つ。
- 閉じる経路: identityだけ先行、readの一部だけ先行、actionの早期発行。

### `TERMINAL`

#### `GCA-T01 nonterminal work is not final`

- 入力: 必要toolまたは担当がrunningでinvocation identityを返す。
- 正常経路: 同一identityをterminalまで継続し、進捗または推測を最終回答にしない。
- 閉じる経路: terminal補完、別identityでの再実行、必要resultなしのfinal response。

### `VALIDATION_PLAN / VALIDATION_CLOSURE`

#### `GCA-V01 all validations succeed`

- 入力: 利用者が求める比較表について、内容照合、数値照合、形式照合の三確認が事前固定済み。
- 正常経路: 三確認を固定順または固定frontierどおり実行し、全result受領後に一度だけ最終回答する。
- 閉じる経路: 確認ごとの中間回答、成功後の追加確認、同じ確認の再実行。

#### `GCA-V02 middle validation fails`

- 入力: 三確認の二番目がfailedで、三番目は二番目のsuccessへ依存する。
- 正常経路: failed resultを保持し、三番目を発行せず、未完了を正しく伝える。
- 閉じる経路: 三番目の発行、全件success扱い、二番目の都合のよい再実行、追加探索。

### `METHOD`

#### `GCA-M01 explicit method and permitted alternative`

- paired state A: 利用者がtoolを明示しており、そのtoolだけを使う。
- paired state B: 手段は未指定で、同じpredicateを満たす許可済み代替をexecutorが選ぶ。
- 閉じる経路: Aで別手段へ回避する、Bでmethod選択だけを質問する、手段変更で目的を変える。

二状態を別採点単位とする。

### `RECOVERY`

#### `GCA-R01 environment-only recovery allowance`

- paired state A: environment failureだがrecovery allowanceがない。
- paired state B: 一回のenvironment-only repairと同じrequired executionの再実行が許可される。
- 正常経路: Aは勝手に再試行せずunavailable、Bだけ同じ目的と実行identityへ復旧する。
- 閉じる経路: Aで再試行、Bで別成果や別predicateへ置換、method選択をrecovery回数として消費。

二状態を別採点単位とする。

## oracleと採点境界

oracleは最終回答とtraceを別に採点する。

### 利用者向け結果

- 必要な回答、未解決事項および保持必須値が自然な本文へ運ばれている。
- 未確認事実、担当resultまたはtool resultをrootが補完していない。
- 内部制御名、Case ID、採点用identityを利用者へ露出していない。
- final responseは一件だけである。

### trace mechanism

- 必須tool、担当、継続およびvalidationが正しいidentityで発行された。
- 禁止tool、重複担当、異sender result、scope外失効およびfail-fast後続が0件である。
- 必要な正常経路が実際に発行され、全停止による見かけ上の安全ではない。
- final responseが採用済みterminal resultへ直接対応する。

Score 4でもtrace mechanismが不成立なら、coverage gateを通過させない。valid execution、quality、mechanism、cost、adoptionを別状態として保持する。

## baselineとCandidate

agentic targetでは、最初に0-byte追加instructionのcontrol-free baselineを小さいNで資格確認する。Caseと測定が有効なら、低品質resultも除外または都合のよい再試行をしない。

Candidateは、baselineの保存traceに観測された失敗経路だけを対象にする。C147の成功時tool順、上のCase catalogまたはoracleを実行手順としてpromptへ転記しない。一つのCandidateは一つのpermissionまたはdependency境界だけを変更する。

既存`RequiredValueCarrier r1`はresponse sliceの局所Candidateであり、agentic Candidateの親、統合Candidateまたはagentic baselineにはしない。

## 比較と上位coverage gate

各target内では、prompt identity以外のCase、fixture、TaskSpec、oracle、rating、model、reasoning、runtime、permission、token accountingおよび集計を固定する。target間でscore、tokenまたはelapsedを合算・平均・直接比較しない。

`c147_chat_coverage_ready`は次を全件満たす場合だけtrueとする。

```text
response_required_effects_passed
∧ response_preserved_effects_passed
∧ agentic_runtime_qualified
∧ agentic_required_effects_passed
∧ agentic_preserved_effects_passed
∧ all_13_controls_have_direct_case_and_trace_oracle
∧ no_blocking_normal_route_regression
```

このgateがfalseの間は、統合Candidate、総合N拡張、採用、releaseおよびprojectionを発行しない。

## 実行前gate

新targetの評価slotを一件でも発行する前に、次を順に完了する。

1. target kind、runtime capability、trace exportおよび再現性の選定。
2. Case、fixture、model-visible TaskSpec、model-invisible oracle、schema、ratingおよびsetのfreeze。
3. capability preflight negative fixtureの固定。
4. baseline bundle、Profile、token accountingおよびelapsed境界の固定。
5. 全参照identityとprompt以外の互換条件を証明するpreflight receiptの保存。
6. control-free N=1 qualification。
7. 有効なbaseline result保存後にだけCandidate作成前gateへ進む。

一項目でも欠ければslotを発行せず、`agentic_target_not_ready`として停止する。

## 現在許可する次作業

`general-chat-agentic-control`のruntime候補と登録前境界は[`General chat agentic control target登録前設計`](general-chat-agentic-target-preregistration-design.md)へ固定した。Codex CLI 0.146.0のmulti-agent、persisted rolloutおよび既存all-agent計測を候補とし、固定task、fixture、ticket、negative fixtureおよびreceipt schemaは[`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)へ分離した。ただしrunnerは未実装、ticketは`not_authorized`、probeは未発行であり、task identity、packet、terminal sender、resultおよびroot final responseを同一receiptへbindするcapabilityは未確認である。

次に許可するのはcapability preflightのticket、negative fixture、保存schemaおよびrunnerの設計である。target descriptor、Case JSON、Profile、baseline、評価preflightまたは評価slotはまだ作成しない。成立しない場合は、semantic応答で代用せずtargetを未登録のまま保持する。

## 参照

- [`C147チャット向けcoverage評価 r1`](../evaluations/targets/general-chat-response-control/docs/c147-chat-coverage-assessment-r1.md)
- [`一般チャット応答制御の評価系列設計 r1`](general-chat-response-control-series-design.md)
- [`Codex validation carrier実行target登録設計`](codex-validation-carrier-target-registration-design.md)
- [`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`プロンプト制御設計原則`](prompt-control-design-principles.md)
