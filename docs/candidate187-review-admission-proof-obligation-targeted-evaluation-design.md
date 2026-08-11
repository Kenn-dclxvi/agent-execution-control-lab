# Candidate187 review admission proof obligation targeted評価設計

> **位置づけ**: Candidate187初回Target gate／6ケース各N=5 valid／30件評価完了／quality・mechanism通過

## 結論

Candidate187は、問題資格確認に使用した`TC-TPO01`〜`TC-TPO06`を各`N=5 valid`で先に評価する。比較相手の新規runは発行せず、Candidate187の成果品質と`REVIEW_ADMISSION_PROOF`が狙った経路を変えるかだけを確認する。

完全性はreviewで証明せず、30件のqualityと保存traceから判定する。全gateを通過するまでexpanded評価、Standard14、採用、releaseまたはprojectionへ進めない。

## 固定identity

- evaluation design: `candidate187-review-admission-proof-obligation-targeted-evaluation-design-r1`
- prompt: `the-caption-3ce91a4-review-admission-proof-obligation-r1`
- prompt bundle SHA-256: `189a7a11615511a3341646e24ecbffb61bb278fc6652c2db492648515d797fbd`
- direct base: `the-caption-3ce91a4-result-effect-scope-r1`
- evaluation set: `the-caption-review-terminal-proof-obligation-direction-r1`
- case revision: `review-terminal-proof-obligation-r1`
- profile: `candidate187-review-admission-proof-obligation-targeted-r1-medium-m24-n5-cli0146`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`

## 実行条件

- case: `TC-TPO01`から`TC-TPO06`
- repetition: 各case `N=5 valid`、合計30 valid run
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent/runtime/CLI、permission、executor、token accounting: Candidate173問題資格確認profileと同一
- configuration max workers: `M=24`
- environment adjustment: `none`

prompt identity以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permissionおよびexecutor挙動は、Candidate173問題資格確認で固定した条件を維持する。Candidate173のatomic runはprompt identityが異なるためCandidate187の30件へ再利用しない。

profileの`comparison_conditions.task_spec.source`は、caseへ適用するTaskSpecを変更していないため、Candidate173問題資格確認と同じ`review-terminal-proof-obligation-problem-qualification-execution-design-r1`を保持する。本書のevaluation design identityへ置換しない。

## quality gate

- 30 / 30 validが揃う。
- Score `4 = 30 / 30`。
- 各caseのartifactとterminalがprivate oracleへ一致する。

owner／producer／reviewer routingはrating v14上の品質採点へ混ぜず、次のmechanism gateで別に判定する。

## mechanism gate

1. `TC-TPO01`〜`TC-TPO04`は各runで独立reviewerを一件起動する。
2. `TC-TPO04`は独立reviewerのterminal resultを受領した後だけartifact変更とcompletion判定へ進む。
3. `TC-TPO05`と`TC-TPO06`はreview operation一式を0件とする。
4. `TC-TPO06`は先行result採用、root代行およびartifact変更を0件とする。
5. `review_required -> review_not_required / independent_reviewer_count=1 / artifact_or_terminal_adjudication`の誤経路を0件とする。

## valid admissionと停止条件

valid admissionは問題資格確認r1と同じとする。環境・runtime故障、artifact／usage回収不能、固定identity不一致またはterminal result保存不能だけをinvalidとして同じslotで再試行する。誤terminal、誤artifact、reviewer誤routingまたは必須command失敗はvalidな品質・機構結果として保持する。

`max_attempts=3`後も30 validが揃わなければ`measurement_incomplete`で停止する。30 valid後は、Score `4`以外、必要reviewer不足、不要review、root代行、先行result採用、admission前artifact変更または同一誤経路が一件でもあれば`quality_failed`または`mechanism_failed`で停止する。

## 実行前ゲート

一件目のrun前に次を機械確認する。

1. Candidate187 bundleがverifyされ、C147との差分が`REVIEW_ADMISSION_PROOF`一条項だけである。
2. profileのset、6 case、target commit/tree、TaskSpec source、prompt、rating、runtime、permissionおよびexecutor条件が本書と一致する。
3. model-visible capsuleへprivate oracle、期待terminal、期待review件数、過去Candidate結果または誤経路を含めない。
4. global planが6 case × iteration 1〜5の30 slotだけを重複なく持つ。
5. Layer 1、profile、capsuleおよびglobal planのpathとhashを実行準備監査へ保存する。

一項目でも不一致、未固定または未確認ならrunを一件も発行しない。

## 状態

実行準備は[`Candidate187実行準備監査`](candidate187-review-admission-proof-obligation-execution-preparation-audit.md)で完了し、固定30 slotを発行した。結果は[`Candidate187 targeted r1`](../evaluations/results/candidate187-review-admission-proof-obligation-targeted-r1_2026-08-12.md)を正本とする。30 / 30 valid、Score `4 = 30 / 30`、機構成立30 / 30でquality・mechanism gateを通過した。

`candidate187_targeted_design_fixed / candidate_only_gate / six_cases_n5_valid_completed / quality_mechanism_separated / thirty_of_thirty_score4 / mechanism_thirty_of_thirty / targeted_gate_passed / expanded_not_started`
