# THE-CAPTION planning-first D01対象試験 第1版

## 結論

Candidate81とCandidate85へ、既存`TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1`を変更せず適用する。caseの明示worker producer binding、TaskSpec、fixture、oracle、allowed readは既存revisionをそのまま使う。

## 固定条件

- set ID: `the-caption-planning-first-d01-r1`
- revision: `r1`
- case: `TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- reasoning effort: `medium`
- repetition: C81 / C85それぞれ`N=5`
- prompt以外のcomparison conditionsはpair内で同一
- token tolerance: `0`
- elapsed tolerance: `0`

## 判定境界

5 / 5 valid・rateable、score `4`、zero driftに加え、既存TaskSpecで指定されたworker identityのterminal resultを要求する。Worker指定は既存の明示成果条件であり、owner語列から推定しない。

F04 gate通過時だけ実行する。標準14、採用、release、runtime projectionは判断しない。

## 状態

F04でCandidate85が`cost_control_failed`となったため、profileは準備artifactとして保持し、model runは実施しない。

Candidate86ではF04 gateを通過したため、同じD01 r1を変更せずC81 / C86へ適用した。[`result`](../../results/candidate81-candidate86-producer-plan-fast-path-v14-medium-d01-n5_2026-07-29.md)は両条件5 / 5 score `4`かつ指定worker route成立だったが、C86はtoken中央値`+83.28%`、elapsed中央値`+45.81%`の`cost_control_failed`となり停止した。
