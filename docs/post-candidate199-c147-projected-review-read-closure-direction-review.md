# Candidate199停止後のC147投影済みreview read閉包方向レビュー

> **結果**: `direction_review_passed_after_revision / initial_blocking_counterexamples_2 / unresolved_blocking_counterexamples_0 / reviewed_states_18 / candidate_implementation_allowed`

## 結論

[`C147投影済みreview read閉包設計`](post-candidate199-c147-projected-review-read-closure-design.md)をcase名に依存しない18状態で確認した。初稿には、rootがreviewer-owned observationを起動前に先読みできる競合と、一つのreviewer invocationへclosed sourceと許可targetを混ぜられる競合があった。

設計を改訂し、`reviewer_observation_read_set`のownerをreviewerへ固定してrootの先読みを禁止し、`reviewer_read_admissible`へ「一invocationが許可target以外を読まない」を追加した。改訂後の未解決blocking counterexampleは0件である。

次に許可するのはCandidate147を直接親とする新Candidateの実装と静的検証である。Candidate199のprompt本文、bundleまたはmanifestを差分元にしない。評価profileとslotは実装後に別アーティファクト単位で作る。

## 初稿のblocking counterexample

### rootによるreviewer observation先読み

初稿はreviewerのread targetを限定したが、rootが同じdescriptor targetを起動前に読んでpacketへmissing resultを入れる経路を禁止していなかった。これではOBSERVATIONのproducerがrootへ移り、reviewer read closureが成立しても独立観測にならない。

修正版は`reviewer_observation_read_set`の各targetをreviewer-owned unobserved predicateへbindし、rootが起動前にvalue、missingまたはunreadableを観測しない。reviewerがexact targetを読み、そのresultを自身のjudgementへ使う。

### 一commandへのclosed source混入

初稿はread target membershipだけを見ていたため、許可manifest pathとclosed `design-admission.json`を一つのshell commandへ混ぜる余地があった。C199の失敗はこの形だった。

修正版は一invocationの全read targetが`reviewer_observation_read_set`に属することを要求し、closed sourceまたは許可外targetが一件でも含まれればread全体をinadmissibleにする。field選択readや存在確認も例外にしない。

## 一般18状態

| # | 一般状態 | 必須経路 | 判定 |
|---:|---|---|---|
| 1 | 開始identity contractなし | C147通常経路 | 反例不成立 |
| 2 | mismatch時に全repository operation禁止 | 三値identity一件だけ先行 | 反例不成立 |
| 3 | review contractなし | packet、reviewer、追加readなし | 反例不成立 |
| 4 | required scope空集合 | review非適用 | 反例不成立 |
| 5 | 明示reviewかつpermission denied | reviewerと変更なしで`unavailable` | 反例不成立 |
| 6 | root観測済み許可value | valueとprovenanceだけpacketへ投影 | 反例不成立 |
| 7 | root観測sourceに禁止fieldあり | source全体をclosedにしてreviewer read禁止 | 反例不成立 |
| 8 | packet投影済みsourceのfield選択read | read inadmissible | 反例不成立 |
| 9 | packet投影済みsourceの存在確認 | read inadmissible | 反例不成立 |
| 10 | required manifest targetが未観測 | exact targetだけreviewer read集合へ | 反例不成立 |
| 11 | reviewer-owned targetをrootが先読み | 発行禁止 | 反例不成立 |
| 12 | 許可targetがmissing | reviewerのnon-value observation | 反例不成立 |
| 13 | 許可targetとclosed sourceを一commandでread | invocation全体inadmissible | 反例不成立 |
| 14 | 許可target以外を同じcommandでread | invocation全体inadmissible | 反例不成立 |
| 15 | concrete counterexampleと無関係missing | `counterexample_found`を維持 | 反例不成立 |
| 16 | required scopeとmanifest全件valueで反例なし | `no_counterexample_found` | 反例不成立 |
| 17 | 未解決predicateとrequired non-value | `unavailable` | 反例不成立 |
| 18 | closed source read後に正しいresult kind | result inadmissible、変更禁止 | 反例不成立 |

## 実装境界

- direct parent: Candidate147
- changed target: root `AGENTS.md`のみ
- 新規条項: `START_BOUNDARY`、`PRECHANGE_REVIEW`
- C147 `EVIDENCE_GATE`の末尾遷移だけ置換
- `PRECHANGE_REVIEW`内部に`PACKET`と`READ_CLOSURE`を別責任として置くが別model stepにはしない
- current result限定
- ADR9 r2全9ケースN=5を最初の評価とし、一件でも不通過ならStandard14を開始しない

静的検証はdirect parent、他18 target同一、C147他12条項逐語保持、projected source closure、reviewer-owned observation、混在invocation禁止、歴史Candidate名とprivate oracle不在を確認する。

## 状態

`post_candidate199_projected_review_read_closure_direction_review_passed / initial_blocking_counterexamples_2 / unresolved_blocking_counterexamples_0 / reviewed_states_18 / c147_direct_parent_required / projected_source_read_closed / reviewer_owned_observation / mixed_read_invocation_forbidden / current_result_only / ADR9_then_Standard14_only / candidate_implementation_allowed / candidate_not_created`
