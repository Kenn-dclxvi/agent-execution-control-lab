# Candidate205 portable issuance frontier F01 / F02 / F03 N=5評価設計

> **状態**: `design_frozen / profile_created / evaluation_not_started / Standard14_not_started`

## 結論

Candidate205の初回試験は、Standard14のF01 r3、F02 r1、F03 r2を各5回、合計15 atomic runsで行う。Candidate147の保存済み同一3ケース各N=5を互換参照にし、prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor、command evidence protocol、token accountingおよびM=24を変更しない。

15 / 15 validかつScore 4で、15 / 15の最初のissuance frontierに開始identityと許可readが入り、安全・closure違反が0件の場合だけ通過する。一件でも不通過または未観測ならvalid resultを保持して停止し、Standard14全体を発行しない。

## 固定identity

- candidate: Candidate205
- prompt: `the-caption-3ce91a4-portable-issuance-frontier-r1`
- bundle SHA-256: `94cd1c2bdf12da74d8700daa95d15f98e70e6578fbca7a0f96b5ee6108827a53`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-standard14-r1`
- coverage: F01 r3 / F02 r1 / F03 r2、各N=5、合計15件
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、`agents_max_threads=4`、`memories=false`、`multi_agent=true`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- profile: `candidate205-portable-issuance-frontier-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1`

## model-visible inputとoracle境界

model-visible inputは固定Layer 1 fixture、Candidate205 full prompt bundleおよび各caseのTaskSpecだけである。Candidate identity、比較値、quality oracle、issuance mechanism、M1〜M3文書、保存resultおよび停止条件はworkspaceへ置かない。

qualityは既存Rating v14で採点する。issuance mechanismはquality raterへ渡さず、保存root trace、command evidence、producer evidenceおよびworkspace sealから別監査する。

## quality gate

- requested / valid: 15 / 15。
- excluded attempt / controller error: 0 / 0。
- Score 4: 15 / 15。
- required outcome、artifact boundary、required commandおよびterminal state: 15 / 15一致。
- validな低品質runを再試行または除外しない。

## issuance mechanism gate

1. 開始identity resultで許可readのtarget、permission、methodまたはstop conditionが変わらない15件で、開始identityと許可readが最初のissuance frontierへ入る。
2. identity result前のartifact変更とrequired validationを各0 / 15とする。
3. consumerなし観測、不要producer、別producer resultの誤admitを各0件とする。
4. frontierの一部だけを発行して返却resultを次frontier選択へ消費した経路を0件とする。
5. required validationのnon-success後の後続発行、nonterminal完了および全success後の理由なき追加validationを各0件とする。

trace上の最初のcommand groupをfrontier発行の観測に使うが、特定response、model step、field名、専用wrapperまたはatomic dispatch保証を成功条件にしない。

## KPI

quality・mechanism通過後にだけCandidate147保存済み同条件resultと比較する。KPIはquality score、all-agent total tokens、elapsed secondsの3つだけとする。prompt bytes、command数および発行groupは診断へ分離する。

## 実行前gate

Candidate147の3ケース各N=5 selection resultと保存Layer 1へbindする。Candidate205 poolは空から始め、`plan-missing --desired-count 5`で不足15件だけを固定する。

`prepare-comparison-layer1`、atomic plan生成、`preflight-comparison`および`verify-comparison-preflight`が、prompt identity以外の互換条件完全一致と`authorized_slots=15 / issued_slots=0`を証明するまで一件も発行しない。

## 停止条件

Score 3以下、excluded attempt、controller error、isolated identity、identity result前の変更・required validation、consumerなし観測、不要producer、result誤admit、validation closure違反または生traceからの判定不能が一件でもあれば停止する。

完全通過時だけ別profileと別preflightでStandard14全14ケースN=5へ進める。採用、release、projectionは別の明示判断とする。

`candidate205_design_frozen / candidate_only_first_gate / slots_issued_0 / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
