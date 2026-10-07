# 比較条件の識別方法の見直し（設計案）

2026-10-08。状態：利用者の確認済み。実装済み（範囲は末尾の「実装の範囲」を参照）。

## 解決したい問題

比較条件（`comparison_conditions`）は、プロンプト以外の条件が同じ結果同士だけを比べるための仕組みである。今は、条件の全項目をそのまま互換キーのハッシュに入れている。その結果、計測の中身に影響しない違いでも比較できなくなり、次の問題が起きた。

- **評価コードのSHA-256**（`executor_parameters.time_recording.code_sha256`）：評価コード十数ファイルのハッシュが条件に入っている。起動時照合の見直しのような、KPIに影響しない変更でも互換キーが変わる。C280 lowを測るときは、比較のために古いコードを`git archive`で写して使う必要があった。
- **組み込みプラグインと契約プラン**：アカウントの違いだけで、作業が正常に終わった222回が除外された（[起動時照合の方針](claude-runtime-surface-plugin-policy.md)）。
- **申告と実際のずれ**：条件の多くは、プロファイルに書いた「予定」である。lowの2系列では、プロファイルの発行方式が`global_queue`のまま、実際は`wave_barrier`で発行していたが、どの照合でも検出されなかった。
- **場所の違い**：実行ファイルのパスや設定フォルダのパスも条件に入っている。中身が同じでも、置き場所を変えるだけで比較できなくなる。

比較できなくなると、基準側を流し直すことになり、トークンと時間を使う。逆に、本当に一致すべき条件（実際にモデルへ渡した課題文など）は、コードのハッシュ値で間接的にしか守られていない。

## 原則

互換キーに入れるのは、結果の値を変えうる条件だけにする。それ以外は、後から追えるように記録として残し、互換キーには入れない。

結果の値を変えうる条件は、次の3種類である。

1. **モデルに見えるもの**：課題文、プロンプト本文（実験変数）、対象リポジトリとfixture、コマンド記録の手順の文面
2. **エージェントの動き方を決めるもの**：モデル、推論設定、権限、Claude Codeの版と実行ファイルの中身、ツール、エージェント、動きを変えるプラグイン、MCP、skill、設定の読み込み元、プロセスの環境変数、記憶の扱い
3. **KPIの数え方**：トークンの数え方の版、経過時間の記録規則の版、採点契約とその証拠の版、外部失敗の扱い

条件は、できるだけ申告ではなく観測で確かめる。実際に渡した課題文のSHA-256は、各runの`claude-adapter/execution.json`に`task_sha256`として既に記録されている。

## 項目ごとの扱い（案）

| 項目 | 今 | 案 | 理由 |
| --- | --- | --- | --- |
| `task_spec`、`target_repository_ref`、評価セット、fixture | 互換 | 互換 | モデルに見える |
| 各runの`task_sha256`（ケースごと） | 記録のみ | **互換（観測値で照合）** | 実際にモデルへ渡した文面。コードのハッシュ値の代わりに、課題文の一致を直接確かめる |
| `command_protocol_text_revision`、`command_evidence_protocol` | 互換 | 互換 | 課題文と採点の証拠を変える |
| `model`、`reasoning_effort`、`permission` | 互換 | 互換 | 動き方を決める |
| Claude Codeの`version_output`、`executable_sha256` | 互換 | 互換 | 動き方を決める |
| `tools`、`agents`、`mcp`、`skills`、`setting_sources`、`flag_settings`、`process_environment`、`auto_memory`、`session_mode` | 互換 | 互換 | 動き方を決める |
| `plugins` | 互換（全件） | 互換（動きを変えるものだけ） | 組み込みの補助プラグインは動きを変えない |
| `token_accounting`、`time_recording.contract`、`quality_rating`の契約と証拠の版、`adapter_owned_teardown`、`external_failure_policy` | 互換 | 互換 | KPIの数え方 |
| `time_recording.code_sha256`（評価コードのハッシュ） | 互換 | **記録のみ** | 必要な一致は、課題文の観測値とKPIの版で直接確かめる |
| `executable`のパス、`config_dir`のパス、`code_signature_team_identifier` | 互換 | 記録のみ | 置き場所と署名者。中身は`executable_sha256`で確かめる |
| `authentication` | 互換 | 記録のみ | ログイン方式やプランはモデルの動きを変えない。APIキーの有無だけは、課金の経路の記録として残す |
| `python_version`、`runtime_identity_sha256`（評価側のPython環境） | 互換 | 記録のみ | エージェントではなく評価側の環境。KPIの数え方は版で確かめる |
| `schedule_policy`、`max_attempts`、`monitor_interval_seconds`、`duration_hint_method` | 互換 | 記録のみ（観測値で残す） | 発行の仕方。経過時間には影響しうるので、`max_workers`と同じく、比較の時に層別して示す |
| `repetition_condition.iterations`、`max_workers` | 記録のみ（既存） | 記録のみ | 既存の扱いを維持 |

## コードのハッシュ値を外す代わりの守り

コードのハッシュ値を外すと、KPIの数え方や課題文の作り方を変えたのに、版を上げ忘れる危険が生まれる。次の2つで防ぐ。

- **課題文**：比較のときに、ケースごとの`task_sha256`が両方の系列で一致することを確かめる。これは観測値なので、版の上げ忘れに左右されない。
- **KPIの数え方**：トークンの集計、経過時間の記録、採点の各処理について、保存済みの小さな入力に対する出力を固定した試験を置く。出力が変わる変更は、対応する版（`token_accounting.revision`、`time_recording.contract`、採点契約）を上げない限り、試験が通らないようにする。

## 既存の結果との関係

- 既存の結果、プロファイル、互換キーは書き換えない（追記専用の原則）。
- 新しい互換キーは、新しいschemaの版として追加する。既存の結果にも条件の全項目が保存されているので、新しい規則での互換キーは、保存済みの条件から計算できる。既存の結果同士や、既存と新規の結果を、新しい規則で比べる「導出した比較」を作れる。
- ただし、既存の結果のうち`task_sha256`が保存されていない系列は、課題文の一致を観測で確かめられない。その系列は、旧来どおりコードのハッシュ値の一致を条件とする。
- 既存の比較結果の判断は変えない。新しい規則による比較は、別の比較の記録として追加する。

## 変更が必要なもの

- `scripts/evaluation_loop.py`と`scripts/atomic_run_registry.py`：互換キーの計算を、上の分類に基づく新しいschemaへ分ける（既存のschemaは残す）。比較時に`task_sha256`の一致を確かめる処理を加える。
- `scripts/run_claude_evaluation.py`、`scripts/run_codex_evaluation.py`：発行方式などを、申告ではなく観測値として記録する。
- 試験：互換キーの分類の試験と、KPIの数え方の出力を固定する試験を加える。
- 規則の文書：`evaluations/AGENTS.md`の「互換条件」と「比較試験の実行前ゲート」、`docs/prompt-comparison-workflow.md`、`docs/evaluation-loop-manual.md`を更新する。ルートの`AGENTS.md`の`PROMPT_ONLY_COMPARISON`は、守る対象（ケース、fixture、TaskSpec、モデル、推論設定、Agent/runtime/CLI、権限、executorの挙動、トークンの数え方）を変えないので、文面の更新は不要と考える。

## 決めていただきたいこと

1. 上の表の分類でよいか。特に、契約プランとログイン方式、評価側のPython環境、発行方式を「記録のみ」にしてよいか。
2. 既存の結果を新しい規則で比べる「導出した比較」を作れるようにするか。作る場合、起動時照合の見直しの前に測ったC280 low・C291 lowと、見直しの後に測る系列のように、コードのハッシュ値だけが違う組み合わせも、`task_sha256`の一致を確かめたうえで比べられるようになる。
3. 進め方。この設計記録を先にコミットし、実装は別のPRに分けることを提案する。

## 実装の範囲（2026-10-08）

利用者は、上の3点を設計案どおりとした（分類はこの表のとおり、導出した比較を作る、実装は別のPR）。

- 分類：`scripts/comparison_identity.py`。Claudeアダプターの起動時照合も、組み込みプラグインの判定をここから使う。
- 発行前の照合：`preflight-comparison --compatibility-rule effective-v1`。既定は従来の`exact`。
- 保存済みの結果の比較：`compare-effective`。課題文の一致を`task_sha256`で確かめる。
- KPIの数え方の固定：`tests/test_kpi_revision_guard.py`。Claudeのトークン集計と経過時間の記録を対象にした。Codexのトークン集計と採点契約は、既存の試験と契約のSHA-256で守っており、この版で固定表には加えていない。
- 対象外（当初）：atomic run経路は、最初の実装では従来の完全一致のままとした。
- atomic run経路（追加実装）：`seed-pool --compatibility-rule effective-v1`で`run-pool/v2`を作る。既存の`run-pool/v1`とrun記録は書き換えず、保存済みの条件から新しいキーを計算して所属を判定する。新しく登録するrunには、記録元に課題文の`task_sha256`を残す。アダプターが発行方式を観測値として記録する変更も、この版では行っていない。発行方式は、並列実行の要約（`parallel-run/summary.json`の`schedule_policy`）に観測値として残っている。
