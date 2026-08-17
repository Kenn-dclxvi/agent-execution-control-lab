# Candidate270 Standard14 N=5 評価

## 結論

Candidate270（`the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1`）は、Standard14の14項目を各5件で評価し、70 / 70件がScore `4`だった。required validationを持つ7項目35件では、全件でvalidation carrier機序も成立した。

ただし、Candidate147との互換比較では、5回の集約中央値がtoken `+18.16%`、elapsed `+9.09%`で、ともに増加した。したがって現在状態は、`standard14_evaluated / quality_gate_passed / validation_carrier_mechanism_passed / aggregate_cost_both_higher / cost_necessity_not_established / adoption_not_decided / release_not_created / projection_not_performed`とする。N=5の差を安定傾向とは扱わない。

この評価では、既存のCandidate270分析文書、比較解釈および保存済み分析結果を入力へ使っていない。固定bundle、Standard14 profile、保存済み一次result、write-once atomic run、persisted rolloutだけから結果を作成した。

## 固定条件と実行

- profile: `candidate270-natural-language-predicate-bound-validation-result-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- bundle SHA-256: `481a035966f1cc6ad8faba7fd05b07baf357d29e0a75dccc563963878547c439`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI: `0.146.0`
- 外側並列上限: `M=24`
- 比較基準: Candidate147一次result `f7baeadc5bd44399ac13cc0e0a8aff48`
- comparison compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- C270 Standard14一次result: [`3658861abc824d52b2fd49dbba6900d3.json`](3658861abc824d52b2fd49dbba6900d3.json)

preflightはprompt identity以外の全互換条件を照合して`ready`となり、50 slotだけを承認した。C270の既存一次resultからF01、F02、F03、F10 entrypointの各5件、合計20件をatomic runとして再利用し、残る10項目の各5件、合計50件だけを新規発行した。

新規50件は174.05秒の外側実行で全件terminalとなった。valid 50、excluded 0、再試行0、controller error 0だった。execution sealはworkspaceを検証済みarchiveへ保存した後、live workspaceから約1.49 GiBを回収した。

## 品質

一次resultの70件は、全項目で5 / 5件がScore `4`だった。新規50件の採点では、成果不成立、必須command違反、許可外path変更、command protocol違反はいずれも0件だった。

owner-producer evidenceは新規50件中40件が`failed`、10件が`not_applicable`だった。これは独立producerの成立証拠を確認できなかったという診断であり、Rating v14の`diagnostic_only`規則に従って品質点へ混ぜていない。

## validation carrier機序

[`candidate270-natural-language-predicate-bound-validation-result-standard14-n5-validation-carrier-audit-r1.json`](candidate270-natural-language-predicate-bound-validation-result-standard14-n5-validation-carrier-audit-r1.json)は、required validationを持つ7項目35件をpersisted rolloutの`response_item`で監査した。

| 項目 | 成立 | nonterminal receipt | 途中validation出力 |
|---|---:|---:|---:|
| F01 duplicate asset key | 5 / 5 | 3 | 0 byte |
| F02 history date bound | 5 / 5 | 2 | 0 byte |
| F03 atomic cleanup | 5 / 5 | 2 | 0 byte |
| F04 web audit column | 5 / 5 | 5 | 0 byte |
| F06 empty snapshot | 5 / 5 | 9 | 0 byte |
| F07 canonical runner | 5 / 5 | 5 | 0 byte |
| F07 dependency provenance | 5 / 5 | 0 | 0 byte |
| 合計 | 35 / 35 | 26 | 0 byte |

全35件で、required validationは一つの外側`exec` callに入り、nonterminal時の継続は同じcell IDへの`wait`だけで、AIへ返るvalidation resultは一つのterminal outputだった。機序不成立0件、観測不能0件である。

## Candidate147との3 KPI比較

Candidate147も既存分析値を流用せず、保存済みatomic runから同じ14項目×5件のselectionを新規作成し、同じ集計器で再集計した。

| 指標 | Candidate147 | Candidate270 | 差分 |
|---|---:|---:|---:|
| quality中央値 | 100.00 | 100.00 | 0.00 |
| token中央値 | 1,447,626 | 1,710,578 | +262,952（+18.16%） |
| elapsed中央値 | 852.54秒 | 930.00秒 | +77.46秒（+9.09%） |

項目別中央値は次のとおりである。

| 項目 | C147 token | C270 token | token差 | C147 elapsed | C270 elapsed | elapsed差 |
|---|---:|---:|---:|---:|---:|---:|
| A01 | 19,195 | 20,059 | +4.50% | 12.15秒 | 11.42秒 | -6.01% |
| A02 | 129,085 | 194,840 | +50.94% | 73.38秒 | 89.97秒 | +22.61% |
| F01 | 107,202 | 121,788 | +13.61% | 66.42秒 | 67.46秒 | +1.57% |
| F02 | 128,236 | 138,017 | +7.63% | 100.61秒 | 76.98秒 | -23.49% |
| F03 | 104,320 | 128,806 | +23.47% | 70.87秒 | 70.55秒 | -0.44% |
| F04 | 151,170 | 182,485 | +20.72% | 91.43秒 | 104.24秒 | +14.01% |
| F05 clarify | 37,242 | 42,225 | +13.38% | 26.73秒 | 24.26秒 | -9.21% |
| F05 out-of-scope | 37,366 | 42,437 | +13.57% | 25.29秒 | 27.10秒 | +7.15% |
| F06 | 151,542 | 150,164 | -0.91% | 79.39秒 | 96.90秒 | +22.05% |
| F07 canonical | 102,504 | 134,020 | +30.75% | 72.55秒 | 86.51秒 | +19.25% |
| F07 dependency | 87,284 | 91,964 | +5.36% | 54.32秒 | 54.06秒 | -0.49% |
| F08 | 113,067 | 141,024 | +24.73% | 56.34秒 | 80.07秒 | +42.11% |
| F10 entrypoint | 87,934 | 114,084 | +29.74% | 61.55秒 | 64.03秒 | +4.04% |
| F10 monthly | 93,096 | 138,512 | +48.78% | 51.80秒 | 58.58秒 | +13.09% |

tokenは14項目中13項目で増え、elapsedは8項目で増えた。大きい増加はA02、F10 monthly、F07 canonical、F08に集中している。ただし、このN=5結果だけでは、増加がCandidate270の差分文に因果帰属することも、必要な正常経路を維持するための不可避なcostであることも確定していない。

## 保存先と状態

raw試験rootは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate270-natural-language-predicate-bound-validation-result-v14-medium-standard14-n5-cli0146-20260817-r1`である。preflight、50件の実行証拠、fresh selection、fresh C147再集計、比較view、quality audit、validation carrier監査、execution sealを保持する。

この結果はStandard14 N=5の評価完了を示す。採用、release作成、THE-CAPTION本体へのprojectionは承認も実施もしていない。
