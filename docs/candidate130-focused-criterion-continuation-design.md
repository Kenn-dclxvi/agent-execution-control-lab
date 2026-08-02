# Candidate130 focused criterion continuation設計

## 結論

Candidate130はCandidate128を直接親とし、`EVIDENCE_GATE`のcontinuation request preferenceだけを変更する。未観測criterionへ一意にbind済みのsymbol identityがある場合は、全未取得contentではなく、その全symbol contextを一つのinvocationで直接返す。symbol identityを一意にbindできない場合だけ、同一targetの全未取得contentを終端まで要求する。

## Identityと変更軸

- candidate number: Candidate130
- prompt identity: `the-caption-3ce91a4-focused-criterion-continuation-r1`
- direct parent: `the-caption-3ce91a4-required-effect-closure-r1`
- changed target: root `AGENTS.md`
- changed rule: `EVIDENCE_GATE`
- changed axis: continuation evidenceのfocused symbol優先
- bundle SHA-256: `690885185785d8e254b52370a34543fe5ae37fc58b14111c2ca7c0eadcfe2486`
- evaluation: `targeted_f04_n5_evaluated / quality_gate_failed / stopped`
- adoption: `not_adopted`

## 既存制御との重複監査

Candidate124は、read可能targetの未観測criterionを`missing`と分け、同じtargetのrangeまたはsymbol周辺へ一度だけcontinuationする境界を導入した。しかしbounded rangeを620行で終えた2 / 5件がfalse stopした。

Candidate125は、未観測criterionへbindしたsymbol contextまたは全未取得contentを覆うrequestを許可し、F04 N=5のfalse stopを0件へ戻した。ただし二方式が同順位のOR条件であり、既知symbolがあっても全未取得contentを選べる。C129 F04では3 / 5件が全残存contentを要求し、保存raw outputには必要contentが存在した一方、model-visible resultの中央部分が切り詰められたため停止した。

Candidate121のlocator-only result後に別content invocationを発行する二段階routeは、F02のdecision roundとcostを増やしたため継承しない。Candidate130はlocator identityを独立resultにせず、一つのcontinuation invocationから直接contextを返す。

## 保存済み誤経路

C129のscore 1三件では、初回resultから`hasAuditKey = true`を観測した。次の`sed -n '261,$p' App.tsx`は保存raw outputで各41,435 bytesあり、`Audit Key`と正しい`colSpan={hasAuditKey ? 7 : 6}`を含んだ。しかしmodelへ渡されたresponse itemは中央contentが切り詰められ、モデルは`colSpan`を未観測と判断してartifact変更とrequired validationを開始しなかった。

これはreport delivery自体をpromptで制御できるという証拠ではない。prompt-visibleに選べるのは、既知symbolへ直接bindした小さいrequestを先に選ぶことだけである。

## 一つのpredicate

`continuation_scope_complete := 未観測criterionへ一意にbind済みのsymbol identityが一つ以上なら同一targetの全bind済みsymbol contextを一つのinvocationで直接返す ∨ symbol identityを一意にbindできない場合に限り同一targetの全未取得contentを終端まで覆う`

変更しないものは次である。

- Candidate128の`RECOVERY`と`required_effects_closed`
- `single_change_target_ready`
- continuation一回上限
- 複数targetのinitial content wave
- effect stateとchange admission
- dependency grouping
- validation control

## F04 N=5 gate

初段はF04 r2だけをN=5、M=24で実施する。model、reasoning、CLI、runtime、permission、rating、fixture、TaskSpec、token accounting、executor条件はCandidate128の保存済みF04 runと互換に固定する。

- valid / rateable / score `4`: 5 / 5
- score `3`以下: 0 / 5。一件でも発生したら停止
- 初回contentで全criterionが見えない場合、focused symbol continuation: 5 / 5
- locator-only独立result: 0 / 5
- 全未取得content continuation: symbol identityを一意にbindできない場合だけ
- continuationのmodel-visible resultに必要symbol context: 5 / 5
- artifact変更なしfalse stop: 0 / 5
- continuation二回目、新target、repository-wide search: 0 / 5

このgateではinitial patch failureをEvidence coverageの合否へ混ぜない。Candidate128 recoveryで5 / 5の成果完了を要求するが、first patchのeffect選定は第3点の別検証で扱う。F04通過後だけ、F02 N=5で複数target initial waveの保持を確認する。

## Targeted evaluation result

2026-08-01にF04 r2 N=5を実施した。5件はすべてvalidでexcluded attemptは0件だったが、score分布は`4 / 1 = 2 / 3`となった。全5件がfocused symbol contextではなく`sed -n '261,$p' App.tsx`を選び、focused continuationは0 / 5だった。3件は必要contentのmodel-visible切詰めまたはpatch不一致後に変更・required validationなしで停止した。

追加した優先関係は実行判断を制御しなかった。事前停止条件に従いCandidate130を停止し、F02、Standard14、採用、release、本体投影へ進めない。一次結果は[`Candidate128 / Candidate130 F04 N=5`](../evaluations/results/candidate128-candidate130-focused-criterion-continuation-v14-medium-f04-atomic-n5-cli0146_2026-08-01.md)を正本とする。
