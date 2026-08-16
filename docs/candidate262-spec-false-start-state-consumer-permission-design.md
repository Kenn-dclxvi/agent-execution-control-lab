# Candidate262 未確定成果時の開始状態読み取りpermission閉鎖設計

## 結論

Candidate262はCandidate147を直接の基準にする。Candidate261は、TaskSpecへ固定した内部状態を利用者向け進捗として出力する経路を閉じたが、`spec_ready=false`でもTaskSpec明示の開始状態を直接観測できるpermissionを残した。このためA01では5件中1件で、未指定のmodeを質問する前にworkspace、branch、HEAD、clean状態を読み取った。

Candidate262は、`spec_ready=false`における開始状態の直接観測を、その結果が未固定のrequired outcome value、clarification resultのpermission、またはclarification operationのstop conditionを変え得る場合だけ許可する。結果を受け取る未完了の判断がないA01では開始状態を読むpermissionを閉じる。一方、開始状態によって質問の可否または停止条件が変わるTaskSpecでは観測を残す。

Candidate261の`SPEC`追加文は継承しない。成功runのcommand構成、読み取り順、読み取り回数、待機方法も追加しない。変更はCandidate147の`EVIDENCE_GATE`にある`spec_ready=false`時の一文置換だけとする。

## Identity

- candidate number: Candidate262
- prompt identity: `the-caption-3ce91a4-spec-false-start-state-consumer-permission-r1`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- changed target: root `AGENTS.md`
- changed axis: `spec_ready=false`時に、clarificationへ影響しない開始状態を直接観測できるpermission
- Candidate261の扱い: A01で残った1件とF03の費用増を示す失敗履歴。親または本文継承元にはしない
- evaluation status: `not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 1. 比較の基準と最短正常経路 | Candidate147。利用者が決めるrequired outcome valueが未固定なら、その値だけを質問してclarification operationをterminalにする。開始状態の結果が質問の対象、permission、stop conditionを変えない場合はrepository evidenceを取得しない |
| 2. 保存traceで確認した問題経路 | Candidate261 A01の1件は、workspace、branch、HEAD、clean状態を読み取ってから未指定modeを質問し、38,028 tokenを使った。他の4件はrepository commandなしで質問した。C147 A01にも同種の開始状態確認があり、Candidate261の出力禁止だけでは読み取りpermissionを完全には閉じなかった |
| 3. 問題を許した辺 | Candidate147の`EVIDENCE_GATE`は`spec_ready=false`でも`TaskSpec明示の開始状態の直接観測`を無条件に許可する。A01の開始状態resultは、未指定mode、質問permission、clarificationのstop conditionのいずれも変えないが、観測を受け取る判定がなくても発行可能である |
| 4. 変更する条件 | `spec_ready=false`時の許可文を置換し、TaskSpec本文は許可する。開始状態の直接観測は、そのresultが未固定のrequired outcome value、clarification resultのpermission、またはclarification operationのstop conditionを変え得る場合だけ許可する |
| 5. 実行できなくなる問題経路 | A01で未指定modeだけを質問すれば完了するのに、質問へ影響しないworkspace、branch、HEAD、clean状態を先に読む経路。開始状態resultを消費する未完了の判断がないため、読み取りpermissionが成立しない |
| 6. 維持する正常経路 | 未固定値の質問、開始状態によって質問permissionまたはstop conditionが変わるTaskSpecでの直接観測、`spec_ready=true`後の実装選択用証拠取得、Candidate147の`DECISION_BOUNDARY`を含む他の全条項。F03は`spec_ready=true`の経路なので変更対象外とする |
| 7. 新しく増える判断と対象外影響 | 新しいcommand、順序、回数、出力種別、ticket、ownership labelは増やさない。開始状態resultがclarificationの対象、permission、stop conditionのいずれかを変え得るかという既存の結果影響範囲だけをpermission条件へ使う |
| 8. 評価 | 最初はA01とF03を各N=5で実施する。品質はケースごとにScore分布を記録する。A01ではclarification前のrepository evidence発行数、F03ではCandidate147が保った開始identity観測と許可済みreadの初回発行関係を診断する。KPIは品質、all-agent `total_tokens`、`elapsed_seconds`をCandidate147の保存済み同条件resultとケース別・合算で比較する |
| 9. 停止条件 | Score `4`未満、必要な質問の欠落、開始状態resultが必要な正常経路の遮断、開始result受領前の禁止済み変更またはrequired commandが一件でもあれば停止する。行動経路の成立率だけで自動採否を決めない。品質が同じでtokenまたは時間の一方が増える場合は、その増加が必要処理の結果かを調べ、説明できなければ追加N、Standard14、採用へ進めない |

九項目を固定できたため、Candidate bundleを作成できる。評価profileと評価slotは、bundle identityの検証と比較前照合が完了するまで作成または発行しない。

## Bundle identity

- bundle path: `prompts/candidates/the-caption-3ce91a4-spec-false-start-state-consumer-permission-r1`
- bundle SHA-256: `61c0735fc0cadcb0d45d2132346d01540d8366040ce886bb3f4332279915ba33`
- root `AGENTS.md`: 10,954 bytes
- Candidate147との差: `+182` bytes
- changed target: `AGENTS.md`だけ
- root以外の18 target: Candidate147と同一entry

Candidate147との差分は、`EVIDENCE_GATE`の`spec_ready=false`時の許可文一件の置換だけである。Candidate147の`SPEC`、`DECISION_BOUNDARY`およびその他の全条項は逐語同一である。

## 置換する条件

Candidate147の次の一文を置換する。

> `spec_ready=false`では`TaskSpec本文 / TaskSpec明示の開始状態の直接観測`だけを許可し、未固定のrequired outcome valueをclarification resultにして変更前evidence operationをterminalにする。

Candidate262では次の一文にする。

> `spec_ready=false`では`TaskSpec本文`だけを許可する。TaskSpec明示の開始状態の直接観測は、そのresultが未固定のrequired outcome value、clarification resultのpermissionまたはclarification operationのstop conditionを変え得る場合だけ許可する。未固定のrequired outcome valueをclarification resultにして変更前evidence operationをterminalにする。

これは「開始状態を読まないよう判断する」という指示ではない。開始状態resultを受け取る合法な未完了判断がない場合に、読み取りへ至るpermissionの辺を閉じる。

## 継承しないもの

- Candidate261の`SPEC`追加文。出力先の分類をモデルへ追加する全体制御はF03で費用増と発行関係の変化を伴ったため継承しない。
- Candidate254からCandidate260までの自然文再構成、読み取り回数条件、同一model stepの手順化、部分read条件。
- 成功runのcommand、tool順、判断順、待機方法。
- Candidate147以外のCandidate本文。

## 評価判断

Candidate147のA01 / F03保存済み各5件を比較基準へ固定し、新しいCandidate147 runは発行しない。Candidate262の不足10件だけを発行する。品質比較とKPI比較は、行動経路の診断結果にかかわらず実施する。

初回N=5は対象境界と非対象経路の回帰を確認する段階であり、Standard14、採用、releaseまたはtarget本体への反映を意味しない。

現在状態は`candidate_creation_gate_passed / c147_direct_baseline_fixed / candidate261_not_inherited / spec_false_start_state_consumer_permission_only / candidate262_bundle_created / bundle_identity_verified / a01_f03_n5_completed / a01_no_repository_command_5_of_5 / standard14_completed / score4_70_of_70 / aggregate_token_regressed_5_06_percent / elapsed_improved_2_65_percent / unjustified_token_regression / additional_n_not_authorized / adoption_not_approved / release_not_created / projection_not_performed`とする。targeted結果は[Candidate262 A01 / F03 N=5](../evaluations/results/candidate262-spec-false-start-state-consumer-permission-a01-f03-n5_2026-08-16.md)、全体判断は[Candidate262 Standard14 N=5](../evaluations/results/candidate262-spec-false-start-state-consumer-permission-standard14-n5_2026-08-16.md)を正本とする。
