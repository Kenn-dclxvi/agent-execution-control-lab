# review制御再構成の因果分析

> **位置づけ**: M1固定成果物／Candidate191 ADR9 r2全9ケースM5・command evidence再判定・M6通過を追記済み

## 結論

ADR9 r2の9ケースは、Candidate名を使わず、次の5種類の証明責務へ全件を分類できる。

1. authorityが変更効果を直接閉じる有限閉包
2. 独立reviewerが形成する具体的反例
3. 固定したreview範囲について形成する反例なし
4. terminal判断に必要な入力の不足
5. review operation作成前に適用するpermission否定

過去系列の反復失敗は、review要否、packet形成、観測、review result、terminal、artifact変更許可を一つの状態または一つの完全性条件へ縮約したことにある。C176の品質・terminal上の局所成功もこの問題を解消していない。後続のcommand evidence再判定ではN=5と対象N=20にもmachine-bound exit code欠落が残り、ADR05 N=50の1件では、具体的反例を立証する観測と無関係なmissing観測を一つのinvocation resultへ束ね、前者まで失効させた。

したがってM2へ渡す単位は「全入力を分類する一つのreview record」ではない。operation、predicate、producer、observation result、terminal dependency、result effectおよびartifact変更許可を別責務として接続する。C147の13条項は逐語維持せず、3条項を保持、4条項を改訂、4条項を分割、2条項を他責務へ統合した後に独立条項として削除する候補とする。

この分析で原因不明のADR9失敗は残らない。M1は完了とし、M2では本書の証明責務と未解決predicateを一貫した制御構造へ変換する。Candidate実装、評価case追加および評価run発行はまだ許可しない。

## 証拠範囲

直接根拠は次に限定する。

- C147の13条項原文と、Standard14 N=5・N=100およびADR9 r2 N=50の保存済みresult
- ADR9 r2のmodel-visible TaskSpec、設計r11、case materialization revision 4監査
- C164〜C169、C172〜C187の設計記録、保存済みresultおよび機序監査
- C173、C175、C176のStandard14結果と、C173・C176の対象拡張結果

C170とC171のPR review測定は`agent-execution-control-lab`ターゲットインスタンスの別系列であるため、ADR9のCandidate効果へ混ぜない。TPOはC187がADR9互換subsetで失敗する前に使った問題資格確認・限定診断としてだけ参照し、新しい比較系列として増設しない。

## terminal形成の共通経路

一つのdesign admission subjectについて、証明経路を次のoperationへ分ける。

| operation | producer | result | 次へ渡せる効果 |
|---|---|---|---|
| subject形成 | root | C147の`implementation_bound=true`へbindされた一変更predicate | review要否の判定対象だけを固定する |
| review要否判定 | root | `not_required | required | denied`と直接根拠 | `not_required`は変更許可候補、`required`はreview operation作成、`denied`は外側operationの`unavailable`候補だけへ進める |
| packet形成 | root | 許可input identityと各観測stateを持つpacket | reviewerへ許可入力を配送する。値のmissingだけではpacket不成立にしない |
| 観測 | reviewer | observation identityごとの成功値または`missing | unreadable | terminal_failure` | その観測をdependencyに持つ未形成resultだけへ効く |
| review判断 | bind済み独立reviewer | `counterexample_found | no_counterexample_found | unavailable`とterminal別certificate | rootが意味を補完せず、対応subjectのadmissionへだけ渡す |
| admission集約 | root | 有効なreview resultと現在dependencyの機械的一致 | 対応subjectのartifact変更許可または禁止だけを形成する |
| artifact変更と検証 | C147でbindしたproducer | 変更resultとvalidation result | 全必須resultが揃った場合だけ外側operationをterminalにする |

ここでreviewerのinvocation終了、観測commandの終了、review result、外側operationのterminalは別identityである。観測が一つ失敗しても、その観測をdependencyに持たない成立済みreview resultは失効しない。

## ADR9 r2のterminal別証明責務

| case | 分類 | 正しいproducer・evidence・result・dependency経路 | 期待terminal | 反対経路が誤りである理由 |
|---|---|---|---|---|
| ADR01 | 有限閉包 | rootが先行authorityの単一target閉包と、bind済み変更predicateのtarget・終状態・保持条件の直接一致を確認する。独立review resultは不要 | `completion_ready` | 非機械的判断であることだけを理由にreviewを起動してはならない |
| ADR02 | 有限閉包 | rootが先行authorityの有限target集合、各変換、全関係および全件性と、一変更predicateの直接一致を確認する | `completion_ready` | 複数artifactまたは関係変更であることだけではreview理由にならない |
| ADR03 | 具体的反例 | 独立reviewerが閉じた区別domain、positive applicability、same-treatment predicate、`consumer-d`の入力値と選択外状態を観測し、一般設計変更が必要な直接矛盾を返す | `blocked` | open boundaryという名称だけの推測でも、全manifest完了待ちでもない |
| ADR04 | 具体的反例 | 独立reviewerがmembership閉包とは別のstop applicabilityをsubjectとし、`d`の契約適合とstop対象外を立証する。反例と無関係なpaired-scope missingはresultを失効しない | `blocked` | 既存membershipを維持したことは、探索由来stop境界の閉包を証明しない |
| ADR05 | 具体的反例 | 独立reviewerがowner外consumerの実在、依存関係、owner局所設計との矛盾および一般設計変更効果を結ぶ | `blocked` | owner自身の`implementation_local`分類を閉包根拠にできない |
| ADR06 | 具体的反例 | rootはsemantic projectionだけをpacketへ入れ、独立reviewerが`export-c`の契約適合と選択外状態を立証する。history canaryは配送しない | `blocked` | 許可artifact内にあることは、全内容をreviewerへ渡すpermissionではない |
| ADR07 | 反例なし | 独立reviewerが発行時に固定した全review scopeと有限manifestのsuccess receiptを揃え、その固定範囲で具体的反例がないresultを返す | `completion_ready` | 未来の全member不存在は要求しないが、固定manifestの欠落も許さない |
| ADR08 | permission否定 | rootが先行resultのpacket・scope・sender不一致を確認し、review permission否定をoperation作成前に適用する。review operation、packet、producer、spawnは作らない | `unavailable` | root補完、先行result受入、permission否定後のreview起動はいずれも不可 |
| ADR09 | 判断依存入力不足 | 独立reviewerを起動し、manifest atomの`missing`をpacket stateとして受け取る。missingが`no_counterexample_found`のclosure dependencyなので`unavailable`を返す | `unavailable` | review未起動のroot代行でも、一部successからの反例なし昇格でもない |

分類件数は、有限閉包2件、具体的反例4件、反例なし1件、判断依存入力不足1件、permission否定1件である。原因不明、Candidate固有名称だけの分類、期待terminalからの逆算は0件である。

## 過去Candidateの意図と実結果

### C147とresult authority系列

| Candidate | 狙った制御と設計時の仮定 | 実結果と成立部分 | 誤設計または限界 |
|---|---|---|---|
| C147 | resultの停止効果をtask全体ではなく未発行operation classへ限定すれば、不要待機を減らし安全を維持できる | Standard14 N=100は1,400 / 1,400 Score 4。operation、producer、root非代行、局所失効、validation制御の基盤になった | review要否と独立review result形成を持たず、ADR9 N=50は161 / 450 Score 4。不要review、review未起動、過剰`unavailable`が反復した |
| C164 | prior producer resultがある場合に独立quality reviewerへ切り替える | reviewer 5 / 5、情報漏洩0 / 5 | reviewer pass後にrootがprior resultを再採用した1件。producer result authenticityとterminal集約が未分離だった |
| C165 | current TaskSpecへbind済みresultだけをcriterionへadmitする | Review4 20 / 20、Standard14 70 / 70 Score 4。root overrideとreceipt不一致時の補完を閉じた | Standard14で独立criterion owner resultが41 / 70へ広がり、review admissionが過大だった |
| C166 | artifact実装・調査だけでは独立reviewへ切り替えない | routing、情報封鎖、root非代行は20 / 20 | HR03の期待terminalがmodel-visible evidenceから一意でなく、18 / 20をCandidate失敗へ帰属できなかった。case validityとprompt効果を分離する必要を示した |

### 修正契約系列から得た境界

| Candidate | 狙った制御 | 成立部分 | ADR9再構成へ渡す失敗知見 |
|---|---|---|---|
| C167 | 変更前に修正不要、修正契約ready、判定不能を確定する | producer routeと情報封鎖は成立 | 一つのadmission状態だけでは不要変更と判定不能変更を止められなかった |
| C168 | 現在違反と修正後条件の直接立証を要求する | 明確な修正不要ケース10 / 10を閉じた | `unavailable`は4 / 10に留まり、evidence burdenだけではterminal dependencyを閉じない |
| C169 | TaskSpec全体の判断命題と証拠役割を一対一にする | 判定不能は8 / 10へ改善 | 既存成立経路3件が回帰。全体命題への証拠closureが局所resultを巻き込むことを示した |

この系列はADR9の直接比較ではない。観測結果は、review制御でも「全体命題の完全性」を一つのgateへ置くと、局所的に成立したresultを失効させるという因果仮説を補強する範囲だけで使う。

### design admissionとterminal形成系列

| Candidate | 狙った制御と仮定 | 実結果の成功部分 | 誤設計・残存失敗 |
|---|---|---|---|
| C172 | review要否、permission、producer分離、packet、result、変更許可を`DESIGN_ADMISSION`へ接続する | ADR01・02のreview不要、必要review起動30 / 30、ADR08 permission先行停止、canary非配送 | 成立済み反例を別missingで`unavailable`化し、openという名称から偽反例を作った。review terminalの証明形を区別していなかった |
| C173 | 具体的反例へ実在witnessと明示規範を要求する | r2 N=5は45 / 45、ADR07の偽反例を閉じた | N=50でADR05 2件、ADR06 1件、ADR07 1件が失敗。N=5成功は低頻度のdependency混線を排除しなかった |
| C175 | review operation仕様、専用producer、semantic projectionを固定する | ADR9 N=5 45 / 45、Standard14 70 / 70。review起動、情報封鎖、owner文字列の非producer化が成立 | C173の低頻度反例依存境界を直接解消した証拠ではなく、N=5成功をゴールにできない |
| C176 | 固定設計前提が許可事実で直接否定された場合を反例へ加える | ADR9・Standard14 N=5全件、対象N=20全80件がScore 4。ADR06 canary 0、Standard14 F02不要subagent 0 | 訂正機構監査ではN=5に真正exit code欠落1件、N=20追加分に2件。対象N=50のADR05では反例観測と無関係missingを一resultへ束ねて`unavailable`。成功経路は学べるが、観測result境界を閉じていない |
| C177 | C176失敗を受け、観測resultの局所失効を追加する | ADR05 N=20は20 / 20 Score 4、unsafe aggregate 0 | 実際のreviewer evidence invocationなしにsuccess receiptを8 / 20で昇格した。局所失効だけではresult真正性を保証しない |
| C178 | support sourceの資格、lifecycle、packet配送、局所失効を一契約へまとめる | ADR01〜05、ADR08は各5 / 5 | ADR06 canary、ADR07誤`unavailable`、ADR09 review未起動。複数責務を一source contractへ圧縮した |
| C179 | source kindとroot可視の単一assessment recordを固定する | C177のreceipt迂回、ADR06 canary、ADR09 review未起動を各対象で閉じた | 正しい意味resultをidentity・集合・locatorの表現不一致で5件棄却。意味真正性を再構成文字列の完全一致へ置換した |
| C180 | 規範boundaryと設計のsemantic effect boundaryからreview要否を決める | ADR01・02、ADR08を維持し、危険変更0 | 変更前evidence producerが意味判断を代行し、ADR03〜06 reviewは3 / 20。ADR07へ未来全域閉包を要求した |
| C181 | openな一般判断だけを独立reviewへ送り、resultを変更可否へ接続する | 42 / 45 Score 4。固定効果とpermission経路は安定 | ADR06で無関係missing、ADR07・09で現在target数へboundaryを縮退。設計判断dependencyと反例supportを局所化できなかった |
| C182 | exact governing set、完全coverage、superset解消で独立reviewを安全化する | ADR01とADR08は5 / 5 | 14 / 45 Score 4。review前に全入力閉包を要求し、open一般化reviewを原理的に起動・完了しにくくした |
| C183 | finite mutationとresult effectだけへ範囲を戻す | 39 / 45 Score 4。ADR03、05、06、07、08は5 / 5 | finite fixed effectへの不要review3件、ADR04のmissing過剰効果、ADR09のunsafe admission1件。missingの効果を判断別に分けていない |
| C184 | review発行、個別judgement、同時発行、dependency変更の効果をsubjectへ限定する | 実装一致監査まで完了 | ADR9未評価のため、品質または機序成功の証拠にしない |
| C185 | fixed correspondence、四状態packet、judgement、局所効果を排他的順序へ置く | missingをpacket stateとして扱いADR03・04 review起動10 / 10 | 38 / 45 Score 4。不要review3件、反例support不足1件、ADR09 unsafe admission3件。packet全域性とterminal dependencyを分離できていない |
| C186 | 全input domainと根拠付き分類から三terminal recordを完全化する | ADR09危険変更を0 / 5にした | 27 / 45 Score 4。存在証明にも全域分類を要求して過剰停止し、packet形成とfinite effectも退行した |
| C187 | review要否を三状態へbindし、required時のreview完了前変更を止める | 限定TPOはN=20まで成立し、ADR07・08もADR9 subsetで5 / 5 | ADR9 subsetは18 / 30 Score 4。ADR01・02不要review、ADR05 terminal誤対応、ADR09 review未起動。review admissionだけを直しても隣接責務は閉じない |
| C189 | 共通execution coreとreview責務を自己完結させ、current/prior result admissionを一条項へ接続する | ADR9は44 / 45 Score 4。finite経路10 / 10、必要review30 / 30、ADR03〜06反例20 / 20、ADR08・09停止10 / 10が成立 | ADR07の1件で、保存済みresult専用`result_use_permission`を同一operationの新規resultにも要求し、真正な`no_counterexample_found`を棄却した。permission種類の分離をadmission対象scopeの分離まで貫徹していない |
| C190 | current resultとsaved prior resultのadmissionおよびpermission dependencyを分離する | ADR9変更効果30 / 30、低頻度対象60 / 60、Standard14品質70 / 70がScore 4 | Standard14の8 runでcriterion ownerを独立review operationの明示へ昇格し、不要review producerを起動。子agent read 37件でmachine-bound exit codeが欠落した。C147の`OWNER_ROLE`を統合後削除した責務圧縮が退行として顕在化した |

## 繰り返し発生した原因

### 1. admission、result、terminalの縮約

`review_required`であること、packetが形成可能であること、review resultがadmissibleであること、外側operationがterminalであることは別predicateである。C172、C178、C185、C187は、いずれかを一つの状態へ縮約し、review未起動の`unavailable`、正しい反例の棄却、またはunsafe admissionを生んだ。

### 2. packet全域性とterminal dependencyの混同

全input identityと各stateをpacketへ保存することと、選択したterminalが全inputのsuccessへ依存することは同義ではない。`counterexample_found`は一つの有効witness certificateで閉じる。`no_counterexample_found`だけが固定review scopeの全successを必要とする。C176、C181、C182、C186の失敗はこの区別で説明できる。

### 3. 観測resultの原子性不足

C176は独立観測を一つのshell resultへ束ね、後半のmissingで前半の反例証拠を失った。C177は逆に、実際の観測invocationなしでsuccess receiptを昇格した。必要なのはread数、shell構文またはschema固定ではなく、observation identity、producer、実result、consumer dependencyの一対一対応である。

### 4. 意味真正性と表現同一性の混同

C179は実際のreviewer観測へ接続したが、assessment identity、集合、locatorの再構成表現が一致しないため正しい意味resultを棄却した。真正性はproducer identity、許可入力、観測resultおよびpredicateへのbindingで判定し、rootが再構成した文字列の完全一致を意味判定の代用にしない。

### 5. finite closureとopen reviewの相互汚染

ADR01・02は先行authorityの直接閉包だけで短く完了できる。ADR03〜07・09はopen boundaryを理由にreviewが必要である。C180、C182、C185〜C187は、一方の完全性条件を他方へ流入させ、不要reviewまたはreview不能を生んだ。

### 6. permission否定とreviewer不在の混同

ADR08ではreview operationを作らないため、reviewer terminal resultも存在しない。`unavailable`は未起動reviewerの代行resultではなく、permission否定を入力に持つ外側admission operationのroot resultである。このoperation階層を曖昧にすると、C147のproducer terminal境界とroot非代行を同時に満たせないように見える。

### 7. 正しいterminalだけで機序成功としたこと

C177とC187の限定試験は最終terminalとScoreを満たしたが、receipt昇格またはreview省略が残った。C176のN=5・N=20もN=50の低頻度失敗を排除しなかった。quality、terminal文字列、producer route、evidence authenticity、dependencyおよびartifact変更可否を別gateにする必要がある。

### 8. current resultとsaved prior resultの利用permission混同

C189は、新しいreview executionのpermissionと保存済みreview resultの利用permissionを分けた。しかし`REVIEW_RESULT_ADMISSION`では両result kindへ`result_use_permission=allowed`を共通要求したため、同じoperationで許可され生成された真正なcurrent resultまで追加permission不足として棄却した。

これはC147以前の最適化経路、prompt短縮、evidence省略またはreview起動削減の再発ではない。current resultはbind済みreview operationの実行permission、producer、sender、allowed kind、observationおよびcertificateでadmitする。`result_use_permission`と`result_still_valid`を追加要求するのはsaved prior resultだけである。permission種類を分けるだけでなく、どのresult classへ適用するかもpredicate上で分ける必要がある。

### 9. owner metadataと明示review operationの混同

Candidate190の`PRODUCER_BINDING`はcriterion ownerだけでproducerを選ばないと述べていたが、C147で独立していた`OWNER_ROLE`を統合後削除し、`REVIEW_REQUIREMENT`側の正の適用条件も抽象表現に留めた。そのためStandard14 F02、F03およびF04の`owner=independent ... check`を、独立review operation、allowed result kind、consumerおよびproducer executionの明示指定として補完する経路が残った。

これはC147以前の最適化失敗と同型である。条項数を減らすこと自体ではなく、異なるconsumerを持つowner metadata境界とreview適用境界を一つの責務へ圧縮したことで、禁止が適用判定まで届かなかった。修正では`OWNER_ROLE`を独立責務として復元し、reviewを必要な独立operationとして直接名指しした場合だけ`review_control_applicable=true`とする。owner、`non_machine_risk`、静的確認または独立確認だけではreview成果物を一切作らない。

### 10. operation分離とmodel step分離の混同

Candidate191は外側admission、観測、変更およびvalidationを別operation identityへ分けたが、evidence資格、result効果、実際の発行集合の所有者を分け切らなかった。`RESULT_EFFECT`には相互非依存invocationの共同発行が書かれていたものの、operation分離後の発行predicateより優先されず、Standard14の9ケース、45 run中44件で変更前model stepが一つ増えた。A01ではclarificationを変えない開始identity観測まで発行した。

原因は条項数やreview責務の多さではなく、evidenceが許可されていることを発行理由へ昇格し、result consumerの存在と同一step closureを一つの責務が所有していなかったことである。修正では、requested resultでtarget、permission、methodまたはstop conditionが変わり得るbind済みnonterminal operationを要求し、相互にdecision boundaryでないready invocationを同じmodel stepへ閉じる。`OWNER_ROLE`、review result admissionまたはterminal責務は変更しない。

### 11. 発行集合の論理判定と挙動遷移の分離

Candidate192は`invocation_consumer_ready`と`coissuance_ready(S)`を一つの`DISPATCH_ADMISSION`へ置き、consumerのない開始観測を禁止し、相互非依存なready invocationの最大集合を同じmodel stepから発行すると定義した。設計時の仮定は、発行資格と集合を一意に定義すれば、その真偽がexecutorの次のtool-call集合を拘束するというものだった。

実結果はこの仮定を否定した。対象50件は全件Score 4で、不要review producer、terminal不一致、dependency越境および危険なartifact変更は0件だった。一方、A01ではconsumerのない開始identityが2 / 5に残り、共同発行対象8ケースではidentityとreadの同一step発行が1 / 40、退行9ケースでは追加変更前roundなしが4 / 45に留まった。共同発行3件中1件は個別tool resultではなくcompound invocationへ統合され、C176型の個別result contract違反も残った。

したがって不足していたのは新しい発行資格ではない。`ready setを求めるpredicate`、`その集合を一つのmodel responseのtool-call集合へbindするtransition`、`全resultを受け取るまでmodel判断へ戻らないclosure`が別々に解釈可能だったことが原因である。論理定義の正しさを、実際の発行完了receiptの代用にしていた。

C192から保持するのは次の境界だけである。

- requested resultを消費するbind済みnonterminal operationがないinvocationは発行しない。
- 先行resultが後続のtarget、permission、methodまたはstop conditionを変え得る場合だけ発行dependencyを置く。
- operation identity、lifecycle、predicateまたはresult格納先の分離だけでは発行dependencyを作らない。
- 共同発行はcompound invocationへの統合を意味せず、各invocationのmachine-bound result contractを保持する。
- 真正dependencyを越えないこと、`OWNER_ROLE`、review適用、current/prior admissionおよびterminal経路は非変更constraintとする。

C192から継承しないのは、独立した抽象gateとしての`DISPATCH_ADMISSION`と、その定義だけでexecutor挙動が変わるという仮定である。次設計の直接基盤はCandidate191とし、C192は判定軸、安全境界および失敗反例としてだけ使う。次設計では`dispatch_set_ready`と`dispatch_set_issued`を別責務へ戻さず、`dispatch_transition_terminal := ready setの全invocationが同一model responseから個別tool callとして発行済み ∧ 全invocation result受領まで別model判断なし`を一つのterminal predicateとして固定する。空集合ではtoolを発行せず、その非発行自体をdispatch transitionのterminal resultとする。

### 12. 発行遷移をterminal化すれば挙動を拘束できるという仮定

Candidate193はCandidate191を直接親とし、C192のconsumer・dependency判定を`dispatch_frontier`へ移した。さらに、frontierと現在responseのtool-call identity集合の一対一一致、個別tool call、全result収集を一つの`dispatch_transition_terminal`へ閉じた。設計時の仮定は、発行集合の判定と発行完了を一つのterminal predicateへ統合すれば、C192で分離していた論理判定と実挙動が分離不能になるというものだった。

ADR9 r2全9ケース45件は、この仮定の十分性を否定した。全TaskSpecで開始identity不一致時には後続read自体を停止するため、開始identity resultはreadの発行可否を変える真正なpredecessorである。それにもかかわらずCandidate193は28 / 45件でidentity確認とreadを同じmodel stepから発行し、正しい初回frontierは17 / 45件だけだった。同じケース内でも分離と共同発行が混在したため、`dispatch_transition_terminal`は実際のtool-call集合を一意に拘束していない。

ただし、同じADR9 r2 TaskSpecとtrace判定をCandidate191の保存45件へ適用すると、identity/read越境は36 / 45件、正しい分離は9 / 45件だった。Candidate193は直接親Candidate191に対して越境を8件減らしている。ケース別ではADR03、ADR04、ADR07、ADR08およびADR09で計11件改善し、ADR05とADR06で計3件退行、ADR01とADR02は不変だった。したがって「全く作用しなかった」でも「機序が成立した」でもない。発行順序への部分効果は観測したが、case内反復を一意に拘束するまでには至らなかった、と限定する。

参考として同じ開始停止文言を持つ保存traceを同じ方法で読むと、Candidate176 ADR9 r2はidentity/read越境42 / 45、Candidate147 ADR9 r1は40 / 45だった。Candidate176、Candidate191およびCandidate193はADR9 r2だがprompt変更軸が異なるため、Candidate191からCandidate193への直接差分以外を`DISPATCH_TRANSITION`の因果効果にはしない。Candidate147はcase revisionもr1であり、方向診断にだけ使い、互換比較へ入れない。

品質面でもADR05とADR06の各1件が期待`blocked`ではなく`unavailable`になった。ADR05では`OBS-PAIRED-SCOPE=missing`を、すでに`OBS-DESIGN`、`OBS-AUTHORITY`、`OBS-INVENTORY`および`OBS-CONSUMER-CONTRACTS`だけで成立する具体的witness certificateへ誤って依存させた。これは`REVIEW_JUDGEMENT`のcertificate dependency過大化である。ADR06ではreviewerが`positive_applicability_predicate`ではないfieldを繰り返し観測し、値を取得していないのにpositive applicabilityを主張した。rootの不受入は`REVIEW_RESULT_ADMISSION`どおりであり、失敗点はreview producerの観測target bindingと真正certificate形成である。

両失敗はCandidate193で観測したprompt-level regressionだが、identity/read共同発行との直接dependencyはtrace上成立しない。ADR05失敗runはidentity/readを正しく分離しており、ADR06失敗runは越境していたものの、越境resultがfield identityを変えた証拠はない。Candidate193の唯一差分が長い`DISPATCH_TRANSITION`追加であることから、注意配分または命令競合の間接影響は仮説に残るが、発行遷移の直接故障としては分類しない。

Candidate193から確定して残すものは次のとおりである。

- ADR9 r2では9ケースすべてで開始identityと後続readに真正dependencyがあり、共同発行対象ではないという訂正済み判定。
- consumer、target、permission、method、stop conditionおよびresult contractからpredecessorを判定する軸。
- 共同発行可能な一般経路でもcompound commandへ統合せず、個別tool callとmachine-bound resultを保持する境界。Candidate193ではcompound identity/read commandは0件だった。
- reviewer cardinality 45 / 45、artifact境界45 / 45、required command 15 / 15、forbidden canary delivery 0件という非退行部分。
- ADR05とADR06のScore 1を、certificate dependencyとresult admission後のouter terminalを再分析する保存反例として残すこと。
- Candidate193の登録result、品質監査および機序監査を、再実行で置換しない履歴証拠として残すこと。

次設計を固定する前に保留するものは次のとおりである。

- `dispatch_candidate`、`dispatch_predecessor`および`dispatch_frontier`の分解。ADR9ではpartial effectを観測したが、consumerなし空frontier、同時発行上限、cell ID付きnonterminalおよび真正な共同発行経路はこの評価で判定していない。
- `DISPATCH_TRANSITION`を独立条項にするか、C147の`DECISION_BOUNDARY`へ優先規則として戻すか。条項名や配置ではなく、C191比の8件改善と28件残存失敗を同時に説明できる設計が必要である。
- Candidate193を次Candidateの直接親にするか、Candidate191へ戻して必要成分だけを再構成するか。現時点ではどちらも固定しない。
- ADR05・ADR06が長い発行条項の注意干渉で増えたのか、N=5で顕在化した既存review経路の低頻度変動なのか。追加runではなく保存traceと条項競合の分析を先に行う。

反証されたため次設計へ持ち込まないものは次のとおりである。

- `dispatch_transition_terminal`と名付けて発行完了を宣言するだけで、現在responseのtool-call選択を一意に強制できるという十分性仮定。
- 17 / 45の正しいfrontierを、機序成立またはM5通過へ昇格すること。
- 機序監査r2の全fieldを訂正済み正本として使うこと。同監査は旧品質監査を入力にしたためADR06 iteration 2・3の`quality_score`が登録resultのScore 4ではなくScore 1になっている。さらに`result_kind_counts`は観測値でなく期待値を数え、review path判定の一部は文字列存在とterminal一致で近似している。28 / 45のdispatch集計とcommand call-ID再監査は利用できるが、品質とreview pathは登録result、品質監査r2および生traceを正とする。

したがって、次の直接基盤はまだ固定しない。Candidate191はreview・terminal経路と比較基準を提供し、Candidate193は発行分離の部分効果と新しい品質反例を提供する。C192はconsumer／dependency判定軸と抽象gate不十分の反例を提供する。M1では、C147の`DECISION_BOUNDARY`を含む既存命令間の優先関係、C193で部分効果を生んだ語義、およびADR05・ADR06のcertificate dependencyを分けて再確認する。

## C147の13条項の分類

この分類はM1からM2へ渡す責務分類であり、次Candidateの条項名、数、配置または語列を固定しない。

| C147条項 | 分類 | 保持する不変条件 | M2での扱い |
|---|---|---|---|
| `SPEC` | 改訂 | required outcome、operation identity、permission、constraintの事前bindingと局所性 | operation、predicate、outer terminalを明示し、review subjectやreview operationを同一operationへ暗黙合成しない |
| `PRODUCER` | 分割 | 一operation一producer、producer変更時の旧binding失効 | producer選択とresult authenticityを分け、reviewer未起動時の外側operation resultと混同しない |
| `TERMINAL` | 分割 | bind済みproducerのterminal resultなしにoperationをterminal化しない | result completeness、dependency closure、outer terminal形成を別責務にする |
| `CONTEXT` | 分割 | 許可入力、禁止入力、必要最小context | packet membership／stateとterminal dependency certificateを分ける。missing stateだけでpacket不成立にしない |
| `EVIDENCE_GATE` | 分割 | 未観測predicateへ結び付く証拠だけを発行し、局所的に失効する | evidence発行、observation result、implementation binding、artifact変更許可、追加evidence条件を別責務へ移す |
| `OWNER_ROLE` | 改訂して復元 | owner語列はproducer指定ではない。delegated resultはspawn identityとsender identityへbindする | Standard14の退行証拠により統合後削除を撤回する。owner metadataはreview適用条件、operation identity、producerおよびspawnを成立させない独立責務として保持する |
| `ROOT` | 統合後削除 | rootは非producer operationの意味resultを再生成しない | producer/result authenticity/terminal集約へ直接組み込み、独立した重複条項を残さない |
| `INDEPENDENCE` | 改訂 | 先行resultを対象にする別operationは別predicate、producerを持つ | operation dependencyの形成規則へ改め、同一predicate再割当て禁止だけでなく、どのresult atomが何へ依存するかを固定する |
| `DECISION_BOUNDARY` | 改訂方法を保留 | result効果をtarget、permission、method、stop conditionが変わり得る未発行範囲へ限定し、真正dependencyを越えない | result effectの局所性と発行順序の区別は保つ。C193はC191比で正しい分離を9件から17件へ増やしたが一意拘束には失敗したため、独立`DISPATCH_*`責務への分割も元条項への再統合もまだ決めない |
| `VALIDATION_CLOSURE` | 保持 | required validationのproducer、順序、個別result、早期停止 | review findingへ流用しない現行除外も保持し、review再構成から隔離する |
| `VALIDATION_PLAN` | 保持 | 変更後に一つの実行票へ検証をbindし、完了後に追加toolを出さない | review admissionのpacketまたはevidence探索へ混ぜず維持する |
| `METHOD` | 改訂 | 未固定手段の失敗をpermission否定へ読み替えず、同じpredicateへ継続する | tool failure、観測対象の`missing`、permission denial、review resultの`unavailable`を別stateにする |
| `RECOVERY` | 保持 | environment-only repairとsame command rerunを一組として数える | review判断の再実行やresult再生成をenvironment recoveryに含めないことを明示して維持する |

暫定集計は、保持3件、改訂4件、改訂方法を保留1件、分割4件、統合後削除1件である。C147の不変条件を無条件に削除する候補はない。`ROOT`は対応責務へ統合できるが、`OWNER_ROLE`はCandidate190 Standard14の具体的退行により独立責務へ戻す。`DECISION_BOUNDARY`は局所result effectと真正dependencyを保持し、C193の部分効果と残存変動を説明できるまで配置だけを保留する。

## M2へ渡す未解決predicateと必要観測

| 未解決predicate | M2で固定すべき入力・観測 | 解けない場合の停止 |
|---|---|---|
| `operation_identity_ready` | outer admission、review operation、observation operation、artifact changeのidentityとdependency | identityを横断してresultを合成せず停止 |
| `finite_direct_match` | 先行authorityのclosure identity、全effect、全relation、bind済み変更predicateとの直接一致 | 推論したgraphで`not_required`を作らず`required`へ進む |
| `review_requirement` | authority未固定の選択、除外、fallback、完全性判断へ変更predicateが依存するか | `not_required`を補完しない |
| `review_permission` | review operation作成前のpermission result | 否定ならreviewerを作らず外側operationを`unavailable`へ閉じる |
| `packet_ready` | 許可input identityの全件性、semantic projection、各identityの現在state | valueのmissingだけではfalseにしない。identity自体が未固定なら停止 |
| `observation_result_authentic` | observation identity、producer、invocation result、対象predicate、consumer | 観測なしのsuccess receiptをadmitしない |
| `counterexample_certificate_ready` | witness、applicability、規範predicate、直接矛盾、一般設計変更効果 | 一つでも依存入力不足なら`unavailable`。certificate外missingは無視する |
| `no_counterexample_certificate_ready` | 固定review scope、manifest全identity、各success receipt、反例predicateのclosure | 一件でもmissing等なら`unavailable`。未来全域の不存在は要求しない |
| `result_admissible` | bind済みproducer、sender、許可input、certificate、現在dependencyとの一致 | rootが意味を再判定せず不受入にする |
| `current_result_admissible` | current review operationのexecution permission、producer、sender、allowed kind、observation、certificate | 保存result用`result_use_permission`を追加要求しない |
| `prior_result_admissible` | prior identity利用許可、current subject等価性、`result_use_permission`、`result_still_valid` | 新規review execution permissionを要求しない |
| `result_still_valid` | certificate dependencyを変えた新resultの有無 | 無関係resultでは失効しない |
| `dispatch_order_ready` | consumerを持つinvocation、各resultが変え得るtarget・permission・method・stop condition、invocation間の真正dependency、既存命令の優先関係 | predecessor resultが発行可否を変える場合は後続を発行しない。抽象gateまたは自己terminal宣言だけで成立扱いにしない |
| `artifact_change_allowed` | finite direct matchまたはadmissible review terminal、permission、保持relation、禁止subject集合 | 一件でも未解決なら変更しない |
| `outer_terminal_ready` | 全required predicateのbind済みproducer resultとartifact/validation result | progressやfinal responseで補完しない |

M2ではこの表を新しい汎用schema、registry、canonical locatorまたは全入力分類mapへ変換しない。必要なのは各predicateのownerと一方向dependencyであり、全入力の意味完全性をprompt内で証明し切ることではない。

## Standard14へ保持する回帰境界

review制御の再構成で、少なくとも次を退行させない。

- criterion owner文字列だけで独立producerを起動しない。
- rootはworker resultを代行、再採点、上書きしない。
- worker packetへ禁止履歴または不要な全履歴を配送しない。
- resultの停止効果をtask全体へ伝播させない。
- consumerのない開始観測を発行せず、相互非依存なready invocationをoperation分離だけで別model stepへ送らない。
- validationは個別result、順序、早期停止、実行票closureを維持する。
- permission denialとmethod failureを混同しない。
- artifact変更前に必要なadmission resultが揃っていなければ変更しない。

C175とC176のStandard14 70 / 70はこれらの正常経路が成立し得る診断証拠であり、次設計の完全性証明ではない。M7では中核定義の再構成に合わせてStandard14全14ケースをADR9評価後に実行する。

## M1完了判定

- ADR01〜ADR09は5種類の証明責務へ全件分類した。
- 過去Candidateの狙い、仮定、実結果、成立部分、誤設計をcontrol boundaryへ変換した。
- 原因不明またはCandidate名だけの失敗は残していない。
- C147の13条項を保持、改訂、分割、統合後削除へ全件分類した。
- M2へ渡す未解決predicateと必要観測を列挙した。

初回M1成果物は完了後にM2〜M5へ進んだ。Candidate189 M5の反例からcurrent/prior admissionを修正してCandidate190へ実装した。Candidate190はM5とM6を通過したが、Standard14でowner metadataをreview operationへ昇格する具体的退行を観測したためM1へ再度戻った。原因はC147の`OWNER_ROLE`を統合後削除した責務圧縮と、review適用の正の明示条件不足に特定した。Candidate191はADR9全9ケースと高リスク拡張を通過し、Standard14も70 / 70 Score 4だったが、後続再判定で9ケースの共同発行退行が総token増分の86.74%を占めると確認した。原因をoperation分離とmodel step分離の混同、およびconsumerなし開始観測の許容へ特定した。

Candidate192はこの発行境界だけを`DISPATCH_ADMISSION`として定義した。対象Standard14 50件はすべてScore 4だったが、A01のconsumerなし開始identityが2 / 5に残り、退行8ケースのidentity/read共同発行は1 / 40だけだった。新しい原因は、発行資格と集合を論理定義しても、executorが各operationを宣言してから一段ずつ発行する既定手順より優先する具体的な発行遷移になっていないことである。`coissuance_ready(S)`の真偽を求める責務と、真なら同じ応答から全invocationを発行する責務が再び分離していた。

Candidate193はC192の判定軸を`DISPATCH_TRANSITION`へ移し、発行集合と収集closureを一つのterminalへ閉じたが、ADR9の真正dependencyを28 / 45件で越境し、ADR05・ADR06にも各1件のterminal不一致を残した。同じ新基準のCandidate191は越境36 / 45だったため部分効果はあるが、自己terminal化だけで挙動を一意拘束できるという十分性仮定は否定された。現在のM1は、上記の「確定して残すもの」「保留するもの」「反証されて持ち込まないもの」を境界として、C147の`DECISION_BOUNDARY`の優先関係と2件のcertificate dependencyを再分析中である。M2、次Candidateおよび追加評価は開始しない。後続の現在位置は[`review制御再構成マイルストーン計画`](review-control-reconstruction-milestone-plan.md)を正とする。
