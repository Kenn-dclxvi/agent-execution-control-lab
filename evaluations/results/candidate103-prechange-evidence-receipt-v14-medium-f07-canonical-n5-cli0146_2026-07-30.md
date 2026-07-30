# Candidate103 Rating v14 Medium F07 canonical N=5

## 結論

Candidate103はF07 canonical r2の5 / 5でvalid・rateable・score `4`だった。しかし、最初のinvocation前に`PRECHANGE_RECEIPT`を出したのは4 / 5で、対象外を含む広い検索なしは0 / 5、履歴参照なしは4 / 5だった。

実行票を先に出した4件も、repository authority、fixture、開始gateの実装箇所等の広い探索をconsumerへ含めて正当化した。残る1件は広い探索後に実行票を出した。F07-C1〜C3、checkout identity、clean statusはTaskSpecに明示済みであり、新しい判断項目を作ったことが主因ではない。固定済み判断へ必要な証拠の範囲を、TaskSpecで十分な入力が与えられた後も広げたことが主因である。

設計の停止条件に従い、現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。

Candidate103の直接親はCandidate98である。Candidate99からCandidate102まではprompt lineageへ含めず、誤経路の観測証拠としてだけ参照した。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-prechange-evidence-receipt-r1` |
| bundle SHA-256 | `e3acc82d0712db6c2834dc69d154a50f470cc119db2db0bb2ed1ceb6cbfede8f` |
| direct parent | Candidate98 |
| case | `TC-F07-CANONICAL-V4-RUNNER/r2` |
| source Evaluation set | `the-caption-standard14-r1/r1` |
| registered coverage | F07、iteration 1〜5 |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / runtime | `0.146.0` / Python `3.14.5` |
| execution | global queue、設定上の`M=24`、実同時実行5件、`N=5` |
| result ID | `ca504a5203f24b93a3111eaa434a9f81` |
| compatibility key | `06b6c76f2ed5a00bea385adcd7c7f3f7d5619da55d2847e22c17501e0fb8d72f` |

TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameterはCandidate102から変更していない。model slot発行前にF07 iteration 1〜5をcoverageへbindし、Layer 4 resultを登録した。

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| required command evidence | 5 / 5 |
| command protocol violation | 0 / 5 |
| excluded attempt | 0 |
| root-only | 5 / 5 |

## 変更前実行票

| iteration | command数 | 最初のcommand前に実行票 | 履歴参照なし | 広い検索なし | 判定 |
| ---: | ---: | --- | --- | --- | --- |
| 1 | 13 | 成立 | 成立 | 不成立 | mechanism不成立 |
| 2 | 9 | 成立 | 成立 | 不成立 | mechanism不成立 |
| 3 | 12 | 成立 | 不成立 | 不成立 | mechanism不成立 |
| 4 | 11 | 成立 | 成立 | 不成立 | mechanism不成立 |
| 5 | 14 | 不成立 | 成立 | 不成立 | mechanism不成立 |

iteration 1〜4は実行票を先に出したが、TaskSpecが既に指定するF07-C1〜C3と開始条件の証拠として、repository authority、fixture、開始gateの実装箇所等を追加で探索した。実行票は追加探索を止める境界ではなく、固定済み判断に対する証拠範囲を広げる説明欄になった。

iteration 5は`rg --files`とrepository全体の文字列検索を行った後で`spec_ready=true`とし、観測済み結果を`PRECHANGE_RECEIPT`へ記載した。これは発行前固定の違反である。iteration 3はさらに`git log -1`を実行した。

保存済みCandidate100 iteration 4では、同じTaskSpecに対してcheckout identity、clean status、`run.sh`だけを読み、修正とrequired validationへ進んだ。これはTaskSpecの判断項目と必要な入力が不足していない直接証拠である。

したがって、次の制御対象はpredicate identityではない。固定済みpredicateについて、TaskSpecが指定した値、開始条件の直接観測、target artifactの現在内容で判定可能になった時点を証拠十分として扱い、矛盾を実際に観測していない限り別authority、fixture、履歴、gate実装の探索へ広げない境界である。新しいcandidateを作る前に、Candidate99〜Candidate103がこの証拠十分条件をなぜ表現できなかったかを比較する。

## token・elapsed診断

| iteration | all-agent token | elapsed |
| ---: | ---: | ---: |
| 1 | 137,344 | 96.443秒 |
| 2 | 133,600 | 98.189秒 |
| 3 | 135,937 | 78.875秒 |
| 4 | 214,087 | 110.478秒 |
| 5 | 148,747 | 158.113秒 |
| 中央値 | 137,344 | 98.189秒 |
| 最小〜最大 | 133,600〜214,087 | 78.875〜158.113秒 |

最大 / 最小比はtoken `+60.25%`、elapsed `+100.46%`である。互換なCandidate102比でtoken中央値は`-10.82%`、elapsed中央値は`+14.78%`だった。品質は維持したがmechanism gateが0 / 5なので、この差を実行票の効果へ帰属しない。

## 保存場所

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate103-prechange-evidence-receipt-v14-medium-f07-canonical-n5-cli0146-20260730-r1`
- registered result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/ca504a5203f24b93a3111eaa434a9f81.json`
- execution archive: `batch-001/compact/execution-evidence.tar.zst`

execution archiveはSHA-256 `3cb49dfc3492d30eddf211f4cb0355eb7881f7a9823ce992671bfbbf12ed93d8`でseal済みである。非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。
