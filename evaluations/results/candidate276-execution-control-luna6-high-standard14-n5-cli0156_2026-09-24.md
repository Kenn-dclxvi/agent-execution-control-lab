# Candidate276 Standard14 GPT-6 Luna High N=5（2026-09-24）

## 結果

利用者指定の4項目をroot `AGENTS.md`へ適用したCandidate276を、C275のStandard14 resultと同じ条件で比較した。14ケース各5回、計70 runを実施し、70件がvalid・rateable、除外0件、Score 4は70 / 70件だった。品質監査でcommand protocol違反は0件。owner-producer evidenceの欠落・不一致55件はRating v14の定義どおり診断情報として扱い、品質scoreを下げる条件にはしていない。

C275とC276のN=5 median比較では、qualityは双方100、all-agent total tokensはC276が77,345（3.16%）多く、経過時間は12.849秒（1.37%）短かった。これは固定Standard14における比較結果であり、改善の一般化、誤経路の機序閉鎖、採用可否を示すものではない。

| 指標 | C275 | C276 | C276 - C275 |
| --- | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 0 |
| Score 4（登録値） | 69 / 70 | 70 / 70 | +1 |
| Score 4（C275訂正反映） | 70 / 70 | 70 / 70 | 0 |
| quality中央値（0–100） | 100.000 | 100.000 | +0.000 |
| all-agent token中央値 | 2,448,245 | 2,525,590 | +77,345（+3.16%） |
| elapsed中央値 | 937.950秒 | 925.101秒 | -12.849秒（-1.37%） |

C275の登録resultではScore 4が69 / 70件だが、F02 1件の採点訂正後の分布は70 / 70件Score 4である。C276との品質中央値比較はN=5のsample中央値に基づき、双方100となった。C275の訂正履歴を含む背景は[Candidate275 result](four-verified-lines-ablation-luna6-high-standard14-n5-cli0156_2026-09-24.md)を参照。

### Control-Freeとの比較

追加比較の依頼を受け、同じcomparison keyを持つ保存済みControl-Free GPT-6 Luna High result `71a8231c6cc048d0a522aaa43d3a91b6`も比較した。再実行はせず、同じ14ケース×5回の70件から5 sampleを選び、C276とexecution stratumが一致することを確認した。

| 指標 | Control-Free | C276 | C276 - Control-Free |
| --- | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 0 |
| quality中央値（0–100） | 92.857 | 100.000 | +7.143 |
| all-agent token中央値 | 3,141,404 | 2,525,590 | -615,814（-19.60%） |
| elapsed中央値 | 1,043.654秒 | 925.101秒 | -118.553秒（-11.36%） |

これは保存済みControl-Free結果との同条件比較であり、C276の一般的な品質・費用改善や特定機序の因果効果を示すものではない。以下は各ケース5回の中央値で、品質は0–4点、Score 4は5回中の件数、差分率はControl-Free比である。

| ケース | Score 4（Free→C276） | 品質中央値（Free→C276） | Token中央値（Free→C276） | Elapsed中央値（Free→C276） |
| --- | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 0/5→5/5 | 0→4 | 443,240→74,507 (-83.2%) | 98.191→24.701秒 (-74.8%) |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 5/5→5/5 | 4→4 | 311,131→222,238 (-28.6%) | 76.200→75.066秒 (-1.5%) |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 5/5→5/5 | 4→4 | 228,850→243,699 (+6.5%) | 65.988→67.231秒 (+1.9%) |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 5/5→5/5 | 4→4 | 429,669→380,581 (-11.4%) | 97.908→92.859秒 (-5.2%) |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 5/5→5/5 | 4→4 | 207,635→197,400 (-4.9%) | 71.104→90.054秒 (+26.7%) |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 5/5→5/5 | 4→4 | 307,990→234,225 (-24.0%) | 78.982→74.896秒 (-5.2%) |
| `TC-F05-CLARIFY-UNITS-MODE` | 5/5→5/5 | 4→4 | 33,043→32,504 (-1.6%) | 30.996→25.791秒 (-16.8%) |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 5/5→5/5 | 4→4 | 77,502→51,364 (-33.7%) | 32.503→31.689秒 (-2.5%) |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 5/5→5/5 | 4→4 | 247,341→229,022 (-7.4%) | 73.380→63.757秒 (-13.1%) |
| `TC-F07-CANONICAL-V4-RUNNER` | 5/5→5/5 | 4→4 | 233,194→240,762 (+3.2%) | 82.469→97.076秒 (+17.7%) |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 5/5→5/5 | 4→4 | 173,869→155,791 (-10.4%) | 66.618→61.909秒 (-7.1%) |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 5/5→5/5 | 4→4 | 160,487→198,643 (+23.8%) | 54.247→70.863秒 (+30.6%) |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 5/5→5/5 | 4→4 | 216,802→214,023 (-1.3%) | 90.169→73.847秒 (-18.1%) |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 5/5→5/5 | 4→4 | 79,447→80,633 (+1.5%) | 52.300→77.041秒 (+47.3%) |

負の差分率はC276の値が小さいことを示す。ケース別にはA01の品質が0→4、F03の経過時間が+26.7%、F07 canonical CLI reference syncがtoken +23.8%・経過時間+30.6%、F10 monthly format test reviewが経過時間+47.3%となった。全体中央値だけでは見えないケース差があるため、これらは個別の固定試験結果として扱う。全数値と差分は[ケース別機械可読内訳](candidate276-control-free-case-breakdown-luna6-high-standard14-n5_2026-09-24.json)を参照。


## 固定条件と登録情報

- prompt identity: `the-caption-3ce91a4-execution-control-r1` r1、bundle SHA-256 `4d2dcd4f34749b32155139138654cbc2bb33b78fc6841ba6eb14d29c8f7a678f`
- 比較基準: Candidate275 `the-caption-3ce91a4-four-verified-lines-ablation-r1` r1
- model / reasoning: `gpt-6-luna / high`
- Codex CLI / Python: `0.156.1 / 3.14.5`
- evaluation set: `the-caption-standard14-r1` r1、14 cases × N=5
- permission: `workspace-write / never`、configured M=24
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- compatibility key: `d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`
- C275 result: `975c33cb36404c2381ce0715fc7a2592`
- C276 result: `9c659e7e0e0847beb97051fd23d92d94`
- C276 result content SHA-256: `0afa43893a033f7f03e769dd928df7dd5d721ccb009c8ed71dfbe694620d20de`
- preflight: `ready`、70 slots authorized、M=24
- execution: 70 / 70 valid、excluded 0、runner elapsed 244.311秒
- run evidence: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/c276-c275-std14n5-l6h-mufhlihg-h1acny`
- final evidence archive SHA-256: `925908eba49fe1c8f52711a36a9182062e0bd36a5bc0c28b39738306c30ebea9`

一次登録resultは[機械可読result](candidate276-execution-control-luna6-high-standard14-n5-cli0156_2026-09-24.json)、70件の採点内訳は[quality audit](candidate276-execution-control-luna6-high-standard14-n5-quality-audit-r1.json)、C275との差分は[C275比較view](candidate276-candidate275-comparison-luna6-high-standard14-n5_2026-09-24.json)、Control-Freeとの差分は[Control-Free比較view](candidate276-control-free-comparison-luna6-high-standard14-n5_2026-09-24.json)を参照。
