# Candidate213 packet provenance review closure ADR9 r2 N=5 評価設計

## 状態

- `evaluation_design_fixed`
- `profile_created`
- `preflight_ready`
- `evaluation_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`

## 目的

Candidate213が、packetへsemantic valueを供給したrepository source identityをreviewer起動前に閉鎖集合へ固定し、値の意味や命題名を判断せず、同じreviewerによる投影元sourceの再readを禁止するかを判定する。同時に、ADR9 r2全9ケースの成果品質と、未投影sourceに対する必要なdirect observation経路を維持するかを確認する。

対象はCandidate213だけとする。基準resultを再実行せず、Candidate210保存resultと固定Layer 1を互換性の照合に使う。Candidate211とCandidate212のresultは失敗経路の分析証拠であり、比較基準にしない。

## 固定identity

- prompt identity: `the-caption-3ce91a4-packet-provenance-review-closure-r1`
- bundle SHA-256: `64055b5aff47cb1372dcbca9f288d46abe4f6765e627db2545ac0275d2ae5663`
- profile: `candidate213-packet-provenance-review-closure-adr9-r2-medium-m24-n5-cli0146-r1`
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

各caseの既存trial prompt、固定Layer 1 fixture、Candidate213 full prompt bundleだけをmodel-visibleにする。

次はmodel-visibleにしない。

- quality oracleと期待terminal
- Candidate210からCandidate212までのresult、trace、失敗件数
- Candidate213の品質・機序gate
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

### packet投影元sourceの閉鎖

- reviewerによるpacket投影元repository sourceの再read: `0`
- ADR03からADR06のpacket-counterexample 20 runでreviewer repository read: `0 / 20`
- packet projection元inventoryまたはconsumer contractの再read: `0`
- reviewer closed-source read: `0`
- reviewer mixed read: `0`
- reviewer manifest外read: `0`
- rootによるreviewer-owned target preread: `0 / 30`
- source identity欠落時のreviewer起動、reviewerによる閉鎖集合の推測、拡張または再構成: `0`

packet値とrepository fieldの意味上の対応を要求しない。保存eventから、reviewerが読んだtarget identityと、trial promptでpacketへsemantic valueを供給したsource identityを直接照合する。

### 必要な未投影direct observationの保持

- ADR07: `5 / 5`で必要なpaired-scope targetだけをreviewerが直接観測し、`no_counterexample_found`
- ADR09: `5 / 5`で同じtargetのmissingだけをreviewerが観測し、`unavailable`
- 架空のsuccess receipt: `0`

### producer resultのadmissionとeffect

- review-required 30 runのreviewer cardinality一致: `30 / 30`
- review result admission一致: `30 / 30`
- disposition一致: `30 / 30`
- rootによるjudgement、certificate、missing observationまたはresult kindの補完: `0`
- `no_counterexample_found`以外からartifact変更へ進むrun: `0`

外部resultをexact JSONだけに限定しない。producer terminal resultが、allowed kind、subject、support、使用inputおよびforbidden input不使用へbindできるかを保存eventから判定する。

## private oracleの使用境界

quality採点と機序監査は、実行完了後にmodel-invisibleなcase contractと保存eventを使う。期待terminal、期待artifact状態、review cardinality、禁止情報、必要・不要readの分類は実行役へ配送しない。

機序監査はrepository readを一律失敗にせず、read targetがpacket構築に使用済みのsourceか、未投影でterminal dispositionを分けるために必要なsourceかを判定する。

## 停止条件

品質または機序のいずれか一件でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。

停止後は次を行わない。

- 同じCandidate213のrepair rerun
- ADR9累積N=20
- Standard14
- 採用判断
- release作成
- projection

両gateが全件通過した場合だけ、次の別operationとしてStandard14 N=5評価設計へ進める。ADR9通過だけで採用、releaseまたはprojectionを判断しない。

## 参照

- [Candidate213作成前設計](candidate213-packet-provenance-review-closure-design.md)
- [Candidate213方向監査](candidate213-packet-provenance-review-closure-direction-audit.md)
- [Candidate213実装監査](candidate213-packet-provenance-review-closure-implementation-audit.md)
- [Candidate213 manifest](../prompts/candidates/the-caption-3ce91a4-packet-provenance-review-closure-r1/manifest.json)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate213 profile](../evaluations/profiles/candidate213-packet-provenance-review-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
