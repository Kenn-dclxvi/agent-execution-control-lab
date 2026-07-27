# Click No-AGENTS / Repository Authority Medium F10 authority N=5

## 結論

THE-CAPTION F10と同じrepository authority availabilityの差をClickでも再現した。
No-AGENTSは5 / 5件が`authority_unavailable`でsource-only推論をせず停止し、
score `1`だった。Repository Authorityは5 / 5件が`src/AGENTS.md`を読み、
指定3 sourceと照合してinventoryを完了し、score `4`だった。全10件がvalid・
rateable、zero driftで、excluded attemptは0件だった。

この結果は、repository authority本文が利用可能なときだけ、TaskSpecが要求する
authority-bound inventoryを完成できることを示す。1 caseのavailability差であり、
sub instruction全般、Std14全体、C81、採用、release、Click本体への反映へは
一般化しない。

## 比較条件

| 条件 | prompt identity | result ID | score分布 | 終端経路 |
| --- | --- | --- | --- | --- |
| No-AGENTS | `click-00e592c-no-agents-r1` | `b9b7277c39a146d7852752a05bf48270` | `1 = 5` | `authority_unavailable = 5` |
| Repository Authority | `click-00e592c-repository-authority-r1` | `699004d386c64c438bb490ab17992d2f` | `4 = 5` | `authority_available_inventory = 5` |

- set: `click-f10-authority-availability-r1` / `r1`
- case: `CLICK-F10-COMMAND-API-INVENTORY/r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Case / N / B / M: `1 / 5 / 1 / 24`
- rating: `click-outcome-abstract-condition-preserving-v10`
- set identity:
  `6fcfc544a1326cf77c379c5a3050ab3940597fdbaae3e74e993e8a20bb6955e7`
- compatibility key:
  `229d9d93047da4d1691825e8f0b03bf33224305791e616f54c47f87638fb0f46`
- excluded attempt: 両条件`0`

両profileのcomparison conditions SHA-256は
`275ccdd96933f8c12755ba4c24b0e8fb66885520f86a219aae40ad1bdbe5ca9e`
で一致する。empty bundleとauthority bundleは、いずれも固定Click commitを親とする
metadata overlay commitを1段作る。開始HEADの段数は同じである。

## 公式3 KPI

| KPI | No-AGENTS | Repository Authority | 差 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 25.000 | 100.000 | +75.000 | +300.00% |
| all-agent token中央値 | 64,147 | 216,055 | +151,908 | +236.81% |
| elapsed中央値 | 59.017秒 | 102.318秒 | +43.300秒 | +73.37% |

No-AGENTSはauthority確認後に主要成果を作らず停止し、Repository Authorityは
authorityと3 sourceを読んでinventoryを完成した。両条件の作業量とdone conditionが
実際に分岐するため、tokenとelapsedの増加をprompt効率の悪化とは扱わない。

No-AGENTS iteration 3は253.441秒で、他4件の44.527〜72.528秒から外れた。
5件合計elapsedはNo-AGENTS 482.279秒、Repository Authority 510.917秒である。
M=24環境の1件の待ち時間が合計へ影響するため、elapsedの固有効果は主張しない。

## 経路監査

No-AGENTSの5件はすべて`src/AGENTS.md`の不存在を確認した後、
`src/click/decorators.py`、`src/click/core.py`、`src/click/__init__.py`を読まずに
停止した。adapterが確認した最終changed pathsは全件空だった。

Repository Authorityの5件はすべて次を満たした。

- `src/AGENTS.md`の`Command construction API authority`節を直接read
- `click.command`と`click.group`を`src/click/decorators.py`で確認
- `Command`、`Group`、`CommandCollection`を`src/click/core.py`で確認
- public exportを`src/click/__init__.py`で確認
- test、edit、外部operationを行わずzero driftで終了

したがって、THE-CAPTION ControlFreeGeneric / ControlFreeRepositoryのF10で観測した
「authorityなしでは停止し、authorityありでは同じinventoryを完成する」方向は、
Clickのrepository固有authorityでも再現した。

## 判定境界

- 事実: authority availabilityにより5 / 5対5 / 5で終端経路とscoreが分離した。
- 事実: source-only推論、unexpected drift、excluded attemptは0件だった。
- 推論: Clickでもrepository authorityは、TaskSpecがそれを成果前提へ明示した場合に
  意味のある差を作る。
- 非目標: 配置だけのStd14 resultを上書きしない。F10以外への効果を主張しない。
- 非目標: Candidate採用、release、runtime projectionを判断しない。

## Evidence

- No-AGENTS campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-no-agents-reasoning-medium-f10-authority-global-m24-n5-20260727-r1`
- Repository Authority campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-repository-authority-reasoning-medium-f10-authority-global-m24-n5-20260727-r1`
- comparison view:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5-20260727-r1.json`
- No-AGENTS result SHA-256:
  `6823b3944a5ffefc149d74dd250ec28fc4b2606c53e8bc1a33b8a6300500fc5b`
- Repository Authority result SHA-256:
  `12d66ae20fa51575121089e23a1b84a6600e16ebfd31c8f010e3cc9b4ea640fc`
- 設計正本:
  [`Click repository authority availability比較設計`](../../../../docs/click-repository-authority-availability-design.md)
