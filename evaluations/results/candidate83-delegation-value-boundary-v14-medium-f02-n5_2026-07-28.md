# Candidate83 delegation value boundary Rating v14 Medium F02 N=5

## 結論

Candidate83はF02の成果品質を5 / 5で満たしたが、不要Worker抑止gateを通過しなかった。5 runすべてが`/root/independent_contract_check`を起動し、1 runは最初のWorkerが証拠不足を返した後に`/root/independent_contract_check_v2`へ同じ確認を再割当てした。合計6 child sessionである。

設計の停止条件「F02 / F04で価値根拠のない逐次重複workerが1件でもあれば停止」に該当する。Candidate83を`targeted_f02_evaluated / stopped`とし、F04、D01、A06、標準14、採用、release、THE-CAPTION本体反映へ進めない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt identity | `the-caption-3ce91a4-delegation-value-boundary-r1` |
| bundle SHA-256 | `0e3fd8e8b24b82f84fad1d2e9c68f391a7e3fa722b82fcfc5cbff80a2d6bf852` |
| evaluation set | `the-caption-delegation-value-f02-r1` / `r1` |
| case | `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1` |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| repetition | `N=5` |
| excluded attempt | 0 |

## 一次result

| 項目 | 値 |
| --- | --- |
| result ID | `c93d64261dd24d43aaa30caaa5da9081` |
| content SHA-256 | `b7e68d81f7ddec60c7349140dc4133db4c6afd1e2774c19f1d1f370372961f19` |
| compatibility key | `b14880b6baeb00977e0a15894aed69a29141b23926078fe6de3d32b68baffa0f` |
| valid / rateable | 5 / 5 |
| score分布 | `4 = 5` |
| quality中央値 | 100.000 |
| all-agent token中央値 / 合計 | 407,217 / 2,214,609 |
| elapsed中央値 / 合計 | 138.186秒 / 725.006秒 |

成果、required validation、許可path、終了条件のquality failureは0件だった。command evidence format違反はiteration 1と3で各2件、合計4件である。いずれもchildの補助read commandにmachine-bound exitを対応付けられなかった診断であり、明示required commandの成功は別証拠で成立している。

## Worker route監査

| iteration | run ID | child | child token | route |
| ---: | --- | ---: | ---: | --- |
| 1 | `38b653f2468042cea62fa3afa8cad20b` | 1 | 74,488 | `/root/independent_contract_check` |
| 2 | `dc4ffecb446245cdb37fb6ed1a93484c` | 1 | 33,670 | `/root/independent_contract_check` |
| 3 | `732d9bd18fc4479c914756ebf2abd391` | 2 | 51,010 | 初回FAIL後に`independent_contract_check_v2`へ再割当て |
| 4 | `fc8bcdfa9a7a4dee8ee0d570ca1df865` | 1 | 243,051 | `/root/independent_contract_check` |
| 5 | `95d8ac453ad8484aae8b02c70e430df8` | 1 | 101,476 | `/root/independent_contract_check` |

child token合計は503,695で、all-agent token合計の22.74%である。各childはroot実装後のtest差分、date-bound assertion、許可pathを確認し、artifact変更を行わなかった。iteration 3の初回childだけはallowed read不足を理由にFAILし、rootは同じ確認を別childへ再割当てした。

`delegation_value_ready`の「TaskSpecが独立性を要求」を、TaskSpecの`owner=independent contract check`から成立させたと解釈した経路が5 / 5で再現した。したがって「criterion owner語列だけでは成立させない」という後続文だけでは、同じTaskSpec内の独立性表記を価値根拠へ再分類する経路を閉じられていない。

## 判定境界

- 事実: 成果品質は5 / 5 score `4`である。
- 事実: 不要な独立contract check Workerを5 / 5で起動した。
- 事実: 1 runは同じ確認を2人目のWorkerへ再割当てした。
- 判断: Worker route gateは不通過で、Candidate83は停止する。
- 未実施: F04、D01、A06、標準14、採用、release、runtime projection。

Candidate82のv13/B20結果は変更しない。Candidate82をv14で再実行しておらず、本resultにC82との互換KPI比較はない。

## 登録証跡

- execution archive SHA-256: `87b9191528fcf29c4e62d2b8d8d4629aec7013342ea5cd3844c670353f7e295c`
- final archive SHA-256: `cb18d7bd15729670d866c454a2e3d02f4ead0f5343f2e13393e40dd4b7081c46`
- route audit: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate83-delegation-value-boundary-v14-reasoning-medium-delegation-value-f02-global-m5-n5-20260728-r1/route-audit-v1.json`
