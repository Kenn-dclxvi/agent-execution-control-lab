# Candidate190 Standard14 N=5実行準備監査

> **位置づけ**: M7実行前監査／70件承認／発行0件

## 結論

Candidate190のStandard14全14ケース各5件、合計70件は、comparison preflightで`ready`となった。Candidate176の保存済みresultへbindし、prompt identity以外の互換条件を機械照合した。監査時点の発行数は0件である。

最初に参照したCandidate176実行rootの比較用Layer 1はF01 fixture digestが基準resultと一致せず、発行前に停止した。基準resultと一致する保存済みStandard14 reference Layer 1を特定して差し替えた。次にatomic capsuleへN管理用`repetition_condition`を含めた準備誤りもpreflightが拒否したため、atomic identityからその項目を除外してplanを再生成した。どちらの停止でもslotは発行しておらず、条件を緩和していない。

## 固定値

- reference result: `a0702207f03a4cb18c8b501329b74023`
- reference result content SHA-256: `d1e8e4a28d44b1a98e5773cc49158335516e7dd537f565994ba71a2a7b71100d`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- Candidate190 pool key: `4f894eb7973e77c12beec6bfb114d3039947c6b3c182aa474c14ad757ddf6ef9`
- evaluation set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- profile SHA-256: `24b36d14a9567cf73b927aabe4cd1db7a363d66cc7aeb0d46e18aa8e19597cf6`
- global plan SHA-256: `ebeebf75b987ce86a05ab7c0f5f4e6591e0529b94247c3fce7acbea12138973c`
- dispatch plan SHA-256: `4dce67c6000697ca93a784e0c0c571c7df1c6951eb40e6aafe1bf6c6ab62a14c`
- preflight receipt content SHA-256: `5f0c45eeebf9ce5d4cdf9bed8cbc60814b4b26a0e344a1129598d0fc203882f6`
- authorized slots: `70`
- issued slots: `0`
- max workers: `24`

一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate190-current-prior-review-result-admission-v14-medium-standard14-n5-cli0146-20260812-r1`に保存した。固定global planは`atomic-plan-r2/global-plan.json`、comparison preflight正本は`cycle/layer1/comparison-preflight.json`である。

## 入力封鎖

14 templateと70 capsuleにはprivate oracle、期待terminal、期待producer件数、過去Candidate結果、quality scoreまたは修正後の正解値を混入していない。case固有のTaskSpec、許可path、required commandおよび固定comparison conditionsだけをmodel-visible inputへ含めた。

## 境界

本監査は互換性、入力封鎖および発行範囲だけを証明する。Candidate190のStandard14品質または機序、採用、releaseおよびprojectionは証明しない。次に許可する操作は、固定70 slotの発行だけである。

## 状態

`execution_preparation_passed / standard14_reference_bound / all_fourteen_cases / authorized_70 / issued_0 / private_boundary_passed / ready_for_m7_execution`
