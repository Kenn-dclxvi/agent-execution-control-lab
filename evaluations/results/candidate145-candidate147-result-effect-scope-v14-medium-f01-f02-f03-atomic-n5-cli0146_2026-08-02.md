# Candidate147 Rating v14 Medium F01 / F02 / F03 atomic N=5

## 結論

Candidate147はF01 / F02 / F03各N=5の15 / 15件でscore `4`を維持し、狙った`result_effect_scope`も15 / 15件で成立した。

開始identityと初回の許可済みsource / test readは全件で同じmodel stepから発行された。共同result受領前のartifact変更とrequired validationは0件だった。source / test初回既知観測の共同発行も15 / 15件で維持した。

3 case集約中央値はCandidate145比でtoken `-135,338`（`-25.97%`）、elapsed `-68.696秒`（`-22.34%`）だった。case別tokenはCandidate125比`+2.43%〜+5.16%`まで縮まった。F02 elapsedだけはCandidate125比`+27.92%`が残る。

これはF01 / F02 / F03各N=5の局所結果である。Standard14全体、低頻度退行、採用可否へは一般化しない。

## Identityと実行

- candidate: `the-caption-3ce91a4-result-effect-scope-r1`
- direct parent: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`（Candidate145）
- bundle SHA-256: `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`
- changed target / axis: root `AGENTS.md` / `DECISION_BOUNDARY`のoperation class別result effect scope
- evaluation set / cases: `the-caption-standard14-r1 / F01, F02, F03`
- N / configured M: `5 / 24`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI / Python: `0.146.0 / 3.14.5`
- formal reference: Candidate145 F01 / F02 / F03 N=5 result `03a862cf469a4b0fbaf0cd1bc1386563`
- preflight compatibility key: `a1264d0c1bc19834f7ac43266bc2d1489bfddfae171ce7356cb20d4ce5c9cb11`
- Candidate147 pool: `7bfa7086e5960c705561d197cd378f0c542ce8918b95258de61a198a7567dda2`
- issued / valid / excluded: `15 / 15 / 0`
- selection / analysis: `ed4adb5afd1a498d96913499b1a8b9cb / 3e7cb71842904abfbb18e23f5edaef0b`
- registered subset result: `d752f7ee160e4f0ba8a65a2b74036d3f`
- atomic comparison key: `eff03fb5215d7742c58d2550c3c3125005b68fddf9e3703f0f5fc9115aa54d85`

比較前にCandidate145の固定Layer 1、全case fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動、token accountingを機械照合した。Candidate145の既存runは再実行せず、Candidate147の不足15 slotだけを発行した。

subset result登録時のcompatibility keyは、profileへ列挙した3 case fixtureだけを含むため`c024bec705b9ba022d9365a1bd5431dcb50fcbfbcb9b576dffa10886234ca6ee`である。KPI比較はこのresult keyをCandidate145の14-case fixture keyへ直接照合せず、実行前preflightと同一atomic comparison keyを持つ両analysisのmatched stratumで行った。

## 品質

15件はすべてscore `4`だった。required outcome、focused validation、full validation、許可変更path、終了条件を満たした。

- score `3`以下: 0件
- controller error: 0件
- excluded attempt: 0件
- command protocol violation: 0件

したがって初段quality gateは通過した。N=5なので低頻度の品質退行を否定しない。

## model step機構

model stepは`command_execution`件数ではなく、`item.completed / agent_message`を境界として数えた。複数commandの間に`agent_message`がなければ、同じmodel stepから発行されたtool call群として扱う。

| gate | 実測 |
| --- | ---: |
| identityと初回許可readの共同model step | 15 / 15 |
| source / test初回既知観測の共同発行 | 15 / 15 |
| 共同result受領前のartifact変更 | 0 / 15 |
| 共同result受領前のrequired validation | 0 / 15 |
| 利用先のない変更前追加evidence | 0 / 15 |

F02の2件は変更前に二つ目のread stepがあった。どちらも初回出力が途中で切れたことを受領した後、欠けた関数本体またはassertionへ範囲を限定した再読である。Candidate145のconsumer gateが許可する`missing / unreadable`後のcontinuationであり、開始identityと許可readの共同発行失敗ではない。

変更前model step中央値はF01 / F02 / F03すべて`1`だった。Candidate145の各`2`から一つ減り、Candidate125の各`1`と一致した。

## KPI比較

| case | candidate | token中央値 | elapsed中央値 | 変更前model step中央値 |
| --- | --- | ---: | ---: | ---: |
| F01 | C125 | 104,663 | 63.337秒 | 1 |
| F01 | C145 | 154,553 | 88.154秒 | 2 |
| F01 | C147 | 107,202 | 66.424秒 | 1 |
| F02 | C125 | 124,094 | 78.648秒 | 1 |
| F02 | C145 | 196,118 | 114.228秒 | 2 |
| F02 | C147 | 128,236 | 100.607秒 | 1 |
| F03 | C125 | 99,202 | 68.374秒 | 1 |
| F03 | C145 | 166,152 | 93.882秒 | 2 |
| F03 | C147 | 104,320 | 70.866秒 | 1 |

3 case集約中央値はCandidate145 `521,159 token / 307.558秒`に対し、Candidate147は`385,821 token / 238.862秒`だった。quality中央値は両方`100.000`である。

Candidate145比のcase別差は次のとおりである。

- F01: token `-30.64%`、elapsed `-24.65%`
- F02: token `-34.61%`、elapsed `-11.92%`
- F03: token `-37.21%`、elapsed `-24.52%`

Candidate125比では、tokenはF01 `+2.43%`、F02 `+3.34%`、F03 `+5.16%`だった。elapsedはF01 `+4.87%`、F02 `+27.92%`、F03 `+3.64%`だった。

## 解釈

事実として、Candidate147はCandidate145で分離していた開始identityと許可readを全15件で同じmodel stepへ戻し、変更とrequired validationだけを共同result後へ保持した。品質を落とさず、変更前model step中央値とtoken / elapsedの両方が3 caseすべてで低下した。

これは`result_effect_scope`が狙った経路へ作用した証拠である。ただしN=5では、全体cost改善や低頻度のdrift時安全性までは確定しない。特にF02 elapsedはC125との差が残り、初回content truncation後の限定continuationが2 / 5件ある。

後続の[`Standard14 N=5`](candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)は先行15 runを再利用し、不足55 runだけを発行した。70 / 70件がscore `4`で、Candidate145比token `-9.17%`、elapsed `-23.13%`だった。変更前step中央値は9 / 14 caseで低下した。一方、F06 tokenはCandidate145比`+28.09%`で局所残差として残った。

## 状態

`f01_f02_f03_n5_evaluated / quality_gate_passed / result_effect_scope_mechanism_15_of_15 / aggregate_cost_both_lower_than_c145 / standard14_n5_evaluated_after_targeted_gate / result_registered / adoption_not_decided`

## 結論表

| gate / 比較 | 実測 | 判定 |
| --- | ---: | --- |
| valid / score `4` | 15 / 15 | quality pass |
| score `3`以下 | 0件 | pass |
| identity + 許可read共同model step | 15 / 15 | mechanism pass |
| 共同result前の変更 / required validation | 0 / 15 | safety boundary pass |
| 利用先のない変更前evidence | 0 / 15 | pass |
| C147 - C145 token中央値 | `-25.97%` | lower |
| C147 - C145 elapsed中央値 | `-22.34%` | lower |
| C147 - C125 case別token | `+2.43%〜+5.16%` | near target |
| Standard14 | 70 / 70 score `4` | evaluated / quality pass |
| N>5 | 未発行 | not evaluated |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |
