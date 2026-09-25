# Candidate277 事前方針文の削除試験

## 目的と比較対象

Candidate276のroot `AGENTS.md` 5行目にある「作業開始前に必要な成果・対象・実施方法・維持条件を一つの方針にまとめる」という指示を一行だけ削除した直接子Candidateを作成し、GPT-6 Luna High・Standard14・N=5で計測する。主比較はCandidate276 result `9c659e7e0e0847beb97051fd23d92d94`とし、同じ14ケース×5回、同じ比較条件、同じLayer 1を使う。Control-Freeは既存の互換resultだけを参考比較へ再利用し、再実行しない。

Candidate identityは`the-caption-3ce91a4-execution-control-no-upfront-plan-r1`（Candidate277）とする。Candidate276 `the-caption-3ce91a4-execution-control-r1`（bundle SHA-256 `4d2dcd4f34749b32155139138654cbc2bb33b78fc6841ba6eb14d29c8f7a678f`）を直接の親とし、変更対象はroot `AGENTS.md`だけに限定する。3行目、6行目、7行目と、他の全target、case、fixture、TaskSpec、rating、runtime、token accounting、集計条件を保持する。

## 設計前の観測

Candidate276の保存traceでは、F01、F03、F07、F08、F10の確認対象runの冒頭に、作業方針または調査範囲を宣言するassistant messageが記録されていた。F08のshell command数は7〜16、F10は3〜11だった。一方で確認した作業は各TaskSpecの許可範囲内であり、Free側のrun-level traceがないため、冒頭の計画記述やケース別cost差を5行目へ因果帰属できない。

したがって、このCandidateは原因確定後の修正ではなく、「5行目が既存TaskSpecと重複する計画生成を要求し、追加costを生む」という利用者指定の仮説を、固定条件で検証する一要素削除試験とする。短文化だけを改善の根拠にせず、品質・all-agent `total_tokens`・`elapsed_seconds`を独立して確認する。

## 変更境界と維持する動作

- 削除するのはCandidate276 `files/AGENTS.md.txt` 5行目の一文だけとする。見出し、他の3規則、表記、改行および全targetの他ファイルを変更しない。
- Candidate276の最短正常経路として、TaskSpecでrequired outcomeとpermissionをbindし、必要なauthorityと対象だけを確認し、許可された作業とrequired validationを完了する動作を維持する。作業前の独立task分割、結果の対応付け、方針確定後の追加探索制限も維持する。
- 5行目が加えていた単一の全体方針記述を要求しなくする。代替のplanning指示、成功traceからの手順転記、例外条件、worker義務は追加しない。
- 狙う変化は、作業前の全体方針の明示とそれに伴う追加判断・出力コストの減少である。品質低下、required effect欠落、必須検証の省略、維持条件の不成立を許容しない。

## 評価と停止条件

- Candidate277だけを先行計測し、C276とControl-Freeを再実行しない。C276の保存済みLayer 1と同じ14ケース×5回を使用し、prompt identity以外の条件をpreflightで照合する。
- 比較の一次指標はquality score、all-agent `total_tokens`、`elapsed_seconds`とする。Score分布、valid / rateable、除外、計測エラーを併記する。計画記述・調査・tool呼び出しは原因診断に限り、独立した合否条件にしない。
- preflightで互換条件の不一致、未固定または未確認が一項目でもあればslotを発行しない。実行結果にinvalid、採点不能、required effect欠落または比較条件逸脱があれば、成功として集約せず実測状態を報告する。追加N、採用、release、runtime projection、本体反映へ進まない。
- 評価状態はCandidate登録、valid実行、quality、cost、trace機序、採用を分けて記録する。Candidate作成・評価だけで採用を意味しない。
