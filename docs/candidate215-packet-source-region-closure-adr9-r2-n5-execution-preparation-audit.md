# Candidate215 ADR9 r2 N=5 実行準備監査

## 結論

Candidate210保存result `9ac8eb53cf79463f9c7ae446c61b625a`とCandidate147保存Layer 1へbindした。Candidate215の空poolに対する`plan-missing --desired-count 5`は9ケース各5件、合計45件だけを発行対象へ固定した。

`prepare-comparison-layer1`、atomic plan作成、`preflight-comparison`および`verify-comparison-preflight`は通過した。prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、target commit/treeおよびtoken accountingはCandidate210保存resultと一致する。

発行前状態は`preflight_ready / authorized_45 / issued_0`だった。正規batch `r3`から45件を発行し、45 / 45 valid、除外0件で完了した。

## identity

- Candidate: `the-caption-3ce91a4-packet-source-region-closure-r1`
- bundle SHA-256: `da08a220485f0e48fe38165ec379ae52c60a0cbef9b225b92fc3edb7ff855a4f`
- profile: `candidate215-packet-source-region-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- profile SHA-256: `bba98ffac3f44253d81166854b7491e7337e04208c562876e061d7e67c38645e`
- reference result: `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool key: `04a012a30045314867b430fe63cd981d1fb62992d391de4814cc72741eb9b45f`
- comparison key: `e57ff13335daac3e76c8755cb32214bb62ad5f83a9742d756631e51876066938`
- global plan SHA-256: `8445b177f36b7274ddc367d797b9c528bfb9edebe5f5beceda0227e16a6477ae`
- dispatch plan SHA-256: `bdbfbafa35e3dfd7c9725c1e2eadf32ddbd4fb385b5ea1374ad93ca33384ac3b`
- comparison preflight SHA-256: `c4e464d02dfcdd1e96983f514220ab476e27f637a525207dabe0daadd24cff9d`
- execution root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate215-packet-source-region-closure-adr9-r2-n5-20260814-r3`

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

同名`r1`にはCandidate214 identityの旧preflightが残っており、`r2`では保存Layer 1の指定を誤ったため生成途中で停止した。どちらからもslotを発行していない。Candidate215の正規実行batchは`r3`だけとする。

## 実行後gate

品質は45 / 45 valid、45 / 45 Score 4および全成果境界一致を要求する。機序は投影元regionの重複read0件、region未知の同一container read0件、Candidate214誤停止経路の回復、root preread0件、ADR07 / ADR09の必要paired observation各5 / 5、review result admission / effect一致を要求する。

一件でも外れた場合はrepair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 実行結果

- requested / attempt / valid / excluded: `45 / 45 / 45 / 0`
- execution elapsed: `215.373`秒
- Score `4 / 1`: `41 / 4`
- result ID: `e459b816c1ae4b97b2a776252b6f3367`
- result content SHA-256: `5ee4eb09f40ac1bcac929cac9e0adbf22f0b83e4c732d59ca9ab9a12b642d5aa`
- state: `quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 一次参照

- [Candidate215評価設計](candidate215-packet-source-region-closure-adr9-r2-n5-evaluation-design.md)
- [Candidate215 profile](../evaluations/profiles/candidate215-packet-source-region-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate210保存result](../evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json)
