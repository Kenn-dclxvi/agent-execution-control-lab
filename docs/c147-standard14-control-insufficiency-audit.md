# Candidate147 Standard14結果起点の制御不足・過剰品質境界監査

> [!IMPORTANT]
> **状態**: `standard14_n100_primary_result_bound / quality_1400_of_1400 / three_kpi_bound / diagnostic_semantics_classified / archived_event_runs_1385_audited / root_reread_runs_130 / start_gate_review_read_overcoissue_19_of_100 / start_gate_barrier_rejected_as_current_overquality / validation_false_unavailable_rerun_1_of_685 / hidden_full_exit_normal_59_of_60 / validation_followup_exec_22_of_685 / H2a_existing_control_deviation / H2b_positive_admission_not_yet_necessary / cost_reduction_hypotheses_2 / candidate_not_created`
>
> 本監査はCandidate147の本文だけから最適化余地を推測しない。Standard14 N=100の一次result、case別KPI、quality diagnosticおよび保存event routeから、成立した制御、品質を保ったまま削減し得るcost、現在のoracleでは便益を観測できない過剰品質案を分ける。既存result、prompt bundle、profileおよび評価条件は変更せず、新しいslotも発行しない。

## 結論

Candidate147のStandard14 N=100は1,400 / 1,400 Score 4であり、固定14ケースにおける成果品質とterminal成立は強い。一方、この品質通過だけからC147を最適、最小、または不足なしとは判断できない。

保存eventを読める1,385 / 1,400 runを再監査すると、次の未閉鎖経路があった。

1. root `AGENTS.md`のC147本文をtoolで再取得したrunが130 / 1,385件あった。特にF10 monthly reviewは99 / 100件だった。
2. F10 monthly reviewの19 / 100件は、identity確認と少なくとも一つのreview対象readを同じ発行群へ入れた。全19件はScore 4で、token中央値もgate先行群より低かった。したがって、この経路を禁止する開始バリアは現行oracle上の最適化候補ではなく、未観測driftに備える過剰品質案である。
3. required-validation対象685件では、F02の1件がmachine-bound `exit_code=0`とtest summaryを受領した後、表示途中省略を「exit証跡欠落」と誤認して`main_verify`を再実行した。最初のvalidation発行後に別のmodel発行群から完了evidenceを追加したrunは22 / 685件あり、元rollout監査では不足relationでなく既存closureからの逸脱だった。
4. F10 monthly reviewの数値位置は累積94 / 100 exact、6 / 100 mismatchだった。全6件は同じ誤動作と影響を正しく指摘し、変更行`25`の隣接するassignment位置`24`を示した。これはreview応答精度の残差だが、現在のratingではdiagnostic-onlyであり、制御不足へ自動昇格しない。
5. owner / producer evidenceの`inadmissible` 950 / 1,400件は不足件数ではない。case別にはA01、A02、F01だけがeligibleで、他のowner語列は独立producer executionの明示ではない。C147が不要workerを起動しない正常経路と一致する。

したがって、現在の最適化対象はruntime語の単純削除でも、未観測の安全性を足すことでもない。Standard14で品質を保ったままcostを減らせる可能性が観測された対象は、次の三つである。

- model-visibleまたは受領済みのadmitted evidenceを、入力が失効させるまでcurrent resultとして保持し、同じidentityを再取得しない状態遷移。
- machine-bound terminal statusと必要なpass summaryがあるresultを、表示本文の省略だけで`unavailable`へ戻さないresult admission条件。

これらは別の変更軸である。root再読とfalse-unavailable再実行を一つのCandidateへ混ぜない。22件のvalidation後続発行は、追加するrelationではなく既存制御からの逸脱として分離する。F10 monthlyのreview開始前readは、現行結果では削減対象ではない。

## 監査境界

### 一次result

| 項目 | Candidate147 Standard14 N=100 |
|---|---:|
| valid / Score 4 | 1,400 / 1,400 |
| Score 3以下 | 0 |
| excluded attempt / controller error | 0 / 0 |
| quality中央値 | 100.000 |
| all-agent token中央値 | 1,394,412.5 |
| elapsed中央値 | 831.914秒 |

case別中央値は全14ケースでControlFreeRepositoryよりtokenとelapsedが低かった。ただしFreeはA01で100件のScore 0を含み、quality分布が異なるため、同一品質の効率差とは扱わない。

### event route

Standard14 N=100を構成した保存waveのうち、現在のarchiveから`codex-events.jsonl`を読める1,385件を対象にした。内訳はStandard14 N=5追加55件、F06追加95件、remaining13追加1,235件である。先行targeted評価から再利用したF01 / F02 / F03各5件、計15件はこのevent route集計に含めない。一次qualityと3 KPIは全1,400件の登録resultを使う。

route件数を未読15件へ外挿しない。

## diagnosticを不足へ読み替えない境界

### owner / producer evidence 950件

保存event 1,385件のcase別状態は次だった。

- A01 100 / 100、A02 100 / 100、F01追加95 / 95はeligible。
- F02、F03、F04、F05二種、F06、F07二種、F08、F10二種は全件inadmissible。

後者のTaskSpecには`owner=independent ... check`があるが、独立producer execution、task identityまたはworker result consumerは明示されていない。C147の`PRODUCER / OWNER_ROLE`はowner metadataだけからworkerを作らない。Candidate190でこの境界を統合後削除した際に不要review producerが8件発生した反例もある。

したがって950件は「producerが950件不足した」という意味ではない。collectorのeligibilityとTaskSpecのproducer要求を分離し、C147の正常なroot producer経路を保持する。

### monthly numeric location 6件

N=5の5件は全てexactで、追加95件はexact 89、mismatch 6だったため、累積はexact 94 / 100、mismatch 6 / 100である。6件の応答は全て次を満たした。

- `format_test=args.format_test`から`format_test=args.force`への変更を特定した。
- `--format-test`が通常送信へ進み得ることと、`--force`がformat testで終了することを説明した。
- finding count 1、major、zero driftを満たした。

mismatchは固定diffの追加行`25`ではなく、同じassignmentの表示位置`24`をlocationにしたものだった。review内容欠落ではないが、正確な行位置という応答精度残差として保持する。これをprompt制御へ足すには、一般review契約でexact lineをrequired outcomeにする別のoracleが必要であり、現在のStandard14 ratingを事後変更しない。

## Standard14 routeで観測したcost削減余地

### 1. admitted evidenceの状態保持

root `AGENTS.md`の本文取得は1,385件中130件だった。`find ... AGENTS.md`や`rg --files`によるlocatorだけのcommandは含めず、`sed / cat / nl / rg`または`git show <commit>:AGENTS.md`で本文を取得したrunを数えた。

| case | root C147本文のtool再取得run |
|---|---:|
| A02 | 2 / 100 |
| F02 | 1 / 95 |
| F04 | 4 / 100 |
| F06 | 6 / 100 |
| F07 canonical | 5 / 100 |
| F08 | 13 / 100 |
| F10 monthly | 99 / 100 |
| その他7ケース | 0 / 790 |
| 合計 | 130 / 1,385 |

同じcase内でroot本文再取得あり・なしの両群が複数件ある主要4ケースを、登録済みKPIへbindした。値は`token中央値 / elapsed中央値`である。

| case | root再取得なし | root再取得あり | ありrun数 |
|---|---:|---:|---:|
| F04 | 156,922.5 / 84.514秒 | 188,456 / 104.689秒 | 4 |
| F06 | 104,844 / 76.465秒 | 184,633 / 86.682秒 | 6 |
| F07 canonical | 101,569 / 62.492秒 | 131,993 / 71.090秒 | 5 |
| F08 | 100,271 / 59.953秒 | 112,812 / 59.225秒 | 13 |

F04、F06、F07 canonicalでは再取得群のtokenとelapsedがともに高く、F08ではtokenだけが高かった。routeは無作為割当てではなく、他の追加readも混在するためroot再取得の単独因果値にはしない。ただし「現行costが観測されていない」という旧判断は棄却できる。A02、F02は再取得群が各2件、1件、F10 monthlyは非再取得群が1件だけなので群間中央値を判断へ使わない。

F10 monthlyの99件はcommand executionの実体で再確認した。引用符付き`sed`、`nl`、`git show <commit>:AGENTS.md`も本文取得として数え、locatorだけのcommandは含めていない。再取得しなかったiteration 88もScore 4で、root本文を再取得せず`src/AGENTS.md`、固定diff、changed file、`monthly_engine.py`から同じmajor findingとzero driftを成立させた。root再取得99件の中央値は93,597 token / 56.639秒、非再取得1件は93,948 token / 48.684秒である。1件とのtoken差は因果値に使えないが、root再取得が品質成立の必要条件ではない反例になる。

全runは同じCandidate147 bundle identityを使い、root C147本文は実行inputのrepository instructionとして供給される。F06の個別監査でもtool前のroot本文可視性を21 / 21件で確認済みである。したがって、少なくともF10 monthlyの99件を「不足authorityを得る正常read」と一括判定できない。対して`src/AGENTS.md`や`tests/AGENTS.md`はpath-local instructionであり、開始inputへ含まれない場合の取得を保持する。

C147の`EVIDENCE_GATE`はconsumer、未観測state、追加evidenceの開放条件を定めるが、model-visible inputまたは受領resultをどのidentityでcurrent stateへadmitし、どの入力が来るまで再利用するかを正の状態遷移として固定していない。この不足により、同じroot authorityの再取得と、runner-verified開始条件を`.agents / .codex`から探すprobeが残り得る。

F10 monthlyのTaskSpecが`AGENTS.md`を許可readへ列挙していても、それはread上限であって発行要件ではない。C147にもpermission / allowed readをevidence開放条件にしない規則はある。99 / 100件がrootを「許可されたauthority」として再取得した事実は、禁止の不足ではなく、model-visible instructionを`observed / current`へ移す正のadmissionが曖昧なことと整合する。

追加候補は「rootを読まない」という禁止ではない。次の関係である。

```text
admitted_evidence_current(evidence_identity) :=
  model-visible inputまたはterminal resultがrequired predicateへbind済み
  ∧ そのidentityの入力を変えるresultが未受領
```

このstateがtrueの間は同じevidence identityを`unobserved`へ戻さず、再取得しない。path-local instruction、changed content、失効後の再観測は別identityまたはinvalidated stateとして許可する。

### 2. start gate barrierは現行最適化から除外する

F10 monthlyのTaskSpecは、固定seed commit不存在または予期しないdriftなら「reviewを開始せず停止する」と明示する。review対象readは固定diff、changed file、`src/AGENTS.md`、`monthly_engine.py`である。

100件の発行群は次に分かれた。

| route | run数 | 判定 |
|---|---:|---|
| identity result受領後に全review対象readを発行 | 81 / 100 | start gateを先に消費 |
| identity確認と少なくとも一つのreview対象readを同じ発行群へ含める | 19 / 100 | 全件Score 4。現在のfixtureでは品質欠損なし |

固定fixtureはcleanでseed commitも存在し、19件は全て成果を正しく返してScore 4だった。drift時のstop機序は観測していないため、この19件から安全性の同値性は主張できない。一方、観測していないdrift便益を理由に追加制御を最適化として採用することもできない。

同じ100件の登録KPIをroute別に記述すると、共同発行した19件はtoken中央値75,070、elapsed中央値57.886秒、gateを先に消費した81件はtoken中央値93,801、elapsed中央値55.158秒だった。routeは無作為割当てではないため単独因果値にはしないが、少なくとも共同発行を禁止すると評価済み品質が改善する証拠はなく、tokenは増える方向にある。開始バリアがもたらせるのは未観測drift時の早期停止だけであり、現在のStandard14 oracleに対する結果改善ではない。よってH3は`not_evaluated_counterfactual / rejected_as_current_overquality`とし、Candidate候補から外す。

C147の`DECISION_BOUNDARY`は、drift時にread自体が禁止される場合はreadを別stepへ置く。物理primitiveとしての`read`をTaskSpec上の`review operation`へ所属させる追加関係は設計できるが、それが必要だとする失敗resultは今回のfixtureにない。

参考として、その機序を形式化するなら次の関係になるが、これは現在の追加候補ではない。

```text
operation_start_member(invocation, operation) :=
  invocation resultのconsumerがそのoperationのpredicateだけ
  ∧ TaskSpecがgate成立前にそのoperationを開始しないと明示
```

この関係がtrueなら、そのinvocationは物理primitiveがreadでもgate resultの`result_effect_scope`へ入る。得られるのはdrift時にreview専用readまで始めないという追加安全性であり、clean fixtureの成果品質改善ではない。

これはC19x系列のような全read逐次化とは異なるが、局所化しても便益未観測の追加制御である点は変わらない。別のoracleがdrift時早期停止をrequired outcomeとして固定し、その失敗を観測した場合にだけ再検討する。

## 既存制御からの低頻度逸脱

required-validation eventを読める685件では、全required groupが存在した。通常routeは強いが、0件ではなかった。

| route | 件数 | 現在判断 |
|---|---:|---|
| required group成立 | 685 / 685 | supported |
| required commandの再実行 | 1 / 685 | F02で`main_verify`を二度実行。最初のeventは`exit_code=0` |
| required commandを二つのmodel発行群へ分割 | 1 / 685 | 最初の成功resultを表示省略だけで証跡欠落と誤認した同じF02 run |
| 最初のvalidation発行後に別model発行群から完了evidenceを追加 | 22 / 685 | F02 3、F03 2、F04 9、F06 5、F07 canonical 3 |

validation後続発行あり・なしを同一case内で登録済みKPIへbindした。値は`token中央値 / elapsed中央値`である。

| case | reentryなし | reentryあり | ありrun数 |
|---|---:|---:|---:|
| F02 | 127,644.5 / 78.094秒 | 240,069 / 133.402秒 | 3 |
| F03 | 99,830 / 70.291秒 | 140,658 / 98.550秒 | 2 |
| F04 | 150,158 / 83.218秒 | 220,196 / 95.822秒 | 9 |
| F06 | 104,861 / 76.489秒 | 205,413 / 95.674秒 | 5 |
| F07 canonical | 101,603 / 62.492秒 | 162,637 / 92.306秒 | 3 |

5ケース全てで後続発行群のtokenとelapsedが高かった。routeは無作為割当てではなく、複雑なrunが後続発行も高costも生んだ可能性を除けないため単独因果値にはしない。全件合格を変えずにこの発行を減らせれば観測costは減るが、元rollout監査によりC147へ足せる新しい制御は特定できなかった。

[先行H2監査](c147-validation-control-overlap-causal-audit.md)の190件ではrequired command再実行0、wrapper分割1、post-required reentry 11だった。その監査は未読runへ外挿しないと明記していた。今回の広いevent監査により、「通常routeの二重実行0」という全体判断は撤回する。

22件の元rolloutを再監査すると、全22件で後から取得したdiff / status / source等をvalidation開始前に明示していた。内訳は、cell ID付きnonterminal resultを同じcellで待たず別`exec`へ進んだ11件、terminal outputですでに見えていたevidenceを再取得した10件、required commandと完了evidenceを別発行へ分割した1件である。

C147本文はすでに、完了判定evidenceを一つの実行票へbindすること、cell ID付きnonterminal resultでは同じcellへのwaitだけを発行すること、実行票terminal後は入力失効等がない限りtoolを追加しないことを定めている。したがって`validation_ticket_items`という集合関係を足しても新しい判断点は増えず、22件を生じた機序も変えない。H2aは不足relation仮説ではなく、既存制御への実行逸脱として閉じる。詳細と対象runは[validation二制御群の重複原因監査](c147-validation-control-overlap-causal-audit.md)を正とする。

F02の1件は別である。iteration 76、run `cebc391f0eb14005922d0e008bc95183`では、最初の`main_verify` eventが`exit_code=0`で、agent自身も326 pass・3 skipを認識していたが、長い表示の途中省略により「protocol必須のJSON exit証跡だけが返らない」と判断した。保存command auditは最初の実行をsuccessfulと認め、protocol violation 0だった。したがって外部command failureやenvironment recoveryではなく、result admissionの問題である。

ただし、この1件だけを見てC147全体の不足へ昇格しない。F02の保存rollout 100件を同じ条件で比較すると、focusedとfull gateを含むterminal wrapperでfull gateのpass summaryは見えるがfull command用JSON exit行が途中省略されたrunは60件あった。そのうち59件は同じrequired commandを再実行せず完了し、再実行したのはiteration 76だけだった。

| full command用JSON exit行が見えないroute | run数 | required command再実行 |
|---|---:|---:|
| 正常admission | 59 | 0 |
| false-unavailable判断 | 1 | 1 |
| 合計 | 60 | 1 |

59件の正常routeも、outer wrapperのterminal、`326 passed, 3 skipped`のsummary、およびfail-fast分岐を通過しなければ発行されない後続command resultから成功をadmitしていた。つまり、JSON行の表示省略は再実行の十分条件ではない。

登録済みKPIでは正常59件の中央値が125,612 token / 76.446秒、再実行runが229,719 token / 112.566秒で、差は+104,107 token / +36.120秒だった。この差にはrun全体の複雑さが混ざり、二度目の`main_verify`だけの因果値ではない。一方、再実行を含むrouteが無costともいえない。

追加候補があるとすれば、表示本文の完全性と、fail-fast制御フローからadmitできるterminal statusを分ける正の関係である。

```text
terminal_status_admitted := machine-bound terminal statusがbind済み
  ∨ terminal wrapper内で当該commandのnonzero停止分岐を通過し、後続resultとpass summaryがbind済み
display_payload_complete := predicateに必要な観測値が表示本文からbind済み
```

`terminal_status_admitted=true`かつpass conditionに必要なsummaryがbind済みなら、表示途中省略だけで同じrequired commandを`unavailable`へ戻さない。ただし59 / 60件はこの関係を追加しなくても正常admissionできている。always-on文言を足した場合のtoken増加に対し、Score 4のまま1件の再実行だけを防ぐ効果は現行の中央値KPIでは判定しにくい。この一件だけから文言を確定せず、H2bを`positive_relation_hypothesis / candidate_not_ready`に留める。

## KPIと不足判断の関係

case別中央値だけを高低順に見ても、必要制御は決まらない。固定command時間やtask規模が異なるためである。ただしroute監査の優先順位には使える。

| case | token中央値 | elapsed中央値 | 今回の残差 |
|---|---:|---:|---|
| F04 | 160,125.5 | 84.840秒 | validation後続発行9件、wrapper分割既知1件 |
| F06 | 105,044.5 | 77.552秒 | root再読6件、locator / probe、validation後続発行5件 |
| F10 inventory | 101,655.5 | 69.745秒 | authority resultを待つrouteと共同read routeの両方。直列性だけでは判定しない |
| F10 monthly | 93,601.5 | 55.994秒 | root再読99件、共同発行19件、location mismatch 6件。後二者は現行oracleでは修正対象外 |

F10 monthlyのtoken中央値はStandard14内で最大ではない。99%のroot再読は同じauthorityの再取得costとして削減候補になる一方、19%の共同発行は全件合格かつ低tokenであり、同じ「残差」として扱わない。

## 最適化仮説の再構成

| 仮説 | 足りない制御 | 対象route | 非対象route | 現在状態 |
|---|---|---|---|---|
| H1 revised | admitted evidenceのidentityと失効までのstate保持 | root再読130 / 1,385、F06 / F07のconsumerなしmetadata probe、ADR9 root再読111 / 450 | 未取得path-local instruction、target content、失効後の再観測 | `optimization_hypothesis / candidate_not_ready` |
| H2a closed | 追加制御なし。既存のone-ticket、wait-only、terminal後追加tool禁止を適用 | validation後続発行22 / 685 | 必要なdiff / status自体、terminal ticket内の発行 | `existing_control_deviation / candidate_not_justified` |
| H2b analyzed | fail-fast通過を含むterminal statusとdisplay payload完全性の分離 | false-unavailable rerun 1 / 685。同型表示省略60件中59件は正常 | 実際のnonterminal、nonzero、pass条件に必要な観測値欠落 | `positive_relation_hypothesis / candidate_not_ready` |
| H3 rejected | start gateの禁止operationと、その専用evidence invocationのmembership | F10 monthly共同発行19 / 100は全件Score 4、token中央値75,070 | gate先行81 / 100のtoken中央値93,801 | `not_evaluated_counterfactual / rejected_as_current_overquality` |
| H4 | producer三条項の読解cost | 具体的Standard14 costなし | owner metadataをworker要求へ昇格しない正常route | `not_evaluated` |

## 現在判断と次作業

1. H3は、現在のStandard14で結果改善がなく、tokenは増加方向（elapsedは約2.7秒短縮）にあるため最適化候補から外す。
2. H2aは22件の元rolloutまで追跡し、不足relation仮説を棄却する。既存制御の同義反復をCandidateへ足さない。
3. H1とH2bだけを、評価済み品質を維持したまま観測costを減らし得る別々の仮説として保持する。
4. H2bは同型正常route 59件まで比較した。再実行costはあるが、既存制御で59 / 60件が成立し、品質差もないため、追加文言のnet costと効果を判定できるgateが固定されるまでCandidateを作らない。
5. 現在残るH1とH2bのうち、H1は130 / 1,385件の反復routeを持ち、H2bは1 / 685件である。次の分析優先度はH1へ戻す。
6. 新Candidateを作る前に、変更軸がADR9の既知review品質失敗と混ざらず判定できるかを固定する。現行系列ではADR9を先に評価し、通過後だけStandard14へ進む。
7. 現時点ではprompt set、profile、preflightまたは評価slotを作らない。

## 参照

- [Candidate147 Standard14 N=100一次result](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [ControlFreeRepository / Candidate147 N=100比較](../evaluations/results/control-free-candidate147-v14-medium-standard14-atomic-n100-cli0146_2026-08-03.md)
- [Candidate147 Standard14 N=5](../evaluations/results/candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)
- [Candidate147 validation二制御群の重複原因監査](c147-validation-control-overlap-causal-audit.md)
- [Candidate147 F06 authority route原因監査](c147-f06-authority-route-causal-audit.md)
- [Candidate147 runtime固有表面形・意味拘束監査](c147-runtime-surface-portability-audit.md)
- [Candidate191 Standard14コスト機序再判定](candidate191-standard14-cost-mechanism-reassessment.md)
