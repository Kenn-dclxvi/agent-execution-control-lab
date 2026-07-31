# click profiles

target instance `click`のevaluation profileを置く。`M`は指定がない限り24へ固定する。段階ごとのCase / N / B / Mは[`docs/public-target-selection-phase0.md`](../../../../docs/public-target-selection-phase0.md)の「Phase 1の実行設定」を正本とする。

2026-07-27以降の新規通常比較はreasoning effort `medium`を運用基準とする。既存`high` profileとresultは履歴として保持し、reasoningが異なるresultを同一comparisonへ混ぜない。

## 現在のprofile

| profile_id | set | Case | N | B | M | 状態 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [`click-control-free-f01-only-global-m24-n1-r1`](click-control-free-f01-only-global-m24-n1-r1.json) | `click-f01-only-r1` | 1 | 1 | 1 | 24 | execution前停止（token accounting宣言不足、result 0件） |
| [`click-control-free-f01-only-global-m24-n1-r2`](click-control-free-f01-only-global-m24-n1-r2.json) | `click-f01-only-r1` | 1 | 1 | 1 | 24 | P1-a完了（valid 1 / 1、score 4） |
| [`click-control-free-f01-only-global-m24-n5-r1`](click-control-free-f01-only-global-m24-n5-r1.json) | `click-f01-only-r1` | 1 | 5 | 3 | 24 | P1-b / P1-c完了（3 result、valid 15 / 15、全件score 4） |
| [`click-control-free-f02-only-global-m24-n3-r1`](click-control-free-f02-only-global-m24-n3-r1.json) | `click-f02-only-r1` | 1 | 3 | 1 | 24 | 完了（valid 3 / 3、全件score 4） |
| F03 / F04 / F05 / F05-OS / F06の各`only-global-m24-n3-r1` | 対応するonly set | 各1 | 3 | 1 | 24 | 完了（各3 / 3、全件score 4） |
| `click-control-free-f07-only-global-m24-n3-r1` | `click-f07-only-r1` | 1 | 3 | 1 | 24 | 実行済み・未rating（command evidence照合不能） |
| [`click-control-free-f07-only-global-m24-n3-r2`](click-control-free-f07-only-global-m24-n3-r2.json) | `click-f07-only-r2` | 1 | 3 | 1 | 24 | 完了（3 / 3 score 4） |
| `click-control-free-f07-p-only-global-m24-n3-r1` / `r2` | 対応するonly set | 各1 | 3 | 1 | 24 | 完了（各3 / 3 score 3） |
| [`click-control-free-f07-p-only-global-m24-n3-r3`](click-control-free-f07-p-only-global-m24-n3-r3.json) | `click-f07-p-only-r3` | 1 | 3 | 1 | 24 | 完了（3 / 3 score 4） |
| F08 / F10 / F10-R / A01 / A02の各`only-global-m24-n3-r1` | 対応するonly set | 各1 | 3 | 1 | 24 | 完了（各3 / 3、全件score 4） |
| [`click-control-free-standard14-global-m24-n5-r1`](click-control-free-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-c81-full-standard14-global-m24-n5-r1`](click-c81-full-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-control-free-reasoning-medium-standard14-global-m24-n5-r1`](click-control-free-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | Medium基準完了（70 / 70、全件score 4） |
| [`click-c81-full-reasoning-medium-standard14-global-m24-n5-r1`](click-c81-full-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | Medium水平比較完了（70 / 70、全件score 4） |
| [`click-no-agents-reasoning-medium-standard14-global-m24-n5-r1`](click-no-agents-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-repository-subagents-reasoning-medium-standard14-global-m24-n5-r1`](click-repository-subagents-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-no-agents-reasoning-medium-f10-authority-global-m24-n5-r1`](click-no-agents-reasoning-medium-f10-authority-global-m24-n5-r1.json) | `click-f10-authority-availability-r1` | 1 | 5 | 1 | 24 | 完了（5 / 5 valid、score 1 × 5） |
| [`click-repository-authority-reasoning-medium-f10-authority-global-m24-n5-r1`](click-repository-authority-reasoning-medium-f10-authority-global-m24-n5-r1.json) | `click-f10-authority-availability-r1` | 1 | 5 | 1 | 24 | 完了（5 / 5 valid、score 4 × 5） |
| [`click-no-agents-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-no-agents-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 65 / score 1 × 5） |
| [`click-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 70） |
| [`click-c81-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-c81-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 65 / score 1 × 5） |
| [`click-c81-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-c81-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 70） |
| [`click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-r1`](click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | CLI 0.146.0で完了（70 / 70 valid、score 4 × 65 / score 1 × 5）。CLI 0.144.0のC81とは非互換 |

`B`はprofileのfieldではなく、同一profileを変更せず独立resultとして反復した回数である。P1-cはP1-bと同じ`N=5` profileを変更せず、合計`B=3`として完了した。

F01 profile r1はLayer 2開始前に必須のall-agent token accounting宣言がないことを検出し、runを生成せず停止した。履歴を上書きせず、r2で`token_accounting`とrequired commandのcommand evidence protocolだけを追加した。各profileの一次結果とClick Std14の集約値は[`click results`](../results/README.md)を正本とする。

## 実行環境の固定

`agent_environment`は比較条件であり、次を実測して固定した。

| 項目 | 値 | 根拠 |
| --- | --- | --- |
| `codex_cli` | 既存Click result `0.144.0` / Candidate125 `0.146.0` | 各実行前の`codex --version`実測値。異なるCLIのresultを同一comparisonへ混ぜない |
| `python_version` | `3.14.5` | 共有runtimeの`platform.python_version()` |
| `runtime_identity_sha256` | r1 `e591efde94b1b8cf5901a8e9d71857bbc2abe1740ca9a66eea92fbe2cae13c37` / r2 `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952` | 共有venvの`pip freeze --all`出力のSHA-256。r2は`uv==0.11.32`を追加 |

共有runtimeは`/Users/kenn/repos/_verification/click-prompt-ab-measurement/environment/.venv`に置き、`runtime_links`の`venv_shim`としてworkspaceの`.venv`へmaterializeする。fixture生成元のlocal cloneは`/Users/kenn/repos/click`（target commitでdetach）である。

- 共有venvは`pytest`と、target commitから通常installした`click`を持つ。`click`を入れるのは`importlib.metadata`へversion metadataを供給するためで、実装はgate実行時に`PYTHONPATH=src`でworkspace側の`src`から解決させる。
- `pip install .`は`direct_url.json`を残し、`pip freeze`が`click @ file:///...`という環境依存の行を出す。identityをpath非依存にするため、install後に`direct_url.json`を削除してから`pip freeze --all`を取得した。結果は`click==8.5.0.dev0`である。
- `PYTHONPATH=src`を付けない場合、`tests/test_deprecations.py`が`PackageNotFoundError`でcollection errorになる。`venv_shim`は共有purelibを`.pth`で追加するだけでworkspaceの`src`を通さないため、gate commandへ明示する。
- F07-Pではconsole scriptに依存せず、`UV_CACHE_DIR=.uv-cache .venv/bin/python -m uv lock --check --offline`を使う。Std14の全runはruntime r2へ固定した。

## 実測したgateの挙動

| 条件 | 結果 |
| --- | --- |
| seed未適用（target commit）full gate | `1939 passed, 25 skipped, 1 xfailed` |
| seed適用済みfixture focused gate | `30 failed, 250 passed` |
| seed適用済みfixture full gate | `30 failed, 1909 passed, 25 skipped, 1 xfailed` |

gate実行後もfixtureは`git status`上cleanである（pytestが`.pytest_cache/.gitignore`を自動生成するため、cacheがdriftにならない）。
