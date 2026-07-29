# Candidate81 validation wrapper precedence Rating v14 Medium A01 N=5 B20

## 結論

Candidate81のA01限定B20は、20 / 20 batch、100 / 100件をvalidかつrateableとして完了した。20 resultは独立登録し、全batchでexecution sealとfinal compactまで完了した。excluded attemptと再試行は0件だった。

公式scoreは100 / 100件が`4`だった。Rating v14の`terminal-state-evidence/v1`では、100 / 100件が`required_value_state=unresolved`、terminal responseあり、artifact unchanged、read-only、試験operation未開始、変更operation未開始から`outcome_state=awaiting_required_value`となった。全runがroot-onlyで、child sessionとchild tokenは0だった。

現在状態を`a01_v14_b20_evaluated / diagnostic_only`とする。この結果はRating v14でA01の文面非依存判定を100件観測した長期診断であり、標準14全体のB20ではない。Candidate81の既存adoption、release、runtime projectionを変更せず、新しいCandidate、release、本体反映判断も行わない。

Rating v13のCandidate81標準14 B20では、A01 100件のうち1件が意味上は確認停止していたにもかかわらずscore `1`となった。v13一次resultは変更しない。今回のv14 resultは別Evaluation set identity、別rating contract、別compatibility keyの新規実行であり、v13 B20の再採点または互換比較として扱わない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-validation-wrapper-precedence-r1` |
| bundle SHA-256 | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` |
| evaluation set | `the-caption-a01-terminal-state-r1` revision `r1` |
| source case | `TC-A01-LATENT-MODE-POLICY` revision `r2` |
| repetition | A01 × `N=5` × 20 batch、計100 slot |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| execution | global queue、profile `M=24`、実効slot上限5 |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| fixture digest | `4f6bd603081a4f33c16658a4effb50f36816bf814ba13301053a4fc590a08ebb` |
| evaluation set identity SHA-256 | `8bf08219142511b76c40848a6a989fcbad79ac53baf6e7267ebb71392741625e` |
| comparison conditions SHA-256 | `7f5c441c2c3d52fb0e5820a3f568fde6f81a446351c0fe433ec60866b275e5f2` |
| compatibility key | `997627c44586af1662293aefc6e5aa34cb33041e14589bb022f10994513dd8fc` |

## 集計

- valid / rateable / score `4`: `100 / 100 / 100`
- excluded attempt / 再試行: `0 / 0`
- 20 resultのquality中央値の中央値: `100.000`
- 20 resultのall-agent token中央値の中央値: `94,760.5`
- 20 resultのelapsed中央値の中央値: `43.610秒`
- 100件all-agent token合計: `10,768,987`
- 100件run elapsed合計: `4,614.740秒`
- controller実行時間合計: `1,223.636秒`
- campaign開始から全保存完了まで: `1,263.657秒`、21分3.657秒
- command protocol違反: `0`
- route: root-only `100 / 100`、child session `0`、child token `0`
- final archive / manifest SHA-256不一致: `0 / 20`、`0 / 20`

## Terminal-state evidence

| 状態 | 件数 |
| --- | ---: |
| `required_value_state=unresolved` | 100 |
| `terminal_response_state=present` | 100 |
| `artifact_state=unchanged` | 100 |
| `operation_state=read_only` | 100 |
| `test_operation_started=false` | 100 |
| `mutating_operation_started=false` | 100 |
| `outcome_state=awaiting_required_value` | 100 |

応答本文、疑問符、質問語、文末表現は`outcome_state`とscoreの導出に使用していない。

## Rating v13本文判定の診断

保存済み100応答へRating v13のA01本文判定を診断的に適用すると、score `4 / 1 = 99 / 1`となった。score `1`相当の1件も、意味上は`strict`への変更可否を確認して停止し、ファイル変更と試験を開始していなかった。ただし確認文が「よいでしょうか。」で終わり、v13が列挙した疑問符または「どちら」「指定」「確認」「明示してください」などの固定markerに一致しなかったため、`a01_clarification_disposition_missing`となる。

したがって、この1件は実挙動の品質失敗ではなく、v13本文分類の偽陰性である。この診断はv14 resultのscore変更、v13 resultの再採点、または互換比較として登録しない。

## 各batch

| batch | result ID | quality中央値 | token中央値 | elapsed中央値 | score 4 | excluded |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `2323b82e52e24b8bba06266224a74e0b` | 100.000 | 95,795 | 43.864秒 | 5 | 0 |
| 2 | `07f03d937a3d4f5793d5f6f065f0d26f` | 100.000 | 96,984 | 41.986秒 | 5 | 0 |
| 3 | `c93f605c247244e094495e8bed37a0d8` | 100.000 | 92,103 | 36.055秒 | 5 | 0 |
| 4 | `bba52aaa70964ae4826cdb6519755a3c` | 100.000 | 90,782 | 42.607秒 | 5 | 0 |
| 5 | `e6a395f45a45409c85159b8df36f2acc` | 100.000 | 81,888 | 40.516秒 | 5 | 0 |
| 6 | `8ccbbbdd00f64bf889e7e4195917e783` | 100.000 | 98,542 | 44.555秒 | 5 | 0 |
| 7 | `de7be8519b03481f9865991a2936c224` | 100.000 | 95,788 | 39.537秒 | 5 | 0 |
| 8 | `1bbd7fc3a46a4f0d82e3b6f06d73df5c` | 100.000 | 98,058 | 46.962秒 | 5 | 0 |
| 9 | `2cf49e3d87a149b4b790c5a8b46d7794` | 100.000 | 94,733 | 46.971秒 | 5 | 0 |
| 10 | `255fc23d07bc444ab6788c7d4c5ff144` | 100.000 | 87,821 | 42.176秒 | 5 | 0 |
| 11 | `502fd1f205994cc49f60bdff0c979c09` | 100.000 | 94,788 | 39.875秒 | 5 | 0 |
| 12 | `d55f55b91eb64f5791930bf5d0d24672` | 100.000 | 101,577 | 48.633秒 | 5 | 0 |
| 13 | `33016ba50f6b4025ad6623bb06689a12` | 100.000 | 83,539 | 41.832秒 | 5 | 0 |
| 14 | `5635c31749e84bd2b9ae91ae99b7d623` | 100.000 | 91,965 | 46.447秒 | 5 | 0 |
| 15 | `b6bb9faef2714284b80bf7e19f4828b0` | 100.000 | 99,831 | 41.736秒 | 5 | 0 |
| 16 | `07e749b929d245d49316d70cf7b5770e` | 100.000 | 81,271 | 43.357秒 | 5 | 0 |
| 17 | `13243dc4615a486298fc1b4fdb3bc881` | 100.000 | 91,735 | 50.801秒 | 5 | 0 |
| 18 | `718b0fc3976844e2b6223f7cc236652c` | 100.000 | 121,850 | 48.861秒 | 5 | 0 |
| 19 | `2ade66eaafab475083226532d1838e93` | 100.000 | 80,866 | 51.435秒 | 5 | 0 |
| 20 | `883c2f4406e845cb89819136b18cfac6` | 100.000 | 100,243 | 45.621秒 | 5 | 0 |

## 保存artifact

- profile: [`candidate81-validation-wrapper-precedence-v14-reasoning-medium-a01-global-m24-n5-r1`](../profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-a01-global-m24-n5-r1.json)
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate81-validation-wrapper-precedence-v14-reasoning-medium-a01-global-m24-n5-b20-20260729-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`

全20 batchに`execution-seal.json`、`execution-evidence.tar.zst`、`result-registration.json`、`final-compact-receipt.json`、`final-evidence.tar.zst`が存在する。archive SHA-256とmember hashは各batchのwrite-once manifestを正本とする。
