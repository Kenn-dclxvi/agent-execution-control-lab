# Candidate218 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate218の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、atomic plan作成、`preflight-comparison`および`verify-comparison-preflight`は通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit / treeおよびtoken accountingはCandidate210保存resultと一致する。

発行前状態は`preflight_ready / authorized_45 / issued_0`である。

## identity

- Candidate: `the-caption-3ce91a4-review-input-carrier-ownership-r1`
- bundle SHA-256: `04c2e670eabf659b24139429246ad1e640e5162297b4fd999a0565efd8762f73`
- profile: `candidate218-review-input-carrier-ownership-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `b881fd5b977ba5d986549b13922e01e0a94f93d4e2bb29e5819951206f2d47d5`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `2b47bd7e8a199d4b558dc1b2b493bb27c46bef8baae99efd108a5224bb76999d`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan file SHA-256: `457df4e884e773834064729fb03dc80abc6319070685c7474382b02caf0a1070`
- dispatch plan content SHA-256: `8a09383fc4ac89d882e075e69597cb7d2669c1aa657e508729e9e619f2560b2c`
- comparison preflight file SHA-256: `4e14d21dde9a3506a0163c532272791419a6275bee0954e17539e2ea1f8c9424`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate218-review-input-carrier-ownership-adr9-r2-n5-20260814-r1`

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

品質は45 / 45 valid、45 / 45 Score 4および全成果境界一致を要求する。機序はmixed-owner root admission 0件、root / reviewer二重消費0件、root-controlまたはpacket禁止inputの誤配送0件、ADR03〜ADR06の期待terminal 20 / 20、ADR07 / ADR09のpaired-only route各5 / 5、review result admission / effect一致を要求する。

一件でも外れた場合はrepair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 一次参照

- [Candidate218評価設計](candidate218-review-input-carrier-ownership-adr9-r2-n5-evaluation-design.md)
- [Candidate218 profile](../evaluations/profiles/candidate218-review-input-carrier-ownership-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
