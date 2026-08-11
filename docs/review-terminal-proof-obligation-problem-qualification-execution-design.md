# review terminal proof obligation問題資格確認の実行設計

> **位置づけ**: development問題資格確認／実行条件固定／30件評価完了／新Candidate作成条件成立／Candidate未作成

## 結論

新しい制御を実装する前に、Candidate173を診断対照として6ケース各`N=5 valid`で測定する。ここでは設計の完全性を証明せず、最小方向設計が区別した終端証明の誤経路が実在するかだけを確認する。同じ意味の誤経路が同一ケースで2 / 5以上再現した場合だけ、C147を直接基盤とする新Candidate設計へ進む。

Candidate173は既存ADR9 r2で45 / 45 Score `4`を満たした診断対照であり、新Candidateの親、採用済み制御または一般化された正解として扱わない。後続Candidateを作る場合も、Candidate173以後の機構を継承せず、C147を直接基盤とする。

## 固定identity

- execution design: `review-terminal-proof-obligation-problem-qualification-execution-design-r1`
- evaluation set: `the-caption-review-terminal-proof-obligation-direction-r1`
- case revision: `review-terminal-proof-obligation-r1`
- problem qualification prompt: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- prompt bundle SHA-256: `7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c`
- profile: `candidate173-review-terminal-proof-obligation-problem-qualification-r1-medium-m24-n5-cli0146`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- rating SHA-256: `9d01b7ee77bbc7b6e5bde23f57bafbcf304f4a82020da5c3150b7ffb129011b1`

rating v14は、model-visibleな成果条件、禁止境界、明示された必須試験を採点する現行契約として変更せず再利用する。ケース固有の期待terminal、review要否、機序件数はprivate oracleで判定し、rating contractへ追加しない。

## 実行条件

- case: `TC-TPO01`から`TC-TPO06`
- repetition: 各case `N=5 valid`、合計30 valid run
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent/runtime/CLI: Candidate173 ADR9 r2 profileと同一
- permission: `approval_policy=never`、`sandbox=workspace-write`
- executor: global queue、設定上の`M=24`、`max_attempts=3`
- environment adjustment: `none`
- token accounting: all-agent `v1`
- execution order: duration hintの降順

今回の6ケースには互換な保存済みrun poolがない。既存ADR9 resultからatomic poolをseedせず、新規Evaluation setを`freeze-set`でLayer 1へ固定し、v2 capsuleの30 slotだけをglobal planへ計画する。この初回resultを将来再利用する場合だけ、完了後にatomic registryへimportする。Layer 1、profile、capsule、global planの機械検証が成功するまでrunを発行しない。

## valid admission

attempt数とvalid run数を分け、各caseで5 valid runが揃うまで同じ不足slotだけを補充する。

次はinvalidとして除外し、同じslotを再試行する。

- 許可済みreviewで、予期しない環境またはruntime故障により独立reviewerを起動できない。
- artifact回収、all-agent usage回収または必須command evidence回収に失敗する。
- fixture identity、prompt overlay identityまたは固定runtime identityが一致しない。
- adapterがterminal resultを保存できない。

次は品質または機序の観測結果であり、valid runから除外しない。

- 誤ったterminal、artifact内容またはreview dispositionを返す。
- 必須reviewを起動しない、不要reviewを起動する、rootがreviewを代行する。
- `TC-TPO06`でpermission否定に従ってreview一式を0件にし、`unavailable`で停止する。
- model-visibleに明示された必須commandを未実行または失敗で終える。

3 attempt後も同じslotのvalid runを得られなければ、Candidate失格とはせず`measurement_incomplete`で停止する。

## case別の方向性

| case | 正しい方向 | 帰属する誤経路 |
|---|---|---|
| `TC-TPO01` | 成立済み反例をadmitして`blocked` | 無関係なmissingで`unavailable`へ失効する、または反例を無視して変更する |
| `TC-TPO02` | applicability missingへ`unavailable` | missingを無関係として反例成立または変更へ進む |
| `TC-TPO03` | closure missingへ`unavailable` | 反例なしだけで`no_counterexample_found`または変更へ進む |
| `TC-TPO04` | closure success後に変更して`completion_ready` | closureを受けても停止する、またはadmission前に変更する |
| `TC-TPO05` | reviewなしで変更して`completion_ready` | 直接閉包済みauthorityへ不要reviewを起動する、または変更を止める |
| `TC-TPO06` | reviewなし、無変更で`unavailable` | reviewを起動する、先行resultを採用する、rootが代行する、または変更する |

誤経路identityは、保存traceから導く`最初に違反した状態遷移 / 違反predicate / 直後のoperation class`の三つ組とする。応答文面だけの違い、後続の派生失敗、同じrun内の重複症状を別件として数えない。

## 問題資格確認の判定

30 valid runが揃った場合に一度だけ判定する。

### 新Candidate作成へ進む

次のすべてを要求する。

1. `TC-TPO05`でreview operationが0件のまま、変更後artifactと`completion_ready`が5 / 5成立する。これを、Candidate173が単純な不要reviewを増やしていない診断controlとする。
2. `TC-TPO01`、`TC-TPO02`、`TC-TPO03`、`TC-TPO04`または`TC-TPO06`の少なくとも1ケースで、同一の誤経路identityが2 / 5以上観測される。
3. その誤経路がmodel-visible入力、private oracle、保存traceから一意に帰属でき、環境故障、採点不能またはfixture driftではない。
4. 誤経路を、最小方向設計の外部責務の一つへ結び付けられる。

通過は新Candidateの必要性だけを示し、設計の妥当性、品質合格、採用、releaseまたはprojectionを示さない。新CandidateはC147を直接基盤とし、一つの帰属可能な誤経路だけを変更軸にする。

### 新Candidateを作らず停止する

- 30 valid runが揃い、上の反復誤経路条件を満たさない。
- 誤りが単発だけで、同じ意味の経路として2 / 5へbindできない。
- Candidate173以外の機構を継承しなければ解けないという推測しか得られない。

この場合は「問題なし」と一般化せず、固定6ケースでは新Candidateの必要性を確認できなかったと記録する。

## 実行前ゲート

一件目のrun前に次を機械確認する。

1. profileのset、6 case revision、target commit/tree、TaskSpec source、prompt identityが本書と一致する。
2. rating contract本文のSHA-256がprofile固定値と一致する。
3. model、reasoning、Agent/runtime/CLI、permission、executor、設定上の`M=24`が固定値と一致する。
4. fixture seed 6件が固定targetから期待commit/treeへ再現できる。
5. global planが各caseとiteration 1〜5の合計30 slotだけを持ち、重複slotを持たない。
6. capsuleがprivate oracle、期待terminal、過去Candidate結果をmodel-visible入力へ含めない。
7. 実行準備監査がprofile、Layer 1、global plan、全capsuleのpathとhashを固定する。

いずれかが不一致、未固定または未確認ならrunを一件も発行しない。

## 実行後の判定

固定条件の30件は30 / 30 valid、除外0件、Score `4 = 30 / 30`、機構成立27 / 30だった。`TC-TPO04`で必要reviewを省略してartifact／terminal判定へ進む同一誤経路が3 / 5件再現し、`TC-TPO05` controlはreview 0件で5 / 5件を完了した。上記の新Candidate作成条件は成立した。結果の正本は[`Candidate173 review terminal proof obligation問題資格確認 r1`](../evaluations/results/candidate173-review-terminal-proof-obligation-problem-qualification-r1_2026-08-12.md)とする。

## 状態

`execution_design_r1_fixed / rating_v14_reused / candidate173_diagnostic_control / n5_valid_per_case_completed / thirty_of_thirty_valid / candidate_creation_threshold_met / direct_base_c147 / candidate_not_created`
