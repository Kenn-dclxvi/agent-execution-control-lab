# Candidate131 F04 N=29 stability result

## 結論

Candidate131はF04の既存N=5を再利用し、追加24件で合計N=29へ拡張した。追加分はscore `4 / 2 = 23 / 1`、合計は`28 / 1`だった。score `2`が一件出たため事前停止条件に従って停止した。次の評価slot、F02、F07、Standard14へ進めない。

低Score runはartifact変更を発行していない。初回contentで`audit_match_key`と`hasAuditKey`を受領していたが、直接anchor検索ではなく全残存contentを選んだ。配送されたcontentが途中で切れ、`colSpan`開始状態を確認できないとして変更とrequired validationをすべて止めた。

したがって、Candidate131はF04 N=5の初段mechanismを通過したが、N=29の低頻度安定性を通過しなかった。Point 5のstale change constructionは0 / 29だった。残差はPoint 2のanchor選択をall-or-nothingの`criterion_anchor_ready`判定へ置いたことにある。

## 固定条件

- candidate: `the-caption-3ce91a4-criterion-anchor-continuation-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `56646b697deda9484163e46aabdba70aa93120834fe535cffcc6dec923d4129a`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `29` / `24`
- reused / new runs: `5 / 24`
- direct reference result: `1d8c4a2713d74f15a42f8e96fcb7b5d9`
- pool: `1aba2830735aa0f347de511e6f1529f264c888abf3b037733ff1242b4f531dd4`
- execution preflight compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `8af0935112d74e94b34b04f831cd8a03`
- analysis: `7d56cc325b714f7ca1184f86f4f49cb2`
- registered result: `7d89d8e5c4274fe4aad96c8c9406395d`
- excluded attempt: 0

## 方法

Candidate131のprompt、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingをN=5 resultと一致させた。atomic方式ではNをrun互換条件へ含めず、固定N=5 profileで不足24 runのdispatchをpreflightした。完了後、既存5件と新規24件を同じpoolからN=29 selectionへ固定し、派生N=29 profileでresultを登録した。

準備中に二つのslot-free失敗があった。最初は既存candidate poolを再作成しようとしてwrite-once競合となった。次はN=29 profileをexecution preflightへ使い、固定Layer 1のN=5 coverageと不一致になった。いずれもslot発行前に停止した。partial preparationはcampaign内に保持し、既存pool直接参照と固定N=5 profileへ戻した後にpreflightを通した。

追加24件はM=24のglobal queueで一括実行した。24 / 24件がvalid・rateableで、excluded attemptとrunner errorは0件だった。

## 結果

| 範囲 | score `4` | score `2` | direct anchor content | 全残存content fallback | 必要変更と3 validation完備 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 既存N=5 | 5 | 0 | 5 | 0 | 5 |
| 追加24件 | 23 | 1 | 23 | 1 | 23 |
| 合計N=29 | 28 | 1 | 28 | 1 | 28 |

成功28件は直接anchor検索から`hasAuditKey`周辺を取得し、観測済みの`const hasAuditKey = true;`だけをdata-dependentな式へ変更した。staleまたは未観測preimageを持つ変更、`colSpan`変更、初回artifact変更失敗は各0 / 29だった。

低Score runは`e3907d1b47534d05aa19bb6721bf4374`である。execution上のiterationは10、N=29 selection上のiterationは27である。

1. 初回waveで`App.tsx` 1〜260行、`package.json`、`package-lock.json`を取得した。
2. `App.tsx`内の`audit_match_key`と`const hasAuditKey = true;`はmodel-visibleだった。
3. それでも直接anchor検索を選ばず、`sed -n '261,$p' App.tsx`を発行した。
4. 全残存contentの配送が途中で切れ、`colSpan`開始状態を確認できなかった。
5. artifact変更0件、required Node validation 0 / 3のまま停止し、score `2`となった。

## 解釈

Candidate132で懸念したstale preimageは、Candidate131 N=29では一件も発生しなかった。したがって保存済みF04 traceでは、Change constructionへ独立global gateを追加する必要性は支持されない。

一方、Candidate131の`criterion_anchor_ready`は「各未観測criterionにanchorが一つ以上あるか」を一つのtrue / falseへまとめる。低Score runはTaskSpecと初回contentに完全一致可能な語があったにもかかわらず、このglobal readinessをfalse側として全残存content fallbackへ進んだ。28件の成功は複数のanchor集合やcontext幅を使っており、特定commandの不足ではない。問題はexact anchorが存在する状態でも、その利用をglobal readiness判定の後へ置いたことである。

次案を作る場合はCandidate131を直接親にしない。Candidate128へ戻り、Candidate131を診断証拠として、未観測criterion全体のready判定ではなく「TaskSpecまたは受領済みcontentに現れるexact anchor集合が空でなければ、その集合の直接content取得を全残存contentより先にする」という一軸を検討する。ただしanchor取得後も全required effectを判定できない場合の停止境界を作成前gateで固定する。

N=29中央値はquality `100.000`、token `155,862`、elapsed `137.319`秒だった。低Score runが変更・validation前に停止しているため、効率改善とは解釈しない。

## 状態

`targeted_f04_n29_evaluated / quality_gate_failed / direct_anchor_28_of_29 / full_content_fallback_1_of_29 / stale_preimage_0_of_29 / required_validation_complete_28_of_29 / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 29 / 29 | 29 / 29 | pass |
| score `4` | 29 / 29 | 28 / 29 | fail |
| score `3`以下 | 0 / 29 | 1 / 29 | fail / stop |
| direct anchor content | 29 / 29 | 28 / 29 | fail |
| 全残存content fallback | 0 / 29 | 1 / 29 | fail |
| staleまたは未観測preimageを持つ変更 | 0 / 29 | 0 / 29 | pass |
| 必要なartifact変更 | 29 / 29 | 28 / 29 | fail |
| required validation完備 | 29 / 29 | 28 / 29 | fail |
