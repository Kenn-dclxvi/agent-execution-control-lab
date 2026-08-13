# Candidate204 portable execution core F01 / F02 / F03 N=5評価設計

> **状態**: `design_frozen / profile_created / evaluation_not_started / Standard14_not_started`

## 結論

Candidate204 `the-caption-3ce91a4-portable-execution-core-r1`の初回試験は、Standard14のF01 r3、F02 r1、F03 r2を各5回、合計15 atomic runsで行う。Candidate147の同じ3ケース各N=5を互換参照にし、prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor、command evidence protocol、token accountingおよびM=24を変更しない。

15件すべてがvalidかつScore 4で、許可readへの偽dependency、identity result前の変更・required validation、consumerなし観測、不要producer、result誤admitおよび検証closure違反が0件の場合だけ初回gateを通す。一件でも不通過または未観測ならvalid resultを保持して停止し、Standard14全体を発行しない。

## 固定identity

- candidate: Candidate204
- prompt: `the-caption-3ce91a4-portable-execution-core-r1`
- bundle SHA-256: `d9c90d877e97479d95e5be51306111b221dd7e53c5c921e14599fb39df1faf5e`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-standard14-r1`
- coverage: F01 r3 / F02 r1 / F03 r2、各N=5、合計15件
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、`agents_max_threads=4`、`memories=false`、`multi_agent=true`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- profile: `candidate204-portable-execution-core-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1`

## model-visible inputとoracle境界

model-visible inputは固定Layer 1 fixture、Candidate204 full prompt bundleおよび各caseのTaskSpecだけである。Candidate identity、C147比較値、quality oracle、portable mechanism predicate、M1〜M3文書、保存resultおよび停止条件はworkspaceへ配置しない。

qualityは既存Rating v14で採点する。portable mechanismはquality raterへ渡さず、root trace、command evidence、producer evidenceおよびworkspace sealから別監査する。

## quality gate

- requested 15、valid 15、excluded 0。
- Score `4 = 15 / 15`。
- required outcome、artifact boundary、required commandおよびterminal stateが15 / 15一致する。
- validな低品質runを再試行または除外しない。

## portable mechanism gate

1. F01〜F03は開始identity drift時にもreadを禁止せず、identity resultでread targetまたはpermissionが変わらない。identity判定を待つだけの許可read先送りを0 / 15とする。
2. identity result受領前のartifact変更とrequired validationを各0 / 15とする。
3. consumerなし観測、不要な別producer execution、別producer resultの誤admitを各0件とする。
4. required validationを個別resultへbindし、non-success後の後続発行、nonterminal resultによる完了および全success後の理由なき追加validationを各0件とする。
5. method executionの`failed / unavailable`をpredicate terminalへ昇格した経路を0件とする。

現行trace上のcommand発行groupは観測方法にだけ使う。`同一model step`、特定field名、専用wrapper、待機IDの使用自体を成功条件にしない。

## KPI

quality・mechanism通過後にだけCandidate147保存済み同条件resultと比較する。KPIはquality score、all-agent total tokens、elapsed secondsの3つだけである。prompt bytes、command数、producer数および発行groupは機構診断として分離する。

## 実行前gate

Candidate147の3ケース各N=5 selection resultと、それを生成した保存Layer 1へbindする。新しいCandidate204 poolは空から始め、`plan-missing --desired-count 5`で不足15件だけを固定する。

`prepare-comparison-layer1`、atomic plan生成、`preflight-comparison`および`verify-comparison-preflight`が、prompt identity以外の互換条件完全一致と`authorized_slots=15 / issued_slots=0`を証明するまで一件も発行しない。

## 停止条件

Score 3以下、excluded attempt、controller error、許可readの偽dependency、identity result前の変更・required validation、consumerなし観測、不要producer、result誤admit、validation closure違反または生traceからの判定不能が一件でもあれば停止する。

完全通過時だけ、別profileと別preflightでStandard14全14ケースN=5へ進める。採用、release、projectionは別の明示判断とする。

`candidate204_design_frozen / candidate_only_first_gate / slots_issued_0 / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
