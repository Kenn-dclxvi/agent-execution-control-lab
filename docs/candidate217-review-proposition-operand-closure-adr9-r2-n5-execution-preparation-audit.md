# Candidate217 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate217の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、atomic plan作成、`preflight-comparison`および`verify-comparison-preflight`は通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit/treeおよびtoken accountingはCandidate210保存resultと一致する。

発行前状態は`preflight_ready / authorized_45 / issued_0`である。

この発行前監査の後に45件を発行し、45 / 45 valid、除外0件で完了した。結果は品質・機序gateを通過しなかったため停止した。発行前互換性が成立したことを、評価品質またはCandidate採用へ昇格しない。

## identity

- Candidate: `the-caption-3ce91a4-review-proposition-operand-closure-r1`
- bundle SHA-256: `627c8e27541e0b6ab96129e19121def1a43a289d903222d8260d52cf66507056`
- profile: `candidate217-review-proposition-operand-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `9fda9c3b0960cec76350f1dee325b2b3fd1eeb9d748ce784a84ab5e54144b2a6`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `d227b6ff53d2bd960a5bc4e9719e1ab596a0a426607635dea864170b02ef29c5`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `4f499d3061caf7ee76dbeed53053e3ed15daf60bc18544a72edbc584dc299bc7`
- dispatch plan file SHA-256: `0220ada61a661497b84d44871085ab6b0187028bc2bd2c1dfd92eb1291f016e5`
- comparison preflight file SHA-256: `2394d23eac55fe34147d86748c15f3f494e1b7af9579dde890020b19c9001d72`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate217-review-proposition-operand-closure-adr9-r2-n5-20260814-r1`

## 発行前証拠

- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: `TC-ADR01`から`TC-ADR09`
- existing: 各0件、合計0件
- missing: 各5件、合計45件
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- configured M: `24`
- max attempts: `3`
- comparison preflight: `ready`
- authorized / issued before run: `45 / 0`

## 実行後gate

品質は45 / 45 valid、45 / 45 Score 4および全成果境界一致を要求する。機序は既取得direct operand再取得0件、必須operandのexactly one supply binding、ADR03〜ADR06の期待terminal 20 / 20、ADR07 / ADR09のpaired-only route各5 / 5、projection conflict・誤paired read・root preread各0件、review result admission / effect一致を要求する。

一件でも外れた場合はrepair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 一次参照

- [Candidate217評価設計](candidate217-review-proposition-operand-closure-adr9-r2-n5-evaluation-design.md)
- [Candidate217 profile](../evaluations/profiles/candidate217-review-proposition-operand-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
