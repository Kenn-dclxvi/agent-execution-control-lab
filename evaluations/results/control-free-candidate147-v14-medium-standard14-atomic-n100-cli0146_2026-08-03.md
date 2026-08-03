# ControlFreeRepository / Candidate147 Rating v14 Medium Standard14 N=100比較

## 結論

ControlFreeRepository（以下Free）とCandidate147（以下C147）の、実効互換なStandard14各N=100を比較した。両条件はprompt identity以外のEvaluation set、fixture、TaskSpec、rating、model、reasoning、Agent / runtime / CLI、permission、executor挙動、token accountingが一致する。

Freeは1,400件中1,300件がscore `4`、100件がscore `0`だった。score `0`はすべてA01 latent mode policyで発生した。C147は1,400 / 1,400件がscore `4`だった。

Standard14集約中央値の`C147 - Free`は、quality `+7.143`、all-agent token `-2,063,112.5`（`-59.67%`）、elapsed `-349.083秒`（`-29.56%`）だった。case別中央値でも、C147は14 / 14 caseでtokenとelapsedがFreeを下回った。

ただし、FreeとC147はquality分布が異なる。このためcost差を同一品質における効率差とは扱わない。結果は、固定したStandard14、GPT-5.6 Sol Medium、CLI `0.146.0`の範囲に限定する。

## 比較条件

| 条件 | 固定値 | 照合結果 |
| --- | --- | --- |
| Evaluation set | `the-caption-standard14-r1` / identity `2096d15e...63c33` | 一致 |
| coverage | 14 case × 各100件 | 一致 |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` | 一致 |
| model / reasoning | `gpt-5.6-sol` / `medium` | 一致 |
| Agent / runtime / CLI | Codex、persisted、memory off、multi-agent on、Python `3.14.5`、CLI `0.146.0`、runtime `61b26e61...9a73` | 一致 |
| permission | `workspace-write / never` | 一致 |
| executor / token | global queue、設定上の`M=24`、all-agent token accounting v1 | 一致 |
| atomic comparison key | `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1` | 一致 |
| prompt | Free `the-caption-3ce91a4-control-free-repository-r1` / C147 `the-caption-3ce91a4-result-effect-scope-r1` | 宣言変更軸 |

N、iteration集合、dispatch順、実際の同時実行数はexecution provenanceであり、atomic runのmember identityへ含めない。

## 一次結果

| 条件 | pool | N=100 selection | N=100 analysis |
| --- | --- | --- | --- |
| Free | `91a82726350e2ce3b40e3785a4dc8daa5f4a5a9792878d4f8eccd7e1b8665c92` | `d0557b8cb1f14261a752c8538478d6cb` | `78b4bffd89c546fc8bb93e51cb51fa84` |
| C147 | `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5` | `51283680f9ce48a7a6a20b39909129ef` | `f42d5652fd1f400f88cf48cc65b7e1fa` |

この比較では登録済みrunを再利用した。新しい評価slotは発行していない。一次rating、selection、analysisは変更していない。

## 3 KPI

| 条件 | score分布 | quality中央値 | all-agent token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Free | `4 / 0 = 1,300 / 100` | 92.857 | 3,457,525 | 1,180.997秒 |
| C147 | `4 = 1,400` | 100.000 | 1,394,412.5 | 831.914秒 |

差分はC147からFreeを引いた値である。

| 差分 | quality | all-agent token | elapsed |
| --- | ---: | ---: | ---: |
| `C147 - Free` | +7.143 | -2,063,112.5（-59.67%） | -349.083秒（-29.56%） |

C147のtoken中央値はFreeの`40.33%`だった。C147のelapsed中央値はFreeの`70.44%`だった。

## case別結果

score分布は各caseの100件を示す。KPI欄は`token中央値 / elapsed中央値`である。差分率はC147をFreeと比較した値である。

| case | Free score | C147 score | Free KPI | C147 KPI | token差 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | `0×100` | `4×100` | 339,775 / 113.487秒 | 36,203.5 / 18.499秒 | -89.34% | -83.70% |
| A02 repository-resolvable routing | `4×100` | `4×100` | 291,520.5 / 93.114秒 | 129,387.5 / 76.422秒 | -55.62% | -17.93% |
| F01 duplicate asset key | `4×100` | `4×100` | 213,974.5 / 71.198秒 | 110,938.5 / 64.017秒 | -48.15% | -10.09% |
| F02 history date bound | `4×100` | `4×100` | 306,097.5 / 90.767秒 | 127,941.5 / 78.820秒 | -58.20% | -13.16% |
| F03 atomic cleanup | `4×100` | `4×100` | 182,815.5 / 77.196秒 | 100,252 / 70.780秒 | -45.16% | -8.31% |
| F04 audit column visibility | `4×100` | `4×100` | 233,536 / 88.147秒 | 160,125.5 / 84.840秒 | -31.43% | -3.75% |
| F05 clarify units mode | `4×100` | `4×100` | 79,598 / 29.799秒 | 37,463.5 / 22.479秒 | -52.93% | -24.57% |
| F05 out-of-scope deploy | `4×100` | `4×100` | 79,872 / 31.816秒 | 37,393 / 22.937秒 | -53.18% | -27.91% |
| F06 empty snapshot contract | `4×100` | `4×100` | 274,425 / 87.902秒 | 105,044.5 / 77.552秒 | -61.72% | -11.77% |
| F07 canonical v4 runner | `4×100` | `4×100` | 327,281 / 96.767秒 | 101,854 / 62.749秒 | -68.88% | -35.15% |
| F07 dependency provenance | `4×100` | `4×100` | 152,153 / 69.886秒 | 81,785 / 57.813秒 | -46.25% | -17.27% |
| F08 CLI reference sync | `4×100` | `4×100` | 431,885 / 131.681秒 | 101,086.5 / 59.869秒 | -76.59% | -54.53% |
| F10 entrypoint inventory | `4×100` | `4×100` | 251,747 / 103.014秒 | 101,655.5 / 69.745秒 | -59.62% | -32.29% |
| F10 monthly format review | `4×100` | `4×100` | 219,613.5 / 88.091秒 | 93,601.5 / 55.994秒 | -57.38% | -36.44% |

FreeとC147がともに100 / 100件score `4`だった13 caseでも、C147のtokenとelapsed中央値はすべてFreeを下回った。したがって、Standard14全体のcost差はA01の早期停止だけでは説明できない。

## 品質経路

FreeのA01は100 / 100件で、利用者が決める未固定値の確認前に変更または試験へ進んだ。これはN=5で確認済みだったFreeの既知経路が、N=100でも同じ比率で再現した結果である。

C147のA01は100 / 100件がscore `4`だった。C147は未固定のrequired outcomeを開始gateで閉じる。開始identity結果が影響しない許可済みreadは、結果を待たず同じmodel stepから発行できる。artifact変更とrequired validationは、結果を受領するまで閉じる。

この比較から直接確定できるのは、A01のscore経路、3 KPI、case別中央値である。N=100の登録schemaは全runのmodel step、tool call、追加readをKPIとして集計しない。そのため、他13 caseのcost差を単一の内部経路へ因果分解しない。

## 記述的特徴

事実として、C147のtoken差はA01、F08、F07 canonicalで特に大きかった。elapsed差もA01とF08で大きかった。

F04はtokenが`-31.43%`である一方、elapsedは`-3.75%`だった。F04は`npm ci`、lint、buildをrequired validationとして実行する。したがって、固定command時間がelapsed差を小さくした可能性がある。これはKPIとTaskSpecから得た解釈であり、command時間の個別因果分解ではない。

C147のF06には、別のN=100診断でauthority追加readが21 / 100件残った。それでも本比較のF06中央値はFree比でtoken `-61.72%`、elapsed `-11.77%`だった。C147の局所的な高cost経路は、Freeとのcase中央値差を反転させなかった。

Freeはroot `AGENTS.md`を0 byteにした条件である。TaskSpecとpath-scoped repository authorityは残る。したがって、この比較は全model-visible指示を削除した条件との比較ではない。

## 解釈境界

- 両条件はprompt identity以外の実効互換条件が一致する。
- quality分布が異なるため、同一品質を前提としたcost比較ではない。
- 13 caseは両条件とも100 / 100件score `4`であり、その範囲でもC147のcase別tokenとelapsed中央値はすべて小さい。
- N=100は観測したStandard14における分布を示す。別model、別runtime、別Evaluation setへ一般化しない。
- 本比較は評価結果を記録する。adoption、release、projection、本体反映の状態を変更しない。

状態は`n100_compatible_comparison_documented / free_a01_score0_100_of_100 / c147_score4_1400_of_1400 / three_kpi_and_case_medians_recorded / primary_results_unchanged / adoption_release_projection_unchanged`である。

## 参照

- [ControlFreeRepository N=100](control-free-repository-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-03.md)
- [Candidate147 N=100](candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [Baseline / ControlFreeRepository / Candidate147 N=5](baseline-control-free-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md)
- [Candidate147 F06 N=100](candidate147-result-effect-scope-v14-medium-f06-atomic-reuse-n100-cli0146_2026-08-02.md)
