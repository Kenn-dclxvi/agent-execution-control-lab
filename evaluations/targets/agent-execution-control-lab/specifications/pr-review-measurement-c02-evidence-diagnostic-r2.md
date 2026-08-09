# C170診断測定 r2

## 目的

保存済みのC170 Run Resultで、初回7件の共同read後に4件の追加readと、総token減少に対するreported cost増加を観測した。Candidate170のprompt本文、Case、model、権限、review contract、採点を変えず、追加readの操作種別と結果状態、および価格区分別tokenを内容非保存で観測する1回の診断測定を行う。

## 固定条件

CaseはPRR-C02/r2、関係レビュー役はOpus 1人、rootは`claude-sonnet-5`とする。Candidate170の正式なprompt identityと本文SHA-256を保持する。fixture、repository snapshot、authority、review contract、rating、権限、Action revision、timeout、既存のall-agent token accountingをC170の初回測定と一致させる。

変更するのは診断hook、collector、Run Result schema、workflow、Profileだけである。初回C170 Run Resultは再分類または上書きせず、診断の開始根拠として固定する。この診断resultをCandidate169との正式なKPI比較へ混ぜない。

## 内容非保存の診断値

fixture-toolについて、操作種別、成功・失敗・拒否、batch内の順序だけを保存する。引数、対象path、標準出力、標準エラー、review対象本文は保存しない。

tokenはroot、subagent、全agentについて、通常入力、cache作成入力、cache読取り入力、出力へ分ける。既存KPIのall-agent `total_tokens`は変更せず、価格区分別値はreported costの原因を分類する診断情報としてだけ扱う。

## 完了条件

測定成立、quality、3 KPI、mechanism状態は従来どおり保存する。追加で、11回のfixture-tool accessを操作種別と結果状態へ分類でき、4件の追加readが初回readの再発行、個別file取得、失敗回復のどれに当たるかを判断できることを診断完了条件とする。

この1回はC170の挙動診断であり、新しいCandidate、fresh held-out evidence、一般化、採用、release、本体反映を意味しない。
