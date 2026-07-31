# click standard14 第2版

F10 authority availability修正を含むClick標準14項目setである。既存
`click-standard14-r1`の13 case revisionを維持し、
`CLICK-F10-COMMAND-API-INVENTORY`だけを`r1`から`r2`へ置換する。

- set_id / revision: `click-standard14-r2` / `r2`
- Case / N / B / M: `14 / 5 / 1 / 24`
- prompt: `click-00e592c-no-agents-r1` / `click-00e592c-repository-authority-r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime identity:
  `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`
- rating: `click-outcome-abstract-condition-preserving-v10`

収録revisionはF01 r1、F02 r1、F03 r1、F04 r1、F05 r1、F05-OS r1、F06 r1、
F07 r2、F07-P r3、F08 r1、F10 r2、F10-R r1、A01 r1、A02 r1である。

## 目的

F10 targeted qualificationで成立したauthority availability経路を含めた修正版
Std14全体を、No-AGENTSとRepository Authorityで各70件実行する。13 caseの回帰、
F10の意図した分岐、公式3 KPI、sub authorityの露出経路を同じsetで確認し、
試験群全体の互換性を判定する。

## 期待と停止条件

- No-AGENTSはF10 r2だけが`authority_unavailable`で停止し、他13 caseは既存成果を
  維持する。
- Repository AuthorityはF10 r2を含む14 caseすべてで成果条件を満たす。
- 全140 slotがvalidかつrateableになるまで、欠損slotだけを再実行する。
- unexpected drift、required command evidence欠落、F10のsource-only推論、または
  authorityありF10の未完了が1件でもあれば、互換性達成を判定しない。
- rating、登録、比較は両条件70 / 70件が揃った後に行う。

F10 targeted結果はqualification evidenceとして保持し、このStd14 resultへ混ぜない。
採用、release、runtime projectionは別gateである。

## 評価結果

2026-07-27に両条件70 / 70件を完了した。F10以外の13 caseは両条件とも
65 / 65件がscore `4`だった。F10はNo-AGENTSがscore `1` × 5、Repository
Authorityがscore `4` × 5で期待経路へ分離した。全140件がvalid・rateable、
excluded attemptとunexpected driftは0件だった。

互換性判定と公式KPIは
[`Click No-AGENTS / Repository Authority Medium Std14 r2 N=5`](../../results/click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)
を正本とする。

C81とC81 + Repository Authorityの追加比較も各70 / 70件を完了した。F10以外は
両条件65 / 65件がscore `4`、F10はscore `1` × 5 / score `4` × 5へ分離した。
組合せ結果は
[`Click C81 / C81 + Repository Authority Medium Std14 r2 N=5`](../../results/click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)
を正本とする。

2026-07-31にはCandidate125 root本文の水平適用をCodex CLI `0.146.0`で各case
N=5実施した。70 / 70件がvalid・rateableで、F10以外65 / 65件がscore `4`、
authorityなしF10はscore `1` × 5だった。保存済みC81はCLI `0.144.0`で非互換なため、
KPI差は算出しない。正本は
[`Click Candidate125 Medium Std14 r2 N=5 CLI 0.146`](../../results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md)
とする。
