# Candidate264開始確認結果影響範囲の復元 F01・F02・F03・F10 entrypoint N=5

## 結論

Candidate264 `the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1`をF01、F02、F03、F10 entrypointで各N=5実行した。20 / 20件がvalidかつ採点可能で、すべてScore `4`だった。

狙ったF03の機序は、Candidate254の共同発行3 / 5件、分離2 / 5件から、Candidate264では共同発行5 / 5件、分離0 / 5件へ改善した。F01とF02の共同発行も各5 / 5件を保持した。一方、局所`src/AGENTS.md`が配下readの対象または許可を変え得るF10では、instruction resultを受領してからentrypoint本文を読む正常経路がCandidate254の3 / 5件から2 / 5件へ悪化した。

四ケースを一組とする5標本の中央値は、Candidate264が品質100、all-agent総token `484,121`、経過時間`307.710`秒だった。Candidate254比でtokenは94,854、`16.38%`減った一方、経過時間は14.581秒、`4.97%`増えた。Candidate147の保存済みStandard14 N=5から同じ四ケースを抽出した値との比較では、tokenは10,585、`2.14%`減り、経過時間は4.781秒、`1.58%`増えた。品質は三者とも100である。経過時間の増加を品質または必要な正常経路へ対応づけられず、F10の正常経路も悪化したため、設計時の停止条件に該当する。

品質結果と対象機序の改善は無効化しない。ただしCandidate264は`quality_passed / target_mechanism_passed / normal_route_regressed / token_improved / elapsed_regressed / unjustified_cost_regression / stopped`とし、追加N、Standard14、採用、release、projectionへ進めない。Candidate254の正式採用も未承認のまま保持する。

## 実行と登録

- 直接の親および比較基準: Candidate254。
- cases: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1。
- 各N=5、合計20件。
- valid / rateable: 20 / 20。
- excluded / execution error: 0 / 0。
- Score: `4 = 20`。
- Candidate147比較元result: `f7baeadc5bd44399ac13cc0e0a8aff48`。保存済みStandard14 N=5の70件から同じ四ケース20件を抽出した。
- Candidate254基準result: `4208b6ca016d485684f8df9fadc5b38e`。
- Candidate264登録result: `1a64c1b2429c4e89aff3aedd6836944e`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- Candidate254 selection: `abcb8911b8824361a44db8b8459c51ad`。
- Candidate264 selection: `b1b87cc78c3648659960216d27296ca4`。

## ケース別KPI

### all-agent総token

| ケース | Candidate147 | Candidate254 | Candidate264 | Candidate264のC147比 | Candidate264のC254比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 107,202 | 113,598 | 145,447 | `+35.68%` | `+28.04%` |
| F02 cross-layer history date bound | 128,236 | 184,341 | 133,018 | `+3.73%` | `-27.84%` |
| F03 atomic context cleanup | 104,320 | 182,945 | 133,285 | `+27.77%` | `-27.14%` |
| F10 entrypoint inventory | 87,934 | 105,979 | 90,323 | `+2.72%` | `-14.77%` |
| 四ケース合算中央値 | 494,706 | 578,975 | 484,121 | `-2.14%` | `-16.38%` |

### 経過時間

| ケース | Candidate147秒 | Candidate254秒 | Candidate264秒 | Candidate264のC147比 | Candidate264のC254比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 66.424 | 56.578 | 72.577 | `+9.26%` | `+28.28%` |
| F02 cross-layer history date bound | 100.607 | 85.479 | 80.972 | `-19.52%` | `-5.27%` |
| F03 atomic context cleanup | 70.866 | 87.773 | 77.404 | `+9.23%` | `-11.81%` |
| F10 entrypoint inventory | 61.546 | 68.331 | 71.026 | `+15.40%` | `+3.94%` |
| 四ケース合算中央値 | 302.929 | 293.129 | 307.710 | `+1.58%` | `+4.97%` |

Candidate147のケース別値は、登録result `f7baeadc5bd44399ac13cc0e0a8aff48`の同じ四ケース・各N=5から算出した。ケース別中央値の合計と、同じselection iterationを組にした合算中央値は集計方法が異なるため一致しない。合算行は各iterationで四ケースを合算した5標本の中央値であり、ケース別値は原因診断へ使う。

## 挙動の比較

### F01・F02

Candidate264とCandidate254はどちらも、開始確認と、開始確認resultで対象または許可が変わらない許可済みreadを5 / 5件で同じAI判断から発行した。既に成立していた正常経路は保持した。

### F03

Candidate264は5 / 5件で開始確認と必要readを同じAI判断から発行した。Candidate254では3 / 5件が共同発行、2 / 5件が分離だったため、原因分解記録が指定した四つの関係を一組で復元した変更は、対象としていた不要なモデル再判断を今回のN=5で解消した。

### F10 entrypoint

正常経路は、`src/AGENTS.md`のresultを受領してから三つのentrypoint本文を読む経路とした。局所規則によって配下readの対象または許可が変わり得るためである。

Candidate264でこの経路を通ったのは2 / 5件だった。残る3件は、`src/AGENTS.md`のresultを受け取る前にentrypoint本文も発行した。Candidate254は正常経路3 / 5件だったため、Candidate264は必要な依存関係を保持できず、設計時に固定した停止条件へ該当する。

## 判断

Candidate264は、原因分解記録で唯一許可したCandidate254への四関係の復元だけを実施し、F03の対象経路を閉じた。しかし、同じ変更がF10の必要な依存関係を安定して保持せず、正常経路をCandidate254より悪化させた。全件Score `4`であることや全体tokenが減ったことを、この正常経路の悪化を無視する採用根拠にはしない。

原因分解記録の範囲外である本文圧縮、完了待ち対策、command、wrapper、wait時間、read範囲の指定、別Candidateの修正は行わない。Candidate264の結果を反例として保持し、ここで停止する。

現在状態は`targeted_n5_completed / valid_20_of_20 / score4_20_of_20 / f01_joint_5_of_5 / f02_joint_5_of_5 / f03_joint_5_of_5_target_mechanism_passed / f10_required_dependency_2_of_5_normal_route_regressed / token_improved_16_38_percent / elapsed_regressed_4_97_percent / unjustified_cost_regression / stopped / standard14_not_started / candidate264_adoption_not_approved / candidate254_adoption_not_approved / release_not_created / projection_not_performed`とする。
