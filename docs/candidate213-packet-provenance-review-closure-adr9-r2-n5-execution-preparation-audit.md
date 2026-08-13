# Candidate213 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`、Candidate210 profileおよびCandidate147から保存されているADR9 r2 Layer 1へbindした。Candidate213の空poolに対する`plan-missing --desired-count 5`は、9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`および`verify-comparison-preflight`はすべて通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit/treeおよびtoken accountingはCandidate210保存resultと一致する。

現在状態は`preflight_ready / authorized_45 / issued_0`である。

## identity

- Candidate: `the-caption-3ce91a4-packet-provenance-review-closure-r1`
- bundle SHA-256: `64055b5aff47cb1372dcbca9f288d46abe4f6765e627db2545ac0275d2ae5663`
- profile: `candidate213-packet-provenance-review-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `a53674f16d81f6e2064da7486a88f21e4f4752f24b93e76923d75ba5dca4b2d0`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- reference compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `c6f0f93578e041740b4304b773960e3fbfe7e57879f628b96631696c19275a7f`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `23dedd31d9c5f11230f605ec018be3d0fd6b60e8065983ec74bc91dcd2f993b3`
- dispatch plan file SHA-256: `7c9fbe010e883020ddce04128836ac06b14f675dad17ec00c51062bc4f0c38f2`
- comparison preflight file SHA-256: `5f654872e34688e2b6dbbeefe099ec842d25b4cafba3f1a955ee9ba75e9dfc1d`

## 発行前証拠

- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: `TC-ADR01`から`TC-ADR09`、各revision `adversarial-design-review-r2`
- existing: 各0件、合計0件
- missing: 各5件、合計45件
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- configured M: `24`
- max attempts: `3`
- comparison preflight: `ready`
- authorized / issued before run: `45 / 0`

## 実行後gate

品質は45 / 45 valid、45 / 45 Score 4、terminal、artifact境界、reviewer cardinality、required commandおよび禁止情報境界の一致を要求する。

機序は、reviewerによるpacket投影元source再read 0件、ADR03からADR06のrepository read 0件、ADR07 / ADR09で必要な未投影paired-scope observation各5 / 5、review result admissionとeffect 30 / 30を要求する。exact JSONだけを要求せず、producer resultをallowed kind、subject、supportおよび使用inputへbindできるかを監査する。

一件でも品質または機序gateを満たさない場合は、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。有効な低品質runは除外または自動再実行せず保存する。

## 一次参照

- [Candidate213評価設計](candidate213-packet-provenance-review-closure-adr9-r2-n5-evaluation-design.md)
- [Candidate213 profile](../evaluations/profiles/candidate213-packet-provenance-review-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
