# Candidate266 C147明示instruction配下read依存設計

> **目的対応の訂正（2026-08-16）**: この案を作成した時点の`task_objective`は、Candidate254系の有効制御を保持したまま、Candidate264で弱くなった制御を復元することだった。C147上の単独機序probeは、その目的に残る保持predicateまたは改善predicateを直接bindできず、Candidate254改善系列をC147直接系列へ置き換えていた。本来はこの派生operationを発行対象へ入れず、同じ`task_objective`のままCandidate254を直接の基盤とする別設計へ進むべきだった。作成済みbundleとN=5結果は、現在系列の改善根拠、親または必須gateにせず、`off_target_diagnostic_evidence`としてのみ保持する。

> **Candidate267方針（2026-08-16）**: 上の訂正にある「Candidate254を直接の基盤とする別設計」は、Candidate265の履歴上の直接比較元とCandidate264までの本文をどう扱うかを分けておらず、後続設計の基盤として採用しない。利用者の明示判断により、Candidate267はCandidate264を直接の基盤とし、Candidate264の本文とF01・F02・F03で成立した共同発行を保持したまま、F10で残ったinstruction result前の配下read permissionだけを閉じる。Candidate266はexact path、配下path関係およびterminal success resultによる閉鎖の`off_target_diagnostic_evidence`に限定し、Candidate267の親、必須gateまたは成功根拠にしない。

## 履歴上の直接比較元とCandidate267の基盤

- Candidate265の履歴上の直接比較元はCandidate264である。Candidate265はCandidate264の他の本文を同一byteで保持し、`DECISION_BOUNDARY`だけへ追加差分を置いた。
- Candidate267の直接の基盤もCandidate264とする。Candidate264の`DECISION_BOUNDARY`を含む本文とF01・F02・F03の成立効果を保持し、F10のpermission edgeだけを変更対象にする。
- Candidate265は、意味の自己分類ではpermissionを閉じられなかった診断反例として使う。Candidate265のbundle、predicate、評価上の成功状態は継承しない。
- Candidate266は、exact path関係とterminal success resultによる機械的な閉鎖の診断証拠としてだけ使う。C147直接という基盤、bundle、N=5通過はCandidate267へ継承しない。

## 結論

Candidate266は、最後にStandard14 N=100で品質を実証したC147 `the-caption-3ce91a4-result-effect-scope-r1`を直接の基盤とする。停止済みCandidate264または作成前gate違反のCandidate265を親、追加条件の材料、成功状態の継承元として使わない。両者は、F10で残った誤経路と、自己分類でpermissionを閉じられなかった反例としてだけ参照する。

このためCandidate266は、Candidate264を置き換える完成案ではない。Candidate254系の他制御を保持したまま改善する前に、自己判定を使わない一つのpermission edgeだけをC147上で単独検証する機序probeとする。

変更する機序は一つである。TaskSpecがread対象として`D/AGENTS.md`をpath文字列で明示した場合、そのexact instructionの成功resultを受領するまで、`D/AGENTS.md`自身を除く`D/`配下readのpermissionを開かない。instructionがreadへ影響するか、読む必要があるか、適用対象かをモデルへ分類させない。

```text
declared_instruction(D) :=
  TaskSpecのread対象にexact path D/AGENTS.mdが明示されている

declared_descendant_read(read, D) :=
  normalized(read.target) != D/AGENTS.md
  ∧ normalized(read.target)がD/配下にある

instruction_result_ready(D) :=
  D/AGENTS.mdにbindしたread invocationがterminal success
  ∧ そのcontent resultを受領済み

declared_instruction(D)
∧ declared_descendant_read(read, D)
∧ instruction_result_ready(D)=false
-> authorized_read(read)=false
```

この否定は`result_effect_scope`、TaskSpecの一般的な`read=true`、配下pathの列挙または開始identityがreadを禁止しないことより優先する。`D/AGENTS.md`のread自体は同じ否定の対象にしないため、開始identityと相互非依存ならC147どおり同じmodel stepから発行できる。

## Candidate作成前の検討gate

### 1. 比較基準と正常な最短経路

- 直接の基盤はC147である。Candidate264とCandidate265は親にしない。
- F01、F02、F03のTaskSpecは`D/AGENTS.md`のexact pathをread対象へ明示していない。したがって新しいdependencyは成立せず、開始identityと許可済みsource/test readを同じmodel stepから発行するC147の正常経路を維持する。
- F10のTaskSpecは`src/AGENTS.md`と`src/app/entrypoints`配下readを明示する。開始identityと`src/AGENTS.md`は同じmodel stepから発行できる。`src/AGENTS.md`の成功result受領後、三本文read、必要なlisting、retired path不存在確認および終了statusを既存permission内で完遂する。

### 2. 保存traceで確認した問題経路

C147 Standard14 N=5のF10では、`src/AGENTS.md` result後にentrypoint本文readを発行したのは2 / 5件だった。残る3件はinstruction result前に配下本文を発行した。passはrun `6f198e7175f0425d9b736e543e9d1ebd`と`9636b46d3767412aabf25d46bf7366bd`、failは`4b2eb9a7b0774c1baac9ee698c821850`、`726f0a953a664eb5bcc96726e4114915`、`873734aa221648bba9ac3372112070d6`である。

Candidate264 N=20で同じ必要依存が2 / 20件にとどまったことは、問題経路の再現性を示す診断証拠としてだけ使う。Candidate265 N=5の4 / 5件は、自己分類を加える案が一件のpermissionを残す反例としてだけ使う。

### 3. 問題経路を許したpermission edge

C147の`DECISION_BOUNDARY`は、resultが後続readのtargetまたはpermissionを変え得るかを実行時に分類する一般則である。F10ではTaskSpecが`src/AGENTS.md`と配下readをともに明示していても、一般的な`read=true`と配下path列挙から本文readを`decision_boundary=false`と扱える。このため、同じ入力でもモデルの分類次第でinstruction result前の本文readをprompt準拠のまま発行できる。

### 4. 変更する条件と直接判定可能性

- 入力はTaskSpecに現れるexact `D/AGENTS.md`文字列と、発行しようとするread targetのnormalized pathだけである。
- dependencyの対象はpath prefixで機械的に決まり、「影響し得る」「必要」「適用される」という意味分類を使わない。
- permissionを開くresultは、exact instruction read invocationのterminal successとcontent受領へ機械的にbindする。
- instruction resultの内容がTaskSpecと矛盾する場合は既存TaskSpecの停止条件を適用する。矛盾の有無を配下read permissionの開放条件にはしない。
- C147の他条項と、`DECISION_BOUNDARY`内の既存文は同一byteで保持し、この否定だけを追加する。

### 5. 実行できなくなる問題経路

同じmodel outputまたは同じcommandに`D/AGENTS.md` readと`D/`配下readを含めても、配下read側は発行時点で`authorized_read=false`である。モデルが判断順、tool grouping、command compositionまたは`result_effect_scope`分類を変えても、exact instruction success resultの受領前に配下readをprompt準拠で構成できない。

### 6. 維持する正常carrier

- 開始identityとexact instruction readの共同発行。
- instruction pathをTaskSpecが明示していないF01、F02、F03の開始identityと許可済みreadの共同発行。
- exact instruction success result受領後の複数配下readの共同発行。
- F10で必要な三本文、directory listing、retired path不存在および最終statusのread-only完遂。

carrierは`TaskSpec -> exact instruction invocation -> terminal success content result -> 配下read permission`の一つに固定する。別のlabel、ticket、ownershipまたは自己分類でpermissionを開かない。

### 7. 新しく増える判断と対象外影響

新しい意味判断は増えない。増えるのはexact文字列照合、path prefix照合およびterminal success resultの対応付けだけである。TaskSpecがinstruction pathを明示しないreadへは影響しない。validation完了時機、wrapper、yield、wait、command選択、read範囲および出力量は変更しない。

### 8. 評価ケースと比較単位

初回はCandidate266だけを次の四ケース各N=5で実行し、C147の保存済み同一四ケース各N=5を再実行せず比較する。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

F01、F02、F03では開始identityと必要readの共同発行を診断する。F10では、exact `src/AGENTS.md` success result前の`src/`配下listing・本文readが0件であることと、result後に必要readを完遂したことを別々に確認する。品質、機序、変更対象外影響、all-agent `total_tokens`、`elapsed_seconds`を分離する。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F10で`src/AGENTS.md` success result前に`src/`配下listingまたは本文readを一件でも発行した場合は`mechanism_failed`として停止する。
- F10でinstruction result後に必要readを完遂できない場合は`normal_route_failed`として停止する。
- F01、F02、F03で開始identityと必要readを同じAI判断から発行できないrunが一件でもあれば`unaffected_route_regressed`として停止する。
- C147比でtokenまたは経過時間が増え、必要なinstruction dependencyへ増加分を対応づけられない場合は`unjustified_cost_regression`として停止する。
- 全gate通過前に追加N、Standard14、採用、releaseまたはprojectionへ進めない。

## 非目標

- Candidate264またはCandidate265の本文継承。
- 「instructionが影響し得るか」「必要か」「適用されるか」の自己判定。
- 成功runのtool順、command、read範囲またはmodel stepの転記。
- validation完了待ち、wrapper、yield、wait時間またはruntimeの変更。
- TaskSpec、case、fixture、oracleまたはrating contractの変更。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

## 現在状態

作成前gate 1〜9を満たした。条件は明示入力、path prefixおよびmachine resultから直接判定でき、自己分類を含まない。bundle SHA-256は`274217c1f7adbaadbbb7bbec31a3443bdd336f53b5794ef99d799f8509dbc4b4`である。

対象四ケース各N=5は20 / 20件がScore `4`だった。F01、F02、F03の正常な共同発行は各5 / 5件、F10のexact instruction result先行は5 / 5件、必要read完遂も5 / 5件だった。C147比はtoken`-3.60%`、elapsed`-3.78%`である。結果は[`Candidate266 F01・F02・F03・F10 entrypoint N=5`](../evaluations/results/candidate266-declared-instruction-descendant-read-dependency-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)へ固定した。

当時の機序観測は保持するが、現在状態は`objective_mismatch_confirmed / candidate_should_not_have_been_created_for_current_objective / off_target_diagnostic_evidence / historical_isolated_mechanism_observation_only / not_candidate264_replacement / not_parent / not_required_gate / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
