# Candidate104 Rating v14 Medium A02 / F07 N=5

## 結論

Candidate104はA02 r2とF07 r2の各5件、計10件でvalid・rateable・score `4`だった。F07は5 / 5で対象外を含む広い検索と履歴参照を行わず、A02は5 / 5でclarificationを返さずrepository authorityから正規routeを解決した。A02でrequested valueをbindした後のauthority、fixture、履歴探索も0 / 5だった。

現在状態を`targeted_a02_f07_evaluated / quality_gate_passed / mechanism_gate_passed / result_registered / standard14_not_started`とする。Standard14 N=5へ進めるが、Standard14通過前にB20、採用、release、本体反映へ進めない。

Candidate104の直接親はCandidate98である。Candidate57、58、62とCandidate99からCandidate103までは観測証拠であり、prompt lineageへ含めない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-staged-evidence-admission-r1` |
| bundle SHA-256 | `b25d13fb2f9d598adfae2359bd5cfbcef2591731d07e9165b1f9b3fc83e036b0` |
| direct parent | Candidate98 |
| cases | `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2`、`TC-F07-CANONICAL-V4-RUNNER/r2` |
| source Evaluation set | `the-caption-standard14-r1/r1` |
| registered coverage | A02 / F07、各iteration 1〜5 |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / runtime | `0.146.0` / Python `3.14.5` |
| execution | global queue、設定上の`M=24`、実同時実行10件、各`N=5` |
| result ID | `5f688da95ff4456cbd20448d77ee3a3f` |
| compatibility key | `361ed9be3892c5bb4d65e36126d5840806bb77645e8bc8aa604866916c649b0b` |

TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameterはCandidate103から変更していない。model slot発行前にA02とF07のiteration 1〜5をcoverageへbindし、一つのglobal queueで実行してLayer 4 resultを登録した。

## 品質と制御経路

| 指標 | A02 | F07 |
| --- | ---: | ---: |
| valid / rateable | 5 / 5 | 5 / 5 |
| score `4` | 5 / 5 | 5 / 5 |
| required command evidence | 5 / 5 | 5 / 5 |
| root-only | 5 / 5 | 5 / 5 |
| clarificationなし | 5 / 5 | 5 / 5 |
| 履歴参照なし | 5 / 5 | 5 / 5 |
| 対象外を含む広い検索なし | 対象外 | 5 / 5 |
| repository authorityから正規routeを解決 | 5 / 5 | 不要 |
| requested value bind後のauthority / fixture / 履歴探索なし | 5 / 5 | 5 / 5 |

F07は全5件が開始状態、`run.sh`、変更、required validation、差分確認の経路へ収束した。Candidate103で5 / 5発生したrepository全体、fixture、履歴、gate実装の変更前探索は0件だった。

A02はrequested outcome valueがTaskSpecで未固定のため、全5件が`run.sh`の不一致を観測後、repository authorityまたは現行entrypoint実体から`src.app.entrypoints.v4_daily_main`を解決した。値確定後に別authority、fixture、履歴へ探索を広げたrunはなかった。2件は変更後、TaskSpecの「既存test」を具体化するためtest設定を読んだ。これは変更前のoutcome authority探索ではなく、required validationの確定として記録する。

## token・elapsed診断

| case | token中央値 | token最小〜最大 | elapsed中央値 | elapsed最小〜最大 |
| --- | ---: | ---: | ---: | ---: |
| A02 | 157,918 | 130,236〜197,596 | 82.252秒 | 66.287〜98.136秒 |
| F07 | 127,465 | 106,746〜130,875 | 72.343秒 | 66.424〜73.458秒 |

F07の最大 / 最小比はtoken `+22.61%`、elapsed `+10.59%`である。互換条件のCandidate103 F07比ではtoken中央値`-7.19%`、elapsed中央値`-26.32%`だった。ただしCandidate103はmechanism gate不通過なので、この差だけをCandidate104の一般的効果へ帰属しない。

## 保存場所

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate104-staged-evidence-admission-v14-medium-a02-f07-n5-cli0146-20260730-r1`
- registered result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/5f688da95ff4456cbd20448d77ee3a3f.json`
- execution archive: `batch-001/compact/execution-evidence.tar.zst`

execution archiveはSHA-256 `1a82fb1426d29ae52f7ed120fec88c8db2115f3ada879b2920de1a6f526915c5`でseal済みである。非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。
