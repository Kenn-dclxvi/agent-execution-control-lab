# ControlFreeRepository Rating v14 Medium Standard14 atomic reuse N=100

## 結論

Candidate147と実効互換な条件で実施したControlFreeRepositoryのStandard14追試を、14 caseそれぞれ`N=100`、合計1,400 runまで完了した。全caseの登録数は100件であり、N=80から不足していた各20件、計280件だけを新規実行した。

追加280件は280 / 280件がvalidかつrateableで、excluded attemptとrunner errorは0件だった。Rating v14の分布はscore `4 / 0 = 260 / 20`である。既存runと合わせたN=100の分布は`4 / 0 = 1,300 / 100`となった。score `0`はすべてA01 latent mode policyで、未固定値の確認前に変更または試験へ進んだ既知のFree経路である。

N=100のStandard14集約中央値は、quality `92.857`、all-agent token `3,457,525`、elapsed `1,180.997秒`だった。N=5比ではqualityは不変、tokenは`-31,086`（`-0.89%`）、elapsedは`+14.701秒`（`+1.26%`）である。これは同じrun poolを拡張したときの記述的な差であり、prompt効果や一般的な性能差を示す因果値として扱わない。

## 試験状態

- ControlFreeRepository: `standard14_n100_evaluated / low_score_observed / registered`
- 実行: `additional_280_of_280_valid / excluded_0 / runner_error_0`
- 比較: `candidate147_compatibility_matched / within_free_n_descriptive_only`
- Candidate147の採用、release、projection状態: 変更なし

ユーザーは本追試をエビデンス取得として明示し、scoreにかかわらずN=100まで継続するよう指定した。このため、各waveのscoreは記録したが、追試停止条件には使用していない。

## 実行前gateとatomic再利用

既存のN=80 poolを再実行せず、`plan-missing --desired-count 100`で各caseの不足20件だけをwrite-once planへ固定した。新規280 slotの発行前に`prepare-comparison-layer1`、`prepare_atomic_plan`、`preflight-comparison`を実行し、次の条件を機械照合した。

| 条件 | 固定値 | 照合結果 |
| --- | --- | --- |
| Evaluation set | `the-caption-standard14-r1` / identity `2096d15e...63c33` | 一致 |
| coverage | 14 case × 各100件。新規分は各20件 | 一致 |
| prompt | `the-caption-3ce91a4-control-free-repository-r1` | 一致 |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` | 一致 |
| model / reasoning | `gpt-5.6-sol` / `medium` | 一致 |
| Agent / runtime / CLI | Codex、persisted、memory off、multi-agent on、Python `3.14.5`、CLI `0.146.0`、runtime `61b26e61...9a73` | 一致 |
| permission | `workspace-write / never` | 一致 |
| executor / token | global queue、設定上の`M=24`、all-agent token accounting v1 | 一致 |
| atomic comparison key | `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1` | 一致 |
| comparison preflight key | `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561` | `ready` |

ControlFreeRepositoryのatomic pool keyは`91a82726350e2ce3b40e3785a4dc8daa5f4a5a9792878d4f8eccd7e1b8665c92`である。N、iteration集合、dispatch順、実際の同時実行数はrun identityではなくexecution provenanceとして保持した。

## N=5からN=100までの比較

各行は、そのNでcase別件数を固定したselection receiptとLayer 4 analysisの集約中央値である。

| N | 登録run | score分布 | quality中央値 | all-agent token中央値 | elapsed中央値 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 70 | `4 / 0 = 65 / 5` | 92.857 | 3,488,611 | 1,166.296秒 |
| 20 | 280 | `4 / 0 = 260 / 20` | 92.857 | 3,488,514.5 | 1,195.583秒 |
| 40 | 560 | `4 / 0 = 520 / 40` | 92.857 | 3,457,525 | 1,164.954秒 |
| 60 | 840 | `4 / 0 = 780 / 60` | 92.857 | 3,449,348.5 | 1,170.890秒 |
| 80 | 1,120 | `4 / 0 = 1,040 / 80` | 92.857 | 3,462,062 | 1,180.997秒 |
| 100 | 1,400 | `4 / 0 = 1,300 / 100` | 92.857 | 3,457,525 | 1,180.997秒 |

quality中央値は全Nで同じだった。tokenとelapsedの中央値はN拡張に伴って一方向には動かず、N=5からN=100の範囲ではtokenが`3,449,348.5〜3,488,611`、elapsedが`1,164.954〜1,195.583秒`に分布した。したがって、N=5の単一点だけをFreeの固定costとして扱わない。

## 診断境界

追加280件のowner-producer collectorは`failed: 220 / not_applicable: 60`だった。これはowner-producer証拠を標準schemaで取得できたかを示すdiagnosticであり、3 KPIまたはRating v14のscoreではない。本追試の停止、採用、release、projection判断には用いない。

## 保存証拠

- N=5一次結果: [`Baseline / ControlFreeRepository / Candidate147 N=5`](baseline-control-free-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md)
- N=5 analysis: `5fba2d90027244b584ec99d27e63ef10`
- N=20 analysis: `b6246fe227fc48e1b415e401cf307918`
- N=40 analysis: `5ba1c04abdbf4f6d8fb80aebbf6a7c93`
- N=60 analysis: `7074f883d0f14f308084a397f871e236`
- N=80 analysis: `b035253fac2b421dbf2ce0af9be72dc3`
- N=100 selection: `d0557b8cb1f14261a752c8538478d6cb`
- N=100 selection content SHA-256: `32b90e08b8831f2e9863ef086a498e661cad459b562bde01617bb38aa35cd172`
- N=100 analysis: `78b4bffd89c546fc8bb93e51cb51fa84`
- N=100 analysis content SHA-256: `1a7d5dfad3d83b97143fa7637e84fb28e1e726c10952d5cf5f6dc34934de735c`
- N=80からN=100への追加execution archive SHA-256: `c10177af60238401cca36794b404f9ab958739d93cb80152fbd15c04a7f7fda0`

raw evidence、selection、analysis、sealは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/`配下へ保存した。registryの既存run、一次rating、N=5結果文書は変更していない。
