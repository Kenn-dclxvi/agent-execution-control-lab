# Portable semantic heldout r3 N=5比較結果

> [!IMPORTANT]
> **状態**: `completed / compatible / c147_score4_69_of_70 / portable_score4_70_of_70 / portable_token_sum_regression / portable_elapsed_sum_improvement / adoption_not_decided`

## 結論

同じheldout r3と実行条件で、C147 referenceとportable full-agent r1を各Case N=5まで拡張した。既存N=1の14 runをi001として再利用し、i002〜i005の56 runだけを新規発行した。

portableは70 / 70でScore 4・機序成立を維持した。C147は`PIC-H17-i002`で必要なread開始を`unavailable`へ誤分類し、69 / 70に留まった。有効な低品質runなので再実行せず保存した。

効率はN=1と同様に一方向の改善ではない。portableはC147よりtoken合計が2,322（0.204%）多く、対応runでも56 / 70件で多かった。一方、elapsed合計は24.812秒（3.596%）短く、43 / 70件で短かった。token中央値だけは2少ないが、対応差の中央値は+42 tokenであり、token削減とは判定しない。

| 指標 | C147 | portable | portable - C147 |
| --- | ---: | ---: | ---: |
| Score 4・機序成立 | 69 / 70 | 70 / 70 | +1件 |
| token中央値 | 16,314.5 | 16,312.5 | -2.0 |
| token合計 | 1,135,937 | 1,138,259 | +2,322 |
| 対応token差の中央値 | — | — | +42.0 |
| elapsed中央値 | 10.033秒 | 9.984秒 | -0.048秒 |
| elapsed合計 | 689.955秒 | 665.143秒 | -24.812秒 |
| 対応elapsed差の中央値 | — | — | -0.376秒 |

## 外部失敗の扱い

初回の同時発行中に、C147で25件、portableで23件の接続側`429 Too Many Requests`およびWebSocket `403 Forbidden`が発生した。これらは`excluded_external_failure`として保持し、初回成功runを再実行せず、失敗した同一slotだけを低並列の別attemptで再発行した。再発行は全件成功した。除外attemptのtokenとelapsedはKPIへ混ぜていない。

## 境界

- portable prompt、C147 prompt、TaskSpec r4、heldout r3、oracle、rating、model、reasoning、permission、token accountingは変更していない。
- N=1 resultは上書きせず、N=5 resultからhashで参照する。
- C147の1件の失敗はportableの優位性を一般化する根拠ではない。今回の70 run内で観測した品質差として扱う。
- elapsed短縮とtoken増加が併存するため、総合的なcost改善や採用は未判断である。

## 正本

- [`C147 N=5 result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-reference-heldout-r3-n5-qualification-r1.json)
- [`portable N=5 result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-portable-full-agent-heldout-r3-n5-qualification-r1.json)

N拡張は完了した。後続の正本は[`N=20比較結果`](portable-semantic-heldout-r3-n20-comparison-result.md)とする。
