# Portable full-agent conformance r1不通過境界監査

> [!IMPORTANT]
> **状態**: `portable_objective_rebound / c147_reference_score4_6 / heldout_r1_reference_not_qualified / response_projection_contract_underdefined / portable_equivalence_unresolved / efficiency_work_paused / compact_candidate_not_created / conformance_candidate_not_created`

## 結論

portable full-agent r1のheld-out r1 N=1は、正式result上では14件中7件だけがScore 4であり、portable版は完成していない。ただし、不通過7件をそのままportable本文の機能欠落7件として扱うこともできない。

PIC-H03、H04、H05、H13、H14の5件では、期待された主要な開始、result admission、局所失効またはrecovery closureは応答に含まれていた。不通過の直接差は、入力時点ですでにterminalまたはpermission deniedだったoperationや、今回の応答で新しい遷移を生じないoperationを`terminal_operation_ids`、`unavailable_operation_ids`または`invalidate_operation_ids`へ追加したことである。一方、model-visibleなTaskSpecとresponse schemaは、各配列が「入力時点の状態一覧」ではなく「この応答で新たに確定または開始する遷移だけ」を表すことを定義していない。

PIC-H10とH11では、失敗した個別validation resultのadmissionと後続validation非開始は成立したが、実行中の集約validationまでterminalにした。後続のC147 reference先行資格確認でも両CaseはScore 1となり、同じ個別result／集約状態projectionを一意にできなかった。したがって、この差をportable本文固有の曖昧さへ帰属できない。

したがって、現在の目的を効率化からportable機能完成へ戻す。block統合、byte削減、compact CandidateおよびN拡張は停止したままにする。C147が6 / 14だったheld-out r1はportable同等性gateに使わず、target固有のresponse projection contractを別revisionで直して再びC147を先行資格確認するか、このsemantic setを完成gateから外してStandard14へ一本化する。portable promptへCase固有の出力規則を転記しない。

## 固定する目的

`task_objective`は次で固定する。

- target改善系列: C147の実行制御を、製品名、CLI名、tool名およびrepository layoutに依存しないfull-agent一枚へ再構成する。
- required effect: C147由来81 primitiveの意味、permission、dependency、result admissionおよびterminal closureを欠落なく保持する。
- preserved effect: componentで管理しながら、modelへは外部component readを要求しない自己完結した一枚を配送する。必要な正常経路を閉じず、成功runの処理順を新しい義務へしない。
- artifact relation: C147を直接の意味上の親とし、portable r1は継承元ではなく、評価protocolの未定義と集約terminal曖昧さを露出した反例とする。

本文短縮、byte削減、token削減、elapsed削減、root-only化および他surfaceへのprojectionは、この目的の完了条件へ入れない。

## 一次resultで観測した7件

| Case | 期待された主要効果 | r1で成立した効果 | 不通過になった追加出力 | 現在の分類 |
| --- | --- | --- | --- | --- |
| PIC-H03 | 必要な`op-read-checksum`だけを開始 | 必要observationを開始し、禁止readとactionは開始しなかった | satisfiedな`op-read-theme`を失効、deniedな`op-read-history`をunavailableへ掲載 | response projection未定義が直接影響 |
| PIC-H04 | `res-a`をadmitし、`op-a2`だけを失効、独立`op-b1`を開始 | 3効果すべて成立 | 入力時点でterminalの`op-a1`とdeniedの`op-c1`を状態一覧として追加 | response projection未定義が直接影響 |
| PIC-H05 | bind済みactorの`res-saffron`だけをadmit | 正しいresultだけをadmit | 入力時点でterminalの`op-review`を追加 | response projection未定義が直接影響 |
| PIC-H10 | failed `res-v1`をadmitし、後続を開始せず、集約をnonterminalに保持 | admissionと後続非開始は成立 | 後続をinvalidateし、個別`op-v1`と集約`op-validation`をterminalへ掲載 | projection未定義に加え、集約terminal境界が曖昧 |
| PIC-H11 | success／failedのprefixを個別admitし、後続を開始せず、集約をnonterminalに保持 | 2 resultのadmissionと後続非開始は成立 | 後続をinvalidateし、個別`op-v1`、`op-v2`と集約`op-validation`をterminalへ掲載 | projection未定義に加え、集約terminal境界が曖昧 |
| PIC-H13 | environment failureをadmitし、allowanceなしrecoveryをunavailableにする | admissionとrecovery closureは成立 | 入力時点でterminalの`op-exec`を追加 | response projection未定義が直接影響 |
| PIC-H14 | environment failureをadmitし、exact recoveryだけを開始 | admissionとexact recovery開始が成立し、代替methodを開始しなかった | 入力時点でterminalの`op-exec`とdeniedな代替methodを状態一覧として追加 | response projection未定義が直接影響 |

この表は不通過を合格へ読み替えるものではない。固定済みoracleに対する正式状態は`quality_failed`のまま保持する。目的は、次のpromptへ7 Case分の正解routeを転記しないために、prompt責務と評価protocol責務を分けることである。

## model-visible contractの不足

held-out r1のmodel-visible TaskSpecは、供給したCaseについてresponse schemaに適合するJSON objectを一件返すことだけを要求する。response schemaは各fieldをuniqueなstring配列として定義するが、次を定義していない。

- `terminal_operation_ids`が現在terminalである全operationなのか、この応答で新しくterminalになるoperationだけなのか。
- `unavailable_operation_ids`がpermission deniedを含む現在状態一覧なのか、必要resultを作れず今回terminal closureするoperationだけなのか。
- `invalidate_operation_ids`が今後開始しない全operationなのか、受領resultによって既存bindingが今回失効したoperationだけなのか。
- すでにterminalの個別operationを、admitしたresultと同じ応答へ再掲するか。

設計文書には「次に合法な操作集合」という説明があるが、その文はmodel-visible packetへ配送されていない。prompt identityを比較する評価で、portable promptだけへこのtarget固有projectionを追加すると、prompt差へ評価protocolの不足を混ぜることになる。

## C147にも残った境界

PIC-H10とH11は、projection contractを明示しても次の区別を必要とする。

1. 個別validation executionのfailed resultは、その個別executionについて確定したterminal resultである。
2. failed resultを受領すると、固定順の後続executionを開始するpermissionは閉じる。
3. そのfailed resultだけでは、全required validationがsuccessした場合にだけ成立する集約operationのcompletionは満たさない。
4. 後続を開始しないことと、後続operationの既存bindingを失効させることは同じ効果ではない。

portable r1だけでなくC147 referenceも、個別executionと集約operationのどちらをresponse fieldへ投影するか一意にできなかった。この観測は評価contractのrevision根拠にはなるが、portable本文変更の根拠にはしない。C147にない新機能を要求するならportable同等性とは別系列にし、C147の意味を測るなら新revisionでC147が通ることを先に確認する。

## Candidate作成前gateの現在値

| 項目 | 現在値 |
| --- | --- |
| 直接の親 | C147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 正常経路 | 個別resultをoperation／actor／input／kindへadmitし、failed時は後続発行を閉じ、全required successが揃うまで集約を完了しない |
| 実測問題経路 | failed個別resultを受けた同じ応答で、実行中の集約validationをterminalへ移した |
| 閉じる必要がある辺 | 個別executionのterminal resultを、集約operationのcompletionへそのまま昇格できる辺 |
| 維持する経路 | success prefixの個別admission、最初のnon-success後の後続非開始、missing／unexpected result時の非補完 |
| 許可するprompt差分 | 個別result、後続発行permission、集約completionのownerを一意にする意味修復だけ |
| 許可しない差分 | Case別正解、response field名、byte削減、責務統合、tool順、runtime adapter、TaskSpec、case、oracle、ratingの同時変更 |
| 評価条件 | held-out r1はC147 6 / 14で不適格。新しいresponse projection revisionを作る場合もC147先行資格確認が必要 |
| 停止条件 | projection revision未固定、正常経路を閉じる、81 primitive欠落、または問題辺をprompt準拠のまま残す場合はCandidateを作成しない |

評価条件が未固定であるため、現時点ではCandidate bundle、Profile、preflightおよびslotを作成しない。

## 次の分離された作業

1. **評価protocolの別revision**: model-visible共通contractへ、各response fieldが現在状態一覧ではなく今回の合法な遷移を返すこと、および既存terminal／denied operationを再掲しないことを、Case固有正解を含めず固定する。既存held-out r1、oracle、resultは変更しない。
2. **C147先行資格確認**: 新revisionをportableより先にC147で実行し、全Case Score 4の場合だけ局所診断へ使用する。
3. **portable意味修復**: C147が通る新revisionでportable固有の差を観測した場合だけ、C147を直接の親としてtarget非依存の意味境界を修復する。
4. **Candidate N=1 quality gate**: 資格確認済みrevisionでportableを測る。効率は記録してもportable完成の修復差分へ混ぜない。
5. **効率化の再開**: portable機能完成を確認した後にだけ、機能block統合とcost比較を別Candidateとして再開する。

既存held-out r1は変更しない。後続のC147 reference結果は[`先行資格確認r1結果`](portable-semantic-c147-reference-qualification-r1-result.md)を正とする。

## 一次参照

- [`portable full-agent r1正式result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json)
- [`portable full-agent r1品質gate`](portable-full-agent-candidate-quality-gate-r1-result.md)
- [`portable semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`held-out r1 freeze`](portable-instruction-semantic-conformance-heldout-r1/)
- [`portable full-agent r1 bundle`](../evaluations/targets/portable-instruction-semantic-conformance/prompts/candidates/portable-semantic-c147-portable-full-agent-r1/)
- [`C147 reference bundle`](../evaluations/targets/portable-instruction-semantic-conformance/prompts/baselines/portable-semantic-c147-full-agent-reference-r1/)
- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
