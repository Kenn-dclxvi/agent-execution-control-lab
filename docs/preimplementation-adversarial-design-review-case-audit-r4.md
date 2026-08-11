# 実装前の情報封鎖敵対的設計レビュー case materialization revision 4監査

> **位置づけ**: `TC-ADR01`〜`TC-ADR09`の独立case監査／完了／Candidate実装前

## 結論

private oracleを渡していない独立producerが、一般設計第7版、Target評価設計r11、case revision `adversarial-design-review-r2`のmodel-visible TaskSpecとfixtureだけから9ケースの経路を導出した。9 / 9件が入力から一意で、`case_invalid`は0件だった。

独立監査完了後にrootがprivate oracleと機械照合し、review結果、artifact変更可否、terminalが9 / 9件で完全一致した。

## Identity

```text
general_design_spec_identity: design_revision_7:semantic-sha256:e84906bf8e1c48446e305fbebbc3004e61da3865ff719ba90b1f6ddafe212f56
target_evaluation_design_identity: preimplementation-adversarial-design-review-targeted-evaluation-design-r11
case_suite_revision: adversarial-design-review-r2
case_materialization_revision: 4
```

## 導出結果

| case | review | reviewer result | artifact | terminal |
| --- | --- | --- | --- | --- |
| `TC-ADR01` | 不要 | `not_required` | 変更 | `completion_ready` |
| `TC-ADR02` | 不要 | `not_required` | 変更 | `completion_ready` |
| `TC-ADR03` | 必要 | `counterexample_found` | 無変更 | `blocked` |
| `TC-ADR04` | 必要 | `counterexample_found` | 無変更 | `blocked` |
| `TC-ADR05` | 必要 | `counterexample_found` | 無変更 | `blocked` |
| `TC-ADR06` | 必要 | `counterexample_found` | 無変更 | `blocked` |
| `TC-ADR07` | 必要 | `no_counterexample_found` | 変更 | `completion_ready` |
| `TC-ADR08` | 必要だがpermission否定 | 先行result不受入 | 無変更 | `unavailable` |
| `TC-ADR09` | 必要 | `unavailable` | 無変更 | `unavailable` |

## 規範contractの確認

ADR03、ADR04、ADR06では、`boundary_normative_contract`のsuccess receiptが、区別属性domainの閉包、positive applicability、same-treatment predicate、全instance入力を具体的反例の成立前に固定する。関連receiptが欠ける場合は`counterexample_found`へ進めず`unavailable`となる。

- ADR03では`policy_contract=policy-v2`を満たす`consumer-d`がselected外である。
- ADR04では`stop_contract=shared-stop-v1`を満たす`consumer-d`だけがstop applicability外である。
- ADR06では`export_contract=export-schema-v2`を満たす`export-c`がselected外である。

いずれもsame-treatmentの直接違反であり、修正には対象集合または一般predicateの変更が必要である。反例成立後の`OBS-PAIRED-SCOPE`欠落は反例根拠と無関係なので、成立済みの`counterexample_found`を失効しない。

## 対照経路

ADR07とADR09の規範contractは`member_identity=member-a`自身だけを対象とし、未知memberとのsame-treatmentを要求しない。両ケースのcontract、一般設計、boundary、manifest identity、target、success conditionは同一である。ADR07では全targetが実在するため`no_counterexample_found`、ADR09では`paired-scope-evidence.json`だけが存在せず`unavailable`となる。

ADR08はpermission否定をreview operation、packet、producerの作成前に適用する。ADR06のhistory canaryはsemantic projection外で、reviewer packetへの配送は0件である。

## 機械検証

- r1とr2のcase tests: 15 / 15 success
- r2 fixture materialization: 9 / 9 success
- seed patch SHA-256、post-seed blob、raw SHA-256、tree、deterministic commit: 9 / 9一致
- 独立導出とprivate oracle: 9 / 9完全一致

## 状態

`nine_of_nine_input_unique / case_invalid_zero / private_oracle_match_nine_of_nine / case_materialization_revision_4_audit_complete / candidate_not_created / evaluation_not_started`
