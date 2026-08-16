# Candidate263結果影響範囲の依存関係閉鎖 F03・F10 entrypoint N=5

## 結論

Candidate263 `the-caption-3ce91a4-result-effect-dependency-closure-r1`をF03とF10 entrypointで各N=5実行した。10 / 10件がvalidかつ採点可能で、すべてScore `4`だった。

しかし、狙った挙動はCandidate254から改善しなかった。F03で開始確認の結果に影響されない必要readを別のAI判断へ分けたrunは、Candidate254の2 / 5件に対してCandidate263も2 / 5件だった。F10でpath-local instructionとentrypoint一覧を確認してから三つのentrypoint本文を読んだ正常経路も、両者3 / 5件で同数だった。

二ケースを一組とする5標本の中央値は、Candidate263が品質100、all-agent総token `270,323`、経過時間`181.310`秒だった。Candidate254比でtokenは5,419、`1.97%`減った一方、経過時間は29.316秒、`19.29%`増えた。経過時間の増加を品質または必要な正常経路へ対応づけられず、F10ではtokenも`7.17%`増えたため、`unjustified_cost_regression`とする。

Candidate263は`quality_passed / mechanism_failed / unjustified_cost_regression / stopped`とし、追加N、Standard14、採用、release、projectionへ進めない。Candidate254の正式採用も未承認のまま保持する。

## 実行と登録

- 直接の親および比較基準: Candidate254。
- cases: `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1。
- 各N=5、合計10件。
- valid / rateable: 10 / 10。
- excluded / execution error: 0 / 0。
- Score: `4 = 10`。
- Candidate254基準result: `c9023c2303bd45cebb61bd67736f34e4`。
- Candidate263登録result: `478d39fb4327490e8d9c2202bff66e43`。
- comparison compatibility key: `f02b8f95c958a564b607d0aaf73f8402baa90fc54a1bc703375d3ec8796adc32`。
- Candidate263 selection: `21697433f0df45e58fead3803bebcbd7`。
- Candidate263 analysis: `5b7ca52da333400fa5b58b04e353a91c`。

## ケース別KPI

| ケース | Candidate254 token | Candidate263 token | token差 | Candidate254秒 | Candidate263秒 | 時間差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F03 atomic context cleanup | 182,945 | 151,877 | `-16.98%` | 87.773 | 102.820 | `+17.14%` |
| F10 entrypoint inventory | 105,979 | 113,573 | `+7.17%` | 68.331 | 88.201 | `+29.08%` |
| 二ケース合算中央値 | 275,742 | 270,323 | `-1.97%` | 151.994 | 181.310 | `+19.29%` |

ケース別中央値の合計と、同じselection iterationを組にした合算中央値は集計方法が異なるため一致しない。比較判定には登録済み合算中央値を使い、ケース別値は原因診断へ使う。

## 挙動の比較

### F03

Candidate263の3件は、開始状態の確認と対象source・testのreadを同じAI判断から発行した。残る2件は、開始状態だけを先に確認し、そのresultをAIへ返してから対象readを発行した。

Candidate254の保存済み5件も同じ内訳で、共同発行3件、分離2件だった。したがって、`result_effect_scope`と待機permissionを明示的に接続した置換は、今回のN=5では分離の発生率を変えていない。

### F10 entrypoint

正常経路は、`src/AGENTS.md`とentrypoint一覧までを同じ判断から確認し、そのresultを受け取った後に三つのentrypoint本文を読む経路とした。path-local instructionは配下readの対象またはpermissionを変え得るためである。

Candidate263は3 / 5件、Candidate254も3 / 5件がこの経路だった。両者の残る2件は、`src/AGENTS.md`のresultを受け取る前にentrypoint本文も発行した。Candidate263は過剰遮断で正常経路を失ってはいないが、必要な依存関係の再現性も高めていない。

## 判断

Candidate263はCandidate254を直接の親とする本来の修正として測定したが、置換した一般文による挙動差は確認できなかった。品質Scoreだけを理由に採用せず、token減少だけで経過時間増加を相殺しない。

今回の結果から、同じ意味の制御をさらに強い文へ書き換える案は作らない。F03の分離はCandidate254の開始確認専用文にも反しており、文面の強調を重ねても新しいpermissionまたはdependencyを閉じたことにならないためである。次の検討を再開する場合は、Candidate254の別の合法な開放辺を保存traceから特定するか、Candidate254の意味を保った本文圧縮を独立した目的として設計する必要がある。

現在状態は`targeted_n5_completed / valid_10_of_10 / score4_10_of_10 / f03_split_2_of_5_same_as_candidate254 / f10_required_dependency_3_of_5_same_as_candidate254 / token_improved_1_97_percent / elapsed_regressed_19_29_percent / mechanism_failed / unjustified_cost_regression / stopped / standard14_not_started / candidate263_adoption_not_approved / candidate254_adoption_not_approved / release_not_created / projection_not_performed`とする。
