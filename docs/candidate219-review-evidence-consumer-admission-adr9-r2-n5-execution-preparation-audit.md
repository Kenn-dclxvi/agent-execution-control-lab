# Candidate219 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate219の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、atomic plan作成、`preflight-comparison`および`verify-comparison-preflight`は通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit / treeおよびtoken accountingはCandidate210保存resultと一致する。

発行前状態は`preflight_ready / authorized_45 / issued_0`である。

## identity

- Candidate: `the-caption-3ce91a4-review-evidence-consumer-admission-r1`
- bundle SHA-256: `5ec4728576b24b8dd4aceb45903cae6f9fe0f46b58bf382a3cbe4c50cdfabf95`
- profile: `candidate219-review-evidence-consumer-admission-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `e8d952c2fae17246dd2ced76ba064d40c8f93bac0dcd0608e3db543fba1363be`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `98749deeeab519aef85a24ccfc15e10faf453a38527da7eca009021858a927c3`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan file SHA-256: `1b225a52b6729a0249eeb7a1a1bb609ed2c7ef9512ba10f3a34a480dccc222ec`
- dispatch plan content SHA-256: `cf1b2ff0815818252bf89539b9b61d8d04cc1e11b00513090ef0b525cc79a3c2`
- comparison preflight file SHA-256: `de5093ca071e307a005a471c259cfbc91ce851548fbcaeb70900ff7e9d08ca0d`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate219-review-evidence-consumer-admission-adr9-r2-n5-20260814-r1`

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

品質は45 / 45 valid、45 / 45 Score 4および全成果境界一致を要求する。機序はconsumer外result 0件、root / reviewer二重消費0件、packet禁止inputのroot取得・配送0件、ADR03〜ADR06の期待terminal 20 / 20、ADR04 terminal support後のmissing伝播0件、ADR07 / ADR09のpaired-only route各5 / 5、review result admission / effect一致を要求する。

一件でも外れた場合はrepair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 一次参照

- [Candidate219評価設計](candidate219-review-evidence-consumer-admission-adr9-r2-n5-evaluation-design.md)
- [Candidate219 profile](../evaluations/profiles/candidate219-review-evidence-consumer-admission-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
