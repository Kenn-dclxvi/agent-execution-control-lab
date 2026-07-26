# Candidate71 / Candidate78 project index navigation 第13版標準14項目 N=5

## 結論

Candidate78は70 / 70件がvalid・rateableかつscore `4`で、Candidate71と同じ品質中央値`100.000`を維持した。一方、Candidate71比でall-agent `total_tokens`中央値は`+184,448`（`+8.66%`）、`elapsed_seconds`中央値は`+48.817`秒（`+4.38%`）だった。

狙ったA02ではproject indexの先行参照を5 / 5で観測したが、repository-wide探索も5 / 5で残った。TaskSpecで対象が閉じたF10 Entryでは不要なindex参照を2 / 5で観測した。事前停止条件に従い、Candidate78は`standard14_evaluated / stopped`とする。採用、release、THE-CAPTION本体への反映、runtime有効化は行わない。

## 評価identity

| 項目 | Candidate71 | Candidate78 |
| --- | --- | --- |
| prompt identity | `the-caption-3ce91a4-validation-closure-r1` | `the-caption-3ce91a4-project-index-navigation-r1` |
| bundle SHA-256 | `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695` | `23d42dfad1bca0305f23fb77d2b1b58e0056eb676ce55283246927775146a581` |
| result ID | `1b3d8048c391460eae8234e083494763` | `79be353bf88940bda9344d2f341511b9` |

両resultのcompatibility keyは`7426ecd03421590549c30a4e16373722153ceefc00280bc305eedb1aa0955633`で一致する。標準14項目、各`N=5`、`M=24`、rating v13、model、target ref、Agent環境、permission、executor parameter、token accountingは同一で、差はprompt identityだけである。excluded attemptは両resultとも0件だった。

## 公式Layer 4比較

| KPI中央値 | Candidate71 | Candidate78 | Candidate78 - Candidate71 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| all-agent `total_tokens` | 2,131,059 | 2,315,507 | +184,448（+8.66%） |
| `elapsed_seconds` | 1,114.525 | 1,163.343 | +48.817（+4.38%） |

各iterationの集計値は次のとおりである。これは標準14項目をiteration内で集約した公式Layer 4値である。

| iteration | Candidate71 tokens | Candidate78 tokens | Candidate71 seconds | Candidate78 seconds |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1,928,147 | 2,315,507 | 1,028.754 | 1,193.716 |
| 2 | 2,131,059 | 2,186,831 | 1,114.525 | 1,163.343 |
| 3 | 2,537,273 | 2,426,347 | 1,205.900 | 1,167.093 |
| 4 | 2,203,516 | 2,390,773 | 1,147.891 | 1,158.183 |
| 5 | 2,063,685 | 2,259,304 | 1,028.308 | 1,144.776 |

## 経路diagnostic

経路観測はKPIではなく、追加predicateがどの経路を変えたかを確認する補助情報である。

| case | Candidate71 | Candidate78 | 判定 |
| --- | --- | --- | --- |
| A02 trigger | index本文の直接read 0 / 5、repository-wide探索 5 / 5 | index先行read 5 / 5、repository-wide探索 5 / 5 | triggerは作動したが、狙った広域探索を減らさなかった |
| F10 Entry non-trigger | index read 0 / 5 | index read 2 / 5 | TaskSpecで対象が閉じたcaseに不要な参照が増えた |

A02のcase別token中央値は`233,171 → 197,882`、elapsed中央値は`101.885 → 89.438`秒だった。ただし、標準14項目全体ではtokenとelapsedの両中央値が増加したため、A02単独の方向をcandidate全体の効果へ一般化しない。

## 保存artifact

- Candidate78 profile: [`candidate78-project-index-navigation-v13-standard14-global-m24-n5-r1`](../profiles/candidate78-project-index-navigation-v13-standard14-global-m24-n5-r1.json)
- Candidate78設計: [`candidate78-project-index-navigation-design.md`](../../docs/candidate78-project-index-navigation-design.md)
- registry result content SHA-256: `32857de1f03a036d6557cb15521662116437496a0004439da5bbfc609f1d8fc7`
- comparison view: `candidate71-candidate78-project-index-navigation-v13-standard14-n5-20260726-r1.json`
- compact evidence SHA-256: `df87b0dbbff707f23768b97f770f0f20b9b83e03749d669f52db999c089fba48`

runtime registry、comparison view、compact execution evidenceはverification environmentへappend-onlyで保存した。raw run logはrepositoryへcommitしない。
