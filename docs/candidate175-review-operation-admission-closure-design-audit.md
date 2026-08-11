# Candidate175 review operation admission closure設計監査

## 結論

Candidate175の改訂設計について、最初の設計監査では一般修正を必要とする具体的反例が閉じた。その後の実装監査で、一般`PRODUCER`への適用範囲が設計文書と一致しない反例が見つかったため、設計範囲を再度開いて監査する。

監査producerにはCandidate175設計、一般仕様、Candidate173のprompt本文、適用中repository instructionだけを許可した。評価case、fixture、oracle、rating、既存評価result、会話履歴は渡していない。

## 初回監査

初回設計では二つの反例が成立した。

1. 独立reviewに専用producer bindingがない場合、rootへfallbackする解釈とrequired reviewを起動しない解釈が両立した。
2. 許可fieldまたはprovenance receiptが欠けて`semantic_projection_valid=false`になった場合、`unavailable`への遷移が定義されずnonterminal経路が残った。

設計を次のように修正した。

- `design_review_admission_state=required`では独立producerを常に要求する。
- 専用review contract内のproducer execution identityを、一意なreview operation identityへ対応できる場合だけ有効なbindingとする。
- binding不足時はrootへfallbackせず、operation作成前に`unavailable`とする。
- permission、operation仕様、producer binding、semantic projectionのいずれかが不成立なら、全て`unavailable`へ写す`review_dispatch_state`を追加する。

## 再監査

再監査では、permissionが`allowed`または`denied`へ正規化できない場合にdispatch状態が未定義になる反例が残った。

設計を、TaskSpecが当該review operationを明示的かつ一意に許可した場合だけtrueになる`review_permission_allowed`へ修正した。明示deny、欠落、未知、競合、形式不正、operationへのbind不能はすべてfalseとし、operation作成、producer binding、packet構築・配送より前の`unavailable`へ写した。

## 最終監査

最終監査は`no_counterexample_found`だった。`design_review_admission_state=required`の入力は次の三経路へ一意に分かれる。

```text
permission非許可
  -> unavailable

permission許可 ∧ (operation仕様不足 ∨ producer binding不足 ∨ projection不成立)
  -> unavailable

permission許可 ∧ operation仕様完成 ∧ producer binding完成 ∧ projection成立
  -> dispatch
```

次の9条件もすべて通過した。

1. 禁止fieldに実値があっても配送しない。
2. 禁止fieldが空またはnullでも配送しない。
3. source全体を渡して無視を指示する経路を拒否する。
4. manifest descriptorが固定済みなら、target missingを理由にrootがreviewを差し止めない。
5. ownerまたはcriterionの語だけではworkerを起動しない。
6. 専用producer bindingが一意なら、そのidentityのworkerを起動する。
7. packet projectionだけで判定可能なsourceをreviewerが再読しない。
8. permission非許可ではoperation、producer、packetを作らない。
9. 許可fieldまたはprovenance不足をrootが補完せず`unavailable`にする。

Candidate173の`PRODUCER`、`OWNER_ROLE`、`ROOT`、`CONTEXT`、`DESIGN_ADMISSION`との矛盾、rootによるreview代行、required reviewの起動漏れ、不要reviewの誤起動、禁止情報配送、case固有分岐の具体的反例は確認されなかった。

## 実装範囲の再監査

最初の実装監査では、一般`PRODUCER`と`OWNER_ROLE`も変更した実装に対して、設計文書がDESIGN_ADMISSION外は既存制御に従うとのみ記載していたため、変更範囲の不一致が確認された。

Standard14で観測されたowner語列からの誤起動も同じreview operation admission軸で扱うため、一般producer指定の「明示」を次の肯定条件へ精密化した。

```text
explicit_producer_execution_required :=
  TaskSpecのcriterion ownerとは別のfieldまたは文が
  producer execution identityを対応operation identityへ直接かつ一意にbind
```

特定field名またはschemaは要求しない。したがって従来の正当な自然言語指定を維持し、identityを指定しないowner、criterion、pass conditionまたは説明文の役割語だけを除外する。DESIGN_ADMISSION required reviewでは、この一般条件に加えて専用review contractと一意なreview operation対応を要求する。

再監査は`no_counterexample_found`だった。正当な自然言語指定の保持、owner語列だけの非起動、一般operationでのroot既定、required reviewでのroot fallback禁止、先の9条件、既存制御との整合を確認した。

## 状態境界

- design audit: `passed_after_scope_reaudit`
- candidate implementation: `created / implementation_reaudit_passed`
- evaluation: `not_started`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`
