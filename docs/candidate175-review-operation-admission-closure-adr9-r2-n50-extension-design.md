# Candidate175 ADR9 r2累積N=50延長設計

## 結論

Candidate175の低頻度品質・機序を確認するため、保存済みADR9 r2 N=5 atomic runを再利用し、各ケース累積N=50へ延長する。prompt、case、TaskSpec、fixture、rating、model、reasoning、runtime、permissionおよびexecutor条件は変更しない。

本延長はCandidate175の採用、releaseまたはprojectionを判断しない。N=5で成立したreview operation仕様、専用producer bindingおよびallow-list semantic projectionが、累積N=50でも品質と機序を保持するかだけを記録する。

## 発行範囲

1. 保存済みCandidate175 N=5 result `eba0a4bc1d0e4391afa631462b8daccb`と、そのatomic poolに登録済みの5件×9ケースを再利用する。
2. `plan-missing --desired-count 50`が固定する不足45件×9ケース、合計405件だけを発行する。
3. 累積450件を固定rating contractで採点し、品質、review cardinality、terminal、artifact effect、禁止情報配送およびread機序を監査する。
4. validな低品質runまたは機序不通過runは再試行で消さず、そのまま累積resultへ含める。

## 互換preflight

発行preflightは保存済みN=5 result、N=5 profileおよび保存Layer 1へbindする。累積N=50 profileは最終selection resultのcoverageにだけ使う。

prompt identity以外のEvaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor条件、target commitおよびtreeが一項目でも不一致、未固定または未確認なら、一件も発行しない。preflight receiptは承認405件・発行0件を要求する。

## 判定

- 品質は450 / 450 validかつScore `4`を合格条件とする。
- review cardinalityは、ADR03〜ADR07およびADR09の300 / 300でrequired reviewerが一回起動し、ADR01、ADR02およびADR08の150 / 150で起動しないことを要求する。
- ADR06の禁止canary配送、未admit artifact変更、terminalまたはresult effect不一致を各0件とする。
- projected counterexample certificate成立後の不要read、reviewer closed-source再読およびroot prereadを、保存済みtraceへ適用済みの定義と同じ単位で計数する。最終resultが正しくても、consumerを持たないreadは機序不通過として保持する。
- KPIは累積N=50の`quality_score`、all-agent `total_tokens`および`elapsed_seconds`を記述する。N=5との差はpaired因果値として扱わない。

## 停止条件

- preflight不一致、予定外slot、valid coverage不足または採点不能。
- Score `4`未満、required reviewer欠落、不要reviewer、禁止情報配送、未admit変更またはterminal/result effect不一致が一件でもある。

停止条件に達しても、発行済みvalid runとその失敗は削除または再実行しない。追加Candidate、Standard14、採用、releaseおよびruntime projectionへ自動接続しない。
