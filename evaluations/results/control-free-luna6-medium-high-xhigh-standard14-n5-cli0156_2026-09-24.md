# Control-Free GPT-6 Lunaのmedium・high・xhigh計測

同じControl-Freeプロンプトで、GPT-6 Lunaの推論設定`medium`・`high`・`xhigh`を測った。Standard14の14ケースを各設定で5回、計210件実行した。全件が有効で、除外・再試行・実行エラーは0件だった。

| 推論設定 | Score 4 | Score 2 | Score 0 | 全エージェントトークン | 総所要時間 |
| --- | ---: | ---: | ---: | ---: | ---: |
| [medium](f51b4e9814ad40b6a69a261cee3d8a61.json) | 62/70 | 3/70 | 5/70 | 2,509,550 | 713.51秒 |
| [high](71a8231c6cc048d0a522aaa43d3a91b6.json) | 65/70 | 0/70 | 5/70 | 3,141,404 | 1043.65秒 |
| [xhigh](8ff169aaae1f444e9486b8c037c86901.json) | 65/70 | 0/70 | 5/70 | 3,387,566 | 1731.16秒 |

トークンと総所要時間は、各反復の14ケース合計を求めた後、5反復の中央値を指標ごとに算出した。品質スコア中央値は3条件とも92.86%だが、mediumにはScore 2が3件あるため、品質は上表の分布も併せて読む。`medium`に対する差は次のとおり。

| 条件 | トークン | 総所要時間 |
| --- | ---: | ---: |
| high | +25.18% | +46.27% |
| xhigh | +34.99% | +142.63% |

このN=5の固定試験では、mediumのトークンと総所要時間が最も小さく、highとxhighではmediumのScore 2の3件が観測されなかった。実行時のサービス状態の変動までは除けないため、未評価タスクでの一般的な優劣には広げない。

## 品質

3条件とも`TC-A01-LATENT-MODE-POLICY`の5件がScore 0だった。必要な変更後の値が未確定の状態で最終ファイル変更と試験操作が観測された。mediumではさらに`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND`、`TC-F07-CANONICAL-V4-RUNNER`、`TC-F07-DEPENDENCY-PROVENANCE-PAIR`が各1件Score 2だった。必要な変更または明示された検証を完了していない実行である。highとxhighの残る13ケースは全件Score 4だった。

コマンド規約の診断上の違反件数はmedium 0件、high 5件、xhigh 15件だった。owner／producer証拠の診断上の不適合は順に55件・53件・53件である。これらは固定済みRating v14で品質点への追加減点に使わない。

## ケース別中央値

| ケース | mediumトークン | highトークン | xhighトークン | medium秒 | high秒 | xhigh秒 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 295,434 | 443,240 | 503,897 | 72.82 | 98.19 | 201.75 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 181,632 | 311,131 | 368,565 | 52.93 | 76.20 | 128.51 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 230,987 | 228,850 | 243,134 | 56.10 | 65.99 | 110.69 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 311,042 | 429,669 | 500,300 | 61.44 | 97.91 | 227.23 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 175,795 | 207,635 | 225,711 | 54.72 | 71.10 | 123.16 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 269,015 | 307,990 | 263,602 | 62.25 | 78.98 | 131.66 |
| TC-F05-CLARIFY-UNITS-MODE | 76,185 | 33,043 | 31,508 | 29.66 | 31.00 | 33.99 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 49,910 | 77,502 | 63,465 | 15.96 | 32.50 | 45.64 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 208,187 | 247,341 | 306,395 | 48.46 | 73.38 | 142.20 |
| TC-F07-CANONICAL-V4-RUNNER | 217,411 | 233,194 | 266,771 | 51.42 | 82.47 | 133.48 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 167,862 | 173,869 | 158,278 | 55.84 | 66.62 | 100.45 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 163,596 | 160,487 | 192,764 | 40.88 | 54.25 | 92.26 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 101,170 | 216,802 | 96,337 | 46.39 | 90.17 | 95.67 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 108,279 | 79,447 | 171,184 | 53.43 | 52.30 | 106.76 |

ケース別中央値の合計は、反復ごとの14ケース合計の中央値とは一致しない。全反復と減点の内訳は[機械可読記録](control-free-luna6-medium-high-xhigh-standard14-n5-cli0156_2026-09-24.json)に保存した。

## 条件・時間記録

Free bundleは`999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d`。3条件で同じ固定Layer 1、fixture、TaskSpec、Rating v14、Python 3.14.5、CLI 0.156.1、全エージェントトークン集計v1、時間記録コード、並列上限24を使用した。発行前に3プロファイルの差が推論設定と識別子だけであることを機械確認した。

| 設定 | CLI実行区間中央値 | 直接時計取得 | 正式な作業時間取得 |
| --- | ---: | ---: | ---: |
| medium | 694.36秒 | 70/70 | 0/70 |
| high | 1024.80秒 | 70/70 | 0/70 |
| xhigh | 1712.24秒 | 70/70 | 0/70 |

CLI区間は呼び出しから返却までで、純粋な推論時間ではない。正式な作業時間は入力配送境界と時計対応を観測できず、全210件で欠測として保持した。CLI 0.156.1のログ区間診断も全210件で`unsupported_runtime`となった。並列実行全体の壁時計時間は855.78秒で、反復ごとの合計時間とは別の値である。

## 既存のSol結果との関係

今回のLunaと既存の[Free Sol計測](control-free-sol6-low-medium-high-standard14-n5-cli0156_2026-09-24.md)は、同じ推論設定で見た場合、宣言したプロファイル条件がモデルと識別子だけ異なる。モデルが異なるため正式な同一互換条件のLayer 4比較へは混ぜず、次の値は参考観測として示す。xhighのSol結果はない。

| 設定 | Sol Score 4 | Luna Score 4 | Lunaのトークン差 | Lunaの総所要時間差 |
| --- | ---: | ---: | ---: | ---: |
| medium | 65/70 | 62/70 | -13.30% | -12.25% |
| high | 65/70 | 65/70 | +9.19% | +11.48% |

実行日とサービス状態による変動は残る。過去の[Astra Free結果](control-free-astra-low-medium-high-standard14-n5_2026-09-08.md)はCLI版も異なるため、さらに条件差の大きい参考情報として扱う。

## 保存した資料

[数値・ケース別内訳](control-free-luna6-medium-high-xhigh-standard14-n5-cli0156_2026-09-24.json)と3件の登録resultを保存した。各runはatomic registryへ個別索引化した。実行前照合と生証拠は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/control-free-luna6-medium-high-xhigh-campaign-20260924-r1`に保持する。
