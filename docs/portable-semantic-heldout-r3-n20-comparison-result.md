# Portable semantic heldout r3 N=20比較結果

> [!IMPORTANT]
> **状態**: `completed / compatible / c147_score4_275_of_280 / portable_score4_280_of_280 / portable_token_regression / portable_elapsed_improvement / adoption_not_decided`

## 結論

同じheldout r3、TaskSpec r4、runtimeおよびprompt bytesのまま、C147 referenceとportable full-agent r1を各Case N=20まで拡張した。N=5の70 runを再利用し、i006〜i020の210 runだけを各条件へ追加した。

portableは280 / 280でScore 4・機序成立を維持した。C147は275 / 280で、`PIC-H17`の必要readを`unavailable`へ誤分類するrunが4件、`PIC-H22`で全selectorを誤って開始するrunが1件あった。有効な低品質runは再実行せず保持した。

効率の方向はN=5から変わらなかった。portableはtoken合計が10,195（0.225%）多く、対応runの230 / 280件で多かった。一方、elapsed合計は56.230秒（2.463%）短く、163 / 280件で短かった。このheldout r3 N=20内では、portableは時間を少し短縮するがtokenを少し増やす一枚であり、総合的なcost改善とは判定しない。

| 指標 | C147 | portable | portable - C147 |
| --- | ---: | ---: | ---: |
| Score 4・機序成立 | 275 / 280 | 280 / 280 | +5件 |
| token中央値 | 16,164 | 16,206 | +42 |
| token合計 | 4,535,959 | 4,546,154 | +10,195 |
| 対応token差の中央値 | — | — | +42 |
| elapsed中央値 | 7.650秒 | 7.560秒 | -0.090秒 |
| elapsed合計 | 2,283.263秒 | 2,227.033秒 | -56.230秒 |
| 対応elapsed差の中央値 | — | — | -0.185秒 |

新規i006〜i020だけでも、portableはtoken合計が7,873（0.232%）増え、elapsed合計が31.417秒（1.972%）減った。したがってN=5再利用部分だけが方向を作ったわけではない。

## Case分布

token合計がportable側で少なかったのは`PIC-H17`と`PIC-H24`の2 Caseだけで、残り12 Caseは増加した。elapsed合計がportable側で短かったのは9 Case、長かったのは5 Caseだった。特定内容の勝敗ではなく、固定instructionを毎run処理する効率分布として扱う。

## 外部失敗の扱い

初回発行では両条件に各6件の接続側WebSocket `403 Forbidden`が発生した。204件ずつの成功runは再実行せず、失敗した同一slotだけを各条件1並列で再発行し、全件成功した。除外attemptはresultへhash付きで保持し、そのtokenとelapsedをKPIへ混ぜていない。

## 境界

- portable prompt、C147 prompt、TaskSpec r4、heldout r3、oracle、rating、model、reasoning、permissionおよびtoken accountingは変更していない。
- N=1、N=5 resultは上書きせず、N=20 resultからN=5をhashで参照する。
- C147の275 / 280はexact quality gate不通過であり、C147が常に正解することを前提にしたsetではない。一方、同一固定条件の効率観測自体は対応runとして保持できる。
- portableの280 / 280を他のtarget、Standard14、採用、releaseまたはruntime projectionへ一般化しない。

## 正本

- [`C147 N=20 result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-reference-heldout-r3-n20-qualification-r1.json)
- [`portable N=20 result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-portable-full-agent-heldout-r3-n20-qualification-r1.json)
