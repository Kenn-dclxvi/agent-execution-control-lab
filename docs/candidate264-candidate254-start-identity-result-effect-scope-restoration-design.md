# Candidate264 Candidate254開始確認結果影響範囲の復元設計

## 結論

Candidate264はCandidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`を直接の親とする。変更対象はroot `AGENTS.md`の`DECISION_BOUNDARY`全体だけとし、Candidate254のその他の本文は同一byteで保持する。

Candidate147でF01、F02、F03の開始確認と許可済みreadの分離を0 / 15件にした四つの関係を、一組の依存関係として復元する。

```text
result_effect_scope := 受領resultが対象、許可、方法または停止条件を変え得る未発行operation classの集合
decision_boundary(next_operation) := next_operation.class ∈ result_effect_scope
identity_result_effect_scope = {artifact_change, required_validation}
authorized_read ∉ identity_result_effect_scope
```

Candidate263は一般的な`result_effect_scope`だけを置換し、開始確認固有の後二行を固定しなかったため、この復元を実施したCandidateとは扱わない。

## Candidate作成前の検討gate

### 1. 比較基準と最短正常経路

- 直接の親はCandidate254である。
- 開始確認の停止条件が成果物変更と必須検証だけを禁止する場合、開始確認とTaskSpecで許可済みのreadを同じAI判断から発行する。
- 共同resultを受領して開始状態が正常だと判定されるまで、成果物変更と必須検証だけを発行しない。
- 開始確認でread自体が禁止される場合、またはread対象か許可が変わり得る場合は、readを結果受領後へ置く。

### 2. 保存済み実行記録で確認した問題経路

Candidate254 Standard14 N=20のF03では、開始確認の結果が必要readの対象または許可を変えないのに、開始確認のresultを受領してから別のAI判断でreadを発行した実行が6 / 20件あった。Candidate147では、同じ判定基準によるF01、F02、F03の対象15件すべてで開始確認と許可済みreadを同じAI判断から発行していた。

### 3. 問題経路を許した依存関係

Candidate254は「同じAI判断から発行する」という行動を記述するが、開始確認resultが停止できる後続作業を固定集合へ限定していない。そのため、モデルが開始確認resultを許可済みreadの待機条件として扱う余地が残る。

Candidate263も、結果が影響できる作業だけを待機対象にする一般条件へ置換しただけで、開始確認の影響範囲を`artifact_change`と`required_validation`へ固定せず、許可済みreadをその範囲から明示的に除外しなかった。

### 4. 変更する条件と責任範囲

- 変更targetはroot `AGENTS.md`だけとする。
- `DECISION_BOUNDARY`全体を、一般的な結果影響範囲と開始確認固有の集合関係を持つ本文へ置換する。
- Candidate254のその他のtargetと本文は同一byteで保持する。
- Candidate147、Candidate261、Candidate262、Candidate263の本文を親として継承しない。

### 5. 実行できなくなる問題経路

開始確認の`identity_result_effect_scope`へ許可済みreadを含めないため、開始確認resultの受領を、そのreadの開始条件にする経路はpromptに適合しない。判断順が変わっても、readを後続へ分離するには、TaskSpecがreadを禁止するか、そのresultでread対象または許可が変わり得る必要がある。

### 6. 維持する正常経路

- A01と対応したCandidate254の`SPEC`境界を保持する。
- Candidate254の`EVIDENCE_GATE`、`OWNER_ROLE`、`VALIDATION_CLOSURE`および`VALIDATION_PLAN`を保持する。
- F10 entrypointで、path-local instructionによって配下readの対象または許可が変わり得る場合は、instruction resultを先に受領できる。
- 特定のcommand、read範囲、tool順、wait時間またはwrapper構成を固定しない。

### 7. 新しく増える判断と対象外影響

新しい自己分類、処理手順または例外条件は増やさない。開始確認について、結果が停止できる後続作業と停止できない許可済みreadを事前に集合へ固定する。`DECISION_BOUNDARY`以外は変更しないため、他の制御群の圧縮や再構成を同時に行わない。

### 8. 評価ケースと比較単位

初回評価はCandidate264だけを次の四ケース各N=5で行う。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

F01、F02、F03では開始確認と許可済みreadの分離を診断する。F10ではinstruction resultがread対象または許可を変え得る場合の必要な分離を診断する。品質、問題経路、正常経路、all-agent `total_tokens`、`elapsed_seconds`を別々に記録する。直接比較には保存済みCandidate254の同一条件・同一ケース・同一iterationを使う。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- 共同result受領前に、開始確認が禁止する成果物変更または必須検証を発行した場合は停止する。
- F10でinstruction resultによってread対象または許可が変わり得るのに、配下readを先行発行した場合は停止する。
- F01、F02、F03で分離が残った場合は結果を保持し、追加NまたはStandard14へ自動で進めない。機序と品質再現性の相関が100%とは確認されていないため、品質結果自体は無効化しない。
- Candidate254比でtokenまたは経過時間の一方でも増え、品質または必要な正常経路との対応を確認できなければ`unjustified_cost_regression`として停止する。

## 非目標

- Candidate254本文の圧縮。
- 完了待ちの発生頻度を変えること。
- command、read範囲、tool順、wait時間、wrapper構成または実行回数の指定。
- Candidate147への全面復帰。
- Candidate261、Candidate262またはCandidate263への修正追加。
- Standard14、採用、releaseまたは本体反映。

## 現在状態

現在状態は`design_complete / candidate_created / targeted_n5_completed / quality_passed / target_mechanism_passed / normal_route_regressed / unjustified_cost_regression / stopped / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。評価結果は[`evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md`](../evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)を正本とする。

## 利用者の明示的判断によるN=20後続観測

2026-08-16に、利用者の明示的な判断により、停止済みのCandidate264を同じ四ケースだけ各N=20まで観測した。この後続観測は上記N=5停止判断を遡及変更せず、Standard14、採用、releaseまたはprojectionを許可しない。

既存20件を再利用して不足60件だけを発行し、80 / 80件がScore `4`だった。F01、F02、F03の共同発行は各20 / 20件で成立したが、F10の必要なinstruction result境界は2 / 20件にとどまり、追加15件では0 / 15件だった。C147同数比較に対しtokenは`+7.45%`、elapsedは`+5.52%`となったため、Candidate264は引き続き`normal_route_regressed / unjustified_cost_regression / stopped`とする。後続結果は[`Candidate264 F01・F02・F03・F10 entrypoint N=20`](../evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n20_2026-08-16.md)を参照する。
