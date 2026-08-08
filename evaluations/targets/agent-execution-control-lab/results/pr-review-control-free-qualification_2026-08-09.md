# PRレビュー Control-Free資格確認

## 結論

現行仕様からoracleを導出できるPRR-C02/r1とPRR-C03/r1は、同じcontrol-free条件で測定が成立し、どちらもquality score `4`だった。この2ケースから成る最小setについて、新インスタンスのcontrol-free品質条件を満たした。

PRR-C05/r1とPRR-C06/r1はモデル品質の失敗として扱わない。C05ではmodel-visibleな`single_artifact_unit`違反をoracleが欠き、C06では参照先を読めないのに`document_quality: pass`を要求していたため、いずれもcase不備として資格確認対象から除外した。

## 一次result

| case | GitHub run | 測定 | quality | all-agent tokens | review | execution |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| PRR-C02/r1 | [31276611327](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31276611327) | satisfied | 4 | 234,423 | 47.293秒 | 67.445秒 |
| PRR-C03/r1 | [31276612631](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31276612631) | satisfied | 4 | 342,225 | 45.947秒 | 60.673秒 |
| PRR-C06/r1 | [31276613765](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31276613765) | satisfied | 3 | 447,317 | 78.284秒 | 97.656秒 |

C06はfindingを返していないが、情報不足を正しく`unknown`としたため、graderとのsummary不一致でscore `3`になった。これはcase不備を示す診断resultであり、2ケースsetの集約へ含めない。

## 境界

この資格確認はfixtureと実行経路の最小品質条件を確認したものであり、関係レビュー役、Opus、Core Baselineとの比較結果ではない。使用したケースはheld-out evidenceではない。次の比較では、比較条件を実行前に固定したうえで、資格確認や校正に使っていないケースを用意する。
