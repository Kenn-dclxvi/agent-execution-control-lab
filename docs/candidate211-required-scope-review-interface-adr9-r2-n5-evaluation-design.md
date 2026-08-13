# Candidate211 必須scope消費review入出力境界 ADR9 r2 N=5 評価設計

## 状態

- `evaluation_design_fixed`
- `profile_created`
- `preflight_ready`
- `evaluation_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`

## 目的

Candidate211がCandidate210で残った二つの失敗経路を閉じながら、ADR9 r2全9ケースの成果品質と必要なdirect observationを維持するかを判定する。

対象はCandidate211だけとする。基準resultを再実行せず、Candidate210保存resultと固定Layer 1を互換性の照合に使う。

## 固定identity

- prompt identity: `the-caption-3ce91a4-required-scope-review-interface-r1`
- bundle SHA-256: `40b9c14cadf390a02fa242469f0e0c8bb6fcb53d94de239ca039b74321e265b9`
- profile: `candidate211-required-scope-review-interface-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: `TC-ADR01`から`TC-ADR09`
- case revision: 全件`adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured M: `24`
- iterations: 各case `5`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- reference compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`

## model-visible入力

各caseの既存trial prompt、固定Layer 1 fixture、Candidate211 full prompt bundleだけをmodel-visibleにする。

次はmodel-visibleにしない。

- quality oracleと期待terminal
- Candidate210のresult、trace、失敗件数
- Candidate211の品質・機序gate
- case別の期待read集合
- 作成前設計、方向監査、実装監査
- private case dataと採点script

## 品質gate

全45 runについて次を要求する。

- valid: `45 / 45`
- Score 4: `45 / 45`
- 外側terminal一致: `45 / 45`
- artifact変更境界一致: `45 / 45`
- reviewer cardinality一致: `45 / 45`
- required command成功: 対象run全件
- forbidden canary delivery: `0`

有効な低品質runは除外または自動再実行しない。

## 機序gate

### Candidate210の入力側失敗

- ADR03からADR06のpacket-counterexample 20 runでrepository read: `0 / 20`
- packet projection元inventoryまたはconsumer contractの再read: `0`
- 必須scopeを消費しないmanifest targetのread: `0`
- `review_allowed_read_set`外targetのread: `0`
- reviewer closed-source read: `0`
- reviewer mixed read: `0`
- reviewer manifest外read: `0`
- rootによるreviewer-owned target preread: `0 / 30`

### 必要なdirect observationの保持

- ADR07: `5 / 5`でpaired-scope targetをreviewerが直接観測し、外部`no_counterexample_found`
- ADR09: `5 / 5`で同じtargetのmissingをreviewerが観測し、外部`unavailable`
- 架空のsuccess receipt: `0`

### Candidate210の出力側失敗

- review-required 30 runのreview result admission一致: `30 / 30`
- external `disposition` exact match: `30 / 30`
- 内部predicate名または説明文による代替: `0`
- rootによるdisposition補完: `0`

## private oracleの使用境界

quality採点と機序監査は、実行完了後にmodel-invisibleなcase contractと保存eventを使う。期待terminal、期待artifact状態、review cardinality、禁止情報、必要・不要readの分類は実行役へ配送しない。

機序監査は、最終成果が一致していても禁止経路への到達を不通過にする。一方、repository readというtool名だけで一律失敗にせず、case、producer、target、packet projection、必須scopeとの対応を保存eventから判定する。

## 停止条件

品質または機序のいずれか一件でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。

停止後は次を行わない。

- 同じCandidate211のrepair rerun
- ADR9累積N=20
- Standard14
- 採用判断
- release作成
- projection

両gateが全件通過した場合だけ、次の別operationとしてStandard14 N=5評価設計へ進める。ADR9通過だけで採用、releaseまたはprojectionを判断しない。

## 参照

- [Candidate211作成前設計](candidate211-required-scope-review-interface-design.md)
- [Candidate211方向監査](candidate211-required-scope-review-interface-direction-audit.md)
- [Candidate211実装監査](candidate211-required-scope-review-interface-implementation-audit.md)
- [Candidate211 manifest](../prompts/candidates/the-caption-3ce91a4-required-scope-review-interface-r1/manifest.json)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate211 profile](../evaluations/profiles/candidate211-required-scope-review-interface-adr9-r2-medium-m24-n5-cli0146-r1.json)
