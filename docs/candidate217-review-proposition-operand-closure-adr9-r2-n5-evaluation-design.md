# Candidate217 review proposition operand closure ADR9 r2 N=5評価設計

## 状態

- `evaluation_design_fixed`
- `comparison_preflight_ready`
- `evaluation_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- `adoption_not_decided`
- `release_not_created`
- `projection_not_performed`

## 目的

Candidate217が、review命題のdirect operandをpacketまたは未取得observationへ一意にbindし、Candidate216で観測した既取得operand再取得14回、7 runと必須operand欠落1 runを閉じるかを判定する。

品質と機序を先に判定し、両方が通過した場合だけ後続を検討する。Candidate210またはCandidate216を再実行せず、Standard14もこの試験と同時には開始しない。

## 固定条件

- prompt: `the-caption-3ce91a4-review-proposition-operand-closure-r1`
- bundle SHA-256: `627c8e27541e0b6ab96129e19121def1a43a289d903222d8260d52cf66507056`
- profile: `candidate217-review-proposition-operand-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: `TC-ADR01`から`TC-ADR09`
- repetition: 各N=5、合計45 atomic run
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- max attempts: `3`
- permission: `workspace-write / never`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- reference Layer 1: Candidate147 ADR9 r2 N=50保存Layer 1
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`

prompt identity以外のcase、fixture、TaskSpec、rating、target commit / tree、model、reasoning、Agent/runtime/CLI、permission、executor、Mおよびtoken accountingを変更しない。

## 品質gate

- valid 45 / 45
- Score 4 45 / 45
- terminal一致45 / 45
- artifact境界一致45 / 45
- reviewer cardinality一致45 / 45
- required command一致15 / 15
- forbidden canary delivery 0件
- review result admission / effect一致45 / 45

有効な低品質runは除外または自動再実行しない。

## 機序gate

### operand supply closure

- admission済みdirect operandをpacketへ含めずreviewerが再取得するrun: 0件
- 必須operandがpacketまたは許可済みobservationへexactly one bindingを持たないままreviewerを起動するrun: 0件
- packet済みoperandをreview evidence consumerへ戻すread: 0件
- closure確認またはpacket readinessのためのroot preread: 0件

### 必要routeの保持

- ADR03からADR06の期待terminal一致: 20 / 20
- 未取得でterminalを分け得る必要非重複operandのobservationを遮断しない
- missing / unreadable operandを根拠ある`unavailable`へbindできる
- ADR07 / ADR09のpaired targetだけのroute: 各5 / 5

### 既存closureの保持

- packet projection重複またはwhole-container read: 0件
- packet caseの誤paired read: 0件
- reviewer mixed read: 0件
- manifest外read: 0件
- root reviewer-owned target preread: 0件

## 診断方法

45 runのroot / reviewer trace、workspace、result、command evidenceを使用し、caseごとにpacketで供給されたcurrent value、reviewerのrepository read target、terminal kind、artifact effectを照合する。case名やfield名をCandidate本文の制御根拠へ逆輸入しない。

## 停止条件

品質gateまたは機序gateが一項目でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

両gateが全件通過した場合だけ、保存済みtraceで意図したroute変化を再確認して次の評価範囲を別途固定する。

## 参照

- [Candidate217作成前設計](candidate217-review-proposition-operand-closure-design.md)
- [Candidate217実装監査](candidate217-review-proposition-operand-closure-implementation-audit.md)
- [Candidate216 ADR9結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
- [Candidate217 profile](../evaluations/profiles/candidate217-review-proposition-operand-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
