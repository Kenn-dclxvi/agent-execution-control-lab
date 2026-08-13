# Candidate208 ADR9・Standard14累積N=50延長設計

## 結論

Candidate208の低頻度品質・機序とKPIの安定性を確認するため、既存N=5 atomic runを再利用し、ADR9とStandard14を順に各ケース累積N=50へ延長する。prompt、case、TaskSpec、fixture、rating、model、reasoning、runtime、permission、executor条件は変更しない。

ADR9 N=5で観測済みのADR05不要read 1件とADR09 root preread 1件は、N=50でも同じ定義で監査する。Standard14 N=5は明示的なリスク受容により既に実施済みだが、N=50延長でもADR9結果を先に確定する。

## 発行順と範囲

1. ADR9は既存5件×9ケースを再利用し、不足45件×9ケース、合計405件だけを発行する。
2. ADR9累積450件を固定rating contractで採点し、品質と既存機序を再監査する。
3. ADR9の結果を保存した後、Standard14は既存5件×14ケースを再利用し、不足45件×14ケース、合計630件だけを発行する。
4. Standard14累積700件を採点し、command protocol、monthly numeric locationおよび通常経路の診断値を確認する。

## 互換preflight

各系列のcomparison preflightには保存済みN=5 result、N=5 profileおよび保存Layer 1を使う。atomic N延長の発行対象は`plan-missing --desired-count 50`が固定する不足slot集合であり、累積N=50 profileは最終selection resultのcoverageへ使う。

prompt identity以外の互換条件が一項目でも不一致、未固定または未確認なら、その系列では一件も発行しない。preflight receiptはADR9で承認405件・発行0件、Standard14で承認630件・発行0件を要求する。

## 判定

- 品質はADR9 450 / 450、Standard14 700 / 700のScore 4を合格条件とする。
- ADR9機序はreviewer cardinality、result kind admission/effect、artifact境界、packet反例成立後read、packet供給元再読およびroot prereadをN=5と同じ定義で監査する。
- Standard14機序は固定quality contractのcommand protocolとmonthly numeric locationを判定し、owner/producer evidenceは`diagnostic_only`のまま保持する。
- KPIは累積N=50の品質中央値、全agent token中央値、経過時間中央値を各系列のN=5結果と比較する。N差があるためpaired因果値とは扱わない。

## 停止条件

- preflight不一致、予定外slot、valid coverage不足または採点不能。
- ADR9でScore 4未満、required reviewer欠落、禁止情報配送、未admit変更、terminal/result effect不一致が一件でもある。
- Standard14でScore 4未満またはcommand protocol違反が一件でもある。

validな低品質runや既知の機序残差は再実行で消さず、累積resultへそのまま含める。採用、releaseおよびruntime projectionは本延長の自動効果にしない。
