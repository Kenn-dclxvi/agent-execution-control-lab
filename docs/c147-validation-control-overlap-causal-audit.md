# Candidate147 validation二制御群の重複原因監査

> [!IMPORTANT]
> **状態**: `partial_scope_190_preserved / saved_validation_runs_190_audited / required_command_groups_403 / one_wrapper_189 / split_wrapper_1 / repeated_required_command_0_in_190 / nonterminal_wait_runs_52 / wait_invocations_79 / wait_interleaving_0 / full_standard14_validation_followup_exec_22_audited / prebound_completion_evidence_22_of_22 / nonterminal_ticket_bypass_11 / terminal_visible_evidence_reacquisition_10 / split_ticket_1 / H2a_missing_relation_rejected`
>
> Candidate147の`VALIDATION_PLAN`と`VALIDATION_CLOSURE`について、文章上の類似ではなく保存runの実行routeを監査する。本監査の190件という部分scopeの結果は保持する。後続の[Standard14結果起点監査](c147-standard14-control-insufficiency-audit.md)でeventを読めるrequired-validation 685件へ広げて検出した「post-validation reentry」22件は、本監査で元rolloutまで追跡した。その結果、22件は不足したticket集合関係ではなく、既存closureからの三種類の逸脱だった。

## 結論

`VALIDATION_PLAN`と`VALIDATION_CLOSURE`の重なりは、現時点では行動上の冗長性ではなく、実行票からrequired validation closureへのhandoffとvalidation lifecycleの局所強化である。

保存rolloutから直接確認できるrequired-validation 190 runでは、403 required command groupの再実行は0件だった。189 / 190 runは全required commandを一つのcustom exec wrapperへ閉じた。nonterminal resultを受けた52 runの79 waitは、全件で同じvalidation invocationまたは直前の同一waitから続き、waitより先に別toolまたは利用者向けmessageを挟んだ例は0件だった。

残差は二種類ある。

- F04の1 runで、3 required commandを3 custom tool callへ分け、各result後にmodelへ戻った。
- 11 runで、最初のvalidation result後にdiff、status、変更source等の完了判定evidenceを別custom tool callから発行した。

これらは二条項が同じrequired commandを二重発行した結果ではない。既存の`VALIDATION_PLAN`がdiff / statusを含む実行票を事前固定し、`VALIDATION_CLOSURE`が全required commandを一つのwrapperへ閉じるよう要求しているにもかかわらず、そのclosureから外れた低頻度routeである。類似文を削除または統合しても消えると判断できず、むしろ既知のclosureを弱める。

190件の範囲で二条項の重なりを`optimization_hypothesis`から外し、`supported / intentional_handoff_and_specialization`とした判断は、22件の元rollout監査後も変わらない。22件を閉じる新しい`validation_ticket_items`関係は不要であり、H2aのCandidateは作らない。required commandを成功後に再実行した別の1件はresult admissionのH2bとして分離する。

## 監査対象

Candidate147 Standard14 N=100の全1,400 runのうち、現在のsession保存からcommand eventとtool-result順序を直接追える次の190 runを対象にした。

| 保存系列 | case内訳 | run数 | required command group数 |
|---|---|---:|---:|
| F06 N=29〜N=100の追加run | F06 95件 | 95 | 190 |
| remaining13 N=100最終wave | F01 3件、F02 23件、F03 23件、F04 23件、F07 canonical runner 23件 | 95 | 213 |
| 合計 | 6 case | 190 | 403 |

F06の先行5件と、remaining13のそれ以前のwaveはこの190件へ含めていない。登録済みStandard14 N=100の品質状態は1,400 / 1,400 Score 4だが、本監査のroute件数を未読のrunへ外挿しない。

## 判定軸

各runについて、artifact変更後のeventを次の順で照合した。

1. TaskSpecとcommand evidence protocolに列挙されたrequired command group。
2. required command groupを含むcustom tool call identity。
3. 同じrequired command groupの再実行。
4. required command完了前の別model tool roundtrip。
5. nonterminal result後のwait identityと、その前に挟まる別toolまたは利用者向けmessage。
6. required command完了後に発行したdiff、status、source readまたは追加validation。

tool call数自体をKPIへ昇格せず、二条項の重なりが同じ判断またはcommandを重複させたかを判定するdiagnosticとしてだけ使った。

## 実行routeの結果

### required commandの発行

| route | run数 | 判定 |
|---|---:|---|
| 全required command groupを一つのwrapperへbind | 189 / 190 | 正常closure |
| required command groupを複数custom tool callへ分割 | 1 / 190 | F04の低頻度closure違反 |
| required command groupの再実行 | 0 / 403 group | 二条項による二重発行なし |
| artifact変更後、required command前の追加tool | 0 / 190 | validation開始前の再探索なし |

F04の1件は`npm ci`、`npm run lint`、`npm run build`を三つのcustom tool callへ分けた。各commandは一回だけ成功経路へ使われており、同じvalidationを二つの条項が重複実行したのではない。

### nonterminal resultのclosure

| route | 件数 | 判定 |
|---|---:|---|
| nonterminal resultによりwaitを使ったrun | 52 / 190 | 対象経路 |
| wait invocation | 79 | 全件同じvalidation経路を継続 |
| waitより先に別toolを発行 | 0 / 79 | 違反なし |
| waitより先に利用者向けmessageを発行 | 0 / 79 | 違反なし |

この経路では`VALIDATION_PLAN`のnonterminal ticket保持と、`VALIDATION_CLOSURE`のterminal result必要条件が異なる入口から同じ誤完了を閉じている。片方の重複を削る根拠ではなく、防御的強化が実行時に消費されている証拠である。

### full Standard14で検出した22件の再分類

最初の190件では11件、full Standard14のeventを読めるrequired-validation 685件では22件が、最初のvalidation発行後にdiff、status、変更source等を別custom tool callから取得した。full集計のcase内訳はF02 3件、F03 2件、F04 9件、F06 5件、F07 canonical 3件である。

この22件の元rolloutについて、validation開始直前のassistant message、custom exec入力、custom exec出力、次のcustom tool callを照合した。全22件で、後から取得した完了判定evidenceはvalidation開始前に明示されていた。したがって、何をticketへ含めるかが未知だったrunは0件である。

| 最初のvalidation発行後の状態 | run数 | 実際のroute |
|---|---:|---|
| cell ID付きnonterminal result | 11 | 同じcellを待たず、別の`exec`で完了evidenceを取得 |
| terminal result内に後続evidenceがすでに表示済み | 10 | 入力失効なしで、表示済みのdiff / status / source等を別の`exec`から再取得 |
| required commandと完了evidenceを最初から別発行へ分割 | 1 | F04 iteration 97。`npm ci`、`npm run lint`、`npm run build`を個別発行し、その後に完了evidenceを発行 |
| 合計 | 22 | 全件で完了evidenceはvalidation前に既知 |

terminal 10件のうち6件は長いtool outputに途中省略表示があったが、後から再取得したevidence種別は省略前後を含むterminal output内ですでに確認できた。残る4件は途中省略もなかった。したがって、これら10件を「必要resultが欠けたための追加evidence」とは分類しない。

nonterminal 11件は、required commandが完了した後のreentryではない。validation wrapperがまだnonterminalなのに、同じcellへのwait以外を発行したticket継続違反である。このため、従来の`post-validation reentry`という集計名は検出用ラベルとしては保持できても、機序名には使えない。

ただし、現行本文にはすでに次がある。

- `VALIDATION_PLAN`: required validationと完了判定に必要なdiff / status等を一つの実行票へbindする。
- `VALIDATION_CLOSURE`: 全required validationを一つのwrapperから発行し、全result受領後に一度だけ完了判断する。
- `VALIDATION_PLAN`: 実行票完了後はresult失効等がない限りtoolを追加しない。
- `VALIDATION_PLAN`: cell ID付きnonterminal resultでは、実行票がterminalになるまで同じcell IDへのwaitだけを発行する。

したがって、22件は不足predicateまたは不足relationを特定する証拠ではなく、明示済みclosureからの低頻度逸脱である。`validation_ticket_items := required validations ∪ pre-bound completion evidence`を追加しても、全22件で既に認識されていた集合を再定義するだけで、新しい判断点を減らさない。

### 対象run

| case | iterationとrun ID |
|---|---|
| F02 | 12 `3217c539026e4e0c810a803d41474718`、20 `82e3d35f31a2462bb2447df686661f16`、84 `556737b2a8794da1870773e6c2763cfe` |
| F03 | 51 `e2caea97d47340f38a8283aa6682c013`、59 `4fb9be42e3ff421b9020f8ff9cf502b5` |
| F04 | 4 `b662a1878b5a4d3e9e7ca927c3562e2e`、21 `be64bed4b8134a58bde1981ef4c353a4`、28 `f6aa34fa484c4a7f9c380d8d47f2d09d`、53 `ffd0eeb5631c4610b7ea248edd1f205a`、70 `b240046809824c13835f2b84b688bb35`、90 `85f34a0eb03f4ef883810a5ffd894fc0`、91 `97823cf7c2244136b3a1662158a8c3b6`、94 `a076d4916b84496f9f17e1d17efcc699`、97 `ea6eb19b18e24bcc902076fe7ae69f23` |
| F06 | 5 `dcc13d3951834f7594292abf1eddd01e`、69 `b4df8039cd484b32b5209cc6ee29682b`、87 `61c5f525070f4acba279240e2e61b6e7`、94 `d115261c79a048a69af19858903fb626`、97 `ed3535e3d3bc47069002866b1c073875` |
| F07 canonical | 32 `3482f4a740f647a7a92dfcbb57d7835c`、90 `6a2dfbd1525b4d7bad1547b94d52f763`、95 `a635682eae9a40e5936757653302a9d5` |

## 二制御群の責任境界

| 制御群 | 固有責任 | 重なる位置 |
|---|---|---|
| `VALIDATION_PLAN` | validation set、順序、method、diff / status等を一つのticketへ固定し、nonterminal時もticket identityを保持する | ticketがterminalになるまで別判断へ戻さない |
| `VALIDATION_CLOSURE` | readiness、個別command発行、exit判定、fail-fast、全result admission、validation operation terminalを閉じる | 全result後に一度だけ完了を判断する |

前者が「何を一つの実行票として継続するか」、後者が「その実行票のrequired validation resultをどう発行・判定・閉鎖するか」を所有する。両方に一回判断が現れるのは、同一ownerの重複ではなくticket persistenceからterminal admissionへのhandoffである。

## 履歴反例との対応

- Candidate69からCandidate71は`VALIDATION_CLOSURE`だけを追加し、Standard14 N=5でtoken中央値`-28.52%`、elapsed中央値`-6.65%`、required validation欠落0件となった。
- Candidate72 / Candidate73はclosureを短縮し、F06の編集後model再入を増やした。抽象名またはtool closureだけではresponse closureを維持できなかった。
- Candidate81はwrapper precedenceを明示し、複数required command caseのone-step closureを30 / 35から35 / 35へ改善した。
- Candidate105〜Candidate108はnonterminal result後のticket継続を`VALIDATION_PLAN`へ固定した。Candidate107のF03 B20では同一cell wait 6 / 6、required validation再実行0 / 100となった。
- Candidate110 / Candidate111の抽象的なdecision boundary置換は、terminal前model再入を完全には閉じなかった。

二条項は別の失敗系列で独立に効果を持ち、現在の190 runでもwrapper closureとwait closureの両方が消費されている。統合または片側削除を安全とする保存反例はない。

## 現在判断

| 仮説 | 判定 | 理由 |
|---|---|---|
| 二条項がrequired commandを二重実行させる | `rejected` | 403 groupで再実行0件 |
| 二条項の類似文が通常runへ二回の完了判断を加える | `rejected` | 189 / 190件は一wrapper、wait 79件もinterleaving 0件 |
| 二条項を統合または片側削除できる | `change_not_justified` | 固有責任と独立反例があり、現在の残差は明示済みclosure違反 |
| validation後続発行22件を新しいticket集合relationで閉じる | `rejected / duplicate_control` | 22 / 22件で完了evidenceは事前認識済み。11件はwait-only違反、10件は表示済みresultの再取得、1件は既存one-ticket規則への違反 |

full eventで再開したH2aは、22件の元rollout監査まで完了した。正常routeとの差は新しいticket membershipではなく、既存のone-ticket、wait-only、terminal後追加tool禁止を守ったかどうかである。H2aは`existing_control_deviation / candidate_not_justified`として閉じる。F02のsuccessful required command再実行1件だけは、machine terminal statusと表示payloadを分けるH2bとして残す。

## 参照

- [`Candidate147 制御群・境界重複・最適性監査`](c147-control-group-overlap-optimality-audit.md)
- [`Candidate69 / Candidate71 Standard14 N=5`](../evaluations/results/candidate69-candidate71-validation-closure-v10-standard14-n5_2026-07-22.md)
- [`Candidate81からCandidate125までのprompt制御知見`](candidate81-candidate125-control-findings-synthesis.md)
- [`Candidate147 Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [`Candidate147 Standard14結果起点の制御不足監査`](c147-standard14-control-insufficiency-audit.md)
