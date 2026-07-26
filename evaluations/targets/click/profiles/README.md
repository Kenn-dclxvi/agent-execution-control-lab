# click profiles

target instance `click`のevaluation profileを置く。`M`は指定がない限り24へ固定する。段階ごとのCase / N / B / Mは[`docs/public-target-selection-phase0.md`](../../../../docs/public-target-selection-phase0.md)の「Phase 1の実行設定」を正本とする。

## 現在のprofile

| profile_id | set | Case | N | B | M | 状態 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [`click-control-free-f01-only-global-m24-n1-r1`](click-control-free-f01-only-global-m24-n1-r1.json) | `click-f01-only-r1` | 1 | 1 | 1 | 24 | execution前停止（token accounting宣言不足、result 0件） |
| [`click-control-free-f01-only-global-m24-n1-r2`](click-control-free-f01-only-global-m24-n1-r2.json) | `click-f01-only-r1` | 1 | 1 | 1 | 24 | P1-a完了（valid 1 / 1、score 4） |

`B`はprofileのfieldではなく、同一profileを変更せず反復した回数である。P1-b（`N=5`）とP1-c（`N=5`を`B=3`）は別revisionのprofileとして固定する。

r1はLayer 2開始前に必須のall-agent token accounting宣言がないことを検出し、runを生成せず停止した。履歴を上書きせず、r2で`token_accounting`とrequired commandのcommand evidence protocolだけを追加した。P1-aの一次結果は[`click results`](../results/click-control-free-f01-only-p1a-n1_2026-07-26.md)を正本とする。

## 実行環境の固定

`agent_environment`は比較条件であり、次を実測して固定した。

| 項目 | 値 | 根拠 |
| --- | --- | --- |
| `codex_cli` | `0.144.0` | `codex --version`の実測値 |
| `python_version` | `3.14.5` | 共有runtimeの`platform.python_version()` |
| `runtime_identity_sha256` | `e591efde94b1b8cf5901a8e9d71857bbc2abe1740ca9a66eea92fbe2cae13c37` | 共有venvの`pip freeze --all`出力のSHA-256 |

共有runtimeは`/Users/kenn/repos/_verification/click-prompt-ab-measurement/environment/.venv`に置き、`runtime_links`の`venv_shim`としてworkspaceの`.venv`へmaterializeする。fixture生成元のlocal cloneは`/Users/kenn/repos/click`（target commitでdetach）である。

- 共有venvは`pytest`と、target commitから通常installした`click`を持つ。`click`を入れるのは`importlib.metadata`へversion metadataを供給するためで、実装はgate実行時に`PYTHONPATH=src`でworkspace側の`src`から解決させる。
- `pip install .`は`direct_url.json`を残し、`pip freeze`が`click @ file:///...`という環境依存の行を出す。identityをpath非依存にするため、install後に`direct_url.json`を削除してから`pip freeze --all`を取得した。結果は`click==8.5.0.dev0`である。
- `PYTHONPATH=src`を付けない場合、`tests/test_deprecations.py`が`PackageNotFoundError`でcollection errorになる。`venv_shim`は共有purelibを`.pth`で追加するだけでworkspaceの`src`を通さないため、gate commandへ明示する。

## 実測したgateの挙動

| 条件 | 結果 |
| --- | --- |
| seed未適用（target commit）full gate | `1939 passed, 25 skipped, 1 xfailed` |
| seed適用済みfixture focused gate | `30 failed, 250 passed` |
| seed適用済みfixture full gate | `30 failed, 1909 passed, 25 skipped, 1 xfailed` |

gate実行後もfixtureは`git status`上cleanである（pytestが`.pytest_cache/.gitignore`を自動生成するため、cacheがdriftにならない）。
