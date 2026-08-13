# Candidate195 operation ticket型review制御 ADR9 r2全9ケースN=5

## 結論

Candidate195のADR9 r2全9ケースを各5件発行し、45 / 45 valid、除外0件、runner error 0件で完了した。Rating v14の品質判定はScore `4 / 1 = 43 / 2`であり、固定済みの全件Score 4条件を満たさなかった。機構監査でも、開始identityとdesign readの同一model step発行3件、三値tupleを返せない`git status --porcelain=v2 --branch`の開始identity method使用5件、reviewer cardinality不一致2件、期待review result kind不一致3件を確認した。

したがってCandidate195は`quality_failed / mechanism_failed / stopped`とする。失敗runを再実行で置き換えず、M6、Standard14、採用、releaseおよびprojectionへ進まない。次の作業は、9件の機構失敗をCandidate195の27責任へ戻して原因分類し、C147から再開するM1判断である。

## 固定identity

- prompt: `the-caption-3ce91a4-operation-ticketed-review-control-r1`
- bundle SHA-256: `097a7d2c0f35f60aca40c23ecb912714f96a9bf0255db7dadd58dad835bdda64`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- profile: `candidate195-operation-ticketed-review-control-adr9-r2-medium-m24-n5-cli0146`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case revision: `adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- max workers: `24`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- comparison reference result: Candidate194 `04c8b680e4884eafa39929e06a935035`
- registered result ID: `457400a8506d404f8b564074d0b28802`
- registered result content SHA-256: `e4cf5b9a2690b52ecfc1fb67f15167c7521a8404c18c5948b65bcbea045a2fd4`
- Candidate195 pool key: `5643489ca90215addca33c43a4de5bce88a5b6a7d9363784671dba7fd4fe7428`
- valid / excluded: `45 / 0`
- Score `4 / 1`: `43 / 2`

Candidate194の登録済みresultと保存Layer 1はprompt identity以外の互換条件照合にだけ使用した。Candidate194のrunをCandidate195へ流用していない。Candidate195の直接親はCandidate147のままである。

## 品質失敗

Rating v14の`owner_producer_evidence_policy=diagnostic_only`に従い、reviewer cardinality単独ではquality scoreを下げていない。品質はmodel-visible成果条件、artifact route、terminal、明示required commandおよび禁止入力境界で判定した。

| case | iteration | run ID | 観測 | 期待 | 付随結果 |
| --- | ---: | --- | --- | --- | --- |
| ADR04 | 3 | `81d9930eb62349838c72e891484c334a` | `unavailable` | `blocked` | reviewerは起動したが期待した`counterexample_found`を返さず、変更0 |
| ADR07 | 2 | `cfc6af2a13b84290a49865a3c249f94b` | `unavailable` | `completion_ready` | 必要reviewer未起動、変更・required commandなし |

terminal一致は43 / 45、artifact変更境界一致は44 / 45、明示required command一致は14 / 15だった。validな低品質runは補充、再実行または除外していない。

## 機構失敗

全9ケースのmodel-visible TaskSpecは、実行時HEAD系列が不一致なら停止すると明示する。開始identity resultは後続design readの発行可否を変えるため、同一model step、wrapperまたはcompound commandへ越境できない。

- 開始identityとdesign readの同一model step発行: 3 / 45
- うちidentityとreadを一つのcompound commandへ統合: 1件
- `git status --porcelain=v2 --branch`を開始identity methodとして使用: 5 / 45
- reviewer cardinality一致: 43 / 45
- 期待review result kind一致: 27 / 30
- authentic observation result成立: 28 / 30
- current result admission成立: 27 / 30
- mechanism failure run: 9 / 45
- ADR01・ADR02の不要reviewer起動: 0 / 10
- ADR06 forbidden canary配送: 0 / 5

開始発行の8件とreview結果だけが失敗したADR04 iteration 3の1件を合わせ、失敗runは9件である。`git status --porcelain=v2 --branch`は現在HEADしか返さず、要求された`HEAD / HEAD^ / HEAD^^`の三値tupleをbindできない。うちADR03 iteration 4は後続のeligible methodで回復したが、固定predicateはineligible methodを開始identity methodとして実行したrunを0件と定めているため機構不通過のままである。ADR07 iteration 2とADR09 iteration 5はこのmethodを早期terminal化し、必要reviewerを起動しなかった。

reviewer cardinality不一致2件はADR07 iteration 2とADR09 iteration 5の必要reviewer未起動である。品質Score 4を維持したADR09も機構失敗に含め、品質と機構を同一判定にしていない。

## command evidenceの訂正境界

collectorは103件をprotocol violationとして報告した。しかしcall IDへ戻した再監査では、root commandを持つ45 / 45 runでmachine-bound exit statusを確認し、reviewer内の実観測154件もinteger `exit_code`、`exit_status`、`structured_exit`または`exit`へbindできた。3件のwrapper失敗は後続の同一観測operationで回復し、未回復wrapperは0件、真正なmachine-bound exit status欠落は0件だった。

したがって103件はcollector誤検出として品質・機構の停止理由から除外する。開始dependency越境、ineligible identity method、review経路およびterminal失敗は残るため、結論は変わらない。初回機構監査r2の`authentic_observation_result_count`と`current_result_admission_count`はreviewer未起動runを肯定側へ数えたため、機構監査r3がその解釈を置き換える。

## Candidate194との診断比較

同じcompatibility keyのCandidate194はScore `4 / 1 = 40 / 5`、Candidate195は`43 / 2`で、品質失敗は3件減った。Candidate194のmechanism failure runは15件、Candidate195は9件で6件減った。一方、Candidate195でも開始発行8件とreview経路3件の不一致が残り、全件成立には至っていない。

これはoperation ticket、method eligibility、finite closure certificateおよびobservation ledgerの部分効果を示す診断証拠として保持する。ただしCandidate195を成功、採用可能またはC147に代わる親へ格上げする証拠には使わない。

## 未観測境界

固定fixtureでは開始identity mismatchと競合changeが発生しなかったため、`suppressed_by_predecessor` runtime経路と`conflict_keys`による直列化は未観測のままである。品質・機構が不通過なので、これらの追加評価やStandard14へ進まない。

## 一次証拠

- [登録result](457400a8506d404f8b564074d0b28802.json)
- [品質監査r1](candidate195-operation-ticketed-review-control-adr9-r2-n5-quality-audit-r1.json)
- [機構監査r3](candidate195-operation-ticketed-review-control-adr9-r2-n5-mechanism-audit-r3.json)
- [機構監査r2](candidate195-operation-ticketed-review-control-adr9-r2-n5-mechanism-audit-r2.json) — r3が観測・admission件数の解釈を置換
- [評価設計](../../docs/candidate195-operation-ticketed-review-control-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate195-operation-ticketed-review-control-adr9-r2-n5-execution-preparation-audit.md)

`candidate195_M5_completed / valid_45 / score4_43_score1_2 / quality_failed / mechanism_failed / mechanism_failure_runs_9 / initial_dependency_crossing_3 / ineligible_identity_method_5 / reviewer_cardinality_mismatch_2 / stopped / M6_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
