# Candidate109 validation実行票outer wait closure設計

## 結論

Candidate109はCandidate108を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

Candidate108の実行票全体のterminal wait-only遷移はfallbackとして維持する。通常経路ではvalidation wrapperのouter yieldをruntimeが一回で待てる最大値へ固定し、意図的な短時間yieldによるmodel再入を閉じる。

## Identityと状態

- candidate number: Candidate109
- prompt identity: `the-caption-3ce91a4-validation-ticket-outer-wait-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- bundle SHA-256: `fe39d4f66f981f0be35fe20dcf53562cf06dc00442dfc909895e3dcd10fc8c0d`
- evaluation status: `targeted_f03_evaluated / quality_gate_passed / terminal_before_reentry_passed / cost_both_lower / prompt_design_boundary_failed / result_registered / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate108とする。
2. 基準状態での最短正常経路は、全required validationと完了確認を一つのwrapperへbindし、wrapperがterminal resultを一回で返し、全result受領後に一度だけ完了を判断する経路とする。
3. 保存済み誤経路はCandidate108 Standard14 N=5とする。command protocol対象35件中12件がouter yield `1000ms`を選び、12 / 12件がcell ID付きnonterminal resultを返した。
4. 全70 runではCandidate107の3回に対してCandidate108は23回の`wait`を発行した。C108 minus C107の70 run合計token増分`1,176,155`のうちinput tokenは`1,172,806`で、増分の99.7%だった。
5. Candidate108のterminal wait-only fallbackは23 / 23件で成立したため削除しない。既存TaskSpecとrepository authorityはouter yieldの選択を固定せず、Candidate108はearly yield自体を非目標にしたため`1000ms`を防げない。
6. 置換するpredicateは`VALIDATION_PLAN`一つとする。変更軸はouter yield選択の固定とする。
7. 消す判断点は、実行票完了前に返却するための短時間outer yieldを選ぶ分岐である。
8. 新たに増える判断点はない。outer yieldはruntimeが一回で待てる最大値へ固定する。runtime上限によるnonterminal返却だけをCandidate108と同じwait-only fallbackへ渡す。
9. F03 r2、Rating v14、Medium、N=5で、score `4`、required command evidence、required validation一実行票、意図的な短時間outer yield 0、途中message 0、required validation再実行 0を確認する。
10. qualityまたはmechanism条件が5 / 5で成立しなければ停止する。成立時は保存済みCandidate108 F03 N=5と3 KPIを比較し、tokenまたはelapsedのどちらかが高ければStandard14へ進めず停止する。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindする。検証success後はmodelへ戻らず実行票の残りを発行し、
全result受領後に一度だけ完了を判断する。実行票完了後はTaskSpec追加要求またはresult失効がない限り
toolを追加しない。validation wrapperのouter yieldはruntimeが一回で待てる最大値へ固定し、実行票
完了前の返却を意図した短時間yieldを指定しない。runtime上限によってcell ID付きnonterminal resultが
返った場合、その返却を実行票の完了判定へ使わず、実行票全体がterminalになるまで同じcell IDへの
waitだけを発行する。commentary / 進捗報告 / 判断 / 別toolを先に発行しない。
```

## 非目標

- executorのruntime上限変更
- nonterminal result自体の全面禁止
- validation以外の長時間command制御
- TaskSpec、required validation、evaluation set、fixture、ratingの変更
- commandのshell compound化
- Candidate108の評価履歴の変更
- 採用、release、THE-CAPTION本体反映

## 最初の試験

- case: F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- reference: Candidate108の保存済みF03 N=5

## 評価結果と現在状態

F03 N=5は5 / 5 score `4`で、terminal前model再入、途中message、required validation再実行は0件だった。保存済みCandidate108比はtoken中央値`-15.97%`、elapsed中央値`-16.43%`だった。

ただし、後続の設計原則再確認で、outer yieldの最大値という実行方法をpromptへ指定した変更軸自体が不適切と判断した。数値結果は診断証拠として保持し、現在状態を`targeted_f03_evaluated / quality_gate_passed / terminal_before_reentry_passed / cost_both_lower / prompt_design_boundary_failed / result_registered / stopped`とする。

詳細は[`Candidate108 / Candidate109 F03 atomic N=5結果`](../evaluations/results/candidate108-candidate109-validation-ticket-outer-wait-closure-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md)を正本とする。
