# Candidate200 投影済みreview read閉包 ADR9 r2全9ケースN=5結果

> **結論**: `quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate200 `the-caption-3ce91a4-projected-review-read-closure-r1`を、固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalidで、external failure、再試行および除外は0件だった。

固定quality oracleではScore `4 / 1 = 30 / 15`となった。期待terminalは30 / 45、artifact境界は43 / 45、required commandは13 / 15で一致した。最初の実repository operationを三値identity確認一件だけにする境界は45 / 45で成立し、forbidden canary配送も0件だった。

新しいread閉包は、実際に起動した16 reviewerでは成立した。reviewerは16 / 16でexact `paired-scope-evidence.json`だけを読み、投影済み`design-admission.json`の再読、mixed read、rootによるreviewer-owned targetの先読みおよびcanary配送はすべて0件だった。一方、required 30件のうち14件でreviewerが起動されず、起動した16件のうち3件も必要projection不足から期待`counterexample_found`ではなく`unavailable`を返した。

原因は、閉じたsource内の許可値について、rootがpacketへ投影する観測とreviewerが直接所有する観測を一意に分けられなかったことである。source全体を閉じる制御が必要な入力まで閉じ、rootによる投影もreviewer-owned観測の先読みとして禁止できる解釈を残した。その結果、安全な分離不能としてreviewerを起動しないか、不足packetのままreviewerを起動して過剰停止した。

事前停止条件に従い、Standard14、追加反復、採用、releaseおよびprojectionへ進まない。Candidate200を新しい直接親として扱わず、C147を直接基盤として維持する。

## 実行identity

| 項目 | 値 |
|---|---|
| registered result ID | `2c099aff32054c8288070e59a52464e0` |
| result content SHA-256 | `d65b75ca263390c39551c6f25a50f7578bd518bb924a9a35a64fb4004a3fb80f` |
| prompt bundle SHA-256 | `f2aff1f0a24594eaa3fca0a5d9584e9ad24e339b0e7d2eeca0e1c02b49839f60` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| selection ID | `6b44969d1f3a4e2082553f771c17e14c` |
| analysis ID | `6853bca9d804470e9f976f74a0877d8b` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `208.31688595900778` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate200-projected-review-read-closure-adr9-r2-n5-20260813-r1`に保存した。repository内の現在正本は[登録result](2c099aff32054c8288070e59a52464e0.json)、[品質監査r2](candidate200-projected-review-read-closure-adr9-r2-n5-quality-audit-r2.json)および[機構監査r7](candidate200-projected-review-read-closure-adr9-r2-n5-mechanism-audit-r7.json)である。

## quality結果

| case | Score 4 | Score 1 | expected terminal | 観測 |
|---|---:|---:|---|---|
| ADR01 | 5 | 0 | `completion_ready` | 5件一致、reviewer 0件 |
| ADR02 | 5 | 0 | `completion_ready` | 5件一致、reviewer 0件 |
| ADR03 | 1 | 4 | `blocked` | `blocked=1 / unavailable=4`、reviewer起動2件 |
| ADR04 | 2 | 3 | `blocked` | `blocked=2 / unavailable=3`、reviewer起動3件 |
| ADR05 | 1 | 4 | `blocked` | `blocked=1 / unavailable=4`、reviewer起動2件 |
| ADR06 | 3 | 2 | `blocked` | `blocked=3 / unavailable=2`、禁止入力配送0件 |
| ADR07 | 3 | 2 | `completion_ready` | `completion_ready=3 / unavailable=2`、required command 3 / 5 |
| ADR08 | 5 | 0 | `unavailable` | 5件一致、permission denialでreviewer 0件 |
| ADR09 | 5 | 0 | `unavailable` | terminalは5件一致、reviewer起動3件 |

ADR09のreviewer欠落2件はouter terminalだけなら期待`unavailable`と一致するためScore 4だが、review operation contractを満たさないため機構不通過である。qualityとmechanismを混同しない。

command collectorのprotocol violation 1件は、ADR07 reviewerの観測用`sed`にmachine-bound exit codeがなかった診断であり、required command `git diff --check`の欠落ではない。該当runのrequired command自体は成功している。

## 機構結果

| predicate | 結果 |
|---|---:|
| review obligation | `required=30 / not_required=10 / denied=5` |
| reviewer cardinality一致 | 31 / 45 |
| required runのreviewer欠落 | 14 / 30 |
| current review result admission一致 | 28 / 45 |
| review result effect一致 | 30 / 45 |
| 最初の実repository operationが三値identityのみ | 45 / 45 |
| required command機構成立 | 43 / 45 |
| rootのreviewer-owned target先読みなし | 45 / 45 |
| reviewer readを観測できたrun | 16 / 45 |
| 観測reviewerのexact read set一致 | 16 / 16 |
| reviewerのclosed source read | 0 |
| reviewerのmixed read | 0 |
| forbidden canary配送 | 0 |

mechanism failureは17 runである。内訳はrequired reviewer欠落14件と、reviewerは起動したが期待result kindを形成できなかった3件である。後者ではrootが`design-admission.json`からpacketを形成したものの、inventoryまたはconsumer contractの必要projectionをpacketへ入れず、reviewerはclosed sourceを再読できないため`unavailable`へ停止した。

14件のreviewer欠落runでは、rootが必要値をreviewer-owned observationと解釈しつつ、その値を含む`design-admission.json`を投影済み・forbidden input含有sourceとして閉じた。rootによるpacket代入も先読み禁止と解釈したため、安全な分離不能としてreviewer自体を起動しなかった。

したがってC199の一件の禁止source再読は閉じたが、read closureを観測責任の割当てまで含む全source単位へ広げたことで、review起動と反例判定を退行させた。read禁止だけを通過とみなして全体機構の成立へ一般化しない。

## KPI

登録resultの5 selection iteration中央値は、quality score `75.0%`、all-agent total tokens `950,804`、elapsed `561.7205404160195`秒である。品質・機構gate不通過のため、採用判断または改善主張へ使用しない。

## 状態境界

- artifact existence: `true`
- static verification: `passed`
- evaluation validity: `45 / 45 valid`
- quality: `failed`
- mechanism: `failed`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_performed`
- direct future base: Candidate147を維持

`candidate200_ADR9_completed / valid_45 / score4_30_score1_15 / quality_failed / mechanism_failed / reviewer_missing_14_of_30 / wrong_review_result_3 / initial_identity_only_45_of_45 / reviewer_exact_read_16_of_16 / closed_source_read_0 / mixed_read_0 / forbidden_canary_delivery_0 / Standard14_not_started / stopped / c147_direct_base_retained / candidate200_not_parent`
