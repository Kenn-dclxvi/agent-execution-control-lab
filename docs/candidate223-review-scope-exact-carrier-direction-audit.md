# Candidate223 review scope exact carrier 方向監査

## 判定

`direction_passed / candidate_creation_authorized / evaluation_input_change_required`

## 監査結果

Candidate223の狭い差分は、pre-review source readのpermissionとresult recipientを、source内容ではなくsource外のscope-to-observation対応へbindすることだけである。

これは、whole sourceを読んだ後にownerを分類する条件ではない。root whole-source output、scope外reviewer outputおよびmixed-recipient outputは対応するcarrier entryを持たず、禁止される。必要な正常経路には、root packet projectionとscope固有のreviewer direct projectionがsource読取前から存在する。

ADR03からADR06でmissing paired targetを追加せず、carrierから除外する。ADR07とADR09ではinventory / contractsをcarrierから除外する。これは成功runの順序を固定する措置ではなく、現在のrequired review scopeへ関係しないread permissionを閉じる措置である。

Candidate promptだけではsource外の対応表を作れないため、TaskSpec、case revisionおよびEvaluation setを更新する必要がある。fixtureの意味、oracle、期待terminal、rating、runtime、permissionおよびexecutor条件は変えない。r2保存resultとの品質比較は行わず、Candidate223の新規45件だけを判定する。

## 動的に確認すること

- rootが全45件で列挙済みprojectionだけを受領するか。
- 必要reviewerが30 / 30件起動するか。
- ADR03からADR06でinventory / contractsだけを直接観測するか。
- ADR07とADR09でpaired scopeだけを直接観測するか。
- reviewer-owned resultがroot補完なしで期待terminalと変更effectへ接続されるか。

静的方向監査はこれらの成立を主張しない。
