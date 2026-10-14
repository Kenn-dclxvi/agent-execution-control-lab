# Claude Code計測でキャッシュの条件を揃える比較方法

## 結論

Claude Codeで制御なしとCandidateの費用を比べるときは、制御なしの側にも、Claude Codeが必ず読み込むroot `CLAUDE.md`を置く。中身は指示を含まない1文（「このリポジトリには、作業の進め方についての追加の指示はありません。」）とし、root `AGENTS.md`に置いて`CLAUDE.md`をそのリンクにする。Clickでは[`click-00e592c-control-free-loaded-instruction-r1`](../evaluations/targets/click/prompts/baselines/click-00e592c-control-free-loaded-instruction-r1/manifest.json)がこの比較元である。

## 何が偏っていたか

[ClickのC316の費用の内訳分析](../evaluations/targets/click/results/click-c316-sonnet55-low-standard14-r4-n5_2026-10-14-cost-analysis.md)で、次のことが分かった。

- root `CLAUDE.md`を読み込む条件では、最初のリクエストでキャッシュから読めるのはシステムとツール定義（6,155トークン）までで、指示文と課題文は毎回書き込みになる。これは2026-10-09〜10-14のすべての計測で同じだった。読み込んだ指示が、runごとに違う絶対パスとともに課題文より前に入るためと推定している。
- root `CLAUDE.md`を読み込まない条件では、2026-10-12までは同じく共有できなかったが、2026-10-14からは、同じケースの2回目以降が課題文までキャッシュから読めるようになった。Claude Codeの版は同じ`2.1.288`で、変わった理由は分からない。
- そのため、10-14以降に制御なし（`CLAUDE.md`を読み込まない）と`CLAUDE.md`を置くCandidateを比べると、同じ課題文を繰り返し流す評価だけで生じる得が、制御なしの側にだけ乗る。直前の計測が1時間以内に同じ課題文を流したかどうかでも、制御なしの費用が変わる。

## 揃え方

どの条件でもroot `CLAUDE.md`を読み込ませれば、どの条件も課題文を毎回書き込む。差は指示文の量と、作業の違いだけになる。読み込む条件が共有できない性質は、10-12以前と10-14以降で変わっていないので、サーバー側の変化にも左右されにくい。直前の計測によるキャッシュの温まり方の違いも、課題文については生じなくなる。

確認した読み込みのふるまい（単発、登録しない。Click F05、各2回）：

| root `CLAUDE.md`の中身 | 読み込まれたか | 課題文までキャッシュから読めたか |
| --- | --- | --- |
| 空（`click-free-claude-md-path-check-20261014-r1`ほか） | 読み込まれない | 読める |
| HTMLコメントだけ（`click-free-comment-probe-20261014-r1`） | 読み込まれない | 読める（2回中1回） |
| 指示を含まない1文（`click-free-sentence-probe-20261014-r1`） | 2回とも読み込まれた | 2回とも読めない |

1文の追加で、最初のリクエストの書き込みは約240トークン増える。

## 守ること

- 比較元の1文は、事実だけを述べ、作業の進め方の指示を含めない。文面を変えるときは新しいbundleとして固定する。
- 制御なしとCandidateの費用の比較には、この比較元を使う。読み込まない比較元（`click-00e592c-control-free-r1`など）との比較は、10-14以降の計測では課題文のキャッシュが偏るので、費用の比較に使わない。
- THE-CAPTIONの系列でも、10-14以降に測るときは同じ偏りが生じる。THE-CAPTIONの制御なし（`the-caption-3ce91a4-control-free-repository-r1`）もroot `CLAUDE.md`は空のリンクで、読み込まれない。THE-CAPTIONでは、ControlFreeRepositoryのroot `AGENTS.md`だけを同じ1文へ置き換えた[`the-caption-3ce91a4-control-free-repository-loaded-instruction-r1`](../prompts/candidates/the-caption-3ce91a4-control-free-repository-loaded-instruction-r1/manifest.json)を比較元とする。単発の診断（`runs/the-caption-free-loaded-path-check-20261014-r1`、Sonnet、F05を2回）で、2件ともroot `CLAUDE.md`が読み込まれ、最初のリクエストの読み取りが6,155で止まることを確かめた。

## 限界

- 読み込んだ指示が課題文より前に入るという説明は推定で、リクエストの本文は保存していない。
- 1文がモデルの振る舞いを変えないことは、品質と費用の計測で確かめる。
