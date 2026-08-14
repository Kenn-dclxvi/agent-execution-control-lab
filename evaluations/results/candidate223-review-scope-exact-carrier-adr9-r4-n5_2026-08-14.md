# Candidate223 review scope exact carrier ADR9 r4 N=5結果

## 結論

Candidate223は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 43 / 2`で、artifact境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件だった。

root deliveryとscope外reviewer readの閉鎖は成立した。rootは45 / 45件で列挙済みexact projectionだけを受領し、whole-container、reviewer-owned projectionおよびunproven projectionは各0件だった。起動したreviewerはADR03からADR06でinventory / contractsだけ、ADR07とADR09でpaired scopeだけを読み、scope外direct readは0件だった。

しかし、目的である必要reviewの完遂は28 / 30件に留まった。ADR06の2件で、TaskSpecが`SCOPE-CONTRACT`へ要求した`OBS-BOUNDARY-LEDGER`がsource内finite evidence manifestに存在しないと判定され、reviewer開始前に`unavailable`となった。したがってCandidate223は`quality_failed / mechanism_failed / stopped`である。有効runを保持し、repair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-scope-exact-carrier-r1`
- bundle SHA-256: `85473ee6fc8d50c1e9946b2fb4d328fae68a260ade5380e9c32501ed2fbd9320`
- profile: `candidate223-review-scope-exact-carrier-adr9-r4-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r4`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r13`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- execution: requested 45、valid 45、excluded 0、attempt 45
- runner elapsed: 269.709秒

## 必要reviewと配送境界

| 指標 | 結果 |
| --- | ---: |
| 必要reviewer起動 | 28 / 30 |
| review result admission一致 | 43 / 45 |
| review result effect一致 | 43 / 45 |
| 期待terminal一致 | 43 / 45 |
| root exact projection | 45 / 45 |
| root whole-container delivery | 0 |
| root reviewer-owned delivery | 0 |
| packet caseのpaired read | 0 |
| paired caseのdesign-container read | 0 |
| reviewer whole-container read | 0 |
| review不要時のreviewer read | 0 |

## 得られた手がかり

scope別exact carrierは、C214から残っていたroot bootstrap deliveryと、共通target和集合が許したscope外readを同時に閉じた。失敗はこの配送構造ではなく、source外対応表のobservation identity整合性にある。

`OBS-BOUNDARY-LEDGER`はTaskSpec r13が新設したpacket observation identityだが、source内finite evidence manifestには存在しない。Candidate本文はcontractとmanifestの不一致時にreviewを開始しないため、ADR06の2件が安全停止した。他の43件がこの不整合を無視して進んだことを次案の根拠にはしない。

次案では、source内manifestに存在しないobservation identityをrequired scopeへ割り当てない。`SCOPE-CONTRACT`は既存manifestの`OBS-DESIGN`へbindし、boundary ledgerはobservation identityを新設せずpacket-carried supporting valueとして保持する。この対応を静的に全case検証できなければ`candidate_not_created`とする。成功runのread順、判断順またはcase別期待結果は追加しない。

## KPI

| KPI | Candidate223 |
| --- | ---: |
| `quality_score` median | 100.0 |
| all-agent `total_tokens` median | 1,135,039 |
| `elapsed_seconds` median | 869.370 |

中央値が100でも、必要review 2件が欠落したため品質・機序通過とは扱わない。

## 状態

`candidate223_ADR9_completed / valid_45 / score4_43 / score1_2 / quality_failed / mechanism_failed / stopped / next_candidate_not_created / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠

- execution archive SHA-256: `e64475e450718f3d85de8c320e10383b6400eaa5521c76cd20b41665ff4e742c`
- execution seal SHA-256: `38af0ae5f504a76e989d9d2ef2af0b044af671060c0d4704ae99e9e37433f2a5`
- compact後の最終archive SHA-256: `0dedb74daa8467dfe266524d5bb85a91680e8c96c8e9a7031012667d65301f88`
- compact後の最終manifest SHA-256: `c17a85908c18141da7490a56a176ad2ea0a90115ed97f4fd710ad8316d42fc5e`

## 一次アーティファクト

- [登録result](abac73500213486e80469c7066dbdc43.json)
- [品質監査](candidate223-review-scope-exact-carrier-adr9-r4-n5-quality-audit-r1.json)
- [基本機序監査](candidate223-review-scope-exact-carrier-adr9-r4-n5-mechanism-base-audit-r1.json)
- [配送境界監査](candidate223-review-scope-exact-carrier-adr9-r4-n5-delivery-boundary-audit-r1.json)
- [Candidate223設計](../../docs/candidate223-review-scope-exact-carrier-design.md)
- [実行準備監査](../../docs/candidate223-review-scope-exact-carrier-adr9-r4-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate223-review-scope-exact-carrier-implementation-audit.md)
