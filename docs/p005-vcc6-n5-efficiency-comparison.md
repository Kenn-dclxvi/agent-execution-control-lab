# P005 VCC6 N=5効率比較

> [!IMPORTANT]
> **結果**: `90/90 valid / P005 Score 4 x30 / mechanism 30/30 / P003比2 KPI改善 / P001比elapsed増 / Standard14不許可`

## 結論

P005は、同じ品質と機序を満たしたP003より効率がよい。tokens合計を1.44%、elapsed合計を5.72%減らした。

一方、直接親P001との比較ではtokens合計を14.50%減らしたが、elapsed合計は18.40%増えた。作成前に固定した停止条件は「P001比でtokensまたはelapsedの一方が増えたら停止」であるため、P005はVCC6 N=5 cost gate不通過とする。Standard14、N=20、採用、releaseおよびtarget本体へのprojectionへ進まない。

## 比較条件

- arm: P001、P003、P005。
- 各arm: VCC6 6 Case x 5反復、30 fresh slot。
- 合計: 90 fresh slot、保存済みresult再利用なし。
- 同一条件: Case、fixture、TaskSpec、oracle、rating、model、reasoning、Codex CLI、permission、runner bytes、token accounting、集計方法および`max_workers=24`。
- 実験変数: prompt identityだけ。
- P004はN=1品質gate不通過のため比較armに含めない。

## arm集計

| arm | valid | Score 4 | 機序成立 | tokens合計 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| P001 | 30 / 30 | 26 / 30 | 6 / 30 | 1,876,743 | 853.354秒 |
| P003 | 30 / 30 | 30 / 30 | 30 / 30 | 1,628,157 | 1,071.649秒 |
| P005 | 30 / 30 | 30 / 30 | 30 / 30 | 1,604,686 | 1,010.334秒 |

P001の低いelapsedは、validation carrier機序を24 / 30件で満たしていない状態を含む。したがってP005のP001比elapsed増は、同じ機序をより遅く実行した差だけではなく、P001が実行しなかった制御効果をP005が取得する費用も含む。それでも固定済みgateは変更せず不通過とする。

## P003から得た改善

P005はP003と同じく30 / 30件でScore 4・機序成立を維持しながら、次を減らした。

- tokens: 23,471減、1.44%減。
- elapsed: 61.315秒減、5.72%減。

case別ではH01とH02がP003より増え、H03からH06までが減った。したがって全Case一様な短縮ではなく、terminal projection ownershipによって後半Caseのraw result処理と再推論が減った集計効果である。

## P001との差と停止

P005はP001よりtokensを272,057減らしたが、elapsedは156.980秒増えた。品質と機序を維持したまま両KPIをP001未満にする目的は未達である。

P005へ条件を追加して同じCandidateを再実行しない。P001を直接親として保持し、P002からP005までをそれぞれ異なる失敗routeまたは費用反例として次の一差分検討へ渡す。
