# Candidate220 review observable output closure ADR9 r2 N=5評価設計

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

Candidate220がsource availabilityとproducer modelへ配送されるobservable tool outputを分離し、Candidate219で残ったwhole-container root result、不要reviewer、必要reviewer observation欠落およびterminal regressionを閉じるかを判定する。

品質と機序を先に判定し、両方が通過した場合だけ後続を検討する。Candidate210、Candidate219または他Candidateを再実行せず、Standard14も同時には開始しない。

## 固定条件

- prompt: `the-caption-3ce91a4-review-observable-output-closure-r1`
- bundle SHA-256: `739719baebd5f7c993fc5f6e1bc9623f145617724ecc65cbca5a82da6ee47654`
- profile: `candidate220-review-observable-output-closure-adr9-r2-medium-m24-n5-cli0146-r1`
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

- root observable resultへreviewer用またはforbidden valueが返るrun: 0件
- 同じcurrent value identityをrootとreviewerが二重消費するrun: 0件
- whole-container outputまたは受領後非admissionを使うrun: 0件
- ADR01 / ADR02のreviewer起動: 0 / 10
- ADR03からADR06の期待terminalと必要reviewer observation: 20 / 20
- terminal support後に別kind用missingを伝播するrun: 0件
- ADR07 / ADR09のpaired targetだけのroute: 各5 / 5
- reviewerによるpacket-carried projection再read、mixed read、manifest外read: 各0件
- permission denied時のreviewer起動、forbidden canary delivery: 各0件

## 診断方法

45 runのroot / reviewer trace、repository command evidence、commandからmodelへ返るobservable result、packet input、terminal kind、artifact effectを照合する。sourceがfixedまたはmodel-visibleであることや、request目的の自己申告はresult admissionの証拠にしない。

case名やfield名は保存traceの監査locatorにだけ使い、Candidate本文の制御根拠へ逆輸入しない。

## 停止条件

品質gateまたは機序gateが一項目でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

両gateが全件通過した場合だけ、保存traceでobservable output closureと必要route保持を再確認して次の評価範囲を別途固定する。

## 参照

- [Candidate220作成前設計](candidate220-review-observable-output-closure-design.md)
- [Candidate220方向監査](candidate220-review-observable-output-closure-direction-audit.md)
- [Candidate220実装監査](candidate220-review-observable-output-closure-implementation-audit.md)
- [Candidate219 ADR9結果](../evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5_2026-08-14.md)
- [Candidate220 profile](../evaluations/profiles/candidate220-review-observable-output-closure-adr9-r2-medium-m24-n5-cli0146-r1.json)
