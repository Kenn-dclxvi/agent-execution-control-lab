# Candidate147 自律review r1 coverage停止記録

## 結論

`the-caption-autonomous-review-r1`はcase設計のcoverage gateで停止した。Candidate147のreview qualityまたは自律routingは評価していない。

2026-08-04にCandidate147を3 case × N=5で実行した。15 / 15 runはexecutor上valid、excluded attempt 0だった。一方、15 / 15 runでmodel-visibleな`HEAD^..HEAD -- src/app/entrypoints/monthly_main.py`が空になり、全runが`unavailable`で停止した。required machine validationも15 / 15 runで未実行だった。

原因は、fixtureのseed commit後にevaluation adapterがprompt overlay commitを追加するためである。実行時の`HEAD^..HEAD`はseed差分ではなくprompt overlay差分を表す。case r1のTaskSpecはこのcommit境界を誤って固定していた。

したがって、この15 runへquality scoreを付けない。Layer 4へ登録しない。`prompt_gap_observed`、`existing_mechanism_verified`、Candidate作成のいずれにも進めない。

## 固定条件

| field | value |
| --- | --- |
| Evaluation set | `the-caption-autonomous-review-r1 / r1` |
| Evaluation set identity | `9494ee941767bb7daad861e971f5867d38af8166cc7c82cdd80a02490acec418` |
| prompt | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| bundle SHA-256 | `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc` |
| rating contract | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| model / reasoning / CLI | GPT-5.6 Sol / Medium / Codex CLI `0.146.0` |
| permission | `workspace-write / never` |
| coverage | 3 case × iterations `1..5` |
| configured max workers | `M=24` |

preflight r1はrating contract objectの不一致によりmodel invocation前に15 / 15 controller拒否となった。有効runは0件である。履歴を上書きせず、v14正本と完全一致させたr2 preflightを新規作成した。

r2 preflightはset、fixture、TaskSpec、profile、prompt、rating、model、reasoning、CLI、permission、coverage、planを固定し、15 slotを承認した。

## 観測結果

| observation | count |
| --- | ---: |
| executor-valid run | 15 / 15 |
| excluded attempt | 0 |
| final disposition `unavailable` | 15 / 15 |
| 固定source diffが空 | 15 / 15 |
| required command 2件とも未実行 | 15 / 15 |
| root-only session | 15 / 15 |
| child / additional tokens | 0 / 15 run |
| quality rating | 0 / 15 |
| Layer 4 registration | 0 |

runner elapsedは`70.52190941711888`秒、invalid case executionのall-agent token合計は`1,043,298`だった。caseが目的のreview判断点へ到達していないため、これらをqualityまたはcost KPIへ使用しない。

## 解釈

root-only 15 / 15はreviewer未起動を示す。しかし全runが固定diff欠落の停止条件で終了しているため、自律review routingの不成立根拠には使えない。事前評価canaryの遮断、finding recall、finding precision、不要review抑止も評価不能である。

現在状態は`case_design_invalid / coverage_gate_failed / quality_not_rated / mechanism_not_evaluable / result_not_registered / stopped`とする。

## 再開条件

既存r1を変更せず、新しいEvaluation set revisionを作る。新revisionはadapterのprompt overlay commitをmodel-visible境界へ含め、seed差分を一意に参照できるidentityを固定する。現行adapter境界を使う場合、source差分は`HEAD^^..HEAD^`、seed commitは`HEAD^`として扱う必要がある。

新revisionではmodel slot発行前に、prompt overlay適用後workspace上で次をqualificationする。

1. 3 caseとも指定source diffが非空である。
2. AR01 / AR02 / AR03のpostimageとdiff identityがprivate oracleに一致する。
3. required machine validationのexact argvが実行可能である。
4. model-visible TaskSpecが実際のcommit境界と一致する。

再qualification前にCandidate、Baseline正のcontrol、追加model slotを作成または発行しない。

## Primary artifact

- r1 controller rejection: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-result-effect-scope-v14-medium-autonomous-review-n5-cli0146-20260804-r1`
- r2 execution: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-result-effect-scope-v14-medium-autonomous-review-n5-cli0146-20260804-r2`
- r2 preflight: `r2/execution-preflight.json`
- r2 runner summary: `r2/parallel-run/summary.json`
- blind final responses: `r2/batch-n005/cycle/layer2/extensions/<run_id>/codex-adapter/final-response.txt`
- command audit: `r2/batch-n005/cycle/layer2/extensions/<run_id>/command-protocol-audit/audit.json`

