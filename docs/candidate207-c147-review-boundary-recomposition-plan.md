# Candidate207 C147 review境界再構成・検証計画

## 結論

Candidate207はCandidate206の短縮版にはしない。Candidate147を直接基盤とし、C147の13制御群、その意図的な重複、相互制限および`DECISION_BOUNDARY`の正の共同発行を保持したうえで、保存結果で必要性または作用が確認できたreview固有境界だけを既存制御群へ接続する。

C206の`DESIGN_ADMISSION`が持つ設計台帳の構築、全境界の分類、review operation準備、packet配送、判定順、revision loopは継承しない。これらはC147に不足した境界そのものではなく、既存のproducer、context、evidence、terminal、result effectおよび変更許可をもう一つのlifecycleとして手順化した記載だからである。

C206固有の`admitted_evidence_current`もC207の初回軸へ入れない。同一evidence再取得を減らす作用は観測されたが、C147比の3 KPIで費用対効果を通過しておらず、review再構成と混ぜると何が品質とcostを変えたか分離できない。

現在状態は`steps_1_to_6_complete / ADR9_quality_passed / ADR9_mechanism_failed / stopped`とする。実施順1〜3の処分表、入力所有権、九ケース状態表およびC207本文案は[`candidate207-c147-review-boundary-recomposition-draft.md`](candidate207-c147-review-boundary-recomposition-draft.md)、実施順4は[`candidate207-c147-review-boundary-recomposition-direction-review.md`](candidate207-c147-review-boundary-recomposition-direction-review.md)、実施順5〜6と停止判断は[ADR9結果](../evaluations/results/candidate207-c147-review-boundary-recomposition-adr9-r2-n5_2026-08-13.md)を正とする。

## 1. 固定する設計目的

C207が解くのは次の一件である。

> C147の通常実行制御を変えず、model-visibleなTaskSpecとrepository authorityが開いた設計境界にだけ、独立review resultをartifact変更前の追加dependencyとして要求する。

この目的に含めないものは次のとおりである。

- C147の制御群の統合、削除または一般的な整理
- review以外のexecution control最適化
- 同一repository evidenceの再取得抑止
- C191以後のoperation分離、発行遷移または別Candidateの抽象gateの継承
- 新しいケース、oracle、rating contractまたは評価条件
- TPOその他の別系列

## 2. C206差分の取捨選択

C147からC206へ追加された全文を、Candidate作成前に次の四分類へ固定する。保存結果がない「良さそうな圧縮」は採用理由にしない。

| C147に対する追加 | C207での扱い | 理由 |
| --- | --- | --- |
| 明示された独立producerだけをoperation identityへ一意にbindする肯定条件 | `PRODUCER / OWNER_ROLE`の局所強化として残す | owner語列の誤昇格を防ぐ既存境界を、review用の肯定条件まで閉じる |
| model-visibleなboundary recordからreview要否を決める条件 | review固有の新境界として残す | C147 ADR9で不足し、後続保存結果で品質便益が確認された |
| semantic projection、forbidden input、root非補完 | `CONTEXT / ROOT`へreview固有値だけを接続する | packet作成手順ではなく入力・権限境界として必要 |
| `counterexample_found / no_counterexample_found / unavailable`の異なる証明条件 | review result certificateとして残す | 一つのwitnessと全scope成功を同じ完全性条件へ入れないために必要 |
| admissible review resultだけがartifact変更を開く条件 | 既存`implementation_bound`への追加dependencyとして残す | reviewを別の変更lifecycleにせず、既存変更許可へ効果を渡す |
| review対象台帳を構築し、全件を三値分類する記載 | 除外 | ADR9のtrial inputはboundary ledgerとreview contractをmodel-visible入力として固定済み。prompt内で再構築する必要がない |
| operation準備、manifest作成、packet配送を順番に行う記載 | 除外 | `PRODUCER / CONTEXT / OWNER_ROLE`が所有する境界を手順として重複する |
| 「先に投影反例、その後だけdirect read」とする判定順 | 境界へ変換 | 文中順序では発行資格を閉じられず、保存traceで先読みが発生した |
| revision identityを作り、台帳とreviewを再実行するloop | 除外 | C147のinvalidationとresult effectを越えてreview固有workflowを作る |
| `admitted_evidence_current` | 初回C207から除外 | 作用は成立したがC147比のoptimizationは不通過。別軸でしか再検討しない |

各追加文は、最終的に`既存C147制御で成立済み / C147制御の局所強化 / review固有の新境界 / 除外`のいずれか一つへbindする。分類不能な文が残る間はCandidateを作らない。

## 3. C207の予定構造

新しい巨大なreview lifecycleは作らない。review適用結果とreview result certificateだけをreview固有のまとまりとして定義し、その値をC147の既存群が消費する。

### 3.1 review適用境界

判定対象は、ADR9のTaskSpecから直接model-visibleになっている`boundary_ledger`、authority、required validation coverage、consumer contractおよびreview contractに限る。promptが新しい台帳を探索・構築してはならない。

予定する判定は次の三値である。

- `required`: 提供済みboundary recordについて、設計がそのboundaryへ依存し、closure sourceがautonomous explorationで、authorityによる直接closureがなく、required validationが非網羅で、反例がvalidationを通過し得て、その反例が設計変更を要求する。
- `not_required`: 提供済みの設計依存境界が、authorityの単一対象または有限列挙と全関係検証で直接閉じている。
- `unavailable`: `required`または`not_required`の現在値を決めるためにTaskSpecが要求したmodel-visible値が欠けるか、非値である。

これは境界値の判定であり、「台帳を作る」「全境界を分類してから次へ進む」という新しい実行手順にはしない。permission否定は既存のpermission境界でreview operation作成前に停止する。

### 3.2 既存制御群への接続

| C147制御群 | C207が渡すreview固有値 | 保持する意味 |
| --- | --- | --- |
| `PRODUCER / OWNER_ROLE` | TaskSpecが明示したreview task identity | owner metadataからproducerを推測せず、独立reviewが必要な場合だけ一producerへbindする |
| `CONTEXT / ROOT` | semantic projection、allowed scope、forbidden input | rootの予想反例、履歴、実装案を渡さず、rootがreview結果を補完しない |
| `EVIDENCE_GATE` | unresolvedなresult kindを変えられるobservation consumer | direct readは「文中で後に書かれたから」ではなく、投影済み証明で未解決かつ当該readが判定を変えられる場合だけ開く |
| `TERMINAL / ROOT` | bind済みproducerの真正なreview certificate | 起動、途中result、root再構成をterminal resultにしない |
| `DECISION_BOUNDARY` | 受領review resultが変え得る未発行operation class | review責務の分離をmodel-step分割へ変換せず、相互非依存invocationの共同発行を維持する |
| `implementation_bound` | admissible review result dependency | `no_counterexample_found`だけが変更を開き、`counterexample_found`は変更を止め、`unavailable`は許可を作らない |

### 3.3 review result certificate

- `counterexample_found`: 固定された対象boundaryと同一処理条件にbindできる有効な一つの反例witnessでterminalにできる。別scopeの欠落は成立済みwitnessを失効させない。
- `no_counterexample_found`: 固定された全review scopeについて、bind済みproducerのsuccess receiptが揃った場合だけterminalにできる。
- `unavailable`: 現在未解決のresult kindを決めるため必須のnamed dependencyが欠ける、読めない、または値を返さない場合だけ成立する。

この三種類の必要evidence集合を共有のmanifest完全性へまとめない。

## 4. Candidate作成前の静的ゲート

次の四つを通過してからC207 bundleを作る。

1. **文単位の差分処分表**
   C147→C206の全追加文が第2節の分類へ入り、継承・変換・除外の理由と保存証拠を持つ。
2. **入力所有権表**
   各predicate引数を`TaskSpec supplied / repository authority supplied / reviewer observed / root projection forbidden`へ分ける。rootが投影できない値をdispatch前提にしない。
3. **九ケース状態表**
   ADR01、ADR02はreviewなし、ADR03〜ADR07とADR09は独立review一件、ADR08はpermission否定でreviewなしになることを、private oracleではなくmodel-visible入力だけで導出する。
4. **正常経路・共同発行反証**
   C147 Standard14の正常trace、C173の低頻度失敗、C175の成立traceと先読みtrace、C191の逐次化反例へ予定構造を当てる。review非適用時の追加判断はreview applicability一件だけで、既存のready setを分割しない。

固定文字数を静的gateにはしない。必要な境界量は、C147の既存制御では閉じられない保存済み誤経路と、その誤経路を閉じる最小のpredicate / permission / consumer / result effect / result admissionから決める。各追加文には、消す判断点または誤経路、接続先のC147制御群および非対象経路へ増やさない判断点を対応づける。対応を持たない文は、短くても追加しない。

C147、C206およびC207の文字数、bytes、条項数、定義数は、実装後の構造差を説明する診断値として記録する。本文が短いこと自体を合格条件にせず、実際の常時負担は互換するStandard14の`total_tokens`と`elapsed_seconds`で判定する。

## 5. 実装計画

静的ゲート通過後にだけ、次を一つのCandidateアーティファクト単位として行う。

1. C147のbundleを直接複製し、新しいprompt identityを与える。
2. root `AGENTS.md`だけへ、承認済みの局所強化とreview固有境界を反映する。
3. `CLAUDE.md`のlink構造をC147と同じに保つ。
4. root以外のtarget file、ケース、set、rating contract、fixtureおよびoracleがC147/固定評価条件から変わっていないことを機械確認する。
5. 専用構造test、bundle verification、identity snapshot、全test suite、`git diff --check`を実行する。

ここまで通っても状態は`static_verification_passed / not_evaluated`であり、採用またはreleaseとはしない。

## 6. 評価計画と停止条件

比較基準はC147に固定する。C173、C175、C191〜C206は失敗機序を反証する診断証拠であり、親またはKPI比較基準にしない。新規baseline runは発行せず、互換するC147の保存済みatomic runを使う。

全段階で、発行前にprompt identity以外の互換条件を一意にbindしたpreflight receiptを保存する。Layer 1、set revision、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、token accountingおよび`max_workers=24`のいずれかが一致しなければ、一件も発行しない。atomic run registryから不足分だけを固定し、validな低品質runを再実行しない。

KPI比較単位もresult確認前に固定する。C147とC207で同じcase・iterationを選び、登録済み比較経路が出す全case集約中央値を正式gateにする。case別paired delta、model step、tool call、reviewer routingおよび再読件数は、集約値の原因を判定する診断値に限定する。`total_tokens`と`elapsed_seconds`の許容増加はともに0とし、結果確認後に許容幅またはKPIの重みを追加しない。

### M5-A: ADR9 r2 N=5 qualification

- 9ケース×5回、合計45 atomic run。
- quality gate: 45 / 45 validかつ45 / 45 Score 4。
- applicability/cardinality gate: ADR01、ADR02、ADR08はreviewer 0、ADR03〜ADR07、ADR09は各runでreviewer 1。
- mechanism gate: forbidden canary 0、root補完0、permission否定後review 0、投影済みcertificateで閉じる場合の不要direct read 0、必須observation欠落時の誤completion 0。
- C147の共同発行を分割したtrace、consumerのないread、またはresult kindを越えたmanifest完全性要求が一件でもあれば停止する。

一件でもgateを外れたら`quality_failed`または`mechanism_failed`として保存し、repair rerun、Standard14、N=20延長を行わない。

### M5-B: Standard14 N=5 cost qualification

ADR9 N=5を全gateで通過した場合だけ、Standard14 14ケース×5回、合計70 atomic runを実施する。

- quality gate: 70 / 70 validかつ70 / 70 Score 4。
- mechanism gate: reviewer起動0、owner metadataのproducer昇格0、C147の共同発行・evidence・validation closureの退行0。
- KPI gate: 互換するC147 N=5に対し、`total_tokens`と`elapsed_seconds`のどちらも悪化しないことを要求する。

Standard14はC147がすでに全件合格しているため、品質が同じまま一方のcost KPIだけでも悪化する場合、その増分をreview品質の便益で正当化しない。一方が改善し他方が悪化する場合も、KPIの重みを後付けせず`cost_tradeoff_unresolved`で停止する。

### M6: 累積N=20 stability

ADR9 N=5とStandard14 N=5の両方が通過した場合だけ延長する。

1. ADR9 r2を全9ケースについて累積N=20へ延長する。N=5を再利用し、不足135件だけを発行する。
2. ADR9累積N=20がquality・cardinality・mechanism gateを通過した後、Standard14を全14ケースについて累積N=20へ延長する。N=5を再利用し、不足210件だけを発行する。
3. Standard14累積N=20でもC147の互換N=20 selectionに対して、両cost KPIの非悪化を要求する。互換するC147 N=20が保存済みrunから組めない場合は、C147を習慣的に再実行せず、比較不能として停止して別途判断する。

N=20はN=5の不通過を上書きするために使わない。N=5で成立した停止条件を、標本追加で再解釈しない。

## 7. 最終判断

C207を採用候補にできるのは、次がすべて成立した場合だけである。

- C147直接基盤と承認済み差分が証明されている。
- ADR9 N=20でquality、review cardinality、result admission、direct-read consumerおよびterminal機序が通過している。
- Standard14 N=20でC147の正常経路を維持し、reviewerを起動していない。
- Standard14の`total_tokens`と`elapsed_seconds`が、互換するC147に対して悪化していない。
- C206から除外した手順制御を、実装後の説明で暗黙に前提としていない。

この条件を通過しても、評価結果、採用判断、releaseおよびprojectionは別stateとして扱う。C207の検証完了だけで本体反映しない。

## 8. 実施順

1. **完了**: C147→C206全追加文の処分表を完成する。
2. **完了**: review predicateの入力所有権表とADR9九ケース状態表を作る。
3. **完了**: C147の既存制御群との接続だけでC207本文案を作り、各追加文の誤経路対応、消す判断点および手順化禁止を監査する。
4. **完了**: 保存traceによる事前反証を行う。初回本文案のdirect-read eligibility反例を修正後、blocking counterexample 0件。
5. **完了**: C207 bundleを実装し、静的検証する。
6. **完了**: ADR9 N=5をpreflight後に実施する。45 / 45 Score 4だが、packet反例成立後のdirect readが12 / 20で機序gate不通過。
7. **停止条件により未実施**: Standard14 N=5。
8. **停止条件により未実施**: ADR9 N=20およびStandard14 N=20。
9. **完了**: 品質と機序を分けて記録し、採用、releaseおよびprojectionを未判断・未実施として保持する。

## 関連一次記録

- [Candidate206 review制御コスト・記述構造分析](candidate206-review-control-cost-representation-analysis.md)
- [C147制御群の重複・最適性監査](c147-control-group-overlap-optimality-audit.md)
- [C147 functional decomposition再分析](c147-functional-decomposition-reanalysis.md)
- [ADR9 r2 set](../evaluations/sets/the-caption-preimplementation-adversarial-design-review-r2/README.md)
- [Standard14 set](../evaluations/sets/the-caption-standard14-r1/README.md)
- [prompt制御設計原則](prompt-control-design-principles.md)
