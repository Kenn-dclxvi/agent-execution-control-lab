# Candidate196 materialized adjudication control ADR9 r2全9ケースN=5結果

> **結論**: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate196 `the-caption-3ce91a4-materialized-adjudication-control-r1`を、固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalid、external failureによる除外は0件だった。

固定quality oracleではScore `4 / 1 = 36 / 9`となった。9件は期待`blocked`に対して`unavailable`を返した。artifact変更境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0 / 5だったが、terminal不一致が一件でもあるためquality gateは不通過である。

materialized adjudicationの生trace監査も不通過だった。三値identityだけを最初の実repository操作にしたrunは33 / 45、receiptで覆ったroot toolは140 / 150、receiptのselected method familyと直後toolが一致したものは136 / 150、result-kind adjudicationの順序とterminalが一致したrunは26 / 45だった。三値tupleを返せない`git status --porcelain=v2 --branch`の実行は0件まで閉じたが、開始dependency越境12件、receipt非被覆10 tool、method family不一致14 toolおよびresult-kind経路不一致が残った。

事前停止条件に従い、この結果を保持してM6、Standard14、採用、releaseおよびprojectionへ進まない。Candidate196をCandidate147に代わる親として扱わない。

## 実行identity

| 項目 | 値 |
|---|---|
| registered result ID | `76fa5af714b149baa2328516e5722f9f` |
| result content SHA-256 | `3f0e05b9e1c9dc31f93963990ed13c454a4c16fc781c2e7f942a83bab2a70fd3` |
| prompt bundle SHA-256 | `352eee02c72101769d374d398db4aae061f4e97a38dc24fa283af8a87e839e2c` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| selection ID | `e49f310c177b43e7a95f751d289ebd44` |
| analysis ID | `0ad653b8185446f6bf2c7018b46d70df` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `474.91684820799856` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate196-materialized-adjudication-control-adr9-r2-n5-20260812-r1`に保存した。repository内の一次証拠は[登録result](76fa5af714b149baa2328516e5722f9f.json)、[訂正品質監査r3](candidate196-materialized-adjudication-control-adr9-r2-n5-quality-audit-r3.json)および[機構監査r3](candidate196-materialized-adjudication-control-adr9-r2-n5-mechanism-audit-r3.json)である。

## quality結果

| case | Score 4 | Score 1 | expected terminal | 不一致 |
|---|---:|---:|---|---|
| ADR01 | 5 | 0 | `completion_ready` | 0 |
| ADR02 | 5 | 0 | `completion_ready` | 0 |
| ADR03 | 3 | 2 | `blocked` | 2件が`unavailable` |
| ADR04 | 4 | 1 | `blocked` | 1件が`unavailable` |
| ADR05 | 1 | 4 | `blocked` | 4件が`unavailable` |
| ADR06 | 3 | 2 | `blocked` | 2件が`unavailable` |
| ADR07 | 5 | 0 | `completion_ready` | 0 |
| ADR08 | 5 | 0 | `unavailable` | 0 |
| ADR09 | 5 | 0 | `unavailable` | 0 |

初回品質監査r1は、ADR01の1件で末尾に明示された`結果: completion_ready`を先頭行だけのparserが読めずScore 1へ誤分類した。r2は応答全体の別terminal語まで拾う過剰修正になった。r3では先頭行を優先し、未分類時だけ明示`結果`行を末尾から読むことで固定oracleのterminal抽出を訂正した。r1とr2は準備rootに判断履歴として保持し、登録ratingとrepository内監査はr3へbindした。

## materialized adjudication監査

| predicate | 結果 |
|---|---:|
| root tool target | 150 |
| predispatch receipt | 163 |
| receiptで直前被覆されたtarget | 140 / 150 |
| selected method familyと直後tool一致 | 136 / 150 |
| run単位receipt coverage成立 | 40 / 45 |
| run単位exact method family成立 | 37 / 45 |
| receipt wrapper内tool callが一件 | 45 / 45 |
| no-side-effect control command分類成立 | 34 / 45 |
| terminal receipt schema成立 | 41 / 45 |
| 最初の実repository操作が三値identityのみ | 33 / 45 |
| `git status --porcelain=v2 --branch`の実identity使用 | 0 |
| root command machine exit成立 | 45 / 45 |

receiptの存在数だけでは通過させていない。immutable rolloutのtool-call順序から、各receiptと直後toolを対応づけ、receipt wrapperが一nested toolだけを実行したこと、machine-returned schema、control commandのread API不使用、selected method familyと次toolの一致を別々に確認した。

## result-kind adjudication監査

三result-kindの順序、対応receipt、reviewer finalおよびouter terminalが一致したrunは26 / 45だった。期待counterexampleのADR03〜ADR06では、真正counterexampleを`unavailable`へ落とした9件に加え、result-kind receiptをmaterializeせずreviewer finalだけで補ったrun、不要なno-counterexample / unavailable判定まで進んだrunがあった。ADR07・ADR09にもreceipt欠落または重複判定があった。

ADR04でM2が狙ったcertificate外missing分離は5件中4件で`blocked`を維持したが、1件がpaired-scope missingを理由に`unavailable`となったため成立とは判定しない。固定caseで観測されなかった`receipt_input_drift`、`suppressed_by_predecessor`および`conflict_key_serialization`は`not_observed`のままである。

## 状態境界

- artifact existence: `true`
- static verification: `passed`
- evaluation validity: `45 / 45 valid`
- quality: `failed`
- mechanism: `failed`
- M6: `not_started`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_performed`
- direct future base: Candidate147を維持

`candidate196_M5_completed / valid_45 / score4_36_score1_9 / quality_failed / mechanism_failed / initial_identity_only_33 / initial_dependency_crossing_12 / receipt_covered_140_of_150 / receipt_method_family_match_136_of_150 / result_kind_route_match_26_of_45 / ineligible_status_identity_0 / M6_not_started / Standard14_not_started / stopped / c147_direct_base_retained / candidate196_not_parent`
