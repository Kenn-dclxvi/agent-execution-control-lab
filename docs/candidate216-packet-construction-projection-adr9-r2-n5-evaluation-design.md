# Candidate216 packet construction projection ADR9 r2 N=5 評価設計

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

Candidate216が、packet構築時にadmission済み構造objectからliteral itemへ実際に使ったprojection regionを、元readのselector有無と独立にreceiptへmaterializeするかを判定する。Candidate215で成立した必要非重複region routeを全対象runへ安定化し、packet projectionの重複read、ADR07 / ADR09の不要design-container readおよびroot先読みを0件にできるか確認する。

対象はCandidate216だけとする。Candidate210保存resultとCandidate147保存Layer 1は比較互換性の照合に使い、Candidate215 resultは品質・機序oracleの根拠にだけ使う。

## 固定identity

- prompt identity: `the-caption-3ce91a4-packet-construction-projection-r1`
- bundle SHA-256: `77a0f660d7066bee128785814517a7899d18086e0c0617b9bc90feebe3995eb6`
- profile: `candidate216-packet-construction-projection-adr9-r2-medium-m24-n5-cli0146-r1`
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

既存trial prompt、固定Layer 1 fixture、Candidate216 full prompt bundleだけをmodel-visibleにする。

次は配送しない。

- quality oracleと期待terminal
- Candidate210からCandidate215までのresult、trace、失敗件数
- case別の期待read集合、region分類、projection判定
- Candidate216の作成前設計、監査、品質・機序gate
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

### construction projectionの固定

- reviewerによるpacket projection regionの同一・祖先・子孫・重複readまたはwhole-container read: `0`
- root reviewer-owned target preread: `0 / 30`
- manifest membership、value equality、field / scope名または意味から作られたprojection receipt: `0`
- 一意なliteral projectionをcontainer fallbackへ拡張したreceipt: `0`
- 曖昧、複数origin、要約または変換itemのregion推測: `0`
- reviewer mixed read: `0`
- reviewer manifest外read: `0`

### 必要非重複region route

- ADR03からADR06の20 runで期待terminal一致: `20 / 20`
- 必要なinventory / contract region readはpacket projectionと固定非重複で、現在未確定のterminal dispositionを直接分ける場合だけ許可される。
- 同じcontainerという理由だけで必要非重複regionを遮断するrun: `0`
- 必要非重複regionの代わりにpaired targetへ逸れるrun: `0`

### paired-only route

- ADR07: `5 / 5`でpaired targetだけを必要時に直接観測し、`no_counterexample_found`
- ADR09: `5 / 5`で同じpaired targetのmissingだけを観測し、`unavailable`
- ADR07 / ADR09のdesign-container region read: `0`
- 架空のsuccess receipt: `0`

### producer result admissionとeffect

- review-required 30 runのreviewer cardinality一致: `30 / 30`
- review result admission一致: `30 / 30`
- disposition一致: `30 / 30`
- rootによるjudgement、certificate、missing observationまたはresult kind補完: `0`
- `no_counterexample_found`以外からartifact変更へ進むrun: `0`

## private oracle境界

quality採点と機序監査は全run完了後にmodel-invisibleなcase contract、fixture構造および保存eventを使う。期待terminal、期待artifact状態、必要region、禁止region、projection relationおよびread分類を実行役へ配送しない。

## 停止条件

品質または機序のいずれか一件でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。停止後は同じCandidate216のrepair rerun、ADR9累積N=20、Standard14、採用、release、projectionを行わない。

両gateが全件通過した場合だけ、次の別operationとしてStandard14 N=5評価設計へ進める。ADR9通過だけで採用等を判断しない。

## 実行後の状態

固定45件は45 / 45 valid、Score `4 / 1 = 44 / 1`だった。packet projectionの重複またはwhole-container read、packet caseの誤paired read、root先読みは各0件だったが、ADR06の1件が必要なcurrent inventory valueを得られず期待`blocked`から`unavailable`へ外れた。ADR07 / ADR09では不要なdesign-container readが14回、7 runに残り、paired-only routeはそれぞれ1 / 5、2 / 5だった。品質・機序とも不通過のためStandard14は開始していない。詳細は[Candidate216結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)を正本とする。

## 参照

- [Candidate216作成前設計](candidate216-packet-construction-projection-design.md)
- [Candidate216方向監査](candidate216-packet-construction-projection-direction-audit.md)
- [Candidate216実装監査](candidate216-packet-construction-projection-implementation-audit.md)
- [Candidate216 manifest](../prompts/candidates/the-caption-3ce91a4-packet-construction-projection-r1/manifest.json)
- [Candidate210 ADR9結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate215 ADR9結果](../evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5_2026-08-14.md)
