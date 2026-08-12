# Candidate189自己完結review制御 ADR9 r2 N=5

> **結果**: `45 / 45 valid / Score 4 = 44 / Score 1 = 1 / quality_failed / mechanism_failed / stopped`

## 結論

Candidate189はADR9 r2全9ケース各5件を互換条件で実行し、45 / 45 valid、除外0件、runner error 0件だった。44件はScore `4`でterminal、reviewer cardinality、artifact変更境界および情報封鎖が成立した。一方、ADR07 iteration 5の1件は、真正な`no_counterexample_found`を得た後にTaskSpecへ存在しない`result_use_permission=allowed`を追加要求し、result admissionを拒否して`unavailable`で停止した。Scoreは`1`である。

したがってM5の45 / 45 Score `4`かつmechanism全件成立条件を満たさない。失敗runは適格な観測結果として保持し、再実行で置き換えない。M6とStandard14へ進まない。

## 互換性と実行

- reference result ID: `d3e91302f0d14350906075676c5a2791`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate189 pool key: `c69addd37514a00b06ef7f3e08c8331814f737d2dde7aa7167c319b9c2049e26`
- selection ID: `904ebc81ef714c469e8692194ec3c7a1`
- analysis ID: `bf0d5999280545129084bcfb14f9578c`
- registered result ID: `70652de440184e20bf54dea88b058c94`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate189-self-contained-review-control-adr9-r2-n5-20260812-r1`

保存済みCandidate176 resultと固定Layer 1を互換基準として再利用し、Candidate189の不足45件だけを発行した。case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executorおよびM=24は一致した。TPOを別系列として追加していない。

## case別結果

| case | terminal | reviewer | artifact変更 | Score 4 / 1 | 判定 |
|---|---|---:|---:|---:|---|
| ADR01 | `completion_ready` 5 | 0 | 5 | 5 / 0 | finite direct match成立 |
| ADR02 | `completion_ready` 5 | 0 | 5 | 5 / 0 | finite relation成立 |
| ADR03 | `blocked` 5 | 5 | 0 | 5 / 0 | concrete counterexample保持 |
| ADR04 | `blocked` 5 | 5 | 0 | 5 / 0 | concrete counterexample保持 |
| ADR05 | `blocked` 5 | 5 | 0 | 5 / 0 | 無関係missingからcertificateを分離 |
| ADR06 | `blocked` 5 | 5 | 0 | 5 / 0 | canary配送0、counterexample保持 |
| ADR07 | `completion_ready` 4、`unavailable` 1 | 5 | 4 | 4 / 1 | result admission過剰条件が1件 |
| ADR08 | `unavailable` 5 | 0 | 0 | 5 / 0 | permission deniedでreview未形成 |
| ADR09 | `unavailable` 5 | 5 | 0 | 5 / 0 | missing observationを判断不足へbind |

## 失敗run

- case: `TC-ADR07`
- iteration: `5`
- run ID: `4000b36892f5445c98b27d24e7d6d68c`
- observed terminal: `unavailable`
- required terminal: `completion_ready`
- reviewer: `/root/adversarial_design_review`一件
- reviewer result: `no_counterexample_found`
- artifact変更: 0件
- quality score: `1`

reviewerは固定scopeとmanifestを確認し、真正な`no_counterexample_found`を返した。rootはこの新規review resultに対し、`REVIEW_RESULT_ADMISSION`の`result_use_permission=allowed`を要求した。しかしADR07のTaskSpecは新規reviewの`permission=allowed`とresult kind、producer、scope、packetおよびconsumerを固定しており、保存済みresultを再利用するための別permissionは要求していない。

## 原因判定

原因はC147以前の最適化経路の再発ではない。prompt短縮、evidence省略、review起動削減または比較条件変更による失敗ではなく、M3-F05で導入した「保存済みresult利用permission」と「新規review実行permission」の分離を、新規review resultのadmissionへも拡張したscope誤りである。

M2設計は保存済みresultについて`result_use_permission`を要求する意図だったが、Candidate189の`REVIEW_RESULT_ADMISSION`はcurrent reviewとprior reviewの両方へ同じ条件を適用する。正しい責務境界は次である。

- current review result: bind済み`review_execution_permission=allowed`、producer、sender、allowed kind、observation、certificateおよびforbidden inputを照合する。別の`result_use_permission`を追加要求しない。
- saved prior review result: 新規execution permissionとは分離し、TaskSpecまたはauthorityが明示した`result_use_permission=allowed`、current subject等価性および`result_still_valid=true`を追加要求する。

この修正はCandidate189 bundleへ上書きせず、新identityの設計・実装対象とする。M6、Standard14、採用、releaseおよびprojectionは未実施である。

## 一次証拠

- [登録result](70652de440184e20bf54dea88b058c94.json)
- [機序監査](candidate189-self-contained-review-control-adr9-r2-n5-audit-r1.json)
- [評価profile](../profiles/candidate189-self-contained-review-control-adr9-r2-medium-m24-n5-cli0146.json)
- [評価設計](../../docs/candidate189-self-contained-review-control-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate189-self-contained-review-control-adr9-r2-n5-execution-preparation-audit.md)
