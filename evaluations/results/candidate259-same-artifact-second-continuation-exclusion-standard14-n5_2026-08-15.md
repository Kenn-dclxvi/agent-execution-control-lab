# Candidate259 同一artifact二度目継続read除外 Standard14 N=5

## 結論

Candidate259はStandard14 14ケース×N=5の70件をすべて有効かつ採点可能なrunとして完了し、70 / 70件がScore `4`だった。既存F04 5件を再利用し、不足65件だけを新規発行した。

互換な保存済みCandidate147 Standard14 N=5と比べると、品質中央値は同じ100、all-agent token中央値は`+4.32%`、elapsed中央値は`-6.70%`だった。今回のN=5では、tokenは増え、elapsedは短く、一方が他方を全指標で支配する結果ではない。

ただし、Candidate259の「同じ変更方針に対する同一artifactの追加readは一度だけ」という回数ベース制御は、正本設計原則と衝突することを[後続監査](../../docs/candidate259-design-principle-conflict-followup-audit.md)へ固定済みである。このStandard14品質通過は衝突を解消せず、回数ベース機序の成立、採用、releaseまたはprojectionを意味しない。Candidate259を次Candidateの親本文にも使わない。

状態は`standard14_n5_completed / quality_passed / design_principle_conflict_retained / adoption_not_decided / release_not_created / projection_not_performed`とする。

## 固定条件

- prompt: `the-caption-3ce91a4-same-artifact-second-continuation-exclusion-r1`、bundle SHA-256 `93d1874f285dc1381122248fd4786a13c05ce04ef976d39050cb8892f9616eac`。
- evaluation set: `the-caption-standard14-r1` r1、14ケース、各N=5。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- configured M: 24、all-agent token accounting v1。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- comparison baseline: Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`。新しいbaseline runは発行していない。
- Candidate259 F04: 既存result `7453ee7e3e0147d5871918a633d1a134`の5 atomic runを再利用し、再採点や再発行をしていない。

prompt identity以外の互換条件を発行前receiptで一致させ、F04を除く不足65件だけを発行した。詳細は[実行準備監査](../../docs/candidate259-same-artifact-second-continuation-exclusion-standard14-n5-execution-preparation-audit.md)を参照する。

## 集計結果

| 指標 | Candidate147 | Candidate259 | 差 |
| --- | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 0 |
| Score `4` | 70 / 70 | 70 / 70 | 0 |
| quality中央値 | 100 | 100 | 0 |
| all-agent token中央値 | 1,447,626 | 1,510,151 | +62,525（+4.32%） |
| elapsed中央値 | 852.543秒 | 795.387秒 | -57.156秒（-6.70%） |

新規65件のparallel runner全体の外側経過時間は166.134秒だった。これは不足分を並列実行した運用時間であり、互換比較に使うiteration別elapsed中央値795.387秒とは別の値である。

## 診断

command protocol violationは0件だった。Rating v14で診断専用のowner-producer evidenceは、既存F04を含む55件がinadmissibleだった。月次format reviewの数値位置診断は5 / 5件がexactだった。これらはrating contract上の診断値であり、70件すべてのScore `4`を変更しない。

登録resultは[`1d27ee8fc6b74946aa76132aee5478aa.json`](1d27ee8fc6b74946aa76132aee5478aa.json)、採点内訳は[`candidate259-same-artifact-second-continuation-exclusion-standard14-n5-quality-audit-r1.json`](candidate259-same-artifact-second-continuation-exclusion-standard14-n5-quality-audit-r1.json)を正本とする。
