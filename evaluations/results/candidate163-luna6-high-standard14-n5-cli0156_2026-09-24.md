# C163 GPT-6 Luna High Standard14 N=5（2026-09-24）

## 結果

C163をGPT-6 Luna、reasoning `high`でStandard14の14ケース各5回、計70 run計測した。70件すべて実行・採点可能で、除外attemptは0件だった。品質は69件がScore `4`、1件がScore `3`となり、事前に固定した70 / 70件Score `4`の品質gateは通過しなかった。

同じ実行条件のControl-Free保存resultと比較した。品質とコストの指標はiterationごとの選択値5件の中央値である。

| 指標 | Control-Free | C163 | C163 - Control-Free |
| --- | ---: | ---: | ---: |
| quality score | 92.857 | 100.000 | +7.143 |
| Score `4` | 65 / 70 | 69 / 70 | +4件 |
| all-agent total tokens | 3,141,404 | 2,439,785 | -701,619（-22.33%） |
| elapsed seconds | 1,043.654 | 1,054.798 | +11.144（+1.07%） |

C163のScore `3`はF02 iteration 3で、必須pytestの成功証拠がなく、後続の`main_verify.sh`も未実行だったrunである。減少したtokenと増加したelapsedは記録するが、品質gate未通過のためコスト改善の判定には使わない。結果はN=5の記述値であり、統計的優位は主張しない。

## 固定条件とresult

- prompt identity: `the-caption-3ce91a4-five-verified-lines-integrated-r1` r1、bundle SHA-256 `4813ccf9fb3813b5b4f48b58a53dc4c8833b9971140a65aadd3b3c76d6bea62b`
- model / reasoning: `gpt-6-luna / high`
- Codex CLI: `0.156.1`
- Evaluation set: `the-caption-standard14-r1` r1、14 case × 5 run
- permission: `workspace-write / never`、`max_workers=24`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- compatibility key: `d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`
- Control-Free reference result: `71a8231c6cc048d0a522aaa43d3a91b6`
- C163 result ID: `e92b8cfddcd942cda3d5686b7f532726`
- result content SHA-256: `804f6820e9b10a764e42085100d27ce129821dbce608e65aed72e4cf1cbcba93`
- 実行・preflight・採点証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate163-luna6-high-standard14-n5-cli0156-20260924-r1`

採用は未判断、releaseは未作成、runtime projectionは未許可である。一次resultは[`e92b8cfddcd942cda3d5686b7f532726.json`](e92b8cfddcd942cda3d5686b7f532726.json)、機械可読比較は[`計測集計`](candidate163-luna6-high-standard14-n5-cli0156_2026-09-24.json)を参照。
