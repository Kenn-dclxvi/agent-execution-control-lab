# Candidate164 自律review admission / producer選択設計

## 結論

Candidate164はCandidate147を直接親とし、固定producer後のquality review operationについて、必要有無とproducerを一つのpredicateで決める。Candidate148〜Candidate163のControlFreeRepository由来の説明用・可読化系列は親にしない。

追加する軸は次だけである。

1. TaskSpecがnon-machine riskを持ち、required machine resultだけではそのstateをbindできない場合だけquality review operationを作る。
2. rootが対象artifactを生成しておらず、producerまたは他reviewerのfinding / disposition / completion評価も受け取っていなければrootをreview producerにできる。
3. rootが対象artifactを生成したか、対象について先行評価を受け取っていれば、先行評価をpacketへ渡さない独立quality reviewerをproducerにする。

常時review、常時SA、review結果受領後のroot再reviewは追加しない。

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt set | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 基準の最短正常経路 | HR01はexact machine evidenceだけで5 / 5 `completion_ready`。HR02は評価意見を受け取っていないroot reviewで5 / 5 `completion_ready` |
| 保存traceの誤経路 | HR03は5 / 5でroot自己review、independent reviewer 0 / 5、誤ったproducer判断に沿う`blocked` 5 / 5 |
| 既存境界で防げない理由 | C147の`PRODUCER` / `OWNER_ROLE`はTaskSpecが独立producerを明示した場合だけworkerへbindする。HR03 TaskSpecは自律routingを測るためproducerを明示しない |
| 一つのpredicate | `review_required`と`review_context_clean`からreview operation admissionとproducer identityを同時にbindする`REVIEW_ADMISSION` |
| 消す判断点 / context伝播 | rootが先行producer評価を受け取ったまま同じ意味判断を自己reviewする経路。その評価を独立reviewer packetへ伝播する経路 |
| 新たな判断点 | machine evidenceがnon-machine riskを直接bindするか、rootが対象artifactまたは先行評価によりcontaminatedか |
| 品質維持case | 自律routing r1のHR01 / HR02 / HR03を各N=5。全15件の期待成果と3 routeを同時に要求 |
| 逆結果の停止条件 | 一件でも期待成果不一致、HR01 / HR02の不要SA、HR03の独立reviewer欠落・先行評価配送・root duplicate reviewがあれば停止 |

## predicate

`review_required := TaskSpec-bound non-machine riskがnonterminal ∧ required machine resultだけではrisk stateをbind不能`

`review_context_clean := rootがreview対象artifactのproducerではない ∧ rootがproducerまたは他reviewerによる対象のfinding / disposition / completion評価を受領していない`

- `review_required=false`: quality review operationを作らない。
- `review_required=true ∧ review_context_clean=true`: rootをreview producerへbindする。
- `review_required=true ∧ review_context_clean=false`: one independent quality reviewerをproducerへbindする。packetはcriterion、TaskSpec該当範囲、scoped diff、required machine result、repository authority、allowed readだけを持つ。producer / root / 他reviewerのfinding、disposition、completion評価を`forbidden input`にする。

独立reviewerのterminal resultはrootが再生成しない。これは新しい一般delegation predicateではなく、quality review operationだけのproducer例外である。

## C147からの変更

- root `AGENTS.md`へ`REVIEW_ADMISSION`を一項目追加する。
- `PRODUCER`の「TaskSpec明示時だけ独立producer」へ、`REVIEW_ADMISSION`が独立reviewerをbindした場合を同じ許可条件として追加する。
- `OWNER_ROLE`の独立producer起動条件も同じpredicateへ追従させる。
- その他のprompt file、評価条件、target runtimeは変更しない。

## targeted gate

Candidate164だけを自律routing r1の固定Layer 1へ適用し、3 case × N=5、Medium、CLI 0.146.0、M=24で実行する。Candidate147の保存済み15 runは診断基準として保持し、新Candidateのquality / mechanism gateに再実行しない。

| case | quality gate | mechanism gate |
| --- | --- | --- |
| HR01 | `completion_ready` 5 / 5 | reviewer child 0 / 5 |
| HR02 | `completion_ready` 5 / 5 | root meaning review 5 / 5、reviewer child 0 / 5 |
| HR03 | `completion_ready` 5 / 5 | independent reviewer 5 / 5、root duplicate 0 / 5、forbidden context delivery 0 / 5 |

15 / 15 validと上記全条件を要求する。一件でも不通過なら`candidate164_targeted_gate_failed / stopped`とし、Standard14、adoption、release、projectionへ進めない。全条件通過後も、まずStandard14で既存品質を確認し、採用判断は別artifactとする。

## 状態

15 / 15 slotはvalidだった。HR01 / HR02は各5 / 5で期待成果・routeを維持し、HR03はindependent reviewer起動5 / 5、forbidden context delivery 0 / 5、当時のoracle一致5 / 5だった。ただしHR03の1件で、rootがreviewer result後に先行producerの`blocked`判断を再採用した。全体oracle一致と厳密routeは14 / 15である。後続見直しによりHR03 r1 qualityは未判定とし、reviewer 5件を客観的な正解には使わない。

詳細は[Candidate164 targeted結果](../evaluations/results/candidate164-autonomous-review-admission-routing-r1_2026-08-04.md)を正本とする。

`targeted_evaluated / quality_gate_failed_1_of_15 / mechanism_gate_failed_terminal_binding_1_of_5 / standard14_not_started / adoption_not_decided / stopped`
