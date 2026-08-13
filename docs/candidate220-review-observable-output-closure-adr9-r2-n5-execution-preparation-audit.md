# Candidate220 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate220の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、atomic plan作成、`preflight-comparison`および`verify-comparison-preflight`は通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit / treeおよびtoken accountingはCandidate210保存resultと一致する。

発行前状態は`preflight_ready / authorized_45 / issued_0`である。

## identity

- Candidate: `the-caption-3ce91a4-review-observable-output-closure-r1`
- bundle SHA-256: `739719baebd5f7c993fc5f6e1bc9623f145617724ecc65cbca5a82da6ee47654`
- profile: `candidate220-review-observable-output-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `3f0a5ca92e90033e9011f6140539dcdc12dfa13c6b46f0da54f061ba562216fd`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `4ff3a42b43b2bf060bb175ceccb84666a606397bd40e4891d271261adcedb83b`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan file SHA-256: `16fbe9f05794e33f1a5baf6e7c11d2effeb87f4a631aea066dbb405d9ae86991`
- dispatch plan content SHA-256: `726f58245d578acaffb10f161beaa61cc41ff4e8f3834592fd5e90b26d7b34b1`
- comparison preflight file SHA-256: `053c440fb752f9dbb9cdf8b433d615b72acd901c4c18a5676e89f4ae8b0b0c99`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate220-review-observable-output-closure-adr9-r2-n5-20260814-r1`

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

品質は45 / 45 valid、45 / 45 Score 4および全成果境界一致を要求する。機序はroot mixed-owner observable result 0件、二重消費0件、不要reviewer 0件、ADR03〜ADR06の期待terminalと必要観測20 / 20、ADR07 / ADR09のpaired-only route各5 / 5およびreview result admission / effect一致を要求する。

一件でも外れた場合はrepair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 一次参照

- [Candidate220評価設計](candidate220-review-observable-output-closure-adr9-r2-n5-evaluation-design.md)
- [Candidate220 profile](../evaluations/profiles/candidate220-review-observable-output-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
