# C275〜C277・C279・Free Standard14 N=5統合比較（2026-09-25）

Free、C275〜C277、C279のStandard14 N=5一次resultを統合した。従来runと共通`AGENTS.md`を空にした再試験は別条件として保持し、各一次resultは変更していない。統合JSONには7条件・490試行をrun単位で収録する。

## 条件別集計

| 条件 | Score 4 / 3 / 2 / 0 | 品質中央値 | トークン中央値 | 経過時間中央値 |
|---|---:|---:|---:|---:|
| Free（GPT-6 Luna High） | 65 / 0 / 0 / 5 | 92.86 | 3,141,404 | 1,043.65秒 |
| C275（4文版） | 69 / 1 / 0 / 0 | 100.00 | 2,448,245 | 937.95秒 |
| C276 | 70 / 0 / 0 / 0 | 100.00 | 2,525,590 | 925.10秒 |
| C277（従来run） | 70 / 0 / 0 / 0 | 100.00 | 2,659,295 | 1,028.22秒 |
| C277（共通AGENTS.md空） | 68 / 0 / 0 / 2 | 100.00 | 2,719,631 | 1,051.03秒 |
| C279（従来run） | 69 / 0 / 1 / 0 | 100.00 | 2,509,039 | 984.12秒 |
| C279（共通AGENTS.md空） | 64 / 1 / 0 / 5 | 92.86 | 3,205,076 | 1,242.34秒 |

すべて70 / 70試行がvalidで、除外attemptは0。トークンはall-agent集計。中央値は各resultに保存された5反復の集約値。

## C275からC277

| Candidate | Score 4 / 3 / 2 / 0 | 品質中央値 | トークン中央値 | 経過時間中央値 | 前段からのトークン差 | 前段からの時間差 |
|---|---:|---:|---:|---:|---:|---:|
| C275（4文版） | 69 / 1 / 0 / 0 | 100.00 | 2,448,245 | 937.95秒 | — | — |
| C276 | 70 / 0 / 0 / 0 | 100.00 | 2,525,590 | 925.10秒 | +77,345 (+3.16%) | -12.85秒 (-1.37%) |
| C277（従来run） | 70 / 0 / 0 / 0 | 100.00 | 2,659,295 | 1,028.22秒 | +133,705 (+5.29%) | +103.12秒 (+11.15%) |

C275→C276→従来C277の記録上の互換条件は一致する。品質中央値は100を維持。トークン中央値は各段階で増え、経過時間はC276でわずかに短縮後、C277で増加した。[評価基盤の比較view](candidate275-candidate277-standard14-n5-comparison_2026-09-25.json)にも3つの一次resultをまとめた。

## 比較条件の区別

- 2026-09-24のFree・C275・C276・従来C277・従来C279は記録上同じcompatibility key（`d72f…`）。Free実行時の共通`AGENTS.md`状態は確定できないため、Freeとの差をpromptまたは共通指示の因果効果として扱わない。
- 2026-09-25のC277・C279は共通`AGENTS.md`が0 byteの条件でcompatibility objectが一致する。
- 共通`AGENTS.md`空条件でのC277中央値は、C279比でトークン`-15.15%`、経過時間`-15.40%`。この別試験をC275→C277系列へ混ぜない。

## 空の共通AGENTS.md条件：C277 − C279

| 試験 | トークン中央値 C277 − C279 | 差 | 経過時間中央値 C277 − C279 | 差 |
|---|---:|---:|---:|---:|
| TC-A01-LATENT-MODE-POLICY | 143,730 − 480,744 | -337,014 (-70.1%) | 57.22 − 134.18秒 | -76.95秒 (-57.4%) |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 226,696 − 229,455 | -2,759 (-1.2%) | 71.05 − 68.33秒 | +2.72秒 (+4.0%) |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 222,965 − 244,568 | -21,603 (-8.8%) | 76.49 − 77.04秒 | -0.55秒 (-0.7%) |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 486,317 − 403,209 | +83,108 (+20.6%) | 126.09 − 127.34秒 | -1.25秒 (-1.0%) |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 192,550 − 208,662 | -16,112 (-7.7%) | 81.22 − 84.04秒 | -2.82秒 (-3.4%) |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 290,595 − 328,749 | -38,154 (-11.6%) | 80.90 − 84.92秒 | -4.02秒 (-4.7%) |
| TC-F05-CLARIFY-UNITS-MODE | 78,691 − 31,697 | +46,994 (+148.3%) | 34.36 − 34.41秒 | -0.05秒 (-0.1%) |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 50,043 − 50,334 | -291 (-0.6%) | 34.73 − 40.94秒 | -6.21秒 (-15.2%) |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 272,213 − 268,556 | +3,657 (+1.4%) | 71.70 − 77.42秒 | -5.72秒 (-7.4%) |
| TC-F07-CANONICAL-V4-RUNNER | 227,737 − 207,195 | +20,542 (+9.9%) | 81.62 − 83.87秒 | -2.25秒 (-2.7%) |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 134,203 − 118,397 | +15,806 (+13.4%) | 62.42 − 53.54秒 | +8.88秒 (+16.6%) |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 216,080 − 172,891 | +43,189 (+25.0%) | 91.13 − 70.12秒 | +21.01秒 (+30.0%) |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 124,633 − 173,876 | -49,243 (-28.3%) | 77.55 − 105.87秒 | -28.32秒 (-26.8%) |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 96,021 − 193,961 | -97,940 (-50.5%) | 73.54 − 74.54秒 | -0.99秒 (-1.3%) |

## 収録した一次result

- Free（GPT-6 Luna High）: [71a8231c6cc048d0a522aaa43d3a91b6.json](71a8231c6cc048d0a522aaa43d3a91b6.json) — result ID `71a8231c6cc048d0a522aaa43d3a91b6`
- C275（4文版）: [four-verified-lines-ablation-luna6-high-standard14-n5-cli0156_2026-09-24.json](four-verified-lines-ablation-luna6-high-standard14-n5-cli0156_2026-09-24.json) — result ID `975c33cb36404c2381ce0715fc7a2592`
- C276: [candidate276-execution-control-luna6-high-standard14-n5-cli0156_2026-09-24.json](candidate276-execution-control-luna6-high-standard14-n5-cli0156_2026-09-24.json) — result ID `9c659e7e0e0847beb97051fd23d92d94`
- C277（従来run）: [candidate277-remove-upfront-plan-luna6-high-standard14-n5-cli0156_2026-09-24.json](candidate277-remove-upfront-plan-luna6-high-standard14-n5-cli0156_2026-09-24.json) — result ID `6ae61524a1e34f8b8e97c677e0ad985d`
- C277（共通AGENTS.md空）: [candidate277-no-user-global-standard14-n5-cli0156-no-user-global_2026-09-25.json](candidate277-no-user-global-standard14-n5-cli0156-no-user-global_2026-09-25.json) — result ID `19986f857f7e4dbab09f2c40a5468c1a`
- C279（従来run）: [candidate279-empty-root-agents-luna6-high-standard14-n5-cli0156_2026-09-24.json](candidate279-empty-root-agents-luna6-high-standard14-n5-cli0156_2026-09-24.json) — result ID `0f3d949876f5421da0cecece6dfc59ca`
- C279（共通AGENTS.md空）: [candidate279-empty-root-agents-no-user-global-standard14-n5-cli0156_2026-09-25.json](candidate279-empty-root-agents-no-user-global-standard14-n5-cli0156_2026-09-25.json) — result ID `1e2a80b2204e4d29b8cc81683e6d79cb`

統合JSON: [candidate277-candidate279-free-merged-standard14-n5_2026-09-25.json](candidate277-candidate279-free-merged-standard14-n5_2026-09-25.json)。7条件×70試行のrun-level値、出典result ID、互換キー、品質・トークン・経過時間を収録。

C275〜C277の同一互換条件比較: [比較view](candidate275-candidate277-standard14-n5-comparison_2026-09-25.json)。
