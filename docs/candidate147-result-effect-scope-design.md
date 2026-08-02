# Candidate147 result effect scope設計

## 結論

Candidate147はCandidate145を直接親とし、`DECISION_BOUNDARY`一軸だけをoperation class別の`result_effect_scope`へ置換する。

開始identity resultが変え得る後続操作をtask全体へ広げない。TaskSpecがdrift時にartifact変更とrequired commandだけを禁止し、readを禁止しない場合は、identity観測と既に許可・固定されたreadを同じmodel stepから発行する。その共同resultを受領してidentityが正常と判定されるまで、artifact変更とrequired commandだけを閉じる。

Candidate125のexact target set、single-target continuation、固定spanは継承しない。Candidate146のconsumer closureも継承しない。

## Identity

- candidate number: Candidate147
- prompt identity: `the-caption-3ce91a4-result-effect-scope-r1`
- direct parent: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`（Candidate145）
- changed target: root `AGENTS.md`
- changed axis: `DECISION_BOUNDARY`のresult effect scope
- evaluation status: `standard14_n5_evaluated / quality_gate_passed / mechanism_generalization_supported / f06_local_token_residual`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. C143はrequired outcome全体のimplementation bindによりF02 / F04 / F07各N=100を300 / 300 score `4`で通過した。
2. C145はStandard14 70 / 70 score `4`で、consumerのないA02 evidence再入を閉じた。
3. C125 / C145 / C146のF01 / F02 / F03各5件を`agent_message`境界で再監査した。
4. source / testの初回既知観測はC125、C145、C146の全45件で同じmodel stepから共同発行されていた。
5. identityとcontentの共同発行はC125 13 / 15、C145 0 / 15、C146 1 / 15だった。
6. 変更前model step中央値はC125がF01 / F02 / F03すべて1、C145がすべて2、C146が3 / 3 / 2だった。
7. 評価TaskSpecはidentity確認を最初のeditまたはrequired command前に要求するが、read前には要求しない。
8. C145の`DECISION_BOUNDARY`はresultが何らかの後続invocationを変え得るかを判定するが、影響を受けるoperation classを限定していない。
9. Candidate146は誤ったcommand / model-step分析を根拠にしたため親にしない。保存traceは診断証拠としてだけ使う。
10. executor、CLI、runtime hook、wrapper、rating contractは変更しない。

## 置換する境界

```text
result_effect_scope :=
  受領resultがtarget / permission / method / stop conditionを
  変え得る未発行operation classの集合

decision_boundary(next_operation) :=
  next_operation.class ∈ result_effect_scope
```

resultの停止効果を、task全体や後続全invocationへ伝播させない。後続operationごとに、そのclassが`result_effect_scope`へ入る場合だけresult受領まで発行を待つ。

F01 / F02 / F03の開始identityは次のようにbindする。

```text
identity_result_effect_scope = {artifact_change, required_validation}
authorized_read ∉ identity_result_effect_scope
```

そのためidentity観測とTaskSpecで既に許可・固定されたcontent readは同じmodel stepから発行できる。共同resultを受領してidentityが正常と判定されるまで、artifact変更とrequired commandは発行できない。

TaskSpecがdrift時にreadも禁止する場合、またはidentity resultでread target / permissionが変わり得る場合は、readもscopeへ入り別stepになる。

## 既存制御との関係

- Candidate69の`DECISION_BOUNDARY`はresultが次invocationを変え得るかを一般判定した。Candidate147はその判定をoperation class別にし、停止効果の伝播範囲を明示する。
- Candidate112のscheduling分離は発行順を変更したが、resultがどのoperation classへ効くかを固定しなかった。Candidate147はscheduling手続きを追加しない。
- Candidate125はidentityとcontentを13 / 15件で共同発行したが、exact target waveとsingle-target continuationを伴う。Candidate147は共同発行のauthorityをTaskSpec permissionと`result_effect_scope`だけに置く。
- Candidate143のrequired outcome implementation bind、Candidate144のvalidation predicate / method境界、Candidate145のlifecycle consumer gateは保持する。
- Candidate146のconsumer closureはC145ですでに成立していた挙動を再記述したため継承しない。

## 汎用性

`result_effect_scope`は開始identity専用ではない。

- schema確認resultが生成操作だけを止め、無関係なreadは止めない場合
- permission確認resultがexternal sendだけを止め、local analysisは止めない場合
- dependency確認resultがinstallだけを止め、manifest readは止めない場合
- failure resultが一つのrework targetだけを失効し、他effectを失効しない場合

に同じ境界を適用できる。

重要なのは、先行resultがtask全体に影響するかではなく、次operationのclassに実際に影響するかである。

## 初回評価gate

初回はF01 / F02 / F03各N=5、M=24とする。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| identityと初回許可readの共同model step | 15 / 15 |
| identity共同result受領前のartifact変更 | 0 / 15 |
| identity共同result受領前のrequired command | 0 / 15 |
| source / test初回既知観測の共同発行 | 15 / 15 |
| consumerのないevidence | 0 / 15 |

一件でもscore `3`以下、identity result前の変更・required command、またはidentity / read共同発行欠落があれば停止する。

## Cost gate

- 直接比較は同一互換条件のCandidate145 F01 / F02 / F03各N=5とする。
- C125同caseは到達目標として補助比較する。
- 3 case合計token中央値とelapsed中央値がCandidate145以下であることを確認する。
- case別上昇があればmodel step、continuation、content output、cached inputを分ける。
- N=5からStandard14全体へ一般化しない。

## 非目標

- identity result受領前のartifact変更またはrequired command
- drift時にTaskSpecが禁止するoperationの先行発行
- exact target set、single-target continuation、固定span
- shell compound、特定command、file数、read数の固定
- Candidate146 consumer closureの継承
- required validationの省略または緩和
- executor、CLI、runtime hook、wrapper変更

## 初回試験

- cases: F01 r3 / F02 r1 / F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- repetition / configured M: 各`N=5` / `24`
- direct reference: Candidate145同case atomic run
- prompt以外の互換条件: Candidate145と完全一致

Candidate145の既存runは再実行しない。Candidate147の不足15 slotだけを発行する。全gate通過時だけ追加試験を別判断する。

## 初回評価結果

F01 / F02 / F03各N=5は15 / 15件がscore `4`だった。開始identityと初回許可readの共同model step、source / test初回共同発行、共同result後のartifact変更はすべて15 / 15件で成立した。共同result前のrequired validationと、利用先のない変更前evidenceは0件だった。

3 case集約中央値はCandidate145比でtoken `-25.97%`、elapsed `-22.34%`だった。変更前model step中央値は3 caseすべてCandidate145の`2`から`1`へ減り、Candidate125と一致した。

詳細は[`Candidate147 F01 / F02 / F03 N=5 result`](../evaluations/results/candidate145-candidate147-result-effect-scope-v14-medium-f01-f02-f03-atomic-n5-cli0146_2026-08-02.md)を正本とする。targeted評価完了時点ではStandard14とN>5は未評価で、Standard14は後続の別判断で実施した。

## Standard14評価結果

先行15 runを再利用し、不足55 runだけを発行したStandard14 N=5は70 / 70件がscore `4`だった。変更前command-bearing model step中央値はCandidate145比で9 / 14 caseが一つ減り、5 caseは同じで、増加caseはなかった。

集約中央値はCandidate145比token `-9.17%`、elapsed `-23.13%`だった。Candidate125比はtoken `+3.31%`、elapsed `+0.73%`まで縮まった。一方、F06 tokenはCandidate145比`+28.09%`で、追加instruction / authority確認2件と完了確認重複1件が高token側3件に対応した。

詳細は[`Candidate147 Standard14 N=5 result`](../evaluations/results/candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)を正本とする。

## F06 N=100追試

既存5件を再利用し、`+24 → +24 → +24 → +23`の順で不足95件だけを発行した。各waveの採点後にscore `3`以下を確認し、100 / 100件がscore `4`で完走した。token中央値はN=29以降約`105k`で安定し、初期N=5の`151,542`は代表中央値ではなかった。

authority追加readは21 / 100件に残り、発生群のtoken中央値`160,327`は非発生群`104,230`より`53.82%`高かった。高token上位10件中7件が該当する一方、3件は非該当だった。よって局所的な高token経路との関連は支持されるが、単独原因とは確定しない。

詳細は[`Candidate147 F06 N=100 result`](../evaluations/results/candidate147-result-effect-scope-v14-medium-f06-atomic-reuse-n100-cli0146_2026-08-02.md)を正本とする。この追試はF06だけであり、Standard14全体のN=100安定性を示さない。この時点では採用判断を行っていない。

## Standard14 N=100と後続の採用判断

後続の[`Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)は14 case合計1,400 / 1,400件がscore `4`で、score `3`以下、excluded attempt、controller error、command protocol violationは0件だった。集約中央値はtoken`1,394,412.5`、elapsed`831.914秒`だった。

一次evaluation resultの`adoption_not_decided`は変更しない。2026-08-03の後続別stateで[`Candidate147採用判断`](candidate147-adoption-decision.md)を記録し、`adopted / release_not_created / runtime_not_projected`とした。
