# P005 THE-CAPTION投影 Standard14 N=5評価

## 結論

P005のroot `AGENTS.md`をTHE-CAPTIONへ投影し、Candidate147の非root 18 targetをbyte一致で保持した条件で、Standard14の14項目を各5件評価した。70 / 70件が`valid`かつScore `4`だった。

P001との互換比較では、5回の14項目集約中央値がtoken `-36.30%`、elapsed `+1.23%`だった。P005のterminal projectionはP001で増えたtokenの一部を回収したが、経過時間は改善していない。Candidate147比ではtoken `+36.14%`、elapsed `+18.48%`で、portable化に伴うcostは残る。現在状態は`standard14_n5_completed / quality_gate_passed / p001_token_cost_recovered_partially / p001_elapsed_not_improved / c147_cost_regression_persists / p005_canonical_unchanged / adoption_not_decided / release_not_created / runtime_projection_not_authorized`とする。N=5の差を安定傾向とは扱わず、N=20へ自動拡張しない。

## identityと互換条件

- P005正本: `p005-portable-full-agent-codex-validation-terminal-projection-r1`
- P005 root SHA-256: `2cb70ccd11fcfe605accf9b212050ed08b6db0eb0a522d502d35c33d58301681`
- Standard14投影bundle: `p005-the-caption-standard14-projection-r1`
- 投影bundle SHA-256: `bfee25ef8b710ec03d4c73d81aea7fc1fd16e558f4565fd5565990dea2d4c01b`
- profile: `p005-the-caption-standard14-projection-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- permission: `workspace-write / never`
- 設定上の並列上限: `M=24`
- token accounting: all-agent v1
- 直接比較基準: Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`
- portable親比較: P001 result `e8bb0207c8014e5bac8d79ec2cf74bf4`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- P005投影result: [`28082254ecc6447f8d76d63e85062299.json`](28082254ecc6447f8d76d63e85062299.json)

投影bundleはC147 bundleと同じ19 targetを持ち、root `AGENTS.md`だけをP005 bytesへ置換した。P005単体bundleを直接重ねた場合に残るTHE-CAPTION元promptを比較差へ混ぜていない。作成前の境界は[`P005 THE-CAPTION Standard14投影設計`](../../docs/p005-the-caption-standard14-projection-design.md)を正とする。

preflightはprompt identity以外の条件を照合し、14項目×5件の70 slot、発行済み0件、status `ready`を固定した。新規70件は235.715秒の外側実行で完了し、valid 70、excluded 0、再試行0、controller error 0だった。

## 品質

Rating v14では70 / 70件がScore `4`で、成果不成立、必須command失敗、許可外path変更および採点failureは0件だった。

owner-producer evidence不成立53件、command protocol diagnostic 2件、F10 monthlyのnumeric location不一致1件を診断情報として記録した。Rating v14では、いずれも成果、必須commandの成功および許可範囲を満たした品質点へ混ぜていない。

## 3 KPI比較

Candidate147とP001も同じatomic registryから14項目×5件を選択し、同じ集計器で再集計した。

| 指標 | Candidate147 | P001投影 | P005投影 | P005-C147 | P005-P001 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100.00 | 100.00 | 100.00 | 0.00 | 0.00 |
| token中央値 | 1,447,626 | 3,094,024 | 1,970,857 | +523,231（+36.14%） | -1,123,167（-36.30%） |
| elapsed中央値 | 852.543秒 | 997.840秒 | 1,010.082秒 | +157.539秒（+18.48%） | +12.243秒（+1.23%） |

## 項目別KPI

各値は同一項目5件の中央値である。差分率はP005を左記の比較対象に対して計算した。

| Case | C147 token | P001 token | P005 token | 対C147 | 対P001 | C147秒 | P001秒 | P005秒 | 対C147 | 対P001 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 19,195 | 35,466 | 36,580 | +90.6% | +3.1% | 12.148 | 16.842 | 17.054 | +40.4% | +1.3% |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 129,085 | 440,835 | 203,624 | +57.7% | -53.8% | 73.379 | 97.585 | 97.754 | +33.2% | +0.2% |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 107,202 | 237,695 | 144,610 | +34.9% | -39.2% | 66.424 | 69.421 | 74.229 | +11.7% | +6.9% |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 128,236 | 400,542 | 250,072 | +95.0% | -37.6% | 100.607 | 115.735 | 111.245 | +10.6% | -3.9% |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 104,320 | 221,961 | 164,494 | +57.7% | -25.9% | 70.866 | 107.884 | 100.423 | +41.7% | -6.9% |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 151,170 | 343,553 | 196,763 | +30.2% | -42.7% | 91.431 | 92.742 | 124.681 | +36.4% | +34.4% |
| `TC-F05-CLARIFY-UNITS-MODE` | 37,242 | 36,369 | 39,618 | +6.4% | +8.9% | 26.725 | 18.396 | 17.728 | -33.7% | -3.6% |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 37,366 | 39,100 | 39,797 | +6.5% | +1.8% | 25.291 | 21.969 | 20.419 | -19.3% | -7.1% |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 151,542 | 258,687 | 151,513 | -0.0% | -41.4% | 79.393 | 76.623 | 80.465 | +1.3% | +5.0% |
| `TC-F07-CANONICAL-V4-RUNNER` | 102,504 | 258,328 | 151,826 | +48.1% | -41.2% | 72.547 | 99.795 | 88.799 | +22.4% | -11.0% |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 87,284 | 139,368 | 100,259 | +14.9% | -28.1% | 54.324 | 59.386 | 54.703 | +0.7% | -7.9% |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 113,067 | 335,000 | 119,932 | +6.1% | -64.2% | 56.343 | 105.185 | 79.126 | +40.4% | -24.8% |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 87,934 | 144,698 | 110,600 | +25.8% | -23.6% | 61.546 | 66.582 | 64.905 | +5.5% | -2.5% |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 93,096 | 92,499 | 98,857 | +6.2% | +6.9% | 51.796 | 41.545 | 47.159 | -9.0% | +13.5% |

P001比ではtokenが9 / 14項目で減り、elapsedは7 / 14項目で減った。token回収が大きいA02、F01、F02、F04、F06、F07 canonical、F08は、P005のterminal projectionがP001のvalidation carrier負担を抑えた結果と整合する。一方、F04はtokenを42.7%減らしてもelapsedが34.4%増え、全体でもtoken減少がelapsed改善へ直結していない。N=5の項目別中央値だけから、個別文または単一tool待機へ因果帰属はしない。

## 後続のC147移植損失監査

同じ保存traceをC147からの移植損失として再集計した。三者で選択済みraw traceが揃う11 Case各55 runでは、P005がP001のaction後wave超過43件のうち34件を回収した一方、action前waveはC147より23件多く、P001よりも6件多かった。未移植境界はvalidation carrierではなく、C147の`DECISION_BOUNDARY`をplatform上で運ぶfrontier carrierへ限定する。F04のelapsed増は静的確認のmethod失敗・再確認と一件の誤った独立producer起動が混在し、次差分の主対象にはしない。詳細は[`P005 Standard14 C147移植損失監査`](../../docs/p005-standard14-c147-transplant-loss-audit.md)を正とする。

## 保存先と境界

raw試験rootは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/p005-the-caption-standard14-projection-v14-medium-standard14-n5-cli0146-20260819-r1`である。preflight、70件の実行証拠、quality audit、P005・P001・C147のselection・analysis・comparison、execution seal、result登録およびfinal compactを保持する。execution archive SHA-256は`bd9ea426a486bd03b7e06a2d2ae0e8a33cd32b9977f6419e7031615259000594`、final compact archive SHA-256は`d34746a3e597484e26fc7377a5a85bbfb289394d1754d99062d55ad7b50787a9`である。

この結果はTHE-CAPTION Standard14上のP005投影評価だけを示す。P005のVCC6 N=5結果、P005正本、採用、release、他platformへの配置およびruntime projectionは変更していない。
