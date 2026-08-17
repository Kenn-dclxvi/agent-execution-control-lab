# Candidate270失敗後の次自然語route閉鎖分析

## 結論

Candidate270のKPI低下を、C269で特定した原因がそのまま解消した結果とは扱えない。C269とC270は、同じvalidationを別の高費用routeで実行した。

- Candidate269は一回の外側validation wrapperを保持したが、`発行済みの全result`を完了resultへ昇格させ、raw validation outputを一つのmodel-visible carrierへ大量に再配送した。
- Candidate270は`各resultを対応する検証と合格条件へ明確に対応づける`ことを追加したが、F01・F02の10 / 10件でwrapperを使わず、各validation resultをAIへ返してから残りを発行した。

したがって次に閉じる辺は、stdout量、byte上限、wait回数またはwrapper実装ではない。validation開始前に各validationとその実行を一意に対応づけ、validation ticket全体が未完了な間は、個別validation resultをAIへ返す外側invocationを発行できない関係である。個別実行が生成したoutputは、その事実だけではticketのcompletion resultにならない。

Candidate270の追加文は継承しない。一方、Candidate270は「事後に各resultを明確に対応づける」という要求がwrapper迂回routeを開いた反例として次設計へ必ず残す。実装byteの親はCandidate269とし、Candidate270を失敗反例にするのが最短である。これはC254へ戻ることではなく、C269までの成立routeとC270で得た負の知見を同時に保持する関係である。

## KPIで起きたこと

### N=5ケース別中央値

| ケース | C147 token | C269 token | C270 token | C269からの減少 | C147との差 | C269からC147までの差を回収した割合 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,202 | 163,264 | 121,788 | `-41,476`（`-25.40%`） | `+14,586`（`+13.61%`） | `73.98%` |
| F02 | 128,236 | 166,758 | 138,017 | `-28,741`（`-17.24%`） | `+9,781`（`+7.63%`） | `74.61%` |
| F03 | 104,320 | 133,527 | 128,806 | `-4,721`（`-3.54%`） | `+24,486`（`+23.47%`） | — |
| F10 | 87,934 | 115,122 | 114,084 | `-1,038`（`-0.90%`） | `+26,150`（`+29.74%`） | 目的未達C147 routeを含むため不使用 |

四ケース合算中央値はCandidate269の569,253 tokenからCandidate270の532,952 tokenへ`-6.38%`、経過時間は368.193秒から286.186秒へ`-22.27%`だった。品質は両方100である。

F01・F02では、C269からC147までのtoken差の約74%がC270で消えた。これはC269の過大carrierが大きな費用だったという原因仮説を支持する。ただしC270はC147と同じrouteへ戻らず、required validation間のmodel再入を再開したため、残り約26%を「自然語固有費用」と確定できない。

F10は変更後validationを持たないread-only caseで、C269からのtoken差が`-0.90%`にとどまった。C270の大きな削減がprompt全体の文字数または自然語一般の効果ではなく、validationを持つcaseのroute変更に対応していることを示す。C147の目的達成済み5応答route 108,454 tokenと比べたC270中央値は`+5.19%`で、F10の新しいinstruction result dependencyを維持した通常費用の範囲にある。

## traceで確認したroute差

| 観測 | Candidate269 | Candidate270 | 読み取れること |
| --- | ---: | ---: | --- |
| F01・F02の外側validation wrapper | 正常routeとして使用 | 0 / 10 | C270はC269のcarrierを修正せず迂回した |
| required validation間にresultをAIへ返却 | wrapper内で抑止 | 10 / 10 | C69・C71で閉じたmodel再入が再開した |
| validation後のdiff / statusを別の外側callで取得 | C269 F01 N=5では問題route 3件 | 10 / 10 | C270では完了resultの別取得が通常routeになった |
| F03開始identityと影響を受けないreadの共同発行 | 4 / 5 | 0 / 5 | 保持すべき既知境界を再現できていない |
| F10 instruction result dependency | 5 / 5 | 5 / 5 | 新目的に必要な依存は保持した |

C270のF01・F02では、focused testが完了してmodelへ返った後にfull testを発行し、その完了後にdiffまたはstatusを別発行した。外側wrapperのnonterminal resultを待ったrunや、一回carrier内で全validationを完了したrunは0件だった。

この差はvalidation command、出力量または品質の差ではない。Candidate269とCandidate270のTaskSpec、case、fixture、required validation、rating、model、reasoning、runtime、permissionおよびexecutorは同一であり、prompt差はroot `VALIDATION_CLOSURE`だけである。

## C5からC147までの既知知見との対応

### C69・C71

Candidate69は、shell command数ではなくtop-level tool cycleがtokenと強く対応することを確認した。同一case中央値を除いた相関は、all-agent tokenに対してtop-level tool call `0.9148`、shell command数`0.2357`だった。

Candidate71は完全に確定したvalidation集合について、個別validationの間でmodelへ戻らないことで、Candidate69比token中央値`-28.52%`、top-level tool call `469 -> 338`、model step `539 -> 408`を記録した。C270の10 / 10件は、この既知の効率leverを逆向きに開いた。

### C80・C81

Candidate80はroot wrapperを指定しても1-step closureが9 / 10だった。失敗runはTaskSpecの「順に」「個別」をトップレベル逐次実行として解釈した。

Candidate81は「順に」「1 commandずつ個別」をwrapper内の発行順とinvocation単位へ対応づけ、command resultをmodelへ返して別callから次を発行する意味ではないと固定した。F04で10 / 10、Standard14の複数required-command caseで35 / 35の1-step closureを記録した。

Candidate270はwrapperの内側で個別に行うと書いていたが、追加したresult対応づけをどの主体が、いつ完了させるかを固定しなかった。トップレベルで各commandを発行すれば、tool result自体がcommand identityと終了状態を持つため、AIが最も容易に「明確な対応づけ」を作れる。結果としてC81が閉じた逐次解釈が再び選ばれた。

### C243からC246

Candidate244の「途中結果を次の発行判断に使わない」は2 / 5しか閉じず、Candidate245の「判断側へ返さない」も1 / 5しか閉じなかった。Candidate246が、順に行う必須検証の途中resultを`AI`へ返してから残りを実行してはならないと返却先を固定すると5 / 5で閉じた。

Candidate270にも`AI`はあったが、対象を`個別検証の途中result`と表現したうえで、各resultを個別validationの終了状態まで確定させることを追加した。この組合せでは、focused testの終了resultは「個別検証の途中result」ではなく「一件の検証について確定したresult」と解釈できる。validation ticket全体は未完了でも、その確定resultをAIへ返して次へ進むrouteを強く誘発した。

## Candidate270本文が開いたpermissionとdependency

Candidate270が意図したrouteは次である。

`validation ticket発行 -> wrapper内で各validation実行 -> 各resultをvalidationへ対応づけ -> ticket terminal -> 一回返却`

実際に選ばれたrouteは次である。

`validation Aをトップレベル発行 -> Aのterminal resultがAIへ返る -> AIがAへ対応づけ -> validation Bをトップレベル発行 -> Bのterminal resultがAIへ返る -> AIがBへ対応づけ -> diff / statusを別発行 -> 完了判断`

後者が選べた理由は三つある。

1. resultの対応づけがvalidation開始前のbindではなく、result受領後の作業として読める。
2. 対応づけのownerがwrapperまたはticketではなく、resultを受け取るAIでも成立する。
3. AIへ返してはならない対象が、ticket未完了時の全child resultではなく、各個別validationの`途中result`と読める。

開いている辺は次である。

`ticket内に未実行validationが残る -> 一件のvalidationはterminal -> そのresultをAIへ返すtop-level invocationを発行可能 -> AIが事後にpredicateへ対応づけ -> 残りを別発行可能`

これは「wrapperを使うべき」という条件判断の失敗ではない。top-level invocationの発行permissionと、そのtool resultをAIへ返せるdependencyが閉じていなかったことが原因である。

## 次に変更すべき一つの境界

次設計では、result受領後にAIが対応づける作業を追加しない。validation ticketを発行する前に、各required validation、個別の合格条件、実行identityおよび停止時の依存関係を一つのticketへ固定する。個別実行のterminal resultは、その事前bindingをそのまま継承し、後から対応先を選ばない。

そのうえで、ticketが未完了の間にmodel-visible resultを返す外側invocationの発行permissionを閉じる。個別validation resultをAIへ返せるのは、そのresultによってticket全体がterminalになる場合だけである。ticket terminalとは、全required validationがterminalになった場合、または失敗・利用不能によって未実行の依存validationがすべて発行禁止になった場合を指す。

この関係によって、最初のvalidationをトップレベルtool callとして発行すると、そのtool boundaryがresultをAIへ返してticket未完了のままになるため、発行対象にできなくなる。残りをAIへ戻らず続行できる同じ実行境界だけが正常routeとして残る。

個別invocationのraw stdoutやstderrは実行証拠であり、生成されたという理由だけでticket completion resultにはならない。一方、raw outputの非配送、byte上限、truncationまたは特定のsummary形式は要求しない。ticket completion resultが持つ必要があるのは、事前にbindした各validationのterminal状態と、ticketがterminalになったことだけである。

## 次設計で維持するもの

- Candidate269の一回の外側validation実行とnonterminal時の同一cell terminal dependency。
- validation開始前にrequired validation、順序、合格条件、停止条件、diff / statusを一つの実行票へ固定する関係。
- 各validationを一つのshell commandへ結合せず、結果を区別できる個別実行として扱うこと。
- failureまたはunavailable時に、それへ依存する後続だけを発行しないこと。
- F01〜F03の開始identityと影響を受けないreadの共同発行。
- F10のinstruction result dependencyと必要な配下readの完遂。
- 自然語だけで構成すること。

## 次設計へ持ち込まないもの

- Candidate270の`各resultを対応する検証と合格条件へ明確に対応づける`という事後対応づけ要求。
- Candidate269の`発行済みの全result`というinvocation所有の返却対象。
- C147の形式記法、本文、wrapper code、成功runのtool順またはoutput上限。
- stdout抑制、byte上限、truncation、wait回数または特定commandの固定。
- F03共同発行を同じCandidateで修正する追加文。F03は保持効果として評価するが、validation result境界と別predicateを同時変更しない。

## 追加試験の判断

Candidate270の追加Nは不要である。F01・F02の10 / 10件で同じwrapper迂回routeが観測され、対象機序を一件も実行していない。Nを増やしてKPI中央値の精度を上げても、Candidate270の効果としてpredicate-bound carrierを評価できない。

次Candidateでは、まずF01・F02で次をrun別に観測する。

- ticket未完了時にchild validation resultをAIへ返したか。
- 各validation identityと合格条件が実行前に固定され、terminal resultがそのbindingを継承したか。
- 一回の外側実行を保持したか。
- completion resultとは別にraw invocation output全件をcompletion resultへ昇格させたか。
- validation後にdiff / statusまたはrequired commandを別の外側callから再取得・再発行したか。
- nonterminal outer result後に同じcellのterminal resultだけを待ったか。

KPIはcase別token・経過時間の中央値と全run分布を保持する。C147、Candidate269、Candidate270との比較を行うが、機序を実行していないCandidate270のKPI低下を次Candidateの到達基準にはしない。F03は共同発行、F10はinstruction dependencyを非対象影響として別に確認する。合格線は次Candidate設計時にC147の保存済み観測率へ合わせて固定し、観測されていない機序を自動的に100%へしない。

## 現在の判断

原因仮説は次のように更新する。

- `C269の過大carrierがF01・F02の大きなtoken差を作った`: 支持される。C270はC269からC147までのN=5 token差を両caseで約74%回収した。
- `C270がC147のpredicate-bound result機序を復元した`: 棄却する。wrapper内での対象機序は0 / 10だった。
- `自然語ではC147と同じcostへ到達できない`: 未確定。C270は別routeなので、この仮説を判定できない。
- `次に必要なのはoutput制御`: 棄却する。必要なのはticket未完了時のmodel-visible result返却permissionと、実行前bindingである。

現在状態は`candidate270_detailed_failure_analysis_complete / candidate269_carrier_cost_hypothesis_supported / candidate270_predicate_binding_restoration_rejected / next_boundary_pre_execution_binding_and_ticket_terminal_return_permission / candidate_not_created`である。
