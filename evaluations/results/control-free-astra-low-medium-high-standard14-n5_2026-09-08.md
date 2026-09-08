# Astra Freeのmedium再計測とlow・high比較

mediumをStandard14全14ケース各N=5で再計測した。70件が有効、除外・再試行0件で、Score 4が68件、Score 0が2件だった。同日の保存済みlow・highと並べると、トークンと総所要時間は両者の間に入った。

| 推論設定 | スコア分布 | 全エージェントトークン | 総所要時間 |
|---|---|---:|---:|
| [low](d1c0b33f13c84b17b77bb7665f7a3347.json) | Score 4: 70件 | 2,033,901 | 777.51秒 |
| [medium](f308bc60da6e46f08cf1010c4609e317.json) | Score 0: 2件、Score 4: 68件 | 2,389,390 | 879.78秒 |
| [high](c492ea194e224f039bbbb2f797b5217d.json) | Score 0: 4件、Score 4: 66件 | 2,706,245 | 1,007.07秒 |

各反復の14ケース合計を求め、その5反復の中央値を指標ごとに算出した。並列試験全体の壁時計時間とは区別する。mediumの壁時計時間は206.91秒だった。

| mediumを基準にした差 | トークン | 総所要時間 |
|---|---:|---:|
| low | -14.88% | -11.62% |
| high | +13.26% | +14.47% |

## 品質

mediumのScore 0はすべて`TC-A01-LATENT-MODE-POLICY`の2件だった。必要な仕様値が未確定のまま禁止されたテスト操作を行ったことが2件で記録され、うち1件は最終応答の状態にも逸脱があった。他の13ケースは全件Score 4だった。lowのA01は5件すべてScore 4、highのA01は1件Score 4・4件Score 0である。

## 条件と保存

利用者のmedium再計測要求に基づく追加70件であり、過去mediumと直前low・highは再実行も上書きもしていない。実行前照合の基準はC274 medium再計測`0dfec297f0fe4d5f9d2d38fb2fff154e`。その固定Layer 1を再利用し、プロンプト以外の全互換条件一致を確認してから発行した。今回の時間記録条件のFree mediumプールは既存0件で、不足70件だけを固定した。

Free bundle、Astra、CLI 0.153.3、Python 3.14.5、Rating v14、全エージェントトークン集計v1、時間記録r1、並列上限24、ケース・fixture・TaskSpecを保持した。low・medium・highのプロファイルの条件差は推論設定だけである。条件ごとに別プールへ登録し、推論設定間の数値差をプロンプト変更の効果として扱わない。

個別runの登録、選択集合の固定、集計result登録、証拠の検証付き圧縮保存まで完了した。生証拠はローカルの`control-free-astra-medium-remeasure-standard14-n5-cli0153-20260908-r1`に保持する。

正式な作業時間は入力配送境界と時計対応が未観測のため欠測とする。9月5日のFree mediumは時間記録条件が異なるので、この3条件の互換比較へ混ぜない。実行時刻やサービス状態も異なり、N=5の観測だけで推論設定の一般的な優劣を確定しない。

## 一次資料

- [3条件の集計と減点記録](control-free-astra-low-medium-high-standard14-n5_2026-09-08.json)
- [mediumプロファイル](../profiles/control-free-astra-medium-remeasure-standard14-n5-cli0153-r1.json)
- [先行するhigh・lowの計測](control-free-astra-high-low-standard14-n5_2026-09-08.md)

後続の[A01分析と説明の訂正](../../docs/astra-free-a01-reasoning-route-audit-r1.md)で、現状テストと推測による編集を区別した。`a01_final_drift`は応答文面ではなく、実際のファイル変更を指す。
