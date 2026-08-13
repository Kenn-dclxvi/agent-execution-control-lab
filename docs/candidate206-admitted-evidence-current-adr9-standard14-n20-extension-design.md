# Candidate206 ADR9・Standard14累積N=20延長設計

## 結論

Candidate206の低頻度品質・機序とKPIを確認するため、既存N=5 atomic runを再利用し、ADR9とStandard14を順に各ケース累積N=20へ延長する。prompt、case、TaskSpec、fixture、rating、model、reasoning、runtime、permission、executor条件は変更しない。

## 発行順と範囲

1. ADR9は既存5件×9ケースを再利用し、不足15件×9ケース、合計135件だけを発行する。
2. ADR9累積180件が全件Score 4で、既存のreview cardinality、forbidden canary、変更admission、root instruction再取得0件を維持した場合だけStandard14へ進む。
3. Standard14は既存5件×14ケースを再利用し、不足15件×14ケース、合計210件だけを発行する。
4. Standard14累積280件が全件Score 4、command protocol違反0、monthly numeric location exact、root instruction本文再取得0件、必要なpath-local instruction取得維持を通過条件とする。

## 互換preflight

comparison preflightには保存済みN=5 resultとN=5 profileを使う。atomic N延長では、発行対象は`plan-missing --desired-count 20`が固定する不足slot集合であり、累積N=20 profileは最終selection resultのcoverageへ使う。N=20 profileをN=5 Layer 1のpreflightへ直接使わない。

## KPIと停止条件

- ADR9とStandard14それぞれで、累積N=20のCandidate206を同じ条件の保存済みCandidate175 N=5と比較する。ただしN差があるためKPI差をpairedまたは同一Nの因果値とは扱わず、安定性の記述値とする。
- Candidate206 N=5との比較では、累積selectionの中央値変化を記述し、追加15件で旧判断が反転するかを確認する。
- 一件でもScore 4未満、required reviewer欠落、不要review、禁止情報配送、未admit変更、root instruction本文再取得、必要な局所instruction取得欠落または計測不能があれば、その段階のvalid resultを保持して停止する。
- 全件合格でも、tokenとelapsedの両方が改善しない限り、既存の`optimization_failed_stopped`を採用へ変更しない。KPI重みを事後に導入しない。

## 非目標

- prompt変更またはCandidate207作成
- Candidate175の採用、releaseまたはprojection
- Candidate206の採用判断をN=20実行前に変更すること
- TPO、他case、他Evaluation setの追加
- executor、runtime hookまたは外部wrapperの変更
