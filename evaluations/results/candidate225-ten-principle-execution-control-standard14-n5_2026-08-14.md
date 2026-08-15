# Candidate225 10原則実行制御 Standard14 N=5

## 結論

Candidate225はStandard14 14ケース×N=5の70件をすべて有効かつ採点可能なrunとして完了し、70 / 70件がScore `4`だった。品質条件は通過した。

互換な保存済みCandidate147 Standard14 N=5と比べると、品質中央値は同じ100だった一方、all-agent token中央値は`+112.61%`、elapsed中央値は`+19.84%`だった。したがって、今回のN=5では10節への自然文再構成によるC147からのcost改善は観測されていない。

利用者の追加指定に従い、[確認済み5文統合版Candidate163の現在記録](candidate163-free-five-verified-lines-integrated-v14-medium-standard14-n5-cli0146_2026-08-04.md)とも比較した。品質は両方70 / 70 Score `4`で同値、Candidate225はall-agent token中央値が`+4.84%`、elapsed中央値が`-7.06%`だった。Candidate163はtokenが少なく、Candidate225はelapsedが短いため、一方が他方を全指標で支配する結果ではない。

10節それぞれの個別機序はこのStandard14集約から分離しておらず、5文との差も各文の因果効果には割り振らない。採用、releaseおよびTHE-CAPTION本体への反映は判断・実施していない。

状態は`standard14_n5_completed / quality_passed / c147_cost_increased / candidate163_tradeoff / adoption_not_decided / release_not_created / projection_not_performed`とする。

## 固定条件

- prompt: `the-caption-3ce91a4-ten-principle-execution-control-r1`、bundle SHA-256 `50d5c742bbf2c983aaa4bf084dfabd810025a023523376323258c124f479613a`。
- evaluation set: `the-caption-standard14-r1` r1、14ケース、各N=5。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- configured M: 24、all-agent token accounting v1。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- comparison baseline: Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`。新しいbaseline runは発行していない。
- additional current-record comparison: Candidate163 result `c498dd3944534631a80e70a814fc8171`。再集計、再採点および新しいrun発行は行っていない。

prompt identity以外の互換条件を発行前receiptで一致させ、Candidate225の不足70件だけを発行した。準備時に検出したwrite-once衝突と旧templateのprompt identity不一致はpreflight前に解消し、その時点の発行数は0件だった。詳細は[実行準備監査](../../docs/candidate225-ten-principle-execution-control-standard14-n5-execution-preparation-audit.md)を参照する。

## 集計結果

| 指標 | Candidate147 | Candidate225 | 差 |
| --- | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 0 |
| Score `4` | 70 / 70 | 70 / 70 | 0 |
| quality中央値 | 100 | 100 | 0 |
| all-agent token中央値 | 1,447,626 | 3,077,793 | +1,630,167（+112.61%） |
| elapsed中央値 | 852.543秒 | 1,021.648秒 | +169.105秒（+19.84%） |

## 確認済み5文統合版との比較

Candidate163とCandidate225のcompatibility keyは、どちらも`cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`で一致する。Candidate163は現在の登録resultと最終記録をそのまま使い、比較のための再実行や再採点は行っていない。

| 指標 | Candidate163（5文） | Candidate225（10節） | C225 - C163 |
| --- | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 0 |
| Score `4` | 70 / 70 | 70 / 70 | 0 |
| quality中央値 | 100 | 100 | 0 |
| all-agent token中央値 | 2,935,725 | 3,077,793 | +142,068（+4.84%） |
| elapsed中央値 | 1,099.295秒 | 1,021.648秒 | -77.647秒（-7.06%） |

Candidate163の現在記録にあるAPI価格換算はusage内訳から算出された値である。Candidate225の登録resultには同じ価格算出用内訳を公開していないため、API価格換算を共通比較指標へ追加しない。

並列runner全体の外側経過時間は258.238秒だった。これは14ケースを並列実行した運用時間であり、互換比較に使うiteration別elapsed中央値1,021.648秒とは別の値である。

## 診断

command protocol violationは0件だった。Rating v14で診断専用のowner-producer evidenceは55件がinadmissible、月次format reviewの数値位置診断はexact 4件、mismatch 1件だった。これらはrating contract上の診断値であり、70件すべてのScore `4`を変更しない。

登録resultは[`89c3babd670c461f8b075e7c9a329248.json`](89c3babd670c461f8b075e7c9a329248.json)、採点内訳は[`candidate225-ten-principle-execution-control-standard14-n5-quality-audit-r1.json`](candidate225-ten-principle-execution-control-standard14-n5-quality-audit-r1.json)を正本とする。
