# Candidate81 / Candidate95 Rating v14 Medium A02 N=5 B20比較

## 結論

Candidate81とCandidate95を、同じA02 r2、Rating v14、Medium、Codex CLI `0.146.0`で各20 batch、各100件新規実行した。両者とも100 / 100件がvalid・rateable・score `4`で、excluded attemptは0件だった。

Candidate95の20 batch中央値はCandidate81比で、all-agent tokenが`-3,917.5`（`-1.72%`）、elapsedが`-5.367秒`（`-6.50%`）だった。対応batchの二側正確Wilcoxon符号付順位検定を行い、2 KPIをHolm補正した。token差は有意ではなかった（補正後`p=0.474905`）。elapsed差は有意だった（補正後`p=0.008442`）。

このA02限定比較ではCandidate95の品質低下を観測しなかった。一方、この結果は標準14全体へ一般化しない。elapsedに有意差が出たため、ユーザー指定の次gateとしてCandidate81 / Candidate95の標準14 B20へ進んだ。

## 固定条件

| 条件 | 値 |
| --- | --- |
| C81 prompt | `the-caption-3ce91a4-validation-wrapper-precedence-r1`、bundle SHA-256 `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` |
| C95 prompt | `the-caption-3ce91a4-required-judgment-owner-boundary-r1`、bundle SHA-256 `8c845f18bd6ed86d6f2f19281ba1257f0f1a213fa1c3466c76ede402451ee190` |
| C81 profile | `candidate81-validation-wrapper-precedence-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1` |
| C95 profile | `candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1` |
| case | `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2 |
| repetition | 各prompt A02 × `N=5` × 20 batch、各100件 |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| execution | global queue、`M=5` |
| Codex CLI | `0.146.0` |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| fixture digest | `bece63e466ad63f5ad0c40f23d2ac98b6a26f2033c1e6d883838e1ed6ab3ca87` |
| comparison | 対応するbatch 1〜20の中央値をpairとする |

両profileの差はprofile IDとprompt identityだけである。TaskSpec、case、fixture、rating、model、reasoning、CLI、permission、M / Nは同一である。

## 集計

| 指標 | Candidate81 | Candidate95 | C95 − C81 | 対応batch | raw p | Holm p |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| score `4` | 100 / 100 | 100 / 100 | 0 | 同点20 | — | — |
| token中央値の中央値 | 227,317.5 | 223,400.0 | -3,917.5（-1.72%） | C95低10 / 高10 | 0.474905 | 0.474905 |
| elapsed中央値の中央値 | 82.575秒 | 77.208秒 | -5.367秒（-6.50%） | C95短16 / 長4 | 0.004221 | 0.008442 |
| token合計 | 23,238,414 | 22,755,305 | -483,109（-2.08%） | — | — | — |
| run elapsed合計 | 8,148.133秒 | 7,764.785秒 | -383.348秒（-4.71%） | — | — | — |
| excluded attempt | 0 | 0 | 0 | — | — | — |

検定は事前に固定した二側正確Wilcoxon符号付順位検定である。二つのKPIを一つのfamilyとしてHolm補正し、`alpha=0.05`とした。中央値差は各promptの「20 batch中央値の中央値」であり、対応差中央値はtoken `-2,118.5`、elapsed `-3.442秒`だった。

## 保存場所

- C81 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate81-validation-wrapper-precedence-v14-medium-a02-continuous-n5-b20-cli0146-20260730-r1`
- C95 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate95-required-judgment-owner-boundary-v14-medium-a02-continuous-n5-b20-cli0146-20260730-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`

各campaignの`campaign-summary.json`が20 result IDを固定する。非公開raw evidenceはverification checkoutに保持し、このrepositoryへcommitしない。
