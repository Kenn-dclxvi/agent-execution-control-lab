# Candidate91 concise output ingress設計

## 結論

Candidate91はCandidate81を直接親とし、Candidate90で成立しなかった取得時projectionを147文字・2文の単一動作へ短文化する。TaskSpec、Evaluation set、fixture、oracle、required validation、rating、executor、model、reasoning、M / Nは変更しない。

既存F02 r1を`N=5`で実行し、まずinstruction complianceを判定する。5 / 5で取得時projectionが成立した場合だけ3 KPIを改善判断へ使う。

## 変更軸

Candidate90の649文字・8文には、observation fields、検索限定、byte閾値、success / failure分岐、再読条件、削除条件が同居していた。F02では5 / 5 score `4`を維持したが、取得時projectionは0 / 5だった。このresultは複雑な記述の失敗であり、prompt制御全般の失敗ではない。

Candidate91は次の一つだけを追加する。

> 出力上限を実行前に確定できないcommandは、stdout / stderrをrepository外の一時fileへ保存するwrapper内で実行する。modelへ返すのはexit codeと次の判断に必要な行だけとし、raw outputを直接返さない。

byte閾値、non-success分岐、一時file削除、再読条件、command別列挙は追加しない。既存C81のrequired evidence、fail-stop、validation closureは維持する。

## 評価と停止条件

1. 保存済みC81とCandidate91を、既存F02 r1、Rating v14、Medium、各`N=5`で比較する。
2. raw traceで、大出力が見込まれるcommandをrepository外の一時file wrapper内で実行し、raw outputを直接modelへ返さないrunをcompliantとする。
3. complianceが5 / 5なら、quality、all-agent token、elapsedの3 KPIをC81と比較する。
4. complianceが4 / 5以下なら`instruction_not_reliable / stopped`とし、prompt文面の追加改訂を重ねない。次の判断候補をexecutor側wrapperとする。
5. 5 / 5 score `4`でない場合も停止する。
6. F04、標準14、採用、release、本体反映は本試験では実施しない。

## 状態境界

candidate bundleとprofile作成時点は`draft / not_evaluated`だった。後続の[`F02 N=5 result`](../evaluations/results/candidate81-candidate91-concise-output-ingress-v14-medium-f02-n5_2026-07-29.md)は5 / 5 score `4`だったが、strict compliance 2 / 5、C81比token中央値`+5.90%`、elapsed中央値`+12.94%`だった。事前停止条件に従う現在状態は`targeted_f02_evaluated / stopped`である。
