# C147 Review-free portable core M3方向監査

> [!IMPORTANT]
> **状態**: `superseded / prior_M3_permission_withdrawn / input_M1_M2_incomplete`
>
> 入力となる旧M1/M2が正の発行遷移と結果収集障壁を閉じていなかったため、このM3のCandidate作成許可は撤回した。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とし、本文は旧方向監査の履歴として保持する。

## 結論

M2初稿には、method executionの失敗をpredicateのterminal resultにも読める所有競合が1件あった。`RESULT_ADMISSION`で両result kindを分離して修正した。修正後の一般18状態にblocking counterexampleは残っていない。

Candidate作成前gateの9項目は全件固定できる。次Candidateの作成を許可する。ただし許可する初回試験は、C147の成立済み正常経路を直接消費するF01 / F02 / F03各N=5だけである。そこで品質またはportable mechanismが一件でも不通過なら、Standard14全体を発行しない。

## 1. 基準promptと最短正常経路

- 基準: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- 保存品質基準: Standard14 N=100、1,400 / 1,400 score `4`
- targeted mechanism基準: F01 / F02 / F03各N=5、15 / 15 score `4`
- 最短正常経路: `outcome bind -> producer/input bind -> consumerのある観測 -> implementation bind -> change -> validation plan -> individual result closure -> completion`
- result effect: 実際に依存する未完了operationだけへ局所化する。

## 2. 再構成目的へbindする具体的誤経路

| 保存trace | 誤経路 | M2で消す判断 |
|---|---|---|
| Candidate190 | owner metadataから不要な別executionを選ぶ | producer選択をTaskSpec明示へ限定する |
| Candidate191〜193 | dispatch gate、response境界、抽象receiptが互いを再定義する | dependencyをresult effectへ戻し配送方式を除外する |
| Candidate202 Standard14 | Review追加後に開始identityだけを先行させ、許可readを不要に直列化する | Review responsibilityを0件にし、独立invocationへ偽dependencyを作らない |
| Candidate203 ADR9 | Review不要時にも別producerを起動する | criterion ownerとproducer identityを分離する |
| C147 release本文 | provenance、context、validation closureに特定runtimeの表面語が残る | 意味を12状態遷移へ移し表面語を削除する |

これらは一つの語句の誤りではなく、C147の構造的不変条件とruntime上の実装手段が同じ条項で所有されている再構成問題へbindする。

## 3. 既存層だけでは防げない理由とprompt層の境界

TaskSpecとrepository authorityはrequired outcome、permission、target状態、validation predicateを与えるが、次を一般には決めない。

- owner metadataをproducer routingへ変換してよいか。
- 受領resultをどのoperationとproducerへadmitするか。
- resultの停止効果をどの未完了operationへ限定するか。
- consumerのない追加観測を発行してよいか。
- nonterminal invocationをoperation完了へ数えてよいか。

これらはmodel-visibleな実行判断なのでprompt制御の対象にできる。一方、複数invocationのatomic dispatch、responseへのreturn timing、非同期配送保証はpromptが直接所有しない。この部分はmechanism predicateへ含めず、外部executor変更も提案しない。

## 4. 変更するpredicateと責任境界の全件集合

変更集合はM2の12責任全件である。

1. `OUTCOME`: required outcomeだけを成果authorityへbindする。
2. `PRODUCER`: 一operation一producerとnonproducer権限を所有する。
3. `INPUT`: 必要十分なinput boundaryを所有する。
4. `INVOCATION`: consumerのある未観測値だけへeligibilityを与える。
5. `RESULT_ADMISSION`: operation、invocation、producer、result kindの対応を所有する。
6. `RESULT_EFFECT`: admitted resultの局所更新と失効を所有する。
7. `IMPLEMENTATION`: 変更前closureを所有する。
8. `COMPLETION`: operation terminalを所有する。
9. `VALIDATION_PLAN`: 変更後の検証全件固定を所有する。
10. `VALIDATION_CLOSURE`: 個別result、fail-fast、全件後の一回判断を所有する。
11. `METHOD`: predicateを変えない手段選択と代替継続を所有する。
12. `RECOVERY`: authorityへbind済みの環境回復だけを所有する。

12変更を分割すると、削除済みruntime fieldの代わりとなるprovenance、nonterminal closureまたはvalidation closureが欠けた中間状態になるため、一つの構造再構成Candidateとして扱う。

## 5. 消える判断点

次の8判断を削除する。

1. `root / worker`のどちらかを先に選ぶ判断。
2. owner語列から別executionを起動する判断。
3. 会話を何turn継承するかをcoreが決める判断。
4. 特定の二field名をprovenanceの意味とみなす判断。
5. 同一responseまたはstepかをdependencyの意味とみなす判断。
6. 専用wrapperをvalidation closureの意味とみなす判断。
7. 待機IDの有無をnonterminal stateの意味とみなす判断。
8. 固有counter名をrecovery authorityの意味とみなす判断。

portable core本文は6,314 bytesで、C147 release source 10,772 bytesより4,458 bytes、41.38%小さい。これは評価前の静的記述であり、tokenまたは経過時間の改善を意味しない。

## 6. 新たに増える判断点

実行時predicateは増やさない。旧条項に分散していたresult provenance、result effect、implementation closure、nonterminal closureを単一ownerへ移す。

新しいlabelは12件だが、旧C147 labelへの参照は0件、core本文内のReview責任参照は0件、Codex固有表面語は0件である。cross-label参照は`IMPLEMENTATION -> VALIDATION_PLAN`と`VALIDATION_PLAN -> METHOD`の2本だけである。

## 7. 品質caseとscore gate

### 初回targeted gate

- case: F01 r3 / F02 r1 / F03 r2
- repetition: 各N=5、合計15 run
- quality pass: 15 / 15 validかつscore `4`
- quality stop: score `3`以下、excluded attemptまたはcontroller errorが一件でもある。

### 後続全体gate

初回targeted gateが品質・mechanismとも通過した場合だけ、Standard14全14ケース各N=5、合計70 runへ進む。quality passは70 / 70 validかつscore `4`とする。一件でも不通過なら停止し、N拡張、採用、release、projectionへ進めない。

ADR9はReview responsibilityの要否とresultを要求するため、Reviewを0件にした共通core単独の初回品質oracleに使わない。これはReview系列の結果をStandard14より先に使う規則の例外ではなく、Review系列から共通core系列へ比較目的を切り替えたことによる評価対象の分離である。

## 8. portable mechanism predicate

prompt本文はruntime固有語を持たないが、現行Codex条件での評価receiptはruntime観測値を使用できる。promptの意味と評価上の観測方法を混同しない。

| 責任群 | 現行条件で観測するpredicate | 合格条件 |
|---|---|---|
| `OUTCOME / INVOCATION` | 未固定成果で変更・検証を開始しない、consumerなし観測を追加しない | 対象runで違反0件 |
| `PRODUCER / RESULT_ADMISSION` | TaskSpecが独立producerを要求しない通常経路で不要な別executionを起動しない。要求時はresultを対応identityへbindする | 不要起動0件、必要経路の誤admit 0件 |
| `INVOCATION / RESULT_EFFECT` | 開始identity resultがreadを禁止せずtargetも変えないF01〜F03で、許可readへ偽dependencyを作らない | 15 / 15でidentity判定待ちによるread先送りなし |
| `IMPLEMENTATION` | identity共同result前にartifact変更またはrequired validationを行わない | 各0 / 15 |
| `VALIDATION_PLAN / VALIDATION_CLOSURE` | required validationを個別結果へbindし、non-success後を発行せず、全success後に一度だけ完了する | 違反0件 |
| `COMPLETION / METHOD / RECOVERY` | nonterminalまたはmethod failureだけでoperationをterminalにせず、権限否定を回避しない | 違反0件 |

`同一model step`、専用wrapper使用、特定field名一致、特定待機ID使用はportable mechanism predicateにしない。ただし現行traceで、許可readをidentity判定後まで先送りした事実は偽dependencyとして判定する。

## 9. 想定する実行量変化

- prompt bytes: C147比`-41.38%`の静的差。
- token: 低下方向を仮説とするが、評価前に効果を主張しない。
- elapsed: 偽dependencyを作らない場合は増加しない方向を仮説とする。
- invocation数: consumerのない観測が増えないことを期待する。
- producer routing: TaskSpecが独立executionを明示しないrunの不要起動0件を期待する。
- validation: 個別件数を保持し、省略による削減を認めない。

KPI比較はquality・mechanism通過後にだけ行い、C147保存済み同条件resultを再利用する。quality分布が異なる場合は効率優位を主張しない。

## 一般18状態の方向監査

| # | 状態 | 期待 | 判定 |
|---:|---|---|---|
| 1 | required outcome未固定 | clarificationだけ | pass |
| 2 | target pathだけ未固定 | implementation choiceとして継続 | pass |
| 3 | owner metadataだけ存在 | producerを増やさない | pass |
| 4 | 独立producer明示 | 一identityへbind | pass |
| 5 | input十分 | 無関係inputを加えない | pass |
| 6 | input不足 | predicateに必要な差分だけ追加 | pass |
| 7 | consumerなし | invocation不発行 | pass |
| 8 | methodだけ未固定 | 追加観測なし | pass |
| 9 | result provenance不一致 | admitしない | pass |
| 10 | predicate `false` | 当該operationだけterminal | pass |
| 11 | method `failed` | predicateはnonterminal | 初稿blocking、修正後pass |
| 12 | 独立eligible invocation複数 | 偽dependencyなし | pass |
| 13 | resultが一operationだけへ影響 | 他resultを保持 | pass |
| 14 | implementation ready | 変更前観測を閉じる | pass |
| 15 | validation non-success | 後続不発行 | pass |
| 16 | validation nonterminal | 同一invocation継続 | pass |
| 17 | permission denial | 回避せず停止 | pass |
| 18 | recovery allowance未固定 | recovery不開始 | pass |

初稿blocking counterexampleは1件、M2修正後の未解決blocking counterexampleは0件である。

## 停止条件

次のいずれか一件でCandidateを停止し、追加Candidateを連続作成しない。

- targeted 15 runにscore `3`以下、excluded attempt、controller errorがある。
- readを禁止しないF01〜F03でidentity判定待ちによる許可read先送りが一件でもある。
- identity result前のartifact変更またはrequired validationが一件でもある。
- 不要な別producer execution、result誤admit、consumerなし観測が一件でもある。
- runtime固有field名なしではrequired result provenanceを現行traceから観測できない。
- promptだけで強制できない配送atomicityを成功条件へ戻す必要が生じる。

最後の二条件では`prompt_control_not_demonstrated / candidate_not_created_or_stopped`として保持し、外部executor変更へ進めない。

## 許可する次作業

Candidate147のrelease sourceを直接基盤とし、AGENTS本文だけをM2 portable coreへ置換する一Candidateを作成できる。Review用promptは0バイトのまま保持する。case、fixture、TaskSpec、rating、model、reasoning、permission、実行環境、executor behavior、token accountingを変えない。

Candidate bundleと初回targeted評価設計を一つずつ作り、静的検証後にcomparison preflightを行う。preflightが`ready`でなければ評価slotを一件も発行しない。

## 参照

- [`c147-review-free-portable-core-causal-reclassification.md`](c147-review-free-portable-core-causal-reclassification.md)
- [`c147-review-free-portable-core-design.md`](c147-review-free-portable-core-design.md)
- [`Candidate147 Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [`Candidate147 F01 / F02 / F03 N=5`](../evaluations/results/candidate145-candidate147-result-effect-scope-v14-medium-f01-f02-f03-atomic-n5-cli0146_2026-08-02.md)
- [`Candidate202 Standard14 N=5`](../evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5_2026-08-13.md)
- [`candidate203-m5-causal-analysis.md`](candidate203-m5-causal-analysis.md)
