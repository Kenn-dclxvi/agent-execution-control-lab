# P005 THE-CAPTION Standard14投影設計

> [!IMPORTANT]
> **状態**: `user_authorized_standard14_measurement / projection_precreation_gate_fixed / p005_canonical_bytes_preserved / c147_nonroot_surface_preserved / standard14_n5_completed / quality_gate_passed / p001_token_cost_recovered_partially / p001_elapsed_not_improved / adoption_not_decided`

## 結論

P005をStandard14 N=5で計測するため、P005本体を変更せず、THE-CAPTION用の投影bundleを別identityで作る。投影bundleはCandidate147の19 targetを比較surfaceとし、root `AGENTS.md`だけをP005の固定bytesへ置換する。root以外の18 target、TaskSpec、fixture、Case、oracle、rating、model、reasoning、runtime、permission、token accountingおよび集計方法は変更しない。

P005の正本は`p005-portable-full-agent-codex-validation-terminal-projection-r1`のまま保持する。Standard14 resultは、実際に配送した投影bundle identityへbindし、VCC6のnamespaced bundle resultまたはP005の一般的platform効果として登録しない。

P005はVCC6 N=5の事前cost gateでP001比elapsedが増え、当初の計画ではStandard14不許可となった。今回の利用者による明示依頼を、停止条件を遡及変更せず追加計測を許可する新しいauthorityとして記録する。この計測は、過去のVCC6 cost判定、採用、releaseまたはruntime projectionを変更しない。

## Candidate作成前gate

1. **比較基準と正常経路**: Standard14の直接比較基準はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`、portable系列の直接親と追加比較基準はP001 `p001-the-caption-standard14-projection-r1`である。正常経路は、固定済みStandard14 TaskSpec、root制御、THE-CAPTION固有の局所instructionおよびrepository authorityを読み、許可された実装、検証、終了へ進む経路である。
2. **実測した問題経路**: P001 Standard14 N=5では、個別validation resultがmodelへ戻る経路がcost主因だった。P005はVCC6でraw nested resultをcarrier-localへ閉じ、terminal projectionだけをouterへ返す機序を30 / 30件で成立させた。Standard14では、この変更を実repository taskで測る。
3. **配送上の問題境界**: P005 namespaced bundleはroot一件だけを持つため、THE-CAPTIONへ単独適用するとCandidate147が空化する非root targetが元内容のまま残る。これではprompt以外の有効surface差を混ぜる。
4. **変更範囲**: Candidate147 bundleの19 targetを保持し、root `AGENTS.md`だけを12,830 bytes、SHA-256 `2cb70ccd11fcfe605accf9b212050ed08b6db0eb0a522d502d35c33d58301681`のP005本文へ置換する。P005本文、Candidate147の非root target、file modeおよびsymlink targetは変更しない。
5. **閉じる配送経路**: 投影bundleへ全targetを明示し、未列挙のTHE-CAPTION元promptが残る経路をなくす。これは評価互換性のcarrierであり、P005本文へ新しい条件または処理手順を追加しない。
6. **維持する正常経路**: THE-CAPTION固有の局所instruction、空化済みlegacy prompt、symlinkおよびrepository authorityはCandidate147、P001投影と同じbytesで届く。P005 rootは自己完結した一枚として配送し、composition componentの追加readを要求しない。
7. **追加costと非目標**: P001 root 10,781 bytesからP005 root 12,830 bytesへの2,049 bytes増とvalidation block置換を実験変数とする。成功runのtool順、commandまたはmodel stepをpromptへ転記しない。VCC6、Standard14のCase、採点、runtime、runnerまたは集計をP005向けに変えない。
8. **評価条件**: `the-caption-standard14-r1`の14 Caseを各N=5で実行する。modelは`gpt-5.6-sol`、reasoningは`medium`、Codex CLIは`0.146.0`、Pythonは`3.14.5`、permissionは`workspace-write / never`、設定上の並列上限は24、token accountingはall-agent v1とする。Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`の保存済みLayer 1を再利用し、P001 result `e8bb0207c8014e5bac8d79ec2cf74bf4`も再実行せず比較する。
9. **停止条件**: 投影bundleのroot以外がCandidate147と一件でも不一致、P005 root bytesが不一致、preflightでprompt identity以外に不一致、coverageが14 Case × 5でない、実行がinvalid、採点不能または必要KPI欠落なら停止する。有効な低品質runは再実行せず保持する。評価成立を採用、releaseまたはruntime projectionへ昇格させない。

## identity境界

| 役割 | identity | 扱い |
| --- | --- | --- |
| portable / Codex機能block正本 | `p005-portable-full-agent-codex-validation-terminal-projection-r1` | P005本文とVCC6 resultの正本 |
| Standard14比較基準 | `the-caption-3ce91a4-result-effect-scope-r1` | Candidate147の保存済み互換resultを再利用 |
| portable直接親比較 | `p001-the-caption-standard14-projection-r1` | P001の保存済み互換resultを再利用 |
| Standard14投影bundle | `p005-the-caption-standard14-projection-r1` | THE-CAPTIONへ配送してStandard14 resultをbindするidentity |

## 評価結果

投影bundleのbyte bindingとcomparison preflightは通過し、新規70 slotを発行した。70 / 70件が`valid`かつScore `4`だった。5回の14項目集約中央値はP001比でtoken `-36.30%`、elapsed `+1.23%`、Candidate147比でtoken `+36.14%`、elapsed `+18.48%`となった。

P005はP001のtoken増加を部分的に回収したが、elapsedは改善せず、Candidate147比のcostも残る。状態は`standard14_n5_completed / quality_gate_passed / p001_token_cost_recovered_partially / p001_elapsed_not_improved / c147_cost_regression_persists / adoption_not_decided`とする。N=5を安定傾向へ一般化せず、N=20を自動発行しない。一次値と項目別KPIは[`P005 THE-CAPTION投影 Standard14 N=5評価`](../evaluations/results/p005-the-caption-standard14-projection-n5_2026-08-19.md)を正とする。

## 参照

- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
- [`P001 THE-CAPTION Standard14投影設計`](p001-the-caption-standard14-projection-design.md)
- [`P005 VCC6 N=5効率比較`](p005-vcc6-n5-efficiency-comparison.md)
- [`P005 VCC6 elapsed境界監査`](p005-vcc6-elapsed-boundary-audit.md)
- [`P005 VCC6 bundle`](../evaluations/targets/codex-validation-carrier-conformance/prompts/candidates/p005-portable-full-agent-codex-validation-terminal-projection-r1/)
- [`Candidate147 bundle`](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/)
