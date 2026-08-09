# Candidate169

保存済みのC02 Opus Run Resultで観測した、規則一覧に存在しない`rule_id`の採用、categoryの取り違え、同じ違反の重複分割を一つの誤経路として扱い、最終findingの採用条件だけを置き換える開発用candidateである。正式なprompt identityは`pr-review-relationship-role-finding-admission-r1`である。

基準は`pr-review-relationship-role-r1:opus`である。関係レビュー役を1人・Opusに固定する構成、rootの役割、入力、権限、review contract、採点、測定方法は変えない。fixture-toolの呼出し回数を減らす制御や、C02固有の正解、対象path、oracleは追加しない。

C02/r2は結果確認済みのため、Candidate169の開発用固定ベンチマークとしてだけ使う。同じrevisionを新しいheld-out evidence、一般化、採用、release、本体反映の根拠にはしない。
