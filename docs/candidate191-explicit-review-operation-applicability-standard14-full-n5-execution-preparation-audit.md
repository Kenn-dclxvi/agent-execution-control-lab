# Candidate191 Standard14全14ケース N=5実行準備監査

> **位置づけ**: M7実行前監査／既存15件再利用／不足55件承認

## 結論

Candidate191のStandard14全14ケース各5件は、Candidate176の保存済みresultへbindしたcomparison preflightで`ready`となった。prompt identity以外の互換条件を機械照合し、既存のF02、F03、F04各5件を再利用して、不足11ケース各5件だけを発行対象へ固定した。

最初に参照したLayer 1はF01 fixture digestが基準resultと一致せず、slot発行前に停止した。基準resultと一致するCandidate190の保存済みLayer 1へ差し替え、条件を緩和せず別cycleでpreflightを通した。

## 固定値

- reference result: `a0702207f03a4cb18c8b501329b74023`
- reference result content SHA-256: `d1e8e4a28d44b1a98e5773cc49158335516e7dd537f565994ba71a2a7b71100d`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- Candidate191 pool key: `60cac4f9994f8d8e088ae044862a16760ad27ac5804d5f089ce04e7e7475a25e`
- evaluation set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- profile SHA-256: `18f2799502da7f33e238ba98edc1198f1ce3b151708849fab0755043a44b46a6`
- global plan SHA-256: `ee1144c8f77c023fd1e39edf94df82e79780a8b891da36cd5653a0f31a5436ca`
- dispatch plan SHA-256: `8309d5fc66b91762e2187d0f48369a18d7247e4e1afa1a07bf34034b52eeeddf`
- preflight receipt SHA-256: `5e9a4dc0eb0225363f8d025537f2cd18f286a9957fd04bb42cc4c9950b089355`
- reused slots: `15`
- authorized new slots: `55`
- max workers: `24`

一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-standard14-full-n5-20260812-r1`に保存した。固定global planは`atomic-plan-r2/global-plan.json`、comparison preflight正本は`cycle-r2/layer1/comparison-preflight.json`である。

## 入力封鎖

14 templateと55 capsuleにはprivate oracle、期待terminal、期待producer件数、過去Candidate結果、quality scoreまたは修正後の正解値を混入していない。case固有のTaskSpec、許可path、required commandおよび固定comparison conditionsだけをmodel-visible inputへ含めた。

## 境界

本監査は互換性、入力封鎖、再利用可能性および発行範囲だけを証明する。Candidate191のStandard14品質または機序、採用、releaseおよびprojectionは証明しない。

## 状態

`execution_preparation_passed / standard14_reference_bound / all_fourteen_cases / reuse_15 / authorized_55 / private_boundary_passed`
