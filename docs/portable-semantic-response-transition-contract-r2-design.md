# Portable semantic response transition contract r2設計

> [!IMPORTANT]
> **状態**: `calibration_completed / valid_14_of_14 / score4_12_of_14 / contract_inconsistency_detected / superseded_by_r3_clarification / new_heldout_not_created`

## 結論

semantic held-out r1がC147 referenceで6 / 14だった直接原因を、portable promptではなくmodel-visibleなresponse projection contractの不足として修正する。r2はresponse JSONの構造、Case、oracleおよびC147本文を変更せず、各response fieldが入力時点の状態一覧ではなく「この応答で新しく発行、admit、失効またはterminal化する遷移」を表すことを共通TaskSpecへ固定する。

既存PIC-H01〜H14はoracleを確認済みなので、新しいportable Candidateのheld-outには再利用しない。r2 contractがC147の既存意味を正しく投影できるかを確認するreference calibrationにだけ使う。C147が14 / 14を通過した場合に限り、同じcontractを使う別内容の未使用held-out revisionを後から凍結する。

## r1で不足していた共通意味

r1 TaskSpecはresponse schemaに適合するJSONを返すことだけを要求し、各配列の時間境界を定義していなかった。そのためC147は次を合法な応答として構成できた。

- 入力時点ですでにterminalのoperationを`terminal_operation_ids`へ再掲する。
- permission deniedのdecoyを`unavailable_operation_ids`へ状態一覧として載せる。
- fail-fast後に開始しない後続operationを、明示失効がなくても`invalidate`または`unavailable`へ移す。
- 個別validationのfailed terminal resultを、実行中の集約validationのterminalへ昇格する。
- `continue_invocation_ids`へinvocation IDではなくoperation IDを返す。

これらをCase別の正解一覧で禁止せず、全Caseへ共通するfield contractで閉じる。

## r2 field contract

全配列は、入力snapshotそのものではなく、この応答で新しく選択または確定するdeltaだけを返す。変化がないfieldは空配列にする。

| field | 入れるidentity | 入れないもの |
| --- | --- | --- |
| `clarification_missing_value_ids` | 今回clarificationへ出す未固定required outcome value | method、候補値、すでにboundのvalue |
| `start_operation_ids` | 現在`not_started`で、permissionとdependencyが今回の開始を許すoperation | denied、terminal、running、後続停止中のoperation |
| `continue_invocation_ids` | すでにrunningで、同じnonterminal invocationのterminal化だけを継続するinvocation ID | operation ID、別operation、未開始invocation |
| `admit_result_ids` | operation、actor、inputおよびresult kindへ対応し、今回admitするreceived result | provenance不一致result、既admit状態の再掲 |
| `invalidate_operation_ids` | admitted resultの明示effect scopeにより、既存bindingが今回失効するoperation | denied、terminal、satisfied、単に開始しない後続、capability欠落 |
| `terminal_operation_ids` | 入力時点でnonterminalだったoperationが、今回admitしたresultにより自身のcompletionを満たす場合 | 入力ですでにterminalのoperation、個別failed resultだけではsuccess completionを満たさない集約operation |
| `unavailable_operation_ids` | required resultを今作る必要があるが、能力、入力またはauthorityがなく合法な代替もないため、今回`unavailable`へ閉じるnonterminal operation | 単なるdenied decoy、入力時点の全denied operation、fail-fast後に開始しないだけの後続 |

received resultの`failed`または`failed_environment`もprovenanceが対応すればadmitできる。admitは、それだけで集約operationのterminal、effect scope外operationの失効または後続operationの`unavailable`を意味しない。fail-fast後の後続非開始は、明示effectによる失効または能力欠落によるterminal closureがない限り、`start_operation_ids`へ入れないことで表す。

## artifact境界

- r1 TaskSpec、held-out r1、oracle、ratingおよび保存resultを変更しない。
- r2 TaskSpecは`semantic-single-json-r2`として別fileへ固定する。
- calibration setは既存14 Caseを参照するが、`portable-instruction-semantic-reference-calibration-r2`という別identityにする。
- calibrationにはC147 referenceだけを発行する。portable r1、control-freeまたは新promptを発行しない。
- response schema構造はr2のまま維持し、field意味だけをTaskSpecで追加する。

## C147 calibration gate

次を全件満たした場合だけcontract r2をqualification済みにする。

- 14 / 14 valid、schema valid、一次tokenおよびelapsed取得。
- 14 / 14 Score 4。
- H01、H03〜H05、H10、H11、H13、H14でr1に観測したsnapshot再掲が0件。

一件でもScore 4を外れた場合はr2 contractを固定失敗として停止する。resultを見て同じrevisionを修正せず、C147本文へfield名やCase条件を足さない。

実測では12 / 14となり、`PIC-H04`ではwrapperがoracleの明示scope失効を禁止する矛盾、`PIC-H13`では必要な唯一のdenied recoveryとdenied decoyの区別不足を確認した。r2は固定失敗として保存し、Case、oracleおよびC147を変えずにこの2境界だけを明確化するr3へ進む。

## calibration通過後

通過後も既存14 Caseはportable評価へ使わない。operation名、値、依存形および正常／禁止routeを新しくしたheld-out r2を、C147 calibration resultとportable promptを変更しない状態で凍結する。その未使用held-outをC147へ先行発行し、C147が全件通過した場合だけportable r1を同じsetへ発行する。

## 参照

- [`C147 reference先行資格確認r1結果`](portable-semantic-c147-reference-qualification-r1-result.md)
- [`C147 transition contract r2校正結果`](portable-semantic-c147-transition-calibration-r2-result.md)
- [`r1 TaskSpec`](../evaluations/targets/portable-instruction-semantic-conformance/contracts/task-spec-wrapper-r1.txt)
- [`r1 held-out`](../evaluations/targets/portable-instruction-semantic-conformance/cases/heldout-r1/)
- [`C147 reference bundle`](../evaluations/targets/portable-instruction-semantic-conformance/prompts/baselines/portable-semantic-c147-full-agent-reference-r1/)
