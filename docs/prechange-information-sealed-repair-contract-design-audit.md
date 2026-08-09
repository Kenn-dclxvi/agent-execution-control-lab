# 変更前の情報封鎖レビューによる修正契約 設計監査

> **位置づけ**: 破棄済み旧設計に対する履歴監査／現行設計の監査結果ではない
>
> 監査対象の旧仕様は破棄済みである。現行設計は[`preimplementation-information-sealed-adversarial-design-review-spec.md`](preimplementation-information-sealed-adversarial-design-review-spec.md)を参照する。

## 結論

[修正契約仕様](prechange-information-sealed-repair-contract-spec.md)は、監査で検出した三つの内部矛盾を同じ文書変更で解消した。修正操作の状態遷移、担当の一回限りの結び付け、入力封鎖、結果受入れ、C147の`implementation_bound`と検証への接続、変更後レビューの停止条件は、評価ケース設計に必要な範囲で一意になった。

したがって、仕様の設計監査は`passed_after_correction`とする。次に許可されるのは、実装を参照しないtargeted評価の設計と固定である。Candidateバンドルの作成は、修正操作に対する保存済みの誤経路を結び付けるまで開始しない。

## 監査対象

- `docs/prechange-information-sealed-repair-contract-spec.md`
- Candidate166 `the-caption-3ce91a4-prior-evaluation-review-admission-r1`
- Candidate147 release `the-caption-3ce91a4-result-effect-scope-release-r1`
- `docs/prompt-control-design-principles.md`
- root、`docs/`、`prompts/`、`evaluations/`、`tests/`の適用中`AGENTS.md`

## 検出した問題と修正

### 1. 受入れ済み結果が生成元照合を自己失効させる

元の仕様では、`repair_contract_required`に「受け入れ可能な修正契約が存在しない」を含め、`repair_contract_required=false`のときは担当を`none`としていた。結果を受け入れた直後に式を再評価すると担当が`none`になり、結果の生成元を元の担当へ照合できない。

`repair_contract_required`と`bound_repair_contract_producer`をadmission時に修正操作の識別情報へ一度だけ結び付け、結果受領後に再評価しない形へ修正した。生成元は結果本文の自己申告ではなく、実行環境の識別情報で照合する。

### 2. `no_repair_required`と修正必須条件が矛盾する

元の`repair_operation_ready`はTaskSpecが是正そのものを必須成果とする場合に限定していた。そのままでは、現在の成果物が判定条件を満たすとする`no_repair_required`がTaskSpecと矛盾する。

操作の必須成果を、欠陥または意味不整合の有無を確定し、存在する場合に是正することへ修正した。機械根拠だけで現在内容が条件を満たす場合も`no_repair_required`へ閉じ、`not_applicable`は「機械根拠だけで修正必要と全修正後条件を確定できる」場合に限定した。

### 3. clean文脈と変更後レビューの受入れ条件が不足する

元のconsumer gateは独立レビューの起動だけを明記し、clean文脈で同じ判定を行う`root`への適用が曖昧だった。また、変更後レビューは担当分離と停止を定めていたが、結果の生成元と形式を受け入れる条件がなかった。

consumer gateを`repair_contract_consumer_ready`として両担当に適用し、実際の起動は結び付き済み担当に限定した。変更後レビューはCandidate166の`RESULT_ADMISSION`に生成元照合を委ね、結果の三区分と、不正な結果を`root`が代行しない停止条件を追加した。

## 不変条件の照合

| 論点 | 根拠 | 判定 |
| --- | --- | --- |
| 同一操作の担当 | admission時に`bound_repair_contract_producer`を一件結び付ける | pass |
| 先行評価の効果 | 同じ修正判定条件の担当切替だけに限定 | pass |
| 入力封鎖 | 許可入力と禁止入力を限定列挙し、中立な場所情報だけ許可 | pass |
| `root`の代行禁止 | 生成元または形式不明を`unavailable`または`blocked`へ閉じる | pass |
| C147への接続 | `ready`だけでは変更できず、別に`implementation_bound`を要求 | pass |
| result effect | `implementation_binding / artifact_change / change_dependent_validation`だけに限定 | pass |
| 変更後レビュー | 非機械的な修正後判定が残る場合だけ起動し、自動再修正しない | pass |
| 実行環境依存 | 必要な意味だけを固定し、ツール名と返却項目名は固定しない | pass |

## Candidate作成前に残るゲート

Candidate作成規律は、保存済みトレースで確認した一つの誤経路を作成前に要求する。既存のCandidate164〜166系で成立したのは、誤った先行評価から読み取り専用レビューの担当を分離する機構である。HR03 r1の品質はoracleを一意に導けないため未判定であり、修正の要否と修正後条件を変更前に誤る修正操作の誤経路はまだ保存されていない。

そのため、次のtargeted評価設計でclean / perturbedの同一fixture対を実装より先に固定する。その後、直接の親であるCandidate166を問題資格確認として実行し、perturbed側で先行評価が修正判定へ混入する誤経路を観測できた場合だけCandidate作成へ進む。観測できなければ、新しいprompt制御を作らず停止する。

## 状態

`audited / three_internal_conflicts_corrected / specification_passed_after_correction / targeted_evaluation_design_allowed / candidate_not_created / evaluation_not_started`
