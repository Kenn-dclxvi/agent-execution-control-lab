# Candidate147 runtime固有表面形・意味拘束監査

> [!IMPORTANT]
> **状態**: `superseded_as_prompt_only_optimality_judgment / runtime_surface_inventory_completed / semantic_roles_separated / machine_observation_points_separated / standard14_route_bound / H3_rejected_as_current_overquality`
>
> 本監査の表面形inventoryは保持する。最適化判断はStandard14の実行resultとKPIへbindし、現行品質を改善せずtokenを増やす機序を追加しない。現在判断は[Standard14結果起点の制御不足・過剰品質境界監査](c147-standard14-control-insufficiency-audit.md)を正本とする。

## 結論

Candidate147のruntime固有表面形は、一種類ではない。少なくとも次の四種類へ分かれる。

1. `root / worker / session`はproducerとcoordinatorを区別する役割名である。
2. `runtime_spawn_result.task_name / FINAL_ANSWER.Sender / cell ID`はproducer来歴またはnonterminal invocationの継続先を照合する機械観測点である。
3. `model step / custom exec wrapper / exec_command / custom tool call / wait / commentary`は、resultを次の判断へ消費する前にどこまで発行し、nonterminal中に何を挟まないかを指定する配送・発行境界である。
4. `fork_turns=none / environment_recovery_max`は、現在のruntimeが提供する設定値または設定名である。

このうち、名称を一般語へ置き換えてもよい可能性が残るのは第4分類である。ただし、現時点では名称が原因の失敗、追加step、追加toolまたは品質低下を保存traceへbindできない。第1〜第3分類は、少なくとも現在のruntimeではC147の意味を観測可能な動作へ落とす接点である。抽象概念だけを残して実際の観測点を消す置換は、同値なportable化ではない。

この分類だけからH3のCandidate可否は決めない。後続のStandard14 route監査では、F10 monthlyでstart gateと少なくとも一つのreview対象readを同じ発行群へ入れたrunが19 / 100件、root C147本文をtoolで再取得したrunが99 / 100件あった。前者は全件Score 4で共同発行群のtoken中央値も低いため、追加barrierは過剰品質として除外する。後者だけが同じauthorityの再取得costとして最適化候補になる。

## 判定基準

表面形のportable置換には、文章上の意味類似だけでなく、次の四条件を全て要求する。

1. 変更対象を一つの制御群と一つの表面分類へ固定できる。
2. その表面形が現在閉じている正の遷移、禁止、result admissionまたはterminal条件を列挙できる。
3. 置換後も同じruntime上で結果から成立を判定できる代替観測点がある。
4. 保存traceへbindできる現行costまたは誤経路があり、その削減を品質・機序と分けて判定できる。

「別runtimeで読みにくい」「製品固有に見える」「より抽象的に書ける」だけでは、C147の観測可能な制御を削る根拠にしない。

## 条項別の表面形と意味

| 条項 | runtime固有に見える表面形 | 同じ条項内で拘束している意味 | 表面分類 | 現在判断 |
|---|---|---|---|---|
| `PRODUCER` | `root / worker` | operationごとのproducer一意性と、producerでないcoordinatorの区別 | 役割名 | `change_not_justified`。名称だけを消すと`ROOT`との権限境界を指す対象がなくなる |
| `TERMINAL` | `worker / session / final response` | producerまたはinvocationがnonterminal、あるいはresult欠落ならoperationもnonterminalとし、文章による補完を認めない | 役割名と出力境界 | `change_not_justified` |
| `CONTEXT` | `worker packet / fork_turns=none` | producer inputの固定と、packetだけで判定可能な場合の履歴非継承 | 役割名と設定値 | packet意味は保持必須。設定名だけの置換効果は`not_evaluated` |
| `OWNER_ROLE` | `worker / runtime_spawn_result.task_name / FINAL_ANSWER.Sender / wait / root` | 明示producerの起動、起動identityとterminal result送信identityの一致、同期結果とprovenanceの分離、異producerやcoordinatorによる補完禁止 | 役割名、機械field、同期primitive | `change_not_justified`。fieldを消すなら同じidentity照合を行う代替観測点が必要 |
| `ROOT` | `root` | producerでないcoordinatorがpacket構築、result binding、terminal集約だけを行う権限制限 | 役割名 | `change_not_justified` |
| `DECISION_BOUNDARY` | `model step` | 相互非依存invocationを、いずれかのresultを次判断へ消費する前に発行対象へcommitする | 発行境界 | `supported`。名称は置換可能でも、このイベント順を弱めてはならない |
| `VALIDATION_CLOSURE` | `root / custom exec wrapper / exec_command / custom tool call / model step` | required validationの個別発行、fail-fast、全result収集およびmodel再入前closure | 役割名と発行境界 | `supported / intentional_specialization` |
| `VALIDATION_PLAN` | `modelへ戻らず / validation wrapper / cell ID / wait / commentary / 別tool` | 実行票の途中resultを外側判断へ返さず、nonterminal invocationを同一identityで継続し、別の発行を挟まない | 発行境界、継続identity、message境界 | `supported` |
| `RECOVERY` | `environment_recovery_max` | environment-only repairと同じrequired command rerunの組だけが回復許容量を消費する | 設定名 | 回数制御の意味は保持必須。変数名のportable置換効果は`not_evaluated` |

`SPEC / EVIDENCE_GATE / INDEPENDENCE / METHOD`にはこの分類の明示的runtime fieldやtransport名はない。これらまでportable化の名目で再編成すると、H3の一軸変更ではなく13条項の責任再構成になる。

## 同じ語でも役割が異なる箇所

表面語の一致だけで重複とは判定しない。

- `wait`は`OWNER_ROLE`では「同期したという事実をproducer provenanceの証拠にしない」ために使われる。`VALIDATION_PLAN`では「同じnonterminal invocationを継続する」ために使われる。前者はresult admission、後者はticket継続であり、同じprimitive名でも境界は異なる。
- `root`は`PRODUCER`ではproducer identityの選択肢、`OWNER_ROLE / ROOT`ではcoordinatorによる代行禁止、`VALIDATION_CLOSURE`ではroot自身がproducerであるvalidationの発行方式を指す。出現回数を減らしても一つの意味へ統合できるわけではない。
- `model step`は`DECISION_BOUNDARY`では相互非依存invocationの発行frontier、`VALIDATION_CLOSURE`ではrequired validation集合の発行frontierを指す。後者には順序、個別exit、fail-fastという追加constraintがある。

## 保存証拠との対応

### 発行境界

Candidate147の対象15 runでは、開始identityと許可済みreadの両方を最初の発行対象へcommitした。Candidate205はportableな`issuance frontier`を追加したが、強いcommand event順ではidentity完了前にreadを開始したrunが0 / 15で、15 / 15が開始identityだけを先行した。これは特定の一語を除いたことだけの効果ではないため、`model step`という綴りの必須性は証明しない。一方、抽象的なfrontier定義だけではC147の正の発行順序を保持できなかった反例として使える。

したがってportableな保持対象は、特定API名ではなく「選択した全invocationを、いずれかのresultを次の選択へ消費する前に開始する」というイベント順である。ただし、同じruntime上でその順序を観測する手段を本文から全て外すことは、意味保存ではない。

### validation closureと継続identity

[validation二条項の原因監査](c147-validation-control-overlap-causal-audit.md)で、required-validation 190 run、403 command groupを確認した。189 / 190 runは全required commandを一つのwrapperへ閉じ、required commandの再実行は0件だった。nonterminal resultを受けた52 runの79 `wait`は、別toolまたは利用者向けmessageを先に挟んだ例が0件だった。

過去系列でも、Candidate81はwrapper precedenceの明示により複数required command caseのone-step closureを30 / 35から35 / 35へ改善した。Candidate107のF03 B20では同一cell wait 6 / 6、required validation再実行0 / 100だった。現在の`wrapper / cell ID / wait`は名称の列挙だけではなく、別々の失敗系列で成立した発行closureと継続identityに接続している。

### producer来歴

`runtime_spawn_result.task_name`と`FINAL_ANSWER.Sender`は、独立producerを起動したという事実と、そのproducerからterminal resultが返ったという事実を結ぶ。`wait`だけではこの対応を証明しない。Candidate190で独立`OWNER_ROLE`を統合後削除した際、Standard14の8 runでowner metadataが不要review producerへ昇格し、Candidate191では独立`OWNER_ROLE`を復元した。この反例はfield名そのものの不可変更性ではなく、producer routingとresult provenanceを別の観測点なしに抽象化・統合してはならないことを示す。

## 置換可能性の判定

| 置換案 | 保持できる意味 | 不足しているもの | 判定 |
|---|---|---|---|
| `root / worker`を`coordinator / producer`へ単純改名 | 役割の説明 | runtimeが返す実identityとの対応、現行cost | `not_evaluated`。Candidate軸にしない |
| `fork_turns=none`を「最小context継承」へ抽象化 | context最小化の目的 | 履歴非継承を実際に選択したことの観測点、現行cost | `not_evaluated` |
| provenance field名を一般的な「起動identity / sender identity」へ置換 | identity一致の概念 | 現runtimeで照合する具体field | `change_not_justified` |
| `model step / wrapper / tool call`を「frontier」だけへ置換 | 発行集合の概念 | result消費前の開始を保証・観測する正の遷移 | C205反例から`change_not_justified` |
| `cell ID / wait`を「同じinvocationを継続」だけへ置換 | 継続の目的 | 同一invocationであることを照合するtokenと操作 | 79 waitの成立経路から`change_not_justified` |
| `environment_recovery_max`を一般名へ改名 | allowance消費の意味 | 現行名が生むcostまたは誤経路 | `not_evaluated` |

## H3の現行判断

- runtime固有表面形を一括削除する案は、複数の意味拘束と観測点を同時に変えるため棄却する。
- 発行境界、producer来歴、nonterminal継続identityは、現在の証拠で実際に消費されている。これらを抽象概念だけへ置換する変更は正当化されない。
- `fork_turns=none`と`environment_recovery_max`の名称だけはportable置換余地があるが、具体的な現行costがない。名称変更だけのCandidateは作らない。
- C204/C205は「全体portable化が失敗した」という反例に限定して使い、個々のruntime語が単独で必須だとは主張しない。
- 新しいprompt set、profile、preflightまたは評価slotはこの表面形inventoryだけから作らない。

Standard14結果まで含めると、start gateの禁止operationとその専用evidence invocationを対応づけるrelationは設計できる。しかし、それがもたらすのは未観測drift時の追加安全性だけである。共同発行19件は全件合格でtokenも低いため、現行oracleの最適化としてrelationを追加しない。

## 後続監査へのhandoff

従来の再開条件に対応する二つのrouteはStandard14保存eventで観測したが、判断は異なる。

1. F10 monthlyの19 / 100件は、start identity resultを消費する前にreview evidence取得を開始したが、全件合格かつ低tokenなので変更対象にしない。
2. Standard14 event 1,385件中130件のroot C147本文再取得は、固定bundleからすでにmodel-visibleな同一authorityの再取得costとしてH1へ渡す。

その場合もADR9を先に評価し、通過後だけStandard14へ進む。TPO、他case、Evaluation setまたは保存済み別系列を現行比較へ混ぜない。

## 参照

- [Candidate147機能再分析](c147-functional-decomposition-reanalysis.md)
- [Candidate147制御群・境界重複・最適性監査](c147-control-group-overlap-optimality-audit.md)
- [Candidate147 Standard14結果起点の制御不足監査](c147-standard14-control-insufficiency-audit.md)
- [validation二条項の原因監査](c147-validation-control-overlap-causal-audit.md)
- [Candidate204 M5原因分析](candidate204-m5-causal-analysis.md)
- [Candidate205 M5原因分析](candidate205-m5-causal-analysis.md)
- [Candidate191 Standard14コスト機序再判定](candidate191-standard14-cost-mechanism-reassessment.md)
- [Candidate191実装監査](candidate191-explicit-review-operation-applicability-implementation-audit.md)
