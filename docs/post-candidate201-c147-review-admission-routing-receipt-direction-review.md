# Candidate201後 review admission routing receipt方向レビュー

## 結論

設計方向はCandidate実装へ進める。一般反例13状態にblocking counterexampleは0件である。許可はC147直接childの作成と静的検証までとし、評価slot発行には別の評価設計、profile、comparison preflightを必要とする。

## 確認した状態

| 状態 | 結果 |
| --- | --- |
| fixed input内の許可値 | root projectionへ一意にrouting |
| fixed input外のallowed exact target | reviewer observationへ一意にrouting |
| 両条件成立 | root projection優先で重複なし |
| route不能 | review前`unavailable` |
| descriptor target missing | reviewer non-value observation |
| forbidden valueあり | packet非配送 |
| forbidden valueが空 / null | keyと存在状態も非配送 |
| projected sourceのreviewer部分read | result inadmissible |
| reviewer targetのroot存在確認 | result inadmissible |
| projection receipt不足 | result inadmissible |
| counterexample後の集合外missing | `counterexample_found`維持 |
| 全manifest success、反例なし | `no_counterexample_found` |
| start mismatch時の共同発行 | identity observation以外を抑止 |

## C175との境界

C175から使うのは、required reviewer 30 / 30、missing targetをreviewerで観測する経路、allow-list semantic projection、counterexample優先およびowner語列非起動の成立証拠である。Candidate175のprompt identity、Candidate173 parentage、当時の監査範囲およびStandard14結果を次Candidateへ継承しない。

今回追加するrouting ruleは、C175でrootが実行したprojectionを、TaskSpec-declared model-visible fixed inputとallowed readの関係へ明示的にbindする。projection receiptとstrict start boundaryはC175で未評価だったため、新CandidateのADR9機構gateで別に確認する。

## 退けた方向

- manifestへ新しいowner fieldを要求する: C201と同じauthority欠落を再発する。
- source種類だけでownerを推定する: case inputではなく実装都合へ責任を移す。
- reviewerへ`design-admission.json`全体を再読させる: C199の禁止source readを戻す。
- rootがpaired-scope targetの存在だけ確認する: reviewer-owned observationの先読みになる。
- reviewer finalの自由文からprojection completenessを推定する: C201の未観測8件を再発する。
- missing observationをcounterexampleより先に評価する: C201 ADR04 iteration 1を再発する。
- C175を直接親にする: C147直接基盤規律と開始境界の新規検証を失う。

## 実装許可

次Candidateでは、C147のfull bundleを直接複製し、root `AGENTS.md`だけを変更する。変更は`START_BOUNDARY`、`PRODUCER`・`OWNER_ROLE`の明示producer精密化、および一つの`DESIGN_ADMISSION` closureに限定する。case ID、fixture名、expected terminal、private oracle、過去Candidate名をprompt本文へ入れない。

実装後はbundle identity、C147との非変更target一致、変更条項、禁止語および書式を静的検証する。評価設計とpreflightが完成するまでslotを発行しない。

`M3_passed / reviewed_states_13 / unresolved_blocking_counterexamples_0 / candidate_implementation_allowed / evaluation_not_authorized`
