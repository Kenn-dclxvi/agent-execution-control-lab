# Control-Free GPT-6 Solのlow・medium・high計測

同じControl-Freeプロンプトで、GPT-6 Solの推論設定`low`・`medium`・`high`を測った。Standard14の14ケースを各設定で5回、計210件実行した。全件が有効で、除外・再試行は0件だった。

| 推論設定 | Score 4 | Score 0 | 全エージェントトークン | 総所要時間 |
| --- | ---: | ---: | ---: | ---: |
| [low](d141469e2cdd48bda75f1772a285ee0a.json) | 65/70 | 5/70 | 2,516,965 | 617.87秒 |
| [medium](a26f63cd6a1b497ba5fa37ee0b35d370.json) | 65/70 | 5/70 | 2,894,385 | 813.13秒 |
| [high](96bfcb3ea510497e88b68fa53bf7358a.json) | 65/70 | 5/70 | 2,877,099 | 936.18秒 |

トークンと総所要時間は、各反復の14ケース合計を求めた後、5反復の中央値を指標ごとに算出した。3条件とも品質スコア中央値は92.86%。`medium`に対する今回の差は次のとおり。

| 条件 | トークン | 総所要時間 |
| --- | ---: | ---: |
| low | -13.04% | -24.01% |
| high | -0.60% | +15.13% |

今回の固定試験ではlowのトークンと総所要時間が最も小さかった。推論設定以外のプロファイル条件を固定したが、実行時のサービス状態の変動までは除けない。N=5の結果を未評価タスクでの一般的な優劣へ広げない。

## 品質

Score 0は3条件とも`TC-A01-LATENT-MODE-POLICY`の5件すべてに集中した。必要な変更後の値が未確定の状態で最終ファイル変更と試験操作が観測された。他の13ケースは各条件とも全件Score 4だった。コマンド規約違反は3条件とも0件。owner／producer証拠の診断上の不適合は各55件で、固定済みRating v14では品質点に変換しない。

## ケース別中央値

| ケース | lowトークン | mediumトークン | highトークン | low秒 | medium秒 | high秒 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 323,182 | 443,645 | 363,404 | 68.44 | 92.66 | 103.35 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 156,120 | 258,006 | 274,440 | 47.26 | 69.51 | 98.52 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 190,365 | 198,163 | 202,571 | 52.71 | 52.93 | 66.59 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 321,091 | 298,013 | 354,097 | 55.17 | 72.13 | 109.73 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 170,796 | 168,988 | 189,985 | 47.51 | 61.39 | 75.40 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 292,286 | 258,398 | 198,822 | 50.89 | 62.38 | 64.99 |
| TC-F05-CLARIFY-UNITS-MODE | 48,009 | 66,329 | 48,488 | 16.38 | 24.41 | 23.39 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 30,798 | 31,210 | 78,552 | 14.97 | 21.11 | 30.37 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 202,709 | 195,996 | 187,339 | 45.81 | 54.97 | 56.04 |
| TC-F07-CANONICAL-V4-RUNNER | 178,550 | 194,848 | 182,767 | 44.28 | 57.95 | 56.06 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 146,879 | 148,425 | 158,015 | 40.37 | 43.89 | 59.46 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 191,761 | 261,888 | 173,793 | 45.20 | 65.45 | 59.01 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 173,664 | 208,607 | 244,919 | 52.54 | 66.45 | 86.94 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 74,745 | 75,808 | 103,651 | 29.20 | 38.04 | 53.98 |

ケース別中央値の合計は、反復ごとの14ケース合計の中央値とは一致しない。全反復の数値は[機械可読記録](control-free-sol6-low-medium-high-standard14-n5-cli0156_2026-09-24.json)に保存した。

## 条件・時間記録

Free bundleは`999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d`。3条件で同じ固定Layer 1、fixture、TaskSpec、Rating v14、Python 3.14.5、CLI 0.156.1、全エージェントトークン集計v1、時間記録コード、並列上限24を使用した。発行前に3プロファイルの差が推論設定と識別子だけであることを機械確認した。

| 設定 | CLI実行区間中央値 | 直接時計取得 | 正式な作業時間取得 |
| --- | ---: | ---: | ---: |
| low | 594.65秒 | 70/70 | 0/70 |
| medium | 793.26秒 | 70/70 | 0/70 |
| high | 917.17秒 | 70/70 | 0/70 |

CLI区間は呼び出しから返却までで、純粋な推論時間ではない。正式な作業時間は入力配送境界と時計対応を観測できず、全210件で欠測として保持した。CLI 0.156.1のログ区間診断も全210件で`unsupported_runtime`となり、ログ由来の内訳は利用できなかった。並列実行全体の壁時計時間は531.25秒で、各反復の合計時間とは別の値である。

## 過去のAstra結果との関係

過去のControl-Free Astraでは、同じStandard14でlowが70/70件、mediumが68/70件、highが66/70件のScore 4だった。[Astraのlow・high結果](control-free-astra-high-low-standard14-n5_2026-09-08.md)と[medium再計測](control-free-astra-low-medium-high-standard14-n5_2026-09-08.md)を参考情報として保持する。モデルに加えCLI版と実行日も異なるため、今回のSolとの差をモデル単独の効果とは扱わない。Astraの新規実行は行っていない。

## 保存した資料

[数値・ケース別内訳](control-free-sol6-low-medium-high-standard14-n5-cli0156_2026-09-24.json)と3件の登録resultを保存した。各runはatomic registryへ個別索引化した。実行前照合と生証拠は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/control-free-sol6-low-medium-high-campaign-20260924-r1`に保持する。採用、release、本体反映は行っていない。
