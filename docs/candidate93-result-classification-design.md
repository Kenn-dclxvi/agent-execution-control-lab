# Candidate93 result classification設計

## 結論

Candidate93はCandidate81を直接親とし、最初にoutput routeとresult classを固定する。一律byte切断をやめ、`EXACT / STRUCTURED / NOISE`の3分類だけで意味保持と出力抑制を両立できるか、既存F02 r1を`N=5`で評価する。

TaskSpec、Evaluation set、fixture、oracle、required validation、rating、executor、model、reasoning、M / Nは変更しない。

## 3分類

- `EXACT`: source / diff / failure / unknown。判断に使う該当範囲を改変せず返す。
- `STRUCTURED`: search / test / status / API。exit code、件数、path、line、symbol等の機械fieldを返す。
- `NOISE`: progress / repetition。modelへ返さない。

完全rawはrepository外の一時fileに保存する。分類不能時は`EXACT`とする。一律byte cap、TaskSpec固有field、自由文semantic summaryは追加しない。

## Gate

5 / 5 score `4`、pre-command routeとresult classの固定、EXACT欠落0、STRUCTUREDへのraw流入0、NOISE返却0を要求する。分類成立5 / 5ならquality、all-agent token、elapsedをC81と比較する。4 / 5以下または両cost悪化なら停止する。

## 状態境界

bundleとprofile作成時点は`draft / not_evaluated`だった。後続の[`F02 result`](../evaluations/results/candidate81-candidate93-result-classification-v14-medium-f02-n5_2026-07-29.md)は分類機構0 / 5だったため、現在状態は`targeted_f02_evaluated / stopped`である。
