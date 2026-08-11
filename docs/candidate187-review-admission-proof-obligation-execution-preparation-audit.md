# Candidate187 review admission proof obligation実行準備監査

> **結果**: `execution_preparation_passed / thirty_slots_authorized / zero_slots_issued`

## 結論

Candidate187の初回Target gateは、固定6ケース各iteration 1〜5、合計30 slotを発行できる直前まで準備できた。保存済みCandidate173問題資格確認resultを基準に、prompt identity以外の互換条件を`preflight-comparison`で照合し、30 slotすべてが承認された。

Candidate187 bundle、profile、Rating v14、固定Layer 1、6 template、30 capsule、global planおよびcomparison preflight receiptは一致した。frozen setとcapsuleへprivate oracle、期待terminal、期待review件数、過去Candidate結果またはreject済みcontractが混入していない。評価runはまだ一件も発行していない。

一次監査票は`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate187-review-admission-proof-obligation-targeted-n5-20260812-r1/execution-preparation-audit-r1.json`に保存した。

## 基準resultと互換性

- reference result ID: `5212c5bdb59043a2b759068826792e3f`
- reference result content SHA-256: `f3c8da34ff32d119fc8a156916c2713b7642f5cfb02dcddfb64a2565e5df861b`
- compatibility key: `e6ddf161cac04abfea912d094059397d50c689cd476e3a27263354addf1d48fe`
- frozen set SHA-256: `e8da310d71c5b5c2a478dc39172898137f75a437276d27101b8dadeb5aa91e26`
- frozen set identity SHA-256: `736421076b89577846e5618102a1bad30fdd9b495548ff1ba9e30b923109b438`

Candidate173のatomic runはCandidate187へ再利用していない。保存済みresultとLayer 1は、Evaluation set、fixture、TaskSpec、rating、model、reasoning、runtime、permissionおよびexecutor条件を照合する基準としてだけ使用した。新規発行対象はCandidate187の30 slotだけである。

## 固定identity

- profile SHA-256: `d4c26242a33d333c558b1b2a2461b324a6fe788eeeef0e30a3b190a68e74fe8f`
- rating contract SHA-256: `9d01b7ee77bbc7b6e5bde23f57bafbcf304f4a82020da5c3150b7ffb129011b1`
- Candidate187 bundle SHA-256: `189a7a11615511a3341646e24ecbffb61bb278fc6652c2db492648515d797fbd`
- Candidate187 manifest file SHA-256: `73c32e01bce68ad85b9857b3a7c5c3ea1d0dd47f8e9401d7b574fcdaa917adaa`
- comparison generation SHA-256: `32dd354886378306d31bf7de210180d4592a2616721883dfe55e4cc519f51c9e`
- comparison preflight file SHA-256: `748ba3b72b0fa28ce950e2f13936abd818507e02987368c9603c1ad645751304`
- global plan SHA-256: `d5957a2767ee8477cadfd60e1c8abd33764ad4248699619e6909ba88a7ef4fdb`
- template manifest SHA-256: `5285c245e0a76d7a9a1d50f0e77a0514de111e96b4ae689c7df71a8cba5121f6`
- capsule manifest SHA-256: `b6a6b914abe827cd16f87fdbd69c6b805387c045982301c68ea6ecba8141a570`

template／capsule manifest hashは、準備rootからの相対pathと各file SHA-256を辞書順に並べたcanonical JSONのSHA-256である。

## 確認内容

1. 6 templateと30 capsuleのcomparison conditionsがCandidate187 profileへ完全一致した。
2. prompt identity、bundle hashおよびprompt bundle pathがCandidate187 manifestへ一致した。
3. `TC-TPO01`〜`TC-TPO06`とiteration 1〜5の30組が重複なく一件ずつ存在した。
4. global planの30 jobsとcapsule集合が一致した。
5. preflight receiptに固定された30 capsule hashが実体と一致した。
6. frozen setと30 capsuleにprivate oracle、期待値、過去Candidate結果またはreject済みcontractがなかった。
7. comparison preflightは`ready`、authorized 30、issued 0だった。

## 境界

これは実行可能性、互換性および入力固定の監査であり、Candidate187のquality、mechanism、改善、採用、releaseまたはprojectionの結果ではない。次に許可される操作は、固定global planのCandidate187 30 slotを発行することだけである。発行後にLayer 1、profile、template、capsule、planまたはpreflight receiptを変更しない。

## 状態

`execution_preparation_passed / reference_compatibility_verified / candidate187_only_thirty_slots / authorized_thirty / issued_zero / private_boundary_passed / ready_for_targeted_execution`

## 後続実行

本監査で固定したglobal planは変更せず後続で発行され、30 / 30 valid、除外0件、外部エラー0件で完了した。本節は実行前監査の当時状態を上書きせず、実行後の導線だけを追加する。結果と現在判断は[`Candidate187 targeted r1`](../evaluations/results/candidate187-review-admission-proof-obligation-targeted-r1_2026-08-12.md)を正本とする。
