# Candidate92 bound output route設計

## 結論

Candidate92はCandidate81を直接親とし、最初のcommand前にoutput routeを固定する。repositoryのread / search / diff / validationを一時file wrapper内だけで実行し、success時のmodel-visible command outputを4096 bytes以下へ固定する。

TaskSpec、Evaluation set、fixture、oracle、required validation、rating、executor、model、reasoning、M / Nは変更しない。既存F02 r1を`N=5`で評価する。

## 根拠

Candidate91ではwrapperを一度以上使うrunが4 / 5へ増えた。最初のcommandをwrapperで開始したrunは後続でもwrapperを使い、最初に直接実行したrunは完全適用へ戻らなかった。

失敗差は二つあった。第一に「出力上限を確定できないcommand」という条件が、固定範囲の`sed`やpath限定済み`rg`を直接実行する余地を残した。第二に「必要な行だけ」に機械上限がなく、wrapper使用runでも最大約22,000〜27,000 bytesを返した。

Candidate92はcommandごとの上限推定を行わない。repository read / search / diff / validationへ同じrouteを適用し、success resultの4096 bytes上限をraw eventから機械判定する。

## Prompt変更

> 最初のcommand前に`output_route=temporary_file`を固定する。repositoryのread / search / diff / validationはrepository外の一時fileへ保存するwrapper内だけで実行し、success時にmodelへ返すcommand outputを4096 bytes以下にする。

Candidate81の既存labelは変更しない。non-success分岐、case固有command、shell template、出力内容の推定は追加しない。

## Gate

1. 既存F02 r1、Rating v14、Medium、`N=5`で実行する。
2. 対象commandのwrapper route成立とsuccess result 4096 bytes以下をraw eventで判定する。
3. routeと上限が5 / 5 runで成立し、5 / 5 score `4`なら、quality、all-agent token、elapsedをC81と比較する。
4. routeまたは上限が4 / 5以下、またはscore `4`が5 / 5未満なら停止する。
5. F04、標準14、採用、release、本体反映は本試験では実施しない。

## 状態境界

candidate bundleとprofile作成時点は`draft / not_evaluated`だった。後続の[`F02 N=5 result`](../evaluations/results/candidate81-candidate92-bound-output-route-v14-medium-f02-n5_2026-07-29.md)は5 / 5 score `4`、pre-command route 5 / 5、4096 bytes cap 3 / 5、C81比token中央値`+51.00%`、elapsed中央値`+28.89%`だった。現在状態は`targeted_f02_evaluated / stopped`である。
