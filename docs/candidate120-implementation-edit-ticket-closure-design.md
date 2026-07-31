# Candidate120 implementation edit ticket closure設計

## 結論

Candidate120はCandidate119を直接親とする。Candidate119で成立したvalidation predicate / exact command method境界を保持し、implementation choiceの確定表明をartifact変更実行票のcommit pointにする一変更軸を追加する。

`implementation_edit_ticket_ready`が成立したproducerでは、次のtool invocationをartifact変更だけに限定する。追加evidenceを予定している間はimplementation choiceまたは変更内容の確定を表明できない。これにより、Candidate119 A02で1 / 5件再発した「canonical implementationを確定した後にrepository evidenceを追加する」経路を対象にする。

## Identityと状態

- candidate number: Candidate120
- prompt identity: `the-caption-3ce91a4-implementation-edit-ticket-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`
- changed target: root `AGENTS.md`
- changed axis: implementation bind表明とartifact変更のtool-level隣接
- evaluation status: `targeted_a01_a02_f01_evaluated / quality_gate_passed / edit_ticket_closure_failed / a02_cost_target_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate119とする。
2. 最短正常経路はCandidate119 A02 run `2117c17ee92e422886f164618bb56bcf`である。canonical implementationをbindした直後に1行を変更し、変更後method探索なしでvalidationへ進んだ。tokenは`129,094`だった。
3. 誤経路はCandidate119 A02 run `d51dd5a794cf4d2298e647db8349f212`である。canonical targetと故障箇所を確定表明した後、二つのcommandでauthority、entrypoint実体、test設定を追加確認してから変更した。tokenは`212,159`だった。
4. Candidate119は変更後method探索を0 / 5件へ閉じたが、Candidate118の変更前terminal closureを1 / 5件で維持できなかった。よって二つの不足制御を同一事象へ畳み込まない。
5. 追加する一つのpredicateは、`implementation_edit_ticket_ready := target artifact ∧ 適用中instruction ∧ 実行可能な変更predicate ∧ 保持constraintが受領済みresultだけへbind済み`である。
6. 消す判断点は、implementation choiceまたは変更内容の確定を表明した後に、一般的安全確認、適用規則の再確認、validation method選択のためrepository evidenceを再び開く分岐である。
7. 新たな判断点は、追加evidenceを予定しているかの一件である。予定しているなら確定表明とticket readinessを遅らせる。確定表明したなら次のtool invocationをartifact変更にする。
8. A01 / A02 / F01各`N=5`で15 / 15 score `4`、A01変更・test 0 / 5、A02 canonical成果5 / 5、bind後・変更前再入0 / 5、変更後method探索0 / 5、F01 required command evidence 5 / 5を要求する。
9. A02 token中央値はCandidate119 `149,154`未満かつC81以降のcase最小Candidate107 `125,559`以下を要求する。一件でもqualityまたはmechanismが崩れるか、cost目標を超えた場合は停止し、N=20とStandard14へ進めない。

## 非目標

- Candidate119のvalidation predicate / method境界の撤回
- evidence output cap、projection、batching、read回数の固定
- validation nonterminal返却またはouter deadlineのexecutor制御
- case固有path、command、token値のprompt記載
- release、runtime projection、本体反映

## 初回試験

A01 r2 / A02 r2 / F01 r3、Rating v14、`gpt-5.6-sol` Medium、CLI `0.146.0`、各`N=5`、profile上の`M=24`へ固定する。Candidate119は保存済みresultを使い、Candidate120の不足15 slotだけを発行する。

## 評価結果

15 / 15件はvalidかつscore `4`だった。変更後method探索0 / 5件は維持したが、A02の確定表明後・変更前再入は2 / 5件へ増え、token中央値も`220,592`となった。事前停止条件に従いN=20とStandard14へ進めず停止する。詳細は[`評価結果`](../evaluations/results/candidate119-candidate120-implementation-edit-ticket-closure-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md)を正本とする。
