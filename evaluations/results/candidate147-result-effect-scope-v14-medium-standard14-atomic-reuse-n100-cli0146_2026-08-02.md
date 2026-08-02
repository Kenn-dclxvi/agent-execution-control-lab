# Candidate147 Standard14 atomic reuse N=100結果

## 結論

Candidate147のStandard14は、14 caseすべてN=100へ到達し、1,400 / 1,400件がscore `4`だった。score `3`以下、excluded attempt、controller error、command protocol violationは0件である。事前に定めた停止条件には一度も該当しなかった。

Standard14集約のN=100中央値は、品質`100.000`、token `1,394,412.5`、elapsed `831.914秒`だった。N=29以降のtoken中央値は`1.383M〜1.394M`、elapsed中央値は`824.903〜831.914秒`で推移した。

保存済みCandidate125 N=5の中央値と記述的に比べると、Candidate147 N=100はtoken `-0.49%`、elapsed `-1.71%`だった。Candidate145 N=5比ではtoken `-12.51%`、elapsed `-24.99%`である。ただし基準側はN=5なので、同数sampleのpaired比較や有意差の主張には使わない。

## 固定条件

- prompt: `the-caption-3ce91a4-result-effect-scope-r1`
- bundle SHA-256: `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`
- evaluation set: `the-caption-standard14-r1`
- cases / N / configured M: `14 / 100 / 24`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI / Python: `0.146.0 / 3.14.5`
- permission: `approval_policy=never / sandbox=workspace-write`
- formal Candidate145 reference result: `071438f43b304001b8b062b238b2af7c`
- formal Candidate125 reference result: `96fb571308de4c08a7aeed0faefb7d72`
- atomic pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- atomic comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`
- N=100 selection / analysis: `51283680f9ce48a7a6a20b39909129ef / f42d5652fd1f400f88cf48cc65b7e1fa`
- N=100 registered result: `e6fc6e10dedd47f5a1d59d114e6e0f57`
- N=100 registered compatibility key: `6b55a8ba3a8ee5e0124da727bbef6f201015827a40600071733490d8ecc2fd24`

## 実行方法

保存済みN=5の13 case各5件と、先行F06追試の100件を再利用した。残る13 caseだけに不足分を発行した。

1. 13 caseへ各24件、計312件を追加してN=29を採点した。
2. score `3`以下が0件であることを確認し、各24件、計312件を追加してN=53を採点した。
3. 同じ停止gateを確認し、各24件、計312件を追加してN=77を採点した。
4. 同じ停止gateを確認し、各23件、計299件を追加してN=100を採点した。

各waveの前に固定Layer 1、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動、token accountingと不足iteration集合を機械照合した。追加1,235件はすべてvalidだった。各batchは採点とrun登録の後にlossless archiveへsealし、最終compactを完了した。

## Wave別結果

| 到達N | 新規発行 | 新規runのscore | 累計token中央値 | 累計elapsed中央値 | result ID |
| ---: | ---: | --- | ---: | ---: | --- |
| 5 | 0 | 保存済み`4 × 70` | 1,447,626 | 852.543秒 | `f7baeadc5bd44399ac13cc0e0a8aff48` |
| 29 | 312 | `4 × 312` | 1,382,747 | 824.903秒 | `ccbf9a51045d4d4aa060da29e2ee5184` |
| 53 | 312 | `4 × 312` | 1,391,570 | 830.033秒 | `a5c74cb9b4814f15bff79ca34f32ebe7` |
| 77 | 312 | `4 × 312` | 1,387,195 | 831.532秒 | `8ccc742cc5e044a6911462ae5d937670` |
| 100 | 299 | `4 × 299` | 1,394,412.5 | 831.914秒 | `e6fc6e10dedd47f5a1d59d114e6e0f57` |

## 品質と診断

- 全pool: score `4` = 1,400 / 1,400、score `3`以下 = 0 / 1,400
- 今回追加分: valid / rateable = 1,235 / 1,235
- excluded attempt / controller error = 0 / 0
- command protocol violation = 0 / 1,235
- monthly review numeric location: exact 89 / 95、mismatch 6 / 95
- owner / producer evidence inadmissible: 950件

`monthly review numeric location`とowner / producer evidenceはdiagnosticであり、KPIまたはquality必須条件ではない。6件のmismatchは月次reviewの成果品質失敗を意味せず、該当runもTaskSpecのreview outcomeを満たしてscore `4`だった。

## KPIの推移と基準比較

| result | N | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Candidate125 | 5 | 100.000 | 1,401,225 | 846.377秒 |
| Candidate145 | 5 | 100.000 | 1,593,744 | 1,109.072秒 |
| Candidate147 | 5 | 100.000 | 1,447,626 | 852.543秒 |
| Candidate147 | 100 | 100.000 | 1,394,412.5 | 831.914秒 |

Candidate147内ではN=5からN=100へtoken中央値が`-3.68%`、elapsed中央値が`-2.42%`移動した。N=29、53、77、100の中央値に一方向の増加傾向はない。したがって、N=5でC125をわずかに上回ったcostはN=100では再現せず、少なくとも観測した100反復の分布中央はC125 N=5と同程度だった。

一方、Candidate125とCandidate145の保存済み基準は各N=5である。Nが異なるため、Candidate147 N=100との差は分布位置の記述に限定する。Candidate147の採用優位やCandidate125より低costであることを、この比較だけから確定しない。

## 状態判断

| gate | 結論 |
| --- | --- |
| Standard14 quality | pass。1,400 / 1,400件がscore `4` |
| Score 3以下停止条件 | 非該当。0件 |
| Standard14 N=100 stability | pass。14 caseすべて100件到達 |
| C125 cost target | N=100中央値はC125 N=5と同程度。paired同数比較ではない |
| adoption | 未判断 |
| release / projection | 未判断 / 未許可 |

状態は`standard14_n100_evaluated / quality_stability_gate_passed / score3_or_lower_zero / aggregate_cost_near_c125_n5_reference / result_registered / adoption_not_decided`である。
