# Candidate105 検証実行票のterminal返却設計

## 結論

Candidate105はCandidate104を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

検証実行票を一回のcustom exec wrapperへ固定した後、意図的な短時間yieldでprogress resultだけをmodelへ返す経路を閉じる。runtime上限がnonterminal resultを返した場合も、新しい判断、進捗報告、plan更新、別toolを挟まず、同じwrapperまたはsessionのterminal result受領だけを継続する。

## Identityと状態

- candidate number: Candidate105
- prompt identity: `the-caption-3ce91a4-validation-terminal-return-r1`
- direct parent: `the-caption-3ce91a4-staged-evidence-admission-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- bundle SHA-256: `6eaf12cd58e26244d514a34f4a9238d217058a3b178f138ea3551e930a496aa5`
- evaluation status: `targeted_f03_stopped_gate_user_reopened_for_standard14 / standard14_evaluated / quality_gate_passed / terminal_return_improved_not_complete / result_registered / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate104とする。
2. 最短正常経路は、変更後にfocused validation、full validation、必要なdiff / statusを一つのcustom exec wrapperで順に実行し、terminal resultを一度受領して完了を判断する経路とする。
3. Candidate104 Standard14 F03 N=5では、model stepが`5 / 5 / 6 / 7 / 7`、all-agent tokenが`112,196 / 128,410 / 149,536 / 190,526 / 192,530`だった。
4. 上位2件は外側custom execへ一秒のyieldを指定し、nonterminal result受領後にfocused進捗報告、wait、full進捗報告または追加status確認へ進んだ。full validation自体は進捗報告より前に開始済みであり、required command順序の誤りではない。
5. TaskSpec、repository authority、required validation、既存`VALIDATION_CLOSURE`はrequired command集合と発行順を固定するが、実行票がterminalになる前の意図的な外側yieldを直接禁止しない。
6. 置換するpredicateは`VALIDATION_PLAN`一つとし、一回のwrapper、terminalまでの意図的なprogress返却禁止、runtime強制返却時の同一session待機だけを追加する。
7. 消す判断点は、nonterminal validation result受領後の進捗報告、plan更新、別tool選択、完了判断である。
8. 新たに増える判断点は、受領resultがterminalかnonterminalかというmachine-boundな一つだけである。
9. F03 r2、Rating v14、Medium、N=5で成果品質と狙った経路を確認する。score、TaskSpec、fixture、required command、permission、model、reasoning、CLI、executor parameterはCandidate104の互換条件から変えない。
10. score `4`、required command evidence、検証実行票の一回wrapper、意図的なnonterminal yield 0、validation中の進捗message 0、実行票後の追加tool 0のいずれかが5 / 5で成立しなければ停止する。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindし、一回のcustom exec wrapperで実行する。
wrapperはbind済みcommandのstop conditionを内部で判定し、実行票全体が
success / failed / unavailableのいずれかへterminalになるまで、意図的な短時間yieldで
progress resultだけをmodelへ返さない。各commandは個別invocationのまま維持し、
shell compound commandへ結合しない。runtime上限によりnonterminal resultが返った場合は、
commentary / plan更新 / 別tool / 完了判断を挟まず、同じwrapperまたはsessionのterminal result受領だけを継続する。
全resultを一度だけmodelへ返し、TaskSpec追加要求またはresult失効がない限りtoolを追加せず完了を判断する。
```

## 非目標

- TaskSpec、required validation、evaluation set、fixture、ratingの変更
- commandのshell compound化
- tool resultのtruncation、raw log保存、compact receipt、executor hookの変更
- validation以外の長時間commandまたはprogress報告の一般制御
- token、message、tool callへの固定上限
- Candidate104の評価resultまたはmanifestの書換え
- 採用、release、THE-CAPTION本体反映

full gate出力のtruncationによって実行票末尾のstatusが見えなくなる問題は、tool result配送の別軸である。Candidate105へ混ぜない。

## 最初の試験

- case: F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- 実際の同時実行数: 最大5件。profileの`M`は変更しない
- Candidate104: 新規実行しない。互換な保存済みF03 N=5を比較基準へbindする

targeted candidate resultだけを先に発行し、quality・mechanism gateの全条件を5 / 5で満たした場合だけ、保存済みCandidate104とのKPI比較またはStandard14を別途判断する。

## 評価結果

F03 r2 N=5は5 / 5でscore `4`だった。意図的なnonterminal yieldとvalidation中の進捗messageは0 / 5だったが、1件が実行票内の許可path判定を誤り、terminal failure後に第2wrapperでrequired validationを完了した。一回wrapperと実行票後toolなしは4 / 5である。

作成前の停止条件に従い、targeted評価時点ではCandidate105を`stopped`とした。その後、ユーザーがStandard14評価だけを明示的に再開した。Standard14 N=5は70 / 70 score `4`で、F03の検証後再取得なしはCandidate104の2 / 5から4 / 5へ改善したが、1件はtool result truncation後にdiff / statusを再取得した。集約中央値はC104比token `+0.70%`、elapsed `+2.65%`である。

現在状態は`targeted_f03_stopped_gate_user_reopened_for_standard14 / standard14_evaluated / quality_gate_passed / terminal_return_improved_not_complete / result_registered / adoption_not_decided`とする。targeted結果は[`Candidate105 Rating v14 Medium F03 N=5`](../evaluations/results/candidate105-validation-terminal-return-v14-medium-f03-n5-cli0146_2026-07-30.md)、正式比較は[`Candidate104 / Candidate105 Standard14 N=5`](../evaluations/results/candidate104-candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146_2026-07-30.md)を正本とする。B20、採用、release、本体反映は未実施・未判断である。
