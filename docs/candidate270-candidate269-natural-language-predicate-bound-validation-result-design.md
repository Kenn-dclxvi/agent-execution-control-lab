# Candidate270 Candidate269自然語predicate-bound validation result設計

## 結論

Candidate270はCandidate269 `the-caption-3ce91a4-natural-language-validation-carrier-closure-r1`を直接の実装親とする。予定prompt identityは`the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1`とする。

変更対象はroot `AGENTS.md`の`VALIDATION_CLOSURE`一節だけである。Candidate269が成立させた一回の外側validation wrapperとnonterminal時のterminal dependencyを保持し、同節で返却対象を`発行済みの全result`へ広げた現在差だけを置換する。各validationの完了resultを、対応するvalidation、合格条件および終了状態へ対応づけ、その確定resultが全件そろった場合だけ完了判断へ渡す。

これは成功stdoutを返さない制御、byte上限、wrapper実装または成功runのtool順ではない。C90〜C93・C96で成立しなかったtool output projectionを再提案しない。Candidate147はresult bindingの機序基準とKPI比較に使うが、形式記法、本文またはwrapperを複写しない。

## 置換する自然語本文

Candidate269の`VALIDATION_CLOSURE`四段落を次の四段落へ置換する。

> 変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。
>
> rootが検証のproducerである場合は、順番のあるすべての必須検証を、一つの実行票を完了させる一回の外側実行へ束ねる。この外側実行をvalidation wrapperとする。各検証はwrapperの内側で結果を区別できる個別の実行として順に行い、各resultを対応する検証と合格条件へ明確に対応づけ、終了状態まで確定させる。失敗または利用不能になった検証があれば、それに依存する後続を発行しない。個別検証の途中resultはAIへ返さず、すべての検証について対応づけ済みの確定resultがそろった後、wrapperが終了した時に一度だけ返す。各検証を一つのshell commandへ結合してはいけない。
>
> root以外が検証のproducerである場合も、すべての必須検証を、結果を区別できる個別の実行として一つのmodel stepから発行する。各resultを対応する検証と合格条件へ明確に対応づけ、終了状態まで確定させた後、対応づけ済みの確定resultを一度だけAIへ返す。失敗または利用不能になった検証に依存する後続は発行しない。
>
> すべての検証が成功し、各確定resultが対応する検証へ明確に対応づけられた場合に限り、一度だけ完了を判断する。追加要求やresultの失効がなければ、完了後にreadや検証を追加しない。

## Candidate作成前の検討gate

### 1. 比較基準と最短正常経路

- 直接の実装親はCandidate269、直接のKPI比較基準もCandidate269とする。
- Candidate269の評価通過、採用、releaseまたはprojectionは継承しない。F03共同発行4 / 5とcost退行は失敗反例として保持する。
- Candidate147は、result bindingがある状態の機序基準とKPIの到達基準に限る。
- 最短正常経路は、変更前evidence、artifact変更、一つの外側validation wrapper、全required validationの確定result受領、一回の完了判断である。
- 外側wrapperがnonterminalなら、Candidate269から保持する`VALIDATION_PLAN`に従い、同じcellのterminal resultだけを待つ。

### 2. 保存traceで確認した問題経路

F02の中央値境界runでは、内部command outputはC147がfocused 23,550文字・full 158,709文字、Candidate269がfocused 23,634文字・full 158,840文字でほぼ同量だった。それにもかかわらず、C147は外側carrierを2,000 tokenへ制限し、Candidate269は各outputを`evidence`配列へ保持して全件を再放出した。wait resultは8,358文字から120,906文字へ増え、Candidate269の最終model入力は15,624 token増えた。

Candidate269 F01では20 run中3 runがvalidation後に完了resultを再取得または再発行した。Candidate147 F01 N=20では同じ理由の再取得は0件だった。Candidate269 F02 N=20では一回待機route 6件の最終入力が約48,400〜49,700 token帯へ寄り、token中央値はCandidate147比`+24.19%`だった。

一方、Candidate147 F02にも80,595文字のcarrier resultが一件ある。したがって問題経路を「raw outputが一件でも返ること」または「外側上限が一定でないこと」と定義しない。問題はCandidate269が局所完了条件をpredicate-bound resultではなくissued invocation resultへ変更し、全output再配送を正規routeにしたことである。

### 3. 問題経路を許したpermissionとdependency

Candidate269のroot producer段落は「発行済みの全resultをwrapperが終了した時に一度だけ返す」と規定する。局所完了段落も「必要な結果がすべてそろった後」とし、各resultがどのvalidation predicateを確定したかを完了条件にしていない。

このため、発行した各invocationのoutputを全件保持・再放出し、そのcarrierから必要値を後で解釈する経路がCandidate269へ準拠する。TaskSpecとcommand evidence protocolはrequired validation、順序、合格条件を固定するが、wrapperが返すresultの対応先をinvocationとpredicateのどちらにするかは固定しない。

開いている依存は次である。

`required validation predicate -> issued invocation -> invocation output全件をcompletion resultとして採用 -> AIへ再配送 -> 必要値を再解釈して完了判断`

### 4. 変更する条件と責任範囲

- 変更targetはroot `AGENTS.md`だけである。
- Candidate269の`VALIDATION_CLOSURE`一節だけを上記四段落へ置換する。
- 各validation resultの対応先を、発行したinvocationではなく、対応するvalidationと合格条件へ戻す。
- resultは対応するvalidationの終了状態まで確定してから完了resultになる。
- すべてのvalidationについて対応づけ済みの確定resultがそろった場合だけ、wrapperの一回返却と完了判断へ進める。
- Candidate269の`DECISION_BOUNDARY`、`VALIDATION_PLAN`および他の全本文と全targetを同一byteで保持する。

### 5. 実行できなくなる問題経路

- invocationを発行したという事実だけでは、そのoutputをvalidationの完了resultとして採用できない。
- 対応するvalidation、合格条件または終了状態が未確定のresultを、全required validationがそろった証拠として完了判断へ渡せない。
- carrierから必要値を後で探し直してresultとの対応を補う経路は、事前のresult対応づけを満たさない。
- nonterminal resultをterminalとして補完する経路は、Candidate269から保持する`TERMINAL`と`VALIDATION_PLAN`に引き続き適合しない。

この変更はtoolがmodelへ返すeventや出力量を強制しない。raw outputが含まれるだけでは不成立にしないが、そのoutput全体を「発行済みだから」という理由だけでcompletion resultへ昇格させることはできない。

### 6. 維持する正常経路

- Candidate269の自然語だけで構成された全文。
- F01〜F03の開始確認と影響を受けない許可済みreadの共同発行。
- F10のinstruction result dependencyとresult後の必要read完遂。
- root producerがrequired validationを一回の外側wrapper内で区別可能な個別実行として扱う経路。
- failureまたはunavailable時に、それに依存する後続を発行しない経路。
- 外側wrapperのnonterminal result後に同じcellのterminal resultを待つ経路。
- root以外のproducerが同一model stepから個別validationを発行し、対応づけ済みresultを一度返す経路。

### 7. 新しく増える判断と対象外影響

新しい自己分類、ticket、owner、command、byte上限、stdout分類、待ち時間、wait回数またはtool順を追加しない。一般`TERMINAL`ですでに要求しているpredicateと確定resultの対応を、validation完了判断の局所節へ戻すだけである。

変更はartifact変更後のvalidationへだけ適用する。変更前read、F10のread-only review、worker選択、evidence admission、implementation bind、recoveryおよびcommand選択は変更しない。

### 8. 評価ケース、比較単位、判定順

初回はCandidate270だけを次の四ケース各N=5で評価する。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

品質は各runを個別に判定し、Score `4`を要求する。機序は次をrun別診断値として保存し、C147で品質との100%相関が確認されていないため、一律100%を合格線にしない。

- wrapperがissued invocation outputを全件completion resultとして扱ったか。
- 各required validationに対応づけ済みの確定resultを作ったか。
- validation後に完了resultを追加取得または再発行したか。
- nonterminal result後に同じcellのterminal resultを待ったか。
- F01〜F03共同発行とF10 instruction dependencyを保持したか。

N=5で品質を維持し、F01・F02の少なくとも一件でpredicate-bound result構成を観測できた場合だけN=20へ拡張する。N=20では保存済みCandidate269 N=20とCandidate147 N=20を再利用し、新規baselineを発行しない。

KPIはN=20で判定する。変更対象であるF01・F02・F03の合算`total_tokens`と`elapsed_seconds`がCandidate269よりともに減少した場合だけcost改善方向とする。F01・F02のcase別token中央値がCandidate147との差をCandidate269より縮めたかを別に示す。F10は変更対象外として、品質、依存経路およびKPI退行を別判定する。四ケースの平均へ置き換えず、case別中央値とrun分布を保持する。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば、追加Nへ進まない。
- N=5のF01・F02全runがissued invocation output全件をcompletion resultとして扱い、predicate-bound result構成を一件も観測できなければ仮説不支持で停止する。
- 必要validationの欠落、失敗resultの無視、terminal resultの補完またはF10の必要read欠落があれば停止する。
- F03共同発行またはF10 instruction dependencyの後退を、新しいresult bindingの成功で相殺しない。
- N=20でF01・F02・F03合算のtokenまたは経過時間がCandidate269より増えた場合はcost退行として停止する。
- N=20でF01・F02のtoken中央値がCandidate147との差をCandidate269より縮めなければ、今回のKPI原因仮説を棄却して停止する。
- Standard14、採用、releaseおよびprojectionは、N=20判定後の別作業とする。

## 作成前の反証確認

1. **C96の繰り返し**: stdout非配送、byte上限またはtool event projectionを要求しないため、C96と変更predicateが異なる。
2. **成功run手順の転記**: C147の2,000 token上限、wrapper code、command順またはtool順を転記しない。
3. **必要resultの欠落**: 対応するvalidation、合格条件、終了状態へbindした確定resultは必ず一度返すため、完了判断に必要な情報を遮断しない。
4. **失敗診断の遮断**: failureまたはunavailable resultも対応するvalidationの確定resultであり、返却対象から除外しない。
5. **C269 terminal closureの喪失**: 一回の外側wrapperとnonterminal時の同一cell dependencyを同一byteで保持する。
6. **F03・F10への混入**: 共同発行とinstruction dependencyの本文を変更せず、評価でも非対象影響として別判定する。
7. **一律100% gate**: C147にraw outputの大きな単発例があり、対象機序と品質の100%相関も未確認なので、raw output 0件や全run同一wrapper構成を要求しない。

blocking counterexampleは0件である。Candidate270 bundleの作成を許可するが、profileと評価枠はbundleの静的identityを検証した後に作成する。

## 非目標

- success stdout、stderrまたはtool output配送の抑制。
- byte上限、truncation、wait回数またはwrapper実装の固定。
- C147本文、形式記法または成功run codeの複写。
- F03共同発行またはF10 instruction dependency本文の変更。
- TaskSpec、case、fixture、oracle、rating contractまたはexecutorの変更。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

Candidate bundleを作成した。prompt identityは`the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1`、bundle SHA-256は`481a035966f1cc6ad8faba7fd05b07baf357d29e0a75dccc563963878547c439`である。Candidate269との差分はroot `AGENTS.md`の`VALIDATION_CLOSURE`一節だけであり、`DECISION_BOUNDARY`、`VALIDATION_PLAN`および他の全targetは同一byteである。

四ケース各N=5のprofileを作成し、Candidate269 N=5登録result `2398d22125bd4e658fe5b653679167b5`との比較preflightを`ready / authorized_20 / issued_0`で固定した。Candidate269 N=20登録result `544afbe7e2444037932c7313da4489b6`は、初期N=5のLayer 1生成基準ではなく、追加N後のKPI比較基準として保持する。

N=5を実行した結果、20 / 20件はScore `4`だったが、F01・F02の10 / 10件が一回の外側validation wrapperを使わず、required validation間のmodel再入を再開した。KPIはCandidate269より低下したが、設計対象のpredicate-bound carrierを実行した効果ではない。F03共同発行も0 / 5へ後退したためN=20へ進めない。結果は[`Candidate270 N=5`](../evaluations/results/candidate270-natural-language-predicate-bound-validation-result-f01-f02-f03-f10-entrypoint-n5_2026-08-17.md)へ固定した。

現在状態は`design_complete / candidate269_direct_implementation_parent / candidate269_failed_state_not_inherited / candidate147_mechanism_and_kpi_reference / natural_language_only / candidate_created / evaluated_n5 / quality_passed / kpi_decreased_by_bypass_route / target_mechanism_not_exercised / f03_regressed / mechanism_failed / no_n20_extension / stopped`である。

## 後続訂正

上記のN=5直後の判定は履歴として保持するが、現在判定には使わない。`codex-events.jsonl`の個別`command_execution`を外側tool callとみなしたため、wrapper内の逐次commandをvalidation間のmodel再入へ誤分類していた。persisted rolloutの`response_item`を直接監査した後続resultでは、Candidate270のF01、F02、F03は15 / 15件で単一outer call、wait-only継続、途中validation output 0 bytes、terminal output一件だった。

また、評価仕様は経路、model step、共同発行およびmechanism成立率を3 KPI差の診断情報とし、それらだけでKPI比較、追加NまたはStandard14を停止しない。したがって、この文書で固定したpredicate-bound result観測とF03共同発行による停止条件は、試験仕様上の採用gateとしては失効した。後続Standard14 N=5は70 / 70件がScore `4`、Candidate147比token `+18.16%`、elapsed `+9.09%`であり、現在状態は`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`とする。
