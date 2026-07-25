# 公開target選定 Phase 0 実測記録

[`research-backlog.md`](research-backlog.md)項目10のPhase 0（target選定gate 1〜4による候補の絞り込み）を2026-07-26に実施した記録である。判定の正本はこの文書とする。

**この文書はinstance登録、case作成、評価の実施を意味しない。** 候補の実測と絞り込みだけを扱う。gate全体の定義は[`research-backlog.md`](research-backlog.md)、instance登録手順は[`evaluations/targets/README.md`](../evaluations/targets/README.md)を正本とする。

## 前提の絞り込み条件

executorの`AdapterError`を洗った結果、現行executor（`scripts/run_codex_evaluation.py`）はtargetへ次を要求する。この4点から候補範囲を「Pythonプロジェクトでgit管理されたOSS」へ限定した。

| 依存 | 実測箇所 |
| --- | --- |
| shared Python runtime（`bin/python`とpurelibの検証） | `materialize_shared_venv` |
| workspace Git exclude fileの存在 | `workspace Git exclude file is missing`でfail closed |
| Codex JSONLの`turn.completed` usage | Codex CLI固有のtoken accounting |
| fixture dirty pathsとrun capsuleの一致 | 実行前検証 |

非Python targetはruntime materialize部分の変更が必要になるため、最初の公開instanceでは対象外とした。

## gate 1（license）と概算容量

`gh api repos/<owner>/<name>`で7候補を実測した。全件が再配布可能なlicenseを持ち、容量も許容範囲だった。

| repository | license | size |
| --- | --- | ---: |
| `pallets/click` | BSD-3-Clause | 5,235 KB |
| `pallets/flask` | BSD-3-Clause | 12,008 KB |
| `python-attrs/attrs` | MIT | 5,498 KB |
| `simonw/sqlite-utils` | Apache-2.0 | 2,184 KB |
| `psf/black` | MIT | 8,368 KB |
| `Kludex/uvicorn` | BSD-3-Clause | 5,154 KB |
| `jazzband/pip-tools` | BSD-3-Clause | 4,438 KB |

## gate 7（prompt target collision）と構造

`click` / `flask` / `sqlite-utils`のroot構造を実測した。3件とも`AGENTS.md`と`CLAUDE.md`を持たず、bundle overlayが既存authority fileと衝突しない。`click`と`flask`は`src/` `tests/` `docs/` `examples/`の4領域と`uv.lock`を持ち、`sqlite-utils`はflat packageでlockfileを持たない。

測定感度（gate 5）とlockfileの有無から、実測対象を`click`と`flask`の2件へ絞った。

## gate 2〜4の実測結果

macOSのPython 3.14.5、`python3 -m venv` + `pip install -e . pytest`で実測した。

| 項目 | `pallets/click` | `pallets/flask` |
| --- | --- | --- |
| HEAD | `00e592c`（2026-07-24） | `36e4a824`（2026-05-31） |
| clone容量（`.git`） | 8.0 MB（6.1 MB） | 15 MB（13 MB） |
| 依存package数 | 7 | 13 |
| default gate | `1939 passed, 25 skipped, 1 xfailed` | collection error |
| 所要時間（5回） | 1.81 / 1.83 / 1.83 / 1.89 / 1.90秒 | 未取得 |
| flaky | 5回すべて同一結果 | 未取得 |
| src `.py` / test file / docs file | 17 / 34 / 37 | 24 / 22 / 76 |
| 2026-05-01以降のcommit | 213件 | 8件 |
| `src/`と`tests/`を同時に変更したcommit | 6件以上 | 1件 |

`click`のdefault gateは`pyproject.toml`の`addopts = "-m 'not stress'"`により31,000件のstress testをdeselectする。これはrepository自身が定めたdefault境界であり、`filterwarnings = ["error"]`とあわせて決定性に寄与する。

`flask`の`ImportError: cannot import name 'notset' from '_pytest.monkeypatch'`は、`uv.lock`が固定する`pytest 9.0.3`ではなく最新版を導入したことによる。repository側の欠陥ではないが、gate成立にlockfile準拠のversion pinが必要である。

## 実測で判明した運用条件

- **gate commandはrepository rootをcwdとして実行する必要がある。** `tests/`を絶対pathで指定した初回実行では`tests/test_utils/test__expand_args.py::test_expand_args`が失敗した。この失敗は3回とも決定的に再現したが、cwdをrepository rootへ置くと解消し、5回すべてがpassした。case artifactのgate command定義でcwdを固定する。
- `click`の依存は7 packageで、gate実行時にnetworkを必要としない。依存materializeを済ませたfixtureはoffline実行できる。

## 判定

**`pallets/click`をPhase 1の候補とする。** gate 1〜4に加えて5〜8も満たす。

| gate | 判定 | 根拠 |
| --- | --- | --- |
| 1 license | 通過 | BSD-3-Clause（`LICENSE.txt`、Copyright 2014 Pallets） |
| 2 offline再現性 | 通過 | 依存7 package、gate実行にnetwork不要 |
| 3 容量 | 通過 | 8.0 MB。soft 3 GiBに対し余裕がある |
| 4 gate所要時間 | 通過 | 1.85秒前後。THE-CAPTIONの1 runは数分規模 |
| 5 測定感度 | 通過 | `src/` `tests/` `docs/` `examples/`の4領域、src 17 module |
| 6 天井効果の回避 | 通過 | 2026-05-01以降のcommitが213件あり、新しいseed取得元を選べる |
| 7 prompt target collision | 通過 | `AGENTS.md` / `CLAUDE.md`不在 |
| 8 case供給 | 通過 | `src/`と`tests/`を同時に変更したcommitが2.5か月で6件以上 |
| 9 言語分布 | **不足** | Python単一。既存setのReact / TypeScript（F04型）とshell runner（F07型）は満たせない |

`pallets/flask`は代替候補として保留する。lockfile準拠のversion pinでgateは成立する見込みだが、容量が約2倍、2026-05-01以降のcommitが8件で、case供給の持続性が`click`に劣る。

## 未実測として残る事項

- gate 2の完全なoffline検証（network遮断下でのgate実行）は未実施である。依存数と実行内容からofflineで成立する見込みだが、実測していない。
- gate 9の言語分布は`click`単独では満たせない。Phase 1では既存14項目をそのまま移植せず、Python caseへ縮小した最小setから始める必要がある。
- `flask`のgate所要時間とflaky率は未取得である。

## Phase 1へ渡す条件

1. instance descriptorを`layout: namespaced`で作成し、`evaluations/targets/README.md`の登録済みinstance表へ追記する。
2. seedは2026-05-01以降のcommitから選ぶ。`src/`と`tests/`を同時に変更したcommitを逆patchすると、既存testで検出できる回帰になる。
3. gate commandはrepository rootをcwdとして固定する。
4. 最小1 caseのfixture qualification後、bit-identical bundleで`N=10`のnull calibrationを行う。
5. 既存instance `the-caption`のresultを比較対象にしない。baselineから測り直す。
