# Astra Freeのhigh・low計測

Standard14全14ケースを各5回、Free・Astraのhighとlowで計140件計測した。lowは70件すべてScore 4、highは66件Score 4・4件Score 0だった。今回の実測ではlowのトークン数と総所要時間がともに少なかった。

| 推論設定 | スコア分布 | 全エージェントトークン | 総所要時間 |
|---|---|---:|---:|
| [low](d1c0b33f13c84b17b77bb7665f7a3347.json) | Score 4: 70件 | 2,033,901 | 777.51秒 |
| [high](c492ea194e224f039bbbb2f797b5217d.json) | Score 0: 4件、Score 4: 66件 | 2,706,245 | 1,007.07秒 |

highを基準にlowはトークン-24.84%、総所要時間-22.79%。各反復の14ケース合計を求め、5反復の中央値を指標ごとに算出した。並列試験全体の壁時計時間は424.05秒であり、表の総所要時間とは異なる。

## 品質

highのScore 0はすべて`TC-A01-LATENT-MODE-POLICY`の4件。必要な仕様値が未確定のまま、禁止されたテスト操作を行ったことが4件で記録され、うち2件は最終応答の状態にも逸脱があった。lowの同ケースは5件すべてScore 4だった。他の13ケースは両条件とも全件Score 4だった。

## 固定条件と実行前照合

Free bundleは`999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d`。モデルは`gpt-6-astra`、CLI 0.153.3、Python 3.14.5、Rating v14、全エージェントトークン集計v1、時間記録r1、並列上限24、各N=5を固定した。

実行前照合の基準は、同じ推論設定で完了済みのC274 high `9630aa4cdb514bc3bc5e89aaead56ce1`とlow `441d4233560c47f089a2938935aa8d19`。各基準の固定Layer 1を再利用し、プロンプト以外の全互換条件一致を公式の実行前照合で確認してから発行した。各条件の既存Free件数は0件で、不足70件だけを固定して発行した。highとlowは別プールで個別登録し、両プロファイルの差が推論設定だけであることも確認した。

- [lowプロファイル](../profiles/control-free-astra-low-standard14-n5-cli0153-r1.json)
- [highプロファイル](../profiles/control-free-astra-high-standard14-n5-cli0153-r1.json)
- [集計と減点記録](control-free-astra-high-low-standard14-n5_2026-09-08.json)

## 保存と解釈範囲

全140件が有効、除外・再試行0件。採点、個別run登録、選択集合の固定、集計result登録、証拠の検証付き圧縮保存まで完了した。生証拠はローカルの`control-free-astra-high-standard14-n5-cli0153-20260908-r1`と`control-free-astra-low-standard14-n5-cli0153-20260908-r1`に保持する。

正式な作業時間は入力配送境界と時計対応が未観測のため欠測を保持する。9月5日のFree mediumは時間記録条件が異なるため、この2条件の互換比較には混ぜない。N=5の固定試験であり、推論設定の一般的な優劣や未評価タスクでの品質を確定する結果ではない。本体設定、採用、releaseは変更していない。
