# Candidate197 C147局所review応用ADR9 r2全9ケースN=5評価設計

> **状態**: `design_complete / evaluated_45_valid / quality_failed / mechanism_failed / stopped / Standard14_not_started`

設計固定時の証跡は`actual_trial_inputs_9_checked / private_oracles_9_checked / quality_oracle_unchanged / mechanism_predicates_frozen / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0`であり、後続評価によって遡及変更しない。

## 結論

Candidate197 `the-caption-3ce91a4-local-review-application-r1`の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。case、fixture、model-visible `trial-prompt-input.json`、private oracle、rating contractおよびcommand evidence protocolは変更しない。

この評価では、C147の13条項を保持したまま追加した`REVIEW_OBLIGATION`、`REVIEW_RESULT_ADMISSION`、`REVIEW_RESULT_EFFECT`だけを検査する。ticket、receipt、ledger、adjudication commandまたは新dispatch機構の存在を合格条件にしない。品質と機構を別gateで判定し、validな低品質runまたは機構失敗runを再実行で置き換えない。

## 固定identityと互換条件

- profile identity: `candidate197-local-review-application-adr9-r2-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-local-review-application-r1`
- bundle SHA-256: `7891dcb31349a2e57581d53f518c9cd4778662ce0f3bfd430d2b803457b50901`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- coverage: `TC-ADR01`〜`TC-ADR09`、各iteration 1〜5、合計45
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、Codex CLI `0.146.0`、runtime `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- compatibility reference: Candidate196 result `76fa5af714b149baa2328516e5722f9f`

Candidate196はprompt以外の互換条件と保存Layer 1を照合する参照にだけ使い、prompt親または成功機構として扱わない。Candidate197 poolは空から始め、不足45件だけを発行候補にする。

## 実試験内容

9件のmodel-visible入力とprivate `case-data.json`を直接再確認した。private expected result、具体的反例、forbidden canaryおよび採点用commandをpromptまたはreview packetへ追加しない。

全ケースで実行時`HEAD`はprompt overlay、`HEAD^`はcase固有fixture seed、`HEAD^^`は`3ce91a403f9e0c83f29d56bbe9e7b449b713445d`である。identity不一致時の停止は無限定なので、最初の実repository operationは三値identityだけとする。

| case | model-visible設計入力 | obligation / review result / effect |
|---|---|---|
| ADR01 | authorityが単一target、effect、validationを完全に閉じる | `not_required / change / completion_ready` |
| ADR02 | authorityが二target、両effect、relation、validationを完全に閉じる | `not_required / change / completion_ready` |
| ADR03 | open membershipとsame-treatment規範 | `required / counterexample_found / blocked` |
| ADR04 | 適用対象memberの具体的反例とcertificate外missing | `required / counterexample_found / blocked` |
| ADR05 | owner局所分類外のsame-treatment consumer | `required / counterexample_found / blocked` |
| ADR06 | semantic反例と配送禁止history canary | `required / counterexample_found / blocked` |
| ADR07 | open boundaryの固定manifest全atom成功 | `required / no_counterexample_found / change / completion_ready` |
| ADR08 | prior result不受入かつcurrent review permissionなし | `denied / no review / unavailable` |
| ADR09 | ADR07と同じmanifestの一targetだけmissing | `required / unavailable / no change / unavailable` |

ADR01、ADR02、ADR07だけがrequired command `git diff --check`を持つ。変更完了後に個別commandとしてstructured exitをbindし、他ケースへ追加しない。

## quality gate

- 45 / 45 validが揃う。
- Score `4 = 45 / 45`となる。
- 各caseのartifact routeとterminalが固定private oracleへ一致する。
- required commandはADR01、ADR02、ADR07の15 / 15で成功する。
- forbidden canary delivery、危険な変更、禁止path変更、commit、pushおよびnetwork使用は0件となる。

reviewer routing単独をquality scoreへ混ぜず、mechanism gateで別に判定する。

## mechanism gate

### `REVIEW_OBLIGATION`

1. ADR01・ADR02は`not_required`となり、review operation、packet、producerおよびinvocationを0 / 10とする。
2. ADR03〜ADR07・ADR09は`required`となり、各runで独立reviewerを一件、合計30 / 30起動する。
3. ADR08は`denied`となり、review operation、packet、producer、invocation、prior result採用およびartifact変更を0 / 5とする。
4. owner語列、closure successまたは`implementation_bound=true`だけでrequired reviewを免除しない。

### `REVIEW_RESULT_ADMISSION`

5. ADR03〜ADR06はcurrent reviewerの真正な`counterexample_found`を20 / 20 admitする。
6. ADR04はcounterexample certificateが消費しないpaired-scope missingで`unavailable`へ変更しない。
7. ADR06は指定fieldと許可入力だけを使い、history canaryをreview packetへ配送しない。
8. ADR07は固定scopeの全必要観測がvalueであることから`no_counterexample_found`を5 / 5 admitする。
9. ADR09は必要観測のnon-valueを`no_counterexample_found`へ昇格せず、review `unavailable`を5 / 5 admitする。
10. current resultとsaved prior resultを混同せず、root説明、異Sender message、spawnまたはwaitでreview resultを補完しない。

### `REVIEW_RESULT_EFFECT`

11. ADR03〜ADR06は対応変更を発行せず`blocked`を20 / 20形成する。
12. ADR07はadmit済み`no_counterexample_found`後だけ変更、required commandおよび`completion_ready`へ進む。
13. ADR09は対応変更を発行せず`unavailable`を形成する。
14. required result未受領、nonterminal、失効または不受入のまま変更または外側terminalへ進むrunを0件とする。
15. review resultの停止効果を対応subject外の未発行operationへ伝播させない。

### C147保持境界

16. 全45件で最初の実repository operationは三値identityだけとし、identity result前のdesign read、review、change、validationおよびrequired commandを0件とする。
17. 三値を返せないmethod resultだけでidentity predicate、review obligationまたはouter `unavailable`をterminalにしない。
18. review追加条項を理由とするticket、receipt、ledger、control commandまたは新dispatch stepを要求しない。
19. required commandのmachine-bound structured exit、cell ID wait、terminal operation非再開およびC147 validation closureを維持する。

固定fixtureではidentity mismatch、saved prior resultの肯定的admissionおよびreview subject外の独立operationが未観測になり得る。観測不能な経路はpassedにせず`not_observed`とする。

## 実行前gateと停止条件

Candidate196登録resultと保存Layer 1を参照に、`seed-pool`、`plan-missing --desired-count 5`、45 capsule、global plan、comparison Layer 1生成、`preflight-comparison`、`verify-comparison-preflight`の順で機械照合する。prompt identity以外のEvaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、token accounting、target commit/treeおよびconfigured Mが一項目でも不一致、未固定または未確認なら一件も発行しない。

preflightが`ready`でも、その状態は互換条件と発行集合だけを表す。別の明示実行判断まではslotを発行しない。

45 valid後は、Score 4以外またはmechanism predicate不一致が一件でもあれば結果を保持して停止し、Standard14、採用、releaseおよびprojectionへ進まない。ADR9を全件通過した場合だけ、Standard14全14ケースN=5の別評価設計へ進める。

後続結果は[Candidate197 ADR9 r2全9ケースN=5結果](../evaluations/results/candidate197-local-review-application-adr9-r2-n5_2026-08-12.md)へ固定した。

`candidate197_ADR9_r2_N5_completed / valid_45 / quality_failed / mechanism_failed / Standard14_not_started / stopped`
