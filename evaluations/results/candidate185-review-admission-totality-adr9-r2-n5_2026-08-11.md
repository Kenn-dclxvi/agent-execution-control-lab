# Candidate185 ADR9 r2 N=5

> 状態: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate185はADR9 r2を45 / 45 valid、除外0件で完了した。Scoreは`4 / 1 = 38 / 7`で、Target gateを通過しなかった。Standard14、採用、release、projectionへは進めない。

Candidate184で多発したmissing入力によるreview起動前停止は閉じ、ADR03とADR04は10 / 10件で独立reviewを起動して期待する具体的反例を保持した。一方、固定済み変更への不要reviewが3件、具体的反例のsupport不足による`unavailable`が1件、判断に関係するmissingがあるまま`no_counterexample_found`を受け入れて変更した実行が3件残った。したがって、packet形成の改善を、review admission全体の成立とは扱わない。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-review-admission-totality-r1`
- bundle SHA-256: `ecf71227e16a264d3102ab711c6f1541433175bafd66081c811757a6e98b6de1`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- evaluation set identity: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- reference result: `d3e91302f0d14350906075676c5a2791`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- atomic pool: `d4f11d730620929f70a5c23235fa010e77fe53151d663b5c82a707619f5c2105`
- selection: `c579fc8b82ec42ac85fec5fad156edef`
- analysis: `37c379eef78c488a86006bcc4bafa43d`
- registered result: `2429f3c50d5c447dbcef8ba671805f91`
- result content SHA-256: `394abb9883c693b69e37694ee9570181b9f0799efd6ffd24262941dc10b53c94`

preflightはCandidate185の新規45スロットだけを許可し、設定上限`M=24`を固定した。case、TaskSpec、fixture、oracle、rating、runtime、permission、executor条件は基準resultから変更していない。

## 結果

| case | Score 4 | Score 1 | reviewer | artifact変更 | terminal |
|---|---:|---:|---:|---:|---|
| ADR01 | 3 | 2 | 2 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR02 | 4 | 1 | 1 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR03 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR04 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR05 | 4 | 1 | 5 / 5 | 0 / 5 | `blocked` 4、`unavailable` 1 |
| ADR06 | 5 | 0 | 5 / 5 | 0 / 5 | `blocked` 5 |
| ADR07 | 5 | 0 | 5 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR08 | 5 | 0 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR09 | 2 | 3 | 5 / 5 | 3 / 5 | `unavailable` 2、`completion_ready` 3 |

中央値はquality `83.33333333333334`、all-agent token `1,321,024`、elapsed `757.578812874388`秒だった。Target gate不通過のため、この値を採用比較へ使わない。

## 機序

### missingをpacketのterminal input stateとして扱う経路は成立した

ADR03とADR04の全10件は、`paired-scope-evidence.json`がmissingでもpacket未完成として止めず、情報封鎖した独立reviewへ配送した。全件で具体的反例を保持して`blocked`となり、artifact変更は0件だった。Candidate184で観測したreview起動前停止はこの範囲では閉じた。

### finite fixed effectの照合は依然として不安定だった

ADR01の2件とADR02の1件は、TaskSpecとauthorityが有限なtarget、終状態および保持条件を固定していたにもかかわらず、`matched / not_required`へ進まず独立reviewを起動した。成果物とterminalは正しかったが、review不要判定の機序を満たしていない。

### judgement resultのsupportとdependencyが安定しなかった

ADR05の1件はreviewerが`counterexample_found`を返したものの、具体的入力、設計上の処遇、authorityとの直接矛盾を十分にbindできず、rootが補完せず`unavailable`で停止した。補完禁止は守ったが、期待する具体的反例resultを形成できなかった。

ADR09の3件は、missing scope evidenceの値によって未選択instanceの具体的反例が成立し得るにもかかわらず、`no_counterexample_found`を受け入れてartifactを変更した。missingをpacketへ配送することと、そのmissingを`no_counterexample_dependency`へbindすることは別であり、後者が安定していない。

## 判定

Candidate185はreview packet形成を改善したが、fixed effect correspondenceとreviewer judgement dependencyの両方に失敗が残った。`quality_failed / mechanism_failed / stopped`とし、Standard14、採用、releaseまたはprojectionへ進めない。

次の作業を行う場合は、既存条項へcase固有分岐を加えず、有限固定効果の照合を実行可能な一つの決定手順へ落とすことと、reviewerがmissingの値で反例成立可否が変わる場合に`unavailable_dependency`を必ず返す形成条件を設計し直す必要がある。

## 一次証拠

- [登録result](2429f3c50d5c447dbcef8ba671805f91.json)
- [機序監査](candidate185-review-admission-totality-adr9-r2-n5-audit-r1.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate185-review-admission-totality-adr9-r2-n5-20260811-r1`
