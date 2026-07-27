# Click No-AGENTS / Repository Authority Medium Std14 r2 N=5

## 結論

見直し後のClick Std14 r2は、THE-CAPTIONから移した実行判断点との互換性を達成した。
No-AGENTSとRepository Authorityを各70件実行し、F10以外の13 caseは両条件とも
65 / 65件がscore `4`だった。F10 r2はNo-AGENTSの5 / 5件が
`authority_unavailable`で停止してscore `1`、Repository Authorityの5 / 5件が
authorityと3 sourceを照合してinventoryを完了しscore `4`だった。

全140件がvalid・rateableで、excluded attemptとunexpected driftは0件だった。
したがって、既存13判断点の回帰を保ちつつ、THE-CAPTION F10と同じrepository
authority availabilityの差を全試験セット内でも再現した。

## 比較条件

| 条件 | prompt identity | result ID | score分布 | F10終端経路 |
| --- | --- | --- | --- | --- |
| No-AGENTS | `click-00e592c-no-agents-r1` | `7e2761fd9fbd45f38d0264d82a2b78de` | `1 = 5`, `4 = 65` | `authority_unavailable = 5` |
| Repository Authority | `click-00e592c-repository-authority-r1` | `bfa5fdf4d1f8405282f87efc289b114f` | `4 = 70` | `authority_available_inventory = 5` |

- set: `click-standard14-r2` / `r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Case / N / B / M: `14 / 5 / 1 / 24`
- rating: `click-outcome-abstract-condition-preserving-v10`
- set identity: `bbba58d8eb5c3dc6719a155d031d886917c2fed7bec19faf9a43dd65705f7ebe`
- compatibility key: `b9c7ee74d90b2c4d30926e5e44c0a5307690e81939fd359d571dceeb32c1a80a`
- excluded attempt: 両条件`0`

両profileのcomparison conditions SHA-256は
`c2738a1d3375b510768ea5875dd32f659a392085381901717d1e11f213aec0f8`
で一致し、異なるのはprompt identityだけである。

## 公式3 KPI

| KPI | No-AGENTS | Repository Authority | 差 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 94.643 | 100.000 | +5.357 | +5.66% |
| all-agent token中央値 | 2,580,528 | 2,724,250 | +143,722 | +5.57% |
| elapsed中央値 | 1,096.187秒 | 1,139.580秒 | +43.393秒 | +3.96% |

quality差はF10のscore `1`対`4`だけで発生し、各iterationで同じ`+5.357`だった。
F10のcase別token中央値は75,492から211,328へ`+135,836`、elapsed中央値は
40.084秒から111.059秒へ`+70.975`秒だった。authorityなしでは停止し、ありでは
authorityと3 sourceを読んで成果を作るため、これは同じdone conditionでのprompt
効率差ではなく、完了した作業量の差である。

全14 caseを合算したpaired iteration差は、tokenが`-119,918`から`+462,248`、
elapsedが`-57.319`秒から`+108.142`秒に分散した。M=24の並列実行でもあるため、
Std14集計のtoken・elapsed差をrepository authorityの一律な負荷とは判定しない。

## case回帰とauthority露出

- F01〜F08、F10-R、A01、A02は両条件65 / 65件がscore `4`で、成果条件と
  expected changed pathsを維持した。
- No-AGENTSのF10は5 / 5件が`src/AGENTS.md`不在を確認し、指定3 sourceを読まずに
  停止した。
- Repository AuthorityのF10は5 / 5件が`src/AGENTS.md`本文を直接readし、
  `decorators.py`、`core.py`、`__init__.py`と照合してinventoryを完了した。
- Repository Authority全70件のcommand traceで、本文の明示readは
  `src/AGENTS.md`が14件、`tests/AGENTS.md`が8件、`docs/AGENTS.md`が0件だった。
  配置したsub instructionが全caseへ一律に露出するのではなく、作業pathと明示探索に
  応じて露出するという従来の観測も維持した。

## 判定境界

- 事実: 見直した14 case、2条件、各N=5の全140件を再実施した。
- 事実: F10以外にquality回帰はなく、F10だけが期待したavailability経路へ分離した。
- 判定: Click Std14 r2は、THE-CAPTION由来の14実行判断点を比較する試験セットとして
  互換性を達成した。
- 非目標: 題材、repository規模、絶対token、絶対elapsedの同一性は要求しない。
- 非目標: Candidate採用、release、runtime projectionは別gateである。

## Evidence

- No-AGENTS campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-no-agents-reasoning-medium-standard14-r2-global-m24-n5-20260727-r1`
- Repository Authority campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-20260727-r1`
- comparison view:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5-20260727-r1.json`
- No-AGENTS result SHA-256: `b29868cf31ac07174e5b5adba6a11cfde79c3b938b5fa4020ccf193ceaabab6d`
- Repository Authority result SHA-256: `90c1d92c0ec6019bdad4fbd5d787cf952a0af9461626bd33570d7f5e11adabba`
- 設計正本:
  [`Click repository authority availability比較設計`](../../../../docs/click-repository-authority-availability-design.md)
