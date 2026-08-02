# Candidate131 / Candidate132 F04 targeted result

## 結論

Candidate132はF04 N=5でscore `4 / 2 = 4 / 1`となり、事前停止条件により停止した。staleまたは未観測preimageを持つ変更単位は0 / 5であり、必要な`hasAuditKey`変更も5 / 5で適用した。しかし1件が直接anchor取得を使わず全残存contentを取得し、正しい一行変更後に未観測の`colSpan` effectを未充足と判定してrequired validationを開始しなかった。

したがって、Point 5のexact preimage制約はstale変更の抑止には成功したが、変更完了後のeffect closureまで安定させなかった。F02、F07、Standard14、採用、release、本体投影へ進めない。Candidate131を最後のquality gate通過地点として維持する。

## 固定条件

- candidate: `the-caption-3ce91a4-observed-preimage-change-construction-r1`
- parent: `the-caption-3ce91a4-criterion-anchor-continuation-r1`
- bundle SHA-256: `5ca73f0ede4f93ac60856f6c7b7067af14e365e0209cc1f543b06df63999dec4`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- direct reference result: `1d8c4a2713d74f15a42f8e96fcb7b5d9`
- reference pool: `1aba2830735aa0f347de511e6f1529f264c888abf3b037733ff1242b4f531dd4`
- candidate pool: `de76f62250ee69c8ad93e4915f90bd9b17db624f5832c431e1a7661ed8776947`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `2487f370e5f349dbb1fa97e4d2384917`
- analysis: `5bc66c27730e43e3ae8a4a8961a1bb9e`
- registered result: `0df428a2026849efbdcf95972f297eb3`
- excluded attempt: 0

## 方法

Candidate131のcriterion anchor coverageを維持し、artifact変更operationがcurrent contentとの一致を要求する削除行、置換前文字列、contextだけを最新の観測済みexact valueへbindする`change_preimage_ready`を追加した。C126の全criterion再監査条件は継承していない。

比較前にCandidate131の保存済みresultを直接参照し、prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合した。preflightが5 slotをauthorizedとして`ready`になった後、不足5 runだけをM=24のglobal queueへ発行した。

最初の準備ではCandidate131 comparison Layer 1をreference Layer 1として再利用しようとしたが、write-onceの`comparison-generation.json`と競合した。評価slotは発行していない。partial準備を`batch-f04-n005-failed-preparation-20260801T2319JST`へ退避し、Candidate131と同じ固定C98 Layer 1から比較cycleを作り直した後にpreflightを通した。

## 結果

| iteration | run | score | content取得 | artifact変更 | required validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `d1f34ffd9b14439fbcf3029223e9705c` | 4 | direct anchor | `hasAuditKey`一行変更 | 3 / 3成功 |
| 2 | `37110bf9c36849f28c6eee5991904bbd` | 4 | direct anchor | `hasAuditKey`一行変更 | 3 / 3成功 |
| 3 | `5528a759f0064ec8a6985ae3c5e1317d` | 2 | 全残存content | `hasAuditKey`一行変更 | 0 / 3、開始せず停止 |
| 4 | `7ae6b7cce6c046f4a6903d55e7db1a68` | 4 | direct anchor | `hasAuditKey`一行変更 | 3 / 3成功 |
| 5 | `82af2935d33348eea915ad0c677b00b6` | 4 | direct anchor | `hasAuditKey`一行変更 | 3 / 3成功 |

全5件でstaleまたは未観測preimageを持つ変更は発行されず、必要な`hasAuditKey`変更は適用された。4件は`npm ci --ignore-scripts --no-audit --no-fund --include=dev`、`npm run lint`、`npm run build`を完了した。

iteration 3は`sed -n '261,$p'`で全残存contentを要求した。保存されたraw outputには`colSpan`が含まれるが、modelへ配送されたcontentは途中で切れた。agentは`colSpan`のpreimageを確認できないと判断し、観測済みの`hasAuditKey`だけを正しく変更した。その後、`colSpan` effectが閉じていないとして3 validationを開始せず、成果を未完了で停止した。

## 解釈

事実として、Candidate132はC125で発生したstale preimageを0 / 5へ抑えた。一方、Candidate131で5 / 5だったdirect anchor routeは4 / 5へ下がり、全残存content fallbackとfalse stopが各1 / 5へ再発した。

原因は、report deliveryを直接制御できないことではない。大きな全残存contentを選んだ結果、model-visibleなcontentが不完全になり、変更前predicateと変更後closureの判断が混線したことである。exact preimageが未確認の変更単位を除くところまでは正しかったが、その未確認を別の独立した必要変更の完了後まで未充足effectとして持ち越した。

このため、Point 5をglobalな変更前gateとして追加すると、Point 2のcoverage選択とPoint 3のeffect closureを再び開く可能性がある。単なる文言修正で次Candidateへ進まず、Point 6の既存closure / recovery制御との重複と境界を先に監査する。

5件中央値はquality `100.000`、token `127,395`、elapsed `87.616`秒だった。ただし1件がrequired validation前に停止しているため、Candidate131より効率が良いとは解釈しない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_failed / stale_preimage_0_of_5 / required_edit_5_of_5 / direct_anchor_4_of_5 / full_content_fallback_1_of_5 / false_stop_1_of_5 / validation_complete_4_of_5 / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 4 / 5 | fail |
| score `3`以下 | 0 / 5 | 1 / 5 | fail / stop |
| direct anchor content | 5 / 5 | 4 / 5 | fail |
| staleまたは未観測preimageを持つ変更 | 0 / 5 | 0 / 5 | pass |
| 必要なartifact変更 | 5 / 5 | 5 / 5 | pass |
| 全残存content fallback | 0 / 5 | 1 / 5 | fail |
| required validation完備 | 5 / 5 | 4 / 5 | fail |
| false stop | 0 / 5 | 1 / 5 | fail |
