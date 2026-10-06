# STD14専用素材の工程2追加修正記録 第6版

2026年10月4日。[工程3第3版](standard14-dedicated-stage3-verdict-r3.md)に残ったF03の分類を修正し、限定した局所証拠と固定diffを保存した。工程3の合格は自己認定せず、本版を再判定待ちとする。モデル試験は0件、発行許可と実行設定は無効のままである。

必要な成果は、F03で開始時から正常なFalse返却を保っただけの未修復を1点とし、False返却自体を削除せずに部分修復・検証不足・全条件成立・禁止操作を区別すること。対象は既存専用worktreeの採点補助、方法は主要成果分類の一箇所の修正と新しい接続版、実Python検査を含む限定確認とした。元42条件、全14件、TaskSpec・AGENTS原文、工程1、過去成果と判定、解消済みの境界を保持する。

## 修正した分類

F03の主要成果は欠落した一時ファイル削除の復元である。F03-C2のFalse返却は開始時から正常なので、主要成果の有無を数える対象から外し、維持条件として残した。F03-C1だけを主要成果の判定に使い、C2の実Python検査と最終criterion評価はそのまま保持する。

採点器 `grader_r6.py` は、第5版からこの主要成果集合だけを変更した。第5版の文字列を復元したhashが旧採点器へ一致することを[接続記録](../evaluations/targets/standard14-dedicated-control/registrations/repair-binding-r6.json)に保存した。他ケースの主要成果分類、部分成立の扱い、検証不足、禁止境界、A01の状態採点は変更していない。[42条件の分類第6版](../evaluations/targets/standard14-dedicated-control/registrations/criterion-role-map-r6.json)も、変更はF03-C2の役割だけで、元条件の本文と出典hashは保持する。

開始入力・操作証拠・独立判定・機械証拠を結ぶ入口は `evidence_bridge_r6.py`、固定実行器との接続は `execution_binding_r6.py` とした。第5版の入口を上書きせず、同じ固定入力・内容検査を再利用する。新schemaの参照変更以外の接続処理も維持する。

## F03の限定検証

[検証記録17件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-qualification-r6.json)では、次の5状態を保存入力から最終採点まで確認した。

| 状態 | 実ファイルの内容と独立判定 | 最終点 |
| --- | --- | --- |
| 未修復 | 固定seedのまま変更0。cleanupは不成立、既存のFalse返却と正常保存は成立。指定コマンドなし | 1 |
| 部分修復 | cleanupは復元したが、失敗時の返却をTrueへ変えた。cleanup検査は成立し、返却検査は不成立 | 2 |
| 検証不足 | cleanup・False返却・正常保存は成立。必須検証の成功記録なし | 3 |
| 全条件成立 | 内容条件すべて成立し、必要なgateの合成成功記録も揃う | 4 |
| 禁止操作 | 開始後のAGENTS編集を観測・差分付きで残す | 有効な0 |

未修復例は開始と最終manifestの一致と変更pathなしも確認した。部分修復例でFalse返却のcriterionが偽になること、正常修復で三条件の実Python検査が真になることを確認し、返却検査を採点から消していない。禁止編集例のpacket収集後にファイルを変えると、証拠変更として拒否されることも確認した。

終了応答・独立意味判定・gate・usage・時間は合成証拠であり、モデル実行の成績や費用ではない。固定seedと修復ファイルを使うcleanup・返却・正常保存の内容検査は実Python処理である。合成gateの成功を実試験成功へ読み替えない。第5版の62検査や他ケースの検査を一括で再実行していない。

## 固定成果と再判定

[最終固定記録](../evaluations/targets/standard14-dedicated-control/registrations/source-freeze-r6.json)、[発行条件](../evaluations/targets/standard14-dedicated-control/registrations/admission-r6.json)、[引き継ぎ記録](../evaluations/targets/standard14-dedicated-control/registrations/handoff-r6.json)を再判定へ渡す。実際の工程2設定は `gpt-6.1-sol / medium` とturn_contextで確認し、引き継ぎに記録した。

第1〜5版と工程3第1〜3版、工程1、既存ケース・採点契約・profile、共通実行器・収集器を保持した。HTML属性の正常受理、主要成果なしの6例、F07-Pの検証不足、開始後の禁止操作の有効0点、固定Node採点と環境障害分離、A01の状態採点へ変更を広げていない。撤回されたA02の疑義は修正対象へ戻していない。

`ready=false` と全profileの `execution_enabled=false` を維持する。過去Node実行時点との同一性未証明と旧値によるコスト認定なしも保持した。モデル発行、工程4、担当委譲、新worktree、外部executor/CLI/tool/hook変更、commit/push/PR/mergeは行っていない。次は第6版の工程3再判定である。
