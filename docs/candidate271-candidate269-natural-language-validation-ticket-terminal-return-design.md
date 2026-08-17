# Candidate271 Candidate269自然語validation ticket terminal返却設計

## 結論

Candidate271はCandidate269 `the-caption-3ce91a4-natural-language-validation-carrier-closure-r1`を直接の実装親とする。予定prompt identityは`the-caption-3ce91a4-natural-language-validation-ticket-terminal-return-r1`である。

Candidate270は親にしない。Candidate270で追加した事後のresult対応づけは、F01・F02の10 / 10件で個別validation resultをAIへ返してから残りを発行する経路を開いた失敗反例としてだけ使う。

変更対象はroot `AGENTS.md`の`VALIDATION_CLOSURE`一節だけである。Candidate269の一回の外側validation実行を維持しながら、次の二つを一つの分離不能な境界として置換する。

1. validation開始前に、各validation、合格条件、実行identityおよび失敗・利用不能時に発行しなくなる後続を一つの実行票へ固定する。
2. 実行票に未実行または未完了のvalidationが残る間は、個別validation resultをAIへ返す外側invocationを発行対象にできない。resultをAIへ返せるのは、そのresultによって実行票全体が完了する場合だけである。

これにより、C269の過大全output carrierとC270のvalidation間model再入の両方を正常経路から外す。raw outputの抑制、byte上限、truncation、wrapper実装または成功runのtool順は指定しない。

## 置換する自然語本文

Candidate269の`VALIDATION_CLOSURE`四段落を次の四段落へ置換する。

> 変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。開始前に、各検証をその合格条件と実行identityへ対応づけ、失敗または利用不能になった場合に発行しなくなる後続とともに、一つの実行票へ固定する。
>
> rootが検証のproducerである場合は、順番のあるすべての必須検証を、その実行票を完了させる一回の外側実行へ束ねる。この外側実行をvalidation wrapperとする。各検証はwrapperの内側で結果を区別できる個別の実行として順に行い、その終了resultは開始前に固定した対応関係を継承する。実行票に未実行または未完了の検証が残る間は、個別検証のresultをAIへ返す外側invocationを発行してはならない。個別resultをAIへ返せるのは、そのresultによって、すべての必須検証が完了するか、失敗または利用不能に依存する残りの検証がすべて発行不能となり、実行票全体が完了する場合だけである。wrapperは実行票の完了状態と、開始前に固定した各検証の終了状態を一度だけ返す。各検証を一つのshell commandへ結合してはいけない。
>
> root以外が検証のproducerである場合も、すべての必須検証を、開始前に固定した対応関係を継承する個別の実行として一つのmodel stepから発行する。未完了の検証を残した個別resultをAIへ返さず、すべての検証が完了するか、失敗または利用不能に依存する残りの検証がすべて発行不能となった時に、実行票の完了状態と各検証の終了状態を一度だけ返す。
>
> 個別実行がresultを生成したという事実だけでは、そのresultは実行票の完了resultにならない。実行中に生じた記録は証拠として保持できるが、発行済みであることだけを理由に完了resultへ昇格させない。実行票の完了resultを受領した後に一度だけ完了を判断し、追加要求やresultの失効がなければreadや検証を追加しない。

## Candidate作成前の検討gate

### 1. 基準プロンプトセットと役割

- 直接の実装親はCandidate269であり、root `AGENTS.md`の`VALIDATION_CLOSURE`以外を同一byteで継承する。
- Candidate269の評価通過、採用、releaseおよびprojectionは継承しない。C269は一回の外側実行とterminal dependencyを成立させた一方、過大carrierを正常経路にした反例でもある。
- Candidate270は、事後の対応づけがwrapper迂回を開いた失敗反例であり、本文を継承しない。
- Candidate147は機序ごとの実測基準とKPI比較基準に限り、形式記法、本文、wrapper codeまたはtool順を継承しない。

### 2. 基準状態の最短正常経路

最短正常経路は、validation開始前の実行票固定、artifact変更、一回の外側validation実行、実行票全体を完了させる一回のresult返却、一回の完了判断である。外側実行がnonterminalなら、Candidate269から同一byteで保持する`VALIDATION_PLAN`に従い、同じcellのterminal resultだけを待つ。

個別validationは結果を区別できる個別実行として扱う。個別実行の終了状態は開始前の対応関係を継承し、AIがresult受領後に対応先を選ばない。

### 3. 保存traceで確認した誤経路

- Candidate269はF01・F02で一回の外側実行を使用したが、`発行済みの全result`を返却対象にした。F02中央値境界ではC147より外側resultが112,548文字大きく、最終model入力が15,624 token増えた。
- Candidate270は返却対象を対応づけ済みresultへ変えたが、対応づけのownerと時点を固定しなかった。F01・F02の10 / 10件で外側wrapperを使わず、focused validation resultをAIへ返してからfull validationを発行した。
- Candidate270ではvalidation後のdiffまたはstatusも10 / 10件で別の外側callになり、F03共同発行は0 / 5だった。

### 4. 既存の入力だけでは防げない理由

TaskSpecとcommand evidence protocolはrequired validation、順序およびcommandを固定するが、個別resultをいつmodel-visibleにできるか、resultの対応先を実行前と実行後のどちらで決めるかは固定しない。

Candidate269ではwrapper終了時に`発行済みの全result`を返せる。Candidate270では一件のvalidationがterminalなら、そのresultを個別validationの確定resultとしてAIへ返し、残りを別発行できる。どちらも現在のpromptへ準拠するため、条件判断の改善だけでは閉じない。

### 5. 変更する条件と責任範囲

- validationと合格条件の対応を、result受領後の作業からvalidation開始前の実行票へ移す。
- 各validationの実行identityと、失敗または利用不能によって発行しなくなる後続も同じ実行票へ固定する。
- model-visible result返却permissionを、個別validationのterminal状態ではなく実行票全体のterminal状態へ依存させる。
- 実行票全体のterminal状態を、全required validationの完了、または失敗・利用不能に依存する残りのvalidationがすべて発行不能になった状態に限定する。
- invocationがoutputを生成した事実と、実行票のcompletion resultを分離する。
- `DECISION_BOUNDARY`、`VALIDATION_PLAN`および他の全本文と全targetはCandidate269と同一byteで保持する。

これらは分割できない。実行前bindingだけではC270と同じ途中返却permissionが残り、返却禁止だけではC269と同じ過大全output carrierをcompletion resultへ昇格できるからである。

### 6. 実行できなくなる誤経路

次の辺を閉じる。

`実行票に未完了validationが残る -> 一件のvalidationだけterminal -> そのresultをAIへ返す外側invocationを発行 -> AIが対応づけ -> 残りを別発行`

最初のvalidationをトップレベルtool callとして発行すると、そのtool boundaryは個別resultをAIへ返して実行票を未完了のまま残すため、発行対象にできない。残りを同じ実行境界内で続行できる経路だけが合法になる。

同時に、`発行済みだから全outputをcompletion resultにする`経路も閉じる。必要な終了状態を保持するが、raw outputを捨てることや一定量へ制限することは要求しない。

### 7. 新しく増える判断、参照、例外

新しい自己分類、repository read、owner、ticket発行手順、command、byte上限、wait回数またはtool順は増やさない。実行票はCandidate269がすでに持つvalidation planの責任範囲を、開始前bindingと返却permissionへ接続する名称であり、別のartifactや外部runtimeを要求しない。

例外は、個別resultによって実行票全体がterminalになる場合だけである。これはAIが必要性を自己判断する例外ではなく、全required validationの終了状態と依存関係から決まる。

### 8. 評価ケース、KPIおよび機序基準

初回はCandidate271だけをF01・F02・F03・F10各N=5で評価する。全run Score `4`を要求し、KPIはcase別`total_tokens`・`elapsed_seconds`の中央値と全run分布を記録する。四ケース平均だけへ置き換えない。

対象機序はF01・F02でrun別に次を観測する。

- 各validation、合格条件、実行identityおよび停止依存が実行前に固定されたか。
- 実行票未完了時にchild validation resultをAIへ返したか。
- 一回の外側実行を維持したか。
- 発行済みinvocation output全件をcompletion resultへ昇格させたか。
- validation後にdiff、statusまたはrequired validationを別の外側callから再取得・再発行したか。
- nonterminal外側result後に同じcellのterminal resultだけを待ったか。

機序合格線を一律100%にしない。C147 N=20でvalidation分割がなかったF01は5 / 5、C147でvalidation分割が1 / 20あったF02は4 / 5以上を初回基準とする。nonterminal resultを実際に受けたrunのterminal dependencyは、C147保存済み観測が4 / 4だったため100%を要求する。

非対象影響は、C147 N=5の保存済み基準に合わせ、F03共同発行5 / 5、F10 instruction result先行2 / 5以上、F10 result後の必要read完遂5 / 5とする。Candidate269・270の成功率を理由に、C147が100%でなかったF10 instruction result先行を5 / 5へ引き上げない。

N=5はKPIの安定傾向を宣言する試験ではない。品質と機序が基準を満たした場合だけN=20へ拡張し、Candidate269 N=20とCandidate147 N=20を再実行せず比較する。Candidate270の低いKPIは誤経路によるため到達基準にしない。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F01またはF02で、実行票未完了時のchild result返却がC147基準を下回れば停止する。
- C269型の全issued output carrierとC270型のvalidation間model再入のどちらか一方を正常routeとして残した場合は停止する。
- 必須validationの欠落、failureの無視、terminal resultの補完または依存する後続の誤発行があれば停止する。
- F03共同発行、F10 instruction dependencyまたは必要read完遂が上記のC147基準を下回れば停止する。
- N=20でF01・F02のcase別token中央値がCandidate269より減らない場合、対象KPI原因仮説を棄却して停止する。
- C147との差はF01・F02ごとに示す。同じrouteでも差が残った場合だけ自然語側の残差として分析し、機序未達runと混ぜない。
- Standard14、採用、releaseおよびprojectionはN=20判定後の別作業とする。

## 作成前の反証確認

1. **C270の同義反復ではない**: 対応づけを事後作業として強めず、開始前bindingとticket terminal返却permissionへ責任を移す。
2. **C269の過大carrierを保持しない**: `発行済みの全result`を返却対象にしない。
3. **成功runの手順化ではない**: C147のwrapper code、tool順、command順、wait回数またはoutput上限を転記しない。
4. **必要resultを遮断しない**: 実行票の完了状態と各validationの終了状態を一度返し、failureとunavailableも返却対象に含む。
5. **raw output制御ではない**: 実行記録の保持を許し、抑制、truncationまたはbyte上限を要求しない。
6. **別predicateを混ぜない**: F03共同発行とF10 instruction dependencyの本文は変更せず、非対象影響としてだけ評価する。
7. **一律100% gateではない**: F02とF10はC147保存済み観測が100%でないため、Candidate271だけ100%へ引き上げない。

blocking counterexampleは0件である。Candidate271 bundleの作成を許可するが、評価profileと発行枠はbundleの静的identityを検証した後に作成する。

## 非目標

- stdout、stderrまたはtool output配送の抑制。
- byte上限、truncation、wait回数またはwrapper実装の固定。
- C147本文、形式記法または成功run codeの複写。
- F03共同発行またはF10 instruction dependency本文の変更。
- TaskSpec、case、fixture、oracle、rating contract、executorまたは外部runtimeの変更。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

Candidate bundleを作成した。prompt identityは`the-caption-3ce91a4-natural-language-validation-ticket-terminal-return-r1`、bundle SHA-256は`368d6e420b08ab1675834a15b828558c7ad4842e7c1d9155a870c1defc72ee89`である。Candidate269との差分はroot `AGENTS.md`の`VALIDATION_CLOSURE`一節だけであり、他の全targetは同一byteである。

四ケース各N=5を実行した。20 / 20件はScore `4`だったが、F01・F02の対象ticket routeは0 / 10件で、10 / 10件が個別validation resultをAIへ返して残りを別発行した。四ケース合算tokenはCandidate269比`-0.06%`で実質同水準、F02は`+3.03%`、F03共同発行は2 / 5だった。N=20へ進めず、結果は[`Candidate271 N=5`](../evaluations/results/candidate271-natural-language-validation-ticket-terminal-return-f01-f02-f03-f10-entrypoint-n5_2026-08-17.md)へ固定した。

現在状態は`design_gate_complete / candidate269_direct_implementation_parent / candidate270_failed_counterexample_only / candidate147_per_mechanism_and_kpi_reference / natural_language_only / candidate_created / evaluated_n5 / quality_passed / target_route_not_exercised / token_not_improved / f03_regressed / mechanism_failed / no_n20_extension / stopped`である。

後続の原因再分析では、Candidate271がCandidate269の直接の途中返却禁止をticket terminal、result種別および発行不能の自己分類へ置き換えたうえで、raw validation outputをticket completion stateだけへ投影するcarrier変更を同じ正常routeへ入れていたと判定した。後者はpromptだけでは安定して強制できないoutput配送境界であり、本設計の「新しい自己分類を増やさない」「raw output制御は非目標」という二つの宣言が実際の変更責務と一致していなかった。訂正後の現在解釈は[`Candidate271失敗とC81・C246の成立範囲差分析`](candidate271-failure-c81-c246-carrier-boundary-analysis.md)を正とする。
