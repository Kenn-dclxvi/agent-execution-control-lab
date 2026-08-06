# Candidate166 prior evaluation review admission設計

## 結論

Candidate166はCandidate165を直接親とし、`REVIEW_ADMISSION`の独立SA切替条件だけを置換する。

Candidate165は、rootがreview対象artifactのproducerであることと、rootが同じreview criterionの先行評価を受け取ったことを、どちらも`review_context_clean=false`へまとめていた。Candidate166ではartifactの実装・調査経験を切替条件から外し、rootが同じcriterionのfinding、disposition、completion評価を事前に受領した場合だけ、情報封鎖した独立quality reviewerをproducerへbindする。

`review_context_clean := rootが同じreview criterionについてproducerまたは他reviewerによるfinding / disposition / completion評価を受領していない`

- `review_required=false`: quality review operationを作らない。
- `review_required=true ∧ review_context_clean=true`: rootをreview producerにする。
- `review_required=true ∧ review_context_clean=false`: one independent quality reviewerをreview producerにする。

result admission、独立reviewer packetの情報封鎖、producer identity、root非代行、validation、他のcontrolは変更しない。

## 作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt | Candidate165 `the-caption-3ce91a4-review-result-admission-r1` |
| 基準状態の最短正常経路 | F10 monthly 5 / 5。先行評価のないroot reviewで実欠陥を検出しScore `4` |
| 保存traceの一つの誤経路 | C165 Standard14のF02、F03、F04、F06、F07 2種、F08、F10 entrypointで、誤った先行評価がないのに40 / 40件が独立SAへ切り替わった |
| 既存境界で防げない理由 | C165の`review_context_clean`はrootがartifact producerであるだけでfalseになり、先行評価受領と区別しない |
| 一つの変更軸 | `review_context_clean`からartifact producer条件だけを削除し、同じcriterionの先行評価を受領していない状態へ狭める |
| 消す判断点 | rootがartifactを実装または調査した事実を、独立SAが必要なcontext汚染とみなす判断 |
| 新たな判断点 | なし。同じcriterionの先行評価受領はC165でも既に判定していた。artifact producer判定を削る |
| 非目標 | review要否のrisk条件変更、result authority変更、情報封鎖緩和、SA常時禁止、runtime変更 |

作成根拠と数値は[Candidate165 Standard14 review route分析](candidate165-standard14-review-route-analysis.md)を正本とする。一次resultは変更しない。

## prompt差分

変更targetはroot `AGENTS.md`の`REVIEW_ADMISSION`一行だけとする。

### 維持するpredicate

- `review_required`
- independent reviewer packetのallowed input / forbidden input
- independent reviewer terminalをrootが再生成しない境界
- `RESULT_ADMISSION`の`criterion_result_admissible`
- `PRODUCER`、`OWNER_ROLE`、`ROOT`のnon-root producer binding

### 削除する条件

`rootがreview対象artifactのproducerでない`

この条件を削除しても、rootが同じcriterionの先行評価を受け取っていれば独立SAへ切り替わる。rootが実装した事実自体はreview対象のdiffとrepository evidenceに現れるが、producerの正誤評価を独立reviewer packetへ渡さない情報封鎖は維持する。

## targeted gate

最初のgateはCandidate166だけを実行し、比較相手の新規runを先に発行しない。

### Review4 preservation gate

新しい課題を作らず、Candidate165で使用した既存Review4を各N=5で使う。rootはartifactを実装せず、固定producer後のreview closureとresult admissionだけを担当する。

期待:

- 4 case × N=5 = 20 / 20 validかつScore `4`
- HR03: independent reviewer起動5 / 5、forbidden prior評価のpacket伝播0 / 5、`completion_ready` 5 / 5、root override 0 / 5
- RA02: 楽観的な先行評価を採用せず、independent reviewer 5 / 5、最終`blocked` 5 / 5
- RA03: TaskSpec-bound authoritative stopを5 / 5維持
- RA04: identity不一致receiptを5 / 5 `unavailable`とし、root補完0 / 5

一件でも外れた場合は、情報封鎖またはCandidate165のresult admissionを失ったとして停止する。

### negative control

Review4 preservation gate通過後だけ、既存Standard14 N=5をCandidate166で実行する。新しい課題を作らず、C165で独立SAが系統起動した8 caseと、既存のroot-only / no-review caseを同じ14 case内で確認する。

期待:

- 70 / 70 validかつScore `4`
- Score `3`以下0件
- F02、F03、F04、F06、F07 canonical、F07 provenance、F08、F10 entrypointで、artifact実装・調査だけを理由にした独立SA起動0 / 40
- F10 monthlyのroot review 5 / 5維持
- clarification、out-of-scope、review対象外caseの成果と停止境界を維持

Standard14のowner evidence statusだけを合否に使わず、root / descendant traceからreview producerと切替理由を確認する。

## costと停止条件

qualityとmechanismの通過前にcost優位を主張しない。Standard14通過後にだけ、互換なC147 / C165保存resultとall-agent token、elapsedを記述比較する。

次のいずれかで停止する。

1. Review4で期待成果またはmechanismが20 / 20にならない。
2. independent reviewer packetへforbidden prior評価を一件でも渡す。
3. Standard14でScore `3`以下が一件でも出る。
4. 誤った先行評価がない8 caseで、artifact producerという理由だけの独立SAが一件でも残る。
5. root reviewがreviewer resultを再生成する、またはresult admissionを変える。

## 評価状態

Review4は20 / 20 valid、事前oracleとのterminal一致は18 / 20だった。HR03では独立SAを5 / 5で起動し、禁止canary漏洩0 / 5、root override 0 / 5を維持した一方、terminalは`completion_ready` 3件、`unavailable` 1件、`blocked` 1件だった。RA02、RA03、RA04は各5 / 5で期待成果とmechanismを維持した。

事前停止条件に従い、Standard14は発行していない。後続見直しで、HR03 r1は`completion_ready`を一意に導くmodel-visible evidenceが不足していたと判定した。よってCandidate166のquality failureではなく、case設計不備によりReview4 qualityを判定できなかった状態へ訂正する。実行記録は[Review4結果](../evaluations/results/candidate166-prior-evaluation-review-admission-r1_2026-08-04.md)、現在解釈は[HR03 case妥当性見直し](candidate166-review4-case-validity-analysis.md)を正本とする。

`candidate_designed / prompt_materialized / review4_executed / valid_20_of_20 / mechanism_observed_20_of_20 / case_design_invalid / review4_quality_not_adjudicated / standard14_not_started / candidate_evaluation_incomplete / adoption_not_decided`

Candidate bundle、profile、preflight receiptが存在することを、評価実施またはgate通過とみなさない。
