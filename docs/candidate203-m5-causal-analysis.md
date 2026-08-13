# Candidate203 M5原因分析

## 結論

Candidate203の不通過は二つの独立した実経路に分かれる。

第一に、`PRECHANGE_REVIEW`は明示review operationだけを許可したが、「設計を確認する」というroot自身の作業とTaskSpecが要求する独立review operationを、tool-call発行時の選択へ結び付けなかった。このためADR01で5 / 5、ADR02で3 / 5の不要reviewer起動が発生した。C192以降で観測した抽象的なadmission predicateと実際のproducer選択の未接続が、別表現で再発した。

第二に、`REVIEW_READ_TRANSITION`はprojection certificate成立時のread禁止を明示したが、reviewerがprojectionの内容を受け取った後に、counterexample判定と`exec`選択を不可分な一遷移として実行することを保証できなかった。ADR05の2 / 5では投影済みclosed sourceとdirect targetを同じreadへ混ぜ、2 / 20のpriority violationになった。

## C202から改善した点

counterexample成立20件のdirect read違反はCandidate202の9件からCandidate203の2件へ減った。projection-first記述は挙動へ影響した。しかし固定gateは0件であり、減少を通過として扱わない。

また、required reviewerは30 / 30、routing completeは30 / 30、root先読みなしは30 / 30、必要direct observationは10 / 10を維持した。品質も45 / 45 Score 4だった。これらは成立した独立predicateとして保持し、不通過predicateと一括失効させない。

## C175正常対照との差

Candidate175は同一ADR9条件でrequired reviewer 30 / 30、review不要時0 / 15、45 / 45 Score 4を成立させた。Candidate203はC147の直接childを維持した一方、C175が一つのreview operation closure内に持っていた「必要時だけ起動する」実発行境界を再構成できず、review不要時8 / 15で起動した。

C175を次Candidateの親にはしない。成功したreview applicabilityの具体的traceと、Candidate203の8件および2件を反例として使い、C147直接基盤から再設計する必要がある。

## 次案の制約

次案を作る場合も、review applicabilityとprojection-first direct readの二つを同時に文言追加して直さない。今回の失敗は二軸に分かれたため、まずreview不要時のproducer発行をC147の既存`PRODUCER` / `OWNER_ROLE`へ接続する一軸を反証し、その後も2 / 20が残る場合にだけread遷移を別軸として扱う。

Candidate203は`quality_passed / mechanism_failed / stopped`として保持する。Standard14を実行せず、採用、releaseおよびprojectionを行わない。

`M5_complete / quality_preserved / applicability_failed_8_of_15 / projection_priority_failed_2_of_20 / Candidate147_direct_base_retained / Standard14_not_started / stopped`
