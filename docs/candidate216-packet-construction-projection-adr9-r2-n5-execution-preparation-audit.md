# Candidate216 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate216の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、atomic plan作成、`preflight-comparison`および`verify-comparison-preflight`は通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit/treeおよびtoken accountingはCandidate210保存resultと一致する。

発行前状態は`preflight_ready / authorized_45 / issued_0`だった。固定45件を発行し、45 / 45 valid、除外0件で完了した。

## identity

- Candidate: `the-caption-3ce91a4-packet-construction-projection-r1`
- bundle SHA-256: `77a0f660d7066bee128785814517a7899d18086e0c0617b9bc90feebe3995eb6`
- profile: `candidate216-packet-construction-projection-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `fb1a654bdf190abb9346cabcda1dc470eb74ded79181ba151c9bf4d6f678f2b0`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `e60c43412542cf22efa1507cf620a7a129910bcbeaaaec12e7ae7389c99d7fe1`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `c23aea965c3b6e646643b7492aa6709e76911e34a8e564b2f76849f83a92cb3a`
- dispatch plan SHA-256: `97c2a8b4835f29bd5bc03f2ed8bcc106fff7417e3bf36b946c8234bfa551844f`
- comparison preflight SHA-256: `f3d9bdb2e06926fdf6032cb457f05ba0efe453744718e1731142e39262ffb8a3`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate216-packet-construction-projection-adr9-r2-n5-20260814-r1`

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

品質は45 / 45 valid、45 / 45 Score 4および全成果境界一致を要求する。機序はpacket projectionの重複またはwhole-container read 0件、ADR03〜ADR06の期待terminal 20 / 20、ADR07 / ADR09のpaired-only route各5 / 5、root preread 0件、review result admission / effect一致を要求する。

一件でも外れた場合はrepair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 実行結果

- requested / attempt / valid / excluded: `45 / 45 / 45 / 0`
- execution elapsed: `213.866`秒
- Score `4 / 1`: `44 / 1`
- result ID: `cb903e23e6a14ebea156351c16963cad`
- result content SHA-256: `60faac4a73f7af50d47b21d3429c455eeb6bad043598163f6c47dc3235eb6513`
- state: `quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 一次参照

- [Candidate216評価設計](candidate216-packet-construction-projection-adr9-r2-n5-evaluation-design.md)
- [Candidate216 profile](../evaluations/profiles/candidate216-packet-construction-projection-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
