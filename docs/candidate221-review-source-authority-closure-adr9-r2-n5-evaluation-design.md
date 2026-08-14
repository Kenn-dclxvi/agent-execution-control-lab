# Candidate221 review source authority closure ADR9 r2 N=5評価設計

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

## 固定条件

- prompt: `the-caption-3ce91a4-review-source-authority-closure-r1`
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

prompt identity以外のcase、fixture、TaskSpec、rating、target commit / tree、model、reasoning、Agent/runtime/CLI、permission、executor、Mおよびtoken accountingを変更しない。完全一致preflight receiptが保存されるまでslotを発行しない。

## 品質gate

- valid、Score 4、terminal、artifact境界、reviewer cardinality、review result admission / effect: 各45 / 45
- required command: 15 / 15
- forbidden canary delivery: 0件

## 機序gate

- root whole-container / mixed-owner result: 0件
- root reviewer-owned target preread: 0件
- packet投影元sourceまたは重複regionのreviewer再read: 0件
- ADR03からADR06の必要reviewer direct observationと期待terminal: 20 / 20
- ADR07 / ADR09のpaired targetだけのroute: 各5 / 5
- reviewer mixed read、manifest外read、permission denied時reviewer起動: 各0件

一項でも外れたら有効runを保持して`quality_failed`または`mechanism_failed`で停止し、repair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。
