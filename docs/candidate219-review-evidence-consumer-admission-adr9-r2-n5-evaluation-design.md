# Candidate219 review evidence consumer admission ADR9 r2 N=5評価設計

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

Candidate219がartifact変更前reviewに関係するrepository evidence invocationを一つのconsumerと閉じたresult projectionへ発行前にbindし、C218で残ったmixed-owner root result、二重消費、不要reviewer、packet projection再readおよびterminal support後のmissing伝播を閉じるかを判定する。

品質と機序を先に判定し、両方が通過した場合だけ後続を検討する。Candidate210、Candidate218または他Candidateを再実行せず、Standard14もこの試験と同時には開始しない。

## 固定条件

- prompt: `the-caption-3ce91a4-review-evidence-consumer-admission-r1`
- bundle SHA-256: `5ec4728576b24b8dd4aceb45903cae6f9fe0f46b58bf382a3cbe4c50cdfabf95`
- profile: `candidate219-review-evidence-consumer-admission-adr9-r2-medium-m24-n5-cli0146-r1`
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

### consumer-bound issuance

- root result envelopeへreviewer-onlyまたはforbidden projectionが返るrun: 0件
- 同じcurrent value identityをrootとreviewerが二重消費するrun: 0件
- packet配送禁止inputをrootが取得、要約、admitまたはpacket配送するrun: 0件
- result envelopeを限定できないためwhole-container fallbackを使うrun: 0件
- consumer外projectionを受領後に非admission扱いするrun: 0件

### 必要routeの保持

- ADR03からADR06の期待terminal一致: 20 / 20
- ADR03からADR06でpacket外かつdirect observation可能な必要値をreviewerが観測できる
- ADR04で具体的counterexample support後に別kind用missingを`unavailable`へ伝播するrun: 0件
- missing / unreadableな必須観測だけを根拠ある`unavailable`へbindできる
- ADR07 / ADR09のpaired targetだけのroute: 各5 / 5

### 既存境界の保持

- reviewerによるpacket-carried projectionの再read: 0件
- reviewer mixed read: 0件
- manifest外read: 0件
- review obligationがemptyまたはpermission denied時のreviewer起動: 0件
- forbidden canary delivery: 0件

## 診断方法

45 runのroot / reviewer trace、repository command evidence、各commandのresult envelope、packetで使用したinput、terminal kind、artifact effectを照合する。root commandがconsumer外projectionを含むresultを返した場合、その値を説明に使わなかったという自己申告だけで非admissionにしない。resultがroot modelへ返った時点でconsumer境界違反と扱う。

case名やfield名は保存traceの監査locatorにだけ使い、Candidate本文の制御根拠へ逆輸入しない。

## 停止条件

品質gateまたは機序gateが一項目でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

両gateが全件通過した場合だけ、保存traceで意図したconsumer-bound issuanceと必要route保持を再確認して次の評価範囲を別途固定する。

## 参照

- [Candidate219作成前設計](candidate219-review-evidence-consumer-admission-design.md)
- [Candidate219方向監査](candidate219-review-evidence-consumer-admission-direction-audit.md)
- [Candidate219実装監査](candidate219-review-evidence-consumer-admission-implementation-audit.md)
- [Candidate218 ADR9結果](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md)
- [Candidate219 profile](../evaluations/profiles/candidate219-review-evidence-consumer-admission-adr9-r2-medium-m24-n5-cli0146-r1.json)
