# Candidate227 C147直接人間語翻訳 Standard14 N=5

## 結論

Candidate227はStandard14の70件をすべて有効かつ採点可能なrunとして完了し、70 / 70件がScore `4`だった。品質条件は通過した。

一方、A02では開始状態の結果を次の判断へ使う前に影響しないreadを発行対象へ含めたrunが2 / 5件に留まり、3 / 5件で開始状態の確認後にreadを別発行した。F02の2件とF03の1件では、独立producer executionの明示ではなくcriterion owner語から独立担当を起動した。事前条件に従い機序不通過として停止し、追加N、採用、release、projectionへ進めない。

状態は`standard14_n5_completed / quality_passed / result_effect_scope_failed_3_of_5 / criterion_owner_producer_gate_failed_3_of_70 / mechanism_failed / stopped / adoption_not_decided / release_not_created / projection_not_performed`とする。

## 固定条件

- prompt: `the-caption-3ce91a4-c147-direct-human-translation-r1`、bundle SHA-256 `bc43decca672dff6ed57d5a91eef09cdba86c50a5dc53f4bb6783ea06c11f54a`。
- Evaluation set: `the-caption-standard14-r1` r1、14ケース、各N=5。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- configured M: 24、all-agent token accounting v1。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- comparison baseline: Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`。新しいCandidate147 runは発行していない。

比較前条件と70件の発行許可は[実行準備監査](../../docs/candidate227-c147-direct-human-translation-standard14-n5-execution-preparation-audit.md)を正本とする。

## 比較

| 指標 | Candidate147 | Candidate225（10節） | Candidate227（C147直接翻訳） |
| --- | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 70 / 70 |
| Score `4` | 70 / 70 | 70 / 70 | 70 / 70 |
| quality中央値 | 100 | 100 | 100 |
| all-agent token中央値 | 1,447,626 | 3,077,793 | 3,083,462 |
| elapsed中央値 | 852.543秒 | 1,021.648秒 | 1,188.945秒 |

Candidate147比でCandidate227はtoken `+113.00%`、elapsed `+39.46%`だった。Candidate225比ではtoken `+0.18%`、elapsed `+16.38%`であり、C147への直接対応だけでは10節版からcostを回復しなかった。

## 機序

- 利用者が決める値を質問するA01は5 / 5件でrepository command、変更、testを開始せず通過した。
- A02は開始状態とreadを同じ発行対象へ含めた2件が通過し、開始状態の結果後にreadを別発行した3件が不通過だった。
- criterion ownerだけを根拠にした独立担当起動をF02で2件、F03で1件観測した。
- required command protocol violationは0 / 60件だった。
- 検証完了後tool closureは、この監査では直接判定できる固定oracleを構築していないため`not_observed`とした。
- permission denialとenvironment recoveryは対象経路が発生せず`not_exercised`とした。

Standard14から観測できない条件を通過へ補完せず、全81 primitiveの成立やC147との完全同値は主張しない。

登録resultは[`2f1ff97cd8e64690b4eaec3e512f4589.json`](2f1ff97cd8e64690b4eaec3e512f4589.json)、採点内訳は[`candidate227-c147-direct-human-translation-standard14-n5-quality-audit-r1.json`](candidate227-c147-direct-human-translation-standard14-n5-quality-audit-r1.json)、機序内訳は[`candidate227-c147-direct-human-translation-standard14-n5-mechanism-audit-r1.json`](candidate227-c147-direct-human-translation-standard14-n5-mechanism-audit-r1.json)を正本とする。
