# Candidate147 F06 atomic reuse N=100結果

## 結論

Candidate147のF06は、既存N=5から`+24 → +24 → +24 → +23`の順に拡張し、N=100まで100 / 100件がscore `4`だった。各waveの採点後にscore `3`以下の有無を確認し、停止条件に該当するrunはなかった。

初期N=5のtoken中央値`151,542`はN=29で`105,030`へ下がり、N=53とN=77も`105,030`、N=100は`105,044.5`だった。したがって、初期N=5で観測したF06 token増加をCandidate147の代表中央値とは扱わない。

一方、authority追加readは21 / 100件に残った。その群のtoken中央値は`160,327`で、非発生79件の`104,230`より`53.82%`高い。高token上位10件中7件にもauthority追加readがあった。これは局所的な高token経路との関連を支持するが、上位3件には同readがないため単独原因とは確定しない。

## 固定条件

- prompt: `the-caption-3ce91a4-result-effect-scope-r1`
- bundle SHA-256: `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`
- case: `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` r2
- evaluation set: `the-caption-standard14-r1` r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- permission: `approval_policy=never` / `sandbox=workspace-write`
- configured parallel limit: `M=24`
- atomic pool: `94b7aaa7c60fe0a8f61cccd3f539baa3cd1fbe993368745bbe1063bff8d0c53a`
- N=100 selection: `2d1c980ce00048b9b13079b07435780d`
- N=100 analysis: `5afbaff263e64ff0aae5b0139b5142cd`
- N=100 registered result: `6c6ad33dec2343f2b06db5a1cea6dc15`
- N=100 compatibility key: `4277a5d5bfb9ea3bdd5a690ef40736c9fb7ca9a52901aa6c55fe1693d09e9377`

## 実行方法

Candidate147 Standard14 N=5で保存済みのF06 5件をatomic runとして再利用した。不足分だけを次の順で発行した。

1. N=5から24件を追加し、N=29を採点した。
2. score `3`以下が0件であることを確認し、24件を追加してN=53を採点した。
3. score `3`以下が0件であることを確認し、24件を追加してN=77を採点した。
4. score `3`以下が0件であることを確認し、23件を追加してN=100を採点した。

各waveは比較前gateで既存件数と不足件数を機械照合した。追加95件はすべてvalidで、excluded attempt、runner error、unexpected changed path、command protocol violationは0件だった。各batchは採点・result登録後にlossless archiveへsealし、最終compactを完了した。

## Wave別結果

| 到達N | 新規発行 | 新規runのscore | 累計token中央値 | 累計elapsed中央値（秒） | result ID |
| ---: | ---: | --- | ---: | ---: | --- |
| 5 | 0 | `4 × 5` | 151,542 | 79.393 | `4dda323dde8142a3926ce5aac9547615` |
| 29 | 24 | `4 × 24` | 105,030 | 76.489 | `a2181c85c7e04dac8d6c78f0555bda64` |
| 53 | 24 | `4 × 24` | 105,030 | 77.838 | `f69d40402b7946eaa0e98699c73e489d` |
| 77 | 24 | `4 × 24` | 105,030 | 77.838 | `385ff661b7b14607b0cc6f009cf1362d` |
| 100 | 23 | `4 × 23` | 105,044.5 | 77.552 | `6c6ad33dec2343f2b06db5a1cea6dc15` |

## N=100分布

| KPI | min | p25 | median | p75 | p90 | max | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| total tokens | 86,978 | 100,475.25 | 105,044.5 | 143,414.5 | 170,789.1 | 248,224 | 125,666.63 |
| elapsed seconds | 55.627 | 68.799 | 77.552 | 82.674 | 90.643 | 110.661 | 76.588 |

100件はすべてscore `4`である。owner / producer evidenceは診断専用であり、追加95件はいずれもscore 4判定への適格証拠にはならなかったが、quality ratingの必須条件ではない。

## 既存結果との記述的比較

同じF06の保存済みN=5中央値と比較すると、Candidate147 N=100はCandidate145比でtoken `-11.21%`、elapsed `-7.46%`だった。Candidate125比ではtoken `+5.90%`、elapsed `+15.39%`だった。

比較条件はatomic runの実効互換条件を満たす。ただし比較対象はCandidate147 N=100に対してCandidate145 / Candidate125 N=5であり、同数sampleのpaired比較ではない。したがって、ここでは分布位置の記述に限定し、有意差や採用優位を主張しない。

## 挙動分析

authority追加readは21 / 100件だった。Candidate145の保存済みF06 N=5では0 / 5件だったが、基準側が5件しかないため、発生確率の増加量は確定できない。

Candidate147内では次の差があった。

| 群 | 件数 | token中央値 | elapsed中央値（秒） |
| --- | ---: | ---: | ---: |
| authority追加readあり | 21 | 160,327 | 81.143 |
| authority追加readなし | 79 | 104,230 | 72.944 |

追加readあり群は、なし群よりtoken中央値が`53.82%`、elapsed中央値が`11.24%`高かった。ただし高token上位10件のうち3件はauthority追加readなしである。よって、authority探索は高token裾の有力な一経路だが、残差全体を単独では説明しない。

N=100で、focused test、full test、`git diff --check`、`git diff --name-only`を同一run内で複数回発行した例は0件だった。初期N=5で「完了確認重複」と解釈した1件は、N=100のcommand回数基準では再現しなかった。

## 状態判断

| gate | 結論 |
| --- | --- |
| quality | pass。100 / 100件がscore `4` |
| Score 3以下停止条件 | 非該当。0 / 100件 |
| F06中央値の安定性 | N=29以降、token中央値は約105kで安定 |
| authority追加read | 21 / 100件で残存。高token裾との関連あり |
| Standard14全体への一般化 | 不可。この追試はF06だけ |
| adoption | 未判断 |
| release / projection | 未判断 / 未許可 |
