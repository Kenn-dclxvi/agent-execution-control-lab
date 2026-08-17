# Candidate265 Candidate264 instruction result read permission復元設計

> **設計gate違反の訂正（2026-08-16）**: この案は`instruction resultがreadのtarget、permissionまたはstop conditionを変え得る`という分類をモデルへ委ねていた。これは`docs/prompt-control-design-principles.md`の自己判定禁止と、Candidate作成前gate 4・5に違反する。本来はbundle、profile、評価枠を作らず`prompt_control_not_demonstrated / candidate_not_created`として棄却すべきだった。作成済みbundleとN=5結果は採用可能なCandidateとして扱わず、同じ設計ミスを再利用しない診断反例としてのみ保持する。

> **直接比較元の範囲**: 上の訂正はCandidate265の設計gate違反と現在の評価上の位置づけを訂正するものであり、Candidate265作成時の直接比較元を遡及変更しない。Candidate265の履歴上の直接比較元はCandidate264であり、Candidate264の`DECISION_BOUNDARY`を含む本文と保持対象の効果を前提に、同境界だけへ追加差分を置いた設計だった。後続のCandidate267もCandidate264を直接の基盤とし、この保持関係を維持したまま、Candidate265で自己分類へ委ねたpermission edgeだけを機械的に閉じ直す。

## 結論

Candidate265は、利用者が明示した改善順序に従い、停止済みCandidate264 `the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1`を直接の比較元とする。Candidate264の成功状態や採用可能性を継承するのではなく、F01、F02、F03で各20 / 20件成立した開始確認と影響を受けないreadの共同発行を保持したまま、F10で18 / 20件残ったinstruction result前の配下read permissionだけを閉じる。

変更対象はroot `AGENTS.md`の`DECISION_BOUNDARY`だけとし、Candidate264の他の本文を同一byteで保持する。validation完了境界、wrapper、yield、wait時間または実行方法はこのCandidateで変更しない。

復元する関係は次の一つとする。

```text
instruction_dependency_pending(read) :=
  TaskSpecがread対象へ適用するrepository instructionを明示している
  ∧ そのinstruction resultがreadのtarget、permissionまたはstop conditionを変え得る
  ∧ terminalかつcompatibleなinstruction resultを未受領

instruction_dependency_pending(read)=true -> authorized_read=false
```

TaskSpecが配下pathをread対象として列挙したことだけでは、この依存を解消しない。instruction自体のreadは配下readではなく、それ自身に未解決dependencyがない限り、開始確認と同じmodel stepから発行できる。

## Candidate作成前の検討gate

### 1. 比較基準と保持する正常経路

- 直接の比較元はCandidate264である。
- 開始確認resultがtarget、permissionまたはstop conditionを変えないF01、F02、F03の必要readは、開始確認と同じmodel stepから発行できる。
- 開始確認と共同発行したresultを受領するまで、Candidate264と同じくartifact変更とrequired validationだけを発行しない。
- TaskSpecが明示した適用repository instructionは、それ自身に未解決dependencyがなければ開始確認と共同発行できる。
- terminalかつcompatibleなinstruction resultを受領した後は、その結果で許可された配下readを同じmodel stepから発行できる。

### 2. 保存traceで確認した問題経路

Candidate264のF10 entrypoint N=20では、`src/AGENTS.md`のresultを受領した後に三つのentrypoint本文を読んだrunは2 / 20件だった。残る18件は、`src/AGENTS.md`が配下readのtarget、permissionまたはstop conditionを確定する前に本文readを発行した。追加N=15だけでは15 / 15件すべてに同じ経路が残った。

一方、F01、F02、F03では、開始確認と影響を受けない必要readの共同発行が各20 / 20件成立した。この成立関係は削除、置換または一般的な逐次実行へ戻さない。

### 3. 問題経路を許したpermission edge

Candidate264は`authorized_read`を開始確認の影響範囲から除外したが、TaskSpecに列挙されたreadと、別のrepository instruction resultで初めてtarget、permissionまたはstop conditionが確定するreadを区別しなかった。そのため、未解決instruction dependencyを持つ配下readも、TaskSpecに列挙済みという理由だけで`authorized_read`として扱える。

Candidate147の`result_effect_scope`は、resultがtarget、permission、methodまたはstop conditionを変え得る未発行operation classをdecision boundaryへ入れていた。しかしCandidate264では、開始確認固有の共同発行を強く固定する過程で、別種のinstruction result dependencyを`authorized_read`の成立条件へ接続できていない。

### 4. 変更するpredicateと責任範囲

- `instruction_dependency_pending(read)`を`DECISION_BOUNDARY`へ追加する。
- 同predicateがtrueのreadを`authorized_read`から除外する。
- TaskSpecのpath列挙だけでは同predicateをfalseにできないよう固定する。
- instruction resultが`compatible`なら配下read permissionを開く。
- instruction resultが`missing / unreadable / contradiction`なら、TaskSpecのstop conditionへbindし、配下read permissionを開かない。
- root `AGENTS.md`以外のtargetと、`DECISION_BOUNDARY`以外の本文はCandidate264と同一byteで保持する。

### 5. 実行できなくなる問題経路

未解決の適用instruction resultを持つ配下readは`authorized_read=false`になるため、instruction readと同じmodel stepから配下本文を先行発行する経路はpromptに適合しない。TaskSpecが配下pathを明示していること、read全般を許可していること、開始確認がreadを禁止しないことは、このpermissionを開く条件にならない。

### 6. 維持する正常経路

- F01、F02、F03の開始確認と影響を受けないreadの共同発行。
- 開始確認と、開始確認から影響を受けないrepository instruction readの共同発行。
- compatibleなinstruction result受領後の複数配下readの共同発行。
- Candidate264の`SPEC`、`EVIDENCE_GATE`、`OWNER_ROLE`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`。
- instruction dependencyを持たないTaskSpec明示readの既存permission。

### 7. 新しく増える判断と対象外影響

増える判断は、各readに未解決のapplicable instruction dependencyがあるかという一predicateだけである。成功runのcommand、tool順、read回数またはwait時間を固定しない。repository instructionを探索する新しいread permissionも作らず、TaskSpecまたは既にmodel-visibleなrepository authorityが明示したinstruction identityだけを使う。

validation wrapperの完了時機と追加model再入は別機序として保留する。このCandidateでは`VALIDATION_CLOSURE`または`VALIDATION_PLAN`を変更せず、同問題の改善を主張しない。

### 8. 評価ケースと比較単位

初回評価はCandidate265だけを次の四ケース各N=5で行う。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

F01、F02、F03では開始確認と影響を受けない必要readの共同発行を診断する。F10では、`src/AGENTS.md`のterminal result受領前に配下listingまたはentrypoint本文を発行していないことと、compatible result受領後に必要readを完遂したことを別々に確認する。品質、機序、all-agent `total_tokens`、`elapsed_seconds`を分離して保存する。

比較が必要になった時点では保存済みCandidate264の同じ四ケース各N=5を使い、Candidate264を再実行しない。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F10でinstruction result受領前に配下listingまたは本文readを一件でも発行した場合は`mechanism_failed`として停止する。
- F10でcompatible result受領後に必要な配下readを完遂できない場合は`normal_route_failed`として停止する。
- F01、F02、F03で開始確認と影響を受けない必要readの分離が一件でもあれば、Candidate264の成立済み関係を保持できなかったものとして停止する。
- Candidate264比でtokenまたは経過時間が増え、その増加を必要なF10 dependency以外へ対応づけた場合は`unjustified_cost_regression`として停止する。
- 初回N=5の全gateを通過する前に追加N、Standard14、採用、releaseまたはprojectionへ進めない。

## 非目標

- C147への全面復帰。
- Candidate264の平易日本語構造の圧縮または全面再構成。
- validation完了待ち、wrapper、yield、wait時間または実行方法の変更。
- 新しいrepository instruction探索。
- F10固有path、case IDまたは期待値のCandidate本文への埋め込み。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

## 現在状態

初回N=5では20 / 20件がScore `4`で、F01、F02、F03の共同発行を各5 / 5件で保持した。F10の必要依存はCandidate264の2 / 5件から4 / 5件へ改善したが、一件で`src/AGENTS.md`のresult受領前に配下listingと本文readを発行したため、固定した`mechanism_failed`停止条件へ該当した。Candidate264比はtoken`+10.75%`、elapsed`+4.08%`で、増加分を必要なF10依存へ対応づけられなかった。評価結果は[`Candidate265 F01・F02・F03・F10 entrypoint N=5`](../evaluations/results/candidate265-instruction-result-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)を参照する。

現在状態は`design_gate_violation_confirmed / self_classification_forbidden / candidate_should_not_have_been_created / prompt_control_not_demonstrated / diagnostic_artifacts_retained / targeted_n5_historical_observation_only / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
