# Candidate147 自律review r2 root-only診断

## 結論

Candidate147のroot-only判定は3 case × N=5の15 / 15で期待成果と一致した。独立SAは全runで起動されなかったが、root-onlyの失敗またはSAによる改善を観測していないため、これをprompt gapまたはmechanism failureと判定しない。

現在状態は`root_only_outcome_verified / SA_necessity_not_demonstrated / information_blocking_benefit_not_evaluated / Candidate_not_justified`である。

## 固定条件

| field | value |
| --- | --- |
| Evaluation set | `the-caption-autonomous-review-r2 / r2` |
| Evaluation set identity | `bead87ccec88f9959f3dc1daea8f55c67e968a5c7b165417e8cc82b29edde426` |
| case revision | `r2-overlay-aware-seed-diff` |
| prompt | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| bundle SHA-256 | `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc` |
| rating contract | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| model / reasoning / CLI | GPT-5.6 Sol / Medium / Codex CLI `0.146.0` |
| coverage | 3 case × iterations `1..5` |
| configured max workers | `M=24` |

r2 preflightはr1/r2 fixture identityの完全一致、prompt overlay後のseed / target identity、非空source diff、AST parse、diff check、clean statusを3 caseで確認した。r1のcoverage欠落はr2で解消した。

## 期待成果と実測

| case | 期待成果 | root実測 | 元oracleのSA期待 | SA実測 | 現在の解釈 |
| --- | --- | ---: | ---: | ---: | --- |
| AR01 defect / favorable prior | 正しいfinding付き`blocked` | 5 / 5 | 1 / run | 0 / 5 | root-only欠陥検出pass |
| AR02 clean / negative prior | false blockerなしの`completion_ready` | 5 / 5 | 1 / run | 0 / 5 | root-only誤検出抑制pass |
| AR03 type-only / neutral prior | `completion_ready` | 5 / 5 | 0 / run | 0 / 5 | root-only低risk判定pass |

AR01は5 / 5で`format_test=args.force`と利用者影響を正しく示した。AR02は5 / 5で`bool(args.format_test)`が`store_true`の意味を保持すると判定した。AR03は5 / 5でtype-only cleanupと判定した。

元oracleはAR01 / AR02で独立SAを必須とした。しかしroot-only outcomeが10 / 10で成立しており、SAを使う必要条件を先に証明していない。このoracle routeを満たさなかったことだけでfailureとするのは循環である。

## Execution diagnostic

| observation | count |
| --- | ---: |
| executor-valid run | 15 / 15 |
| excluded attempt | 0 |
| expected disposition | 15 / 15 |
| root-only session | 15 / 15 |
| AST command exit 0 | 15 / 15 |
| seed diff check exit 0 | 15 / 15 |
| unexpected changed path | 0 / 15 |
| runner elapsed | `74.3780916670803`秒 |
| all-agent token合計 | `1,413,134` |

`command-protocol-audit/v1`はcaretを含むshell-quoted argvをrequired tokenと一致させられなかったが、一次eventには15 / 15 runで両required commandのexit 0がある。このcollector diagnosticはSA必要性の判断へ使わない。

## この試験で確認できないこと

- rootが実装producerでもある自己reviewで同じ精度になるか。
- root-onlyが失敗する変更で、独立SAだけが正解するか。
- 独立SAのfalse positiveがrootより増えないか。
- 情報封鎖ありSAと事前評価を継承したSAで精度差が出るか。

独立SAが存在しないため、worker packet、forbidden-input canary遮断、context isolationも未評価である。

## Gate判断

- root-only outcome diagnostic: pass、15 / 15
- autonomous root review: このcase範囲では成立
- SA necessity: not demonstrated
- information-blocking benefit: not evaluated
- prompt gap: not established
- quality score: not recorded
- Layer 4 registration: not performed
- Candidate: not created

## 後続の課題qualification

r2の後、rootに実装させたり失敗traceを待ったりせず、固定差分へ実装経緯を渡すcontext条件と、渡さないblind条件を作成した。

[情報封鎖review課題 qualification](candidate147-information-closure-task-qualification-dev-r1-r2_2026-08-04.md)のIQ04では、blind 5 / 5に対してcontext 3 / 5となり、情報封鎖の差を識別できるdevelopment課題を作成可能と確認した。この後続結果はr2の15 / 15または当時の判定を変更しない。さらに[held-out](candidate147-information-closure-heldout-r1_2026-08-04.md)はblind 10 / 10、context 10 / 10でB優位を再現しなかった。独立SA producer評価へ進まず、FR-01を`feature_need_not_demonstrated`で停止する。

## Primary artifact

- run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-result-effect-scope-v14-medium-autonomous-review-r2-n5-cli0146-20260804-r1`
- preflight: `execution-preflight.json`
- runner summary: `parallel-run/summary.json`
- final responses: `batch-n005/cycle/layer2/extensions/<run_id>/codex-adapter/final-response.txt`
- all-agent usage: `batch-n005/cycle/layer2/extensions/<run_id>/all-agent-usage/usage.json`
- command evidence: `batch-n005/cycle/layer2/extensions/<run_id>/all-agent-command-evidence/evidence.json`
