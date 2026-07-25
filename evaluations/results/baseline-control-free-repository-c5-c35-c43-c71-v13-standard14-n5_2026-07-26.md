# Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 Rating v13 標準14項目 各5回

## 結論

Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71を、Rating v13、標準14項目、各`N=5`、global queue `M=24`で実行した。6条件とも70 / 70件がvalidかつrateableで、result登録とfinal compactを完了した。

公式score分布は、Candidate43とCandidate71が`4 = 70`だった。ControlFreeRepository、Candidate5、Candidate35は`4 / 0 = 65 / 5`で、5件のscore `0`はすべてA01だった。Baselineは`4 / 3 / 1 / 0 = 62 / 2 / 3 / 3`だった。

5反復中央値では、Candidate43が`quality_score = 100.000`、`total_tokens = 3,109,899`、`elapsed_seconds = 1,180.979秒`、Candidate71が`100.000`、`2,131,059`、`1,114.525秒`だった。Candidate71からCandidate43を引くと、`quality_score = 0.000`、`total_tokens = -978,840`（`-31.47%`）、`elapsed_seconds = -66.453秒`（`-5.63%`）である。

このresultは3 KPIと診断を保存する。winner、採用、release、THE-CAPTION本体反映は判断しない。

## 固定条件

- evaluation set: `the-caption-standard14-r1` revision `r1`
- quality rating: `outcome-abstract-condition-preserving-owner-diagnostic-v13`
- rating contract SHA-256: `d2dd4096911c35257c2866872d071f2ee5137bb3dcb6a7b279853e3ebe581f1f`
- target repository: `THE-CAPTION@3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime: Codex CLI `0.144.0`、Python `3.14.5`、memories `false`
- permission: `workspace-write`、approval `never`
- repetition: 14 case × `N=5` = 70 slot
- schedule: global queue、`M=24`
- token accounting: all-agent / `v1`
- evaluation set identity SHA-256: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- comparison conditions SHA-256: `2a0178f296d603f9db3db726ea853104eb2faf94a1cad70aaa8c2b8b00683564`
- compatibility key: `7426ecd03421590549c30a4e16373722153ceefc00280bc305eedb1aa0955633`

6 profileはprompt identity以外のcase、TaskSpec、permission、executor parameter、rating、反復条件を一致させた。v12以前のresultは比較へ混ぜていない。

## 3 KPI

| 条件 | score分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 70件token合計 | 70件elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 1 / 0 = 62 / 2 / 3 / 3` | 92.857 | 12,568,833 | 3,628.547秒 | 60,941,742 | 17,906.823秒 |
| ControlFreeRepository | `4 / 0 = 65 / 5` | 92.857 | 3,918,502 | 1,308.201秒 | 18,813,966 | 6,431.764秒 |
| Candidate5 | `4 / 0 = 65 / 5` | 92.857 | 11,527,233 | 2,871.018秒 | 56,823,758 | 14,183.290秒 |
| Candidate35 | `4 / 0 = 65 / 5` | 92.857 | 5,454,929 | 1,775.954秒 | 27,127,698 | 8,965.267秒 |
| Candidate43 | `4 = 70` | 100.000 | 3,109,899 | 1,180.979秒 | 16,767,852 | 5,999.076秒 |
| Candidate71 | `4 = 70` | 100.000 | 2,131,059 | 1,114.525秒 | 10,863,680 | 5,525.379秒 |

Baselineとの差は記述的な差分であり、採用順位ではない。

| 条件 | quality中央値差 | token中央値差 | elapsed中央値差 | token合計差 | elapsed合計差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| ControlFreeRepository - Baseline | 0.000 | -8,650,331（-68.82%） | -2,320.345秒（-63.95%） | -42,127,776（-69.13%） | -11,475.060秒（-64.08%） |
| Candidate5 - Baseline | 0.000 | -1,041,600（-8.29%） | -757.529秒（-20.88%） | -4,117,984（-6.76%） | -3,723.534秒（-20.79%） |
| Candidate35 - Baseline | 0.000 | -7,113,904（-56.60%） | -1,852.593秒（-51.06%） | -33,814,044（-55.49%） | -8,941.557秒（-49.93%） |
| Candidate43 - Baseline | +7.143 | -9,458,934（-75.26%） | -2,447.568秒（-67.45%） | -44,173,890（-72.49%） | -11,907.748秒（-66.50%） |
| Candidate71 - Baseline | +7.143 | -10,437,774（-83.04%） | -2,514.021秒（-69.28%） | -50,078,062（-82.17%） | -12,381.445秒（-69.14%） |

Candidate71とCandidate43の直接差は、token合計`-5,904,172`（`-35.21%`）、elapsed合計`-473.697秒`（`-7.90%`）だった。

## 低得点

| 条件 | case | 件数 | 保存された主なfailure |
| --- | --- | ---: | --- |
| Baseline | A01 | 3 | 未固定値の確認前に変更・試験へ進行 |
| Baseline | A02 | 4 | 3件はcanonical routeと変更pathが未達、4件は抽象的な既存test成功証拠が不足 |
| Baseline | F07 dependency | 1 | model-visibleに明示されたdependency確認commandを未実行 |
| ControlFreeRepository | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate5 | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate35 | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate43 | — | 0 | — |
| Candidate71 | — | 0 | — |

BaselineのF07 canonical iteration 3では`command_evidence_incomplete`を1件除外し、同じslotを再実行してvalid resultを得た。他5条件のexcluded attemptは0件だった。

## 診断

診断値は3 KPIへ追加せず、quality scoreを変更しない。

| 条件 | command protocol violation | owner-producer evidence inadmissible | F10 Monthly数値line |
| --- | ---: | ---: | --- |
| Baseline | 523 | 52 | exact 4 / mismatch 1 |
| ControlFreeRepository | 0 | 55 | exact 5 |
| Candidate5 | 345 | 28 | exact 5 |
| Candidate35 | 19 | 0 | exact 5 |
| Candidate43 | 0 | 55 | exact 5 |
| Candidate71 | 0 | 55 | exact 5 |

## Rating v13実行基盤の修正

最初のBaseline実行では70 / 70 valid取得後、`scripts/standard14_quality_audit.py`がv13 contract IDを未登録として採点を拒否した。`evaluation_loop.py`のv13受理とstandard14 auditの対応が一致していなかった。

standard14 auditと共有quality policyへv13を接続した。A02は、提示した抽象条件を未提示の`git diff --check`へ具体化せず、canonical最終状態、変更path、成功した任意の既存test証拠で採点する。修正後、関連47 testsと全体392 tests・261 subtestsが通過した。Baselineの同じsealed batchを採点から再開し、実行済み証拠を変更または再生成していない。

## 保存artifact

| 条件 | result ID |
| --- | --- |
| Baseline | `59e93eaaeb87435c9c0d94d80df9bb9d` |
| ControlFreeRepository | `cab2dd3228e843d799eba40576b8addf` |
| Candidate5 | `393a17c72f534f32bd3252ef6857f811` |
| Candidate35 | `5f5f040fd62d4a248c51fc76851e7dff` |
| Candidate43 | `a86c883ef9644a04a7371907aacb4745` |
| Candidate71 | `1b3d8048c391460eae8234e083494763` |

- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- comparison view: `comparison-views/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5-20260726-r1.json`
- campaign root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs`

各campaignに`batch-001/compact/final-compact-receipt.json`を保存した。raw execution evidenceはrepositoryへcommitしない。
