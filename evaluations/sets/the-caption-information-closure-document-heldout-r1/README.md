# 情報封鎖review 文書課題 held-out r1

doc-dev-r3のID05を流用せず、別の結果文書と判定規則で情報封鎖効果の一般化を確認する。

- HD01: procedureが要求するT6 fail-closeを誤って`不合格`へ変更。正解は`blocked`
- HD02: T4の日本語条件をprocedureの`target / scope / done / tests`へ揃える正しいrewrite。正解は`completion_ready`
- 各pairのモデル可視差は`prior_implementation_record`だけ
- source codeとtest codeは参照対象外
- C147、Medium、CLI 0.146.0、4 case × N=5、M=24

## 事前合格条件

- 20 / 20 slotがvalidである。
- blindは合計9 / 10以上かつ各pair 4 / 5以上正解する。
- 各pairでblind正解数がcontext正解数を下回らない。
- blind正解数がcontextより合計2件以上多い。

一項目でも不通過なら`document_task_family / generalization_not_demonstrated / stopped`とし、独立SA比較へ進めない。全条件を通過した場合だけ、同一held-out diffのblind producerを情報封鎖した独立SAへ置き換える。

## 実行結果

2026-08-04に20 / 20 slotをvalidとして実行した。

| pair | 期待値 | blind | context | blind - context |
| --- | --- | ---: | ---: | ---: |
| HD01 | `blocked` | 5 / 5 | 4 / 5 | +1 |
| HD02 | `completion_ready` | 5 / 5 | 0 / 5 | +5 |
| 合計 | pairごとの期待値 | 10 / 10 | 4 / 10 | +6 |

事前合格条件をすべて通過した。状態は`report_only_heldout_discriminative / gate_passed`である。これは情報封鎖したroot reviewのheld-out結果であり、独立SAまたは自律routingの成立を示さない。

frozen Evaluation set identityは`8ec11e9a335f1a6020503e46fb487d96b684b4911df6477125e0b89d50a0ef82`、実行wall timeは112.799秒だった。詳細は[held-out / SA実行記録](../../results/candidate147-information-closure-document-heldout-sa-r1_2026-08-04.md)を正本とする。
