# Candidate211 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`、Candidate210 profileおよびCandidate147から保存されているADR9 r2 Layer 1へbindした。Candidate211の空poolに対する`plan-missing --desired-count 5`は、9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`および`verify-comparison-preflight`はすべて通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit/treeおよびtoken accountingはCandidate210保存resultと一致する。

現在状態は`preflight_ready / authorized_45 / issued_0`である。

## identity

- Candidate: `the-caption-3ce91a4-required-scope-review-interface-r1`
- bundle SHA-256: `40b9c14cadf390a02fa242469f0e0c8bb6fcb53d94de239ca039b74321e265b9`
- profile: `candidate211-required-scope-review-interface-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `cfeaecf6a6199ebda987254c479b89e0f9fc7f56bbfa5917296017142eede297`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- reference compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `15cd0ac5f19dcaa1b807d19d2816d0da34317b401816b2403dfb50eb8295a0d1`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `830a93018c3c3a373188c44774c90a4fcdccdcb043f4f3627c302455f8d74128`
- dispatch plan SHA-256: `bc10f16169151e0fd713e76cb614db3b7f56db747bed2bdf8fc4ad33eb6a3339`
- comparison preflight file SHA-256: `e488b485287e5044b2155b41192d063867e2d4669f976f123e1ae1b43cd1b688`

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

最初のLayer 1準備では、Candidate210の比較cycle内`layer1`をreference Layer 1として渡したため、そこに含まれる比較receiptと新しいwrite-once receiptが衝突した。この不完全cycleは別名へ隔離し、Candidate210の`comparison-generation.json`が指すCandidate147保存Layer 1を正しいreferenceとして新しいcycleを生成した。評価slotは一件も発行されていない。

## 実行後gate

品質は45 / 45 valid、45 / 45 Score 4、terminal、artifact境界、reviewer cardinality、required commandおよび禁止情報境界の一致を要求する。

機序は、ADR03からADR06のpacket-counterexample 20件のrepository read 0件、packet projection元source再read 0件、必須scope外target read 0件、ADR07の必要direct observation 5 / 5、ADR09のmissing observation 5 / 5、review result admission 30 / 30、exact external disposition 30 / 30を要求する。

一件でも品質または機序gateを満たさない場合は、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。有効な低品質runは除外または自動再実行せず保存する。

## 一次参照

- [Candidate211評価設計](candidate211-required-scope-review-interface-adr9-r2-n5-evaluation-design.md)
- [Candidate211 profile](../evaluations/profiles/candidate211-required-scope-review-interface-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
