# Candidate192 consumer-bound co-issuance実装監査

> **位置づけ**: Candidate191 Standard14コスト機序失敗の修正版／静的検証済み／評価未開始

## 結論

Candidate192 `the-caption-3ce91a4-consumer-bound-coissuance-r1`を、Candidate191の開始観測と変更前共同発行の退行だけを修正する新identityとして作成した。Candidate191の品質結果と機序失敗は診断証拠として保持し、既存bundle、resultまたはratingを上書きしていない。

一変更軸は`DISPATCH_ADMISSION`である。repository evidenceの許可だけで発行可能とはせず、requested resultを消費してtarget、permission、methodまたはstop conditionを変え得るbind済みnonterminal operationを要求する。発行可能なinvocation間に相互のdecision boundaryがなければ、operation identityやresult格納先が別でも同じmodel stepから発行する。

## Candidate作成前ゲート

1. 基準promptはCandidate191 `the-caption-3ce91a4-explicit-review-operation-applicability-r1`とする。
2. 基準状態の最短正常経路は、開始identity resultが許可済みreadのtargetまたはpermissionを変えない場合に、identity確認とreadを同じmodel stepから発行する経路である。
3. 保存trace上の誤経路は、Standard14の9ケース、45 run中44件で変更前model stepが一つ増えた経路である。A01では5件中4件がresult consumerのない開始identity commandを発行した。
4. TaskSpecとrepository authorityは必要な成果、開始状態、許可済みreadを固定していたが、Candidate191本文ではoperation分離後の発行責務と、consumerのない開始観測禁止の優先関係が一つのownerへ固定されていなかった。
5. 追加するpredicateは`invocation_consumer_ready`と、それを入力にする`coissuance_ready`から成る一つのdispatch admissionである。
6. このpredicateはconsumerのない開始観測と、相互非依存invocationの間に作られた追加model result roundを消す。
7. 新たに増える判断は、requested resultのconsumerが実在するかと、ready invocation間に双方向のdispatch dependencyがあるかの二点である。新しいrepository evidence、review、producer、result kindまたはexceptionは増やさない。
8. 品質維持は、まず保存traceで退行を観測したStandard14の9ケースと、開始identityが実際に後続operationを禁止し得る対照経路に限定して確認する。対象外ケースを一律に増やさない。
9. consumerのない開始観測、相互非依存invocationの直列化、真正dependencyを越えた共同発行、Score 4未達または既存review terminalの退行を一件でも観測した場合は停止する。

## 方向を変える具体的反例

### consumerなし開始観測

required outcome valueが未固定でclarificationが唯一のterminalであるとき、開始identity resultはclarificationのtarget、permission、methodまたはstop conditionを変えない。開始状態がTaskSpecに書かれているだけでcommandを許すと、結果consumerのない観測を発行して一round増やせる。したがって開始状態の明示をconsumerとみなさない。

### 真正dependencyがある観測

開始identity driftがread自体を禁止する、またはread target・permissionを変える場合、identity resultとreadは相互非依存ではない。token削減を目的に無条件共同発行すると禁止readを実行するため、`dispatch_dependency=true`では別stepを維持する。

### 個別result contract

共同発行は複数観測を一つのcompound invocationへ統合することではない。aggregate failureで個別successを失う観測は、個別tool callのまま同一model stepから発行する。これによりCandidate176で確認したresult真正性の問題を再導入しない。

三反例はtarget、permission、methodまたはstop conditionを変える追加反例を生じさせない。完全性は試験で確認する。

## 実装対応

- `EVIDENCE_ADMISSION`はpredicate stateとrequested resultの証拠資格を引き続き所有する。
- 新しい`DISPATCH_ADMISSION`だけが、資格を得たinvocationの発行可否と同一model stepへの共同発行を所有する。
- `RESULT_EFFECT`はresultの局所効果とdependencyを所有し、発行順序の所有を`DISPATCH_ADMISSION`へ移した。
- `OWNER_ROLE`、review適用、current/prior result admission、terminal、validationおよびrecoveryは変更していない。

## bundle identity

- prompt identity: `the-caption-3ce91a4-consumer-bound-coissuance-r1`
- bundle SHA-256: `1d5770dec7f508c2c6999ed8bff934779efb94f82fb17358da0a63e2098d0f81`
- root `AGENTS.md` SHA-256: `228b1702cdf9820954e96b8a6c59211aa1b61f1e024652bcca2b8dc32f9c4f94`
- direct parent: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- changed target: `AGENTS.md`だけ
- evaluation status: `not_evaluated`

## 状態

bundle identity、非変更target一致、20条項順、`DISPATCH_ADMISSION`のconsumer・dependency・共同発行predicate、独立`OWNER_ROLE`、current/prior result admissionおよび歴史的identity不在を専用試験で確認した。実装時の全repository回帰は`1179 passed, 1835 subtests passed`である。

後続の[対象Standard14 N=5](../evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md)は50 / 50 validかつScore 4だったが、A01 consumerなし開始identityが2 / 5、退行8ケースのidentity/read共同発行が1 / 40だった。静的なpredicate存在は確認できても発行集合を挙動拘束できなかったため、Candidate192を停止する。評価artifact追加後の全repository回帰は`1182 passed, 1835 subtests passed`である。

`candidate192_created / static_verification_passed / targeted_standard14_quality_passed / mechanism_failed / stopped / not_adopted / not_released / not_projected`
