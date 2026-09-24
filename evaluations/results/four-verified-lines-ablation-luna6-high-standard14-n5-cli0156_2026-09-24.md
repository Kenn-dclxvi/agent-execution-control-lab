# Candidate275（4文版）Standard14 N=5（2026-09-24）

## 結果

4文版CandidateをGPT-6 Luna、reasoning `high`でStandard14の14ケース各5回、計70 run計測した。F02の先行5 runを再利用し、残る13ケース×5回の65 runだけを新規実行した。70件すべて有効・採点可能で、登録result上のScore `4`は69 / 70件、除外attemptは0件だった。F02の1件は、先行F02評価の採点訂正v2でScore `3`から`4`へ訂正済みだが、write-onceのatomic run記録と今回の登録resultには訂正前の`3`が残る。訂正を反映した分布は70 / 70件Score `4`となる。中央値quality scoreは訂正前後とも100で変わらない。

### F02 1件のScore訂正

対象はF02 iteration 2（run ID `f6ec1150753843669e47bcf3a2e7094f`）である。最初の採点は、focused pytestの初回終了コード`2`を失敗としてScore `3`にしたものだった。その後、同じ必須focused pytestを再実行した終了コードは`0`で、`main_verify.sh`も終了コード`0`だった。必須試験の成功証拠が揃い、protocol violationは`0`件、unexpected changed pathsも空だったため、Score `4`へ訂正した。初回結果だけを根拠にした採点を、同一run内の後続試験結果を含めて改めた訂正である。

訂正記録はrating correction v2にwrite-onceで保存した一方、先行時に登録したatomic run recordは上書きしていない。そのため今回のselectionから作った一次登録resultにも元のScore `3`が残る。上表では登録値と訂正反映後の分布を別行にしている。訂正記録、対象runのcommand evidence、rating履歴は実行証拠ディレクトリ内に保持している。

同じ比較条件のControl-Free保存resultとの中央値比較では、quality scoreは`+7.143`、all-agent total tokensは`-693,159`（-22.07%）、elapsedは`-105.704秒`（-10.13%）だった。4文版とC163の5文版は、両方の中央値quality scoreが100だった。5文版に対する4文版の差はtoken `+8,460`（+0.35%）、elapsed `-116.848秒`（-11.08%）だった。

| 指標 | Control-Free | C163 5文版 | 4文版 | 4文版 - Control-Free | 4文版 - C163 |
| --- | ---: | ---: | ---: | ---: | ---: |
| valid / rateable | 70 / 70 | 70 / 70 | 70 / 70 | 0 | 0 |
| Score `4`（登録result） | 65 / 70 | 69 / 70 | 69 / 70 | +4 | 0 |
| Score `4`（F02訂正反映） | 65 / 70 | 69 / 70 | 70 / 70 | +5 | +1 |
| quality中央値 | 92.857 | 100.000 | 100.000 | +7.143 | +0.000 |
| all-agent token中央値 | 3,141,404 | 2,439,785 | 2,448,245 | -693,159（-22.07%） | +8,460（+0.35%） |
| elapsed中央値 | 1043.654秒 | 1054.798秒 | 937.950秒 | -105.704秒（-10.13%） | -116.848秒（-11.08%） |

このN=5結果は固定Standard14での観測であり、未見条件への一般化や一文単独の効果を示さない。採用は未判断、releaseは未作成、runtime projectionは未実施である。

## 固定条件と登録情報

- prompt identity: `the-caption-3ce91a4-four-verified-lines-ablation-r1` r1、bundle SHA-256 `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`
- model / reasoning: `gpt-6-luna / high`
- Codex CLI: `0.156.1`、Python `3.14.5`
- evaluation set: `the-caption-standard14-r1` r1、14 cases × N=5
- permission: `workspace-write / never`、configured M=24
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- compatibility key: `d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`
- Control-Free result: `71a8231c6cc048d0a522aaa43d3a91b6`
- C163 5文版 result: `e92b8cfddcd942cda3d5686b7f532726`
- 4文版 result: `975c33cb36404c2381ce0715fc7a2592`
- result content SHA-256: `34d097d1a45abd3c5cd602f355fb18bb09e0443c27fda696b21e2858f9e71671`
- 実行・preflight・採点証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-luna6-high-standard14-n5-20260924-r1`

preflight receiptは65不足slotを認可し、保存済みF02 5件を再利用した。新規実行は65 / 65 valid、除外0件、外側runner経過時間229.071秒だった。品質監査は[`quality audit`](four-verified-lines-ablation-luna6-high-standard14-n5-quality-audit-r1.json)に、比較の機械可読中央値と差分は[`comparison view`](four-verified-lines-ablation-luna6-high-standard14-n5-comparisons_2026-09-24.json)に保存した。一次登録resultは[`975c33cb36404c2381ce0715fc7a2592.json`](four-verified-lines-ablation-luna6-high-standard14-n5-cli0156_2026-09-24.json)である。F02訂正の根拠は[先行F02 result](candidate163-four-sentence-ablation-f02-luna6-high-n5_2026-09-24.md)と、その外部実行記録のrating correction v2である。
