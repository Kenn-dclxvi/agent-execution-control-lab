# Click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5

## 結論

Clickのtarget-local `AGENTS.md`が完全にない条件と、rootを置かず`docs/`、`src/`、
`tests/`だけへrepository固有のsub `AGENTS.md`を置く条件を、Medium Std14で
比較した。両条件とも70 / 70件がvalid・rateableで、全件score `4`だった。

Repository sub-AGENTSはNo-AGENTS比で、all-agent token中央値が`+96,331`
（`+3.74%`）、elapsed中央値が`+82.143`秒（`+7.90%`）だった。ただし3つの
sub本文は初期model contextへ自動注入されず、本文のreadを確認できたのはA01の
5 / 5件だけだった。したがって、この差を3つのsub instruction本文のStd14全体効果
とは解釈しない。

## 比較条件

| 条件 | prompt identity | target | result ID |
| --- | --- | ---: | --- |
| No-AGENTS | `click-00e592c-no-agents-r1` | 0 | `c8c1092f445f4c8ca67bd1fbe409e999` |
| Repository sub-AGENTS | `click-00e592c-repository-subagents-r1` | 3 | `00194b3331524a0c8b0e4895e6885aa9` |

- set: `click-standard14-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Case / N / B / M: `14 / 5 / 1 / 24`
- rating: `click-outcome-abstract-condition-preserving-v10`
- compatibility key:
  `ab324fc854989f27b51bb1e312bc6bb4881a17fe6cb07e06128c2d3b112c4039`
- excluded attempt: 両条件`0`

既存Bundle Aは0 byteのroot `AGENTS.md`を配置するため、No-AGENTS resultへ
流用していない。empty bundle対応により、No-AGENTSはtarget treeへfileを追加せず、
同じ固定metadataのempty overlay commitだけを作った。

## 公式3 KPI

| KPI | No-AGENTS | Repository sub-AGENTS | 差 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 2,579,130 | 2,675,461 | +96,331 | +3.74% |
| elapsed中央値 | 1,039.378秒 | 1,121.521秒 | +82.143秒 | +7.90% |

iteration別elapsedは、No-AGENTSが`1039.378 / 1086.269 / 1055.126 /
1033.528 / 1001.896`秒、sub-AGENTSが`1150.328 / 1136.621 / 1083.630 /
1121.521 / 1033.110`秒で、sub-AGENTS側が5 / 5回とも長かった。

## sub instructionの露出

70件の各root rolloutで初期`world_state.agents_md`を確認した。3つのsub本文が
初期contextへ入ったrunは`0 / 70`だった。全runで共通していた上位の日本語応答規則は
両条件に同一なので、target-local bundle差には含めない。

operation traceでは、A01の5 / 5件で`src/AGENTS.md`と`tests/AGENTS.md`の本文が
modelへ返った。4件はcommandに対象pathを明示し、残る1件も同じ本文を取得した。
A02は2 / 5件で`rg --files`が`AGENTS.md`の存在を列挙したが、本文のreadは確認
できなかった。他13 caseでsub本文の取得は確認できなかった。

| 範囲 | No-AGENTS token中央値 | sub-AGENTS token中央値 | 差 | 率 |
| --- | ---: | ---: | ---: | ---: |
| A01 | 140,482 | 253,524 | +113,042 | +80.47% |
| A01を除く13 caseのiteration合計 | 2,437,743 | 2,410,592 | -27,151 | -1.11% |

A01はpairedでも5 / 5件でtokenとelapsedが増え、paired差中央値は`+90,273 token`、
`+19.688`秒だった。A01は変更値が未確定のため確認して停止するcaseであり、sub
instructionを読んでもdone conditionは変わらない。このreadは成果品質を変えず、
追加contextだけを増やした。

A01を除くtokenは小幅に減ったが、sub本文の露出を確認できないため、本文の効果とは
扱わない。elapsedはA01を除いても中央値`+48.599`秒（`+4.92%`）であり、M=24の
host条件を含む記述値として保持する。

## 判定

- 事実: target-localなsub `AGENTS.md`の配置だけでは、root cwd開始の全caseへ
  本文は水平適用されなかった。
- 事実: 本文をreadしたA01では品質を維持したが、tokenとelapsedが増えた。
- 推論: THE-CAPTION ControlFreeRepositoryとClickの差を「4つのsub instruction本文が
  常にmodel contextへ入るため」とは説明できない。
- 非目標: この結果からsub instructionの削除、採用、release、Click本体への反映を
  判断しない。
- 次の比較でsub本文そのものの効果を測る場合は、rootから対象領域のauthorityを
  明示的に発見させる別構成が必要であり、今回のresultと同一identityへ混ぜない。

## Evidence

- No-AGENTS campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-no-agents-reasoning-medium-standard14-global-m24-n5-20260727-r1`
- Repository sub-AGENTS campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-repository-subagents-reasoning-medium-standard14-global-m24-n5-20260727-r1`
- comparison view:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-no-agents-repository-subagents-reasoning-medium-standard14-n5-20260727-r1.json`
- 設計正本:
  [`Click repository sub-AGENTS比較設計`](../../../../docs/click-repository-subagents-comparison-design.md)
