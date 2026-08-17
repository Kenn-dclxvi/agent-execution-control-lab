# Candidate271失敗とC81・C246の成立範囲差分析

## 結論

Candidate271がCandidate81またはCandidate246と同じ禁止を弱く書いたため失敗した、という説明は棄却する。Candidate271は、途中resultをAIへ返さない境界をCandidate81・Candidate246より具体的に記載していた。それでもF01・F02の10 / 10件でvalidation間model再入が起きた。

差は、Candidate271が一つの自然語境界で二つの問題を同時に解こうとし、Candidate269で成立していた直接の返却禁止まで条件付きの自己分類へ置き換えたことにある。

1. Candidate81・Candidate246が解いたのは、required validation間でmodelへ戻らず、すべてのrequired validationを一つの外側実行から完了させる発行境界である。
2. Candidate271はその境界を維持したうえで、Candidate269の過大なraw validation output carrierを、実行票の完了状態と各validationの終了状態だけを返すcarrierへ置き換えようとした。

後者は、文面上は`result`の資格を狭める制御に見える。しかし実行上は、外側tool invocationが返すraw outputを、ticket completion stateへ投影してmodel-visibleにすることを必要とする。tool outputの配送内容、byte量またはprojectionはpromptだけでは安定して強制できないことをCandidate90からCandidate96までですでに確認している。

さらにCandidate271は、Candidate269の「個別検証の途中resultはAIへ返さず」という直接の動作境界を、`実行票が完了するresultか`、`個別resultか完了resultか`、`残りが発行不能か`という複数の事前・実行中分類へ置き換えた。設計記録では「新しい自己分類を増やさない」としたが、実際にはmodelがtool発行前に判断する分類を増やしていた。

したがってCandidate271の直接原因は、禁止文の不足ではない。Candidate269で成立していた直接の再入閉鎖をticket状態の自己分類へ薄め、その正常routeへpromptから閉じられないoutput projectionを混ぜたことである。Candidate271の設計時に「raw output制御は非目標」とした一方、実際の正常routeはraw outputをcompletion resultから分離できなければC269の費用問題を解消できない。この矛盾と分類責務の増加を作成前gateで見落とした。

Candidate272へ同じ禁止の追記、ticket名の変更、AIという返却先の再強調または成功runのwrapper手順化は行わない。C147・C269のraw trace比較はすでに完了しており、再調査もしない。promptで閉じられる再入・追加取得のpermissionと、promptでは配送内容を保証できないcarrier methodを分離し、C269が局所的に追加した`発行済みの全result`という広いpermissionだけを失効させる。

## 観測事実

| Candidate | 対象 | validation間model再入を閉じた観測 | token | 判定 |
| --- | --- | ---: | ---: | --- |
| C81 | F04 N=10、Standard14 N=5 | F04 10 / 10、複数required-command case 35 / 35 | C71とほぼ同水準 | wrapper内の個別実行という解釈を固定 |
| C246 | F04 N=5 | 5 / 5 | 183,187、C147比`+21.18%` | AIへの途中返却禁止は成立したがcost未解消 |
| C269 | F01・F02 N=5 | wrapper route 10 / 10 | F01 163,264、F02 166,758 | 再入を閉じたがraw output carrierが大きい |
| C270 | F01・F02 N=5 | 0 / 10 | F01 121,788、F02 138,017 | wrapperを迂回してtoken低下 |
| C271 | F01・F02 N=5 | 0 / 10 | F01 147,496、F02 171,806 | ticket terminal返却routeを実行せず停止 |

C246の成立はF04 N=5だけである。F01・F02へ一般化した証拠ではない。またC246はC147より32,017 token多く、途中返却を閉じてもcarrier costが解消するとは示していない。

C269とC271はF01・F02のTaskSpec、fixture、required validation、model、reasoning、runtime、permissionおよびexecutorが同じで、prompt差はroot `VALIDATION_CLOSURE`だけである。C269は同じF01・F02でwrapperを選んだため、F04とF01・F02のcase構造差だけをC271失敗の原因にはできない。

## C81・C246が閉じた範囲

### Candidate81

Candidate81は、TaskSpecまたはcommand evidence protocolの「順に」「1 commandずつ個別」を、次のどちらとして解釈するかという選択を閉じた。

- wrapper内部で順番を守る個別invocation。
- command resultをmodelへ返してから次を別の外側callで発行するトップレベル逐次実行。

Candidate81は前者だけを合法な意味へ固定した。各exit codeをwrapper内で確認し、完了済みresultを一度だけmodelへ返す。ここでは、返すresultのbyte量、stdout抑制またはsummary形式を解決対象にしていない。

### Candidate246

Candidate246は、F04で「順に行う必須検証の途中結果をAIへ返してから、残りの検証を実行してはならない」とした。Candidate244の「発行判断」とCandidate245の「判断側」という抽象的な返却先を、実際の受領主体であるAIへ置き換えた。

この一文はF04 N=5で5 / 5件成立したが、tokenはC147比`+21.18%`だった。したがって、C246から確定できるのはF04での返却時点の閉鎖であり、compact carrierの成立ではない。

## Candidate269からCandidate271で増えた責務

Candidate269の正常routeは単純だった。

`全required validationを一回の外側実行へ束ねる -> wrapper内で個別実行 -> 発行済みの全resultを一度返す`

このrouteはF01・F02で成立したが、focused gateとfull gateの大量のstdoutを一つのmodel-visible resultへ載せた。保存traceのC269 F01 runでは、focused gate 21,405 bytes、full gate 158,840 bytesを含むvalidation結果が一つの後続model入力へ入っている。

Candidate271は次へ置き換えた。

`全required validationを一回の外側実行へ束ねる -> wrapper内で個別実行 -> raw execution recordはcompletion resultへ昇格させない -> ticket stateと各終了状態だけを一度返す`

問題は最後の二段である。外側実行がraw stdoutを生成している以上、「raw execution recordは保持するがmodelへ返すcompletion resultにはしない」を実現するには、外側tool resultの配送内容を選別する必要がある。これは単に、返却後のAIがresultをどう判断するかという制御ではない。model-visibleになる前のprojectionを要求する。

同時に、最初の二段もCandidate269と同じではない。Candidate269は「途中resultをAIへ返さず、wrapper終了時に一度返す」という時点の禁止を直接記載していた。Candidate271は、途中resultでも`そのresultによって実行票全体が完了する場合`は返せるという条件へ変え、返却可否をticketの完了分類へ依存させた。さらに`外側invocation`、`個別result`、`完了result`、`発行不能`の区別も実行時に要求した。これは名称だけの置換ではなく、C215からC222までで失敗反例になったticket・label・自己分類と同じ方向の責務追加である。

Candidate271本文にも、次の実質的なprojection要求が入っていた。

> wrapperは実行票の完了状態と、開始前に固定した各検証の終了状態を一度だけ返す。

設計記録はstdout抑制、truncationおよびbyte上限を非目標にした。しかしC269の過大carrierを解消するには、raw output全件ではなく上記状態だけを返せる必要がある。非目標と正常routeの必要条件が一致していなかった。

設計記録の「新しい自己分類を増やさない」という判定も訂正する。実行票が別artifactでないことと、modelが新しい状態分類を要求されないことは同義ではない。Candidate271は、tool発行前に返却resultの種類とticket terminalへの寄与を判定させており、C269より判断責務を増やしていた。

## C90からC96までの既知反証

| Candidate | 狙ったoutput境界 | 観測 | 判断 |
| --- | --- | --- | --- |
| C90 | raw outputがmodel contextへ入る前の4096 bytes projection | 0 / 5 | ingress projection不成立 |
| C91 | 短い二文で一時file wrapperへ誘導 | strict 2 / 5 | 適用範囲が安定しない |
| C92 | route事前固定と4096 bytes上限 | cap 3 / 5、token C81比`+51.00%` | capは不安定で再readも増加 |
| C96 | validation success resultをidentity、command、exit codeだけへ投影 | 0 / 5 | 全runでfocused/full stdoutがmodel-visible |

C96ではsuccess projectionが0 / 5でもtoken中央値はC81比`-11.03%`だった。その低下はprojectionの効果ではなく、重複validationや周辺commandの少ないrouteに対応した。これはC270のtoken低下も、狙ったcarrier機序の成立証拠にできないことと同型である。

したがって、C271の「completion resultだけを返す」を別の自然語へ言い換えて再試験する根拠はない。既知の失敗軸を繰り返すことになる。

## 実際にC271で選ばれたroute

C271 F01の保存traceでは、focused gate、full gate、diff、statusがそれぞれ別のトップレベルcommand resultとしてAIへ返った。focused gate成功後にfull gateを発行し、full gate成功後にdiffとstatusを発行した。

`focused gateをトップレベル発行 -> raw resultをAIが受領 -> full gateをトップレベル発行 -> raw resultをAIが受領 -> diff / statusを別発行`

このrouteはC271本文の禁止へ違反している。したがって、prompt準拠の合法routeだったとは判定しない。一方、禁止違反が10 / 10件だった事実は、同じ禁止をさらに詳細化すればよいことも示さない。正常route側が実現不能なprojectionを要求していたため、モデルが実行可能なtool境界へ退避したと読むのが、C269、C270、C271およびC90〜C96の保存結果と最も整合する。

## C147について訂正する点

C147で確実に成立していたのは、required validationを一つのcustom exec wrapper内で完遂し、全result受領後に一度だけ判断する構造である。

C147がsuccess stdoutのcompact carrierをpromptで閉じていた証拠はない。既存のcost再入原因監査でも、C147本文は成功stdout全体をcarrierへ載せるpermissionを制限せず、一部runがcompactな結果表現を選んだだけで、promptがそのmethodを強制した証拠ではないと判定済みである。

したがって、次の二つを分ける。

- C147から復元すべき成立機序: validation間model再入を閉じる外側発行境界。
- C147のKPIへ寄与した可能性があるが、未閉鎖の実行方法: compactなvalidation結果表現。

C147の低いKPIをそのまま「compact carrier閉鎖が成立済み」と読み替えない。ただし、C147との差を自然語一般の固定費とも確定しない。C269の文面が`発行済みの全result`を明示してraw output carrierを正規routeへしたことは、保存traceとprompt差の照合まで完了している。

## 既存raw trace比較で確定済みの量

C147・C269のF02中央値境界runは、すでに内部出力、外側carrierおよび直後のmodel入力まで直接比較済みである。

| 観測 | C147境界run | C269境界run | 差から分かること |
| --- | ---: | ---: | --- |
| total token | 141,684 | 166,758 | C269が25,074 token多い |
| focused内部出力 | 23,550文字 | 23,634文字 | test出力量はほぼ同じ |
| full内部出力 | 158,709文字 | 158,840文字 | test出力量はほぼ同じ |
| 外側wait result | 8,358文字、`max_tokens=2,000` | 120,906文字、`max_tokens=30,000` | 外側carrierが112,548文字増えた |
| 完了判断のmodel入力 | 32,778 token | 48,402 token | C269が15,624 token増えた |

両runのtotal token差25,074のうち、完了判断の一回だけで15,377 token、61.3%を占める。C269 wrapperは各command outputを保持し、全raw outputを個別の`text`として返していた。C147 wrapperは同量の内部出力を生成しながら、比較対象runでは外側carrierを2,000 tokenへ制限していた。

ただしC147の一回待機route 2件のうち別の1件は80,595文字を返した。よって、C147本文がcompact carrierを常に強制したとはいえない。確定したのは、C269の`発行済みの全result`がraw output全件を返す実装をprompt準拠の正常routeにしたことと、それが実測KPIを押し上げたことである。

## promptで閉じられる範囲と閉じられない範囲

| 境界 | promptで扱えること | 今回の判断 |
| --- | --- | --- |
| validation発行 | 未完了validationを残したまま別のトップレベルtool callへ戻るpermission | C81・C246・C269で閉鎖実績がある |
| resultの後続利用 | 完了判定用resultが不足したときだけ追加取得を許すdependency | F01・F02の追加outer call原因として引き続き分析対象 |
| tool result配送 | raw stdoutのどのbytesをmodel-visible payloadへ入れるか | C90〜C96の反証があり、prompt Candidateの成立条件にできない |
| 外側上限・summary形式 | `max_tokens`、truncation、終了状態だけのprojection | C147成功runのmethodであり、次案へ転記しない |

C269はvalidation間再入をすでに閉じた。そのうえで残った大きなcarrier差は、promptが保証できない配送methodを含む。したがって「C147と同じcompact carrierを自然語で再現する」ことを次Candidateの成立条件にはできない。一方、F01・F02に残る最終証拠の別取得、限定追加read、validation分割は、後続operationのpermission・dependencyなので別に調べられる。

## prompt層の追加operationをC147へ照合した結果

### F02

F02の追加operation全体をC147機序の未移植とする仮説は棄却する。

| F02経路 | C147 N=20 | C269 N=20 | 判断 |
| --- | ---: | ---: | --- |
| 二重待機 | 4件 | 0件 | C269が閉じた |
| validation分割 | 1件 | 0件 | C269が閉じた |
| 変更前追加read | 7件 | 3件 | C269が減らした |
| 最終証拠の別取得 | 2件 | 3件 | 一件増だが、支配的な頻度差ではない |

C269のF02は、C147までのprompt層の経路を移植できていないのではなく、一回の外側validation routeをC147より安定して実行している。そのroute一回のcarrierが大きいため、上側11 / 20件が中央値を構成した。よってF02のtoken `+24.19%`を、追加read禁止、validation分割禁止またはwait禁止の追記で直す根拠はない。

### F01

F01にはC147から未移植の関係が残る。C269 N=20では完了result欠落3件、限定追加read 1件、validation分割1件があり、C147 F01 N=20では同じ理由の検証後再取得は0件だった。

このうち確定原因へ直接対応するのは完了result欠落3件である。C147の局所条件は`完了済み`かつ各predicateへ`bind済み`のresultが全件そろった場合だけ完了判断へ進めた。Candidate254の自然語本文も、必須validationと完了判定用diff・statusを同じ実行票へ先に固定し、必要なresultをすべて受け取った後に一度判断するとしていた。C269はその既存関係へ`発行済みの全result`という広い返却資格を追加したため、raw invocation outputを受け取ったことと、完了判定用resultがbindされたことを同一視できるrouteを開いた。

C270はこの差だけを直すと宣言したが、実際には各resultをvalidation、合格条件、終了状態へ`明確に対応づける`新しい実行中作業へ置き換えた。C271はさらにticket terminal分類を加えた。両Candidateとも、C269の直接のwrapper・途中返却禁止を維持したまま広い局所permissionだけを失効させた試験ではない。したがってC270・C271の失敗から、「C269の`発行済みの全result`を変更できない」とは結論しない。

一方、このF01関係を直しても、F02で支配的な112,548文字のcarrier差を閉じたことにはならない。F01の追加operation改善とF02の配送費用を一つの機序効果として相殺してはいけない。

## 次Candidateの解決方針

追加Nは発行しない。C269 N=20で上振れ頻度が確定し、F02境界runのpayload比較も完了している。C271は同じ失敗routeがF01・F02の10 / 10件で起きており、ばらつき精度を上げても設計原因の判定は変わらない。

次Candidateは、F02のcompact carrierを直接強制する案ではなく、C269がraw output全件配送をprompt準拠の正常routeにした局所permissionを取り除く案とする。現在分かった設計境界は次のとおりである。

1. C269の一回の外側実行、直接の途中返却禁止およびnonterminal時の同一cell dependencyは保持対象である。
2. `発行済みの全result`が開いたinvocation-owned result permissionは失効対象である。
3. その失効を、C270のpredicate対応づけ作業またはC271のticket terminal自己分類へ置き換えてはならない。
4. 一般`TERMINAL`、自然語`EVIDENCE_GATE`および`VALIDATION_PLAN`にすでにある、必要resultがそろい、入力が変わったpredicateだけが失効し、実行票後に追加toolを出さない関係を重複して作り直さない。
5. F02のcompact carrier、外側上限またはsummary形式をrequired effectへ入れてはならない。carrier内容はmethodとして残し、C147の実測KPI分布との比較で結果を判定する。

具体的には、C269の次の一文だけを変更対象にする。

`個別検証の途中resultはAIへ返さず、発行済みの全resultをwrapperが終了した時に一度だけ返す。`

これを、返却時点だけを固定し、返却対象を発行済みinvocationへ対応づけない文へ置き換える。

`個別検証の途中resultはAIへ返さず、wrapperが終了した時に一度だけ結果を返す。`

これだけで必要resultが消えるわけではない。一般`TERMINAL`は全predicateのterminal result、自然語`VALIDATION_PLAN`は必須validationと完了判定用diff・statusの事前固定、全result受領後の一回判断、実行票後の追加tool禁止をすでに要求している。C269の局所文から`発行済み`という別ownerを除けば、既存の一般関係が再び返却・完了条件を支配する。新しい対応づけ作業、ticketまたはoutput分類は不要である。

これはraw outputを禁止しない。C147にも大きなcarrierがあるため、機序合格をcompact率100%にはしない。機序は、C269型の`issued invocationだからcompletion resultへ昇格できる`permissionが本文から消え、C269の一回wrapperと途中返却禁止が保持されたかで判定する。KPIはF01・F02のrun分布とcase別中央値をC147・C269へ比較し、機序と分けて判定する。

output byte量、summary方法、wrapper codeまたは成功runのtool順は原因関係へ入れない。carrier配送を必要条件にする案は`candidate_not_created`とする。

## 現在の判断

- `C271はC246より禁止が弱かった`: 棄却。
- `F04とF01・F02のcase差だけが原因`: 棄却。C269が同じF01・F02でwrapperを実行した。
- `ticket terminalという名称を強めれば閉じる`: 棄却。正常routeがoutput projectionへ依存している。
- `C81・C246はcompact carrierまで実証した`: 棄却。
- `C271はprompt層で閉じられる再入と、prompt層で安定強制できないoutput projectionを同時に扱った`: 支持。
- `C271は新しい自己分類を増やしていない`: 棄却。ticket terminal、result種別および発行不能の実行時分類を増やした。
- `C147はcompact carrierを機序として閉じていた`: 未成立。compact実行runはあるが、promptによる強制証拠はない。
- `C147・C269のraw trace比較が未完了`: 棄却。内部出力、外側payload、最終model入力およびtoken差まで確定済みである。
- `F02の大きな差はC147より多い追加operationが原因`: 棄却。C269は二重待機、validation分割および変更前追加readをC147より減らしている。
- `F01の完了result欠落はC147のresult関係を未移植した反例`: 支持。C269の`発行済みの全result`追加と対応する。
- `C270・C271はC269の広いpermissionだけを失効させた試験`: 棄却。新しいpredicate対応づけまたはticket terminal自己分類も同時に追加した。
- `追加NでC271の原因を精密化する`: 不要。同一誤経路10 / 10と既存C269 N=20で判断できる。
- `F02のcompact carrierを100%強制できないためC272を作れない`: 棄却。閉じる対象はcompact表現ではなく、raw output全件配送を正常化した`発行済み`permissionである。
- `次にC272を作成する`: 作成前設計を許可する。C269を直接親とし、上記一文の`発行済みの全result`対応だけを除去する。bundleと評価枠は設計gate後の別状態とする。

現在状態は`candidate271_failure_cause_refined / existing_c147_c269_carrier_trace_reused / f02_extra_operation_regression_rejected / f01_result_binding_gap_confirmed / c269_issued_result_permission_confirmed / c270_c271_added_classification_confound_confirmed / c147_compact_carrier_not_guaranteed / candidate272_single_permission_removal_design_allowed / candidate272_not_created`である。
