# Candidate98 / Candidate104 staged evidence admission Rating v14 Medium 標準14 N=5

## 結論

Candidate104を、保存済みCandidate98 resultへ互換条件を固定した標準14項目各`N=5`で実行した。Candidate104は70 / 70件がvalid・rateable・score `4`で、excluded attemptは0件だった。targeted A02 / F07 gateとStandard14 quality gateの両方を通過した。

Candidate104 minus Candidate98の5 iteration集約中央値差は、quality `0.000`、all-agent token `-121,141`（`-6.48%`）、elapsed `-100.745`秒（`-9.77%`）だった。これは固定Standard14 N=5の記述差であり、一般的効果、採用、release、runtime projectionを意味しない。

現在状態を`targeted_a02_f07_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / result_registered / adoption_not_decided`とする。B20、release、THE-CAPTION本体反映は未実施・未判断である。

## 実行前gate

- reference result: Candidate98 `1d124a27f74a485d855e1f8f275ed0c9`
- reference content SHA-256: `e601a13ee6bcb254641c6202030d60aeba637afab2d15339ad77f7072d850a02`
- Evaluation set: `the-caption-standard14-r1/r1`
- set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- coverage: 標準14項目、各iteration `1..5`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- model / reasoning: `gpt-5.6-sol` / `medium`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- CLI / runtime: Codex CLI `0.146.0` / Python `3.14.5`
- execution: global queue / 設定上の`M=24` / `N=5`

保存済みCandidate98のLayer 1を`prepare-comparison-layer1`で検証・複製した。profile、70 capsule、global planは`preflight-comparison`で機械照合し、`comparison-preflight.json`が70 slotを承認した後にだけ発行した。

旧profile r1はトップレベル`iterations`がなく、r2は保存済みcoverageとcase順が異なったため、どちらも正規preflightを通せなかった。r3で`iterations=5`と保存済みcoverage順を固定した。両失敗preflightはslotを一件も発行していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate98 | `70 / 70` | `100.000` | `1,869,862` | `9,884,513` | `1,031.319`秒 | `5,341.068`秒 |
| Candidate104 | `70 / 70` | `100.000` | `1,748,721` | `8,852,846` | `930.574`秒 | `4,654.722`秒 |
| Candidate104 - Candidate98 | score 4 `0` | `0.000` | `-121,141`（`-6.48%`） | `-1,031,667`（`-10.44%`） | `-100.745`秒（`-9.77%`） | `-686.346`秒（`-12.85%`） |

Candidate104のcommand protocol violationは0件、Monthly reviewの数値位置は5 / 5でexactだった。owner-producer evidence inadmissible 55 / 70はRating v14のdiagnostic onlyであり、quality scoreを変更しない。

## Result identity

- Candidate104 result ID: `6321dcdbe8a54599a07c7ca139a850ea`
- Candidate104 content SHA-256: `74eea9554af185728041fa4ba2f0230f8e75358f0a70363ff8c515612dd08288`
- Candidate104 profile: [`candidate104-staged-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r3`](../profiles/candidate104-staged-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r3.json)
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146-20260730-r5`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate98-candidate104-v14-medium-standard14-n5-cli0146-20260730-r2.json`
- execution archive SHA-256: `e3285ad29e523926410636b29bb2b8e8ef0daf08298fc96aa3627f3650f62ce2`
- final archive SHA-256: `743449b77ba97482a6e696ae2e3783e73a9f3a296f29310af0ebf592f87d5816`

先行campaign r2の登録result `01c42499f4d34b9ba488a57e82e1890e`は、現行規則が必須とする`comparison-preflight.json`なしで発行されていた。履歴として削除しないが、primary result、比較根拠、再利用可能な正式結果として扱わない。

raw run evidenceはverification checkoutに保持し、このrepositoryへcommitしない。
