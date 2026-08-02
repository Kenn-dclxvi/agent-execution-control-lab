# Candidate128 / Candidate131 F04 targeted result

## 結論

Candidate131はF04 N=5で5 / 5件がscore `4`となり、作成前のquality・mechanism gateを通過した。5件すべてがTaskSpecで直接観測済みのcriterion anchorから同一targetの一致箇所と周辺contentを直接取得した。全未取得content fallback、locator-only独立result、false stopは各0 / 5だった。

この結果はF04 N=5でEvidence coverageの狙った経路を観測したことだけを示す。F02、F07、Standard14、採用、release、本体投影は未実施である。

## 固定条件

- candidate: `the-caption-3ce91a4-criterion-anchor-continuation-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `56646b697deda9484163e46aabdba70aa93120834fe535cffcc6dec923d4129a`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- preflight reference result: `cea34faab78149119808da7c59628955`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- pool: `1aba2830735aa0f347de511e6f1529f264c888abf3b037733ff1242b4f531dd4`
- selection: `a2bac98ff6e044749b228c999a9047c3`
- analysis: `e8033bcc384440cfbdaa2ebb8c92c725`
- registered result: `1d8c4a2713d74f15a42f8e96fcb7b5d9`
- excluded attempt: 0

## 方法

Candidate128の`continuation_scope_complete`を、直接観測済みanchorからrequest scopeを作るpredicateへ置換した。F04固有のpath、名前、commandはpromptへ入れていない。Candidate130は保存traceの診断だけに使い、prompt parentにはしていない。

比較前にC125の保存済みresultを一意にbindし、prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合した。preflightが5 slotをauthorizedとして`ready`になった後、不足5 runだけをM=24のglobal queueへ発行した。

## 結果

| iteration | run | score | direct anchor content | artifact変更 | required validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `5389c071305a4a62afc06b7e004a28aa` | 4 | `Audit Key / audit_match_key / colSpan`周辺 | header・row・`colSpan`の3式を同じdata predicateへ変更 | 3 / 3成功 |
| 2 | `7703fafc0aa84b22a12d14700b7e5c77` | 4 | 上記anchor周辺＋`hasAuditKey`周辺 | `hasAuditKey`一行変更 | 3 / 3成功 |
| 3 | `418bb1c493e34240ad4032571f97ba6a` | 4 | 上記anchor周辺＋`hasAuditKey`周辺 | `hasAuditKey`一行変更 | 3 / 3成功 |
| 4 | `b1883d5d460047ddabb78a9634cee3cf` | 4 | 上記anchor周辺＋`hasAuditKey`周辺 | `hasAuditKey`一行変更 | 3 / 3成功 |
| 5 | `f96cf2ef6e3f41a69367069ac65dc426` | 4 | 上記anchor周辺＋`hasAuditKey`周辺 | `hasAuditKey`一行変更 | 3 / 3成功 |

全5件で`npm ci --ignore-scripts --no-audit --no-fund --include=dev`、`npm run lint`、`npm run build`が成功した。変更pathは許可された`src/web/market_units_editor/src/App.tsx`だけだった。

## 解釈

C130では5 / 5件が`sed 261,$p`へ流れ、focused取得は0 / 5だった。C131では5 / 5件が最初のsource evidenceからcriterion anchorの周辺contentを直接返した。したがって、F04 N=5の範囲では、`symbol identity`の抽象分類ではなく、TaskSpecまたは受領済みcontent中の完全一致可能な語をrequest scopeへbindする変更が狙った経路差と対応した。

report deliveryの完全性は制御していない。大きな全残存contentを避けた結果として切詰めに遭遇しなかっただけであり、executorやadapterの改善とは解釈しない。

iteration 1は、共通の`hasAuditKey`定義を変更せず、header、row、`colSpan`へ同じdata predicateを個別適用した。成果とvalidationは成立しているため、これをeffect-state失敗または不要変更とは断定しない。共通上流条件を変更する経路との違いは、次のdependency / change construction監査へ分離する。

5件中央値はquality `100.000`、token `133,024`、elapsed `87.703`秒だった。candidate固有の初段gateではKPI baseline toleranceを固定していないため、cost通過または改善は判断しない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_passed / criterion_anchor_direct_content_5_of_5 / full_content_fallback_0_of_5 / locator_only_0_of_5 / false_stop_0_of_5 / result_registered / point2_n5_passed / adoption_not_decided`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 5 / 5 | pass |
| score `3`以下 | 0 / 5 | 0 / 5 | pass |
| criterion anchorから周辺contentを直接取得 | 5 / 5 | 5 / 5 | pass |
| 全未取得content fallback | 0 / 5 | 0 / 5 | pass |
| locator-only独立result | 0 / 5 | 0 / 5 | pass |
| artifact変更なしfalse stop | 0 / 5 | 0 / 5 | pass |
| required validation完備 | 5 / 5 | 5 / 5 | pass |
