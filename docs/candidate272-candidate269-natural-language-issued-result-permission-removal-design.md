# Candidate272 Candidate269自然語issued result permission除去設計

## 結論

Candidate272はCandidate269 `the-caption-3ce91a4-natural-language-validation-carrier-closure-r1`を直接の実装親とする。予定prompt identityは`the-caption-3ce91a4-natural-language-issued-result-permission-removal-r1`である。

変更対象はroot `AGENTS.md`の`VALIDATION_CLOSURE`一文だけとする。Candidate269が成立させた一回の外側validation wrapper、個別validationの途中resultをAIへ返さない直接禁止、failure時の停止およびnonterminal時の同一cell dependencyは保持する。

Candidate269が追加した`発行済みの全result`という返却対象だけを除く。発行したinvocationがoutputを生成した事実から、その全outputをcompletion resultとして返せるpermissionを失効させる。代わりのpredicate対応づけ作業、ticket terminal分類、output種別、byte上限またはwrapper手順は追加しない。

Candidate270とCandidate271は親にしない。両Candidateは、上記permissionの変更と同時に新しい実行中分類を加え、F01・F02の10 / 10件でCandidate269のwrapper routeを失った失敗反例としてだけ使う。

## 置換する自然語本文

Candidate269 root `VALIDATION_CLOSURE`の次の一文を置換する。

変更前:

> 個別検証の途中resultはAIへ返さず、発行済みの全resultをwrapperが終了した時に一度だけ返す。

変更後:

> 個別検証の途中resultはAIへ返さず、wrapperが終了した時に一度だけ結果を返す。

同じ段落の他の全文、root以外のproducer段落、完了判断段落、`VALIDATION_PLAN`および他の全節はCandidate269と同一byteで保持する。

## Candidate作成前の検討gate

### 1. 目的と比較対象

`task_objective := Candidate254を自然語基盤とする改善系列を維持し、C147までに成立したvalidation間model再入閉鎖と完了resultの利用関係をC269の一回wrapperへ復元し、品質を維持したうえでC147と誤差とはいえないcase別token・経過時間差を縮める`

- 直接の実装親: Candidate269。
- KPI比較基準: Candidate147 N=20とCandidate269 N=20。
- Candidate270・Candidate271: 新しい分類を加えてwrapperを失った失敗反例。本文を継承しない。
- Candidate147: 機序別の実測基準とKPI比較基準。形式本文、wrapper code、output上限または成功runのtool順を継承しない。
- Candidate254: 現在系列の自然語基盤と、必要result受領後に一度判断する既存関係の由来。直接のbundle親には戻さない。

### 2. Candidate269で成立済みの保持効果

- root producerのrequired validationを一回の外側wrapperへ束ねる。
- wrapper内で各validationを区別可能な個別実行として順に行う。
- 個別validationの途中resultをAIへ返して残りを別発行しない。
- failureまたはunavailableなら依存する後続を発行しない。
- nonterminal result後は同じcellのterminal resultだけを待つ。
- F10でTaskSpec明示の`AGENTS.md`成功resultを同一directory配下readのdependencyにする。

これらは一件も再設計せず、変更対象一文以外を同一byteで保持する。

### 3. 保存traceで確定した失敗route

Candidate269は返却対象を`発行済みの全result`とした。F02中央値境界runでは、C147と内部test出力量がほぼ同じだったにもかかわらず、全raw outputを保持・再放出し、外側resultが8,358文字から120,906文字へ増えた。完了判断のmodel入力は15,624 token増えた。

F01では、raw outputと完了判定用diff・statusを同じinvocation-owned carrierへ入れた後、必要な完了resultを利用できず再取得または再発行したrunが3 / 20件あった。C147 F01 N=20では同じ理由の再取得は0 / 20件だった。

開いている辺は次である。

`validation invocationを発行した -> outputが生成された -> 発行済みであるため全outputを返却対象にできる -> raw output受領を必要result受領として扱える`

### 4. 既存入力だけで正常routeが成立する理由

広い局所permissionを除いても、必要resultのownerと完了条件は未定にならない。

- 一般`TERMINAL`は、全predicateについてbind済みproducerのterminal resultがある場合だけoperationをterminalにする。
- 自然語`VALIDATION_PLAN`は、必須validationと完了判定用diff・statusを一つの実行票へ開始前に固定する。
- 同節は、全result受領後に一度だけ完了を判断し、追加要求またはresult失効がなければtoolを追加しない。
- 自然語`EVIDENCE_GATE`は、変更または失敗で入力が変わったpredicateだけを失効させ、必要な事実がそろった後の再確認を許さない。

したがって返却時点だけを`wrapper終了時に一度`へ固定すれば、必要resultの資格は既存の一般関係から決まる。Candidate270のように各resultを実行中に再対応づける作業や、Candidate271のようにcompletion resultの種類を分類する必要はない。

### 5. 閉じるpermissionと残すmethod

閉じるのは、`発行済みinvocationのoutputである`ことだけを全件返却の十分条件にするpermissionである。

閉じないものは次のとおりである。

- success stdoutがtool resultに含まれること。
- 外側carrierのbyte量、truncationまたは上限。
- wrapper内部で結果を保持する実装方法。
- failure診断に必要なoutput。
- executorがpermission内で選ぶ未指定method。

C147にも80,595文字の大きなcarrierが一件あるため、raw output 0件またはcompact carrier 100%を機序合格線にしない。今回の機序はoutput投影ではなく、invocation ownershipから返却permissionを作れなくすることである。

### 6. Candidate270・Candidate271と同じ失敗を繰り返さない理由

- `resultをvalidation、合格条件、終了状態へ明確に対応づける`というC270の実行中作業を追加しない。
- ticket、child result、completion result、発行不能というC271の状態分類を追加しない。
- C269のwrapper、途中返却禁止およびreturn timingを同じ文構造で保持する。
- `発行済みの全result`だけを除き、別の返却対象集合を新設しない。
- C147の2,000 token上限、wrapper codeまたは成功runのtool順を転記しない。

### 7. 評価ケースと機序基準

初回はCandidate272のF01・F02・F03・F10を各N=5で評価する。全runを個別採点し、Score `4`を要求する。

機序はC147のcase別実測へ合わせる。

- F01 validation分割なし: C147 N=20が20 / 20のため、初回5 / 5を要求する。
- F02 validation分割なし: C147 N=20が19 / 20のため、初回4 / 5以上とする。
- nonterminal result後の同一cell terminal dependency: C147保存観測4 / 4に合わせ、該当runの100%を要求する。
- F01の同じ理由による検証後result再取得なし: C147 N=20が20 / 20のため、初回5 / 5を要求する。
- F03の開始確認と影響を受けないreadの共同発行: C147の初回保存観測5 / 5に合わせ、初回5 / 5を要求する。
- F10のinstruction result先行: C147の目的未達の安いrouteを合格扱いせず、Candidate269 N=5の5 / 5を初回保持基準とする。N=20ではCandidate269の18 / 20を下回らないことを要求し、新たに20 / 20へ引き上げない。
- F10のinstruction result後の必要read完遂: C147保存観測5 / 5に合わせ、初回5 / 5を要求する。

raw output非配送率、carrier文字数または特定tool引数は機序基準へ入れない。

### 8. KPI判定と追加N

N=5は品質、route保持および重大な退行の停止判定に使い、安定したKPI傾向を宣言しない。機序基準を満たした場合だけCandidate272を各ケースN=20へ拡張し、保存済みC147 N=20とCandidate269 N=20を再実行せず比較する。

N=20では次をcase別に示す。

- `total_tokens`と`elapsed_seconds`の全run分布と中央値。
- C269との差、およびC147との差が縮んだか。
- F01の完了result再取得、validation分割、追加read。
- F02の通常route、一回待機route、追加outer callおよびcarrier文字数分布。
- compact carrier率を新しい100% gateにせず、C147の分布から外れた一律過大配送が解消したか。

四ケース平均だけへ置き換えない。F01の改善でF02の悪化を相殺せず、caseごとに原因とKPIを判定する。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F01・F02でC147基準を超えるvalidation分割があれば停止する。
- C269の一回wrapperを失い、C270・C271型のvalidation間model再入が再発した場合は停止する。
- required validation、完了判定用result、failureまたはunavailable resultを欠落させた場合は停止する。
- F03共同発行またはF10 instruction dependencyが固定済み基準を下回れば停止する。
- N=20でF01の完了result再取得がC147基準へ戻らなければ、permission除去の対象機序を棄却する。
- N=20でF02のtoken分布がCandidate269から改善せず、`発行済み`permission除去がcarrier methodへ影響しなければ、F02 KPI仮説を棄却する。output capやsummary指定へ進まない。
- Standard14、採用、releaseおよびprojectionはN=20判定後の別作業とする。

## 作成前の反証確認

1. **C270の再試行ではない**: predicate-bound resultを作る新しいoperationを追加せず、C269が追加した局所permissionだけを失効させる。
2. **C271の再試行ではない**: ticket terminalやresult種別の自己分類を使わない。
3. **output projectionではない**: stdout非配送、byte上限、summaryまたはtool event projectionを要求しない。
4. **必要resultを失わない**: 一般`TERMINAL`と既存`VALIDATION_PLAN`が必要resultと完了条件を保持する。
5. **成功runの手順化ではない**: C147のtool順、wrapper code、wait上限またはcompact runを転記しない。
6. **新しい100% gateではない**: C147が100%だった機序だけ100%とし、F02 validation分割とcarrier表現を100%へ引き上げない。
7. **目的をF01へ縮小しない**: F01のresult再取得とF02のcase別KPIを別々に判定し、F02未改善をF01改善で相殺しない。

blocking counterexampleは現時点で0件である。Candidate272 bundleの作成は許可するが、この文書ではbundle、profile、評価枠、実行、採用またはreleaseを作成していない。

この記述は作成前gateを固定した時点の状態である。その後、Candidate272 bundleを作成し、四ケース各N=5を評価した。20 / 20件はScore `4`、required validation間のAI再入はF01 5 / 5、F02 4 / 5、F10 instruction dependencyは5 / 5だった。しかしraw rollout基準のF03共同発行は3 / 5で、C147の5 / 5を下回った。さらにF01・F02の10 / 10件でfull gate raw outputがwrapper carrierへ入り、outer resultにもraw stdoutが残った。F01の1 / 5件は埋もれたdiff / statusを再取得した。F01・F02 token中央値はCandidate269比`+18.04%`・`+32.15%`である。

作成前仮説の「明示permissionを除けば、既存の一般関係だけで必要resultの資格が決まる」は保存traceで反証された。明示permissionの不在はdenyではなく、`wrapperが終了した時に一度だけ結果を返す`という残存文の下で全raw command resultを返す既定経路が合法なまま残った。評価結果は[`Candidate272 N=5`](../evaluations/results/candidate272-natural-language-issued-result-permission-removal-f01-f02-f03-f10-entrypoint-n5_2026-08-17.md)を正とする。

現在状態は`design_gate_complete / candidate269_direct_implementation_parent / candidate270_candidate271_failed_counterexamples_only / candidate147_mechanism_and_kpi_reference / candidate254_natural_language_lineage_preserved / candidate_created / evaluated_n5 / quality_passed / validation_route_shape_passed / f03_mechanism_failed / target_permission_mechanism_failed / major_case_kpi_regression / no_n20_extension / stopped`である。
