# Evaluations

prompt比較用のcase、execution profile、再現可能なresultを管理する。

- `targets/`: 評価対象repositoryごとのinstance台帳とdescriptor
- `cases/`: task入力、fixture contract、oracle / grader境界
- `profiles/`: model、Agent、environment、反復、順序、比較条件
- `rating-contracts/`: quality scoreのrevisionとscore `4`の必要evidence条件
- `results/`: profileとartifact identityへbindした結果
- `examples/`: 現行schemaとfixture境界の説明用artifact

ローカル試行やidentity不一致のrunを正式結果へ昇格させない。

## Minimal four-layer CLI

`scripts/evaluation_loop.py`は、各Layerを別subcommandとして実行する。

1. `freeze-set`: 評価セットとfixtureをcycleへ固定する
2. `bind-coverage`: 対象試験で発行・登録するcaseとiterationを実行前に固定する
3. `prepare-comparison-layer1`: 保存済み基準resultのLayer 1を検証し、比較cycleをその実体から生成する
4. `preflight-comparison`: candidate profile、全capsule、global planを基準resultへ照合し、実行許可receiptを固定する
5. `run`: 外部Run capsuleのadapterを実行し、成果、all-agent token、時間を記録する
6. `rate`: 現行rating contractのevidence必要条件を確認し、blindなrun IDへ0〜4のscoreと短い事実根拠を記録する
7. `record-result`: 1 prompt setの3 KPI、中央値、除外attemptをappend-only registryへ記録する

`query-results`は保存resultを任意件取得し、`compare`は互換条件とtoken accounting revisionを満たす2件以上からread-only viewを作る。比較対象を固定pairとして保存せず、既存resultを再利用して不足するprompt set / slotだけを実行する。

評価set、Run capsule、評価case本体はこの基盤に含めず、外部から渡す。executorは`EVAL_CASE_FILE`と`EVAL_RUN_CAPSULE_FILE`から可変入力を読み、root agentと全SA sessionを合算した`total_tokens`をaccounting identityとともに`EVAL_USAGE_FILE`へ書く。客観的証跡から外部要因またはusage欠損を検出した場合だけ`EVAL_RUN_STATUS_FILE`へ除外statusを書き、基盤はraw artifactを保持して有効iteration数から除外する。token内訳などの詳細データはopaqueな`EVAL_EXTENSION_DIR/<feature>/`へ分離する。Layer出力とregistry resultは既存fileを上書きしない。基盤の出力はKPI情報だけであり、`winner`、promptの改善、採用、release判断は行わない。

利用手順は[`docs/evaluation-loop-manual.md`](../docs/evaluation-loop-manual.md)を参照する。
