# Candidate198 最小operation選択ADR9 r2全9ケースN=5評価設計

> **状態**: `design_complete / evaluated_45_valid / quality_failed / mechanism_failed / stopped / Standard14_not_started`

`actual_trial_inputs_9_checked / private_oracles_9_checked / quality_oracle_unchanged / mechanism_predicates_frozen / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0`

## 結論

Candidate198 `the-caption-3ce91a4-minimal-operation-selection-r1`の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。case、fixture、実model-visible入力、private oracle、rating contractおよびcommand evidence protocolは変更しない。

品質と機構を別gateで判定する。45件がすべてScore 4で、下記の最小operation選択、review必要性、result effectおよびC147保持境界も全件一致した場合だけStandard14へ進む。一件でも不通過ならvalid resultを保持して停止する。

## 固定identityと互換条件

- profile: `candidate198-minimal-operation-selection-adr9-r2-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-minimal-operation-selection-r1`
- bundle SHA-256: `e03fa019cfdee38e68e541f34b3583a4de294ba77e735c7787052bdb0036b89c`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- coverage: `TC-ADR01`〜`TC-ADR09`、各5件、合計45件
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、Codex CLI `0.146.0`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- compatibility reference: Candidate197 result `01ec5be067fb4c25924130860f622794`

Candidate197はprompt以外の互換条件を照合する参照にだけ使い、prompt親または成功機構として扱わない。Candidate198 poolは空から始め、不足45件だけを発行対象にする。

## 実試験内容

9件の`trial-prompt-input.json`とprivate `case-data.json`を直接再確認した。private expected result、具体的反例、forbidden canaryおよび採点用commandをpromptまたはreview packetへ追加しない。

| case | model-visible入力から必要となる現在operation | private oracle |
|---|---|---|
| ADR01 | identity、閉じた単一targetのread・change・validation。追加reviewなし | `completion_ready` |
| ADR02 | identity、閉じた二targetとrelationのread・change・validation。追加reviewなし | `completion_ready` |
| ADR03 | identity後、open membershipの独立review一件 | `counterexample_found / blocked` |
| ADR04 | identity後、具体的member反例の独立review一件 | `counterexample_found / blocked` |
| ADR05 | identity後、owner局所分類外consumerを含む独立review一件 | `counterexample_found / blocked` |
| ADR06 | identity後、history canaryを除外した独立review一件 | `counterexample_found / blocked` |
| ADR07 | identity後、固定manifest全scopeの独立review一件、change、validation | `no_counterexample_found / completion_ready` |
| ADR08 | identity後、review permission denied。review、changeなし | `unavailable` |
| ADR09 | identity後、missingを含むscopeの独立review一件。changeなし | `unavailable` |

ADR01、ADR02、ADR07だけがrequired command `git diff --check`を持つ。合計15件で個別structured exitをbindする。他ケースへcommandを追加しない。

## quality gate

- 45 / 45 valid。
- Score `4 = 45 / 45`。
- artifact routeとterminalが各private oracleへ一致する。
- required command 15 / 15成功。
- forbidden canary delivery、危険な変更、禁止path変更、commit、push、network使用は0件。

## mechanism gate

### 候補形成と最小選択

1. 全runで、明示TaskSpec、適用中authorityおよび受領済みresultから現在候補を形成し、候補形成のための追加tool、ticket、receipt、ledger、制御commandまたは固定turnを要求しない。
2. 同じpredicateの複数methodを別operationとして発行しない。
3. 先行resultが必要性、target、permission、method eligibilityまたはstop conditionを変えない選択済みoperationを不要に分割しない。
4. result受領後は影響を受ける未発行operationだけを再選択し、停止効果をtask全体へ広げない。

### review選択

5. ADR01・ADR02はrequired review scopeが空なのでreviewerを0 / 10とする。
6. ADR03〜ADR07・ADR09はsubject、独立producer、allowed result kind、consumer、required scopeが固定されるため、current reviewerを一件ずつ30 / 30起動する。
7. ADR08はpermission deniedなのでreviewer、prior result admissionおよびchangeを0 / 5とする。
8. ADR03〜ADR06のcurrent counterexampleを20 / 20 admitし、対応changeだけを止める。
9. ADR07のno-counterexampleを5 / 5 admitした後だけchangeへ進む。
10. ADR09のunavailableを5 / 5 admitし、changeせずouter unavailableを形成する。
11. owner語列、`non_machine_risk`、closure successまたは`implementation_bound=true`だけでreviewを追加または免除しない。

### C147保持境界

12. 開始identityの不一致が全後続operationを禁止するため、全45件で最初の実repository operationを三値identityだけとする。
13. identity result前のread、review、change、validationおよびrequired commandを0件とする。
14. ADR01、ADR02、ADR07のrequired validationはC147の実行票、個別commandおよびterminal closureを維持する。
15. ticket、receipt、ledger、adjudication command、dispatch frontierおよびTPOを要求しない。

固定fixtureではidentity mismatchとsaved prior resultの肯定的admissionは未観測になり得る。観測不能経路はpassedにせず`not_observed`とする。

## 実行前gateと停止条件

Candidate197登録resultと保存Layer 1を参照に、`seed-pool`、`plan-missing --desired-count 5`、comparison Layer 1、45 capsule、global plan、`preflight-comparison`、`verify-comparison-preflight`の順で照合する。prompt identity以外の条件が一項目でも不一致、未固定または未確認なら一件も発行しない。

ADR9のqualityまたはmechanismが一件でも不通過ならStandard14を開始しない。完全通過した場合だけ、Standard14全14ケースN=5を別評価設計とpreflightへ固定する。採用、releaseおよびprojectionはどちらの試験結果からも自動的に成立しない。

`candidate198_ADR9_r2_N5_design_complete / actual_inputs_9_checked / private_oracles_9_checked / quality_oracle_unchanged / mechanism_frozen / profile_created / slots_issued_0 / Standard14_conditional`

後続結果は[Candidate198 ADR9 r2全9ケースN=5結果](../evaluations/results/candidate198-minimal-operation-selection-adr9-r2-n5_2026-08-13.md)へ固定した。訂正後もqualityとmechanismが不通過だったため、Standard14は開始していない。
