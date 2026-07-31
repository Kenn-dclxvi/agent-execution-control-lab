# Candidate122 / Candidate125 criterion-complete single-target continuation Rating v14 Medium A01 / A02 / F01 / F02 / F04 atomic N=5

## 結論

Candidate125は初回targeted gateを通過した。25 / 25件がvalidかつscore `4`だった。F04は5 / 5件が変更と3つのrequired Node validationを完了し、false stopは0件だった。変更前contentが出力上限または初回rangeで不足した場合も、全5件が同じ`App.tsx`への一回のcriterion-complete continuationで変更predicateをbindした。

F02は5 / 5件がinitial content後の追加readなしで変更へ進み、content waveを5 / 5で維持した。token中央値`124,094`は目標`173,000`を`48,906`（`28.27%`）下回った。

現在状態は`targeted_a01_a02_f01_f02_f04_evaluated / quality_gate_passed / f04_false_stop_closed / f04_criterion_complete_continuation_passed / f02_content_wave_preserved / f02_cost_target_passed / result_registered / adoption_not_decided`とする。Standard14、採用、release、runtime projection、本体反映は別判断である。

## Identity

- Candidate125 prompt: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- bundle SHA-256: `60e95bfe7f9e09a0cbb2fb980c54f1cd1bd671c37509976e7e88574adf911435`
- profile: `candidate125-criterion-complete-single-target-continuation-v14-reasoning-medium-a01-a02-f01-f02-f04-global-m24-n5-cli0146-r1`
- reference Candidate118 result: `374b32b97f0048e2a39f108cb197a921`
- Candidate125 pool: `6dfc222af7bf84dec1699582beb2c499ce44e8b6f461fc1972a703bc09ab079c`
- Candidate125 selection: `7e839150902045349968acaf40e5da7c`
- Candidate125 analysis: `eab12c368023410e993ec39bbcbfda4f`
- Candidate125 result: `2f9c87c6420046478405e0270d983d73`
- execution: 25 / 25 valid、excluded 0、profile上の`M=24`
- execution archive SHA-256: `23c25c76bd2777129f50a88e559e83f4c2203130539faa528be75f022b9be152`
- final compact archive SHA-256: `7d5d4a7df218cfe35076302c354031f98f7aab0816b1704905e8998cb1d4e722`

## Case別結果

| case | score `4` | token中央値 | mechanism |
|---|---:|---:|---|
| A01 | 5 / 5 | `17,462` | required value待ち、変更・testなし |
| A02 | 5 / 5 | `141,143` | canonical成果、validation method追加探索なし |
| F01 | 5 / 5 | `104,663` | required command evidence完備 |
| F02 | 5 / 5 | `124,094` | content wave 5 / 5、追加read 0 / 5 |
| F04 | 5 / 5 | `166,255` | false stop 0 / 5、criterion-complete continuation 5 / 5 |

5-case集約中央値はquality`100.000`、token`593,330`、elapsed`346.273秒`である。targeted 5 case値は正式なStandard14 KPIの代替にはしない。

## F04の経路

F04はTaskSpecがeditable targetを`App.tsx`一つに限定し、`package.json`と`package-lock.json`はvalidation capabilityの確認対象だった。このため`single_change_target_ready=true`となる。

5件は、初回のpartial contentまたは全contentのmodel-visible出力に不足があった後、同じ`App.tsx`の全未取得contentまたは一覧block全体へ一度だけcontinuationした。変更前に二回目のcontinuation、新しいtarget、repository-wide searchは開いていない。C124の620行終端によるfalse stopは再発しなかった。

## F02の経路

F02は4 editable targetが変更predicateと保持constraintを共同で決めるため、`single_change_target_ready=false`である。5件ともC122のinitial content waveを維持し、content result後に追加rangeまたはsymbol readを発行しなかった。これによりC124の追加read 2 / 5とtoken中央値`188,908`は再発せず、Candidate122の`124,719`と同水準へ戻った。

## 次の判断

targeted gateは通過したため、Candidate125の登録済み25 runを再利用し、Standard14の残り9 case各5件だけを実行する。正式な判断は70件のquality分布とStandard14 token中央値がCandidate107目標`1,523,137`以下かで行う。
