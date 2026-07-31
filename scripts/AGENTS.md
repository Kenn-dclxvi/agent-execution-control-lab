# scripts instructions

`scripts/`の指示は、評価基盤の実行コード、adapter、collector、schema処理を扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。

prompt bundleを生成・合成・展開するscript（`export_prompt_bundle.py`、`materialize_prompt_route.py`、`run_codex_evaluation.py`など）は、次の公開contractを保つ。詳細規則は各正本を参照し、scripts/へ複製しない。

- bundle形式、manifest、identity、at-rest格納、overlayの正本は`docs/prompt-file-bundle.md`。prompt identity、`bundle_sha256`、`files` entry、格納形式(`storage_format`)の不変条件を保つ。
- baseline / candidate / route / releaseのlifecycleとimmutable分離は`prompts/AGENTS.md`と`docs/repository-contract.md`。既存bundleをin-placeで改訂しない。
- model-visible / model-invisible境界、evaluation compatibility、4 Layer / 3 KPIの境界は`docs/prompt-comparison-workflow.md`と`evaluations/AGENTS.md`。overlayでmodel-invisible情報をworkspaceへ流入させない。

- `scripts/evaluation_loop.py`をevaluation foundation v3の固定点として扱う。
- `scripts/atomic_run_registry.py`をcount-free atomic保存・選択・集計の固定点とする。poolへrun member一覧または`N`を保存せず、要求件数はdispatch plan、使用run集合はselection receiptへだけ固定する。
- 新しいpromptのrunが0件でも、互換な基準poolから`seed-pool`でcase別実効条件を固定してから不足runを計画する。空pool作成のために架空runを登録しない。
- 再現可能な不具合または明示要件なしに、Layer、KPI、出力schemaを拡張しない。
- 書込処理はappend-onlyを維持する。
- 既存artifactを上書きしない。
- executor、evidence collector、quality rating、KPI comparisonの責務を混ぜない。
- tokenを推定しない。
- 全session usageが取得できないrunは、外部計測失敗として除外する。
- raw log、secret、credentialを公開artifactへ含めない。
- shell commandやfixture pathを文字列連結によって暗黙変更しない。
- schema変更時は既存revisionを保持し、新しいschema revisionを追加する。
- 実装コードの変更と、評価対象promptの変更を同一変更へ混ぜない。
- scripts変更では、対応するunit testを追加または更新する。
- temporary directoryや評価用workspaceをrepository内へ残さない。
