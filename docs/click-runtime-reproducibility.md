# Click runtime再構築とoffline full gate

## 結論

2026-07-28に、既存の共有venvを使わない空の一時環境からClick評価用known-good runtimeを再構築した。固定target commitと固定package versionを入力にして、既存`requirements.freeze.txt`とbyte単位で同じ8 package identityを再現した。

再構築したruntimeでは、通常条件とprocess単位のnetwork遮断条件の両方でClickのfull gateが同じ結果になった。`uv lock --check --offline`も成功した。既存case、prompt、rating、resultは変更していない。

## 固定した入力

| 項目 | identity |
| --- | --- |
| repository | `https://github.com/pallets/click.git` |
| commit | `00e592cea702e0b2caa0dee42489fdb1c22cd845` |
| tree | `c6aa87f15f2e44a6fcab33714e1eb91e2552d816` |
| Python | `3.14.5` |
| known-good package identity | `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952` |
| uv | `0.11.32` |
| wheel builder | `flit_core==3.12.0` |
| Click wheel SHA-256 | `6ccfe543fe168c5899c1c52ec390cb3467aad7a08072dea1eddd6104e1512b46` |

known-good package identityは、Click評価環境の`requirements.freeze.txt`自体のSHA-256である。内容は`click==8.5.0.dev0`、`iniconfig==2.3.0`、`packaging==26.2`、`pip==26.1.1`、`pluggy==1.6.0`、`Pygments==2.20.0`、`pytest==9.1.1`、`uv==0.11.32`の8件である。

Click repositoryの`uv.lock`だけからこの8 package runtimeを作るわけではない。`uv.lock`は開発用groupを含む81 packageの整合を固定する。一方、評価用known-good runtimeは上の8 packageへ絞った別identityである。runtime再構築には8 packageのfreezeと固定Click sourceを使い、`uv.lock`はF07-Pのdependency pairとoffline整合確認に使う。

## 再構築手順

既存共有venvと既存run workspaceは使用しない。依存準備中だけnetworkを許可する。

```bash
git clone https://github.com/pallets/click.git source
git -C source checkout 00e592cea702e0b2caa0dee42489fdb1c22cd845
python3.14 -m venv runtime
runtime/bin/python -m pip install \
  pip==26.1.1 iniconfig==2.3.0 packaging==26.2 pluggy==1.6.0 \
  Pygments==2.20.0 pytest==9.1.1 uv==0.11.32
python3.14 -m venv build-runtime
build-runtime/bin/python -m pip install pip==26.1.1 flit_core==3.12.0
mkdir wheelhouse
build-runtime/bin/python -m pip wheel \
  --no-build-isolation --no-deps --wheel-dir wheelhouse ./source
runtime/bin/python -m pip install \
  --no-index --no-deps --find-links wheelhouse click==8.5.0.dev0
runtime/bin/python -m pip freeze --all
```

`pip install ./source`を直接使うと、`pip freeze`は一時pathを含む`click @ file:///...`になる。これはpackage内容が同じでもknown-good identityと一致しない。固定sourceからwheelを作り、wheelhouseからpackage名とversionで解決することで`click==8.5.0.dev0`を再現する。

Clickの`pyproject.toml`はbuild dependencyを`flit_core>=3.11,<4`としている。範囲指定のままでは将来別versionが選ばれるため、実測で使われた`3.12.0`をbuild用venvへ固定し、`--no-build-isolation`でwheelを作る。通常のbuild isolationで作ったwheelと、この固定builderで作ったwheelは上表の同じSHA-256になった。build用venvは評価runtimeの8 package identityへ含めない。

## 実測結果

| 検証 | 結果 |
| --- | --- |
| target tree照合 | `c6aa87f15f2e44a6fcab33714e1eb91e2552d816`と一致 |
| `pip freeze --all` | known-good 8 packageとbyte単位で一致 |
| pinned builderでのwheel | 通常buildと同じSHA-256 |
| 通常full gate | `1939 passed, 25 skipped, 31000 deselected, 1 xfailed` |
| network遮断full gate | `1939 passed, 25 skipped, 31000 deselected, 1 xfailed` |
| `uv lock --check --offline` | `Resolved 81 packages` |
| target repository drift | なし |

full gateはrepository rootをcwdとし、`PYTHONPATH=src ../runtime/bin/python -m pytest -q`で実行した。

network遮断はmacOSの`sandbox-exec`で対象processへ`(deny network*)`を適用した。遮断のnegative controlとして同じprofile内の`curl https://github.com`が名前解決失敗になることを先に確認した。Mac全体のnetwork設定は変更していない。

`uv`のoffline確認は、依存準備段階で専用cacheへlock確認に必要な情報をmaterializeした後、同じcacheを使ってnetwork遮断下で実行した。full gate自体は外部通信や追加installを必要としなかった。

## 判定境界

- 事実: 現在host上の空venvで、既存共有venvを参照せず再構築とoffline gateが成功した。
- 推論: 同じmacOS arm64、Python 3.14.5、固定commitを用意できる第三者は、この手順で同じruntimeを再構築できる。
- 未実施: 別の人物または別OS / architectureによる実行は行っていない。platformが変わる場合は新しいruntime identityとして扱う。
- 非対象: model run、標準14再評価、prompt比較、adoption、release、target本体への変更は行っていない。

したがって、現在のClick系列について「lock情報と固定sourceからknown-good runtimeを作る手順」と「依存準備後にnetworkなしでfull gateが通る事実」は確認済みとする。
