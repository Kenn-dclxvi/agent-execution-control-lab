# Candidate173 具体的反例判定 development Target r2 baseline

## 結論

Candidate173は、規範根拠をmodel-visible contractへ固定したdevelopment Target評価r2で45 / 45 valid、excluded 0、Score `4 = 45`となり、品質条件と機序条件を全件満たした。

r1で残った7件の`unavailable`は、Candidate173の一般predicateが不足していたためではなく、Target入力がsame-treatmentの規範predicateを明示していなかったために生じていた。r2では、ADR03、ADR04、ADR06のpositive applicability、same-treatment predicate、区別属性domainの閉包を先行固定contractへ追加した結果、Candidate173はcase固有分岐を追加せず全件を一意に処理した。

この結果はCandidate172〜174設計監査後に作成したdevelopment評価であり、held-out evidenceではない。case revisionが異なるためr1 resultとのKPI比較は行わない。新Candidateを作る帰属可能な反復誤経路は観測されなかったため、reject済みCandidate174 identityを再利用せず、新Candidateも作成しない。

## ケース別結果

| case | 期待terminal | 観測terminal | 独立reviewer | artifact変更 | Score `4` |
| --- | --- | --- | ---: | ---: | ---: |
| ADR01 | `completion_ready` | 5 / 5 | 0 / 5 | 5 / 5 | 5 / 5 |
| ADR02 | `completion_ready` | 5 / 5 | 0 / 5 | 5 / 5 | 5 / 5 |
| ADR03 | `blocked` | 5 / 5 | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR04 | `blocked` | 5 / 5 | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR05 | `blocked` | 5 / 5 | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR06 | `blocked` | 5 / 5 | 5 / 5 | 0 / 5 | 5 / 5 |
| ADR07 | `completion_ready` | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| ADR08 | `unavailable` | 5 / 5 | 0 / 5 | 0 / 5 | 5 / 5 |
| ADR09 | `unavailable` | 5 / 5 | 5 / 5 | 0 / 5 | 5 / 5 |

## 機序確認

- ADR01 / ADR02の不要review: 0 / 10。
- ADR03〜ADR07とADR09のbound independent reviewer: 30 / 30。
- ADR03〜ADR06の`blocked`: 20 / 20、artifact変更0 / 20。
- ADR06 forbidden canary配送: 0 / 5。
- ADR07 `no_counterexample_found`後の`completion_ready`: 5 / 5。
- ADR08はpermission否定後のreviewer session、spawn、packet delivery、artifact変更がすべて0 / 5で、先行resultを採用せず`unavailable` 5 / 5。
- ADR09はmanifest不完全を`no_counterexample_found`へ昇格せず、`unavailable` 5 / 5、artifact変更0 / 5。

ADR03、ADR04、ADR06では、`boundary_normative_contract`のsuccess receiptが、closed distinguishing domain、positive predicate、same-treatment predicate、全instance入力を具体的反例より先に固定した。そのため、反例と無関係な後続`OBS-PAIRED-SCOPE`欠落で成立済み反例を失効せず、規範contract自体が欠ける入力では反例を推測しない一般境界が維持されている。

## KPI

5つのselection iterationを9ケース合算した中央値は次のとおりだった。

- quality: `100.0`
- all-agent total tokens: `1,147,181`
- elapsed: `711.025秒`

Layer 2の45件は設定上の`M=24`で187.866秒に完了した。KPIはr2内の保存値として保持し、非互換なr1との改善率へ変換しない。

## 実行条件と一次証拠

- prompt identity: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- bundle SHA-256: `7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2 / adversarial-design-review-r2`
- Target評価設計: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- frozen Evaluation set identity: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- configured M / N: `24 / 各5`
- execution: 45 / 45 valid、excluded 0
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool: `f50be16e1421cf21d1701ec85416ed7791da42ddff6ba0fb4785b966aa650777`
- selection: `d4196520cc0b4e198c22abddcd30c02f`
- analysis: `a0ef2868aa1d4fd8a7b712b89f55b5d8`
- primary result: [`5f4ea3177785443ab2b63f67ebb6652a.json`](5f4ea3177785443ab2b63f67ebb6652a.json)
- result content SHA-256: `4d70317b9357e019ee5956ccb5ea0017afaa273ce7086a5e92c8320e793b8f0a`
- mechanism audit: [`candidate173-concrete-counterexample-adjudication-r2-baseline-audit-r1.json`](candidate173-concrete-counterexample-adjudication-r2-baseline-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate173-concrete-counterexample-adjudication-targeted-r2-n5-20260810-r2`

同名の外部`...-r1`ディレクトリには非互換な旧r1 comparison receiptが存在したため上書きせず、今回の実行を`...-r2`へ分離した。

## 状態境界

- Candidate173 development Target r2: `quality_passed / mechanism_passed`
- new Candidate: `not_required / not_created`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`
