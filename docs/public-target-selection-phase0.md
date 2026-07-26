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

## 追加実測: 14項目カバレッジの成立確認（2026-07-26同日）

上の判定でgate 9（言語分布）を「不足」とし、初期setをPython caseへ縮小する前提を置いた。これは**試験の目的を取り違えた判定だった**。正本は[`future-roadmap.md`](future-roadmap.md)で、改善対象は「worker起動、context継承、model再入、read、validation、停止、result binding**などの実行上の判断点**」であり、標準評価setは「既存制御の回帰とcandidate間の互換比較に使う固定基準」である。14項目が担保しているのは題材の網羅ではなく実行判断点の網羅であるため、題材が異なっても同じ判断点を観測できれば成立する。

以下は当時の判定を残したまま、同日に追加実測した結果である。

### 14項目のcoverage対応

各caseの`coverage_tags`（`private/case-data.json`から実測）を軸に、`pallets/click`側の題材を対応させた。

| 元case | カバーする判断点（実測タグ） | click側の題材 | 実証状態 |
| --- | --- | --- | --- |
| F01 | 単一fileのsource実装、不変条件の復元 | `71f2baf`の逆patch（`_compat.py` 6行）→ 30 test失敗 | qualification・評価完了 |
| F02 | 複数file・層をまたぐ実装 | `051725f`の機能部分を2 sourceへseedし、公開・非公開stream API contractを復元 | qualification・N=3完了（3 / 3 score 4） |
| F03 | 例外時cleanup、mocked I/O、原子的保存 | `testing.py`のCliRunner / `isolated_filesystem`。cleanup blockの反転で1 test失敗 | qualification・評価完了 |
| F04 | 入れ子package、呼び出し側から見える出力の条件分岐 | nested Groupのshell completion context | qualification・評価完了 |
| F05 | 曖昧さの確認、変更ゼロ | 並び順policyと適用面が未指定の指示 | 評価完了 |
| F05-OS | 範囲外operationの停止、permission境界 | PyPIへのpublish要求 | 評価完了 |
| F06 | testのみ修正、production変更禁止 | `c52f43c`のtest差分を反転 | qualification・評価完了 |
| F07 | 起動経路の正典化、routing | `pyproject.toml`のdefault tox command | r2でqualification・評価完了 |
| F07-P | 依存制約、対になるfileの整合、provenance | `pyproject.toml`と`uv.lock`の対。workspace-local cacheでoffline検証 | r3でqualification・評価完了 |
| F08 | docsのみ、参照の同期、code変更なし | shell completion docsとPowerShell supportの同期 | qualification・評価完了 |
| F10 | read-onlyの棚卸し、変更ゼロ | command / groupのentry point棚卸し | 評価完了 |
| F10-R | 非破壊review、severity、行根拠 | fixed commitのnested completion review | 評価完了 |
| A01 | 未固定値を推測しない、確認前に編集・試験しない | modeと適用対象が未指定の依頼 | 評価完了 |
| A02 | repositoryから解決できる不足を質問しない | default tox routingをrepositoryから解決 | 評価完了 |

**14項目すべてに対応題材がある。初期setの縮小は不要である。**

### 当初「弱点」と判定した2項目の解消

- **F07**: `tox.ini`が存在しないことから起動経路が実質1つと判定したが、誤りだった。clickはtox設定を`pyproject.toml`の`[tool.tox]`へ置いており、env 9種を持つ。file名ではなく設定の実体を確認する必要があった。
- **F07-P**: `uv`が環境に存在しないため検証手段がないと判定したが、`pip install uv`で導入できる（実測: uv 0.11.32）。`uv lock --check --offline`は整合時に`Resolved 81 packages`を返し、`pyproject.toml`のversion指定を矛盾させると失敗する。ただしoffline実行時の失敗messageはnetwork無効のhintを含むため、case設計では「解決不能」と「network不足」が区別できる不整合の作り方を選ぶ。

### 代替候補の実測

| repository | clone容量（`.git`） | default gate | 判定 |
| --- | --- | --- | --- |
| `psf/black` | 16 MB（9.0 MB） | 未測定（実行時に不正な引数を渡したため） | 保留。`src/`が`black` / `blackd` / `blib2to3`の3 package、`scripts/`にPython script 11本を持つ |
| `jazzband/pip-tools` | 5.8 MB（4.8 MB） | 3回すべて`8 failed, 1014 passed, 5 skipped, 2 xfailed`（32.65 / 33.41 / 36.31秒） | 不適。clean cloneで8件が決定的に失敗し、所要時間がclickの約18倍 |

`click`が全項目で優位のため、代替候補の追加実測は行っていない。

### Phase 1の実行設定

`M`は指定がない限り24へ固定する。実行回数が24未満の段階でも宣言値として固定し、比較条件の一部として扱う。

| 段階 | Case | N | B | M | 実行回数 | 確認対象 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1-a 成立確認 | 1 | 1 | 1 | 24 | 1 | fixture、bundle overlay、gate、token集計 |
| P1-b batch内ばらつき | 1 | 5 | 1 | 24 | 5 | 1 result内のN反復ばらつき |
| P1-c batch間ばらつき（P1-bを含む累計） | 1 | 5 | 3 | 24 | 追加10（累計15） | 独立result 3件の中央値の散らばり（基準線） |
| P1-d以降 case追加 | +1ずつ | 3 | 1 | 24 | 各3 | 追加caseのみ。既存caseは再実行しない |
| Bundle A 標準14 | 14 | 5 | 1 | 24 | 70 | 標準setのbaseline 1 batch |
| 標準14 継続 | 14 | 5 | 18 | 24 | 1,260 | 必要時の継続比較単位 |

case追加時の`N=3`は[`evaluations/cases/README.md`](../evaluations/cases/README.md)の追加手順に合わせた。`B`の比較単位はbatchであり、B個のresult中央値の中央値を比較する（実測: [Candidate41 B18結果](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)）。したがってPhase 1の基準線もB=3でbatch間の散らばりとして取る。

### 後続方針の修正（2026-07-26）

Phase 0時点の「bit-identical bundleでnull calibration」という案は後続方針として採用しない。同一contentでも別bundle identityを作ると、過去試験の影響を受けた別条件のように解釈され、安定性測定とCandidate比較の境界が曖昧になるためである。

- P1-a / P1-b / P1-c、case追加、Click Std14 baselineまでは、同じBundle A `click-00e592c-control-free-r1`を固定する。
- 安定性はcontent-identicalなA / Bではなく、同じBundle A identityの独立result間で測る。
- Bundle Aで標準14項目`N=5`を確立した後、1軸だけを変更した実CandidateをBundle Bとして新規固定する。
- Bundle BはBundle Aと同じ標準14項目、rating、model / reasoning、runtime、Mで水平比較する。

この節が後続実行計画の正本であり、下の「Phase 1へ渡す条件」4に残す当初案を上書きする。

この修正方針どおり、P1-a〜P1-c、14 caseの追加確認、Bundle A Std14まで同一identityで完了した。Std14は70 / 70件がscore `4`で、一次結果は[`click control-free Std14 N=5`](../evaluations/targets/click/results/click-control-free-standard14-n5_2026-07-26.md)を正本とする。次のBundleは1軸を変更する実Candidateとしてのみ作成する。

### 実測中に発生した手順上の失敗

いずれも報告値には反映済みで、最終確認としてclean cloneが`1939 passed`であることを確認している。

- 巻き戻し実験の後始末が不完全で、clean状態のはずのcloneで1件失敗した。cloneを作り直して解消した。
- patch出力のリダイレクトがzshの`noclobber`で拒否され、2件目以降が1件目のpatchを使い回していた。file名を分けて測り直した。

## 未実測として残る事項

- gate 2の完全なoffline検証（network遮断下でのgate実行）は未実施である。依存数と実行内容からofflineで成立する見込みだが、実測していない。
- 当初のgate 9「言語分布不足」は、上の追加実測で実行判断点coverageへ訂正済みである。14項目すべてに対応題材があるため、標準setを縮小する必要はない。
- `flask`のgate所要時間とflaky率は未取得である。

## Phase 1へ渡す条件

1. instance descriptorを`layout: namespaced`で作成し、`evaluations/targets/README.md`の登録済みinstance表へ追記する。
2. seedは2026-05-01以降のcommitから選ぶ。`src/`と`tests/`を同時に変更したcommitを逆patchすると、既存testで検出できる回帰になる。
3. gate commandはrepository rootをcwdとして固定する。
4. 最小1 caseのfixture qualification後、bit-identical bundleで`N=10`のnull calibrationを行う（当初案。上の「後続方針の修正」により不採用）。
5. 既存instance `the-caption`のresultを比較対象にしない。baselineから測り直す。
