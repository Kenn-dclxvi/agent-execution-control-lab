# tests instructions

`tests/`の指示は、評価基盤とrepository contractの回帰検証を扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。

- testは公開contractとschemaの挙動を検証する。
- privateな実装順序や内部関数構造へ過剰に固定しない。
- fixtureやexpected dataを、実装結果へ合わせて無条件に変更しない。
- append-only、identity、compatibility、model-visible境界の回帰を維持する。
- 過去schemaと現行schemaの共存を検証する。
- nonzero exit、計測不完全、外部失敗、品質失敗を別状態として検証する。
- test実行中に生成した一時artifactをrepositoryへ残さない。
- scripts変更時は関連testだけでなく、全test discoveryで回帰を確認する。
- symlink構造を検査するtestまたは検証手段では、checkout環境の表示だけでなくGit tree modeも確認する。

## 検証commandの正本

このリポジトリ自身の回帰検証は、repository rootをcwdとして次のexact commandで実行する。ここに列挙したcommandは`METHOD`および`VALIDATION_PLAN`がbindできる固定値であり、exact commandを解決する目的でrepository evidenceを追加しない。

- 全test discovery: `.venv/bin/python -m pytest -q`
- focused実行: `.venv/bin/python -m pytest <test path> -q`

実行環境は次を満たす。`layer2/`のcodex config処理が`tomllib`へ依存するため、Python 3.10以前ではcollection errorになる。

- Python 3.11以上。`.venv`が無い場合は`python3 -m venv .venv`で作成し、`.venv/bin/python -m pip install pytest`でpytestを導入する。
- `.venv/`は`.gitignore`対象であり、commitしない。

2026-08-07時点の`.venv`（Python 3.14.5 / pytest 9.1.1）での全test discovery結果は`905 passed, 1512 subtests passed`である。この値は環境確認の参考であり、pass conditionはexit code `0`かつcollection errorが無いこととする。
