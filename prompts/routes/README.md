# prompt route索引

## 結論

共通プロンプトの全文を複製せず、特定routeでだけmodelへ見せる小さな差分を置く。

route deltaは単独のプロンプトではない。base prompt identity、base bundle hash、完全一致させる外部route facts、挿入位置、一つのmodel-visible差分を固定する。

`scripts/materialize_prompt_route.py`はbase full bundleとroute deltaから、評価または実行時に一枚の解決済みfull bundleを生成する。非一致routeはbase prompt identityを選び、deltaをmodelへ渡さない。

解決済みfull bundleはmodel-visible入力の再現と不変の評価のために保存してよい。保守対象の二つ目の全文のsourceとして編集しない。baseまたはdeltaを変更する場合は新しいidentityとrevisionを作る。

現行routeは[`fixed-evidence-review-r1.json`](fixed-evidence-review-r1.json)である。設計と対象試験は[`Candidate63設計`](../../docs/candidate63-fixed-evidence-route-projection-design.md)と[`Candidate43 / Candidate63 F10 N=5`](../../evaluations/results/candidate43-candidate63-fixed-evidence-route-projection-f10-n5_2026-07-22.md)に置く。
