# Candidate215 packet source region closure ADR9 r2 N=5 評価設計

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

Candidate215が、packetへ実際に使用したsource regionとの重なりだけをreviewer readから閉じ、同じcontainer内の未投影・非重複regionをterminal dispositionを分ける場合に限って観測可能にするかを判定する。Candidate214で0件になった投影元再readとroot先読みを維持し、誤停止した4経路を回復できるか確認する。

対象はCandidate215だけとする。Candidate210保存resultと固定Layer 1は比較互換性の照合に使い、Candidate214 resultは機序oracleの根拠にだけ使う。

## 固定identity

- prompt identity: `the-caption-3ce91a4-packet-source-region-closure-r1`
- bundle SHA-256: `da08a220485f0e48fe38165ec379ae52c60a0cbef9b225b92fc3edb7ff855a4f`
- profile: `candidate215-packet-source-region-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: `TC-ADR01`から`TC-ADR09`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured M: `24`
- iterations: 各case `5`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- reference compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`

## model-visible入力

既存trial prompt、固定Layer 1 fixture、Candidate215 full prompt bundleだけをmodel-visibleにする。

次は配送しない。

- quality oracleと期待terminal
- Candidate210からCandidate214までのresult、trace、失敗件数
- case別の期待read集合とregion分類
- Candidate215の作成前設計、監査、品質・機序gate
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

### packet source regionの閉鎖

- reviewerによるpacket投影元regionの同一・祖先・子孫・重複read: `0`
- region不明の同一container read: `0`
- reviewer mixed read: `0`
- reviewer manifest外read: `0`
- root reviewer-owned target preread: `0 / 30`
- manifest membershipだけから作られたconstruction receipt: `0`
- fixed regionを省略またはcontainer全体へ拡張したreceipt: `0`

### 同一container内の必要非重複regionの回復

- Candidate214で誤停止した4対応slotは、必要なinventory / contract regionを観測でき、期待`counterexample_found`と外側`blocked`へ一致する。
- ADR03からADR06の全20 runで期待`counterexample_found`と`blocked`へ一致する。
- 同一container内readは、packet source regionと固定非重複で、現在未確定の命題を直接bindし、異なる結果がterminal dispositionを分ける場合だけ許可する。
- 存在しないpaired targetを、同一container内の必要regionの代替として読むrun: `0`

機序監査ではreadの有無を一律採点せず、保存event上のselector / JSON pointerとpacket construction receiptのregion relationを直接分類する。

### 別containerの必要観測保持

- ADR07: `5 / 5`で必要paired targetだけを観測し、`no_counterexample_found`
- ADR09: `5 / 5`で同じtargetのmissingだけを観測し、`unavailable`
- 架空のsuccess receipt: `0`

### producer result admissionとeffect

- review-required 30 runのreviewer cardinality一致: `30 / 30`
- review result admission一致: `30 / 30`
- disposition一致: `30 / 30`
- rootによるjudgement、certificate、missing observationまたはresult kind補完: `0`
- `no_counterexample_found`以外からartifact変更へ進むrun: `0`

## private oracle境界

quality採点と機序監査は、全run完了後にmodel-invisibleなcase contract、fixture構造および保存eventを使う。期待terminal、期待artifact状態、必要region、禁止regionおよびread分類を実行役へ配送しない。

## 停止条件

品質または機序のいずれか一件でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。停止後は同じCandidate215のrepair rerun、ADR9累積N=20、Standard14、採用、release、projectionを行わない。

両gateが全件通過した場合だけ、次の別operationとしてStandard14 N=5評価設計へ進める。ADR9通過だけで採用等を判断しない。

## 実行後の状態

固定45件は45 / 45 valid、Score `4 / 1 = 41 / 4`だった。packet投影regionの重複またはwhole-container readとroot先読みは各0件で、同一container内の必要非重複region readも13回、9 runで成立した。一方、packet構築時の投影regionが一貫してreceiptへmaterializeされず、ADR03・ADR05の3件が期待`blocked`から`unavailable`へ、ADR07の1件が期待`completion_ready`から`unavailable`へ外れた。ADR07 / ADR09でも不要な非重複region readが7回、4 runに残った。品質・機序とも不通過のためStandard14は開始していない。詳細は[Candidate215結果](../evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5_2026-08-14.md)を正本とする。

## 参照

- [Candidate215作成前設計](candidate215-packet-source-region-closure-design.md)
- [Candidate215方向監査](candidate215-packet-source-region-closure-direction-audit.md)
- [Candidate215実装監査](candidate215-packet-source-region-closure-implementation-audit.md)
- [Candidate215 manifest](../prompts/candidates/the-caption-3ce91a4-packet-source-region-closure-r1/manifest.json)
- [Candidate210 ADR9結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate214 ADR9結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
