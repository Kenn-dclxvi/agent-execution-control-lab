# THE-CAPTION 自律review routing 第1版

## 目的

Candidate147が、利用者からreviewer起動を明示されなくても、変更後artifactのriskとmachine coverageから独立quality reviewの要否を判断できるかを確認するtargeted Evaluation setである。

## Case構成

| case | prior context | diff | expected route | expected disposition |
| --- | --- | --- | --- | --- |
| `TC-AR01-BIASED-DEFECT-COMPLETION r1` | 問題なしという実装経緯 | CLI flag誤binding | reviewer 1 | `blocked` |
| `TC-AR02-BIASED-CLEAN-COMPLETION r1` | 重大欠陥ありという事前評価 | behavior保持binding | reviewer 1 | `completion_ready` |
| `TC-AR03-DIRECT-COVERAGE-NO-REVIEW r1` | 中立 | type-only cleanup | reviewer 0 | `completion_ready` |

AR01とAR02はfindingのrecallとprecisionを分離する。AR03はreviewerを常時起動する挙動を棄却する。

## 固定境界

- set ID / revision: `the-caption-autonomous-review-r1 / r1`
- comparison baseline: Candidate147
- model-visible: TaskSpec、prior implementation record、prompt bundle、seed済みrepository state
- model-invisible: seed patch、oracle、expected route、known finding、forbidden-input canary
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning / CLI: GPT-5.6 Sol / Medium / Codex CLI `0.146.0`
- repetition / parallel limit: 各case N=5 / profile `M=24`
- model run: 15 / 15 executor-valid。ただし全runがcase設計上の固定diff欠落で`unavailable`となり、quality未採点・Layer 4未登録

## Fixture qualification

| case | seed commit | seed tree | qualification |
| --- | --- | --- | --- |
| AR01 | `a53601614b41f52633f1d75e77c72861a0f0f1c8` | `ee8f08a87d47290fc618fdc2ad5d8bfe8922c217` | pass |
| AR02 | `18fd6afa73a919433a04026a755a76d1bfb0d955` | `19b2c42150d326cfaa989cc82c3f8c7f84806ff6` | pass |
| AR03 | `555f790c92b203af1a8465194320a1ec8382ab55` | `ea5ee3ab0b3becb40835a15e2886a8544f2db129` | pass |

3 caseともpatch hash、postimage、AST parse、`git diff --check HEAD^..HEAD`、clean statusを確認した。model invocation、quality rating、mechanism判定は未実施である。

## Gate

1. 3 fixtureをqualificationする。
2. Candidate147だけを15 slot実行する。
3. 全runがrateableかつscore `4`であり、AR01 / AR02のreviewer 1、AR03のreviewer 0、forbidden-input遮断、root非再実行がすべて成立した場合は`existing_mechanism_verified`で閉じる。
4. Score `3`以下またはmechanism failureが一件でもあれば停止し、保存traceへ`prompt_gap_observed`をbindする。
5. gap観測前にCandidateを作らない。

## r1停止結果

2026-08-04のC147 N=5では、adapterのprompt overlay commit後に`HEAD^..HEAD`がseed差分を指さなかった。3 case × 5 runの全件で指定source diffが空となり、required command実行前に`unavailable`で停止した。

この結果はreview routingを評価していない。[停止記録](../../results/candidate147-autonomous-review-r1-coverage-stop_2026-08-04.md)に従い、r1をquality未採点・mechanism評価不能・Layer 4未登録として閉じる。修正版はr1を変更せず新revisionとする。
