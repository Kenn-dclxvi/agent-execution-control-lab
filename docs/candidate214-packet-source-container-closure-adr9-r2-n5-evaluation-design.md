# Candidate214 packet source container closure ADR9 r2 N=5 評価設計

## 状態

- `evaluation_design_fixed`
- `profile_created`
- `preflight_ready`
- `evaluation_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- `Standard14_not_started`

## 目的

Candidate214が、実際に構築したpacket itemだけへsource container receiptを固定し、値の意味や命題名を判断せず、同じcontainerのfield、selectorまたは部分抽出をreviewer readから閉じるかを判定する。同時に、未投影manifest sourceをrootのpacket readiness readへ昇格せず、ADR9 r2全9ケースの成果品質と必要なdirect observation経路を維持するかを確認する。

対象はCandidate214だけとする。基準resultを再実行せず、Candidate210保存resultと固定Layer 1を互換性の照合に使う。Candidate200、Candidate202およびCandidate213のresultは失敗経路と正常経路の分析証拠であり、比較基準にしない。

## 固定identity

- prompt identity: `the-caption-3ce91a4-packet-source-container-closure-r1`
- bundle SHA-256: `3acb157b05719ca0ebca1d1f3ecbb6f76a53965686532833e1bbbbabd9b9815c`
- profile: `candidate214-packet-source-container-closure-adr9-r2-medium-m24-n5-cli0146-r1`
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

各caseの既存trial prompt、固定Layer 1 fixture、Candidate214 full prompt bundleだけをmodel-visibleにする。

次はmodel-visibleにしない。

- quality oracleと期待terminal
- Candidate200、Candidate202、Candidate210からCandidate213までのresult、trace、失敗件数
- Candidate214の品質・機序gate
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

### packet source containerとfragmentの閉鎖

- reviewerによるpacket投影元repository sourceの再read: `0`
- reviewerによるpacket source container内のfield、selector、hash、存在確認または部分抽出read: `0`
- ADR03からADR06のpacket-counterexample 20 runでreviewer repository read: `0 / 20`
- packet projection元inventoryまたはconsumer contractの再read: `0`
- reviewer closed-source read: `0`
- reviewer mixed read: `0`
- reviewer manifest外read: `0`
- rootによるreviewer-owned target preread: `0 / 30`
- 実際のpacket item以外から作られたconstruction receipt: `0`
- repository-backed packet itemでsource container identityが欠けたままのreviewer起動: `0`
- 未投影manifest targetをpacket readinessまたはreceipt作成のためrootがreadした件数: `0`

packet値とrepository fieldの意味上の対応を要求しない。保存eventから、reviewerが読んだtargetのcontainer / region identityと、packet itemを供給したrepository resultのcontainer / region identityを直接照合する。

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

機序監査はrepository readを一律失敗にせず、read targetがpacket構築に使用済みのsource container内か、未投影でterminal dispositionを分けるために必要な別containerかを判定する。

## 停止条件

品質または機序のいずれか一件でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。

停止後は次を行わない。

- 同じCandidate214のrepair rerun
- ADR9累積N=20
- Standard14
- 採用判断
- release作成
- projection

両gateが全件通過した場合だけ、次の別operationとしてStandard14 N=5評価設計へ進める。ADR9通過だけで採用、releaseまたはprojectionを判断しない。

## 実行後の状態

固定45件は45 / 45 valid、Score `4 / 1 = 41 / 4`だった。packet投影元source再readとroot先読みは各0件になったが、container全体の閉鎖がpacketへ未投影のinventory regionまで遮断し、4件が期待`blocked`に対して`unavailable`となった。品質・機序とも不通過のため、Standard14は開始していない。詳細は[Candidate214結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)を正本とする。

## 参照

- [Candidate214作成前設計](candidate214-packet-source-container-closure-design.md)
- [Candidate214方向監査](candidate214-packet-source-container-closure-direction-audit.md)
- [Candidate214実装監査](candidate214-packet-source-container-closure-implementation-audit.md)
- [Candidate214 manifest](../prompts/candidates/the-caption-3ce91a4-packet-source-container-closure-r1/manifest.json)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate214 profile](../evaluations/profiles/candidate214-packet-source-container-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
