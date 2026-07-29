# Candidate84 delegation marginal-value boundary Rating v14 Medium F02 N=5

## 結論

Candidate84はF02の成果品質を5 / 5で満たしたが、Worker抑止gateを通過しなかった。3 runはroot-onlyで完了した。一方、2 runは`owner=independent contract check`を「TaskSpec指定の独立確認」と再分類し、test差分を再読するWorkerを各1件起動した。

設計の停止条件「F02でWorkerが1件でも起動した場合は停止」に該当する。Candidate84を`targeted_f02_evaluated / stopped`とし、F04、D01、A06、標準14、採用、release、THE-CAPTION本体反映へ進めない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt identity | `the-caption-3ce91a4-delegation-marginal-value-boundary-r1` |
| bundle SHA-256 | `b58ab2d14417be459dc8fd2a66cd1d48c1f8ae538e1e58a38148cb9598825d82` |
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
| result ID | `741581e8622147b3897c5b7e81588825` |
| content SHA-256 | `e4b021595818bd5e3ea22d0ec4a67b391c63043856211060e9427ab3f93d3a1b` |
| compatibility key | `bbbaf125ee7478456eba5bf083706a0034d0608dd8312548cceacc3fd7d28915` |
| valid / rateable | 5 / 5 |
| score分布 | `4 = 5` |
| quality中央値 | 100.000 |
| all-agent token中央値 / 合計 | 291,841 / 1,479,381 |
| elapsed中央値 / 合計 | 100.018秒 / 616.712秒 |

成果、required validation、許可path、終了条件のquality failureは0件だった。command protocol違反も0件だった。owner / producer evidenceは3件で`failed`だが、Rating v14 profileではdiagnostic-onlyであり、quality scoreを変更しない。

## Worker route監査

| iteration | run ID | child | child token | route |
| ---: | --- | ---: | ---: | --- |
| 1 | `7a7c0134654b47e68c1dbe234e51f2d1` | 1 | 34,571 | `/root/independent_contract_check` |
| 2 | `5bc10e4086bd43bdb5cc614e704699e8` | 0 | 0 | root-only |
| 3 | `a1dd3451826442d288a205b4b4f97a4c` | 0 | 0 | root-only |
| 4 | `23a3ebbd61ef4cd8aeba334cc10052b4` | 0 | 0 | root-only |
| 5 | `293bb69fa2c446f79708277c6d67b38a` | 1 | 34,471 | `/root/contract_check` |

child token合計は69,042で、all-agent token合計の4.67%である。2 childはいずれもrootが実装後に既存testの差分、date-bound assertion、skip / xfailを確認し、artifact変更を行わなかった。

Candidate84はcriterion owner、risk owner、`independent`語列、独立確認という作業名だけではstateを成立させないと明記した。それでも2 runは`owner=independent contract check`を「TaskSpec指定の独立確認」と表現し、別execution identityが必要な成果条件へ再分類した。つまり、語列の除外だけでは`separate_identity_required`への意味上の昇格を完全には防げていない。

Candidate83の5 / 5 Worker起動、6 child session、child token 503,695に対し、観測上は2 / 5、2 session、69,042 tokenまで減った。ただしCandidate84 profileの`task_spec.source`記述がCandidate83と異なるためcompatibility keyは一致しない。この差分はmodel-visible trial inputを変えない説明metadataだが、repository contract上、公式KPI比較としては扱わない。

## 判定境界

- 事実: 成果品質は5 / 5 score `4`である。
- 事実: 3 / 5はroot-onlyで完了した。
- 事実: 2 / 5は価値のないtest-contract再確認Workerを起動した。
- 判断: Worker route gateは不通過で、Candidate84は停止する。
- 未実施: F04、D01、A06、標準14、採用、release、runtime projection。

Candidate82とCandidate83は再実行していない。Candidate83の公式resultと`stopped`履歴は変更しない。

## 登録証跡

- execution archive SHA-256: `c3222f6152cb71f357b50cf8cb8187b9973b963d2bf282c237887d2b19c72dc2`
- final archive SHA-256: `0f6589a0e56ee15f8f545eb6fa54754ed6526cc1aed17ceb0dd9ea9ce2f9ed0d`
- route audit: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate84-delegation-marginal-value-boundary-v14-reasoning-medium-delegation-value-f02-global-m5-n5-20260728-r1/route-audit-v1.json`
