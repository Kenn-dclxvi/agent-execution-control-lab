# Candidate218 review input carrier ownership ADR9 r2 N=5評価設計

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

Candidate218がreview inputのcurrent value取得前にconsumer ownershipを固定し、C217で20 / 20 packet caseに生じたfixed input / packet carrier conflictと、rootによるmixed-owner whole-container admissionを閉じるかを判定する。

品質と機序を先に判定し、両方が通過した場合だけ後続を検討する。Candidate210、Candidate217または他Candidateを再実行せず、Standard14もこの試験と同時には開始しない。

## 固定条件

- prompt: `the-caption-3ce91a4-review-input-carrier-ownership-r1`
- bundle SHA-256: `04c2e670eabf659b24139429246ad1e640e5162297b4fd999a0565efd8762f73`
- profile: `candidate218-review-input-carrier-ownership-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: `TC-ADR01`から`TC-ADR09`
- repetition: 各N=5、合計45 atomic run
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- max attempts: `3`
- permission: `workspace-write / never`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- reference Layer 1: Candidate147 ADR9 r2 N=50保存Layer 1
- expected compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`

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

### consumer ownership

- rootがreviewer-owned current valueを含むresultをreview inputへadmitするrun: 0件
- 同じvalue identityをrootとreviewerが二重消費するrun: 0件
- root-control inputをreviewer packetへ配送するrun: 0件
- packet配送禁止inputをpacketへ含めるrun: 0件
- mixed-owner whole-container fallbackをrootへadmitするrun: 0件

### 必要routeの保持

- ADR03からADR06の期待terminal一致: 20 / 20
- ADR03からADR06でpacket外かつdirect observation可能な必要operandをreviewerが観測できる
- missing / unreadableなreviewer-owned inputを根拠ある`unavailable`へbindできる
- ADR07 / ADR09のpaired targetだけのroute: 各5 / 5

### 既存境界の保持

- reviewerによるpacket-carried projectionの再read: 0件
- reviewer mixed read: 0件
- manifest外read: 0件
- review不要またはpermission denied時のreviewer起動: 0件
- forbidden canary delivery: 0件

## 診断方法

45 runのroot / reviewer trace、repository command evidence、packetで使用したinput、terminal kind、artifact effectを照合する。root commandがmixed-owner container全体を返した場合、その値を説明に使わなかったという自己申告だけで非admissionにしない。resultがroot modelへ返りreview inputを構成できる状態になったことをroot admissionとして扱う。

case名やfield名は保存traceの監査locatorにだけ使い、Candidate本文の制御根拠へ逆輸入しない。

## 停止条件

品質gateまたは機序gateが一項目でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

両gateが全件通過した場合だけ、保存traceで意図したowner分離と必要route保持を再確認して次の評価範囲を別途固定する。

## 参照

- [Candidate218作成前設計](candidate218-review-input-carrier-ownership-design.md)
- [Candidate218方向監査](candidate218-review-input-carrier-ownership-direction-audit.md)
- [Candidate218実装監査](candidate218-review-input-carrier-ownership-implementation-audit.md)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate218 profile](../evaluations/profiles/candidate218-review-input-carrier-ownership-adr9-r2-medium-m24-n5-cli0146-r1.json)
