# Measurement Series: C02 Evidence Scope r1

## 目的

Candidate169の保存済みC02 Run Resultを基準とし、Candidate170で証拠取得の発行順と追加read条件だけを変えた1回の開発測定を行う。

## 固定条件

CaseはPRR-C02/r2、関係レビュー役はOpus 1人、rootは`claude-sonnet-5`とする。fixture、repository snapshot、authority、review contract、rating、権限、Action revision、timeout、token accountingを基準Run Resultと一致させる。基準runは再実行しない。

finding採用条件とmodel-visible情報は変えない。変更するのは、7件の既知の独立readを最初のtool-use stepで共同発行し、全result受領後に一度だけ判定し、未確定の判定を動かせない追加readを閉じる制御だけである。

## 観測

3 KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`とする。mechanism診断として、fixture-tool access総数、fixture-toolを含むbatch数、最大batch size、7件の初回共同発行、追加readの有無を保存する。

測定成立とmechanism成立を分ける。構造化結果、model、token、elapsed、1人のOpus関係レビュー役、read-only境界が成立すれば測定は成立する。mechanismは、7件のfixture-tool readが同じbatchで観測され、完全な固定packetに対する追加readが0件の場合に成立する。quality scoreはKPIであり、測定前の合否閾値にしない。

## 解釈境界

C02/r2は結果確認済みの開発用Caseである。このRun Resultはreview evidence schedulingのtargeted mechanismと3 KPIだけを示し、C147の数値効果転用、fresh held-out効果、一般化、model ranking、採用、release、本体反映を示さない。
