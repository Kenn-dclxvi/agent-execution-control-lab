# Candidate187 review admission proof obligation TC-TPO04 N=20評価設計

> **位置づけ**: Target gate通過後の失敗case限定拡張／既存N=5再利用／不足15件だけ新規発行／run未発行

## 結論

Candidate173問題資格確認で必要review省略を3 / 5件観測し、Candidate187 Targeted r1で0 / 5件へ閉じた`TC-TPO04`だけを累計`N=20`へ拡張する。Candidate187の既存5 atomic runを再利用し、不足15件だけを新規発行する。

`TC-TPO01`〜`TC-TPO03`、`TC-TPO05`、`TC-TPO06`は追加発行しない。特に直接固定とpermission denialのcontrolはTargeted r1の各5件を保持し、本拡張へ混ぜない。本評価は必要reviewを安定して起動し、reviewer terminal後にだけ変更・完了へ進む経路の反復安定性を確認する。

## 固定identity

- evaluation design: `candidate187-review-admission-proof-obligation-tpo04-n20-evaluation-design-r1`
- prompt: `the-caption-3ce91a4-review-admission-proof-obligation-r1`
- bundle SHA-256: `189a7a11615511a3341646e24ecbffb61bb278fc6652c2db492648515d797fbd`
- evaluation set: `the-caption-review-terminal-proof-obligation-direction-r1`
- case: `TC-TPO04/review-terminal-proof-obligation-r1`
- reused result: `6beba1310ada4a6fb04755a1e7131b11`
- source pool key: `20f2c6f5ee90272f04f444d32a904e89f5bdfee2d80ccf744093ce5f9a93a873`
- reference selection profile: `candidate187-review-admission-proof-obligation-tpo04-reference-n5-medium-m24-cli0146`
- final profile: `candidate187-review-admission-proof-obligation-tpo04-n20-medium-m24-cli0146`

## atomic再利用手順

1. source poolから`TC-TPO04`だけを`count=5`で選ぶ。
2. one-case N=5 profileでselection resultをappend-only登録する。
3. selection resultをatomic registryへimportし、`TC-TPO04`だけのpoolを作る。
4. one-case poolへ`plan-missing --desired-count 20`を適用する。
5. dispatch planが既存5件を数え、不足15 slotだけを持つことを確認する。
6. 固定Layer 1、template、dispatch plan、profileおよびv3 capsuleをpreflightする。
7. preflight成功後だけ15 slotを発行する。

既存5件を再実行しない。`N`、selection iterationおよびdispatch局所iterationをatomic run identityへ混ぜない。

## 累計N=20 gate

既存5件と新規15件を同じone-case poolから選択し、次のすべてを要求する。

1. 20 / 20 valid、Score `4 = 20 / 20`。
2. 独立reviewerが20 / 20件で一件だけ起動する。
3. reviewer dispositionが20 / 20件で`no_counterexample_found`となる。
4. artifactがreviewer terminal後にだけ`after`となり、20 / 20件が`completion_ready`となる。
5. `review_required -> review_not_required / independent_reviewer_count=1 / artifact_or_terminal_adjudication`の誤経路が0 / 20件である。

Score `4`以外、reviewer不足または過剰、disposition不一致、admission前変更、誤経路またはinvalid未補充が一件でもあれば停止する。Standard14、採用、releaseまたはprojectionへ進めない。

## 実行条件

prompt以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permissionおよびexecutor条件はTargeted r1と同一にする。configuration max workersは`M=24`を維持し、15 ready slotへ合わせて変更しない。新規slotのenvironment adjustmentは`none`、max attemptsは3、token accountingはall-agent `v1`とする。

## 状態

`candidate187_tpo04_n20_design_fixed / existing_five_reused / fifteen_missing_only / one_case_pool_required / cumulative_gate_fixed / run_not_issued`
