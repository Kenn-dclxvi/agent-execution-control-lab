# Candidate267 Candidate264明示instruction配下read permission復元設計

> **後続の優先順位訂正**: Candidate267のF10機序成立はfeedbackとして保持するが、Candidate267を親にせず、次にcarrier等の新制御も加えない。先に[`Candidate254からCandidate267までの自然語feedback優先監査`](candidate254-candidate263-candidate267-natural-language-feedback-priority-audit.md)に従い、Candidate254を直接の基盤として、Candidate263からCandidate267までで成立または不成立を確認した関係だけを自然語へ再構成する。

## 結論

Candidate267はCandidate264 `the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1`を直接の基盤とする。予定prompt identityは`the-caption-3ce91a4-declared-instruction-read-permission-restoration-r1`とする。

Candidate264のroot `AGENTS.md`を直接の本文とし、`DECISION_BOUNDARY`へ一つの機械的なpermission dependencyだけを追加する。Candidate264で復元した一般的な`result_effect_scope`、開始確認固有の`identity_result_effect_scope = {artifact_change, required_validation}`、`authorized_read`の除外、およびF01・F02・F03で成立した開始確認と影響を受けないreadの共同発行を保持する。Candidate264の他の本文と全targetは同一byteで保持する。

Candidate265は、F10で閉じるべき誤経路と、意味の自己分類ではpermissionを閉じられない反例としてだけ使う。Candidate265のbundle、`instruction resultがreadへ影響し得る`というpredicate、評価状態および成功率を継承しない。Candidate266は、exact pathとterminal success resultによる局所的な閉鎖を観測した目的外診断証拠としてだけ参照し、親、必須gateまたはCandidate267の成功根拠にしない。

復元するpermission dependencyは次の一つとする。

```text
declared_instruction(D) :=
  TaskSpecのread対象にnormalized exact path D/AGENTS.mdが明示されている

declared_descendant_read(read, D) :=
  normalized(read.target) != D/AGENTS.md
  ∧ normalized(read.target)がD/配下にある

instruction_result_ready(D) :=
  D/AGENTS.mdへbindしたread invocationがterminal success
  ∧ そのcontent resultを受領済み

declared_instruction(D)
∧ declared_descendant_read(read, D)
∧ instruction_result_ready(D)=false
-> authorized_read(read)=false
```

この否定は一般的なread permission、TaskSpecによる配下pathの列挙、`result_effect_scope`および開始確認の停止範囲より優先する。`D/AGENTS.md`自身のreadには適用しない。permissionを開く条件はexact instruction readのterminal successとcontent result受領だけであり、instructionの必要性、適用性または後続readへの影響をモデルに自己分類させない。

## Candidate作成前の検討gate

### 1. 比較基準と保持する正常経路

- 直接の基盤と比較元はCandidate264である。
- F01、F02、F03では、TaskSpecがread対象として`D/AGENTS.md`を明示していないため新しいdependencyを成立させず、開始確認と影響を受けない必要readを同一model stepから発行するCandidate264の正常経路を保持する。
- F10では、開始確認とTaskSpec明示の`src/AGENTS.md` readを同一model stepから発行できる。
- `src/AGENTS.md`のterminal success content result受領後は、三つのentrypoint本文、必要なdirectory listing、retired path不存在確認および最終statusを既存permission内で完遂できる。
- Candidate264の`SPEC`、`EVIDENCE_GATE`、`OWNER_ROLE`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`および`RECOVERY`を変更しない。

### 2. 保存traceで確認した問題経路

Candidate264のF10 entrypoint N=20では、`src/AGENTS.md`のresult受領後にだけ配下本文readを発行したrunは2 / 20件だった。残る18件はinstruction result受領前に配下readを発行し、追加N=15だけでも15 / 15件に同じ経路が残った。

Candidate265 N=5ではこの経路が1 / 5件残った。失敗run `3e110cb347584b1196b37b4a0e3ef7ed`は、`src/AGENTS.md`のcommand result受領前に`find src/app/entrypoints`と`v4_daily_main.py`本文readを発行した。Candidate265の意味分類は、この経路をprompt準拠で実行できるpermissionを閉じなかった。

一方、Candidate264のF01、F02、F03では、開始確認と影響を受けない必要readの共同発行が各20 / 20件で成立した。この正常経路は変更対象にしない。

### 3. 問題経路を許したpermission edge

Candidate264は開始確認resultの影響範囲から`authorized_read`を除外したが、TaskSpecがexact `D/AGENTS.md`と`D/`配下readをともに列挙した場合に、instruction result受領を配下read permissionの前提へ接続していない。このため、一般的なread permissionと配下path列挙だけで、instructionと配下本文を同一model stepから発行できる。

Candidate265は、この不足を`instruction resultがreadの対象、permissionまたはstop conditionを変え得る`という意味分類で補おうとした。モデルが影響なしと分類すれば配下readを`authorized_read`として発行できるため、permission edgeは残った。

### 4. 変更するpredicateと責任範囲

- Candidate264の`DECISION_BOUNDARY`へ`declared_instruction(D)`、`declared_descendant_read(read, D)`および`instruction_result_ready(D)`の関係を追加する。
- exact `D/AGENTS.md`をTaskSpecがread対象へ明示した場合だけ、新しいdependencyを成立させる。
- normalized targetが同じ`D/`配下にあるreadだけを、instruction result未受領中の`authorized_read`から除外する。
- exact instruction readのterminal successとcontent result受領だけで配下read permissionを開く。
- instruction readがmissing、unreadableまたはnon-successならpermissionを開かず、既存TaskSpecの停止条件へbindする。
- root `AGENTS.md`の`DECISION_BOUNDARY`以外と、Candidate264の他の全targetを同一byteで保持する。

### 5. 実行できなくなる問題経路

TaskSpecがexact `D/AGENTS.md`を明示している場合、同じmodel output、tool groupまたはcommandにinstruction readと`D/`配下readを含めても、配下readは発行時点で`authorized_read=false`になる。モデルがtool順、grouping、`result_effect_scope`またはinstructionの影響有無をどう判断しても、exact instruction result受領前の配下readをprompt準拠で構成できない。

TaskSpecの一般的な`read=true`、配下pathの列挙、開始確認がreadを禁止しないこと、instructionが必要だという説明、ticketまたはownership labelはpermissionを開かない。

### 6. 維持する正常carrier

- 開始確認とexact instruction readの共同発行。
- instruction pathをTaskSpecが明示していないF01、F02、F03の開始確認と必要readの共同発行。
- exact instruction result受領後の複数配下readの共同発行。
- F10で必要な三本文、directory listing、retired path不存在および最終statusのread-only完遂。

carrierは`TaskSpecのexact instruction path -> instruction read invocation -> terminal success content result -> 配下read permission`へ固定する。Candidate265の意味分類やCandidate266のC147本文をcarrierへ含めない。

### 7. 新しく増える判断と対象外影響

新しい意味判断は増やさない。増えるのはTaskSpec上のexact path照合、normalized path prefix照合、read invocationとterminal success resultの対応付けだけである。TaskSpecがinstruction pathを明示しないreadには新しいdependencyを適用しない。repository instructionを探索する新しいread permissionも追加しない。

validation完了待ち、wrapper、yield、wait、command選択、read範囲、出力量、TaskSpec、case、fixture、oracleおよびrating contractは変更しない。

### 8. 評価ケースと比較単位

Candidate bundle作成後の初回評価はCandidate267だけを次の四ケース各N=5で行う。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

F01、F02、F03では開始確認と影響を受けない必要readの共同発行を診断する。F10では、exact `src/AGENTS.md` success result受領前の`src/`配下listing・本文readが0件であることと、受領後に必要readを完遂したことを別々に診断する。品質、機序、変更対象外影響、all-agent `total_tokens`および`elapsed_seconds`を分離する。

比較が必要になった時点では、保存済みCandidate264の同じ四ケース各N=5を直接の基準resultへ固定し、Candidate264を再実行しない。Candidate265とCandidate266のresultは診断証拠に限定し、Candidate267の比較基準にしない。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F10でexact `src/AGENTS.md` success result受領前に`src/`配下listingまたは本文readを一件でも発行した場合は`mechanism_failed`として停止する。
- F10でinstruction result受領後に必要readを完遂できない場合は`normal_route_failed`として停止する。
- F01、F02、F03で開始確認と影響を受けない必要readを同一model stepから発行できないrunが一件でもあれば`preserved_route_regressed`として停止する。
- Candidate264比でtokenまたは経過時間の一方でも増え、増加分を必要なinstruction dependencyまたは正常経路へ対応づけられなければ`unjustified_cost_regression`として停止する。
- 初回N=5の全gateを通過する前に追加N、Standard14、採用、releaseまたはprojectionへ進めない。

## 非目標

- Candidate265のbundleまたは自己分類predicateの修正継承。
- Candidate266のC147本文、bundle、N=5通過または評価状態の継承。
- Candidate264の停止判断、cost退行または未承認状態の取消し。
- 成功runのcommand、tool順、read回数、model stepまたはwait時間の実行義務化。
- validation完了境界、wrapper、yield、wait時間または実行方法の変更。
- 新しいrepository instruction探索。
- TaskSpec、case、fixture、oracleまたはrating contractの変更。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

## 現在状態

Candidate bundleを作成した。prompt identityは`the-caption-3ce91a4-declared-instruction-read-permission-restoration-r1`、bundle SHA-256は`f76cd120292ba1ca6e8752e3bd15ca3376571fe176db722b1650353400216684`である。Candidate264との差分はroot `AGENTS.md`の`DECISION_BOUNDARY`へ追加した一段落だけであり、他のtargetは同一byteである。

専用テストは5件、bundle identity検証は18件・286 subtests、全test discoveryは1,566件・2,008 subtestsが通過した。`git diff --check`も通過した。

対象四ケース各N=5、model `gpt-5.6-sol`、reasoning `medium`、Codex CLI `0.146.0`、`workspace-write / never`、設定上の`max_workers=24`を固定したevaluation profileを作成した。profile identityは`candidate267-declared-instruction-read-permission-restoration-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1`である。Candidate264 result `1a64c1b2429c4e89aff3aedd6836944e`との比較preflightを`ready / authorized_20 / issued_0`で固定し、発行前capacity guard通過後に不足20件だけを発行した。

20 / 20件がvalidかつScore `4`だった。F01、F02、F03の正常経路は各5 / 5件、F10のexact instruction result先行と必要read完遂も各5 / 5件で成立した。一方、Candidate264比はtoken`+31.44%`、elapsed`+10.98%`だった。変更対象のF10はtoken中央値`+1.88%`、elapsed`-4.08%`だが、変更対象外のF01とF02でtoken中央値が`+30.81%`と`+67.61%`増えた。増加分を必要なinstruction dependencyまたは正常経路へ対応づけられないため、固定済み停止条件どおり追加NとStandard14へ進めない。

Candidate147を加えたcase別比較、external `wait`によるmodel再入、および再入以外のread分割・terminal検証後重複確認は、[`candidate267-candidate264-candidate147-cost-reentry-causal-audit.md`](candidate267-candidate264-candidate147-cost-reentry-causal-audit.md)へ分離して記録する。

現在状態は`design_complete / direct_base_candidate264 / candidate265_objective_retained / candidate265_self_classification_not_inherited / candidate266_diagnostic_only / candidate_created / static_verification_passed / targeted_n5_quality_passed / target_mechanism_passed / preserved_routes_passed / unjustified_cost_regression / stopped / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
