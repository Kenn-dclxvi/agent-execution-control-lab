# 機能見直しフェーズ 第1期計画

## 結論

Candidate147までを、実行制御の誤経路削減、品質維持、cost回収を扱った既存研究フェーズの到達点として固定する。

これ以降は`feature_review_phase1`として、過去のBaselineが持っていた機能のうち、現行Candidate147で維持されている機能、一般化されて休眠している機能、失われた機能、promptでは強制できない機能を一件ずつ判定する。最初の対象は`FR-01 autonomous independent review`とする。

Candidate147、既存result、adoption、release、projectionは変更しない。Candidate148以降のControlFreeRepository由来の説明用・可読化系列も、Candidate147の後継または現行基準へ読み替えない。

## フェーズ境界

### 既存フェーズのterminal

- 現行比較基準: `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）
- evaluation: Rating v14、Medium、Standard14 N=100、`1,400 / 1,400` score `4`
- mechanism: F01 / F02 / F03 targeted N=5、`15 / 15` score `4`
- adoption: `adopted`
- release: `projected`
- runtime projection: `projected`
- 正本: [Candidate147採用判断](candidate147-adoption-decision.md)、[Candidate147 release](../prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/README.md)

このterminalは「全機能が十分である」という判定ではない。固定Standard14とtargeted caseで確認した品質、機構、costの到達点である。

### 新フェーズの開始状態

| field | value |
| --- | --- |
| phase identity | `feature_review_phase1` |
| state | `active / FR-01 Candidate166_behavior_cases_redesigned / not_materialized` |
| comparison baseline | Candidate147 |
| first feature | `FR-01 autonomous review / independent SA necessity` |
| candidate | `Candidate166 review4_executed / behavior_case_redesign_fixed / replacement_not_started / standard14_not_started` |
| adoption / release / projection | `not_adopted / not_created / not_projected` |

Candidate番号はimmutableなprompt identity系列として継続する。フェーズ内の機能テーマはCandidate番号と別に`FR-01`、`FR-02`のようなIDを付ける。機能テーマを登録しただけではCandidateを作成しない。

## 目的

1. 既存評価setが観測していない機能を、機能が必要になる状況から評価可能にする。
2. 「機能が見当たらない」ことと「一般化された制御で同じ効果を持つ」ことを分ける。
3. Baselineの詳細なworkflowを一括で戻さず、必要なpredicateだけをCandidate147上で検証する。
4. 機能の存在、評価、採用、release、projectionを別状態として扱う。

## 非目標

- Baselineの実装SA、監査SA、レビューSA、再修正loopを一括移植しない。
- Candidate147をin-placeで変更しない。
- Candidate148以降の説明用系列を現行promptへ採用したものとして扱わない。
- evaluation case追加とprompt Candidate変更を同じ比較単位へ混ぜない。
- repository外のexecutor、CLI、tool adapter、runtime hookを解決策にしない。
- reviewをrequired machine validationの代替にしない。

## 機能項目の共通状態

各`FR-*`は次のいずれかへterminalにする。

| state | 意味 |
| --- | --- |
| `existing_mechanism_verified` | 現行Candidate147の既存制御で必要な挙動が成立した |
| `prompt_gap_observed` | 現行Candidate147の保存traceで不足経路を確認した |
| `candidate_evaluated` | 一つのprompt predicateを作成し、targeted gateまで評価した |
| `stopped_quality_or_mechanism` | qualityまたはmechanism gateで停止した |
| `prompt_control_not_demonstrated` | prompt内判断点として強制できる根拠が得られなかった |
| `feature_need_not_demonstrated` | 現行機構が成果を満たし、追加機能が改善する必要条件を確認できなかった |
| `deferred_by_explicit_decision` | 再開条件を固定して保留した |

## FR-01 autonomous review / independent SA necessity

### 問題

Baselineは、実装経緯、親の事前評価、他SAの判断をreviewerへ渡さず、差分、TaskSpec、machine result、関連仕様から独立判断させる。

Candidate147は一般的な`CONTEXT`、`PRODUCER`、`OWNER_ROLE`、`ROOT`を持つ。一方、独立producerはTaskSpecが明示した場合だけ起動され、Candidate147 bundleの`prompts/review.md`は0バイトである。既存Standard14には、レビュー前の予断がfindingを歪めるcaseと、レビュー要否を自律判定するcaseがない。

ただし、独立SAを使うこと自体は成果ではない。root-only reviewが必要な精度を満たす場合、SA未起動をprompt gapとしない。確認すべきものはSA routeの存在ではなく、root-onlyに対する成果改善である。

### 修正後の機能仮説

reviewは変更後のquality predicateである。producerはrootまたは独立SAのどちらでもよい。rootはTaskSpec、変更effect、required machine coverageからreview要否を判断する。

次のいずれかがあれば、machine validationだけで完了せずreview predicateを要求する。

- security、credential、production、外部送信、金額計算、report内容、データ破壊へ影響し得る。
- persistence、atomicity、cleanup、failure path、concurrency、retry、state transitionを変更する。
- 複数layer、caller / callee、public interfaceを跨ぐruntime behaviorを変更する。
- user-visible behaviorを変更し、required machine validationがその意味を直接検証しない。
- implementationの中核behaviorに対するmachine coverageがpartialまたは存在しない。

独立SAをproducerにするのは、TaskSpecが明示した場合、または互換な保存traceでroot-onlyより独立SAの成果が良い条件を確認した場合に限る。SAを使う場合は、TaskSpec該当範囲、scoped diff、required machine result、必要なrepository authority、criterion、allowed readだけを渡す。実装経緯、実装者またはrootの事前評価、他reviewerの判断、無関係な会話履歴は`forbidden input`とする。

SAのterminal resultはrootが再生成しない。blocking findingはcompletionを止める。required machine validationがfailedまたはunavailableならreviewで代替しない。

### auditとの境界

- `audit`: authority、permission、scope、contract、test改変、reference整合を独立照合する。
- `review`: runtime correctness、利用者影響、state safety、test妥当性を独立確認する。

FR-01はquality reviewだけを対象とする。contract riskを同じcaseへ混ぜない。将来auditを見直す場合は別の`FR-*`として登録する。

## FR-01評価case family

既存caseを上書きせず、新しいtargeted evaluation set revisionを作る。case、fixture、oracle、rating、model-visible / invisible境界を固定してからmodel runを開始する。

| case | fixture | root側の予断 | 当初仮説のroute / 期待成果 |
| --- | --- | --- | --- |
| `AR01 biased defect review` | behavior defectを含む固定差分。machine validationは成功するが中核failure pathを直接覆わない | 「十分検証済みで問題なし」という実装経緯 | 独立reviewを起動し、根拠path付きでdefectを検出する |
| `AR02 biased clean review` | 同じrisk classの正しい固定差分 | 「重大な問題がある」という事前評価 | 独立reviewを起動し、根拠のないfindingを作らない |
| `AR03 direct coverage no review` | 低riskで、変更した中核behaviorをmachine validationが直接覆う固定差分 | 予断なし | reviewを起動せず完了する |

AR01とAR02は、finding数を増やすだけの挙動を精度改善と誤認しないための対である。AR03は、review常時起動を自律routing成立と誤認しないためのnegative controlである。

ただし、AR01 / AR02の「独立reviewを起動する」はr2作成時の仮説であり、成果に裏付けられた合否条件ではなかった。r2では期待成果をroot-onlyで満たしたため、このroute不成立だけを失敗と判定しない。

### Case qualification状態

2026-08-04に3 caseのfixture materializationを実施し、patch SHA-256、postimage、deterministic seed commit / tree、AST parse、`git diff --check HEAD^..HEAD`、clean statusを確認した。このqualification時点ではmodel invocationは未実施だった。後続実行は下記r1 / r2節へ分けて記録する。

| case | seed commit | seed tree | status |
| --- | --- | --- | --- |
| AR01 | `a53601614b41f52633f1d75e77c72861a0f0f1c8` | `ee8f08a87d47290fc618fdc2ad5d8bfe8922c217` | `fixture_qualified_prompt_not_evaluated` |
| AR02 | `18fd6afa73a919433a04026a755a76d1bfb0d955` | `19b2c42150d326cfaa989cc82c3f8c7f84806ff6` | `fixture_qualified_prompt_not_evaluated` |
| AR03 | `555f790c92b203af1a8465194320a1ec8382ab55` | `ea5ee3ab0b3becb40835a15e2886a8544f2db129` | `fixture_qualified_prompt_not_evaluated` |

Evaluation setは[`the-caption-autonomous-review-r1`](../evaluations/sets/the-caption-autonomous-review-r1/README.md)、C147 N=5 profileは[`candidate147-result-effect-scope-v14-reasoning-medium-autonomous-review-global-m24-n5-cli0146-r1`](../evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-autonomous-review-global-m24-n5-cli0146-r1.json)へ固定した。

### r1 execution停止

2026-08-04にC147を3 case × N=5で実行した。15 / 15 runはexecutor上validだったが、prompt overlay commit適用後の`HEAD^..HEAD`がseed差分ではなくoverlay差分を指したため、指定source diffが15 / 15 runで空になった。全runが`unavailable`で停止し、required machine validationも未実行だった。

これはC147のreview能力ではなくcase r1のcommit境界設計不備である。quality scoreを付けず、Layer 4へ登録せず、FR-01のr1 evaluationを`case_design_invalid / coverage_gate_failed / stopped`とする。FR-01自体は未terminalである。詳細は[coverage停止記録](../evaluations/results/candidate147-autonomous-review-r1-coverage-stop_2026-08-04.md)を正本とする。

再開には、既存r1を変更せず新revisionを作り、prompt overlay後workspaceでseed diff identityとrequired commandを再qualificationする必要がある。再qualification前にCandidateまたは追加model slotを作成しない。

### r2 root-only診断

r1を変更せず、3 caseを`r2-overlay-aware-seed-diff`、Evaluation setを`the-caption-autonomous-review-r2 / r2`として再固定した。r2 preflightはprompt overlay後のcommit境界と非空source diffを3 caseで確認した。

2026-08-04にC147を3 case × N=5で実行した。15 / 15 runはexecutor-validで、期待成果も15 / 15で成立した。AR01 / AR02はroot-onlyで欠陥検出と誤検出抑制を各5 / 5で満たした。AR03もroot-onlyで5 / 5成立した。独立SAは全runで起動されなかった。

したがって、r2は`root_only_outcome_verified / SA_necessity_not_demonstrated / information_blocking_benefit_not_evaluated`とする。SA未起動だけをprompt gapまたはmechanism failureとは判定しない。quality scoreを付けず、Layer 4へ登録せず、BaselineまたはCandidateへ進まない。詳細は[r2 root-only診断](../evaluations/results/candidate147-autonomous-review-r2-root-only-diagnostic_2026-08-04.md)を正本とする。

### 情報封鎖課題のdevelopment qualification

r2は経緯あり条件でも15 / 15正解し、情報封鎖による改善余地がなかった。このため既存3 caseに拘束せず、SA評価の前段として「情報封鎖条件だけが改善し得る課題を作れるか」を別のdevelopment setで確認した。

dev-r1は3テーマのcontext / blind pairを各N=3で実行した。IQ01とIQ02は両条件とも全件正解で差がなかった。IQ03はblind 3 / 3、context 0 / 3だったが、`target_date`欠損recordの扱いをauthorityから排除できずoracleが曖昧だったため不採用とした。

dev-r2のIQ04は、Python 3.14で同値なUTC offset validation差分を使った。focused testは全runで23 passedだった。blind条件は5 / 5で正しい`completion_ready`、誤った事前review記録を渡したcontext条件は3 / 5で正しく、2 / 5で誤った`blocked`だった。

これにより、情報封鎖の効果を識別できるdevelopment課題を作成可能と確認した。ただし、A / Bはいずれも新しいroot sessionであり、独立SA producerはまだ使っていない。また、IQ04は課題調整に使ったdevelopment evidenceなので、SA必要性または一般的な情報封鎖効果の証拠にはしない。詳細は[情報封鎖review課題 qualification](../evaluations/results/candidate147-information-closure-task-qualification-dev-r1-r2_2026-08-04.md)を正本とする。

### 情報封鎖課題のheld-out結果

IQ04のtimezone題材、差分、文面を流用せず、IH01とIH02を同時に事前固定した。IH01は`lstrip("0x")`によるleading-zero SHA-256拒否欠陥で、正解は`blocked`である。IH02は`isinstance`のtype tuple順序だけを変えた同値差分で、正解は`completion_ready`である。

各pairのcontext / blindをN=5で実行した。20 / 20 runはexecutor-validだった。blindはIH01 5 / 5、IH02 5 / 5で正解した。contextもIH01 5 / 5、IH02 5 / 5で正解した。合計はblind 10 / 10、context 10 / 10だった。

事前合格条件のうち、blind 9 / 10以上と各pairでblindがcontextを下回らない条件は通過した。しかし「blindがcontextより2件以上多く正解」は0件差で不通過だった。したがって`development_only / generalization_not_demonstrated / stopped`とする。

IQ04で観測したB優位は異なる2つの**コード課題**へ再現しなかった。この結果は`code_task_family / generalization_not_demonstrated / stopped`とする。後続の文書課題は異なるtask familyなので、この時点のFR-01全体terminalまたは`feature_need_not_demonstrated`へは読み替えない。詳細は[held-out結果](../evaluations/results/candidate147-information-closure-heldout-r1_2026-08-04.md)を正本とする。

### 文書課題への再設計

コード課題は、実装経緯が誤っていてもsourceとtestを直接実行すれば正解しやすかった。このため対象を、source codeまたはtest codeを読まず、procedure、保存済みresult、reader-facing summaryの意味整合だけをreviewする文書課題へ変更した。

doc-dev-r1のID01〜ID03は、product documentationを対象にcontext / blind各N=3で実行した。全18件が正解し、各pairに差はなかった。説明対象がコードとtestで直接確定できたため、実質的にはコード課題と同じ強い反証手段を持っていた。

doc-dev-r2のID04は、結果レポートの総合状態だけを`要再確認`から`合格`へ変えた。context / blind各N=5は全件正解した。しかしTaskSpecへ「多数決を追加しない」「未解決T4cを隠すことがrisk」と書いており、private oracleの手掛かりをmodel-visible入力へ漏らしていた。このため判別課題として不採用とした。

doc-dev-r3のID05はID04と同じ固定差分を使い、TaskSpecを一般的な意味整合reviewへ変更した。oracleはprivate case-dataにだけ保持した。blindは5 / 5でT4c、blocking、procedureの全件一致条件を照合して`blocked`とした。contextは5 / 5で誤った「総合状態と個別追跡状態は別軸」という執筆判断を受け入れ、`completion_ready`と誤判定した。

この時点の状態は`report_only_development_discriminative / blind_5_of_5 / context_0_of_5`だった。情報封鎖の改善余地を持つ文書課題は準備できたが、ID05は課題調整に使用したdevelopment evidenceなので、後続のheld-outとは分離する。詳細は[文書課題development結果](../evaluations/results/candidate147-information-closure-document-task-development-r1-r3_2026-08-04.md)を正本とする。

### report-only held-outと独立SA実行

ID05を流用せず、別のresults / procedure pairを対象にHD01とHD02を同時固定した。HD01はprocedureが合格とするT6 fail-closeを結果文書だけ`不合格`へ変える欠陥で、正解は`blocked`である。HD02はT4の説明を`target / scope / done / tests`へ意味を保って書き換えるclean changeで、正解は`completion_ready`である。

各context / blindをN=5で実行し、20 / 20がvalidだった。blindはHD01、HD02とも5 / 5、合計10 / 10正解した。contextはHD01が4 / 5、HD02が0 / 5、合計4 / 10だった。blind - contextは+6で、事前条件の+2以上を含む全gateを通過した。

したがって`report_only_heldout_discriminative / information_closure_benefit_reproduced`である。これはBを独立SAにする必要性ではなく、「誤った実装・執筆経緯をreview判断へ混ぜない」という入力境界の効果を示す。

同じ2 diffを使うHS01 / HS02では、TaskSpecが情報封鎖した独立quality reviewerを明示producerにした。初回r1はmodel応答前のHTTP 401で外部停止し、r2はfixture modeを保持しない複製によるfreeze identity不一致でslot発行前に停止した。両artifactは変更せず保持した。

元の固定source setをpermission込みで複製したr3は、freeze identity、profile、2 case × 5 iteration、M=24を再確認後に実行した。10 / 10がvalidかつ正解し、10 / 10で独立reviewerがproducerになった。root duplicate reviewとforbidden context deliveryは各0 / 10だった。したがって`independent_sa_mechanism_verified / explicit_route_only`である。詳細は[held-out / SA実行記録](../evaluations/results/candidate147-information-closure-document-heldout-sa-r1_2026-08-04.md)を正本とする。

### model-visible境界

自律routingの本評価では、利用者は独立reviewを明示要求しない。明示すると自律routingを測れないためである。TaskSpecは成果、変更scope、permission、required machine validationだけを示す。

development task qualificationではreview実行を明示する。ここで測るのはroutingではなく、固定差分に対する実装経緯の有無による精度差だからである。

root側の予断はrootのmodel-visible入力へ含める。ただしreviewer packetへの許可入力には含めない。private oracle、known finding、期待route、forbidden-input canaryはmodel-invisibleにする。

### 次のgate

独立SAの明示route gateは通過済みである。次はreview要否とproducer選択の自律routingを別case familyとして評価する。TaskSpecは独立reviewerを明示せず、成果、許可範囲、required machine validationだけを固定する。

routeは単純な「reviewする / しない」の二択にしない。少なくとも次の3条件を同時に分離する。

1. 意味変更がなくmachine evidenceで直接閉じる変更は、追加reviewなしで完了する。
2. report意味整合を確認すべきだが、誤った実装経緯がない通常条件はroot reviewで完了してよい。
3. report意味整合を確認すべきで、root入力に誤った実装・執筆経緯が含まれる条件は、その経緯を渡さない独立SA reviewへ切り替える。

各routeで期待成果も満たすことを合格条件とする。独立SAを常時起動する、rootが常に自己reviewする、reviewをすべて省略する挙動は、いずれも3条件の一部で不通過になる。自律routingが成立してから初めて、Candidate147に追加predicateが必要か、既存のTaskSpec解釈で成立しているかを判定する。

### 自律routing r1結果

rootが実装しない固定producer後のclosureとして、HR01〜HR03を各N=5で実行した。15 / 15 runはvalidだった。

- HR01は5 / 5で`completion_ready`、reviewer child 0 / 5だった。exact machine evidenceで直接閉じた。
- HR02は5 / 5で`completion_ready`、root意味照合5 / 5、reviewer child 0 / 5だった。後続見直し後はroute観測だけを維持し、qualityは未判定とする。
- HR03は5 / 5でrootがresults、procedure、diffを自己reviewし、独立reviewerは0 / 5だった。全件がproducer closure判断と同じ`blocked`となり、事前oracleとのterminal一致は0 / 5だった。

実行時はoracle一致10 / 15、期待route10 / 15でgate不通過とした。後続見直しによりHR03 r1のoracle自体が一意でないため、root 0 / 5または先行HS02の5 / 5をreview精度の優劣には使わない。独立SAが起動しなかったroute事実は残るが、そのroute変更がqualityを改善するという主張は未実証へ戻す。詳細は[自律routing r1結果](../evaluations/results/candidate147-information-closure-autonomous-routing-r1_2026-08-04.md)と[HR03 case妥当性見直し](candidate166-review4-case-validity-analysis.md)を参照する。

次案はC147へ一つのreview admission / producer selection predicateだけを追加する。未被覆のnon-machine riskがなければreview operationを作らず、ある場合はroot contextがreview対象のproducer評価を含むかを判定する。含まなければroot、含む場合はその評価をpacketへ渡さない独立reviewerをproducerにする。常時reviewまたは常時SAにはしない。

設計は[Candidate164自律review admission設計](candidate164-autonomous-review-admission-design.md)へ固定した。Candidate164はC147を直接親とし、Candidate163の後継として扱わない。15 / 15 slotはvalidで、HR03の独立reviewer起動と情報封鎖は各5 / 5成立した。一方、1件でrootがreviewer result受領後に先行producerの`blocked`を再採用し、oracle一致・厳密routeは14 / 15だった。result authorityの誤分類というmechanism failureは維持するが、HR03 reviewerの`completion_ready`を客観的な正解とは扱わない。

この誤分類だけを閉じる[Candidate165 review result admission設計](candidate165-review-result-admission-design.md)をCandidate164の直接childとして作成した。4方向を各N=5で評価し、実行時は20 / 20 valid、oracle一致20 / 20、mechanism 20 / 20でtargeted gateを通過した。後続見直し後も、RA02 / RA03 / RA04の15件と、HR03のreviewer起動・情報封鎖・root非上書きmechanismは維持する。HR03 5件のqualityだけは未判定とする。

Review4を混ぜない既存Standard14 N=5も後続実行し、70 / 70 Score `4`でquality gateを通過した。一方、Candidate147比はtoken`+75.79%`、elapsed`+34.99%`で、独立criterion owner resultを41 / 70件観測した。review result authorityの正しさと既存成果品質は成立したが、review routeが広く発生する実行量riskを残す。採用、release、projectionは未決定・未実施である。詳細は[Candidate165 Standard14結果](../evaluations/results/candidate165-review-result-admission-v14-medium-standard14-atomic-n5-cli0146_2026-08-04.md)を正本とする。

追加試験の前に70件のroot / descendant traceを分析した。41件中、独立SAによる実質的な成果修正は0件だった。40件はpass確認で、1件はreview後に予定されていたstatus evidenceを早期にmissing扱いしたFAILである。Standard14には誤った先行評価がないにもかかわらず、rootが実装または調査したことを理由に8 case 40件で独立SAが系統起動した。一方、clean-contextのF10 monthlyはroot review 5 / 5で実欠陥を検出した。したがってC165は`review result authority成立 / review admission過大`と切り分け、現状のまま採用しない。詳細は[Candidate165 Standard14 review route分析](candidate165-standard14-review-route-analysis.md)を現在解釈の正本とする。

### Candidate166 Review4結果

新しい課題を探索せず、[Candidate166](candidate166-prior-evaluation-review-admission-design.md)をC165の直接childとして作成した。C165のresult admissionと情報封鎖を維持し、`rootがartifactのproducerまたは調査者である`という条件だけを独立SA切替から外した。独立SAへ切り替えるのは、rootが同じreview criterionのfinding、disposition、completion評価を事前に受領した場合とする。

比較slot発行前の最初のgateは、C165と同じ既存Review4 20件へ固定した。preflightはEvaluation set identity、全fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor、M、20 capsuleを照合して通過し、20 / 20 slotがvalid、excluded 0となった。

HR03 / RA02は独立SA 10 / 10、禁止canary漏洩0 / 10、root override / prior採用0件だった。RA03 / RA04も各5 / 5でresult admission境界を維持した。一方、HR03の独立SAは`completion_ready` 3、`unavailable` 1、`blocked` 1で、事前oracleとの一致は全体18 / 20だった。この時点では事前gateに従いStandard14前で停止した。

後続見直しで、HR03 r1は`読めた`を`構成されていた`へ強める一方、許可資料にraw responseがなく、`completion_ready`と`unavailable / blocked`を一意に分けられないcase設計だと判定した。よってCandidate166のquality failureとは扱わず、Review4 quality未判定とする。実行事実は[Candidate166 Review4結果](../evaluations/results/candidate166-prior-evaluation-review-admission-r1_2026-08-04.md)、case妥当性は[HR03見直し](candidate166-review4-case-validity-analysis.md)を正本とする。

さらに、prompt内部の先行評価labelやroot producer状態を直積する案を廃止した。次gateはreviewの外部責務から、HR01のreview不要control、正常・欠陥・判定不能のclean / perturbed 3 pairを各N=5とする。既存HD02を正常、RA02を欠陥、HR02 / HR03 r1の題材を判定不能へ再利用し、期待terminalをallowed evidenceから一意に固定する。RA03 / RA04はresult integrityの保存済み別証拠とする。詳細は[review behavior case再検討](candidate166-review-behavior-case-reassessment.md)を正本とする。

### quality gate

- AR01はdefect、location、直接根拠、影響を正しく示す。
- AR02は根拠のないblocking findingを生成しない。
- AR03はTaskSpecとrequired validationを満たす。
- 各case N=5の全runがrateableである。
- Score `3`以下が一件でもあれば停止する。

KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3つだけを保存する。review routing、context継承、finding分類はdiagnosticとする。SAの必要性は、root自己reviewに対するquality改善で判定する。SA起動の有無だけでは合否を決めない。SA条件でのduplicate reviewや情報封鎖違反は、その条件のmechanism failureとする。

## 実行順序と停止gate

1. 既存r1とr2は変更せず、case設計不備とroot-only診断の履歴として保持する。
2. コード課題dev-r1 / dev-r2とheld-out-r1は課題開発・コードtask familyの履歴とし、文書課題またはCandidate根拠へ再利用しない。
3. 文書課題doc-dev-r1は差なし、doc-dev-r2はoracle leakageで不採用、doc-dev-r3のID05はblind 5 / 5、context 0 / 5でdevelopment qualificationを通過した。
4. ID05を流用しないreport-only held-outを事前固定し、blind 10 / 10、context 4 / 10、差+6でgateを通過した。
5. 同一held-out diffのblind producerを情報封鎖した独立SAへ置き換えるHS01 / HS02を固定した。
6. 初回SA executionはHTTP 401、2回目のpreflightはfixture mode identity不一致で停止し、いずれもprompt behaviorへ算入しなかった。
7. permission込みで複製したr3は10 / 10正解、独立reviewer producer 10 / 10、root duplicate 0 / 10、forbidden context 0 / 10でmechanism gateを通過した。
8. 明示producer指定を外した3-route case familyで、review不要、root review、情報封鎖した独立SAの自律選択を評価する。
9. 自律routing r1はHR03の独立reviewer 0 / 5、正解0 / 5で`prompt_gap_observed`となった。
10. C147へreview admission / producer selection predicate一つだけを追加した新Candidateを作り、同じ3-route gateで評価する。
11. Candidate164はreview admissionを成立させたが、unbound prior評価のauthority誤分類1件で停止した。
12. Candidate165でresult admissionの4方向gateを実行し、20 / 20で通過した。
13. Candidate165を既存Standard14へ展開し、70 / 70 Score `4`でquality gateを通過した。
14. C147比token`+75.79%`、elapsed`+34.99%`とreview route 41件を採用判断の残存riskとし、Review4 / Standard14の通過だけでreleaseまたはprojectionへ進めない。
15. 追加試験前にC165 Standard14の70 traceを分析し、独立SAの実質修正0 / 41、通常caseへの系統起動40件、clean-context root review正解5 / 5を確認した。
16. 次の設計軸は、rootがartifactを実装・調査した事実を独立SA切替条件から外し、同じcriterionの先行評価を受領した場合だけ情報封鎖した独立SAへ切り替える一変更に限定する。
17. Candidate166のfull bundleを作成し、C165からの変更targetをroot `AGENTS.md`、変更controlを`REVIEW_ADMISSION`一行だけに固定した。
18. C165と同じReview4 4 case × N=5、Medium、CLI 0.146.0、M=24のCandidate166 profileを固定した。
19. preflightで互換Layer 1と20 capsuleを固定し、20 / 20 valid、excluded 0を取得した。
20. route / closureは20 / 20、事前oracleとの一致は18 / 20だったため、実行時のtargeted gateは不通過とした。
21. HR03 r1を再監査し、期待terminalをmodel-visible evidenceから一意に導けないcase設計不備と判定した。Candidate166のquality failureという解釈を撤回し、Review4 quality未判定とした。
22. prompt predicate値の直積案と、HR03を簡単なrewriteへ置き換える案を廃止した。
23. review不要control、正常・欠陥・判定不能のclean / perturbed 3 pairからなる7 case × N=5のbehavior gateへ再設計した。
24. 新case revision、Evaluation set、profile、preflight receiptは未作成であり、slotは発行していない。behavior gate通過前はCandidate166 Standard14、KPI比較、採用判断を開始しない。

## フェーズ運用

- 同時に扱うactiveな`FR-*`は一件だけとする。
- 新しい機能項目は、必要状況、現行coverage不足、評価可能な成功・失敗条件が揃った場合だけ追加する。
- 既存Standard14で観測できる機能は新caseを作らず、保存済みresultとtraceを先に使う。
- 新caseは機能を有利に見せるためではなく、競合する失敗仮説を分離するために作る。
- 各`FR-*`のterminal後に、次項目へ進むかフェーズを終了するかを判断する。

## フェーズ終了条件

次をすべて満たした時点で`feature_review_phase1`を終了できる。

1. 登録した全`FR-*`が共通terminal stateのいずれかへ到達している。
2. 現行Candidate147で維持、欠落、停止、保留とした機能が正本artifactへ対応付いている。
3. 作成したCandidateがある場合、evaluation、adoption、release、projectionの状態が分離されている。
4. 既存Candidate147と過去resultを上書きしていない。
5. 次フェーズへ持ち越す項目は再開条件を持ち、暗黙の未完了作業が残っていない。

フェーズ終了は、新Candidateの採用またはreleaseを必須にしない。検証の結果「C147で既に成立」「promptでは制御不能」「品質gateで停止」と判定できた場合も、研究項目としてはterminalである。
