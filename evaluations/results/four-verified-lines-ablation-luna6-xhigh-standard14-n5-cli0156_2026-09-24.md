# Candidate275（4文版）Standard14 N=5 GPT-6 Luna xHigh（2026-09-24）

## 結果

Candidate275をGPT-6 Luna、reasoning xhighでStandard14の14ケース各5回、計70 run計測した。70件すべて有効・採点可能で、Score 4は70 / 70件、除外attemptは0件だった。

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | 70 / 70 |
| Score 4 | 70 / 70 |
| 除外attempt | 0 |
| quality中央値 | 100.000 |
| all-agent token中央値 | 2,716,023 |
| elapsed中央値 | 1,560.930秒 |
| owner-producer証拠不適格（診断値） | 50 / 70 |
| command protocol違反（診断値） | 1 |

品質監査のfailure countは空で、70件すべてScore 4だった。owner-producer証拠不適格とcommand protocol違反はRating v14の診断値であり、Scoreに影響しない。

## 固定条件と登録情報

- prompt identity: the-caption-3ce91a4-four-verified-lines-ablation-r1 r1、bundle SHA-256 357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac
- model / reasoning: gpt-6-luna / xhigh
- profile: [four-verified-lines-ablation-luna6-xhigh-standard14-n5-cli0156-r1](../profiles/four-verified-lines-ablation-luna6-xhigh-standard14-n5-cli0156-r1.json)
- evaluation set: the-caption-standard14-r1 r1、14 cases × N=5、set identity SHA-256 2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33
- 実行機: Mac mini（Mac16,10）
- Codex CLI: 0.156.1、Python 3.14.5、runtime codex-0.156.1-aarch64-apple-darwin-625bf838f7d4fa65dfeeb54e6da8ed42b5aa65436bee3d350cf769f565870e17、runtime SHA-256 0196e89fe5a7598f816ee54232c3d7c26d75e502ab5cfe2c9240e81d90f7255a
- runtime identity SHA-256: 61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73
- permission / 並列上限: workspace-write / never、M=24
- rating contract: outcome-terminal-state-evidence-owner-diagnostic-v14
- result ID: 537d74e437474eb7b405fa4577a0f669
- result content SHA-256: 0a5e828442c8e670235ca9738b5978ce71ec13143dcd3769c9a12c5f47a34398
- compatibility key: 686a198243300f1c2cb993a35d8abf7c257f2989976afc4d6e5bc7383a1e4428
- V4 selection ID: 213d8498ddda4403b774aa5fe75039a6
- preflight receipt: /Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-luna6-xhigh-max-standard14-n5-20260924-r1/effort-sweep-preflight.json、SHA-256 15646398f901591a75b127b15ee67d463c443b1c956c7a71b8d7efc8e9e30e4c
- 実行証拠: /Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-luna6-xhigh-max-standard14-n5-20260924-r1/xhigh/cycle。sealed archive SHA-256 5f98a4f49ecca45f4cd2545ed28ee4a153249f86dc279747dc2baee66a726c09

V4のatomic run選択からresultを登録した。result本体は[登録JSON](four-verified-lines-ablation-luna6-xhigh-standard14-n5-cli0156_2026-09-24.json)、採点内訳は[quality audit](four-verified-lines-ablation-luna6-xhigh-standard14-n5-quality-audit-r1.json)に保存した。
