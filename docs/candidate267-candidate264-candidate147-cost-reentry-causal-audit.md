# Candidate267・Candidate264・Candidate147 cost再入原因監査

> **設計優先順位の訂正**: 本監査で特定したcarrier permissionとtruncation dependencyは原因診断として保持するが、次Candidateの先行差分にはしない。先に、[`Candidate254からCandidate267までの自然語feedback優先監査`](candidate254-candidate263-candidate267-natural-language-feedback-priority-audit.md)に従い、Candidate254を直接の基盤として、Candidate263からCandidate267までで成立または不成立を確認した関係だけを自然語へ再構成する。Candidate147は本文の複写元にせず、KPIと機序の比較基準に限る。carrier設計はその後も問題が残る場合だけ再開する。

## 結論

Candidate267はF10の目的を達成した。exact `src/AGENTS.md`のterminal success content result前に配下readへ進む経路を0 / 5件へ閉じ、result後の必要readも5 / 5件で完遂した。F01・F02・F03の固定済み保持観測も各5 / 5件だった。

ただし、採用条件は満たしていない。Candidate267はCandidate264比でtoken `+31.44%`、経過時間`+10.98%`、Candidate147比でもtoken `+28.63%`、経過時間`+12.73%`だった。F10のtoken中央値差はCandidate264比`+1.88%`、Candidate147比`+4.65%`に限られる。大きな増加は、Candidate267の本文差分が適用されないF01とF02へ集中した。

直接使用先は二つへ分ける。

1. nonterminal tool result後に、同じ完了を待つためmodelが再入した。Candidate267は20件中10件、外部`wait` 29回であり、C147の4件・6回、C264の6件・6回より多い。
2. 再入がないrunにも、observable carrierを超える変更前read、大きな成功stdout、およびtruncation warningを兄弟result全体の失効へ伝播させた後の重複確認がある。Candidate267 F02には`wait=0`でも275,558 tokenのrunがあり、再入だけではF02退行を説明できない。

Candidate267がCandidate264へ加えた差分は、normalized exact pathで宣言されたinstructionと、そのterminal success content result前の配下read permissionを結ぶF10限定の一段落だけである。したがって、F01・F02・F03の実行経路差をF10閉鎖の必要費用へ昇格させない。Candidate267は`unjustified_cost_regression`のまま停止し、この監査から待ち時間、tool順または成功runの処理順を新しいCandidateへ転記しない。

## 三候補の位置づけ

| Candidate | この監査での役割 | F10 instruction result前配下read | F10 result後の必要read |
| --- | --- | ---: | ---: |
| Candidate147 | 長期比較基準。F01〜F03正常経路の成立例と、F10未閉鎖の反例 | 3 / 5件で発生 | 5 / 5件完遂 |
| Candidate264 | Candidate267の直接の基盤と直接比較基準 | 3 / 5件で発生 | 5 / 5件完遂 |
| Candidate267 | exact pathとterminal success resultでF10 permissionを閉じた対象 | 0 / 5件 | 5 / 5件完遂 |

C147とC264はF10で安い正常経路を示した基準ではない。どちらも5件中3件で、instruction resultを受け取る前に配下readを発行できた。F10の低いcostは比較値として保持するが、そのままCandidate267の削減目標または実行手順にはしない。

## C147で成立していたか

今回特定したobservable result carrier閉鎖は、C147でも成立していない。

| 境界 | C147本文 | C147の実行証拠 | 判断 |
| --- | --- | --- | --- |
| `carrier_admission_ready` | requested resultがpredicateをbind可能であることは要求するが、required field/regionのprojection上限とcarrier capacityの関係は持たない | F02 run `2d7133babab74be3a61096f6c4257aa3`で初回出力が切れ、関数本体とassertionを追加read | 未成立 |
| `truncation_effect_scope` | artifact変更または失敗resultが入力を変えたpredicateだけを失効する関係は持つ | carrierの部分truncationをfield/region単位で兄弟resultから分離する定義はない | 前身はあるが未成立 |
| `success_output_required` | validation resultを一度だけmodelへ返すが、成功stdout全体をcarrierへ載せるpermissionは制限しない | compactに返して追加確認を避けたrunはあるが、promptで再現を保証していない | 未成立 |
| external `wait`排除 | nonterminal resultをoperation未完了として保持する | 対象20件で4 run、6回のexternal `wait`が発生 | 未成立。ただしpromptで閉じる対象ではない |

C147で成立していたのは別の関係である。`result_effect_scope`により、先行resultが影響しない未発行operationへ停止効果を広げず、F01〜F03の開始identity確認と必要readを同じmodel stepから発行できた。また`VALIDATION_CLOSURE`は、順番のあるvalidationを一つのcustom exec wrapper内で完遂し、全result受領後に一度だけ判断する構造を持っていた。

この二つは次設計でも保持対象だが、今回のcarrier閉鎖そのものをC147から復元するとは表現しない。C147の一部runがcompactな結果表現を選んで安く完了したことは成功したexecution methodであり、C147本文がそのmethodを強制していた証拠ではない。

## KPI比較

### 全体

| Candidate | quality | total_tokens | elapsed_seconds |
| --- | ---: | ---: | ---: |
| Candidate147 | 100.0 | 494,706 | 302.929 |
| Candidate264 | 100.0 | 484,121 | 307.710 |
| Candidate267 | 100.0 | 636,348 | 341.495 |
| Candidate267 − Candidate147 | 0.0 | `+141,642`、`+28.63%` | `+38.567`、`+12.73%` |
| Candidate267 − Candidate264 | 0.0 | `+152,227`、`+31.44%` | `+33.785`、`+10.98%` |

C264はC147比でtoken `-2.14%`、経過時間`+1.58%`だった。C267の全体退行は、C264がC147から既に持っていた固定費の単純な継承ではない。

### ケース中央値

| ケース | C147 token / 秒 | C264 token / 秒 | C267 token / 秒 | C267 − C147 | C267 − C264 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,202 / 66.424 | 145,447 / 72.577 | 190,258 / 85.859 | token `+77.48%`、秒 `+29.26%` | token `+30.81%`、秒 `+18.30%` |
| F02 | 128,236 / 100.607 | 133,018 / 80.972 | 222,958 / 98.779 | token `+73.87%`、秒 `-1.82%` | token `+67.61%`、秒 `+21.99%` |
| F03 | 104,320 / 70.866 | 133,285 / 77.404 | 134,086 / 85.896 | token `+28.53%`、秒 `+21.21%` | token `+0.60%`、秒 `+10.97%` |
| F10 | 87,934 / 61.546 | 90,323 / 71.026 | 92,021 / 68.126 | token `+4.65%`、秒 `+10.69%` | token `+1.88%`、秒 `-4.08%` |

F01とF02がC267対C264のtoken退行を担う。F03はtokenがほぼ同じなのに時間だけ増え、F10は小さなtoken差と時間改善である。したがって、四ケースを一つの原因で説明しない。

## モデル再入の課題

### 数え方

ここでいうモデル再入は、生traceの`response_item.payload.type=function_call`かつ`name=wait`である。すでに発行した処理がnonterminalで返った後、modelが同じcellの完了待ちだけをもう一度発行した回数を数える。custom exec wrapperの内部で行うpollは、modelへ結果を返さないため数えない。

既存のCandidate267機序監査は「外部`wait`があったrun数」を「wait invocation数」として記録し、ケース配分も誤っていた。本監査でraw rolloutとatomic run IDを結び直し、次へ訂正した。

| Candidate | F01 run / 回 | F02 run / 回 | F03 run / 回 | F10 run / 回 | 合計run / 回 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Candidate147 | 1 / 1 | 2 / 4 | 1 / 1 | 0 / 0 | 4 / 6 |
| Candidate264 | 3 / 3 | 0 / 0 | 3 / 3 | 0 / 0 | 6 / 6 |
| Candidate267 | 4 / 15 | 3 / 7 | 3 / 7 | 0 / 0 | 10 / 29 |

Candidate267の`wait`応答が直接使ったtokenは、20 run合計でF01 432,789、F02 231,975、F03 172,749、合計837,513だった。これは同じrun内のwait応答に記録された`last_token_usage.total_tokens`の合計であり、waitがなければ必ずその分だけ減るという反実仮想KPIではない。

代表例はF01 run `76a9f65f4c144165a1199c60ed042e68`である。総418,599 tokenのうち、10回の完了待ちだけで294,139 token、70.27%を使った。F02のtoken中央値run `6d697865b42e47c2b18f3d3468e2bfeb`も、222,958 tokenのうち3回の待ちが99,924 token、44.82%を使った。再入はC267の大きなtoken使用先である。

ただし、発生頻度をCandidate267のprompt差分へ因果帰属しない。C147でもF02の2件が各2回待ち、256,795と263,517 tokenになった。C264でもF01・F03に各3件ずつ一回の待ちがある。三候補ともF10は0回であり、C267のF10限定差分がF01〜F03のtool処理をnonterminalにした証拠はない。

この課題からprompt Candidateへ持ち込める新しいpermissionまたはdependencyは、現在はbindできていない。特定の待ち時間、tool呼び出し構成または成功runの順序を固定しても、最初のtool returnがterminalになることは保証できない。

## モデル再入以外の課題

### 1. F02は再入だけで退行していない

Candidate267 F02 run `1e1ae860e79f44f581419314a7ef6910`は外部`wait`が0回だが275,558 tokenだった。このrunは、開始確認とルートinstruction、四つの対象・test read、追加範囲readを三回の変更前tool resultへ分けた。四つのreadを同居させたresultはoriginal 14,538 tokenでtruncatedとなり、実装をbindするために必要な`_resolve_market_end_date`の本文と`tests/unit/test_v4_engine.py`がmodel-visible resultに残らなかった。そのため追加範囲readへ進んだ。

変更後のvalidation resultもoriginal 39,896 tokenでtruncated warningを伴った。ただし同じmodel-visible result内には、focused gateとfull gateの成功だけでなく、`git diff --check`、diff、statusのterminal receiptも存在した。それにもかかわらず、同じ三確認を別tool callで再発行した。

変更前の追加readと変更後の再確認は同じではない。変更前resultでは必要なfieldが実際に欠け、`implementation_bound`が成立しなかった。validation resultでは兄弟receiptが実際に存在し、truncatedなのは大量のtest stdoutの一部だった。後者の追加確認は新しい品質、変更または機序観測を生んでおらず、現行`VALIDATION_PLAN`の「実行票完了後は追加要求またはresult失効がない限りtoolを追加しない」とも一致しない。

### 2. F01にも検証完了後の重複確認がある

Candidate267 F01のtoken中央値run `3281af66320d40fba41f82132fced9ac`でも、original 39,896 tokenのvalidation resultにtruncated warningが付いた。ただし`git diff --check`とstatusのreceipt自体は同じresult内に存在した。modelは「最終のdiff/status証跡だけ受領結果から省略された」と判断し、同じ二件を別tool callで再発行した。これはwarningの効果を、実際に欠けたtest stdoutのfieldから、存在する兄弟receiptへ広げた誤った失効である。C267側の一回のwait 27,370 tokenに加えて、この重複確認が別のAI応答と結果入力を増やした。

### 3. 結果表現とread分割の固定費をCandidate差分へしない

同じread対象でも、一つのtool resultへまとめるか、複数の結果をJSON文字列として返すかで、後続のmodel-visible入力量が変わる。F02の追加範囲readや大きな出力切断も、後続応答へ固定費として積み上がる。しかし、C267本文はcommand数、出力表現またはreadの行範囲を固定していない。観測された実行方法を新しい手順へ転記しない。

### 4. F03の時間増はtoken原因と分ける

F03はC264比token `+0.60%`だが、経過時間は`+10.97%`だった。C267のwaitあり3件・7回に対し、C264はwaitあり3件・3回なので応答回数差はある。一方、ケースtoken中央値はほぼ同じであり、時間増だけから新しいprompt境界を導かない。実行時間の揺れをtoken退行またはF10 permissionの費用と同一視しない。

### 5. F10の必要依存は削らない

Candidate267のF10は、`src/AGENTS.md`のcontent resultを受け取るAI境界を一回必要とする。C147とC264の3 / 5件はこの境界前に配下readへ進んだため、手数の少なさを合法な高速経路とは扱えない。F10の小さなtoken差だけを理由にinstruction readと配下readを再び共同発行しない。

## 特定したpermissionとdependencyの辺

### 1. oversized carrierを発行できるpermission

現行`EVIDENCE_GATE`は、requested resultが未観測predicateをbindできるかを見ているが、そのresultの必要fieldまたはregionがmodel-visible carrierへ残るかを発行条件にしていない。そのため、各inner readでは大きな出力を許しながら、四つを集約するouter carrierの容量をbindしないF02の発行がprompt準拠のまま到達可能だった。

開いている辺は次である。

`requested evidence identities -> carrier容量未確認のinvocationを許可 -> 必要regionがtruncated -> implementation_bound=false -> 追加AI判断と追加read`

閉じる候補は、tool順や行範囲ではなく、発行前のobservable output境界である。

`carrier_admission_ready(invocation) := requested resultごとにpredicateをbindするrequired field/regionが固定済み ∧ 全projectionの上限がmodel-visible carrier capacity内 ∧ sibling resultを欠落させない`

`carrier_admission_ready=false`のinvocationは発行対象へ入れない。executorは同じpredicateとread permissionを保ったまま、narrower projection、別carrierまたは他の未固定手段を選ぶ。どのcommand、行範囲またはtool構成を使うかは固定しない。

この辺はC267だけで新しく開いたものではない。C147 F02 run `2d7133babab74be3a61096f6c4257aa3`も、初回の関連箇所出力が切れた後に関数本体とassertionを追加readしており、C264 F02 run `5c3a53198c3a436fa1be3c1d67ba3453`も変更前readを二回に分けた。C267はこの既存のcarrier未拘束を継承し、outer carrier容量とinner result上限の不整合を明示的に再現した証拠である。

### 2. partial truncationを兄弟resultへ伝播できるdependency

現行promptは、変更や失敗が入力を変えたpredicateだけを失効できると定める一方、複数resultを運ぶ一つのcarrierが部分的にtruncatedになった場合の効果範囲を定めていない。F01とF02のvalidationでは、この空白により、test stdoutのtruncation warningが、同じresult内に存在するdiff/status receiptまで失効させるdependencyとして使われた。

開いている辺は次である。

`carrier-level truncation warning -> carrier内の全resultをmissing扱い可能 -> satisfiedな兄弟predicateをunobservedへ戻す -> 重複evidenceを許可`

閉じる候補はresult identityとfield/region単位の失効範囲である。

`truncation_effect_scope := required field/regionがmodel-visible resultから実際に欠けているresult identityだけ`

`result.identity ∉ truncation_effect_scope`で、terminal stateとpass condition valueが存在するなら、そのresultは`satisfied`のまま保持する。carrier-level warning、別resultのraw stdout欠落、正確な行位置の欠落は、存在する兄弟receiptを`unobserved`へ戻せない。

### 3. success stdoutがterminal receiptを圧迫できるpermission

F01とF02のvalidation carrierは、必須commandの成否をbindするために不要な大量のsuccess stdoutを運び、original 39,896 tokenになった。合格条件がexit codeで固定されているcommandでは、command identity、terminal state、exit codeおよび必要なpass condition valueがreceiptであり、成功stdout全体は必須resultではない。

したがって、`success_output_required := TaskSpecまたはpass conditionがstdout content自体を要求`とし、falseならraw success stdoutを、後続のterminal receiptを圧迫できるmodel-visible carrierへ載せるpermissionを与えない境界が候補になる。failureまたはunexpected stateの診断に必要な出力は別であり、一律にstdoutを禁止しない。

### 4. external waitには閉じるべきprompt permissionがない

nonterminal cell resultを受け取った後の`wait`は、現行`VALIDATION_PLAN`が要求する合法な同期である。別operation、追加readまたは新しい判定へ進むpermissionはすでに閉じている。問題は最初のtool invocationがterminalになる前にruntimeからmodelへ返ることであり、repository prompt内のpredicate判断の誤りではない。

したがって、external waitからCandidate差分を作らない。待ち時間、yield、command構成または成功runのtool順を固定しても、terminal返却のdependencyはpromptだけでは閉じられない。Candidateで扱えるのは、上のcarrier admission、truncation effect scope、およびsuccess output permissionである。

## 課題一覧と扱い

| 区分 | 課題 | 現在の判断 | 次の扱い |
| --- | --- | --- | --- |
| モデル再入 | external `wait`がC267で29回発生し、F01・F02の主要token使用先になった | 直接使用先は確定。閉じるべきprompt permissionはない | C268の差分にしない。追加Nも発行しない |
| モデル再入 | 監査がrun数とwait回数を混同した | 計測定義の不備 | 機序監査JSONと結果文書を訂正済み |
| 再入以外 | F02でcarrier容量をbindせず四readを集約し、必要regionを失った | oversized carrierの発行permission | `carrier_admission_ready`で閉じる設計候補あり |
| 再入以外 | F01・F02でtruncation warningを存在するdiff/status receiptへ伝播した | partial resultの失効dependency | `truncation_effect_scope`で閉じる設計候補あり |
| 再入以外 | 成否判定に不要なsuccess stdoutがreceipt carrierを圧迫した | raw success outputのcarrier permission | `success_output_required=false`時のcarrier境界候補あり |
| 再入以外 | C147・C264のF10低costには違法な先行readが混ざる | cost比較は可能、合法経路の基準には不可 | F10合法経路内でのみ削減可能性を評価する |
| 横断 | C267の差分外ケースが全体costを支配した | F10機序費用として正当化不能 | `unjustified_cost_regression`で停止を維持 |

## 次Candidateの境界

この監査により、将来検討できる辺は`carrier_admission_ready`、`truncation_effect_scope`、`success_output_required`まで特定した。ただし、C147機序とKPIを復元する前に、この三つをCandidate差分へしない。Candidate268もcarrier差分としては作成しない。

1. Candidate254の自然語本文を正本に、Candidate263からCandidate267までで成立または不成立を確認したpermission・dependency関係を対応づける。
2. Candidate254の自然語構造を保持し、Candidate264で確認したF01からF03の効果とCandidate267で確認したF10閉鎖に必要な関係だけを自然語で再構成する。C147本文とCandidate264以降の形式記法は複写しない。
3. C147比の品質、対象機序、preserved route、tokenおよび時間を先行gateにする。固定入力費用を直す場合も、機序を保つ自然語の意味保存簡潔化に限定する。
4. 成功runのtool順、待ち時間、command構成、行範囲または特定の出力形式を実行義務へしない。
5. carrier境界はC147同水準化後にも問題が残る場合だけ別objectiveとして再開する。

現在状態は`f10_objective_achieved / natural_language_control_invariant / candidate147_comparison_and_mechanism_reference_only / candidate147_text_copy_forbidden / candidate147_and_candidate264_f10_counterexample_preserved / external_wait_reentry_direct_cost_confirmed / external_wait_prompt_edge_absent / oversized_carrier_admission_edge_bound_diagnostic_only / partial_truncation_invalidation_edge_bound_diagnostic_only / success_stdout_carrier_permission_edge_bound_diagnostic_only / natural_language_mechanism_equivalence_first / carrier_design_deferred / unjustified_cost_regression / candidate267_stopped / candidate268_not_created / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。

一次証拠はCandidate147登録result `29cf98307448409f820a739b2d008f7b`、Candidate264登録result `1a64c1b2429c4e89aff3aedd6836944e`、Candidate267登録result `e4dee1e302a2468ba055500a0c3610d7`、各resultの保存済みatomic runとraw rolloutである。
