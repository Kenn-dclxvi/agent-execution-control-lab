# Candidate269 Candidate268自然語validation carrier閉鎖設計

## 結論

Candidate269はCandidate268 `the-caption-3ce91a4-natural-language-result-read-boundary-r1`を直接の親とする。予定prompt identityは`the-caption-3ce91a4-natural-language-validation-carrier-closure-r1`とする。

変更対象はroot `AGENTS.md`の`VALIDATION_CLOSURE`一節だけである。Candidate268で失われた、個別validationを一つの外側terminalへ束縛するcarrierを自然語で再接続する。nonterminal resultを受け取った後に同じcellを待つ禁止を追加するのではなく、その手前で、途中の個別resultをAIへ返さない一回の外側実行をvalidationのproducerへbindする。

F02共同発行はC147基準5 / 5に未達だが、C268本文ですでに禁止された分離を許す別のprompt準拠経路が未特定である。このCandidateへ推測のF02条件を混ぜない。C268の`DECISION_BOUNDARY`三段落を同一byteで保持し、F02は変更対象外の基準観測として評価する。

## 置換する自然語本文

Candidate268の`VALIDATION_CLOSURE`本文を次の四段落へ全置換する。

> 変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。
>
> rootが検証のproducerである場合は、順番のあるすべての必須検証を、一つの実行票を完了させる一回の外側実行へ束ねる。この外側実行をvalidation wrapperとする。各検証はwrapperの内側で結果を区別できる個別の実行として順に行い、各終了状態をwrapperの内側で確認する。失敗または利用不能になった検証があれば、それに依存する後続を発行しない。個別検証の途中resultはAIへ返さず、発行済みの全resultをwrapperが終了した時に一度だけ返す。各検証を一つのshell commandへ結合してはいけない。
>
> root以外が検証のproducerである場合も、すべての必須検証を、結果を区別できる個別の実行として一つのmodel stepから発行し、完了済みの全resultを一度だけAIへ返す。失敗または利用不能になった検証に依存する後続は発行しない。
>
> 必要な結果がすべてそろった後に一度だけ完了を判断する。追加要求やresultの失効がなければ、完了後にreadや検証を追加しない。

この置換はC147の形式定義、論理式または条項本文を複写しない。Candidate268の`VALIDATION_PLAN`に既にある、validation wrapperがcell IDを伴う未完了resultを返した場合の同じcellへの待機を変更しない。今回追加する関係は、その`validation wrapper`が何を所有し、どの時点でresultをAIへ返せるかというcarrier境界である。

## Candidate作成前の検討gate

### 1. 比較基準と最短正常経路

- 直接の親と直接比較基準はCandidate268である。
- Candidate147は機序ごとの基準線とKPIの診断比較に限る。
- 変更前調査、artifact変更、validation実行票の固定まではCandidate268と同じ経路を保持する。
- rootが検証producerなら、一回の外側実行の内側でrequired validationを結果の区別できる個別実行として順に完了し、完了済みresultを一度だけAIへ返す。
- 外側実行がnonterminal resultを返した場合だけ、Candidate268から保持する`VALIDATION_PLAN`に従って同じcellの完了を待つ。
- validation完了後は、追加要求またはresult失効がない限り追加toolを発行せず、一度だけ完了を判断する。

### 2. 保存traceで確認した問題経路

Candidate268四ケース各N=5では、20 run中13 runでvalidation invocationがcell ID付きnonterminal resultを返した。13 runすべてで同じcellを待たず、3件は別`exec`へ進み、10件は追加toolなしで終了した。全20件は保存workspaceから後に収集したcommand evidenceによりScore `4`だったが、実行時のterminal result受領を意味しない。

Candidate147の同じ四ケース各N=5では、nonterminal resultを受けた4 runすべてが同じ完了を待った。Candidate147でexternal `wait`自体がなかったのは16 / 20件なので、次Candidateへ`wait=0`またはmodel再入0件を100% gateとして要求しない。要求するのは、実際にnonterminal resultを受けたrunがそれをterminalとして扱わないことだけである。

### 3. 問題経路を許したpermissionとdependency

Candidate268の`VALIDATION_PLAN`は、cell ID付きnonterminal resultの後に同じcellを待つよう明示している。しかし`VALIDATION_CLOSURE`は、個別validationの途中resultをAIへ返さないよう要求するだけで、個別validationを一つの外側実行へbindしていない。

このため、個別invocationを別々のmodel-visible resultとして返した後、`wait`指示に従うかどうかをモデルの次判断へ残す。開いている経路は次である。

`validation実行票 -> 外側carrierへ未bindの個別invocation -> 個別resultをAIへ返す -> nonterminal result -> 別toolまたはfinalへ進む`

TaskSpec、repository authorityおよび現在状態はrequired validationと合格条件を定めるが、それらの個別resultを一つの外側terminalへ束縛しない。このcarrierはpromptで明示する必要がある。

### 4. 変更する条件と責任範囲

- 変更targetはroot `AGENTS.md`だけである。
- Candidate268の`VALIDATION_CLOSURE`一節だけを上記四段落へ置換する。
- root validation producerへ、一つの実行票を完了させる一回の外側実行をbindする。
- 個別validationは外側実行の内側で区別可能なまま保持し、shell compound commandへ結合しない。
- 個別validationの終了状態は外側実行の内側で確認し、失敗または利用不能時は依存する後続を発行しない。
- 個別validationの途中resultをAIへ返さず、発行済みの完了resultを外側実行の終了時に一度だけ返す。
- root以外のproducer経路では、個別validationを一つのmodel stepから発行し、完了済みresultを一度だけ返す関係を保持する。
- Candidate268の`VALIDATION_PLAN`、`DECISION_BOUNDARY`および他の全本文と全targetを同一byteで保持する。

### 5. 実行できなくなる問題経路

- root producerの個別validation resultは外側実行の途中でAIへ返らないため、その途中resultを受けて別toolまたはfinalへ進む経路を構成できない。
- 外側実行がnonterminalになった場合は、Candidate268から保持する`VALIDATION_PLAN`により同じcellへの待機だけが許される。別tool、判断、進捗出力またはfinalへ進む経路はpromptに適合しない。
- 個別validationを一つのshell commandへ結合して結果identityを失う経路は許可しない。
- 一件の失敗または利用不能を無視して依存する後続validationへ進む経路は許可しない。

### 6. 維持する正常経路

- F01、F02、F03の開始確認と許可済みreadの共同発行。
- F10のinstruction result dependencyとresult後の必要read完遂。
- 必須validationを順番どおり個別に実行し、各結果とexit stateを区別する経路。
- 先行validationが成功した場合だけ依存する後続validationへ進む経路。
- 外側実行がterminal resultを返した場合、追加のwaitを行わず完了判断へ進む経路。
- 外側実行がnonterminal resultを返した場合、同じcellを必要回数待って完了resultを受領する経路。
- root以外が検証producerである場合の個別result識別と一回の集約返却。

### 7. 新しく増える判断と対象外影響

新しい自己分類、ticket、owner、成功手順、command、待ち時間またはwait回数を追加しない。増えるのは、root producerのvalidation実行票を一回の外側実行へbindし、その外側実行が個別resultを返す時点を所有する関係だけである。

この差分はartifact変更後のvalidationだけへ適用する。変更前read、F10のread-only review、worker選択、evidence admission、implementation bind、recoveryおよびcommand選択は変更しない。

### 8. 評価ケース、基準線、比較単位

初回評価はCandidate269だけを次の四ケース各N=5で行う。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

直接比較には保存済みCandidate268の同じ四ケース各N=5を使い、Candidate268を再実行しない。Candidate147は機序ごとの基準線とKPIの診断比較に限る。

機序合格線はC147の同範囲実測に合わせる。

| 観測項目 | 合格線 |
| --- | ---: |
| F01 開始確認・許可済みread共同発行 | 5 / 5 |
| F02 開始確認・許可済みread共同発行 | 5 / 5 |
| F03 開始確認・許可済みread共同発行 | 5 / 5 |
| F10 instruction result先行 | 2 / 5以上 |
| F10 result後の必要read完遂 | 5 / 5 |
| nonterminal resultのterminal dependency | 観測したnonterminal runの100% |

external `wait`なしとF02 truncationなしは機序gateにしない。nonterminal runが0件ならterminal dependencyは`unobserved`とし、合格へ補完しない。品質、対象機序、変更対象外影響、all-agent `total_tokens`および`elapsed_seconds`を分離する。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F01、F02またはF03が上記C147基準線へ届かなければ停止する。
- F10 instruction result先行が2 / 5未満、または必要read完遂が5 / 5未満なら停止する。
- nonterminal resultを受けたrunが一件でも別tool、判断、進捗出力またはfinalへ先に進んだ場合は停止する。
- nonterminal resultが0件でterminal dependencyを観測できなければ、機序を通過扱いにせず`unobserved`で停止する。
- Candidate268比でtokenまたは経過時間が増えた場合、terminal closureまたは必要な正常経路へ対応づけられなければ`unjustified_cost_regression`とする。対応づけられる場合も自動採用せず`tradeoff_requires_human_judgement`とする。
- 初回N=5を判定する前に追加N、Standard14、採用、releaseまたはprojectionへ進めない。

## 作成前の反証確認

次の反例を確認した。

1. **途中resultが必要な順序制御**: 終了状態は外側実行の内側で確認するため、AIへ途中resultを返さなくても失敗時停止を実行できる。
2. **result identityの消失**: 個別validationを一つのshell commandへ結合せず、区別できる個別実行として保持するため、各resultとexit stateを失わない。
3. **外側実行自体のnonterminal**: Candidate268から保持する`VALIDATION_PLAN`が同じcellへの待機だけを許すため、terminal resultまで継続できる。
4. **read-only F10への過剰適用**: 変更後validationだけを対象とするため、F10のinstruction readと配下readには適用しない。
5. **変更前共同発行への過剰barrier**: `DECISION_BOUNDARY`と変更前evidenceを同一byteで保持するため、新しい外側実行を開始確認やsource readへ適用しない。
6. **worker経路の欠落**: root以外のproducerについて、個別実行、一つのmodel step、完了済みresultの一回返却を別段落で保持する。
7. **成功run手順の転記**: command、tool順、待ち時間、wait回数は固定せず、必要なresult carrierとterminal dependencyだけを固定する。

blocking counterexampleは0件である。Candidate作成gateを通過し、上記一節だけを変更するCandidate269 bundleの作成を許可する。profileまたは評価枠はbundleの静的identityを検証した後に限る。

## 非目標

- F02共同発行文の推測変更。
- C147本文または形式記法の複写。
- Candidate254への差し戻し。
- external `wait`、model再入またはtruncationを0件へすること。
- command、tool順、待ち時間、wait回数または成功runの手順化。
- carrier容量、success stdoutまたは部分truncationの同時解決。
- TaskSpec、case、fixture、oracleまたはrating contractの変更。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

Candidate bundleを作成した。prompt identityは`the-caption-3ce91a4-natural-language-validation-carrier-closure-r1`、bundle SHA-256は`19630df248b648690238757813941f55e97aa82c8b5597659a9e731d0877162f`である。Candidate268との差分はroot `AGENTS.md`の`VALIDATION_CLOSURE`一節だけであり、`DECISION_BOUNDARY`、`VALIDATION_PLAN`および他の全targetは同一byteである。

Candidate bundleの静的検証後、C268の保存済み四ケース各N=5を直接基準に初回N=5を実行した。20 / 20件がvalidかつScore `4`で、terminal dependencyはC268の0 / 13から9 / 9へ回復した。F01、F02、F10も合格線を満たしたが、変更対象外のF03共同発行がCandidate147基準5 / 5に対して4 / 5となったため停止した。結果は[`Candidate269四ケースN=5`](../evaluations/results/candidate269-natural-language-validation-carrier-closure-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)を正本とする。

現在状態は`design_complete / candidate268_direct_parent / natural_language_only / validation_carrier_reconnection / terminal_dependency_passed_9_of_9 / f01_f02_f10_passed / f03_failed_4_of_5 / quality_passed / mechanism_failed / stopped / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
