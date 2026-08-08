# Control-Free 4ケース資格確認 r1

## 目的

新インスタンスの正式な比較へ進む前に、レビュー方法をモデルへ委ねるcontrol-free baselineが、現行仕様へ適合した既存4ケースすべてでquality score `4`を返すか確認する。この実行はfixtureと実行経路の資格確認であり、レビュー体制の優劣や採用を測らない。

## 固定条件

- 対象は`PRR-C02/r1`、`PRR-C03/r1`、`PRR-C05/r1`、`PRR-C06/r1`の各1反復とする。
- root modelは`claude-sonnet-5`とし、review方法、subagent使用、担当分割、モデル役割は固定しない。
- model-visible入力は各caseの`input.json`と`review-contract-r1.md`だけとし、oracleとgraderをreview jobへ渡さない。
- 4スロットは相互に独立しており、設定上の`max_workers`は`24`、実際のdispatch concurrencyは`4`とする。
- 正式KPIはquality score、all-agent total tokens、elapsed secondsの3件とする。ただし資格確認の合否はquality scoreだけで決める。

## 合否

各runは構造化出力、要求model、全agent token、経過時間、fixture access、権限拒否0件が揃った場合だけ測定成立とする。4ケースすべてがscore `4`なら新インスタンスのcontrol-free品質条件を満たす。一件でもscore `4`未満なら比較へ進まず、fixture、実行環境、ケース定義を切り分ける。

この4ケースは資格確認に使うためheld-out evidenceではない。次のレビュー体制比較には、資格確認結果を見た後に作るケースも含めず、別に固定した未使用ケースを使う。
