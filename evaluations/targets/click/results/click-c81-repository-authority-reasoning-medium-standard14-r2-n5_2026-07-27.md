# Click C81 / C81 + Repository Authority Medium Std14 r2 N=5

## 結論

C81存在下でもrepository authority availabilityは維持され、他13 caseへのquality
回帰はなかった。C81単体はF10以外の65件がscore `4`、F10の5件が
`authority_unavailable`でscore `1`だった。C81 + Repository Authorityは70件すべて
score `4`で、F10の5件もauthorityと3 sourceを照合してinventoryを完了した。

全140件がvalid・rateableで、excluded attemptとunexpected driftは0件だった。
また、同じauthority状態でC81の有無を比較すると、C81のtoken・elapsed削減方向は
authorityなし／ありの両方で維持された。

## 比較条件

| 条件 | prompt identity | result ID | score分布 | F10経路 |
| --- | --- | --- | --- | --- |
| C81 | `click-00e592c-validation-wrapper-precedence-r1` | `2d895cf954db4e5a8f35f08dce6f3362` | `1 = 5`, `4 = 65` | `authority_unavailable = 5` |
| C81 + Repository Authority | `click-00e592c-c81-repository-authority-r1` | `2c716bf594fb4983b9dd1dd15f67fc12` | `4 = 70` | `authority_available_inventory = 5` |

- set: `click-standard14-r2` / `r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Case / N / B / M: `14 / 5 / 1 / 24`
- rating: `click-outcome-abstract-condition-preserving-v10`
- set identity: `bbba58d8eb5c3dc6719a155d031d886917c2fed7bec19faf9a43dd65705f7ebe`
- compatibility key: `b9c7ee74d90b2c4d30926e5e44c0a5307690e81939fd359d571dceeb32c1a80a`
- comparison conditions SHA-256: `c2738a1d3375b510768ea5875dd32f659a392085381901717d1e11f213aec0f8`
- excluded attempt: 両条件`0`

合成bundleのroot `AGENTS.md`はC81 bundleとbyte-identicalで、`docs`、`src`、
`tests`の3本文はRepository Authority bundleとbyte-identicalである。

## 公式3 KPI

| KPI | C81 | C81 + Authority | 差 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 94.643 | 100.000 | +5.357 | +5.66% |
| all-agent token中央値 | 1,874,755 | 2,040,912 | +166,157 | +8.86% |
| elapsed中央値 | 909.390秒 | 1,014.403秒 | +105.013秒 | +11.55% |

quality差はF10だけで、各iterationとも`+5.357`だった。F10のcase別中央値はtokenが
53,265から131,179へ`+77,914`、elapsedが37.172秒から83.916秒へ`+46.744`秒だった。
authorityなしでは停止し、ありでは成果を完成するため、この差は同じdone conditionでの
prompt効率差ではない。

全体のpaired差はtoken、elapsedとも5 / 5 iterationで増加した。F10を除く13 caseでも
token合計差は5 / 5で正、elapsed合計差は4 / 5で正だった。ただしcase別token中央値は
増加10 case、減少4 caseに分かれ、sub本文の明示readも7 / 70件に限られたため、
全case共通の本文処理コストとは断定しない。

## C81効果のbridge比較

4条件は同じcompatibility keyを持つ。authority状態を固定したC81差は次のとおりである。

| authority状態 | C81なし | C81あり | quality差 | token差 | elapsed差 |
| --- | --- | --- | ---: | ---: | ---: |
| なし | No-AGENTS | C81 | 0.000 | -705,773（-27.35%） | -186.797秒（-17.04%） |
| あり | Repository Authority | C81 + Authority | 0.000 | -683,338（-25.08%） | -125.177秒（-10.98%） |

したがって、C81のtoken・elapsed削減方向はrepository authorityを追加しても維持された。
これはC81全文の構成効果であり、個別predicateへの因果帰属ではない。

## authority経路監査

- C81単体F10は5 / 5件が、root C81本文にClick command API authorityがないことを
  確認し、指定3 sourceを読まずに停止した。
- C81 + AuthorityのF10は5 / 5件が`src/AGENTS.md`本文をreadし、3 sourceと照合した。
- C81 + Authority全70件でsub本文の明示readは、`src/AGENTS.md`がF10の5件、
  `tests/AGENTS.md`がA02とF06の各1件、`docs/AGENTS.md`が0件だった。
- F10以外の65 / 65件は両条件ともscore `4`で、required command evidenceと
  expected changed pathsを維持した。

## 判定境界

- 事実: C81とC81 + Repository AuthorityのStd14 r2を各70件再実施した。
- 判定: C81とsub authorityは共存でき、F10のavailability差と他13 caseの品質を維持した。
- 判定: C81のtoken・elapsed削減方向はauthorityなし／ありの両条件で維持された。
- 非目標: sub追加時のtoken・elapsed増加を個別本文の因果効果へ帰属しない。
- 非目標: 採用、release、runtime projectionを判断しない。

## Evidence

- C81 campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-c81-reasoning-medium-standard14-r2-global-m24-n5-20260727-r1`
- C81 + Repository Authority campaign:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-c81-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-20260727-r1`
- direct comparison view:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-c81-repository-authority-reasoning-medium-standard14-r2-n5-20260727-r1.json`
- four-condition comparison view:
  `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-standard14-r2-four-condition-reasoning-medium-n5-20260727-r1.json`
- C81 result SHA-256: `5bbe2326fbeb7b2783dc4e0430fc9449a78e8275432273be3889835458f805d3`
- C81 + Authority result SHA-256: `62a431df9b9b1d2c83f41eef9dcaae8a2c9eb10cf36d996d8323e9c84b12efbd`
- 設計正本:
  [`Click C81 / C81 + Repository Authority Std14 r2比較設計`](../../../../docs/click-c81-repository-authority-standard14-r2-design.md)
