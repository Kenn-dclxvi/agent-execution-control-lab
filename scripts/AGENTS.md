# scripts instructions

`scripts/`の指示は、評価基盤の実行コード、アダプタ、コレクタ、schema処理を扱う。ルートの`AGENTS.md`の共通規則に加えて、この領域規則を適用する。

プロンプトバンドルを生成・合成・展開するスクリプト（`export_prompt_bundle.py`、`materialize_prompt_route.py`、`run_codex_evaluation.py`など）は、次の公開contractを保つ。詳細規則は各正本を参照し、`scripts/`へ複製しない。

- バンドル形式、マニフェスト、識別子、保存時の格納、オーバーレイの正本は`docs/prompt-file-bundle.md`。prompt identity、`bundle_sha256`、`files`エントリ、格納形式(`storage_format`)の不変条件を保つ。
- baseline / candidate / route / releaseのライフサイクルと不変性による分離は`prompts/AGENTS.md`と`docs/repository-contract.md`。既存バンドルをその場で改訂しない。
- model-visible / model-invisible境界、評価の互換条件、4 Layer / 3 KPIの境界は`docs/prompt-comparison-workflow.md`と`evaluations/AGENTS.md`。オーバーレイでmodel-invisibleな情報をワークスペースへ流入させない。

- `scripts/evaluation_loop.py`をevaluation foundation v3の固定点として扱う。
- `scripts/atomic_run_registry.py`をcount-freeなatomic保存・選択・集計の固定点とする。プールへrunのメンバー一覧または`N`を保存せず、要求件数はdispatch plan、使用run集合はselection receiptへだけ固定する。
- 新しいプロンプトのrunが0件でも、互換な基準プールから`seed-pool`でケース別の実効条件を固定してから不足runを計画する。空のプール作成のために架空のrunを登録しない。
- 再現可能な不具合または明示要件なしに、Layer、KPI、出力schemaを拡張しない。
- 書込処理はappend-onlyを維持する。
- 既存アーティファクトを上書きしない。
- executor、evidence collector、quality rating、KPI comparisonの責務を混ぜない。
- トークンを推定しない。
- 全session usageが取得できないrunは、外部計測失敗として除外する。
- 生のログ、シークレット、クレデンシャルを公開アーティファクトへ含めない。
- shell commandやfixture pathを文字列連結によって暗黙に変更しない。
- schema変更時は既存revisionを保持し、新しいschema revisionを追加する。
- 実装コードの変更と、評価対象プロンプトの変更を同一変更へ混ぜない。
- `scripts/`の変更では、対応するユニットテストを追加または更新する。
- 一時ディレクトリや評価用ワークスペースをリポジトリ内へ残さない。
